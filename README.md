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
[![v5.1.0](https://img.shields.io/badge/version-5.1.0-blue.svg)](https://github.com/ilang-ai/autocode/releases)
[![Skills](https://img.shields.io/badge/Skills-47-blueviolet)](#skills)
[![Zero Deps](https://img.shields.io/badge/Dependencies-0-brightgreen)](#-install)
[![Platforms](https://img.shields.io/badge/Platforms-CC%20%7C%20Codex%20%7C%20Hermes%20%7C%20Cursor%20%7C%20Gemini-blue)](#-install)
[![I-Lang L2](https://img.shields.io/badge/I--Lang-L2_Compatible-d4a858)](https://github.com/ilang-ai/ilang-spec)
[![I-Lang](https://img.shields.io/badge/I--Lang-v4.0-1e3a8a.svg)](https://ilang.ai)

[🇨🇳 中文](docs/README.zh.md) · [🇯🇵 日本語](docs/README.ja.md) · [🇰🇷 한국어](docs/README.ko.md) · [🇪🇸 Español](docs/README.es.md) · [🇧🇷 Português](docs/README.pt.md) · [🇩🇪 Deutsch](docs/README.de.md) · [🇫🇷 Français](docs/README.fr.md) · [🇷🇺 Русский](docs/README.ru.md) · [🇸🇦 العربية](docs/README.ar.md) · [🇮🇳 हिन्दी](docs/README.hi.md)

---

> **Every AI coding tool helps you write code. AutoCode helps you ship it.**
>
> You say what you want. AutoCode builds it, deploys it, and gives you a live URL.
> You don't need to know programming. You just say yes or no.
> When it's done, anyone in the world can visit your website.
>
> Built on I-Lang, the first protocol to formally map Greek mathematical symbols (Σ, Δ, φ, λ, Ω, ∇, μ, Π, ψ, ξ, ζ, θ, ∂) as primitive verbs for AI-to-AI communication, and the first to define a computable vector space for AI judgment (11 dimensions, 4 axioms).

---

</div>

## 🚀 Install

**Claude Code (recommended):**

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

**Works on Claude Code, Codex, and OpenCode.** Same 48 skills, zero changes.

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

## 🧠 48 Skills

All automatic. You never activate them.

<details>
<summary><b>📋 Understanding (5)</b></summary>

| Skill | What it does |
|-------|-------------|
| Intent Detection | Knows what you want instantly |
| Smart Questions | Max 2, never technical |
| Scope Detection | Small task or big project |
| Communication Adapt | Matches your language and level |
| Requirement Lock | Stays on track |
</details>

<details>
<summary><b>📐 Planning (6)</b></summary>

| Skill | What it does |
|-------|-------------|
| Task Breakdown | Big → small steps, 2-5 min each |
| Priority | Core first, polish last |
| Time Estimate | "About 20 minutes" |
| Risk Warning | Warns before problems happen |
| Best Choice | Auto-picks fastest/cheapest/most stable tech |
| Decision Translation | Explains in money/speed/stability |
</details>

<details>
<summary><b>🔨 Building (3)</b></summary>

| Skill | What it does |
|-------|-------------|
| Scaffold | Project foundation |
| Feature Build | One by one |
| UI Build | All devices |
</details>

<details>
<summary><b>✅ Quality (4)</b></summary>

| Skill | What it does |
|-------|-------------|
| Auto Check | Reviews code logic silently |
| Security | Blocks attacks, encrypts data |
| Performance | Fast + cheap to run |
| Multi-Device | Phone/tablet/desktop |
</details>

<details>
<summary><b>🔧 Debugging (5)</b></summary>

| Skill | What it does |
|-------|-------------|
| Observe | Investigates on its own |
| Reason | Finds root cause |
| Fix & Verify | Fixes + confirms |
| Explain | Tells you in your words |
| Fix Guide | Stuck? Guides you to screenshot and upload to [claude.ai](https://claude.ai) |
</details>

<details>
<summary><b>💾 Saving (3) — ⭐ Soul of AutoCode</b></summary>

| Skill | What it does |
|-------|-------------|
| ⭐ **Full Review** | **Every save: reviews entire project from beginning. You watch and learn.** |
| Milestone | Celebrates achievements |
| Rollback | One-click undo |
</details>

<details>
<summary><b>🚀 Deployment (4)</b></summary>

| Skill | What it does |
|-------|-------------|
| Local Run | Your server, your URL |
| Global Deploy | CDN, fast everywhere |
| Edge Deploy | Free tier |
| File Transfer | Server-to-server |
</details>

<details>
<summary><b>📊 Progress (5)</b></summary>

| Skill | What it does |
|-------|-------------|
| Live Progress | "✅ 60% (3/5)" |
| Efficiency Compare | "Outsourcing = $5K. You = 25 min." |
| Celebration | "🎉 Done!" |
| Daily Summary | Today + tomorrow |
| Roadmap | Multi-day plan |
</details>

<details>
<summary><b>🎓 Learning (3)</b></summary>

| Skill | What it does |
|-------|-------------|
| Preferences | Remembers your style |
| Patterns | Learns what you build |
| Mistakes | Never repeats errors |
</details>

<details>
<summary><b>⚙️ Engine (2)</b></summary>

| Skill | What it does |
|-------|-------------|
| Compression | I-Lang v5.0 protocol, structured internal planning |
| Memory | Remembers across sessions |
</details>

---

## 🎯 Precision

Powered by [I-Lang v5.0](https://ilang.ai). Structured instructions mean AI gets it right the first time. No rework.

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
| **Memory** | Resets each session | **Persistent** |
| **Protocol** | None | **I-Lang v5.0** |
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

[ilang.ai](https://ilang.ai) · [ilang.cn](https://ilang.cn) · [Hugging Face](https://huggingface.co/i-Lang/AutoCode) · [@adsorgcn](https://x.com/adsorgcn)

**I-Lang Research · iLang Inc. · Canada · MIT · Free Forever**

*You say it. AutoCode ships it. Powered by [I-Lang v5.0](https://ilang.ai).*

</div>
