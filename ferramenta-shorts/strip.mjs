// usage: node strip.mjs <id> <shotId> <n> <out.jpg>  -> n quadros igualmente espacados de uma cena (para ver o MOVIMENTO)
import url from 'url'; import { launch } from './launch.mjs'; import http from 'http'; import fs from 'fs'; import path from 'path'; import { execSync } from 'child_process';
const [,, id, sid, nArg, out] = process.argv; const N = +nArg || 8;
const { SHOTS } = await import(url.pathToFileURL(path.resolve('web/story.js')).href);
const ss = SHOTS.filter((s) => s.id === sid || s.id.startsWith(sid + '~') || s.id.startsWith(sid + '_')); const a = Math.min(...ss.map((s) => s.a)), b = Math.max(...ss.map((s) => s.b));
const root = path.resolve('web'); const srv = http.createServer((q, s) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); if (!fs.existsSync(p)) { s.writeHead(404); return s.end(); } s.writeHead(200, { 'Content-Type': p.endsWith('.js') ? 'text/javascript' : p.endsWith('.html') ? 'text/html' : p.endsWith('.json') ? 'application/json' : 'application/octet-stream' }); fs.createReadStream(p).pipe(s); }).listen(0);
await new Promise(r => srv.on('listening', r)); const br = await launch(); const pg = await br.newPage({ viewport: { width: 300, height: 533 } }); pg.on('pageerror', e => console.log('ERR', e.message));
await pg.addInitScript(() => { window.RENDER_W = 300; window.RENDER_H = 533; }); await pg.goto(`http://localhost:${srv.address().port}/index.html`); await pg.waitForFunction(() => window.ready || window.err, null, { timeout: 240000 });
fs.rmSync('st_tmp', { recursive: true, force: true }); fs.mkdirSync('st_tmp');
const FR = process.env.FRAMES ? process.env.FRAMES.split(',').map(Number) : null;   /* FRAMES=470,477 -> quadros exatos (conferir o instante de uma acao) */
for (let i = 0; i < (FR ? FR.length : N); i++) { const f = FR ? FR[i] : Math.round(a + (b - a) * (i + 0.5) / N); const d = await pg.evaluate((f) => { window.renderFrame(f); return window.getFrameDataURL(0.85); }, f); fs.writeFileSync(`st_tmp/${String(i).padStart(2, '0')}.jpg`, Buffer.from(d.split(',')[1], 'base64')); }
await br.close(); srv.close(); execSync(`ffmpeg -v error -y -pattern_type glob -i "st_tmp/*.jpg" -vf tile=${N}x1 -q:v 4 ${out}`); console.log('ok', a, b);
