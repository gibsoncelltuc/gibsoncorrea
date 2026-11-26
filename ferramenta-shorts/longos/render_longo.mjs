// node render_longo.mjs <outdir> <f0> <f1> <workers>  -> frames f%05d.jpg 1920x1080 (paralelo, pula os que ja existem)
import { chromium } from 'playwright'; import http from 'http'; import fs from 'fs'; import path from 'path';
const [,, outdir, a0, a1, nw = '4'] = process.argv; const F0 = +a0, F1 = +a1, NW = +nw;
fs.mkdirSync(outdir, { recursive: true });
const root = path.resolve('www');
const srv = http.createServer((q, s) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); if (!fs.existsSync(p)) { s.writeHead(404); return s.end(); } s.writeHead(200, { 'Content-Type': p.endsWith('.js') ? 'text/javascript' : p.endsWith('.html') ? 'text/html' : p.endsWith('.json') ? 'application/json' : 'application/octet-stream' }); fs.createReadStream(p).pipe(s); }).listen(0);
await new Promise((r) => srv.on('listening', r));
const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const todo = []; for (let f = F0; f <= F1; f++) if (!fs.existsSync(path.join(outdir, `f${String(f).padStart(5, '0')}.jpg`))) todo.push(f);
let k = 0, done = 0; const t0 = Date.now();
await Promise.all([...Array(NW)].map(async () => {
  const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } }); pg.on('pageerror', (e) => console.log('ERR', e.message));
  await pg.goto(`http://localhost:${srv.address().port}/doc.html`); await pg.waitForFunction(() => window.ready, null, { timeout: 180000 });
  while (k < todo.length) { const f = todo[k++]; const d = await pg.evaluate(([f]) => { window.renderFrame(f); return window.getFrame(0.9); }, [f]);
    fs.writeFileSync(path.join(outdir, `f${String(f).padStart(5, '0')}.jpg`), Buffer.from(d.split(',')[1], 'base64'));
    if (++done % 300 === 0) console.log(`${done}/${todo.length} quadros, ${((Date.now() - t0) / done / 1000 * NW).toFixed(2)} s/quadro/navegador`); }
}));
console.log(`fim: ${done} quadros em ${((Date.now() - t0) / 60000).toFixed(1)} min`); await b.close(); srv.close();
