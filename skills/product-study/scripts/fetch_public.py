#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AutoCode product-study: collect PUBLIC source material about a product.

Standard library only (Python 3.8+). No login, no cookies, no auth headers,
no bundle/minified-code reading, no network capture. Honors robots.txt,
skips login/account/billing paths, rate-limits one request per second per
host, caps page count and size. Everything it writes lands under
<root>/<slug>/ (default root: .autocode/study).

Usage:
  fetch_public.py discover <homepage_url> [--max 40]
      Print candidate public pages found on the homepage (pricing, docs,
      changelog, API, integrations, security, careers ...). Nothing is saved.
  fetch_public.py fetch <slug> <url> [<url> ...] [--max-pages 25] [--root DIR]
      Fetch the listed pages, extract text + outline, save as S1.txt, S2.txt ...
      and record them in sources.json. Re-running appends; duplicates are skipped.
  fetch_public.py github <slug> <owner/repo> [--root DIR]
      Record a public GitHub repository: metadata (if the API is reachable),
      README and LICENSE from raw.githubusercontent.com. Flags copyleft licenses.
  fetch_public.py list <slug> [--root DIR]
      Show what has been collected so far.
  fetch_public.py links <slug> S3 [--grep docs] [--root DIR]
      Print the same-site links recorded when S3 was fetched (no network): use it
      to walk a docs navigation without re-fetching pages.

Exit status: 0 ok, 1 nothing collected / bad arguments, 2 every URL was refused.
"""
import argparse
import datetime
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser

VERSION = "6.2.1"
USER_AGENT = "autocode-product-study/%s (+https://github.com/ilang-ai/autocode; public pages only)" % VERSION
DEFAULT_ROOT = os.path.join(".autocode", "study")
MAX_BYTES = 3 * 1024 * 1024
TIMEOUT = 20
PER_HOST_DELAY = 1.0

# Paths that mean "this is someone's account, not public product material".
# A product page behind these is out of scope by design, not a bug.
PRIVATE_PATH = re.compile(
    r"/(login|log-in|signin|sign-in|signup|sign-up|register|auth|oauth|sso|"
    r"account|accounts|dashboard|admin|console|checkout|billing|settings|"
    r"workspace|my|me|user|users/[^/]+/private)(/|$|\?)",
    re.I,
)
ALLOWED_TYPES = ("text/html", "application/xhtml", "text/plain", "text/markdown", "application/json")

# Keywords that mark a public page worth reading, in priority order.
DISCOVER_KEYWORDS = [
    ("pricing", 100), ("plans", 90), ("docs", 95), ("documentation", 95), ("developers", 90),
    ("api", 85), ("changelog", 90), ("releases", 85), ("updates", 70), ("whats-new", 70),
    ("features", 90), ("product", 80), ("integrations", 85), ("security", 75),
    ("enterprise", 60), ("customers", 55), ("compare", 70), ("vs", 50), ("templates", 60),
    ("help", 65), ("support", 55), ("faq", 65), ("roadmap", 70), ("method", 50),
    ("about", 50), ("careers", 60), ("jobs", 60), ("blog", 45), ("terms", 40), ("privacy", 40),
    ("import", 50), ("mobile", 45), ("desktop", 45),
]
DOC_SUBDOMAINS = ("docs", "developers", "developer", "help", "support", "api", "learn", "guide", "guides")


class TextExtractor(HTMLParser):
    """HTML -> plain text + outline (h1-h3) + links. Drops script/style/svg."""

    SKIP = {"script", "style", "noscript", "svg", "template", "iframe", "canvas", "pre", "code"}
    BLOCK = {"p", "div", "section", "article", "li", "ul", "ol", "br", "tr",
             "table", "h1", "h2", "h3", "h4", "h5", "h6", "header", "footer", "nav",
             "main", "aside", "pre", "blockquote", "dd", "dt", "dl", "hr", "figure"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.outline = []
        self.links = []
        self.title = ""
        self.description = ""
        self._skip = 0
        self._title = False
        self._heading = None
        self._heading_buf = []

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            if tag in ("pre", "code") and self._skip == 0:
                self.parts.append(" [code omitted: the study records structure, never the original's code] ")
            self._skip += 1
            return
        a = dict(attrs)
        if tag in ("td", "th"):
            self.parts.append("\t")
        if tag == "title":
            self._title = True
        elif tag == "meta" and (a.get("name") or "").lower() == "description":
            self.description = (a.get("content") or "").strip()
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag in ("h1", "h2", "h3"):
            self._heading = tag
            self._heading_buf = []
        if tag in self.BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self._skip = max(0, self._skip - 1)
            return
        if tag == "title":
            self._title = False
        elif tag in ("h1", "h2", "h3") and self._heading == tag:
            text = " ".join("".join(self._heading_buf).split())
            if text:
                self.outline.append((tag, text))
            self._heading = None
        if tag in self.BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if self._skip:
            return
        if self._title:
            self.title += data
        if self._heading:
            self._heading_buf.append(data)
        self.parts.append(data)

    def text(self):
        raw = "".join(self.parts)
        lines = [" ".join(line.replace("\t", " | ").split()).strip("| ").strip() if "\t" in line else " ".join(line.split()) for line in raw.splitlines()]
        out, blank = [], 0
        for line in lines:
            if line:
                out.append(line)
                blank = 0
            else:
                blank += 1
                if blank == 1:
                    out.append("")
        return "\n".join(out).strip()


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def normalize_url(url):
    p = urllib.parse.urlsplit(url.strip())
    path = re.sub(r"/+$", "", p.path) or "/"
    return urllib.parse.urlunsplit((p.scheme.lower(), p.netloc.lower(), path, p.query, ""))


def registrable(host):
    parts = host.split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else host


class Fetcher:
    def __init__(self, log=print):
        self._robots = {}
        self._last = {}
        self.log = log

    def _wait(self, host):
        last = self._last.get(host)
        if last is not None:
            gap = PER_HOST_DELAY - (time.time() - last)
            if gap > 0:
                time.sleep(gap)
        self._last[host] = time.time()

    def _raw_get(self, url, accept="text/html,text/plain;q=0.9,*/*;q=0.5"):
        host = urllib.parse.urlsplit(url).netloc
        self._wait(host)
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
        resp = urllib.request.urlopen(req, timeout=TIMEOUT)
        body = resp.read(MAX_BYTES + 1)
        truncated = len(body) > MAX_BYTES
        return resp, body[:MAX_BYTES], truncated

    def robots_allows(self, url):
        p = urllib.parse.urlsplit(url)
        base = "%s://%s" % (p.scheme, p.netloc)
        rp = self._robots.get(base)
        if rp is None:
            rp = urllib.robotparser.RobotFileParser()
            try:
                resp, body, _ = self._raw_get(base + "/robots.txt", accept="text/plain,*/*;q=0.5")
                ctype = resp.headers.get("Content-Type", "")
                if resp.status == 200 and "html" not in ctype.lower():
                    rp.parse(body.decode("utf-8", "replace").splitlines())
                else:
                    rp.parse([])  # no usable robots.txt -> everything allowed
            except urllib.error.HTTPError as e:
                if e.code in (401, 403):
                    rp.parse(["User-agent: *", "Disallow: /"])  # treat a locked robots.txt as "stay out"
                else:
                    rp.parse([])
            except Exception:
                rp.parse([])
            self._robots[base] = rp
        return rp.can_fetch(USER_AGENT, url) and rp.can_fetch("*", url)

    def refuse_reason(self, url):
        p = urllib.parse.urlsplit(url)
        if p.scheme not in ("http", "https"):
            return "not http(s)"
        if PRIVATE_PATH.search(p.path + "?"):
            return "login/account/billing path: not public product material"
        if not self.robots_allows(url):
            return "robots.txt disallows this path"
        return None

    def fetch_page(self, url):
        """Return (record, text) or (record_with_error, None)."""
        rec = {"url": url, "fetched_at": now_iso()}
        reason = self.refuse_reason(url)
        if reason:
            rec["status"] = "skipped"
            rec["reason"] = reason
            return rec, None
        try:
            resp, body, truncated = self._raw_get(url)
        except urllib.error.HTTPError as e:
            rec["status"] = "skipped"
            rec["reason"] = "HTTP %d" % e.code + (" (requires permission: out of scope)" if e.code in (401, 402, 403) else "")
            return rec, None
        except Exception as e:
            rec["status"] = "error"
            rec["reason"] = "%s: %s" % (type(e).__name__, e)
            return rec, None
        final = resp.geturl()
        rec["final_url"] = final
        if final != url and PRIVATE_PATH.search(urllib.parse.urlsplit(final).path + "?"):
            rec["status"] = "skipped"
            rec["reason"] = "redirected to a login/account page: requires permission, out of scope"
            return rec, None
        ctype = (resp.headers.get("Content-Type") or "").lower()
        if not any(t in ctype for t in ALLOWED_TYPES):
            rec["status"] = "skipped"
            rec["reason"] = "content-type %s is not a text page (PDFs/binaries are not collected)" % (ctype.split(";")[0] or "unknown")
            return rec, None
        charset = "utf-8"
        m = re.search(r"charset=([\w-]+)", ctype)
        if m:
            charset = m.group(1)
        else:
            m = re.search(br'<meta[^>]+charset=["\']?([\w-]+)', body[:4096], re.I)
            if m:
                charset = m.group(1).decode("ascii", "replace")
        try:
            raw = body.decode(charset, "replace")
        except LookupError:
            raw = body.decode("utf-8", "replace")
        if "html" in ctype:
            ex = TextExtractor()
            try:
                ex.feed(raw)
            except Exception:
                pass
            text, title, outline, links, desc = ex.text(), " ".join(ex.title.split()), ex.outline, ex.links, ex.description
        else:
            text, title, outline, links, desc = raw.strip(), "", [], [], ""
        if truncated:
            rec["truncated"] = True
        rec.update({
            "status": "ok", "kind": "html" if "html" in ctype else "text",
            "title": title or urllib.parse.urlsplit(final).path,
            "description": desc, "bytes": len(body),
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "outline": outline, "links": links,
        })
        return rec, text


class Study:
    def __init__(self, slug, root):
        if not re.match(r"^[a-z0-9][a-z0-9._-]{0,63}$", slug):
            sys.exit("slug must be lowercase letters, digits, dot, dash or underscore: %r" % slug)
        self.slug = slug
        self.dir = os.path.join(root, slug)
        self.src_dir = os.path.join(self.dir, "sources")
        self.index_path = os.path.join(self.dir, "sources.json")
        os.makedirs(self.src_dir, exist_ok=True)
        # Fetched page texts are reference material for the blueprint and must
        # never be committed: keep a .gitignore that ignores everything in sources/.
        gi = os.path.join(self.src_dir, ".gitignore")
        if not os.path.exists(gi):
            with open(gi, "w", encoding="utf-8") as f:
                f.write("*\n!.gitignore\n")
        if os.path.exists(self.index_path):
            with open(self.index_path, encoding="utf-8") as f:
                self.index = json.load(f)
        else:
            self.index = {"slug": slug, "tool": "fetch_public.py " + VERSION, "user_agent": USER_AGENT,
                          "policy": "public pages only; robots.txt honored; no login; no captures; no binaries",
                          "sources": [], "skipped": []}

    def save(self):
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)

    def next_id(self):
        return "S%d" % (len(self.index["sources"]) + 1)

    def has(self, url=None, sha=None):
        for s in self.index["sources"]:
            if url and normalize_url(s.get("url", "")) == normalize_url(url):
                return s["id"]
            if sha and s.get("sha256") == sha:
                return s["id"]
        return None

    def add(self, rec, text):
        sid = self.next_id()
        rec = dict(rec)
        rec["id"] = sid
        rec["file"] = "sources/%s.txt" % sid
        outline = rec.pop("outline", [])
        links = rec.pop("links", None) or []
        if links:
            base = rec.get("final_url", rec["url"])
            site = registrable(urllib.parse.urlsplit(base).netloc)
            keep, seen = [], set()
            for href in links:
                absu = urllib.parse.urljoin(base, href.strip())
                p = urllib.parse.urlsplit(absu)
                if p.scheme not in ("http", "https") or registrable(p.netloc) != site:
                    continue
                n = normalize_url(absu)
                if n in seen or PRIVATE_PATH.search(p.path + "?"):
                    continue
                seen.add(n)
                keep.append(n)
            if keep:
                with open(os.path.join(self.src_dir, "%s.links.txt" % sid), "w", encoding="utf-8") as f:
                    f.write("\n".join(keep[:300]) + "\n")
                rec["links_file"] = "sources/%s.links.txt" % sid
        head = ["# %s" % sid, "url: %s" % rec["url"], "final_url: %s" % rec.get("final_url", rec["url"]),
                "title: %s" % rec.get("title", ""), "fetched_at: %s" % rec["fetched_at"],
                "sha256: %s" % rec.get("sha256", ""), "kind: %s" % rec.get("kind", "")]
        if rec.get("description"):
            head.append("description: %s" % rec["description"])
        if rec.get("license"):
            head.append("license: %s" % rec["license"])
        body = "\n".join(head) + "\n---\n"
        if outline:
            body += "## outline\n" + "\n".join("%s %s" % ("#" * int(t[1]), txt) for t, txt in outline) + "\n---\n"
        body += text + "\n"
        with open(os.path.join(self.dir, rec["file"]), "w", encoding="utf-8") as f:
            f.write(body)
        self.index["sources"].append(rec)
        return sid

    def skip(self, rec):
        self.index["skipped"].append({k: rec[k] for k in ("url", "fetched_at", "status", "reason") if k in rec})


# ---------------------------------------------------------------- commands

def cmd_discover(args):
    home = args.url if "://" in args.url else "https://" + args.url
    f = Fetcher()
    rec, text = f.fetch_page(home)
    if text is None:
        print("cannot read homepage: %s" % rec.get("reason"))
        return 1
    base = urllib.parse.urlsplit(rec.get("final_url", home))
    site = registrable(base.netloc)
    seen, scored = set(), []
    for href in rec.get("links", []):
        href = href.strip()
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        absu = urllib.parse.urljoin(rec.get("final_url", home), href)
        p = urllib.parse.urlsplit(absu)
        if p.scheme not in ("http", "https"):
            continue
        host = p.netloc.lower()
        same = registrable(host) == site
        sub = host.split(".")[0]
        if not same and not (sub in DOC_SUBDOMAINS):
            continue
        norm = normalize_url(absu)
        if norm in seen or PRIVATE_PATH.search(p.path + "?"):
            continue
        seen.add(norm)
        hay = (p.netloc + p.path).lower()
        score, why = 0, []
        for kw, w in DISCOVER_KEYWORDS:
            if re.search(r"(^|[/.\-_])%s([/.\-_]|$)" % re.escape(kw), hay):
                score += w
                why.append(kw)
        if sub in DOC_SUBDOMAINS:
            score += 80
            why.append("docs-subdomain")
        if score:
            scored.append((score, norm, ",".join(why)))
    scored.sort(key=lambda x: (-x[0], x[1]))
    print("# candidates on %s (public, robots-allowed paths only; review before fetching)" % base.netloc)
    for score, url, why in scored[: args.max]:
        print("%s\t%s" % (url, why))
    if rec.get("title"):
        print("# homepage title: %s" % rec["title"])
    return 0 if scored else 1


def cmd_fetch(args):
    st = Study(args.slug, args.root)
    f = Fetcher()
    added, refused, count = [], 0, 0
    for url in args.urls:
        if count >= args.max_pages:
            print("max pages reached (%d); stop here, review, then fetch more deliberately" % args.max_pages)
            break
        url = url if "://" in url else "https://" + url
        dup = st.has(url=url)
        if dup:
            print("%s  already collected as %s" % (url, dup))
            continue
        count += 1
        rec, text = f.fetch_page(url)
        if text is None:
            st.skip(rec)
            refused += 1
            print("SKIP  %s  (%s)" % (url, rec.get("reason")))
            continue
        dup = st.has(sha=rec["sha256"])
        if dup:
            print("%s  same content as %s, not stored twice" % (url, dup))
            continue
        if len(text) < 200:
            st.skip(dict(rec, status="skipped", reason="page has almost no readable text (%d chars); likely rendered by JavaScript or empty" % len(text)))
            print("SKIP  %s  (no readable text, %d chars)" % (url, len(text)))
            continue
        sid = st.add(rec, text)
        added.append(sid)
        note = ""
        if len(text) < 2000 and len(rec.get("outline", [])) >= 6:
            note = "; looks like mostly navigation (%d headings, %d chars): cite with care" % (len(rec["outline"]), len(text))
        print("%s  %s  <- %s  (%d chars%s%s)" % (sid, rec.get("title", "")[:60], url, len(text), ", truncated" if rec.get("truncated") else "", note))
    st.save()
    print("collected %d page(s), refused %d; index: %s" % (len(added), refused, st.index_path))
    if not added and refused:
        return 2
    return 0 if added else 1


COPYLEFT = {"AGPL-3.0", "GPL-3.0", "GPL-2.0", "LGPL-3.0", "LGPL-2.1", "SSPL-1.0", "EUPL-1.2", "OSL-3.0", "CC-BY-SA-4.0"}


def cmd_github(args):
    st = Study(args.slug, args.root)
    f = Fetcher()
    m = re.match(r"^(?:https?://github\.com/)?([\w.-]+)/([\w.-]+?)(?:\.git)?/?$", args.repo.strip())
    if not m:
        sys.exit("repo must look like owner/name or https://github.com/owner/name")
    owner, name = m.group(1), m.group(2)
    meta = {}
    try:
        resp, body, _ = f._raw_get("https://api.github.com/repos/%s/%s" % (owner, name), accept="application/vnd.github+json")
        data = json.loads(body.decode("utf-8", "replace"))
        meta = {k: data.get(k) for k in ("full_name", "description", "homepage", "language", "stargazers_count",
                                           "forks_count", "default_branch", "topics", "archived", "pushed_at")}
        if isinstance(data.get("license"), dict):
            meta["license"] = data["license"].get("spdx_id")
    except Exception as e:
        print("GitHub API not reachable (%s); falling back to raw README/LICENSE" % (type(e).__name__))
    branches = [meta.get("default_branch")] if meta.get("default_branch") else ["main", "master"]
    readme_text, readme_url = None, None
    for br in branches:
        for fn in ("README.md", "readme.md", "README.rst", "README"):
            url = "https://raw.githubusercontent.com/%s/%s/%s/%s" % (owner, name, br, fn)
            rec, text = f.fetch_page(url)
            if text:
                readme_text, readme_url, readme_rec = text, url, rec
                break
        if readme_text:
            break
    if not readme_text:
        print("no public README found for %s/%s" % (owner, name))
        return 2
    license_id = meta.get("license")
    if not license_id:
        for br in branches:
            for fn in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"):
                rec_l, lic = f.fetch_page("https://raw.githubusercontent.com/%s/%s/%s/%s" % (owner, name, br, fn))
                if lic:
                    head = lic[:600].upper()
                    license_id = ("AGPL-3.0" if "AFFERO" in head else "GPL-3.0" if "GNU GENERAL PUBLIC LICENSE" in head and "VERSION 3" in head
                                  else "GPL-2.0" if "GNU GENERAL PUBLIC LICENSE" in head else "MIT" if "MIT LICENSE" in head or "PERMISSION IS HEREBY GRANTED" in head
                                  else "Apache-2.0" if "APACHE LICENSE" in head else "BSD" if "REDISTRIBUTION AND USE" in head else "see file")
                    break
            if license_id:
                break
    if not license_id:
        # no LICENSE file: many small repos carry the notice in the header of their main source file
        for br in branches:
            for fn in ("index.js", "main.js", "app.js", "index.html", "main.py", "app.py", "src/index.js", "src/main.js"):
                rec_h, src = f.fetch_page("https://raw.githubusercontent.com/%s/%s/%s/%s" % (owner, name, br, fn))
                if src:
                    head = src[:1200].upper()
                    license_id = ("AGPL-3.0" if "AFFERO" in head else "GPL" if "GNU GENERAL PUBLIC LICENSE" in head
                                  else "MIT" if "MIT LICENSE" in head or "PERMISSION IS HEREBY GRANTED" in head
                                  else "Apache-2.0" if "APACHE LICENSE" in head
                                  else "BSD (file header)" if "BSD-STYLE LICENSE" in head or "REDISTRIBUTION AND USE" in head else None)
                    if license_id:
                        license_id += " via %s" % fn
                        break
            if license_id:
                break
    rec = dict(readme_rec)
    rec.update({"kind": "github", "title": "GitHub %s/%s README" % (owner, name), "url": "https://github.com/%s/%s" % (owner, name),
                "final_url": readme_url, "license": license_id or "unknown", "repo_meta": meta})
    header = ["repository: https://github.com/%s/%s" % (owner, name), "license: %s" % (license_id or "unknown")]
    for k in ("description", "language", "stargazers_count", "forks_count", "topics", "pushed_at"):
        if meta.get(k) not in (None, "", []):
            header.append("%s: %s" % (k, meta[k]))
    text = "\n".join(header) + "\n\n" + readme_text
    rec["sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    dup = st.has(url=rec["url"])
    if dup:
        print("already collected as %s" % dup)
        return 0
    sid = st.add(rec, text)
    st.save()
    print("%s  GitHub %s/%s  license=%s" % (sid, owner, name, license_id or "unknown"))
    if (license_id or "").upper().split("-OR-")[0] in COPYLEFT or "GPL" in (license_id or "").upper():
        print("NOTE: copyleft license (%s). Studying the architecture is fine; copying code into a product under a different license is not. The blueprint must say so." % license_id)
    return 0


def cmd_links(args):
    """Print the same-site links recorded for a fetched page (no network)."""
    st = Study(args.slug, args.root)
    want = args.source.upper()
    for s in st.index["sources"]:
        if s["id"] == want:
            lf = s.get("links_file")
            if not lf or not os.path.exists(os.path.join(st.dir, lf)):
                print("no links recorded for %s" % want)
                return 1
            with open(os.path.join(st.dir, lf), encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and (not args.grep or args.grep.lower() in line.lower()):
                        print(line)
            return 0
    print("unknown source id %s" % want)
    return 1


def cmd_list(args):
    st = Study(args.slug, args.root)
    for s in st.index["sources"]:
        print("%s\t%s\t%s\t%s" % (s["id"], s.get("kind", ""), (s.get("title") or "")[:50], s["url"]))
    for s in st.index["skipped"]:
        print("skipped\t%s\t%s" % (s["url"], s.get("reason", "")))
    print("%d collected, %d skipped" % (len(st.index["sources"]), len(st.index["skipped"])))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    d = sub.add_parser("discover"); d.add_argument("url"); d.add_argument("--max", type=int, default=40)
    fe = sub.add_parser("fetch"); fe.add_argument("slug"); fe.add_argument("urls", nargs="+")
    fe.add_argument("--max-pages", type=int, default=25); fe.add_argument("--root", default=DEFAULT_ROOT)
    g = sub.add_parser("github"); g.add_argument("slug"); g.add_argument("repo"); g.add_argument("--root", default=DEFAULT_ROOT)
    li = sub.add_parser("list"); li.add_argument("slug"); li.add_argument("--root", default=DEFAULT_ROOT)
    lk = sub.add_parser("links"); lk.add_argument("slug"); lk.add_argument("source", help="e.g. S3"); lk.add_argument("--grep"); lk.add_argument("--root", default=DEFAULT_ROOT)
    args = ap.parse_args(argv)
    if not args.cmd:
        ap.print_help()
        return 1
    return {"discover": cmd_discover, "fetch": cmd_fetch, "github": cmd_github, "list": cmd_list, "links": cmd_links}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
