import { chromium } from 'playwright'; import http from 'http'; import fs from 'fs'; import path from 'path';
const root = path.resolve(process.argv[2]), frames = (process.argv[3]||'700,740,1000,1400').split(',').map(Number);
const srv = http.createServer((q, s) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); if (!fs.existsSync(p)) { s.writeHead(404); return s.end(); } s.writeHead(200, { 'Content-Type': p.endsWith('.js') ? 'text/javascript' : 'text/html' }); fs.createReadStream(p).pipe(s); }).listen(0);
await new Promise(r => srv.on('listening', r));
const b = await chromium.launch({ args: (process.env.CHARGS||'--use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist').split(' ') });
const pg = await b.newPage({ viewport: { width: 1080, height: 1920 } }); pg.on('pageerror', e => console.log('ERR', e.message));
await pg.goto(`http://localhost:${srv.address().port}/index.html`); await pg.waitForFunction(() => window.ready || window.err, null, { timeout: 180000 });
await pg.evaluate(() => { window.renderFrame(0); });
for (const f of frames) { const r = await pg.evaluate((f) => { window.__T = {}; const t0 = performance.now(); window.renderFrame(f); const t1 = performance.now(); const o = {}; for (const k in window.__T) o[k] = Math.round(window.__T[k]); const d = window.getFrameDataURL(0.96); o.total = Math.round(performance.now() - t0); o.enc = Math.round(performance.now() - t1) ; return o; }, f); console.log(f, JSON.stringify(r)); }
await b.close(); srv.close();
