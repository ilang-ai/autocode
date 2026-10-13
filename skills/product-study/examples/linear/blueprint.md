# Product blueprint: Linear

Product: Linear · Official site: https://linear.app · Studied on: 2026-10-13 · Goal: 十人软件团队的轻量工单工具，键盘优先，不要企业功能

阅读说明：本蓝图只描述**结构**（产品做什么、对象之间怎么关联、用户走哪些流程），全部来自文末 Sources 列出的公开页面。它是一张用来设计我们自己产品的地图，不包含原产品的界面、文案、图片或品牌，也没有使用任何非公开来源。置信度标记：{高} = 官方页面明确写了；{中} = 官方页面暗示或由上下文推断；{推测} = 我的判断，没有页面直接说。

## 0. 摘要 Summary

Linear 自称是"面向团队与 AI agent 的产品开发系统"，核心对象是工单（issue）、团队（team）、工作区（workspace），往上用项目（project）和倡议（initiative）组织工作，横向用周期（cycle）做短期规划，用视图（view）从不同角度看同一批工单 [S1, S3]。它最强的地方是速度与专注：工单创建、改属性、分诊、跨团队移动都有单键或组合键快捷方式，并配有命令面板 [S17, S7, S6, S8]。定价按席位：免费版无限成员但限 2 个团队、250 条工单；Basic 每人每月 10 美元；Business 每人每月 16 美元解锁私有团队、分诊智能、洞察等；Enterprise 定制并提供 SAML/SCIM [S2]。近一年的更新几乎全在 AI agent、代码审查（diffs）、Loops 自动化和企业级管控上 [S8]——这些正是我们十人团队不需要的部分，也是我们的轻量版本得以存在的理由。

## 1. 功能清单 Feature inventory

| Feature | What it does (one line) | Tier | Sources | Confidence |
|---|---|---|---|---|
| 工单 Issue | 工作的最小单位，必须属于一个团队，必须有标题和状态，按创建顺序分配编号 | core | S3, S17 | 高 |
| 工作流状态 Workflow | 每个团队自定义的一组有序状态，列表按它分组，看板按它分列，系统给默认流可改 | core | S3 | 高 |
| 团队 Team | 主要组织单位，拥有自己的状态流、周期、标签和工单集合；成员可同时属于多个团队 | core | S3, S5 | 高 |
| 工作区 Workspace | 一家公司的总容器，有唯一 URL，新建时自动生成同名团队 | core | S3, S5 | 高 |
| 项目 Project | 围绕一个结果把工单分组，可跨团队共享，但一条工单同时只能属于一个项目 | core | S3, S6 | 高 |
| 周期 Cycle | 团队重复的时间盒规划期，1 到 8 周，开启后自动生成后续周期 | core | S3, S16 | 高 |
| 视图 View | 对同一批工单的不同过滤/分组方式，不改变工单本身；可保存、可分享 URL | core | S3, S8 | 高 |
| 快捷键与命令面板 | 单键 C 新建工单，Shift P 加入项目，Cmd/Ctrl K 打开模糊搜索的命令面板，G 然后 T 跳到分诊 | core | S17, S6, S7, S8 | 高 |
| 优先级 Priority | 四档：紧急、高、中、低 | core | S17 | 高 |
| 标签 Label | 可按团队或工作区作用域，支持标签组 | core | S5 | 高 |
| 评论 Comment | 工单下的讨论，支持 @ 提及和反应 | core | S3, S17 | 中 |
| 负责人与指派 | 工单可指派给一个人，也可指派给其他团队的人 | core | S3, S5 | 高 |
| 里程碑 Milestone | 项目内部的阶段，带目标日期，按所属工单计算完成度 | plus | S3, S6 | 高 |
| 分诊 Triage | 团队的特殊收件箱，外部成员或集成建的工单先进这里，用 1/2/3/H 接受、拒绝、标重复、暂缓 | plus | S3, S7 | 高 |
| 父子工单 | 工单可拆成子工单，子工单可分到任意团队或成员 | plus | S5, S17 | 中 |
| 估点 Estimate | T 恤尺码映射到点数（XS=1 到 XXXL=21） | plus | S17 | 高 |
| 草稿 Drafts | 关掉弹窗可存为跨设备草稿，保留 6 个月；临时草稿只存本机 | plus | S17 | 高 |
| 模板 Template | 团队级工单/项目/文档模板，可生成预填 URL | plus | S5, S17 | 高 |
| 预填建单链接 | 通过 URL 参数预设标题、状态、团队、优先级、负责人、周期、标签、项目 | plus | S17 | 高 |
| 跨团队移动 | Cmd/Ctrl Shift M 把工单移到别的团队，生成新编号，旧链接仍可跳转 | plus | S17 | 高 |
| 批量选择与撤销 | Cmd/Ctrl A 全选列表，Cmd/Ctrl Z 撤销移动 | plus | S17 | 高 |
| 周期自动化 | 未完成工单自动滚入下一周期；活动中的无周期工单可自动加入当前周期 | plus | S16 | 高 |
| 周期容量 | 未开始的周期显示容量表盘，按前三个周期的速度估算 | plus | S16 | 高 |
| 通知收件箱 Inbox | 汇总需要你处理的通知，新增"优先"标签页把要紧的和可等的分开 | plus | S8, S13 | 高 |
| 项目列表/看板/时间线 | 团队和工作区都有项目页，可按状态、负责人、目标日期分组，可切时间线 | plus | S6 | 高 |
| 描述历史 | 可查看并恢复工单描述的早期版本 | plus | S17 | 高 |
| 团队退役与删除 | 退役后只读保留历史；删除有 30 天恢复期 | plus | S5 | 高 |
| 倡议 Initiative | 项目之上的战略层，可嵌套父子倡议 | drop | S3 | 高 |
| 周期性工单 | 按节奏自动重建的工单 | drop | S17 | 高 |
| 邮件建单与 Asks | 给团队或模板配邮箱地址，外部人发邮件即建单 | drop | S17, S7 | 高 |
| 文档 Documents | 项目内 Markdown 文档与外链资源 | drop | S6 | 高 |
| AI 与代码审查 | Linear Agent、编码会话、Loops、Diffs、引导式审查、分诊智能 | drop | S1, S8 | 高 |
| 洞察与仪表盘 | Insights、Dashboards、进度报告 | drop | S2 | 高 |
| 企业管控 | 私有团队、访客、SAML、SCIM、审计日志、IP 限制、域名认领 | drop | S2, S11 | 高 |
| 原生移动端 | iOS/Android 独立应用，推送与通知时段 | drop | S13 | 高 |

## 2. 信息架构 Information architecture

- 容器嵌套：工作区 > 团队 > 工单；项目横跨一个或多个团队并聚合工单；里程碑挂在项目下；周期属于团队；倡议在项目之上 [S3, S5, S6] {高}
- 侧边栏以团队为单位：你加入的团队出现在侧边栏；浏览未加入的团队时它们临时出现在一个"探索中"分区 [S5] {高}
- 每个团队下固定几页：团队主页、分诊（可选开启）、工单、周期（可选开启）、项目、视图 [S5] {高}
- 工作区级也有一个项目总页和倡议页，用来跨团队看所有项目 [S6, S1] {高}
- 个人入口包括收件箱、我的工单、草稿、收藏 [S1, S17, S8] {中}
- 项目页由概览、工单两个固定标签加任意自定义视图标签组成；Cmd/Ctrl I 开关右侧属性栏 [S6] {高}
- 工单编号格式为"团队标识-序号"，项目编号为"P-团队标识-序号" [S6, S17] {高}
- 团队设置分为：通用（名称、标识、时区、估点）、成员、标签、模板、状态与自动化、分诊、周期、周期性工单 [S5] {高}
- 命令面板（Cmd/Ctrl K）是跨页面的全局入口，可用来搜索、执行动作、复制预填链接 [S17, S8] {高}

## 3. 核心对象与数据模型（推断）Core objects and data model (inferred)

| Object | Key fields | Relations | Sources | Confidence |
|---|---|---|---|---|
| 工作区 Workspace | 名称、URL 子路径 | 1:N 团队；N:M 用户（一人可在多个工作区有账号） | S3 | 高 |
| 团队 Team | 名称、标识符、时区、是否开启估点/周期/分诊 | N:1 工作区；1:N 工单；1:N 周期；1:N 状态；1:N 团队级标签；N:M 成员；N:M 项目 | S3, S5 | 高 |
| 状态 WorkflowStatus | 名称、顺序、类别（分诊/待办/未开始/进行中/已完成/已取消） | N:1 团队；1:N 工单 | S3, S7, S16 | 中 |
| 工单 Issue | 标题（必填）、Markdown 描述、状态（必填）、序号、优先级（4 档）、估点、创建时间 | N:1 团队；N:1 项目（可选）；N:1 周期（可选）；N:1 里程碑（可选）；N:1 负责人；N:M 标签；N:1 父工单；1:N 评论；N:M 关联工单 | S3, S17, S6 | 高 |
| 项目 Project | 名称（必填）、状态（必填）、负责人、图标、概览、开始/目标日期（粒度可到年/半年/季/月/日）、编号 | N:M 团队（其中一个为主导团队）；1:N 工单；1:N 里程碑；1:N 文档与外链；N:1 倡议 | S6, S3 | 高 |
| 里程碑 Milestone | 名称、目标日期、描述、顺序 | N:1 项目；1:N 工单 | S3, S6 | 高 |
| 周期 Cycle | 序号、名称、描述、开始/结束日期、时长（1–8 周）、冷却期 | N:1 团队；1:N 工单 | S16 | 高 |
| 标签 Label | 名称、作用域（团队或工作区）、所属标签组 | N:1 团队或工作区；N:M 工单 | S5 | 高 |
| 评论 Comment | 正文、作者、时间 | N:1 工单；N:1 用户 | S3, S17 | 中 |
| 用户/成员 User | 名称、角色（管理员/成员/访客）、显示名 | N:M 工作区；N:M 团队 | S3, S5, S2 | 中 |
| 倡议 Initiative | 名称、状态（含提议/取消）、优先级、标签 | 1:N 项目；父子倡议 | S3, S8 | 高 |
| 草稿 Draft | 内容、创建时间（6 个月后清理） | N:1 用户 | S17 | 高 |
| 模板 Template | 类型（工单/项目/文档）、预设属性、可选邮箱地址 | N:1 团队 | S5, S17 | 高 |

## 4. 关键用户流程 Key user flows

- 流程 A 上手：先逛公开演示工作区看布局 → 用工作邮箱创建工作区 → 系统自动生成同名团队 → 官方建议小团队全员放一个团队、起步只建一两个团队 [S4, S5] {高}
- 流程 B 建单（键盘）：按 C 弹出创建窗（Alt/Option C 走模板）→ 填标题 → 顺手设优先级/负责人/项目/周期/标签 → 创建后 3 分钟内的属性改动不记入活动日志 → 中途离开则保留临时草稿 [S17] {高}
- 流程 C 推进工单：在详情页直接点标题或描述内联编辑 → 工单沿团队状态流前进 → 需要时 Cmd/Ctrl Shift M 移到别的团队，状态映射到最接近的状态并换新编号 [S17, S3] {高}
- 流程 D 分诊：非本团队成员或集成创建的工单落入分诊队列 → G 然后 T 打开 → 1 接受（进入团队默认状态）/ 2 拒绝（变已取消）/ 3 标重复并合并到原单 / H 暂缓 → 可要求必须先设优先级才能离开分诊 [S7] {高}
- 流程 E 周期规划：团队设置里开启周期，选时长、起始星期、未来周期数（最多 15 个）→ 把工单放进当前或未来周期 → 周期结束未完成工单自动滚入下一周期，但移到待办/分诊/取消的不滚 → 未开始的周期按前三个周期速度显示容量 [S16] {高}
- 流程 F 项目协作：从团队或工作区项目页按 + 新建，只需名称和状态 → 选中工单 Shift P 加入项目，或在项目视图里按 C 直接建 → 项目页看概览、工单和自定义视图标签、里程碑与进度图 → 可多团队共享，但只有一个主导团队决定可用项目状态 [S6] {高}
- 流程 G 找东西：Cmd/Ctrl K 命令面板模糊搜索 → 用过滤条件做自定义视图 → 复制 URL（或 Cmd/Ctrl Shift C）把过滤后的视图分享给同事 [S17, S8, S3] {高}

## 5. 技术栈线索 Technical stack clues

- 公开 API 是 GraphQL，认证支持 OAuth 2.0 和个人 API key；文档覆盖分页、过滤、限流、弃用、webhook、附件 [S9] {高}
- 官方提供 TypeScript SDK（强类型模型与操作），以及 CLI 导入器 [S9] {高}
- 对外提供 MCP 服务器，供 Cursor、Claude、ChatGPT、Windsurf 等 AI 客户端读写数据 [S10, S8] {高}
- 移动端用原生 Swift 与 Kotlin 编写，不是 WebView 套壳 [S13] {高}
- 存在桌面应用，部分快捷键和创建命令为桌面端专有 [S8] {高}
- 招聘页把"构建同步引擎"列为团队公开分享的工程主题，说明客户端与服务端之间有实时同步层 [S12] {中}
- 工单与项目描述、文档统一使用 Markdown [S6, S17] {高}
- 传输强制 HTTPS + TLS 1.2，静态数据 AES-256 加密；创建工作区时可选数据放在欧盟或美国 [S11] {高}
- 登录方式：Google SSO、邮箱验证码、Passkeys；SAML/SCIM 仅企业版 [S11, S2] {高}
- 支持通过 URL 查询参数预填新建工单（标题、团队、状态、优先级等） [S17, S9] {高}
- webhook 出口 IP 公布在站点的 .well-known 路径下 [S8] {高}
- 工单描述有版本历史并可回滚；文档支持作者归属标识 [S17, S8] {高}
- 在招岗位以全栈/产品工程师、移动端设计师、AI 产品工程师为主，公司全远程 [S12] {中}

## 6. 定价与商业模式 Pricing and business model

| Plan | Price | What it unlocks | Sources | Confidence |
|---|---|---|---|---|
| Free | 0 美元 | 无限成员、2 个团队、250 条工单、10MB 文件上传、Agent 平台 | S2 | 高 |
| Basic | 每人每月 10 美元（年付） | 5 个团队、无限工单、无限上传、管理员角色 | S2 | 高 |
| Business | 每人每月 16 美元（年付） | 无限团队、私有团队与访客、分诊智能、Loops、代码智能、Insights、Asks、Zendesk/Intercom 集成 | S2 | 高 |
| Enterprise | 定制价，仅年付 | 发票/PO 付款、SAML 与 SCIM、细粒度管理、高级安全、组织建模、迁移与优先支持、客户经理 | S2 | 高 |

- 按席位计费，团队数量是各档的主要门槛：2 / 5 / 无限 / 无限 [S2, S5] {高}
- AI 相关功能（编码会话、Loops）在订阅之外另按 AI 额度计费，管理员可查看用量并设上限 [S2, S8] {高}
- 私有团队、团队级项目状态与项目标签、分诊自动化都从 Business 起 [S5, S6, S7] {高}
- 引导式代码审查在 2026 年 10 月下放到了 Basic 档 [S8] {高}
- 官网宣称超过 4 万家公司/产品团队在用 [S1, S2] {高}

## 7. 集成与生态 Integrations and ecosystem

- 集成目录按用途分类：基础、Agent、AI 客户端、工程、缺陷上报、自动化、客户体验、安全合规、分析、协作、媒体设计 [S10] {高}
- 官方自建集成：GitHub、GitLab、Slack、Figma、Intercom、Zendesk、Front、Notion、Google Sheets、Zapier、Jira 迁移、邮件建单 [S10] {高}
- 编码 agent 可直接领取工单：Codex、Cursor、GitHub Copilot、Devin、Factory、Sentry [S10] {高}
- GitHub 集成覆盖 PR 自动化、在 Linear 内审代码、工单同步；状态流可配 git 自动化与分支命名 [S10, S5] {高}
- 分诊责任轮值可接 PagerDuty、OpsGenie、Rootly、incident.io 的排班 [S7] {高}
- 周期可订阅为日历（Google Calendar 或 .ics） [S16] {高}
- 数据进出：CSV 导出团队工单、从 Jira/GitHub 导入、工作区迁移、Airbyte/Fivetran 同步 [S5, S8, S10, S9] {高}
- 开发者入口：GraphQL API、webhook、TypeScript SDK、OAuth 应用、Agent 交互指南 [S9] {高}
- 移动端 iOS/Android 原生应用，支持实时推送与自定义通知时段 [S13] {高}

## 8. 空白与差异化机会 Gaps and differentiation opportunities

- 免费版封顶 250 条工单、2 个团队 [S2] {高}；一个活跃的十人软件团队几个月就会触顶，被迫付费 {推测}
- 近 12 个月的更新几乎都在 AI agent、编码会话、Loops、diffs 和企业管控 [S8] {高}；产品重心已经偏向大组织和 AI 工作流，对只想要干净工单的小团队是噪音 {推测}
- 定价页上大部分高级能力（分诊智能、洞察、Asks、私有团队）都从 Business 起 [S2] {高}；十人团队用不上，却要为整套系统的复杂度买单 {推测}
- 官方自己建议小团队全员一个团队最简单 [S5] {高}；所以我们的 v1 可以直接把"一个工作区 = 一个团队"写死，省掉整层团队管理 {推测}
- 项目文档承认"持续性工作"没有好方案，只能靠无目标日期的项目或自定义状态绕 [S6] {高}；轻量版可以给"长期事务"一个明确归属 {推测}
- 周期一次只能看一个团队 [S5] {高}；单团队产品天然没有这个问题 {推测}
- 临时草稿只存本机，登出即丢 [S17] {高}
- 数据存放只能选欧盟或美国 [S11] {高}；自托管或境内部署是留白，小团队可以用一个容器自己跑 {推测}
- 移动端是独立原生应用 [S13] {高}；我们 v1 用响应式网页即可，不做原生 {推测}
- 状态流配置页公开文档取不到（404） [S8] {中}；我们的状态类别只能从概念页和周期页侧面推断，v1 用固定五类状态即可 {推测}
- 快捷键体系是它的核心体验，但散落在各个文档页 [S17, S7, S6] {高}；我们可以把快捷键表当作一等公民，在产品内一处可查 {推测}

## 9. MVP 切分 MVP cut

**Users and the one job:** 一个十人软件团队，一个工作区就是一个团队；唯一要做好的事：不碰鼠标也能快速录入、推进、按周期规划工单。

**Objects 对象 (<= 5):** 成员(User)、工单(Issue)、项目(Project)、周期(Cycle)、评论(Comment)

**Screens 界面 (<= 7):** 登录页、工单列表（按状态分组）、工单详情（含评论）、新建工单弹窗（C 触发）、项目页（列表加单个项目的工单与进度）、周期页（当前/下一/历史）、设置页（团队名与成员邀请）

**Dropped from v1 and why:** 多团队与子团队（单团队写死，省掉整层管理）；倡议、里程碑（十人团队用项目就够）；分诊、模板、邮件建单、周期性工单（都是进件流程，v1 先由成员自己建单）；草稿、描述历史、父子工单、估点（好用但可分离，v2 再加）；GitHub/Slack 等任何第三方集成（v1 不做集成）；AI、代码审查、Loops、洞察、仪表盘（不是轻量工单工具的事）；私有团队、访客、SAML、SCIM、审计（企业功能，用户明确不要）；原生移动端（响应式网页替代）。状态固定为五类：待办、未开始、进行中、已完成、已取消，不做自定义状态流；标签做成工单上的简单文本标签，不单独建对象；认证只用邮箱加密码；部署目标只有一个：一个 Docker 容器（Web 服务 + SQLite）跑在一台服务器上。

**Build order (each step ends in something the user can click):**
1. 脚手架 + 邮箱密码登录 + 初始化单团队：登录后能看到一个空的工单列表和侧边栏。
2. 工单主循环：按 C 弹出新建窗（标题必填）、列表按状态分组、j/k 上下移动、Enter 打开详情、详情页内联改标题和描述；工单编号为"团队标识-序号"。
3. 工单属性与快捷键：状态五类、优先级四档、负责人、文本标签；在列表或详情里用单键改状态/优先级/负责人；Cmd/Ctrl K 命令面板可搜索工单和执行这些动作；产品内有一页快捷键表。
4. 评论：详情页下方评论线程，支持 @ 提及成员。
5. 项目：新建项目只需名称和状态；选中工单按 Shift P 加入项目；项目页显示该项目的工单和完成比例。
6. 周期：设置里开启周期（选时长 1–4 周和起始星期），自动生成当前与下一个周期；工单可放入周期；周期到期时未完成的工单自动滚入下一个周期。
7. 设置与上线：邀请成员（生成邀请链接）、改团队名与标识；打包为一个 Docker 容器部署到一台服务器，用 HTTPS 访问。

**Acceptance (v1 is done when):**
- 一名成员用邮箱和密码登录后，能看到团队的工单列表。
- 全程不用鼠标：按 C 新建一条工单，用 j/k 选中它，按 Enter 打开，再用快捷键把状态改为已完成。
- 在一条工单下留评论并 @ 另一名成员，对方刷新后能看到评论。
- 新建一个项目，把三条工单加入，项目页显示正确的完成比例。
- 开启两周一轮的周期，把工单放进当前周期；周期到期后，未完成的工单出现在下一个周期里。

## 10. 我们不会复制的东西 What we will not copy

- 原产品的界面外观、布局、配色、图标和字体：我们自己设计一套。
- 原产品的文案、截图、图片、Logo，以及属于商标的产品名和功能名。
- 原产品任何仓库或前端包里的代码（本次研究没有涉及任何代码仓库，也没有读取任何打包代码）。
- 任何不在公开页面上的东西：没有使用账号内页面、抓包、反编译或泄露材料。

## Sources

<!-- Generated by `blueprint.py sources <slug>` from sources.json. Do not edit by hand. -->

- [S1] Linear – The system for product development — https://linear.app/ (fetched 2026-10-12, sha256 5803e801696a)
- [S2] Pricing – Linear — https://linear.app/pricing (fetched 2026-10-12, sha256 3a1d210e0b6f)
- [S3] Concepts – Linear Docs — https://linear.app/docs/conceptual-model (fetched 2026-10-12, sha256 87d1a6f62177)
- [S4] Start Guide – Linear Docs — https://linear.app/docs/start-guide (fetched 2026-10-12, sha256 bc3a11015a64)
- [S5] Teams – Linear Docs — https://linear.app/docs/teams (fetched 2026-10-12, sha256 cd981d791929)
- [S6] Projects – Linear Docs — https://linear.app/docs/projects (fetched 2026-10-12, sha256 7ab8146b84b8)
- [S7] Triage – Linear Docs — https://linear.app/docs/triage (fetched 2026-10-12, sha256 6e74cfc2f76e)
- [S8] Changelog – Linear — https://linear.app/changelog (fetched 2026-10-12, sha256 b4be4fc828ce)
- [S9] Linear Developers — https://linear.app/developers (fetched 2026-10-12, sha256 92d1f388b49b)
- [S10] Integrations – Linear — https://linear.app/integrations (fetched 2026-10-12, sha256 c507f72b63b9)
- [S11] Security – Linear — https://linear.app/security (fetched 2026-10-12, sha256 36258ee73036)
- [S12] We're hiring – Linear — https://linear.app/careers (fetched 2026-10-12, sha256 cc7b06d13369)
- [S13] Linear Mobile – Available for iOS and Android — https://linear.app/mobile (fetched 2026-10-12, sha256 4d89da62dc27)
- [S14] Linear Method – Practices for building — https://linear.app/method (fetched 2026-10-12, sha256 185ac408692b)
- [S15] An AI product system for modern enterprises — https://linear.app/enterprise (fetched 2026-10-12, sha256 f681f9490d60)
- [S16] Cycles – Linear Docs — https://linear.app/docs/use-cycles (fetched 2026-10-12, sha256 fb01973bd6c9)
- [S17] Issues – Linear Docs — https://linear.app/docs/creating-issues (fetched 2026-10-12, sha256 f3759e2581fe)

Refused or skipped (out of scope by policy, not used):

- https://linear.app/docs/configuring-workflows — HTTP 404
