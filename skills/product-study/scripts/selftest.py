#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline regression for product-study (the release gate runs this; locally:
python3 skills/product-study/scripts/selftest.py). Standard library only, no
external network: a throwaway HTTP server on 127.0.0.1 plays the "product site".

Covers: robots.txt refusal, login/account path refusal, redirect-to-login
refusal, non-text refusal, de-duplication, discover ranking, blueprint init /
check / sources / mvp, and every gate rule (tags, sources, verbatim copy,
assets, code blocks, MVP size)."""
import http.server
import io
import json
import os
import shutil
import sys
import tempfile
import threading
import contextlib

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch_public as fp  # noqa: E402
import blueprint as bp     # noqa: E402

fp.PER_HOST_DELAY = 0
fails = []


def check(name, cond, detail=""):
    print(("ok   " if cond else "FAIL ") + name + ("" if cond else "  " + str(detail)[:300]))
    if not cond:
        fails.append(name)


@contextlib.contextmanager
def captured():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        yield buf


PAGES = {
    "/robots.txt": ("text/plain", "User-agent: *\nDisallow: /secret/\n"),
    "/": ("text/html", """<html><head><title>Acme Tracker – issues for teams</title>
<meta name="description" content="Track issues fast"></head><body><nav><a href="/pricing">Pricing</a>
<a href="/docs/">Docs</a><a href="/login">Log in</a><a href="/changelog">Changelog</a><a href="https://docs.acme.test/start">Guide</a>
<a href="/secret/plan">Secret</a></nav><h1>Acme Tracker</h1><p>Acme Tracker is a keyboard-first issue tracker where every issue belongs to exactly one team and optionally to one project. Cycles are fixed-length sprints that teams opt into.</p>
<script>var x = "should not appear";</script></body></html>"""),
    "/pricing": ("text/html", "<html><head><title>Pricing</title></head><body><h1>Pricing</h1><h3>Free</h3><p>Up to 250 issues and unlimited members on the free plan. The Business plan adds SSO and audit logs for twelve dollars per user per month.</p>" + "<p>filler text to pass the minimum length threshold. </p>" * 10 + "</body></html>"),
    "/changelog": ("text/html", "<html><head><title>Changelog</title></head><body><h1>Changelog</h1>" + "<p>Release note entry about cycles and projects. </p>" * 12 + "</body></html>"),
    "/dup": ("text/html", "<html><head><title>Pricing</title></head><body><h1>Pricing</h1><h3>Free</h3><p>Up to 250 issues and unlimited members on the free plan. The Business plan adds SSO and audit logs for twelve dollars per user per month.</p>" + "<p>filler text to pass the minimum length threshold. </p>" * 10 + "</body></html>"),
    "/secret/plan": ("text/html", "<html><body>" + "robots should keep this out " * 20 + "</body></html>"),
    "/login": ("text/html", "<html><body>" + "login page " * 40 + "</body></html>"),
    "/docs/": ("text/html", "<html><head><title>Docs</title></head><body><h1>Concepts</h1><h2>Workspace</h2><h2>Team</h2><h2>Issue</h2>" + "<p>Each workspace has teams; each team owns issues. </p>" * 8 + "<table><tr><th>Plan</th><th>Teams</th></tr><tr><td>Free</td><td>2</td></tr></table><pre>const secretImplementation = 1;</pre></body></html>"),
    "/brochure.pdf": ("application/pdf", "%PDF-1.4 not a text page"),
    "/thin": ("text/html", "<html><body><div id=app></div></body></html>"),
}


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/members":
            self.send_response(302)
            self.send_header("Location", "/login")
            self.end_headers()
            return
        if path not in PAGES:
            self.send_response(404)
            self.end_headers()
            return
        ctype, body = PAGES[path]
        data = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", ctype + ("; charset=utf-8" if ctype.startswith("text") else ""))
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


def main():
    srv = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d" % port
    tmp = tempfile.mkdtemp(prefix="product-study-selftest-")
    try:
        root = os.path.join(tmp, "study")
        # ---- discover
        with captured() as out:
            rc = fp.main(["discover", base + "/"])
        lines = out.getvalue().splitlines()
        check("discover runs", rc == 0, out.getvalue())
        check("discover ranks pricing", any(l.startswith(base + "/pricing") for l in lines))
        check("discover finds docs path", any(l.startswith(base + "/docs") for l in lines))
        check("discover keeps docs subdomain", any("docs.acme.test" in l for l in lines))
        check("discover drops login", not any("/login" in l for l in lines))
        check("discover drops robots-blocked secret", not any("/secret" in l for l in lines))
        # ---- fetch
        urls = [base + p for p in ("/", "/pricing", "/secret/plan", "/login", "/members", "/brochure.pdf", "/dup", "/thin", "/docs/", "/changelog")]
        with captured() as out:
            rc = fp.main(["fetch", "acme", "--root", root] + urls)
        text = out.getvalue()
        idx = json.load(open(os.path.join(root, "acme", "sources.json"), encoding="utf-8"))
        ids = [s["id"] for s in idx["sources"]]
        skipped = {s["url"].replace(base, ""): s["reason"] for s in idx["skipped"]}
        check("fetch collects public pages", ids == ["S1", "S2", "S3", "S4"], (ids, text))
        check("robots-disallowed path refused", "robots" in skipped.get("/secret/plan", ""), skipped)
        check("login path refused", "login" in skipped.get("/login", ""), skipped)
        check("redirect-to-login refused", "redirected" in skipped.get("/members", ""), skipped)
        check("pdf refused", "not a text page" in skipped.get("/brochure.pdf", ""), skipped)
        check("thin JS page refused", "readable text" in skipped.get("/thin", ""), skipped)
        check("duplicate content stored once", "same content as S2" in text, text)
        s1 = open(os.path.join(root, "acme", "sources", "S1.txt"), encoding="utf-8").read()
        check("script text dropped from extraction", "should not appear" not in s1)
        check("outline recorded", "## outline" in s1 and "# Acme Tracker" in s1)
        check("header has url/sha/date", all(k in s1 for k in ("url:", "sha256:", "fetched_at:")))
        s3 = open(os.path.join(root, "acme", "sources", "S3.txt"), encoding="utf-8").read()
        check("table cells joined with | ", "Plan | Teams" in s3 and "Free | 2" in s3, s3[-300:])
        check("code blocks omitted from sources", "secretImplementation" not in s3 and "code omitted" in s3)
        with captured() as out:
            rc = fp.main(["links", "acme", "--root", root, "S1", "--grep", "pricing"])
        check("links command lists same-site links of a page", rc == 0 and "/pricing" in out.getvalue(), out.getvalue())
        with captured() as out:
            rc = fp.main(["fetch", "acme", "--root", root, base + "/pricing"])
        check("re-fetch of same url is a no-op", "already collected as S2" in out.getvalue())
        # ---- blueprint init / check on template
        with captured():
            rc = bp.main(["init", "acme", "--root", root, "--product", "Acme Tracker", "--site", base, "--goal", "issue tracker for a ten-person team"])
        bpath = os.path.join(root, "acme", "blueprint.md")
        check("init writes blueprint", rc == 0 and os.path.exists(bpath))
        with captured() as out:
            rc = bp.main(["check", "acme", "--root", root])
        check("fresh template fails the gate (TODOs)", rc == 1 and "FAIL no TODO" in out.getvalue())
        with captured() as out:
            rc = bp.main(["mvp", "acme", "--root", root])
        check("mvp refuses unfinished section 9", rc == 1)
        # ---- a good blueprint passes
        good = GOOD.replace("{base}", base)
        with open(bpath, "w", encoding="utf-8") as f:
            f.write(good)
        with captured():
            bp.main(["sources", "acme", "--root", root])
        with captured() as out:
            rc = bp.main(["check", "acme", "--root", root])
        check("good blueprint passes the gate", rc == 0, out.getvalue())
        with captured():
            rc = bp.main(["mvp", "acme", "--root", root])
        mvp = open(os.path.join(root, "acme", "mvp.md"), encoding="utf-8").read()
        check("mvp.md written with objects and no-copy list", rc == 0 and "**Objects" in mvp and "Interface look" in mvp)
        check("Sources section lists refused urls", "Refused or skipped" in open(bpath, encoding="utf-8").read())

        # ---- each gate rule bites
        def gate_fails(mutation, needle, name):
            with open(bpath, "w", encoding="utf-8") as f:
                f.write(mutation(good))
            with captured() as out:
                rc = bp.main(["check", "acme", "--root", root])
            check(name, rc == 1 and needle in out.getvalue(), out.getvalue()[-400:])

        gate_fails(lambda t: t.replace("- Teams own issues; a project groups issues across teams [S1] {high}", "- Teams own issues; a project groups issues across teams [S1]"), "confidence tag", "claim without confidence tag fails")
        gate_fails(lambda t: t.replace("[S1] {high}", "{high}", 1), "cites a source", "high claim without source fails")
        gate_fails(lambda t: t.replace("[S1] {high}", "[S99] {high}", 1), "exists in sources.json", "unknown source id fails")
        gate_fails(lambda t: t.replace("- Teams own issues; a project groups issues across teams [S1] {high}", "- Acme Tracker is a keyboard-first issue tracker where every issue belongs to exactly one team and optionally to one project [S1] {high}"), "verbatim", "verbatim sentence from a source fails")
        gate_fails(lambda t: t.replace("## 2. Information architecture", "## 2. Information architecture\n\n- Logo at " + base + "/logo.png [S1] {high}"), "image/logo", "image link fails")
        gate_fails(lambda t: t.replace("## 5. Technical stack clues", "## 5. Technical stack clues\n\n```\n" + "x = 1\n" * 20 + "```"), "code block", "long code block fails")
        gate_fails(lambda t: t.replace("**Objects (<= 5):** Team, Issue, Project, Cycle, Comment", "**Objects (<= 5):** Team, Issue, Project, Cycle, Comment, Label"), "objects", "six MVP objects fail")
        gate_fails(lambda t: t.replace("1. Scaffold", "x. Scaffold").replace("2. Issue", "x. Issue"), "build order", "missing build steps fail")
        gate_fails(lambda t: t.replace("| Pricing is per user per month | SaaS | S2 | high |", "| Pricing is per user per month | SaaS | S2 | |"), "confidence tag", "table row without confidence fails")
    finally:
        srv.shutdown()
        shutil.rmtree(tmp, ignore_errors=True)
    print("%d failure(s)" % len(fails))
    return 1 if fails else 0


GOOD = """# Product blueprint: Acme Tracker

Product: Acme Tracker · Official site: {base} · Studied on: 2026-10-13 · Goal: issue tracker for a ten-person team

Reading guide: structure only, from public pages.

## 0. Summary

Acme Tracker is an issue tracker built around teams, with optional projects and fixed-length cycles, priced per user with a free tier.

## 1. Feature inventory

| Feature | What it does (one line) | Tier | Sources | Confidence |
|---|---|---|---|---|
| Issues per team | Every issue lives in one team | core | S1 | high |
| Cycles | Fixed-length iterations a team can turn on | plus | S1, S4 | medium |

## 2. Information architecture

- Teams own issues; a project groups issues across teams [S1] {high}
- Workspace holds teams, docs outline shows workspace, team, issue nesting [S3] {high}

## 3. Core objects and data model (inferred)

| Object | Key fields | Relations | Sources | Confidence |
|---|---|---|---|---|
| Issue | title, status, priority | belongs to one team, optional project | S1, S3 | medium |

## 4. Key user flows

- Flow A: create team -> create issue -> move through statuses [S3] {medium}

## 5. Technical stack clues

- No public stack information found; nothing to record {guess}

## 6. Pricing and business model

| Plan | Price | What it unlocks | Sources | Confidence |
|---|---|---|---|---|
| Free | 0 | up to 250 issues, unlimited members | S2 | high |
| Pricing is per user per month | SaaS | S2 | high |

## 7. Integrations and ecosystem

- No integrations page was public at study time {guess}

## 8. Gaps and differentiation opportunities

- Small teams may want a flat free tier without the issue cap {guess}

## 9. MVP cut

**Users and the one job:** a ten-person software team tracking its own issues

**Objects (<= 5):** Team, Issue, Project, Cycle, Comment

**Screens (<= 7):** login, team list, issue list, issue detail, project page, cycle page, settings

**Dropped from v1 and why:** integrations, SSO, audit logs: not needed for ten people

**Build order (each step ends in something the user can click):**
1. Scaffold with auth and the team list
2. Issue list and detail with statuses
3. Projects and cycles

**Acceptance (v1 is done when):**
- a member can sign in and see their team
- an issue can be created, moved to done, and commented on
- a cycle shows its open and closed issues

## 10. What we will not copy

- Interface look, layout, colors, icons and typography of the original: we design our own.
- Copy, screenshots, images, logo, product and feature names that are trademarks.
- Any code from the original's repositories or bundles.
- Anything that was not on a public page.

## Sources
"""

if __name__ == "__main__":
    sys.exit(main())
