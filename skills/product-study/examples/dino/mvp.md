# MVP hand-off

Product: T-Rex Runner（Chrome 离线小恐龙） · Official site: https://wayou.github.io/t-rex-runner/ · Studied on: 2026-10-14 · Goal: 给不会编程的人一个自己的恐龙小游戏：能跳、有仙人掌、能自己调速度

Source blueprint: blueprint.md (same folder). Build only what is below; the rest of the blueprint is context, not scope.

## MVP cut

**Users and the one job 用户与唯一任务:** 不会编程的人（和他们的孩子）：打开一个网址就能玩的恐龙跳仙人掌，而且能用滑块把速度调到自己想要的档位。

**Objects 对象 (<= 5):** 一局游戏（速度、距离、状态）、恐龙、仙人掌、速度设置（滑块值、是否自动加速）、计分

**Screens 画面 (<= 7):** 游戏画面（含控制条：开始、跳跃、重开、速度滑块、自动加速开关）、结束提示（叠在游戏画面上）

**Dropped from v1 and why 不做的:** 翼龙和下蹲（多一种障碍和一种动作，v1 只要「跳」一个动作）、昼夜反转、成就音效、街机模式、高清精灵图、触屏（v1 先在电脑浏览器跑通，手机点击作为 v1.1）、最高分持久化。

**Build order 构建顺序 (each step ends in something the user can click):**
1. 一个 HTML 文件：画布 + 恐龙方块 + 地面，点「开始」地面开始滚动——用户看到动起来。
2. 空格 / 「跳跃」按钮让恐龙起跳落地（重力 0.6、起跳速度 12 的手感）——用户能跳。
3. 仙人掌从右侧按间隙生成、碰撞即「游戏结束」、「重开」回到起点——用户能玩一整局。
4. 速度滑块 2–18 和当前速度数字：拖动即生效，固定速度——用户能调快调慢。
5. 「自动加速」开关：开启时从 6 开始，每次逻辑更新若速度 < 13 则 +0.001，逻辑更新固定每秒 60 次——用户能复现原版手感。
6. 计分和本局最高分——用户有目标。
7. 上线成一个网址（静态托管，零成本）——用户能把链接发给别人。

**Acceptance 验收 (v1 is done when):**
1. 用户做：打开网址点「开始」 → 应看到：仙人掌从右边移过来 → 机器验：页面加载无报错，开始后 2 秒内生成了障碍。
2. 用户做：按空格 → 应看到：恐龙跳起再落下，页面不滚动 → 机器验：跳跃后恐龙 y 值先减后回到地面；空格的默认行为被阻止。
3. 用户做：把滑块从 3 拖到 12 → 应看到：仙人掌明显变快，旁边数字显示 12 → 机器验：滑块值变化后游戏速度等于滑块值。
4. 用户做：撞到仙人掌，点「重开」 → 应看到：结束提示消失、又能玩 → 机器验：重开后距离为 0、速度回到设定值、状态为进行中。
5. 用户做：打开「自动加速」看数字 → 应看到：从 6.000 开始慢慢涨，到 13 附近停 → 机器验：从 6 起跑 0 / 1000 / 4000 / 10000 次更新后速度为 6.000 / 7.000 / 10.000 / 13.001（三位小数）。

**Learned vs own 学来的 / 自己定的:**
- 学来的（只学规则，不抄代码）：起始速度 6、每次更新 +0.001、上限 13（先判断再相加）、重力 0.6、起跳速度 12 [S2]；开局前等待第一次按键、撞毁后重开保留最高分 [S2]。
- 自己定的：画面与配色、恐龙和仙人掌的形状、控制条和滑块（2–18）、每秒 60 次逻辑更新、开局 1.5 秒无障碍、障碍间隙公式、计分换算、所有文案。


## What we will not copy

- 原版的界面、像素风精灵图、配色、字体和布局：恐龙、仙人掌、地面全部自己画。
- 原版的文案、截图、图片、音效，以及 Chrome / Chromium 的名字和标识。
- 原版仓库的任何代码：它的文件头声明 BSD 风格许可（宽松许可，非 copyleft），但我们只学了它的规则（起始 6、每次更新 +0.001、上限 13、重力 0.6、起跳 12、开局 3 秒无障碍），实现全部重写。
- 没有用任何非公开材料：没有登录、抓包、反编译或泄露资料。


## Verify

Keep the rules (numbers, formulas, state changes) in one block the acceptance runner can load without a browser; tag the learned ones [learned].
Ship a checks file next to the build (acceptance.js or acceptance.py) that prints one JSON row per machine check; run it with
`python3 <product-study>/scripts/acceptance_run.py <site_dir>` before go-live and again with `--url <live url>` after. The table it prints is what the user sees.
The remaining checks are actions the user performs; list them as actions, never as 'tests passed'.
