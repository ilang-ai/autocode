# MVP hand-off

Product: Chrome 小恐龙跑酷（Dinosaur Game）· Official site: https://github.com/wayou/t-rex-runner · Studied on: 2026-10-15 · Goal: 给不懂编程的用户做一个可以自己调速度的小恐龙跑酷游戏，一次会话内可玩、可上线

Source blueprint: blueprint.md (same folder). Build only what is below; the rest of the blueprint is context, not scope.

## MVP cut

**Users and the one job 用户与唯一目标：** 不懂编程的用户，想要一个"像 Chrome 断网小恐龙、但速度自己说了算"的跑酷游戏，打开就能玩。

**Objects 对象 (<= 5):** 小恐龙、仙人掌障碍、地面场景、分数、速度控制器

**Screens 屏幕 (<= 7):** 游戏主屏（含速度滑杆）、游戏结束面板

**Dropped from v1 and why v1 不做的：** 翼龙（障碍先只做一种）、下蹲（跳跃已够用）、昼夜交替（纯视觉）、音效、最高分存档——v1 只保"跑、跳、调速、结束重开"。

**Build order 构建顺序 (each step ends in something the user can click):**
1. 静态页面：画布上的小恐龙 + 地面，按空格能跳 → 能跳的小恐龙
2. 加入仙人掌障碍与碰撞，撞到显示结束面板、空格重开 → 可玩的一局
3. 加入计分与速度滑杆 → 用户可调速的完整游戏
4. 写验收检查并跑通 → 验收表全绿

**Acceptance 验收 (v1 is done when):**
1. 用户按空格 -> 小恐龙跳起再落地，落地前可再跳 -> machine: rules.jump() 后 y 坐标先升后降并回到地面值
2. 用户把速度滑杆从 1x 拖到 2x -> 障碍物和背景明显变快 -> machine: rules.setSpeedMultiplier(2) 后 obstacleVelocity 翻倍
3. 用户故意撞上仙人掌 -> 显示游戏结束面板，显示本局分数 -> machine: rules.collide() 后 state 为 gameover
4. 用户按空格重开 -> 分数清零、小恐龙回到起点重新跑 -> machine: rules.reset() 后 score 为 0 且 state 为 running
5. 用户什么都不按跑 5 秒 -> 分数上涨且游戏不结束 -> machine: 300 帧后 score 大于 0 且 state 为 running

**Learned vs own 学来的 / 自己定的:** 学来的规则与数字：重力 0.6、跳跃初速 12、初速 6 上限 13、障碍最大连续 3 个、障碍间距系数 0.6、速降系数 3 [S3]；其余一切——外观、配色、速度滑杆的形式、分数算法——都是我们自己的设计。


## What we will not copy

- Interface look, layout, colors, icons and typography of the original: we design our own.
- Copy, screenshots, images, logo, product and feature names that are trademarks.
- Any code from the original's repositories or bundles. Studied repo license is BSD-3-Clause (not copyleft); its constants informed our rules, none of its code is used.
- Anything that was not on a public page: no account areas, captures, decompilation or leaked material were used.


## Verify

Keep the rules (numbers, formulas, state changes) in one block the acceptance runner can load without a browser; tag the learned ones [learned].
Ship a checks file next to the build (acceptance.js or acceptance.py) that prints one JSON row per machine check; run it with
`python3 <product-study>/scripts/acceptance_run.py <site_dir>` before go-live and again with `--url <live url>` after. The table it prints is what the user sees.
The remaining checks are actions the user performs; list them as actions, never as 'tests passed'.
