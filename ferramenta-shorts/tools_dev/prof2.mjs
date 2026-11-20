import { chromium } from 'playwright'; import http from 'http'; import fs from 'fs'; import path from 'path';
const f = +(process.argv[2]||700); const root = path.resolve(process.env.WEB||'web');
const srv = http.createServer((q, s) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); if (!fs.existsSync(p)) { s.writeHead(404); return s.end(); } s.writeHead(200, { 'Content-Type': p.endsWith('.js') ? 'text/javascript' : 'text/html' }); fs.createReadStream(p).pipe(s); }).listen(0);
await new Promise(r => srv.on('listening', r));
const b = await chromium.launch({ args: (process.env.CHARGS||'--use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist').split(' ') });
const pg = await b.newPage({ viewport: { width: +(process.env.BW||1080), height: +(process.env.BH||1920) } });
pg.on('pageerror', e => console.log('ERR', e.message));
await pg.addInitScript(() => {
  const P = WebGL2RenderingContext.prototype; window.__seg = []; window.__on = false; let cur = null, px = new Uint8Array(4);
  const flush = (gl, label) => { if (!window.__on || !cur) return; gl.readPixels(0,0,1,1,gl.RGBA,gl.UNSIGNED_BYTE,px); cur.ms = performance.now() - cur.t0; window.__seg.push(cur); cur = null; };
  const ob = P.bindFramebuffer; P.bindFramebuffer = function(t, fb) { if (window.__on) { if (cur && t === this.FRAMEBUFFER) { const prev = this.getParameter(this.FRAMEBUFFER_BINDING); this.bindFramebuffer = ob; ob.call(this, t, prev); flush(this); this.bindFramebuffer = P.bindFramebuffer; } if (t === this.FRAMEBUFFER || t===this.DRAW_FRAMEBUFFER) cur = { t0: performance.now(), draws: 0, tris: 0, vp: this.getParameter(this.VIEWPORT).join('x') }; } return ob.call(this, t, fb); };
  for (const n of ['drawElements','drawArrays','drawElementsInstanced','drawArraysInstanced']) { const o = P[n]; P[n] = function(mode, a, b2, c, d) { if (cur) { cur.draws++; cur.tris += (n.includes('Elements') ? b2 : a === undefined ? 0 : b2) / 3; } return o.apply(this, arguments); }; }
  window.__flush = () => { const gl = document.getElementById('c').getContext('webgl2'); flush(gl); };
});
await pg.goto(`http://localhost:${srv.address().port}/index.html`);
await pg.waitForFunction(() => window.ready || window.err, null, { timeout: 180000 });
await pg.evaluate((f) => { window.renderFrame(f); window.getFrameDataURL(0.9); }, f);
for (let i = 1; i < 3; i++) {
  const r = await pg.evaluate((f) => { window.__seg.length = 0; window.__on = true; window.renderFrame(f); window.__flush(); window.__on = false; return window.__seg.map(s => [s.ms|0, s.draws, s.tris|0, s.vp]); }, f + i);
  console.log(JSON.stringify(r));
}
await b.close(); srv.close();
