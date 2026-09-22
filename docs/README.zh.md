# ⚡ AutoCode

<div align="center">

### 你说一句话。所有编程，全自动。

[![MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![v5.0.0](https://img.shields.io/badge/version-5.0.0-blue.svg)](https://github.com/ilang-ai/autocode/releases)
[![Skills](https://img.shields.io/badge/专业技能-48项-blueviolet)](#48项专业技能)
[![Zero Deps](https://img.shields.io/badge/依赖-0-brightgreen)](#安装)
[![Memory](https://img.shields.io/badge/记忆-跨天持久-purple)](#记忆)
[![平台](https://img.shields.io/badge/平台-CC%20%7C%20Codex%20%7C%20Hermes%20%7C%20Cursor%20%7C%20Gemini-blue)](#安装)

[English](../README.md) · [🇯🇵 日本語](README.ja.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇧🇷 Português](README.pt.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇷🇺 Русский](README.ru.md) · [🇸🇦 العربية](README.ar.md) · [🇮🇳 हिन्दी](README.hi.md)

---

> **AutoCode = 自动编程。**
>
> 你说一句话，AutoCode 帮你做出来。
> 选技术、写代码、测试、上线——全部自动。
> 你完全不需要懂编程。

---

</div>

## 🚀 安装

**👉 [看动画教程（3分钟，跟着做就行）](https://ilang.cn/acinstall.html)**

**环境安装（一行命令）：**

```bash
curl -fsSL https://raw.githubusercontent.com/ilang-ai/autocode/main/setup.sh | bash
```

**启动 Claude Code 并安装 AutoCode：**

```bash
claude
```

登录后说：

```
帮我安装autocode插件，地址 github.com/ilang-ai/autocode
```

或者用命令：

```
/plugin marketplace add ilang-ai/autocode
/plugin install autocode@autocode
```

重启。开口说话。完事。

### Codex

在 Codex 中说：

```
Fetch and follow instructions from https://raw.githubusercontent.com/ilang-ai/autocode/refs/heads/main/.codex/INSTALL.md
```

### OpenCode

在 OpenCode 中说：

```
Fetch and follow instructions from https://raw.githubusercontent.com/ilang-ai/autocode/refs/heads/main/.opencode/INSTALL.md
```

**支持 Claude Code、Codex、OpenCode 三大平台。** 48个技能通用，零修改。

### Trae（中文用户推荐）

不需要命令行。打开 [Trae](https://www.trae.ai/)，在AI对话框里粘贴：

```
帮我在当前目录创建 .trae/rules 文件夹，然后从这个地址下载文件保存到 .trae/rules/project-rules.md ：https://raw.githubusercontent.com/ilang-ai/trae/main/.trae/rules/project-rules.md
```

或直接下载 [ZeroCode](https://github.com/ilang-ai/trae)（40个中文技能版）。

---

## 🔰 什么都不会？没关系。

没用过服务器？不知道终端是什么？没问题——下面从零开始教你。

**👉 [打开动画教程](https://ilang.cn/acinstall.html)** — 跟着做就行，每一步都能复制粘贴。

<details>
<summary><b>点这里看完整小白教程</b></summary>

### 第一步：买一台云电脑

你需要一台云电脑（VPS）——你可以理解为一台放在云端、24小时开机的电脑。

**👉 打开 [dev.ilang.ai](https://dev.ilang.ai)** — 新用户赠送 **300美元免费额度**，够用一年多。

**注册：**

1. 点链接 → 注册页面
2. 输入邮箱，设密码（10位以上，包含大小写字母和数字）
3. 去邮箱点验证链接
4. 付款方式选 **支付宝（Alipay）**— 也支持微信、信用卡、PayPal
5. 充值 **10美元**（支付宝扫码）
6. 300美元免费额度自动到账

**创建云电脑：**

1. 点右上角 **"Deploy +"**
2. **"Deploy New Server"**
3. **Type：** 选 "Cloud Compute — Shared CPU"（最便宜）
4. **Location：** 选离你最近的（亚洲选东京Tokyo或新加坡Singapore）
5. **Image：** 选 "Debian 12"
6. **Plan：** 选 $6/月 那个（1核1G，够用了）
7. 点 **"Deploy Now"**

等1-2分钟，状态变成绿色 **Running** 就好了。

**找到连接信息：**

点服务器名字 → 看到：
- **IP Address** — 一串数字，比如 `149.28.xxx.xxx`
- **Username** — `root`
- **Password** — 点眼睛显示，点按钮复制

### 第二步：连上去

**Windows：** 下载 [PuTTY](https://putty.org)，Host Name 填IP，点Open，输入用户名和密码。

**Mac：** 打开终端（Spotlight搜Terminal），输入 `ssh root@你的IP地址`，输入密码。

**手机：** 下载 Termius，新建连接填IP、用户名、密码。

看到黑色屏幕最后有个 `#` = 你进去了。

### 第三步：装环境

粘贴，回车，等2分钟：

```bash
curl -fsSL https://raw.githubusercontent.com/ilang-ai/autocode/main/setup.sh | bash
```

### 第四步：启动

```bash
claude
```

按提示登录（[注册Anthropic账号](https://console.anthropic.com)）。

### 第五步：安装 AutoCode

说：

```
帮我安装autocode插件，地址 github.com/ilang-ai/autocode
```

弹出的权限确认？**每次都选数字最大的那个**（"同意，以后不再问"）。安全的——AutoCode是纯文本文件。

输入 `/exit`，再输入 `claude` 重启。

### 第六步：做产品

```
帮我做一个餐厅网站，要能在线订位
```

**你现在是开发者了。**

</details>

---

## 📖 你会经历什么

### 第一次

```
你：      "帮我做一个餐厅网站"
AutoCode： → 问2个问题 → 25分钟做完 → "打开这个网址看效果"

你花了：1句话 + 2个回答
外包：3-5万，2-4周
AutoCode：25分钟
```

### 第五次

```
你：      "再做一个花店商城"
AutoCode： → 知道你的偏好，直接开始 → "做好了。"
```

### 第二十次

```
你：      "新项目"
AutoCode： → 几乎不问 → 你发现自己能看懂它在做什么了
```

*用户反馈："我都不知道谁在工作了——我以为要编程，结果自己弄完了。"*

---

## 🧠 48项专业技能

全部自动。你不需要知道它们存在。

<details>
<summary><b>📋 需求理解（5项）</b></summary>

| 技能 | 说明 |
|------|------|
| 意图识别 | 你一开口它就知道你要什么 |
| 精准提问 | 最多2个，从不问技术问题 |
| 范围判断 | 自动判断大小任务 |
| 说话方式适配 | 你说什么语言它就说什么语言 |
| 需求锁定 | 确认后不跑题 |
</details>

<details>
<summary><b>📐 智能规划（6项）</b></summary>

| 技能 | 说明 |
|------|------|
| 任务拆解 | 大事拆成小步骤 |
| 优先级排序 | 先核心后锦上添花 |
| 时间预估 | "大概20分钟" |
| 风险预警 | 提前告诉你坑在哪 |
| 最优方案 | 自动选最快最省最稳的 |
| 决策翻译 | 用"省多少钱"来解释 |
</details>

<details>
<summary><b>🔨 产品构建（3项）</b></summary>

| 技能 | 说明 |
|------|------|
| 搭框架 | 自动搭骨架 |
| 做功能 | 一个一个做 |
| 做页面 | 所有设备能用 |
</details>

<details>
<summary><b>✅ 自动质检（4项）</b></summary>

| 技能 | 说明 |
|------|------|
| 自动检查 | 你无感 |
| 安全防护 | 防攻击 |
| 速度优化 | 快+省 |
| 多设备 | 手机/平板/电脑 |
</details>

<details>
<summary><b>🔧 问题修复（5项）</b></summary>

| 技能 | 说明 |
|------|------|
| 观察 | 自己看怎么了 |
| 推理 | 找根本原因 |
| 修复 | 修+确认 |
| 解释 | 用你的话说 |
| 引导 | 搞不定？教你截图传到 [claude.ai](https://claude.ai) |
</details>

<details>
<summary><b>💾 进度保存（3项）— ⭐ 灵魂</b></summary>

| 技能 | 说明 |
|------|------|
| ⭐ **全面复盘** | **每次保存从头检查。你看着学。** |
| 里程碑 | 庆祝节点 |
| 回退 | 一键退回 |
</details>

<details>
<summary><b>🚀 部署（4项）</b></summary>

| 技能 | 说明 |
|------|------|
| 本地跑 | 你的服务器 |
| 全球上线 | CDN秒开 |
| 边缘部署 | 免费方案 |
| 文件传输 | 服务器对传 |
</details>

<details>
<summary><b>📊 项目管理（5项）</b></summary>

| 技能 | 说明 |
|------|------|
| 进度 | "✅ 60%（3/5）" |
| 对标 | "外包2万，你25分钟" |
| 庆祝 | "🎉 完成！" |
| 总结 | 今天+明天 |
| 路线图 | 多天计划 |
</details>

<details>
<summary><b>🎓 越用越懂你（3项）</b></summary>

| 技能 | 说明 |
|------|------|
| 偏好 | 记住你的风格 |
| 规律 | 学你做什么 |
| 不重复犯错 | 错过的不再错 |
</details>

<details>
<summary><b>⚙️ 核心引擎（2项）</b></summary>

| 技能 | 说明 |
|------|------|
| 压缩 | iLang 结构化内部规划 |
| 记忆 | 跨天记住 |
</details>

---

## 💰 省钱

[iLang](https://ilang.cn) 压缩。你什么都不用做。

## 🧠 记忆

今天关了明天还记得。越用越默契。

---

## 🌍 和其他工具的区别

|  | 其他工具 | **AutoCode** |
| --- | --- | --- |
| **面向** | 程序员 | **所有人** |
| **前提** | 懂编程 | **会说话** |
| **核心** | 帮写代码 | **做产品** |
| **技术决策** | 问你 | **替你选** |
| **记忆** | 多数没有 | **自动** |
| **语言** | 通常英文 | **你说什么它说什么** |
| **依赖** | 各种 | **零** |

---

## ❓ 遇到问题？

<details>
<summary><b>出了问题不知道怎么说</b></summary>
说"有问题"。AutoCode问你简单问题。搞不定就教你截图传到claude.ai。
</details>

<details>
<summary><b>/plugin不好使</b></summary>
直接说："帮我安装autocode插件，地址 github.com/ilang-ai/autocode"
</details>

<details>
<summary><b>弹框看不懂</b></summary>
选数字最大的。纯文本文件，安全。
</details>

<details>
<summary><b>安全吗？</b></summary>
100%开源，纯文本。Claude Code自己审查过："没有恶意内容。"
</details>

<details>
<summary><b>多少钱？</b></summary>
AutoCode永久免费。云电脑$6/月（新用户$300免费额度）。加上Anthropic API费用。
</details>

---

<div align="center">

[ilang.ai](https://ilang.ai) · [ilang.cn](https://ilang.cn) · [research.ilang.ai](https://research.ilang.ai) · [@adsorgcn](https://x.com/adsorgcn) · [dev.ilang.ai](https://dev.ilang.ai)

**用 Trae？** 👉 [ZeroCode — 中文版，40个技能](https://github.com/ilang-ai/trae)

**iLang Research · iLang Inc. · Canada · MIT · 永久免费**

*你说一句话。AutoCode 做完所有事。*

</div>
