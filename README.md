---
language:
  - en
tags:
  - skill
  - agent-skill
  - autocode
  - deployment
  - shipping
  - beginner-friendly
  - claude-code
  - codex
  - cursor
  - copilot
  - gemini
  - hermes
  - i-lang
  - zero-dependency
license: mit
---

# ⚡ AutoCode

<div align="center">

### You say it. AutoCode ships it.

[![MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![v6.2.0](https://img.shields.io/badge/version-6.2.0-blue.svg)](https://github.com/ilang-ai/autocode/releases)
[![Skills](https://img.shields.io/badge/Skills-11-blueviolet)](#-11-skills-7-stages)
[![Zero Deps](https://img.shields.io/badge/Dependencies-0-brightgreen)](#-install)
[![Platforms](https://img.shields.io/badge/Platforms-any%20SKILL.md%20agent-blue)](#-install)
[![iLang Spec](https://img.shields.io/badge/iLang-Spec-d4a858)](https://github.com/ilang-ai/ilang-spec)
[![iLang](https://img.shields.io/badge/iLang-v5.0-1e3a8a.svg)](https://ilang.ai)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22865145.svg)](https://doi.org/10.5281/zenodo.22865145)

[🇨🇳 中文](docs/README.zh.md) · [🇯🇵 日本語](docs/README.ja.md) · [🇰🇷 한국어](docs/README.ko.md) · [🇪🇸 Español](docs/README.es.md) · [🇧🇷 Português](docs/README.pt.md) · [🇩🇪 Deutsch](docs/README.de.md) · [🇫🇷 Français](docs/README.fr.md) · [🇷🇺 Русский](docs/README.ru.md) · [🇸🇦 العربية](docs/README.ar.md) · [🇮🇳 हिन्दी](docs/README.hi.md)

---

> **Every AI coding tool helps you write code. AutoCode helps you ship it.**
>
> You say what you want. AutoCode builds it, deploys it, and gives you a live URL.
> You don't need to know programming. You just say yes or no.
> When it's done, anyone in the world can visit your website.
>
> **New in v6: see a product you like, get your own.** Say "I want something like *X*".
> AutoCode studies *X* from its public pages only, writes a blueprint where every line
> carries its source, cuts an MVP small enough to build in one session, and builds it.
> It learns the structure and designs its own look — nothing is reverse-engineered or copied.
>
> Built on iLang, the first protocol to formally map Greek mathematical symbols (Σ, Δ, φ, λ, Ω, ∇, μ, Π, ψ, ξ, ζ, θ, ∂) as primitive verbs for AI-to-AI communication, and the first to define a computable vector space for AI judgment (11 dimensions, 4 axioms).

---

</div>

## 🚀 Install

**Any agent, one command (Claude Code, Codex, Hermes, OpenCode, Gemini CLI, CodeBuddy, Qwen Code, Windsurf, Cursor, Trae, OpenClaw …):**

```bash
git clone https://github.com/ilang-ai/autocode.git && cd autocode
python3 autocode.py setup          # detects your agents, shows the plan, asks once, installs
python3 autocode.py doctor         # read-only health check; run it whenever something feels off
python3 autocode.py uninstall      # removes only what setup installed; your edits stay
```

Python 3.8+ and nothing else. `setup` copies the 11 skills into each agent's skills folder,
adds one managed block to its instructions file (`CLAUDE.md`, `AGENTS.md`, `SOUL.md`, …) so
agents without hooks still get memory, full review and the pre-deploy secret scan, and keeps
backups of anything it touched. `python3 autocode.py clients` lists the supported agents;
the table lives in [`agents.json`](agents.json) — adding an agent is adding an entry.

**Claude Code plugin route (also fine):**

```
/install autocode
```

That's it. One command. [View on Claude Code Marketplace](https://platform.claude.com/plugins/autocode)

**Or from GitHub:**

```
/plugin marketplace add ilang-ai/autocode
/plugin install autocode@autocode
```

Restart. Start talking. Done.

### Codex

Tell Codex:

```
Fetch and follow instructions from https://raw.githubusercontent.com/ilang-ai/autocode/refs/heads/main/.codex/INSTALL.md
```

### OpenCode

Tell OpenCode:

```
Fetch and follow instructions from https://raw.githubusercontent.com/ilang-ai/autocode/refs/heads/main/.opencode/INSTALL.md
```

**Works on Claude Code, Codex, and OpenCode.** Same 11 skills, zero changes.

### Hermes Agent

```bash
hermes skills install ilang-ai/autocode
```

### Cursor

Copy `skills/` into `~/.cursor/skills/`, or browse [Cursor Directory](https://cursor.directory) once listed.

### Gemini CLI

```bash
gemini extensions install https://github.com/ilang-ai/autocode
```

### Any SKILL.md-compatible agent

Copy the `skills/` directory into your agent's skills path.

---

## 🔰 New to Everything? No Problem.

Never used a server before? Don't know what a terminal is? That's fine — this guide starts from zero.

<details>
<summary><b>Click here for the complete beginner guide</b></summary>

### Step 1: Get a Cloud Computer

You need a cloud computer (VPS) — think of it as a computer in the cloud that's always on.

**👉 Go to [dev.ilang.ai](https://dev.ilang.ai)** — new users get **$300 free credit** (enough for over a year).

**How to sign up:**

1. Click the link → registration page
2. Enter email, create password (10+ characters, mix of uppercase, lowercase, numbers)
3. Check email, click verification link
4. Payment: supports **credit card, PayPal, Alipay (支付宝)**
5. $300 free credit applied automatically

**Create your cloud computer:**

1. Click **"Deploy +"** (top right)
2. **"Deploy New Server"**
3. **Type:** "Cloud Compute — Shared CPU" (cheapest)
4. **Location:** Closest to you (Tokyo for Asia, New York for Americas, London for Europe)
5. **Image:** "Debian 12"
6. **Plan:** $6/month (1 CPU, 1GB RAM — enough)
7. Click **"Deploy Now"**

Wait 1-2 minutes. Green **"Running"** = ready.

**Find your connection info:**

Click server name → you'll see:
- **IP Address** — like `149.28.xxx.xxx`
- **Username** — `root`
- **Password** — click eye icon to show, copy button to copy

### Step 2: Connect

**Windows:** Download [PuTTY](https://putty.org). Enter IP, click Open. Type username and password.

**Mac:** Open Terminal. Type: `ssh root@your-ip-address`. Enter password.

**Phone:** Download "Termius". Add host with IP, username, password.

Black screen with `#` = you're in.

### Step 3: Install Everything

Paste this, press Enter, wait 2 minutes:

```bash
curl -fsSL https://raw.githubusercontent.com/ilang-ai/autocode/main/setup.sh | bash
```

### Step 4: Start Claude Code

```bash
claude
```

Log in when prompted ([Anthropic account](https://console.anthropic.com) needed).

### Step 5: Install AutoCode

Say:

```
Install the AutoCode plugin from github.com/ilang-ai/autocode
```

Permission questions? **Always choose the highest number** ("Yes, don't ask again"). Safe — AutoCode is pure text, no executable code.

Type `/exit`, then `claude` to restart.

### Step 6: Build

```
Build me a restaurant website with online reservations
```

**You're a developer now.**

</details>

---

## 📖 What You'll Experience

### First Time

```
You:      "I want to sell cakes online"
AutoCode:  "What computer do you use? Mac or other?"
You:      "Other"
AutoCode:  "I'll help you get a server. $6/month. OK?"
You:      "OK"
AutoCode:  → Sets up server → Builds website → Deploys
           → "Done. Open nainai-cake.com on your phone."

Your effort: 3 yes/no answers
Result: a live website anyone can visit
```

### Fifth Time

```
You:      "Build a booking site for my hair salon"
AutoCode:  → Knows your preferences → Builds → Deploys
           → "Live at salon-booking.com. SSL active."
```

### Twentieth Time

```
You:      "New project"
AutoCode:  → Barely asks → Ships it → You realize you have 20 live websites
```

*User feedback: "I don't even know who did the work — I thought I was supposed to code, but it was already done."*

---

## 🔍 See a product you like, get your own

```
You:      "I want a lightweight issue tracker like Linear, for my 10-person team"
AutoCode:  "I'll study Linear from its public pages, give you a blueprint of how
            it's built, and cut an MVP we can ship today. We learn the structure
            and design our own look."
          → reads pricing, docs, changelog, API docs, integrations, security, careers
          → blueprint.md: 36 features (core / plus / drop), 13 objects with relations,
            7 user flows, pricing, gaps — every line tagged [S3] {high|medium|guess}
          → mvp.md: 5 objects, 7 screens, 7 build steps, 5 acceptance checks
You:      cross out what you don't want, say "go"
AutoCode:  → builds the MVP → deploys → "Live at https://… — open it on your phone."
```

The `product-study` skill works from public pages only: official site, docs, pricing,
changelog, public API docs, open-source repos, app-store listings, public reviews.
It refuses login areas, captures, decompiling and bulk scraping on its own, and its gate
rejects a blueprint that cites nothing, copies a sentence, or embeds the original's
images, logo or code. The interface, copy, brand and code of your product are yours.
A finished study: [`skills/product-study/examples/linear/`](skills/product-study/examples/linear/).
A complete run, study → build → verify → ship: [`skills/product-study/examples/dino/`](skills/product-study/examples/dino/) — a non-technical
ask ("a dinosaur game like that one, but I set the speed"), a one-file game whose rules are kept apart from its
look, and an acceptance table the user can read (check / expected / actual / match, 8/8, rerun on the live URL).

Before shipping, AutoCode runs that table, not "tests passed". A static build ships to GitHub Pages at no cost;
if you have no GitHub account it walks you through signing up, and you approve the login in your own browser.
The whole journey, as the rules AutoCode follows, is [`methodology/see-it-ship-it.md`](methodology/see-it-ship-it.md).

## 🧠 11 Skills, 7 Stages

All automatic. You never activate them. Every skill is one stage of the journey or a
support that runs across it; the journey itself is written down in
[`methodology/see-it-ship-it.md`](methodology/see-it-ship-it.md).

| Stage | Skill | What it does |
|---|---|---|
| S1 see | `see` | Understands what you want from how you said it; your level; the size of the job; locks what you confirmed; asks at most one question that is yours |
| S2 study | `product-study` | "Like X" → public-source blueprint with evidence → MVP cut → verify runner |
| S3 plan | `plan` | Steps that each end in something you can click; minutes, not hours; core first; risks and costs flagged |
| S4 build | `build` | Simplest stack that works, one feature at a time, rules kept apart from the look, checkpoint before anything risky, first-session environment |
| S5 verify | `verify` | Silent checks after every feature, full review before save and deploy, the acceptance table — check / expected / actual / match — local and again on the live URL |
| S6 ship | `ship` | Secret scan, then a public URL: GitHub Pages at no cost for static builds, a server only when needed; domain if you want one |
| S7 hand-back | `hand-back` | Progress lines, real milestones credited to you, session summary, and the final hand-back: URL, table, what to try, what was learned vs decided |
| across | `judge` | When AutoCode acts alone and when it stops and asks — iLang v5.0: perception sets 11 dimensions, the frozen `f_v5` sets the mode, you see one plain line |
| across | `fix` | Observe → reason → smallest fix → verify → explain in your words |
| across | `memory` | Loads what we know at every start, learns patterns, preferences and mistakes without asking, saves on stop — never secrets |
| across | `security` | Secrets never in code or chat; scan before every deploy |

v6.1 had 49 skills; 44 of them were one paragraph each. v6.2 folds them into the
eleven above (the mapping is in the methodology file). `setup` retires the old folders
on upgrade and keeps any you edited.

## 🎯 Precision

Powered by [iLang v5.0](https://ilang.ai). Structured instructions mean AI gets it right the first time. No rework.

## 🧠 Memory

Close today → open tomorrow → remembers everything. Gets better every session.

---

## 🌍 Different from Everything Else

|  | Other AI coding tools | **AutoCode** |
| --- | --- | --- |
| **For** | Developers | **Anyone** |
| **Ends at** | Code written | **Website live** |
| **Requires** | Terminal/IDE knowledge | **Just say yes or no** |
| **Tech decisions** | Asks you | **Decides for you** |
| **Deployment** | You figure it out | **Automatic** |
| **Domain + SSL** | You figure it out | **Guided step by step** |
| **Start from a product you like** | "Make a clone" and hope | **Public-source blueprint with evidence → MVP** |
| **Memory** | Resets each session | **Persistent** |
| **Protocol** | None | **iLang v5.0** |
| **Language** | Usually English | **Your language** |

---

## ❓ Troubleshooting

<details>
<summary><b>Something broke, don't know what to say</b></summary>
Say "something's wrong". AutoCode asks simple questions. If it can't fix it in terminal, it tells you how to screenshot + upload to claude.ai.
</details>

<details>
<summary><b>/plugin command doesn't work</b></summary>
Just say: "Install the AutoCode plugin from github.com/ilang-ai/autocode". Talking works better than commands.
</details>

<details>
<summary><b>Permission popups I don't understand</b></summary>
Choose the highest number. AutoCode is pure text — safe to approve.
</details>

<details>
<summary><b>Can't connect to server</b></summary>
Check IP, username, password in Vultr dashboard. Server must be green "Running".
</details>

<details>
<summary><b>Is it safe?</b></summary>
100% open source, pure text files. Claude Code verified: "No malicious content."
</details>

<details>
<summary><b>Cost?</b></summary>
AutoCode: free forever (MIT). Cloud computer: $6/month (or free with $300 Vultr credit). Plus Anthropic API usage.
</details>

---

<div align="center">

[ilang.ai](https://ilang.ai) · [ilang.cn](https://ilang.cn) · [Hugging Face](https://huggingface.co/datasets/i-Lang/AutoCode) · [@adsorgcn](https://x.com/adsorgcn)

**iLang Research · iLang Inc. · Canada · MIT · Free Forever**

*You say it. AutoCode ships it. Powered by [iLang v5.0](https://ilang.ai).*

</div>

---

## Citation

[CITATION.cff](CITATION.cff); Zenodo archives each release. Concept DOI [10.5281/zenodo.22865145](https://doi.org/10.5281/zenodo.22865145) (all versions).
