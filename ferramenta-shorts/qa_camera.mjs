// Camera QA: flags per-frame camera jumps that are not declared cuts (CUTS), i.e. accidental fly-throughs.
// usage: node qa_camera.mjs web/story.js
import path from 'path'; import url from 'url'; const { camAt, shotAt, TOTAL } = await import(url.pathToFileURL(path.resolve('web/story.js')).href);
import fs from 'fs';
const mod = await import(url.pathToFileURL(path.resolve('web/story.js')).href); const cuts = new Set(mod.SHOTS.map((s) => s.a));
const d3 = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
let bad = 0, prev = camAt(0);
for (let f = 1; f < TOTAL; f++) {
  const c = camAt(f); const near = [...cuts].some((k) => f >= k && f <= k + 1); const sa = shotAt(f - 1).id, sb = shotAt(f).id;
  const jp = d3(c.pos, prev.pos), jl = d3(c.look, prev.look), jf = Math.abs(c.fov - prev.fov); const dist = Math.max(3, d3(c.pos, c.look)); const rel = jp / dist, rell = jl / dist;
  const speed = Math.max(jp, jl * 0.5);
  if (!near && !(c.zb > 0.02 || prev.zb > 0.02) && sa === sb && (rel > 0.12 || rell > 0.3 || jf > 6)) { bad++; console.log(`frame ${f} (${sb}): camera moves ${jp.toFixed(1)} m (${(rel * 100).toFixed(0)}% of its distance to the subject), look ${jl.toFixed(1)} m, fov ${jf.toFixed(1)} in one frame without a cut`); }
  if (!near && sa !== sb && (jp > 1.0)) { /* shot boundary without a flash cut */ if (!cuts.has(f)) { bad++; console.log(`frame ${f}: shot ${sa} -> ${sb} changes location (${jp.toFixed(1)} m) but ${f} is not in CUTS`); } }
  prev = c;
}
console.log(bad ? `${bad} camera problems` : 'camera OK');
process.exit(bad ? 1 : 0);
