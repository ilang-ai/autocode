# ⚡ AutoCode

<div align="center">

### 你说一句话。AutoCode 做出来，放上线。

[![MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![v6.2.2](https://img.shields.io/badge/version-6.2.2-blue.svg)](https://github.com/ilang-ai/autocode/releases)
[![Skills](https://img.shields.io/badge/技能-11项-blueviolet)](#-11-个技能7-个阶段)
[![Zero Deps](https://img.shields.io/badge/依赖-0-brightgreen)](#-安装)
[![Memory](https://img.shields.io/badge/记忆-跨天持久-purple)](#-记忆)
[![平台](https://img.shields.io/badge/平台-任何%20SKILL.md%20Agent-blue)](#-安装)
[![iLang](https://img.shields.io/badge/iLang-v5.0-1e3a8a.svg)](https://ilang.cn)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22865145.svg)](https://doi.org/10.5281/zenodo.22865145)

[English](../README.md) · [🇯🇵 日本語](README.ja.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇧🇷 Português](README.pt.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇷🇺 Русский](README.ru.md) · [🇸🇦 العربية](README.ar.md) · [🇮🇳 हिन्दी](README.hi.md)

---

> **AutoCode = 自动编程。**
>
> 你说一句话，AutoCode 帮你做出来。选技术、写代码、测试、上线，全部自动。
> 你完全不需要懂编程，只回答「行」或「不行」。做完以后，任何人都能打开你的网址。
>
> **v6：看中一个产品，做出你自己的那一版。** 说「我想做一个像 X 的」，
> AutoCode 只从 X 的公开页面学它的结构，出一份每条都带来源的蓝图，切出一个
> 一次会话就能做完的 MVP，然后做出来。学的是结构，皮是自己长的：不逆向、不抄。
>
> 基于 iLang 协议：第一个把希腊数学符号（Σ、Δ、φ、λ、Ω、∇、μ、Π、ψ、ξ、ζ、θ、∂）正式定义为 AI 之间通信的原语动词，
> 也是第一个为 AI 判断定义了可计算向量空间（11 个维度、4 条公理）的协议。

---

</div>

## 🚀 安装

**任何 Agent，一条命令**（Claude Code、Codex、Hermes、OpenCode、Gemini CLI、CodeBuddy、Qwen Code、Windsurf、Cursor、Trae、OpenClaw……）：

```bash
git clone https://github.com/ilang-ai/autocode.git && cd autocode
python3 autocode.py setup          # 自动识别你装了哪些 Agent，先给计划，问一次，再装
python3 autocode.py doctor         # 只读自检，哪里不对一眼看到
python3 autocode.py uninstall      # 只删它自己装的，你改过的留下
```

只要 Python 3.8+，不装任何包。`setup` 把 11 个技能拷进每个 Agent 的技能目录，往它的人设文件
（`CLAUDE.md` / `AGENTS.md` / `SOUL.md`……）里加一段受管的块，没有 hooks 的 Agent 也能有记忆、
完整复查和上线前密钥扫描；改过的文件都有备份。`python3 autocode.py clients` 列出支持的 Agent；
表在 [`agents.json`](../agents.json)，加一个 Agent 就是加一条。从 6.1 升上来的，`setup` 会把并掉的
旧技能目录自动退役（留备份），你改过的留下。

**Claude Code 插件路线（照旧可用）：**

```
/install autocode
```

一条命令，完事。[在 Claude Code 市场查看](https://platform.claude.com/plugins/autocode)

**或者从 GitHub 装：**

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

### Hermes Agent

```bash
hermes skills install ilang-ai/autocode
```

### Cursor

把 `skills/` 拷进 `~/.cursor/skills/`，或者直接 `python3 autocode.py setup --client cursor`。

### Gemini CLI

```bash
gemini extensions install https://github.com/ilang-ai/autocode
```

### Trae / 任何认 SKILL.md 的 Agent

`python3 autocode.py setup` 会认出 Trae；认不出的 Agent，把 `skills/` 目录拷进它的技能路径就行。
只想要纯中文、不用命令行的版本，还有 [ZeroCode](https://github.com/ilang-ai/trae)（40 个中文技能）。

**👉 [看动画教程（3 分钟，跟着做就行）](https://ilang.cn/acinstall.html)**

---

## 🔰 什么都不会？没关系。

没用过服务器？不知道终端是什么？没问题。下面从零开始教你。

<details>
<summary><b>点这里看完整小白教程</b></summary>

### 第一步：买一台云电脑

你需要一台云电脑（VPS）。你可以理解为一台放在云端、24 小时开机的电脑。

**👉 打开 [dev.ilang.ai](https://dev.ilang.ai)**，新用户赠送 **300 美元免费额度**，够用一年多。

**注册：**

1. 点链接，进注册页面
2. 输入邮箱，设密码（10 位以上，包含大小写字母和数字）
3. 去邮箱点验证链接
4. 付款方式选 **支付宝（Alipay）**，也支持微信、信用卡、PayPal
5. 充值 **10 美元**（支付宝扫码）
6. 300 美元免费额度自动到账

**创建云电脑：**

1. 点右上角 **"Deploy +"**
2. **"Deploy New Server"**
3. **Type：** 选 "Cloud Compute, Shared CPU"（最便宜）
4. **Location：** 选离你最近的（亚洲选东京 Tokyo 或新加坡 Singapore）
5. **Image：** 选 "Debian 12"
6. **Plan：** 选 $6/月 那个（1 核 1G，够用了）
7. 点 **"Deploy Now"**

等 1 到 2 分钟，状态变成绿色 **Running** 就好了。

**找到连接信息：**

点服务器名字，看到：
- **IP Address**：一串数字，比如 `149.28.xxx.xxx`
- **Username**：`root`
- **Password**：点眼睛显示，点按钮复制

### 第二步：连上去

**Windows：** 下载 [PuTTY](https://putty.org)，Host Name 填 IP，点 Open，输入用户名和密码。

**Mac：** 打开终端（Spotlight 搜 Terminal），输入 `ssh root@你的IP地址`，输入密码。

**手机：** 下载 Termius，新建连接填 IP、用户名、密码。

看到黑色屏幕最后有个 `#`，你就进去了。

### 第三步：装环境

粘贴，回车，等 2 分钟：

```bash
curl -fsSL https://raw.githubusercontent.com/ilang-ai/autocode/main/setup.sh | bash
```

### 第四步：启动

```bash
claude
```

按提示登录（[注册 Anthropic 账号](https://console.anthropic.com)）。

### 第五步：安装 AutoCode

说：

```
帮我安装autocode插件，地址 github.com/ilang-ai/autocode
```

弹出的权限确认？**每次都选数字最大的那个**（"同意，以后不再问"）。安全：AutoCode 是纯文本文件。

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
你：       「我想在网上卖蛋糕」
AutoCode： 「你用的是 Mac 还是别的电脑？」
你：       「别的」
AutoCode： 「我帮你弄一台云服务器，6 美元一个月，可以吗？」
你：       「可以」
AutoCode： → 配服务器 → 做网站 → 上线
           → 「做好了。手机打开 nainai-cake.com 看看。」

你花的功夫：3 个是/否
结果：一个谁都能打开的网站
```

### 第五次

```
你：       「给我的理发店做个预约网站」
AutoCode： → 知道你的偏好 → 做 → 上线
           → 「上线了：salon-booking.com，证书已装好。」
```

### 第二十次

```
你：       「新项目」
AutoCode： → 几乎不问 → 上线 → 你发现自己已经有 20 个在线的网站了
```

*用户反馈："我都不知道谁在工作了。我以为要编程，结果已经弄完了。"*

---

## 🔍 看中一个产品，做出你自己的

```
你：       「我想做一个像 Linear 的轻量工单工具，给我们十个人的团队用」
AutoCode： 「我从 Linear 的公开页面研究它，给你一份它怎么搭的蓝图，再切一个今天
            就能上线的 MVP。学的是结构，界面我们自己设计。」
          → 读定价、文档、更新日志、API 文档、集成、安全、招聘页
          → blueprint.md：36 条功能（核心/增值/可砍）、13 个对象和关系、7 条用户流程、
            定价、空白，每条带 [S3] {高|中|推测}
          → mvp.md：5 个对象、7 个页面、7 步建造顺序、5 条验收
你：       划掉不要的，说「开始」
AutoCode： → 搭 MVP → 上线 → 「上线了：https://…，手机打开看看。」
```

`product-study` 只用公开页面：官网、文档、定价、更新日志、公开 API 文档、开源仓库、应用商店、
公开评测。登录区、抓包、反编译、批量爬取它自己就拒；蓝图门禁拒绝没来源的、照抄的、带原产品
图片/logo/代码的。你的产品的界面、文案、品牌、代码都是你自己的。
一份做完的研究：[`skills/product-study/examples/linear/`](../skills/product-study/examples/linear/)。
一次完整的跑通，研究 → 做 → 验收 → 上线：[`skills/product-study/examples/dino/`](../skills/product-study/examples/dino/)，
一句外行人的话（「一个像那个的小恐龙游戏，但速度我自己定」）、一个规则和画面分开写的单文件游戏、
一张用户看得懂的验收表（检查 / 预期 / 实际 / 结果，8/8，上线后对着线上网址再跑一遍）。

上线前 AutoCode 跑的是那张表，不是一句「测试通过」。静态站零成本上 GitHub Pages；
没有 GitHub 账号它带你注册，登录在你自己的浏览器里点确认。整段旅程写成规则在
[`methodology/see-it-ship-it.md`](../methodology/see-it-ship-it.md)。

## 🧠 11 个技能，7 个阶段

全部自动。你不需要知道它们存在。每个技能要么是旅程的一个阶段，要么贯穿全程；
旅程本身写在 [`methodology/see-it-ship-it.md`](../methodology/see-it-ship-it.md)。

| 阶段 | 技能 | 做什么 |
|---|---|---|
| S1 看 | `see` | 从你怎么说，听懂你要什么；判断你的水平、任务大小；锁定你确认过的；最多问一个只有你能答的问题 |
| S2 学 | `product-study` | 「像 X 的」→ 只用公开来源、每条带证据的蓝图 → MVP 切分 → 验收跑器 |
| S3 划 | `plan` | 每一步都结束在你能点的东西上；按分钟算不按小时；核心先做；风险和花钱的地方先说 |
| S4 做 | `build` | 最简单能跑的技术栈，一次一个功能，规则和画面分开写，动危险的东西之前先存档，第一次会话先把环境弄好 |
| S5 验 | `verify` | 每个功能做完静静地查一遍，保存和上线前整体复查，验收表（检查 / 预期 / 实际 / 结果）本地跑一遍、上线后对着网址再跑一遍 |
| S6 上 | `ship` | 先扫密钥，再给一个公开网址：静态站零成本上 GitHub Pages，需要后台才用服务器；想要域名就带你绑 |
| S7 交 | `hand-back` | 进度一行、真正的里程碑记在你名下、会话小结，最后固定格式交付：网址、验收表、你亲手试的动作、学来的和自己定的 |
| 贯穿 | `judge` | 什么时候自己干、什么时候停下来问你：iLang v5.0，感知定 11 个维度，冻结的 `f_v5` 定模式，你只看到一句人话 |
| 贯穿 | `fix` | 先看 → 再想 → 最小修改 → 验证 → 用你的话解释 |
| 贯穿 | `memory` | 每次开始先加载已知的，自己学规律、偏好和教训，不问你；结束时保存；永不存密钥 |
| 贯穿 | `security` | 密钥永不进代码和聊天；每次上线前扫一遍 |

v6.1 有 49 个技能，其中 44 个只有一段话。v6.2 把它们并进上面 11 个（对应关系在方法论文件里）。
`setup` 升级时自动退役旧目录，你改过的留下。

## 🎯 精准

基于 [iLang v5.0](https://ilang.cn)。结构化的指令让 AI 第一次就做对，不返工。

## 🧠 记忆

今天关了明天还记得。越用越默契。

---

## 🌍 和其他工具的区别

|  | 其他 AI 编程工具 | **AutoCode** |
| --- | --- | --- |
| **面向** | 程序员 | **所有人** |
| **终点** | 代码写完 | **网站上线** |
| **前提** | 会用终端 / IDE | **会说「行」或「不行」** |
| **技术决策** | 问你 | **替你定** |
| **部署** | 你自己想办法 | **自动** |
| **域名 + 证书** | 你自己想办法 | **一步步带你点** |
| **从看中的产品开始** | 「做个一样的」然后碰运气 | **公开来源的证据蓝图 → MVP** |
| **记忆** | 每次清零 | **持久** |
| **协议** | 没有 | **iLang v5.0** |
| **语言** | 通常英文 | **你说什么它说什么** |

---

## ❓ 遇到问题？

<details>
<summary><b>出了问题不知道怎么说</b></summary>
说「有问题」。AutoCode 问你简单问题。在终端里搞不定，它教你截图传到 claude.ai。
</details>

<details>
<summary><b>/plugin 不好使</b></summary>
直接说：「帮我安装autocode插件，地址 github.com/ilang-ai/autocode」。说话比命令好使。
</details>

<details>
<summary><b>弹框看不懂</b></summary>
选数字最大的。AutoCode 是纯文本文件，放心同意。
</details>

<details>
<summary><b>连不上服务器</b></summary>
到 Vultr 后台核对 IP、用户名、密码。服务器必须是绿色 "Running"。
</details>

<details>
<summary><b>安全吗？</b></summary>
100% 开源，纯文本。Claude Code 自己审查过："没有恶意内容。"
</details>

<details>
<summary><b>多少钱？</b></summary>
AutoCode 永久免费（MIT）。云电脑 6 美元/月（新用户有 300 美元 Vultr 免费额度）。加上 Anthropic API 费用。
</details>

---

<div align="center">

[ilang.ai](https://ilang.ai) · [ilang.cn](https://ilang.cn) · [Hugging Face](https://huggingface.co/datasets/i-Lang/AutoCode) · [@adsorgcn](https://x.com/adsorgcn)

**iLang Research · iLang Inc. · Canada · MIT · 永久免费**

*你说一句话。AutoCode 做出来，放上线。基于 [iLang v5.0](https://ilang.cn)。*

</div>

---

## 引用

[CITATION.cff](../CITATION.cff)；Zenodo 为每个发布版本存档。总 DOI [10.5281/zenodo.22865145](https://doi.org/10.5281/zenodo.22865145)（覆盖所有版本）。
