// 小恐龙跑酷验收检查：加载 <script id="rules"> 纯规则块，逐项验证 mvp.md 的验收行
// 用法：node acceptance.js <html 路径>   逐行输出 {"id","check","expected","actual","ok"}
const fs = require('fs');
const vm = require('vm');

const htmlPath = process.argv[2];
const html = fs.readFileSync(htmlPath, 'utf8');
const m = html.match(/<script id="rules">([\s\S]*?)<\/script>/);
if (!m) { console.error('rules block missing'); process.exit(2); }
const sandbox = {};
vm.createContext(sandbox);
vm.runInContext(m[1], sandbox);
const R = sandbox.DinoRules;
if (!R) { console.error('DinoRules not exported'); process.exit(2); }

function row(id, check, expected, actual, ok) {
  console.log(JSON.stringify({ id: String(id), check, expected: String(expected), actual: String(actual), ok: !!ok }));
}

// 1. 跳跃：跳起后落回地面
{
  const g = R.createGame();
  const jumped = R.jump(g);
  let maxY = 0;
  for (let i = 0; i < 120; i++) { R.tick(g); if (g.y > maxY) maxY = g.y; }
  row(1, '按空格小恐龙跳起再落地', '跳起(最高点>0)并落回地面(y=0)', `jumped=${jumped},最高点=${maxY.toFixed(1)},落地y=${g.y}`, jumped && maxY > 0 && g.y === 0);
}
// 2. 速度滑杆 1x -> 2x，障碍速度翻倍
{
  const g = R.createGame();
  const v0 = g.obstacleVelocity;
  R.setSpeedMultiplier(g, 2);
  row(2, '速度滑杆拖到 2x 障碍变快', `障碍速度 ${v0} -> ${v0 * 2}`, `障碍速度 ${v0} -> ${g.obstacleVelocity}`, g.obstacleVelocity === v0 * 2);
}
// 3. 碰撞 -> 游戏结束
{
  const g = R.createGame();
  R.collide(g);
  row(3, '撞上仙人掌显示游戏结束', "state=gameover", `state=${g.state}`, g.state === 'gameover');
}
// 4. 重开 -> 分数清零、回到起点
{
  const g = R.createGame();
  g.score = 50; R.collide(g); R.reset(g);
  row(4, '按空格重开新的一局', 'score=0,state=running', `score=${g.score},state=${g.state}`, g.score === 0 && g.state === 'running');
}
// 5. 跑 300 帧不操作：涨分且不结束
{
  const g = R.createGame();
  for (let i = 0; i < 300; i++) R.tick(g);
  row(5, '不操作跑 5 秒分数上涨', 'score>0,state=running', `score=${g.score.toFixed(1)},state=${g.state}`, g.score > 0 && g.state === 'running');
}
