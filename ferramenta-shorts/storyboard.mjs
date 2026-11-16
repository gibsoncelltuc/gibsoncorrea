// usage: node storyboard.mjs <story-id> <out.jpg> [W=360]   -> contact sheet of every take (middle frame, plus a second frame for long takes) with shot id, time and the narration being spoken
import url from 'url'; import { launch } from './launch.mjs'; import http from 'http'; import fs from 'fs'; import path from 'path';
const [,, id, out, wArg] = process.argv; const RW = +(wArg || 360), RH = Math.round(RW * 16 / 9);
const { SHOTS, TOTAL } = await import(url.pathToFileURL(path.resolve('web/story.js')).href);
let phr = []; try { const ph = JSON.parse(fs.readFileSync(`stories/${id}/work/phrases.json`, 'utf8')); phr = ph.phrases || ph.segments || []; } catch (e) {}
const root = path.resolve('web');
const srv = http.createServer((q, s) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); if (!fs.existsSync(p)) { s.writeHead(404); return s.end(); } s.writeHead(200, { 'Content-Type': p.endsWith('.js') ? 'text/javascript' : p.endsWith('.html') ? 'text/html' : 'application/octet-stream' }); fs.createReadStream(p).pipe(s); }).listen(0);
await new Promise(r => srv.on('listening', r));
const b = await launch();
const pg = await b.newPage({ viewport: { width: RW, height: RH } }); pg.on('pageerror', e => console.log('ERR', e.message));
await pg.addInitScript(([w, h]) => { window.RENDER_W = w; window.RENDER_H = h; }, [RW, RH]);
await pg.goto(`http://localhost:${srv.address().port}/index.html`); await pg.waitForFunction(() => window.ready || window.err, null, { timeout: 240000 });
fs.mkdirSync('sb_tmp', { recursive: true }); const list = [];
for (const s of SHOTS) { const len = s.b - s.a; const fr = len > 90 ? [s.a + Math.round(len * 0.25), s.a + Math.round(len * 0.7)] : [s.a + Math.round(len * 0.45)]; for (const f of fr) list.push({ id: s.id, f, t: (f / 30).toFixed(1) }); }
let n = 0; for (const j of list) { const d = await pg.evaluate((f) => { window.renderFrame(f); return window.getFrameDataURL(0.85); }, j.f); fs.writeFileSync(`sb_tmp/${id}_${String(n).padStart(3, '0')}.jpg`, Buffer.from(d.split(',')[1], 'base64')); j.file = `sb_tmp/${id}_${String(n).padStart(3, '0')}.jpg`; n++; }
await b.close(); srv.close();
fs.writeFileSync(out.replace(/\.jpg$/, '.json'), JSON.stringify({ id, TOTAL, list }, null, 1));
console.log('frames', list.length);
