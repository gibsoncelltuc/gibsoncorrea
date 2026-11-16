// node abl.mjs <webdir> [frame] [n]  -> ms/frame (sync via readPixels), warm
import { chromium } from 'playwright'; import http from 'http'; import fs from 'fs'; import path from 'path';
const root = path.resolve(process.argv[2]||'web'), f0 = +(process.argv[3]||700), n = +(process.argv[4]||4);
const srv = http.createServer((q, s) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); if (!fs.existsSync(p)) { s.writeHead(404); return s.end(); } s.writeHead(200, { 'Content-Type': p.endsWith('.js') ? 'text/javascript' : 'text/html' }); fs.createReadStream(p).pipe(s); }).listen(0);
await new Promise(r => srv.on('listening', r));
const b = await chromium.launch({ args: (process.env.CHARGS||'--use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist').split(' ') });
const pg = await b.newPage({ viewport: { width: +(process.env.RW||1080), height: +(process.env.RH||1920) } }); pg.on('pageerror', e => console.log('ERR', e.message));
if (process.env.RW) await pg.addInitScript(([w,h]) => { window.RENDER_W = w; window.RENDER_H = h; }, [+process.env.RW, +process.env.RH]);
await pg.goto(`http://localhost:${srv.address().port}/index.html`);
await pg.waitForFunction(() => window.ready || window.err, null, { timeout: 180000 });
const r = await pg.evaluate(async ([f0, n]) => { const gl = document.getElementById('c').getContext('webgl2'); const px = new Uint8Array(4); const out = [];
  for (let i = 0; i < n + 1; i++) { const t0 = performance.now(); window.renderFrame(f0 + i * 37); gl.readPixels(0,0,1,1,gl.RGBA,gl.UNSIGNED_BYTE,px); out.push(Math.round(performance.now() - t0)); } return out; }, [f0, n]);
console.log(path.basename(root), 'ms:', r.join(' '), ' mean(warm)=', Math.round(r.slice(1).reduce((a,b)=>a+b,0)/n));
await b.close(); srv.close();
