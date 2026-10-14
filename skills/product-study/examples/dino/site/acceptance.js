// Acceptance for mvp.md — machine-checkable parts. Prints one JSON row per check (S5 convention).
// Run via: python3 skills/product-study/scripts/acceptance_run.py <site_dir> [--url <live>]
const fs = require('fs'), vm = require('vm');
const html = fs.readFileSync(process.argv[2] || 'index.html', 'utf8');
const rulesSrc = html.match(/<script id="rules">([\s\S]*?)<\/script>/)[1];
const sandbox = { module: { exports: {} } };
vm.runInNewContext(rulesSrc, sandbox);
const R = sandbox.module.exports;
const f3 = n => (Math.round(n * 1000) / 1000).toFixed(3);
const rows = [];
const check = (id, what, expected, actual, ok) => rows.push({ id, check: what, expected: String(expected), actual: String(actual), ok });

// 1. 开始后 2 秒内生成了障碍
{
  const st = R.newState(); R.start(st);
  let firstAt = null;
  for (let i = 1; i <= 120; i++) { R.update(st); if (st.obstacles.length && firstAt === null) firstAt = i; }
  check('1', '开始后 2 秒（120 次更新）内出现障碍', '≤ 120 次更新', firstAt === null ? '未出现' : firstAt + ' 次更新', firstAt !== null && firstAt <= 120);
}
// 2. 跳跃：y 先升后回到地面
{
  const st = R.newState(); R.start(st); R.jump(st);
  let peak = 0, landed = null;
  for (let i = 1; i <= 120; i++) { R.update(st); peak = Math.max(peak, st.dinoY); if (!st.jumping && landed === null && i > 1) landed = i; }
  check('2', '按空格后恐龙跳起再落地', '峰值 > 0 且落地', '峰值 ' + f3(peak) + '，' + (landed ? landed + ' 次更新后落地' : '未落地'), peak > 0 && landed !== null);
}
// 3. 滑块 3 → 12：速度等于滑块值，自动加速关闭
{
  const st = R.newState(); R.setAuto(st, true); R.start(st);
  R.setSliderSpeed(st, 3); const s3 = st.speed; R.setSliderSpeed(st, 12);
  check('3', '滑块拖到 12 后游戏速度', '12.000（自动加速关）', f3(st.speed) + '（自动加速' + (st.auto ? '开' : '关') + '，之前 ' + f3(s3) + '）', st.speed === 12 && !st.auto && s3 === 3);
}
// 4. 重开：距离 0、速度回到设定、状态进行中
{
  const st = R.newState(); R.start(st); R.setSliderSpeed(st, 9);
  for (let i = 0; i < 400; i++) R.update(st);
  st.status = 'crashed'; const dBefore = Math.floor(st.distance);
  R.restart(st);
  check('4', '撞毁后重开', '距离 0，速度 9.000，进行中', '距离 ' + Math.floor(st.distance) + '（之前 ' + dBefore + '），速度 ' + f3(st.speed) + '，' + (st.status === 'playing' ? '进行中' : st.status), st.distance === 0 && st.speed === 9 && st.status === 'playing');
}
// 5. 自动加速：0/1000/4000/10000 次更新后的速度
{
  const ref = { 0: 6.000, 1000: 7.000, 4000: 10.000, 10000: 13.001 };
  for (const n of Object.keys(ref)) {
    const v = R.simulateAcceleration(Number(n));
    check('5', '自动加速 ' + n + ' 次更新后速度', f3(ref[n]), f3(v), f3(v) === f3(ref[n]));
  }
}

for (const r of rows) console.log(JSON.stringify(r));
process.exit(rows.some(r => !r.ok) ? 1 : 0);
