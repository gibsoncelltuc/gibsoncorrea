// TAKE INSPECTOR — runs BEFORE rendering. For every take it projects each character/animal into the camera and checks the declared intent (HEROES in story.js):
//  hero fully inside the frame ('full'), head+torso ('medium'), face ('close'); minimum size; hero occluded by scenery/props; empty takes; camera inside geometry.
// usage: node qa_takes.mjs [step=6] [--json qa_takes.json]       exit code 1 when any take fails
import url from 'url'; import { launch } from './launch.mjs'; import http from 'http'; import fs from 'fs'; import path from 'path';
const { SHOTS, TOTAL, HEROES } = await import(url.pathToFileURL(path.resolve('web/story.js')).href);
const step = +(process.argv[2] && !process.argv[2].startsWith('--') ? process.argv[2] : 6); const only = process.argv.includes('--shots') ? process.argv[process.argv.indexOf('--shots') + 1].split(',') : null;
const root = path.resolve('web');
const srv = http.createServer((q, s) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); if (!fs.existsSync(p)) { s.writeHead(404); return s.end(); } s.writeHead(200, { 'Content-Type': p.endsWith('.js') ? 'text/javascript' : 'text/html' }); fs.createReadStream(p).pipe(s); }).listen(0);
await new Promise(r => srv.on('listening', r));
const b = await launch();
const pg = await b.newPage({ viewport: { width: 540, height: 960 } }); pg.on('pageerror', e => console.log('PAGE ERROR', e.message));
await pg.addInitScript((k) => { window.KFIT = k; }, process.env.KFIT ? JSON.parse(process.env.KFIT) : null);
await pg.goto(`http://localhost:${srv.address().port}/index.html`); await pg.waitForFunction(() => window.ready, null, { timeout: 180000 });
const frames = new Set(); for (let f = 0; f < TOTAL; f += step) frames.add(f); for (const s of SHOTS) { frames.add(s.a); frames.add(s.b); frames.add(Math.round((s.a + s.b) / 2)); }
const inOnly = (f) => !only || SHOTS.some((s) => only.includes(s.id) && f >= s.a && f <= s.b);
const isChar = (a) => a.id !== 'bird' && a.id !== undefined;   // persons, 2D animals and 3D animals (bear/horse/emu)
const fails = [], perShot = {}, tinyBy = {};
for (const f of [...frames].filter(inOnly).sort((x, y) => x - y)) {
  const r = await pg.evaluate((f) => window.inspectFrame(f), f); const HR = HEROES[r.shot] || { hero: 'any', frame: 'medium' }; const H = Array.isArray(HR) ? (HR.find((x) => f >= (x.from ?? -1) && f <= (x.to ?? 1e9)) || HR[0]) : HR; const why = [];
  if (r.cameraInside) why.push(`camera inside geometry (${r.cameraInside})`);
  const chars = r.actors.filter(isChar);
  const match = (a) => H.hero === 'any' ? isChar(a) : (a.id === H.hero || (H.hero === 'US' && (a.id === 'US' || a.id === 'pickett')));
  const heroes = r.actors.filter(match);
  const inM = 0.015;
  const judge = (a) => { const w = []; const [x0, y0, x1, y1] = a.box;
    if (a.behind) return [`${a.id}: behind the camera`];
    if (H.frame === 'full' && (x0 < inM || x1 > 1 - inM || y0 < 0.01 || y1 > 0.99)) w.push(`${a.id}: CROPPED (box ${a.box.join(', ')}; ${Math.round((1 - a.visible) * 100)}% outside)`);
    { const h = y1 - y0, ty = y0 + (H.frame === 'close' ? 0.3 : 0.55) * h; if ((H.frame === 'medium' || H.frame === 'close') && (y0 < 0 || ty > 1.0 || x0 < -0.02 || x1 > 1.02)) w.push(`${a.id}: ${H.frame === 'close' ? 'face' : 'head/torso'} cropped (box ${a.box.join(', ')})`); }
    const minH = H.minH ?? (H.frame === 'full' ? 0.1 : H.frame === 'medium' ? 0.16 : 0.3); if (a.heightFrac < minH) w.push(`${a.id}: too small (${(a.heightFrac * 100).toFixed(0)}% of frame height, min ${(minH * 100).toFixed(0)}%)`);
    if (a.occluded >= 1) w.push(`${a.id}: HIDDEN behind ${a.occluder}`);
    return w; };
  if (H.hero !== 'none') {
    if (!heroes.length) { if (!H.optional) why.push(H.hero === 'any' ? 'empty take: no character in the take' : `hero '${H.hero}' is not in the take at all`); }
    else { const res = heroes.map(judge); if (H.all) { for (const w of res) why.push(...w); } else if (!res.some((w) => w.length === 0)) why.push(...res.sort((p, q) => p.length - q.length)[0]); }
  }
  { // GLOBAL composition rules: apply to EVERY take, also hero:none ones (characters readable, never absurdly close, never all gone)
    const vis = chars.filter((a) => !a.behind && a.visible > 0.5), big = vis.length ? Math.max(...vis.map((a) => a.heightFrac)) : 0;
    if (big > 1.25) why.push(`too close: the biggest character is ${Math.round(big * 100)}% of the frame height`);
    if (chars.length && !vis.length && H.hero === 'none') why.push('empty: characters are in the scene but none is in frame');
    (tinyBy[r.shot] = tinyBy[r.shot] || []).push(vis.length > 0 && big < (H.wide ? 0.028 : vis.length >= 6 ? 0.06 : 0.10) ? 1 : 0); }
  (perShot[r.shot] = perShot[r.shot] || []).push({ f, why });
  if (why.length) fails.push({ f, shot: r.shot, why });
}
await b.close(); srv.close();
const byShot = {}; for (const x of fails) (byShot[x.shot] = byShot[x.shot] || []).push(x);
for (const s of SHOTS.filter((s) => !only || only.includes(s.id))) { const bad = byShot[s.id] || [], n = (perShot[s.id] || []).length; console.log(`${bad.length ? 'FAIL' : ' ok '}  ${s.id.padEnd(9)} frames ${s.a}-${s.b}  ${n - bad.length}/${n} sampled frames pass`); const seen = new Set(); for (const x of bad) for (const w of x.why) { const k = w.replace(/\d+/g, '#'); if (!seen.has(k)) { seen.add(k); console.log(`        e.g. frame ${x.f}: ${w}`); } } }
const tiny = Object.entries(tinyBy).filter(([, v]) => v.length >= 3 && v.reduce((x, y) => x + y, 0) / v.length >= 0.5).map(([k]) => k);
for (const t of tiny) console.log(`TINY  ${t}: characters are smaller than the minimum readable size in most of the take (advisory; fit.sh tightens the camera)`);
fs.writeFileSync('qa_takes.json', JSON.stringify({ fails, tiny }, null, 1));
console.log(fails.length ? `\n${fails.length} sampled frames fail -> fix the takes (see qa_takes.json) BEFORE rendering` : '\nALL TAKES OK');
process.exit(fails.length ? 1 : 0);
