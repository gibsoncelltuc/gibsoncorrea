// usage: node render_cb.mjs <spec> <outdir> <frames "a-b"|"1,2"> [step]   (screenshot da pagina: 3D + texto em DOM)
import { chromium } from 'playwright'; import http from 'http'; import fs from 'fs'; import path from 'path';
const [,, spec, outdir, fr, step = '1'] = process.argv; fs.mkdirSync(outdir, { recursive: true });
let frames = []; for (const p of fr.split(',')) { if (p.includes('-')) { const [a, b] = p.split('-').map(Number); for (let f = a; f <= b; f += +step) frames.push(f); } else frames.push(+p); }
const root = path.resolve('web'); const mime = { '.js': 'text/javascript', '.json': 'application/json', '.html': 'text/html', '.otf': 'font/otf', '.glb': 'model/gltf-binary', '.png': 'image/png' };
const srv = http.createServer((q, s) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); if (!fs.existsSync(p) || fs.statSync(p).isDirectory()) { s.writeHead(404); return s.end(); } s.writeHead(200, { 'Content-Type': mime[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(s); }).listen(0);
await new Promise(r => srv.on('listening', r));
const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const pg = await b.newPage({ viewport: { width: 1080, height: 1920 } });
pg.on('console', m => console.log('PAGE', m.text())); pg.on('pageerror', e => console.log('ERR', e.message));
await pg.goto(`http://localhost:${srv.address().port}/countryball/index.html#${spec}`);
await pg.waitForFunction(() => window.ready || window.err, null, { timeout: 180000 });
if (await pg.evaluate(() => window.err)) { console.log('page error'); process.exit(1); }
const t0 = Date.now();
for (const f of frames) { const o = path.join(outdir, `f${String(f).padStart(4, '0')}.jpg`); if (process.env.RESUME && fs.existsSync(o)) continue; await pg.evaluate(f => window.renderFrame(f), f); await pg.screenshot({ path: o, type: 'jpeg', quality: 92 }); }
console.log(`done ${frames.length} frames, ${((Date.now() - t0) / frames.length / 1000).toFixed(2)} s/frame`); await b.close(); srv.close();
