// usage: node shot.mjs out.jpg '{"f":10,"cam":{"pos":[..],"look":[..],"fov":30,"focus":3,"cinf":6}}'
import { launch } from './launch.mjs'; import http from 'http'; import fs from 'fs'; import path from 'path';
const [,, out, spec] = process.argv; const jobs = JSON.parse(spec); const list = Array.isArray(jobs) ? jobs : [jobs];
const root = path.resolve('web');
const srv = http.createServer((q, s) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); if (!fs.existsSync(p)) { s.writeHead(404); return s.end(); } s.writeHead(200, { 'Content-Type': p.endsWith('.js') ? 'text/javascript' : 'text/html' }); fs.createReadStream(p).pipe(s); }).listen(0);
await new Promise(r => srv.on('listening', r));
const b = await launch();
const pg = await b.newPage({ viewport: { width: 1080, height: 1920 } }); pg.on('pageerror', e => console.log('ERR', e.message));
if (process.env.GRADE_OFF) await pg.addInitScript(() => { window.GRADE_OFF = true; });
await pg.goto(`http://localhost:${srv.address().port}/index.html`); await pg.waitForFunction(() => window.ready || window.err, null, { timeout: 180000 });
let i = 0;
for (const j of list) { const d = await pg.evaluate(([f, cam, wx]) => { window.TESTCAM = cam || null; window.WXO = wx || null; window.renderFrame(f); return window.getFrameDataURL(0.92); }, [j.f, j.cam || null, j.wx || null]); fs.writeFileSync(out.replace('.jpg', list.length > 1 ? `_${i}.jpg` : '.jpg'), Buffer.from(d.split(',')[1], 'base64')); i++; }
await b.close(); srv.close();
