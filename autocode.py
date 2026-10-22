#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AutoCode installer: put the skills and the persona into any supported agent.

Standard library only, Python 3.8+. Reads agents.json next to this file.
Three verbs, in the order you use them:

  python3 autocode.py setup      [--client ID ...] [--dry-run] [--yes]
      Detect installed agents (or take --client), show the plan (which files
      will be created or changed, where the backups go), ask once, apply.
  python3 autocode.py doctor     [--client ID ...] [--json]
      Read-only. For each agent: present? skills installed and unchanged?
      persona block present and current? Exit 1 if anything is unhealthy.
  python3 autocode.py uninstall  [--client ID ...] [--yes]
      Remove only what setup installed (recorded in ~/.autocode/installed.json).
      A skill you edited after install is kept and reported, never deleted.
  python3 autocode.py clients
      List the agents in agents.json and whether each is detected here.

Options for tests and unusual layouts: --home DIR (pretend this is the home
directory), --platform win32|darwin|linux (pretend this is the OS).

What setup writes, per agent:
  <skills_dir>/<skill>/...            a copy of each folder under skills/
  <persona_file>                      one managed block between the markers
                                      <!-- autocode:begin --> and <!-- autocode:end -->;
                                      the rest of the file is untouched; a backup
                                      is taken first
  ~/.autocode/bin/scan-secrets.sh     the pre-deploy secret scan
  ~/.autocode/installed.json          the record uninstall and doctor work from
"""
import argparse
import datetime
import hashlib
import io
import json
import os
import shutil
import stat
import sys

VERSION = "6.2.2"
HERE = os.path.dirname(os.path.abspath(__file__))
AGENTS_FILE = os.path.join(HERE, "agents.json")
SKILLS_SRC = os.path.join(HERE, "skills")
PERSONA_SRC = os.path.join(HERE, "persona", "AUTOCODE.md")
SCAN_SRC = os.path.join(HERE, "scripts", "scan-secrets.sh")
BEGIN, END = "<!-- autocode:begin", "<!-- autocode:end -->"


# ------------------------------------------------------------------ paths

class Context:
    def __init__(self, home=None, platform=None):
        self.home = os.path.abspath(home or os.path.expanduser("~"))
        self.platform = platform or sys.platform
        env = os.environ
        if self.platform == "win32":
            self.appdata = env.get("APPDATA") if not home else os.path.join(self.home, "AppData", "Roaming")
            self.appdata = self.appdata or os.path.join(self.home, "AppData", "Roaming")
            self.xdg_config = self.appdata
        else:
            self.xdg_config = (env.get("XDG_CONFIG_HOME") if not home else None) or os.path.join(self.home, ".config")
            self.appdata = self.xdg_config
        self.autocode_home = os.path.join(self.home, ".autocode")
        self.manifest_path = os.path.join(self.autocode_home, "installed.json")

    def resolve(self, template):
        if not template:
            return None
        p = template.replace("{home}", self.home).replace("{appdata}", self.appdata).replace("{xdg_config}", self.xdg_config)
        return os.path.normpath(p)


def load_agents():
    with open(AGENTS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return data["agents"]


def agent_paths(agent, ctx):
    spec = dict(agent)
    override = (agent.get("paths") or {}).get("win32" if ctx.platform == "win32" else "darwin" if ctx.platform == "darwin" else "linux")
    if override:
        spec.update(override)
    return {
        "marker": ctx.resolve(spec.get("marker")),
        "skills_dir": ctx.resolve(spec.get("skills_dir")),
        "persona_file": ctx.resolve(spec.get("persona_file")),
    }


def detected(agent, ctx):
    p = agent_paths(agent, ctx)
    return bool(p["marker"]) and os.path.isdir(p["marker"])


def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sha_tree(path):
    """Hash of a skill folder: relative paths + contents, so edits anywhere show."""
    h = hashlib.sha256()
    for root, dirs, files in os.walk(path):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        for name in sorted(files):
            if name.endswith(".pyc"):
                continue
            full = os.path.join(root, name)
            h.update(os.path.relpath(full, path).replace(os.sep, "/").encode("utf-8"))
            h.update(b"\0")
            h.update(sha_file(full).encode("ascii"))
            h.update(b"\n")
    return h.hexdigest()


def make_writable(path):
    """Clear a read-only bit. On Windows this clears the read-only attribute; on POSIX it adds owner write."""
    try:
        os.chmod(path, os.stat(path).st_mode | stat.S_IWUSR)
    except OSError:
        pass


def make_dirs_writable(path):
    """After copytree: a checkout that lives in a synced or read-only folder carries the read-only
    attribute on its directories, and copytree (copystat) would carry it into the agent's skills
    folder; a read-only directory cannot be removed on Windows (WinError 5). Files keep their bits."""
    for root, dirs, _ in os.walk(path):
        make_writable(root)


def remove_tree(path):
    """shutil.rmtree for a skill folder whose directories may be read-only (see make_dirs_writable):
    every directory and file is made writable first, top down, so the removal cannot stop halfway."""
    for root, dirs, files in os.walk(path):
        make_writable(root)
        for name in files:
            make_writable(os.path.join(root, name))
    shutil.rmtree(path)


def source_skills():
    out = []
    for name in sorted(os.listdir(SKILLS_SRC)):
        d = os.path.join(SKILLS_SRC, name)
        if os.path.isdir(d) and os.path.exists(os.path.join(d, "SKILL.md")):
            out.append(name)
    return out


def persona_block(ctx, skills_dir):
    with open(PERSONA_SRC, encoding="utf-8") as f:
        body = f.read().strip()
    body = body.replace("{skills_dir}", skills_dir or "<your agent's skills folder>").replace("{autocode_home}", ctx.autocode_home)
    return "%s v%s -->\n%s\n%s" % (BEGIN, VERSION, body, END)


def split_block(text):
    """Return (before, block, after); block is '' when absent."""
    i = text.find(BEGIN)
    if i < 0:
        return text, "", ""
    j = text.find(END, i)
    if j < 0:
        return text, "", ""
    j += len(END)
    return text[:i], text[i:j], text[j:]


def load_manifest(ctx):
    if os.path.exists(ctx.manifest_path):
        with open(ctx.manifest_path, encoding="utf-8") as f:
            return json.load(f)
    return {"version": VERSION, "clients": {}}


def save_manifest(ctx, m):
    os.makedirs(ctx.autocode_home, exist_ok=True)
    with open(ctx.manifest_path, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)


def backup(ctx, client_id, path):
    if not os.path.exists(path):
        return None
    bdir = os.path.join(ctx.autocode_home, "backups", client_id)
    os.makedirs(bdir, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = os.path.join(bdir, "%s.%s" % (os.path.basename(path), stamp))
    shutil.copy2(path, dest)
    return dest


# ------------------------------------------------------------------ plan

def plan_client(agent, ctx, manifest):
    p = agent_paths(agent, ctx)
    cid = agent["id"]
    rec = manifest["clients"].get(cid, {})
    steps = []
    if not p["skills_dir"]:
        steps.append(("manual", "skills", agent.get("notes", "copy skills/ by hand")))
    else:
        for name in source_skills():
            dest = os.path.join(p["skills_dir"], name)
            src_sha = sha_tree(os.path.join(SKILLS_SRC, name))
            if not os.path.exists(dest):
                steps.append(("create", "skill", dest, src_sha))
            else:
                ours = rec.get("skills", {}).get(name)
                cur = sha_tree(dest)
                if cur == src_sha:
                    steps.append(("keep", "skill", dest, src_sha))
                elif ours and ours.get("sha") == cur:
                    steps.append(("update", "skill", dest, src_sha))
                else:
                    steps.append(("conflict", "skill", dest, src_sha))
        # skills we installed earlier that this version no longer ships (merged or renamed):
        # remove them if untouched, leave them (and say so) if the user edited them
        current = set(source_skills())
        for name, info in sorted(rec.get("skills", {}).items()):
            if name in current:
                continue
            dest = info.get("path") or os.path.join(p["skills_dir"], name)
            if not os.path.isdir(dest):
                steps.append(("forget", "skill", dest, None))
            elif sha_tree(dest) == info.get("sha"):
                steps.append(("retire", "skill", dest, None))
            else:
                steps.append(("retire-edited", "skill", dest, None))
    if not p["persona_file"]:
        steps.append(("manual", "persona", agent.get("notes", "paste persona/AUTOCODE.md into the agent's rules")))
    else:
        block = persona_block(ctx, p["skills_dir"])
        if os.path.exists(p["persona_file"]):
            with open(p["persona_file"], encoding="utf-8", errors="replace") as f:
                text = f.read()
            _, old, _ = split_block(text)
            if old == block:
                steps.append(("keep", "persona", p["persona_file"]))
            elif old:
                steps.append(("replace-block", "persona", p["persona_file"]))
            else:
                steps.append(("append-block", "persona", p["persona_file"]))
        else:
            steps.append(("create", "persona", p["persona_file"]))
    scan_dest = os.path.join(ctx.autocode_home, "bin", "scan-secrets.sh")
    if os.path.exists(scan_dest) and sha_file(scan_dest) == sha_file(SCAN_SRC):
        steps.append(("keep", "tool", scan_dest))
    else:
        steps.append(("create" if not os.path.exists(scan_dest) else "update", "tool", scan_dest))
    return p, steps


def print_plan(agent, steps, ctx):
    print("== %s (%s)%s" % (agent["display_name"], agent["id"], "" if agent.get("verified") else "  [path conventions unverified: confirm in the agent's docs]"))
    counts = {}
    for s in steps:
        counts[(s[0], s[1])] = counts.get((s[0], s[1]), 0) + 1
    for (act, kind), n in sorted(counts.items()):
        if kind == "skill":
            print("   %-13s %d skill folder(s)" % (act, n))
    for s in steps:
        if s[1] != "skill":
            print("   %-13s %s: %s" % (s[0], s[1], s[2]))
        elif s[0] == "conflict":
            print("   %-13s %s  (exists, not installed by AutoCode or edited since: left alone; use --force to overwrite)" % (s[0], s[2]))
        elif s[0] == "retire":
            print("   %-13s %s  (this version merged it into another skill; removed, backup kept)" % (s[0], s[2]))
        elif s[0] == "retire-edited":
            print("   %-13s %s  (merged into another skill, but you edited it: left in place; delete it yourself when ready)" % (s[0], s[2]))
    print("   backups of changed files go to %s" % os.path.join(ctx.autocode_home, "backups", agent["id"]))


def apply_plan(agent, p, steps, ctx, manifest, force):
    cid = agent["id"]
    rec = manifest["clients"].setdefault(cid, {"skills": {}, "persona": None, "installed_at": None})
    for s in steps:
        act, kind = s[0], s[1]
        if kind == "skill":
            dest, src_sha = s[2], s[3]
            name = os.path.basename(dest)
            if act in ("create", "update") or (act == "conflict" and force):
                if os.path.exists(dest):
                    backup_dir = os.path.join(ctx.autocode_home, "backups", cid, "skills")
                    os.makedirs(backup_dir, exist_ok=True)
                    shutil.move(dest, os.path.join(backup_dir, "%s.%s" % (name, datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))))
                shutil.copytree(os.path.join(SKILLS_SRC, name), dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                make_dirs_writable(dest)
                rec["skills"][name] = {"path": dest, "sha": src_sha}
            elif act == "keep":
                rec["skills"][name] = {"path": dest, "sha": src_sha}
            elif act == "retire":
                backup_dir = os.path.join(ctx.autocode_home, "backups", cid, "skills")
                os.makedirs(backup_dir, exist_ok=True)
                shutil.move(dest, os.path.join(backup_dir, "%s.%s" % (name, datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))))
                rec["skills"].pop(name, None)
            elif act == "forget":
                rec["skills"].pop(name, None)
            # retire-edited: left in place and still recorded, so doctor keeps mentioning it
        elif kind == "persona" and act != "manual":
            path = s[2]
            block = persona_block(ctx, p["skills_dir"])
            if act == "keep":
                rec["persona"] = {"path": path, "sha": hashlib.sha256(block.encode("utf-8")).hexdigest()}
                continue
            b = backup(ctx, cid, path)
            if os.path.exists(path):
                with open(path, encoding="utf-8", errors="replace") as f:
                    text = f.read()
                before, old, after = split_block(text)
                if old:
                    new = before + block + after
                else:
                    new = text.rstrip("\n") + ("\n\n" if text.strip() else "") + block + "\n"
            else:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                new = block + "\n"
            with open(path, "w", encoding="utf-8") as f:
                f.write(new)
            rec["persona"] = {"path": path, "sha": hashlib.sha256(block.encode("utf-8")).hexdigest(), "backup": b}
        elif kind == "tool" and act != "keep":
            os.makedirs(os.path.dirname(s[2]), exist_ok=True)
            shutil.copy2(SCAN_SRC, s[2])
    rec["installed_at"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rec["version"] = VERSION
    rec["skills_dir"] = p["skills_dir"]
    manifest["version"] = VERSION


# ------------------------------------------------------------------ commands

def select_clients(args, ctx, agents, need_detected=True):
    if args.client:
        wanted = []
        for cid in args.client:
            m = [a for a in agents if a["id"] == cid]
            if not m:
                sys.exit("unknown client %r; see: autocode.py clients" % cid)
            wanted.append(m[0])
        return wanted
    found = [a for a in agents if a["id"] != "generic" and detected(a, ctx)]
    if not found and need_detected:
        print("no supported agent detected under %s; name one with --client (see: autocode.py clients)" % ctx.home)
    return found


def cmd_clients(args, ctx, agents):
    for a in agents:
        p = agent_paths(a, ctx)
        print("%-12s %-36s %s%s" % (a["id"], a["display_name"], "detected" if detected(a, ctx) else ("manual" if not p["marker"] else "not found"),
                                     "" if a.get("verified") else "  (unverified paths)"))
        if a.get("notes"):
            print("             %s" % a["notes"])
    return 0


def cmd_setup(args, ctx, agents):
    chosen = select_clients(args, ctx, agents)
    if not chosen:
        return 1
    manifest = load_manifest(ctx)
    plans = []
    print("AutoCode %s setup plan (home: %s, platform: %s)" % (VERSION, ctx.home, ctx.platform))
    for a in chosen:
        p, steps = plan_client(a, ctx, manifest)
        print_plan(a, steps, ctx)
        plans.append((a, p, steps))
    changes = sum(1 for _, _, steps in plans for s in steps if s[0] in ("create", "update", "replace-block", "append-block", "retire", "forget") or (s[0] == "conflict" and args.force))
    if args.dry_run:
        print("dry run: %d change(s) would be made, nothing written" % changes)
        return 0
    if changes == 0:
        print("nothing to do: everything is already installed and current")
        return 0
    if not args.yes:
        try:
            ans = input("apply %d change(s)? [y/N] " % changes).strip().lower()
        except EOFError:
            ans = ""
        if ans not in ("y", "yes"):
            print("aborted, nothing written")
            return 1
    for a, p, steps in plans:
        apply_plan(a, p, steps, ctx, manifest, args.force)
    save_manifest(ctx, manifest)
    print("done: %d change(s) applied; record in %s" % (changes, ctx.manifest_path))
    for a, p, steps in plans:
        for s in steps:
            if s[0] == "manual":
                print("manual step for %s (%s): %s" % (a["display_name"], s[1], s[2]))
    print("restart the agent so it reloads skills and instructions; then: python3 autocode.py doctor")
    return 0


def cmd_doctor(args, ctx, agents):
    manifest = load_manifest(ctx)
    chosen = select_clients(args, ctx, agents, need_detected=False)
    if not chosen:
        chosen = [a for a in agents if a["id"] in manifest["clients"]]
    report = {"version": VERSION, "python": sys.version.split()[0], "home": ctx.home, "platform": ctx.platform, "clients": []}
    healthy_all = True
    py_ok = sys.version_info >= (3, 8)
    if not py_ok:
        healthy_all = False
    for a in chosen:
        p = agent_paths(a, ctx)
        rec = manifest["clients"].get(a["id"])
        checks = []

        def c(name, ok, fix=""):
            checks.append({"check": name, "ok": bool(ok), "fix": fix if not ok else ""})

        c("agent directory present", not p["marker"] or os.path.isdir(p["marker"]), "install or run the agent once so %s exists" % p["marker"])
        c("setup record present", bool(rec), "run: python3 autocode.py setup --client %s" % a["id"])
        extra = []
        if p["skills_dir"]:
            missing, changed = [], []
            for name in source_skills():
                dest = os.path.join(p["skills_dir"], name)
                src_sha = sha_tree(os.path.join(SKILLS_SRC, name))
                if not os.path.isdir(dest):
                    missing.append(name)
                elif sha_tree(dest) != src_sha:
                    changed.append(name)
            c("all %d skills installed" % len(source_skills()), not missing, "missing %s; run setup" % ", ".join(missing[:5]))
            stale = [n for n in rec.get("skills", {}) if n not in source_skills() and os.path.isdir(rec["skills"][n].get("path", ""))]
            untouched, edited = [], []
            for n in stale:
                info = rec["skills"][n]
                if info.get("sha") and sha_tree(info["path"]) != info["sha"]:
                    edited.append(n)  # user touched it: setup left it in place on purpose
                else:
                    untouched.append(n)  # pristine (or no recorded hash): still a failure
            c("no skills left over from an older version", not untouched, "%s merged into other skills; run setup to retire them" % ", ".join(untouched[:5]))
            extra = ["kept from an older version because you edited it: %s (delete the folder yourself when ready)" % n for n in edited]
            c("installed skills match this version", not changed, "differs: %s; run setup to update (your edits are backed up)" % ", ".join(changed[:5]))
        if p["persona_file"]:
            present, current = False, False
            if os.path.exists(p["persona_file"]):
                with open(p["persona_file"], encoding="utf-8", errors="replace") as f:
                    _, old, _ = split_block(f.read())
                present = bool(old)
                current = old == persona_block(ctx, p["skills_dir"])
            c("persona block present in %s" % os.path.basename(p["persona_file"]), present, "run setup")
            c("persona block is current (v%s)" % VERSION, current, "run setup to refresh the block")
        scan = os.path.join(ctx.autocode_home, "bin", "scan-secrets.sh")
        c("secret scan installed", os.path.exists(scan) and sha_file(scan) == sha_file(SCAN_SRC), "run setup")
        healthy = all(x["ok"] for x in checks)
        healthy_all = healthy_all and healthy
        report["clients"].append({"id": a["id"], "display_name": a["display_name"], "verified_paths": bool(a.get("verified")),
                                  "healthy": healthy, "paths": p, "checks": checks, "extra": extra, "notes": a.get("notes", "")})
    report["healthy"] = healthy_all
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("AutoCode doctor %s  python %s  %s" % (VERSION, report["python"], "ok" if py_ok else "FAIL: Python 3.8+ required"))
        for cl in report["clients"]:
            print("== %s: %s%s" % (cl["display_name"], "healthy" if cl["healthy"] else "needs attention", "" if cl["verified_paths"] else "  [unverified path conventions]"))
            for x in cl["checks"]:
                print("   %s %s%s" % ("ok  " if x["ok"] else "FAIL", x["check"], ("  -> " + x["fix"]) if x["fix"] else ""))
            for n in cl.get("extra", []):
                print("   %s %s" % ("note ", n))
        if not report["clients"]:
            print("no agents to check: run setup, or name one with --client")
    return 0 if healthy_all and report["clients"] else 1


def cmd_uninstall(args, ctx, agents):
    manifest = load_manifest(ctx)
    chosen = select_clients(args, ctx, agents, need_detected=False) if args.client else [a for a in agents if a["id"] in manifest["clients"]]
    if not chosen:
        print("nothing recorded as installed")
        return 0
    actions = []
    for a in chosen:
        rec = manifest["clients"].get(a["id"])
        if not rec:
            print("%s: no setup record, nothing to remove" % a["id"])
            continue
        for name, info in rec.get("skills", {}).items():
            path = info["path"]
            if not os.path.isdir(path):
                continue
            if sha_tree(path) == info["sha"]:
                actions.append(("remove-skill", a["id"], path))
            else:
                actions.append(("keep-edited", a["id"], path))
        if rec.get("persona") and os.path.exists(rec["persona"]["path"]):
            actions.append(("remove-block", a["id"], rec["persona"]["path"]))
    for act in actions:
        print("   %-13s %s" % (act[0], act[2]))
    todo = [x for x in actions if x[0] != "keep-edited"]
    if not todo:
        print("nothing to remove")
    elif not args.yes:
        try:
            ans = input("remove %d item(s)? [y/N] " % len(todo)).strip().lower()
        except EOFError:
            ans = ""
        if ans not in ("y", "yes"):
            print("aborted, nothing removed")
            return 1
    for act, cid, path in todo:
        if act == "remove-skill":
            remove_tree(path)
            parent = os.path.dirname(path)
            if os.path.isdir(parent) and not os.listdir(parent):
                try:
                    os.rmdir(parent)  # an empty skills folder we filled is not worth leaving behind
                except OSError:
                    pass  # not ours to force; an empty folder is harmless
        elif act == "remove-block":
            backup(ctx, cid, path)
            with open(path, encoding="utf-8", errors="replace") as f:
                before, old, after = split_block(f.read())
            new = (before.rstrip("\n") + ("\n" if before.strip() else "") + after.lstrip("\n")) if old else before + after
            if new.strip():
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new if new.endswith("\n") else new + "\n")
            else:
                os.remove(path)
    for a in chosen:
        manifest["clients"].pop(a["id"], None)
    save_manifest(ctx, manifest)
    kept = [x for x in actions if x[0] == "keep-edited"]
    if kept:
        print("kept %d edited skill folder(s) (not ours to delete): %s" % (len(kept), ", ".join(os.path.basename(x[2]) for x in kept)))
    print("uninstalled; backups stay under %s" % os.path.join(ctx.autocode_home, "backups"))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--home", help="pretend this is the home directory (tests)")
    ap.add_argument("--platform", choices=["win32", "darwin", "linux"], help="pretend this is the OS (tests)")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("setup"); s.add_argument("--client", action="append"); s.add_argument("--dry-run", action="store_true")
    s.add_argument("--yes", action="store_true"); s.add_argument("--force", action="store_true", help="overwrite skill folders that were not installed by AutoCode")
    d = sub.add_parser("doctor"); d.add_argument("--client", action="append"); d.add_argument("--json", action="store_true")
    u = sub.add_parser("uninstall"); u.add_argument("--client", action="append"); u.add_argument("--yes", action="store_true")
    sub.add_parser("clients")
    args = ap.parse_args(argv)
    if not args.cmd:
        ap.print_help()
        return 1
    ctx = Context(args.home, args.platform)
    agents = load_agents()
    return {"setup": cmd_setup, "doctor": cmd_doctor, "uninstall": cmd_uninstall, "clients": cmd_clients}[args.cmd](args, ctx, agents)


if __name__ == "__main__":
    sys.exit(main())
