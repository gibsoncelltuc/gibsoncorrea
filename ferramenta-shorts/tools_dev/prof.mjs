// profile one frame stage by stage: node prof.mjs <frame> [W H]
import { chromium } from 'playwright'; import http from 'http'; import fs from 'fs'; import path from 'path';
const f = +(process.argv[2]||700); const root = path.resolve(process.env.WEB||'web');
const srv = http.createServer((q, s) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); if (!fs.existsSync(p)) { s.writeHead(404); return s.end(); } s.writeHead(200, { 'Content-Type': p.endsWith('.js') ? 'text/javascript' : 'text/html' }); fs.createReadStream(p).pipe(s); }).listen(0);
await new Promise(r => srv.on('listening', r));
const args = (process.env.CHARGS||'--use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist').split(' ');
const b = await chromium.launch({ args });
const pg = await b.newPage({ viewport: { width: +(process.env.BW||1080), height: +(process.env.BH||1920) } });
pg.on('console', m => console.log('PAGE', m.text())); pg.on('pageerror', e => console.log('ERR', e.message));
await pg.goto(`http://localhost:${srv.address().port}/index.html`);
await pg.waitForFunction(() => window.ready || window.err, null, { timeout: 180000 });
console.log(await pg.evaluate(() => { const gl = document.createElement('canvas').getContext('webgl2'); const e = gl.getExtension('WEBGL_debug_renderer_info'); return e ? gl.getParameter(e.UNMASKED_RENDERER_WEBGL) : 'n/a'; }));
for (let i = 0; i < 4; i++) {
  const r = await pg.evaluate(async (f) => { const t0 = performance.now(); window.renderFrame(f); const t1 = performance.now(); const gl = document.getElementById('c').getContext('webgl2'); const px=new Uint8Array(4); gl.readPixels(0,0,1,1,gl.RGBA,gl.UNSIGNED_BYTE,px); const t2 = performance.now(); const d = window.getFrameDataURL(0.96); const t3 = performance.now(); return { js: t1 - t0, finish: t2 - t1, jpeg: t3 - t2, len: d.length }; }, f + i);
  console.log(JSON.stringify(r));
}
await b.close(); srv.close();
