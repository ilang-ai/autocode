#!/usr/bin/env python3
"""Run a build's acceptance checks and print the table the user sees.

    python3 acceptance_run.py <site_dir>                 # against the local build
    python3 acceptance_run.py <site_dir> --url <live>    # against the page actually served at the URL
    python3 acceptance_run.py --selftest

Convention (the fixed part of S5-verify): next to the build lives a checks file,
`acceptance.js` (run with node) or `acceptance.py` (run with python3). It receives one
argument, the path of the HTML to check, and prints one JSON object per line:

    {"id": "5", "check": "自动加速 1000 次更新后速度", "expected": "7.000", "actual": "7.000", "ok": true}

Any other stdout lines are ignored. This script renders the rows as
check / expected / actual / match, adds a one-line verdict, and exits 1 on any mismatch,
so go-live can refuse to proceed. With --url it first fetches the live HTML (and waits
for it to carry the build's rules block, `<script id="rules">`), so what is verified is
what people will actually open, not the local file. Python 3.8+, standard library.
"""
import argparse, json, os, subprocess, sys, tempfile, time, urllib.request

for _stream in (sys.stdout, sys.stderr):  # Windows consoles default to cp1252; the table has CJK and ✓
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass


def width(s):
    return sum(2 if ord(c) > 255 else 1 for c in str(s))


def pad(s, n):
    return str(s) + " " * max(0, n - width(s))


def fetch_live(url, tries=30, wait=10):
    last = ""
    for _ in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=15) as r:
                html = r.read().decode("utf-8", "replace")
                if r.status == 200 and '<script id="rules">' in html:
                    return html
                last = "status %s, rules block %s" % (r.status, "present" if '<script id="rules">' in html else "missing")
        except Exception as e:  # noqa: BLE001 - any network error is a retry
            last = str(e)
        time.sleep(wait)
    raise SystemExit("live page not ready after %d tries: %s (%s)" % (tries, url, last))


def find_checks(site_dir):
    for name, runner in (("acceptance.js", "node"), ("acceptance.py", sys.executable)):
        p = os.path.join(site_dir, name)
        if os.path.exists(p):
            return p, runner
    return None, None


def run_checks(checks, runner, html_path):
    r = subprocess.run([runner, checks, html_path], capture_output=True, encoding="utf-8", errors="replace")
    rows = []
    for line in (r.stdout or "").splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                d = json.loads(line)
                rows.append({"id": str(d.get("id", "")), "check": str(d.get("check", "")), "expected": str(d.get("expected", "")),
                             "actual": str(d.get("actual", "")), "ok": bool(d.get("ok"))})
            except ValueError:
                pass
    return rows, r.returncode, (r.stderr or "").strip()


def render(rows, title):
    w = [3, max(10, max((width(r["check"]) for r in rows), default=0) + 2), max(8, max((width(r["expected"]) for r in rows), default=0) + 2),
         max(8, max((width(r["actual"]) for r in rows), default=0) + 2)]
    out = [title, pad("#", w[0]) + pad("检查 check", w[1]) + pad("预期 expected", w[2]) + pad("实际 actual", w[3]) + "结果"]
    for r in rows:
        out.append(pad(r["id"], w[0]) + pad(r["check"], w[1]) + pad(r["expected"], w[2]) + pad(r["actual"], w[3]) + ("✓ 一致" if r["ok"] else "✗ 不一致"))
    bad = sum(1 for r in rows if not r["ok"])
    out.append("")
    out.append("%d/%d 一致 (%d/%d match)%s" % (len(rows) - bad, len(rows), len(rows) - bad, len(rows), "" if not bad else "，%d 项不一致，先修再上线" % bad))
    return "\n".join(out), bad


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("site_dir", nargs="?")
    ap.add_argument("--url", help="verify the page served at this URL instead of the local index.html")
    ap.add_argument("--html", default="index.html", help="local file to check (default index.html)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.site_dir:
        ap.print_help()
        return 1
    site = os.path.abspath(a.site_dir)
    checks, runner = find_checks(site)
    if not checks:
        print("no acceptance.js / acceptance.py next to the build in %s — S5-verify has nothing to run; write one before go-live" % site)
        return 2
    if a.url:
        html = fetch_live(a.url)
        fd, html_path = tempfile.mkstemp(suffix=".html"); os.close(fd)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        title = "验收 · 线上 %s" % a.url
    else:
        html_path = os.path.join(site, a.html)
        title = "验收 · 本地 %s" % a.html
    try:
        rows, rc, err = run_checks(checks, runner, html_path)
    finally:
        if a.url:
            os.remove(html_path)
    if not rows:
        print("checks file ran (exit %d) but printed no JSON rows%s" % (rc, (": " + err[:300]) if err else ""))
        return 2
    text, bad = render(rows, title)
    print(text)
    return 1 if bad else 0


def selftest():
    """No node, no network: a python checks file against a stub page."""
    d = tempfile.mkdtemp()
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write('<html><script id="rules">var START=6;</script></html>')
    with open(os.path.join(d, "acceptance.py"), "w", encoding="utf-8") as f:
        f.write("import json,sys\nh=open(sys.argv[1],encoding='utf-8').read()\n"
                "print(json.dumps({'id':'1','check':'rules block present','expected':'yes','actual':'yes' if 'id=\"rules\"' in h else 'no','ok':'id=\"rules\"' in h}))\n"
                "print(json.dumps({'id':'2','check':'start speed','expected':'6','actual':'6','ok':True}))\n")
    rows, rc, _ = run_checks(os.path.join(d, "acceptance.py"), sys.executable, os.path.join(d, "index.html"))
    text, bad = render(rows, "selftest")
    ok = len(rows) == 2 and bad == 0 and "2/2" in text
    # a failing row must make the verdict non-zero
    rows2 = rows + [{"id": "3", "check": "x", "expected": "1", "actual": "2", "ok": False}]
    _, bad2 = render(rows2, "selftest")
    ok = ok and bad2 == 1
    print("acceptance_run selftest: %s" % ("ok" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
