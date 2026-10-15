#!/usr/bin/env python3
"""AutoCode go-live, target: GitHub Pages (static, zero cost). S6-ship of the see-it-ship-it methodology.

Takes a folder with index.html and ends with a public URL the user can send to
anyone. Python 3.8+ standard library. Talks to GitHub only through `gh`, so the
user's password never passes through AutoCode: `gh auth login --web` shows an
8-character code and the user approves it in their own browser.

    python3 go_live_pages.py <site_dir> --name dino-runner [--yes] [--simulate]

--simulate : mock the GitHub side (no account needed): every gh/git call is
             printed instead of run, and a local static server stands in for
             <owner>.github.io so the "verify live" and "acceptance" steps run
             for real against a served copy of the site.

What the user sees is printed with a leading ">> "; everything else is the log.
"""
import argparse, http.server, json, os, shutil, socket, subprocess, sys, threading, time, urllib.request

for _stream in (sys.stdout, sys.stderr):  # Windows consoles default to cp1252
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

SAY = lambda s: print(">> " + s, flush=True)
LOG = lambda s: print("   " + s, flush=True)


class GitHub:
    """Thin wrapper over gh/git. In simulate mode nothing leaves the machine."""

    def __init__(self, simulate):
        self.simulate = simulate
        self.calls = []
        self._logged_in = False

    def run(self, *cmd, check=True, capture=True):
        self.calls.append(" ".join(cmd))
        if self.simulate:
            LOG("$ " + " ".join(cmd) + "   (simulated)")
            return self._fake(cmd)
        LOG("$ " + " ".join(cmd))
        r = subprocess.run(cmd, capture_output=capture, encoding="utf-8", errors="replace")
        if check and r.returncode != 0:
            raise RuntimeError((r.stderr or r.stdout).strip())
        return (r.stdout or "").strip()

    # --- simulated answers, shaped like the real ones -------------------
    def _fake(self, cmd):
        c = " ".join(cmd)
        if c.startswith("gh auth status"):
            if os.environ.get("SIM_NEW_USER") and not self._logged_in:
                return "You are not logged in to any GitHub hosts."
            return "github.com\n  ✓ Logged in to github.com account demo-user"
        if c.startswith("gh auth login"):
            self._logged_in = True
            LOG("gh 会显示：! First copy your one-time code: AB12-CD34")
            LOG("gh 会显示：Open this URL to continue in your web browser: https://github.com/login/device")
            LOG("(用户在浏览器贴代码、点 Authorize，gh 收到授权后继续)")
            return ""
        if c.startswith("gh api user"):
            return json.dumps({"login": "demo-user"})
        if "repos/" in c and c.endswith("/pages") and "-X POST" in c:
            return json.dumps({"status": None, "html_url": "https://demo-user.github.io/REPO/"})
        if "repos/" in c and c.endswith("/pages"):
            return json.dumps({"status": "built", "html_url": "https://demo-user.github.io/REPO/"})
        return ""


def have(cmd):
    return shutil.which(cmd) is not None


def step_detect(gh):
    """Case A: no gh → install (one line, our decision). Case B: gh but not logged in → device login.
    Case C: no GitHub account → send the user to sign up, then device login."""
    SAY("先看看你的电脑上有没有连到 GitHub。")
    if not gh.simulate and not have("gh"):
        SAY("需要装一个小工具 gh（GitHub 官方命令行），我来装，不用你操作。")
        if sys.platform == "darwin" and have("brew"):
            gh.run("brew", "install", "gh")
        elif sys.platform.startswith("win") and have("winget"):
            gh.run("winget", "install", "--id", "GitHub.cli", "-e")
        else:
            SAY("这台机器我装不了 gh，请打开 https://cli.github.com 点下载安装，装好回来说一声。")
            return False
    status = gh.run("gh", "auth", "status", check=False)
    if "Logged in" in status:
        login = json.loads(gh.run("gh", "api", "user"))["login"]
        SAY("已经连上 GitHub，账号是 %s。" % login)
        return login
    SAY("还没连上 GitHub。你有 GitHub 账号吗？没有的话先注册，免费的：")
    SAY("  1. 打开 https://github.com/signup")
    SAY("  2. 填邮箱、设密码、起个用户名，按提示验证邮箱")
    SAY("  3. 回来告诉我「注册好了」")
    SAY("有账号就直接下一步：我会给你一串 8 位代码，浏览器会打开 GitHub，你把代码贴进去点「Authorize」就行。")
    gh.run("gh", "auth", "login", "--web", "--git-protocol", "https", capture=False)
    login = json.loads(gh.run("gh", "api", "user"))["login"]
    SAY("连上了，账号是 %s。" % login)
    return login


def step_confirm(name, yes):
    """The one question: the site and its files will be public (free Pages needs a public repo)."""
    SAY("我会在你的 GitHub 建一个叫「%s」的公开仓库，把游戏放进去，开通网页托管。" % name)
    SAY("公开的意思是：任何拿到链接的人都能打开游戏，也能看到这个 HTML 文件。免费托管只能这样。可以吗？[y/n]")
    if yes:
        LOG("(--yes) 用户已同意")
        return True
    ans = input().strip().lower()
    return ans in ("y", "yes", "是", "可以", "好")


def step_push(gh, site_dir, name, login):
    SAY("正在上传……")
    work = os.path.join(site_dir, ".autocode-deploy")
    if os.path.exists(work):
        shutil.rmtree(work)
    os.makedirs(work)
    for f in os.listdir(site_dir):
        if f.startswith(".") or f.endswith(".py") or f == "acceptance.js":
            continue
        src = os.path.join(site_dir, f)
        if os.path.isfile(src):
            shutil.copy(src, os.path.join(work, f))
    open(os.path.join(work, ".nojekyll"), "w").close()  # serve files as-is
    cwd = os.getcwd()
    os.chdir(work)
    try:
        gh.run("git", "init", "-q", "-b", "main")
        gh.run("git", "add", "-A")
        gh.run("git", "-c", "user.name=AutoCode", "-c", "user.email=autocode@users.noreply.github.com",
               "commit", "-q", "-m", "go-live: first version")
        gh.run("gh", "repo", "create", name, "--public", "--source=.", "--push", "--disable-wiki", "--disable-issues")
    finally:
        os.chdir(cwd)
    return work


def step_enable_pages(gh, login, name):
    SAY("开通网页托管，等它生成……")
    body = json.dumps({"source": {"branch": "main", "path": "/"}})
    gh.run("gh", "api", "-X", "POST", "repos/%s/%s/pages" % (login, name), "--input", "-", check=False) if gh.simulate else \
        subprocess.run(["gh", "api", "-X", "POST", "repos/%s/%s/pages" % (login, name), "--input", "-"],
                       input=body, encoding="utf-8", errors="replace", capture_output=True)
    url = "https://%s.github.io/%s/" % (login, name)
    for i in range(30):
        info = json.loads(gh.run("gh", "api", "repos/%s/%s/pages" % (login, name), check=False) or "{}")
        if info.get("status") == "built":
            return info.get("html_url", url).replace("REPO", name)
        time.sleep(0 if gh.simulate else 10)
    raise RuntimeError("GitHub Pages 5 分钟内没有生成完成")


def step_verify_live(url):
    for i in range(30):
        try:
            with urllib.request.urlopen(url, timeout=10) as r:
                html = r.read().decode("utf-8", "replace")
                if r.status == 200 and "<script id=\"rules\">" in html:
                    return html
        except Exception:
            pass
        time.sleep(0.2 if "127.0.0.1" in url else 10)
    raise RuntimeError("网址打不开：" + url)


def step_acceptance(site_dir, url):
    """S5 on the live page: the acceptance runner fetches the served HTML itself."""
    runner = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "product-study", "scripts", "acceptance_run.py")
    if not os.path.exists(runner):
        return None, "acceptance_run.py not found; skipped"
    r = subprocess.run([sys.executable, runner, site_dir, "--url", url], capture_output=True, encoding="utf-8", errors="replace")
    return r.returncode == 0, (r.stdout or r.stderr).strip()


# --- simulate mode: a local server standing in for <owner>.github.io ------
def serve_as_pages(work_dir, name):
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    root = os.path.join(work_dir, "..", ".pages-root"); shutil.rmtree(root, ignore_errors=True)
    shutil.copytree(work_dir, os.path.join(root, name), ignore=shutil.ignore_patterns(".git"))
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=root, **k)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return "http://127.0.0.1:%d/%s/" % (port, name), httpd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site_dir"); ap.add_argument("--name", required=True)
    ap.add_argument("--yes", action="store_true"); ap.add_argument("--simulate", action="store_true")
    a = ap.parse_args()
    site = os.path.abspath(a.site_dir)
    if not os.path.exists(os.path.join(site, "index.html")):
        sys.exit("no index.html in " + site)
    gh = GitHub(a.simulate)

    login = step_detect(gh)
    if not login:
        return 1
    if not step_confirm(a.name, a.yes):
        SAY("好，那先不上线。文件在 %s，什么时候想发再说。" % site)
        return 0
    work = step_push(gh, site, a.name, login)
    url = step_enable_pages(gh, login, a.name)
    httpd = None
    if a.simulate:
        sim_url, httpd = serve_as_pages(work, a.name)
        LOG("simulate: %s  ->  %s" % (url, sim_url))
        url_to_check = sim_url
    else:
        url_to_check = url
    SAY("网址生成了，我去打开确认一下……")
    step_verify_live(url_to_check)
    ok, table = step_acceptance(site, url_to_check)
    print(); print(table); print()
    if ok is None:
        ok = True
    if httpd:
        httpd.shutdown()
    SAY("上线了：%s" % url)
    SAY("这个链接谁都能打开。验收表里机器能查的%s；剩下的请你亲手按 mvp.md 验收表里的动作点一遍。" %
        ("全部一致" if ok else "有不一致，我先修再重新上线"))
    SAY("想改什么直接说，改完我重新上线，网址不变。")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
