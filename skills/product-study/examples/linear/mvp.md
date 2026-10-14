# MVP hand-off

Product: Linear · Official site: https://linear.app · Studied on: 2026-10-13 · Goal: 十人软件团队的轻量工单工具，键盘优先，不要企业功能

Source blueprint: blueprint.md (same folder). Build only what is below; the rest of the blueprint is context, not scope.

## MVP cut

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
1. 用户做：用邮箱和密码登录 → 应看到：团队的工单列表 → 机器验：登录后请求工单列表返回 200 且条数等于种子数据。
2. 用户做：全程不用鼠标，按 C 新建、j/k 选中、Enter 打开、快捷键改为已完成 → 应看到：这条工单出现在「已完成」 → 机器验：该工单 status 字段为 done，且过程中没有鼠标事件。
3. 用户做：在一条工单下留评论并 @ 另一名成员 → 应看到：对方刷新后看到评论 → 机器验：评论记录含被 @ 成员的 id。
4. 用户做：新建一个项目，加入三条工单，完成其中一条 → 应看到：项目页显示 1/3 → 机器验：完成比例字段等于 0.333。
5. 用户做：开启两周一轮的周期，放入工单，让周期到期 → 应看到：未完成的工单出现在下一个周期 → 机器验：到期后未完成工单的 cycle 字段指向下一周期。

**Learned vs own 学来的 / 自己定的:**
- 学来的：工单状态流、键盘优先的新建和导航（C / j / k / Enter）、周期（cycle）到期自动顺延、项目完成比例的概念 [S1][S2]。
- 自己定的：界面、配色、布局、全部文案、默认快捷键以外的交互、数据库结构、部署方式。


## What we will not copy

- 原产品的界面外观、布局、配色、图标和字体：我们自己设计一套。
- 原产品的文案、截图、图片、Logo，以及属于商标的产品名和功能名。
- 原产品任何仓库或前端包里的代码（本次研究没有涉及任何代码仓库，也没有读取任何打包代码）。
- 任何不在公开页面上的东西：没有使用账号内页面、抓包、反编译或泄露材料。


## Verify

Keep the rules (numbers, formulas, state changes) in one block the acceptance runner can load without a browser; tag the learned ones [learned].
Ship a checks file next to the build (acceptance.js or acceptance.py) that prints one JSON row per machine check; run it with
`python3 <product-study>/scripts/acceptance_run.py <site_dir>` before go-live and again with `--url <live url>` after. The table it prints is what the user sees.
The remaining checks are actions the user performs; list them as actions, never as 'tests passed'.
