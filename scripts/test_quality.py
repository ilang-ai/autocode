#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AutoCode release gate. Standard library only, no network.
Run before every push: python3 scripts/test_quality.py   (exit 1 = do not release)

Covers: every skill has a complete frontmatter whose name matches its folder;
the skill count and the version are the same in every manifest and badge;
agents.json is well-formed; every script compiles; the installer plans,
applies, detects drift, keeps user edits and uninstalls cleanly on a fake
home for linux, darwin and win32; product-study's own selftest passes."""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import contextlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import autocode as ac  # noqa: E402

fails = []


def check(name, cond, detail=""):
    print(("ok   " if cond else "FAIL ") + name + ("" if cond else "  " + str(detail)[:300]))
    if not cond:
        fails.append(name)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def jload(rel):
    return json.loads(read(rel))


@contextlib.contextmanager
def captured():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        yield buf


# ---- skills and frontmatter
skills = ac.source_skills()
check("skills folder has exactly 11 skills (7 stages + 4 cross-cutting)", len(skills) == 11, sorted(skills))
bad_fm = []
for name in skills:
    text = read(os.path.join("skills", name, "SKILL.md"))
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        bad_fm.append(name + ": no frontmatter")
        continue
    fm = dict(re.findall(r"^(\w+):\s*(.*)$", m.group(1), re.M))
    if fm.get("name") != name:
        bad_fm.append("%s: name=%r" % (name, fm.get("name")))
    if not fm.get("description", "").strip():
        bad_fm.append(name + ": empty description")
    if not fm.get("version", "").strip():
        bad_fm.append(name + ": no version")
check("every skill has frontmatter with matching name, description, version", not bad_fm, bad_fm[:5])
no_pycache = [p for p in subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, encoding="utf-8", errors="replace").stdout.splitlines() if "__pycache__" in p or p.endswith(".pyc")]
check("no __pycache__ or .pyc tracked in git", not no_pycache, no_pycache[:3])

# ---- counts and versions across manifests
N = len(skills)
V = ac.VERSION
plugin = jload(".claude-plugin/plugin.json")
market = jload(".claude-plugin/marketplace.json")
cplugin = jload(".cursor-plugin/plugin.json")
cmarket = jload(".cursor-plugin/marketplace.json")
gemini = jload("gemini-extension.json")
versions = {
    "autocode.py": V,
    ".claude-plugin/plugin.json": plugin.get("version"),
    ".claude-plugin/marketplace.json": market["plugins"][0].get("version"),
    ".cursor-plugin/plugin.json": cplugin.get("version"),
    ".cursor-plugin/marketplace.json": cmarket["plugins"][0].get("version"),
    "gemini-extension.json": gemini.get("version"),
    "skills/product-study/SKILL.md": re.search(r"^version:\s*(\S+)", read("skills/product-study/SKILL.md"), re.M).group(1),
    "skills/product-study/scripts/fetch_public.py": re.search(r'^VERSION = "([^"]+)"', read("skills/product-study/scripts/fetch_public.py"), re.M).group(1),
}
readme = read("README.md")
m = re.search(r"badge/version-([\w.\-]+)-", readme)
versions["README.md badge"] = m.group(1).replace("--", "-") if m else None  # shields.io escapes a dash as --
mism = {k: v for k, v in versions.items() if v != V}
check("one version everywhere (%s)" % V, not mism, mism)
counts = {
    "README.md badge": re.search(r"badge/Skills-(\d+)-", readme),
    ".claude-plugin/plugin.json": re.search(r"(\d+) skills", plugin.get("description", "")),
    ".claude-plugin/marketplace.json": re.search(r"(\d+) skills", market["plugins"][0].get("description", "")),
    ".cursor-plugin/plugin.json": re.search(r"(\d+) skills", cplugin.get("description", "")),
    ".cursor-plugin/marketplace.json": re.search(r"(\d+) skills", cmarket["plugins"][0].get("description", "")),
    "gemini-extension.json": re.search(r"(\d+) skills", gemini.get("description", "")),
}
cmism = {k: (m.group(1) if m else None) for k, m in counts.items() if not m or int(m.group(1)) != N}
check("skill count %d everywhere" % N, not cmism, cmism)
if "-pre" not in V:
    cff = re.search(r'^version:\s*"?([^"\s]+)"?', read("CITATION.cff"), re.M).group(1)
    zen = jload(".zenodo.json").get("version")
    check("CITATION.cff and .zenodo.json carry the release version", cff == V and zen == V, (cff, zen))
else:
    print("note pre-release %s: CITATION.cff / .zenodo.json stay at the last stable version by design" % V)

# ---- agents.json
agents = jload("agents.json")["agents"]
ids = [a["id"] for a in agents]
check("agents.json ids unique", len(ids) == len(set(ids)))
req = [a["id"] for a in agents if not all(k in a for k in ("id", "display_name", "verified"))]
check("agents.json entries have id/display_name/verified", not req, req)
ph = re.findall(r"\{(\w+)\}", json.dumps(agents))
check("agents.json uses only known placeholders", set(ph) <= {"home", "appdata", "xdg_config"}, set(ph))
persona = read("persona/AUTOCODE.md")
check("persona uses only known placeholders", set(re.findall(r"\{(\w+)\}", persona)) <= {"skills_dir", "autocode_home"})
check("persona names product-study and the memory file", "product-study" in persona and ".autocode/memory.md" in persona)

# ---- scripts compile
pyfiles = [os.path.join(dp, f) for dp, _, fs in os.walk(ROOT) for f in fs if f.endswith(".py") and ".git" not in dp and "__pycache__" not in dp]
r = subprocess.run([sys.executable, "-I", "-m", "py_compile"] + pyfiles, capture_output=True, encoding="utf-8", errors="replace")
check("all python compiles (%d files)" % len(pyfiles), r.returncode == 0, r.stderr[-300:])
shfiles = [os.path.join(dp, f) for dp, _, fs in os.walk(ROOT) for f in fs if f.endswith(".sh") and ".git" not in dp]
if sys.platform == "win32":
    # On Windows, `bash` on PATH is usually the WSL launcher (no distro => error) and the
    # checkout may be CRLF; the .sh files are POSIX scripts, parsed on the linux/macos jobs.
    check("all shell scripts parse (%d files; skipped on Windows)" % len(shfiles), True)
else:
    bad_sh = [f for f in shfiles if subprocess.run(["bash", "-n", f], capture_output=True).returncode != 0]
    check("all shell scripts parse (%d files)" % len(shfiles), not bad_sh, bad_sh)
for dp, _, fs in os.walk(ROOT):
    pass
shutil.rmtree(os.path.join(ROOT, "__pycache__"), ignore_errors=True)
for dp, ds, _ in os.walk(ROOT):
    for d in ds:
        if d == "__pycache__":
            shutil.rmtree(os.path.join(dp, d), ignore_errors=True)

# ---- product-study selftest
r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "skills", "product-study", "scripts", "selftest.py")], capture_output=True, encoding="utf-8", errors="replace")
check("product-study selftest passes", r.returncode == 0, (r.stdout + r.stderr)[-400:])

# ---- see-it-ship-it: methodology present, S5 runner self-tests, the dino example passes its gates
meth = read("methodology/see-it-ship-it.md")
stage_genes = ["see-it-ship-it", "S1-see", "S2-study", "S3-cut", "S4-build", "S5-verify", "S6-ship", "S7-hand-back"]
check("methodology/see-it-ship-it.md declares the objective and the 8 genes",
      "::OBJECTIVE{id:see-it-ship-it" in meth and all("::GENE{%s|" % g in meth for g in stage_genes),
      [g for g in stage_genes if "::GENE{%s|" % g not in meth])
r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "skills", "product-study", "scripts", "acceptance_run.py"), "--selftest"], capture_output=True, encoding="utf-8", errors="replace")
check("acceptance_run.py (S5-verify) selftest passes", r.returncode == 0, (r.stdout + r.stderr)[-300:])
r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "skills", "judge", "scripts", "f_v5.py"), "--selftest"], capture_output=True, encoding="utf-8", errors="replace")
check("judge: f_v5 reference function reproduces the canonical cases", r.returncode == 0, (r.stdout + r.stderr)[-400:])
no_proto = [s for s in skills if "[PROTOCOL:iLang|v=5.0" not in read(os.path.join("skills", s, "SKILL.md"))]
check("every skill declares the iLang v5.0 protocol line", not no_proto, no_proto)
bad_ex = [s for s in skills if "::EXAMPLE{" in read(os.path.join("skills", s, "SKILL.md"))]
check("no skill uses the unregistered ::EXAMPLE block (use ::SAY{@A→@B}{...})", not bad_ex, bad_ex)
r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "skills", "product-study", "scripts", "blueprint.py"), "check", "dino", "--root", os.path.join(ROOT, "skills", "product-study", "examples")], capture_output=True, encoding="utf-8", errors="replace")
check("examples/dino blueprint passes the product-study gate", r.returncode == 0, (r.stdout + r.stderr)[-400:])
dino_site = os.path.join(ROOT, "skills", "product-study", "examples", "dino", "site")
check("examples/dino ships a rules block and a checks file", '<script id="rules">' in read(os.path.join(dino_site, "index.html")) and os.path.exists(os.path.join(dino_site, "acceptance.js")))
if shutil.which("node"):
    r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "skills", "product-study", "scripts", "acceptance_run.py"), dino_site], capture_output=True, encoding="utf-8", errors="replace")
    check("examples/dino acceptance: every machine check matches (node)", r.returncode == 0 and "8/8" in r.stdout, (r.stdout + r.stderr)[-400:])

# ---- installer scenarios on a fake home
def run(*argv):
    with captured() as out:
        rc = ac.main(list(argv))
    return rc, out.getvalue()


for platform in ("linux", "darwin", "win32"):
    tmp = tempfile.mkdtemp(prefix="autocode-gate-")
    try:
        os.makedirs(os.path.join(tmp, ".codex"))
        with open(os.path.join(tmp, ".codex", "AGENTS.md"), "w", encoding="utf-8") as f:
            f.write("# mine\n\nkeep this line\n")
        base = ["--home", tmp, "--platform", platform]
        rc, out = run(*base, "setup", "--dry-run")
        check("[%s] dry-run plans codex and writes nothing" % platform, rc == 0 and "codex" in out and "nothing written" in out and not os.path.exists(os.path.join(tmp, ".codex", "skills")), out[-300:])
        rc, out = run(*base, "setup", "--yes")
        check("[%s] setup applies" % platform, rc == 0 and os.path.isdir(os.path.join(tmp, ".codex", "skills", "product-study")), out[-300:])
        rc, out = run(*base, "doctor")
        check("[%s] doctor healthy after setup" % platform, rc == 0 and "needs attention" not in out, out[-300:])
        rc, out = run(*base, "setup", "--yes")
        check("[%s] second setup is a no-op" % platform, rc == 0 and "nothing to do" in out, out[-200:])
        agents_md = open(os.path.join(tmp, ".codex", "AGENTS.md"), encoding="utf-8").read()
        check("[%s] user's own rules kept above the block" % platform, agents_md.startswith("# mine\n\nkeep this line") and agents_md.count(ac.BEGIN) == 1)
        # upgrade from an older version: two skills we installed back then are no longer shipped
        man_path = os.path.join(tmp, ".autocode", "installed.json")
        man = json.load(open(man_path, encoding="utf-8"))
        old_untouched = os.path.join(tmp, ".codex", "skills", "old-untouched"); os.makedirs(old_untouched)
        open(os.path.join(old_untouched, "SKILL.md"), "w", encoding="utf-8").write("old\n")
        old_edited = os.path.join(tmp, ".codex", "skills", "old-edited"); os.makedirs(old_edited)
        open(os.path.join(old_edited, "SKILL.md"), "w", encoding="utf-8").write("old\n")
        man["clients"]["codex"]["skills"]["old-untouched"] = {"path": old_untouched, "sha": ac.sha_tree(old_untouched)}
        man["clients"]["codex"]["skills"]["old-edited"] = {"path": old_edited, "sha": ac.sha_tree(old_edited)}
        json.dump(man, open(man_path, "w", encoding="utf-8"))
        open(os.path.join(old_edited, "SKILL.md"), "a", encoding="utf-8").write("user tweak\n")
        rc, out = run(*base, "doctor")
        check("[%s] doctor reports skills left over from an older version" % platform, rc == 1 and "old-untouched" in out, out[-300:])
        rc, out = run(*base, "setup", "--yes")
        check("[%s] setup retires the untouched old skill and leaves the edited one" % platform,
              rc == 0 and not os.path.exists(old_untouched) and os.path.exists(old_edited) and "retire" in out, out[-400:])
        man = json.load(open(man_path, encoding="utf-8"))
        check("[%s] retired skill is forgotten, edited one still recorded" % platform,
              "old-untouched" not in man["clients"]["codex"]["skills"] and "old-edited" in man["clients"]["codex"]["skills"])
        # user edits an installed skill
        edited = os.path.join(tmp, ".codex", "skills", "hand-back", "SKILL.md")
        with open(edited, "a", encoding="utf-8") as f:
            f.write("\nmy tweak\n")
        rc, out = run(*base, "doctor")
        check("[%s] doctor flags an edited skill" % platform, rc == 1 and "hand-back" in out, out[-300:])
        rc, out = run(*base, "setup", "--dry-run")
        check("[%s] setup treats the edited skill as a conflict, not an overwrite" % platform, "conflict" in out and "1 skill folder" in out, out[-400:])
        rc, out = run(*base, "setup", "--yes", "--force")
        check("[%s] --force overwrites and backs up the edited skill" % platform, rc == 0 and "my tweak" not in open(edited, encoding="utf-8").read() and os.path.isdir(os.path.join(tmp, ".autocode", "backups", "codex", "skills")), out[-300:])
        with open(edited, "a", encoding="utf-8") as f:
            f.write("\nmy tweak again\n")
        rc, out = run(*base, "uninstall", "--yes")
        check("[%s] uninstall removes our skills, keeps the edited one, strips the block" % platform,
              rc == 0 and not os.path.exists(os.path.join(tmp, ".codex", "skills", "product-study")) and os.path.exists(edited)
              and ac.BEGIN not in open(os.path.join(tmp, ".codex", "AGENTS.md"), encoding="utf-8").read()
              and "keep this line" in open(os.path.join(tmp, ".codex", "AGENTS.md"), encoding="utf-8").read(), out[-300:])
        if platform == "win32":
            ctx = ac.Context(tmp, "win32")
            oc = [a for a in agents if a["id"] == "opencode"][0]
            p = ac.agent_paths(oc, ctx)
            check("[win32] xdg_config resolves under AppData/Roaming", "AppData" in p["marker"] and "Roaming" in p["marker"], p)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

print("%d failure(s)" % len(fails))
sys.exit(1 if fails else 0)
