// CHECAGEM DE VISIBILIDADE (ordem do Gibson 24/11: "resolva na raiz"). Roda DENTRO do pipeline, logo depois do storyboard (mesma montagem do web/).
// Mede no proprio motor 3D, em 3 quadros de cada tomada:
//   1) OBJETO CITADO: cada objeto que o roteiro pos na cena (beats.json "props", menos decoracao) tem que aparecer de verdade:
//      parte dele dentro do quadro, sem estar tapado (raio da camera ate' o objeto bate nele primeiro) e com tamanho minimo na tela.
//   2) TAPANDO A CAMERA: um mesmo objeto (caixote, poste, casco de navio, parede) cobrindo boa parte do quadro bem perto da lente.
//   3) CAMERA DENTRO DE OBJETO: a lente dentro da caixa de um objeto grande (navio, casa).
// Resultado: stories/<id>/visibilidade.json + linhas "FALHA bN: ..." ; codigo de saida 3 se houver falha (o make_video bloqueia a aprovacao).
// uso: node visivel.mjs <id>
import url from 'url'; import { launch } from './launch.mjs'; import http from 'http'; import fs from 'fs'; import path from 'path';
const [,, id] = process.argv; const RW = 270, RH = 480;
const ST = await import(url.pathToFileURL(path.resolve('web/story.js')).href); const SPEC = ST.SPEC_DEBUG;
const B = JSON.parse(fs.readFileSync(`videos/${id}/beats.json`, 'utf8'));
const DECOR = /picket_fence|haybale|scarecrow|bush|rocks|flowerbed|lamppost|bench|wheelbarrow|barrel|crate|^ship$|kit\/room|kit\/porch|tree|cone_transito|barreira|palete|grade_evento|mk\/(Chair|Table|Bookcase|Chest|Crate|Barrel|Workbench|Bench)/i;
const need = {};   // shot id -> assets que tem que aparecer
for (const s of SPEC.shots) {
  const k = +String(s.id).replace(/^b(\d+).*/, '$1'); const bt = (B.beats || [])[k]; if (!bt) continue;
  const want = new Set((bt.props || []).map((p) => String(p[0])).filter((a) => !DECOR.test(a)));
  if (bt.explica) continue;   // estudio de explicacao: o objeto e' a cena inteira
  need[s.id] = (s.props || []).map((p) => String(p.asset)).filter((a) => want.has(a));
}
const root = path.resolve('web');
const srv = http.createServer((q, s) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); if (!fs.existsSync(p)) { s.writeHead(404); return s.end(); } s.writeHead(200, { 'Content-Type': p.endsWith('.js') || p.endsWith('.mjs') ? 'text/javascript' : p.endsWith('.html') ? 'text/html' : p.endsWith('.json') ? 'application/json' : 'application/octet-stream' }); fs.createReadStream(p).pipe(s); }).listen(0);
await new Promise((r) => srv.on('listening', r));
const br = await launch(); const pg = await br.newPage({ viewport: { width: RW, height: RH } }); pg.on('pageerror', (e) => console.log('ERR', e.message));
await pg.addInitScript(([w, h]) => { window.RENDER_W = w; window.RENDER_H = h; }, [RW, RH]);
await pg.goto(`http://localhost:${srv.address().port}/index.html`); await pg.waitForFunction(() => window.ready || window.err, null, { timeout: 240000 });
const out = []; const falhas = [];
for (const s of SPEC.shots) {
  const len = s.b - s.a; const frs = [0.2, 0.5, 0.8].map((q) => s.a + Math.round(len * q)); const res = [];
  for (const f of frs) {
    res.push(await pg.evaluate(async ([f, want]) => {
      const THREE = await import('./lib/three.module.js'); window.renderFrame(f);
      const cam = window.__cam, scene = window.__scene, pool = window.__propPool || {};
      const vis = (o) => { for (let p = o; p; p = p.parent) if (!p.visible) return false; return true; };
      const isCard = (o) => o.material && o.material.map && o.material.map.image && o.material.map.image.getContext && o.material.alphaTest > 0;   // personagem (carta pintada)
      const meshes = []; scene.traverse((o) => { if (o.isMesh && vis(o) && !o.userData.sky && !o.userData.ndSkip && (!(o.material && o.material.transparent) || isCard(o))) meshes.push(o); });
      const solido = (h) => { if (!isCard(h.object)) return true; if (!h.uv) return false; const im = h.object.material.map.image; const fl = h.object.material.map.flipY !== false; const px = im.getContext('2d').getImageData(Math.min(im.width - 1, Math.max(0, Math.floor(h.uv.x * im.width))), Math.min(im.height - 1, Math.max(0, Math.floor((fl ? 1 - h.uv.y : h.uv.y) * im.height))), 1, 1).data; return px[3] > 60; };   // carta so' tapa onde o boneco esta pintado
      const first = (hs) => hs.find(solido);
      const rc = new THREE.Raycaster(); const cp = cam.position.clone();
      const top = (o) => { let p = o; while (p.parent && p.parent !== scene && p.parent.parent && p.parent.parent !== scene) p = p.parent; return p; };
      const R = { f, objs: [], bloq: null, dentro: null };
      for (const a of want) {
        const objs = (pool[a] || []).filter(vis); let best = { a, inq: 0, vis: 0, area: 0 };
        for (const o of objs) {
          const pts = []; o.updateMatrixWorld(true); o.traverse((m) => { if (!m.isMesh) return; const ps = m.geometry.attributes.position; const st = Math.max(1, Math.floor(ps.count / 30)); for (let i = 0; i < ps.count; i += st) pts.push(new THREE.Vector3().fromBufferAttribute(ps, i).applyMatrix4(m.matrixWorld)); });
          let inq = 0, ok = 0, x0 = 1, x1 = -1, y0 = 1, y1 = -1;
          for (const p of pts) { const n = p.clone().project(cam); if (n.z > 1 || Math.abs(n.x) > 1 || Math.abs(n.y) > 1) continue; inq++; x0 = Math.min(x0, n.x); x1 = Math.max(x1, n.x); y0 = Math.min(y0, n.y); y1 = Math.max(y1, n.y);
            const d = p.clone().sub(cp); const dist = d.length(); rc.set(cp, d.normalize()); rc.far = dist + 0.05; const h = first(rc.intersectObjects(meshes, false));
            if (!h || h.distance >= dist - Math.max(0.15, dist * 0.04)) { ok++; continue; } let q = h.object; while (q && q !== o) q = q.parent; if (q === o) ok++; }
          const area = inq ? Math.max(0, x1 - x0) * Math.max(0, y1 - y0) / 4 : 0; const r = { a, inq: pts.length ? inq / pts.length : 0, vis: inq ? ok / inq : 0, area };
          if (r.vis * r.area > best.vis * best.area) best = r;
          const bb = new THREE.Box3().setFromObject(o); if (bb.containsPoint(cp) && bb.getSize(new THREE.Vector3()).length() > 4) R.dentro = a;
        }
        R.objs.push(best);
      }
      // tapando a camera: grade de raios; o mesmo objeto (que nao e' chao) cobrindo >= 35% do quadro a menos de 3,5 m da lente
      const cnt = new Map(); let tot = 0;
      for (let i = 0; i < 6; i++) for (let j = 0; j < 10; j++) { tot++; rc.setFromCamera(new THREE.Vector2(-0.9 + i * 0.36, -0.9 + j * 0.2), cam); rc.far = 3.5; const h = first(rc.intersectObjects(meshes, false)); if (!h || isCard(h.object)) continue;
        const nw = h.face ? h.face.normal.clone().transformDirection(h.object.matrixWorld) : null; if (nw && nw.y > 0.75) continue; const t = top(h.object); cnt.set(t, (cnt.get(t) || 0) + 1); }
      for (const [t, c] of cnt) if (c / tot >= 0.35) { let nm = ''; for (const k in pool) if (pool[k].includes(t)) nm = k; R.bloq = { obj: nm || t.name || t.type, frac: c / tot }; }
      return R;
    }, [f, need[s.id] || []]));
  }
  const rep = { id: s.id, quadros: res };
  for (const a of need[s.id] || []) { const ok = res.some((r) => r.objs.some((o) => o.a === a && o.vis >= 0.3 && o.area >= 0.004)); if (!ok) falhas.push(`${s.id}: objeto citado "${a}" nao aparece na tela (escondido, fora do quadro ou pequeno demais)`); }
  const bl = res.filter((r) => r.bloq); if (bl.length >= 2) falhas.push(`${s.id}: "${bl[0].bloq.obj}" tapando a camera (${Math.round(bl[0].bloq.frac * 100)}% do quadro, colado na lente)`);
  const dn = res.find((r) => r.dentro); if (dn) falhas.push(`${s.id}: camera DENTRO de "${dn.dentro}"`);
  out.push(rep);
}
await br.close(); srv.close();
fs.writeFileSync(`stories/${id}/visibilidade.json`, JSON.stringify({ id, falhas, tomadas: out }, null, 1));
if (falhas.length) { console.log('VISIBILIDADE: ' + falhas.length + ' FALHA(S)'); falhas.forEach((x) => console.log('FALHA ' + x)); process.exit(3); }
console.log('VISIBILIDADE OK: objetos citados aparecem, nada tapando a camera, camera fora dos objetos (' + out.length + ' tomadas)');
