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
const out = []; const falhas = []; const porCena = {}; const altCena = {}; const animCena = {};
const ANIM_RX = /\b(cavalos?|urso|ursos|porcos?|galinhas?|emus?|gansos?|vacas?|bois?|cachorros?|caes|gatos?|ovelhas?|cabras?|bodes?|burros?|jumentos?|veados?|cervos?|raposas?|lobos?|coelhos?|leao|leoes|elefantes?|patos?|galos?|gaivotas?)\b/;
for (const s of SPEC.shots) {
  const len = s.b - s.a; const frs = [0.2, 0.5, 0.8].map((q) => s.a + Math.round(len * q)); const res = [];
  for (const f of frs) {
    res.push(await pg.evaluate(async ([f, want, nWho]) => {
      const THREE = await import('./lib/three.module.js'); window.renderFrame(f);
      const cam = window.__cam, scene = window.__scene, pool = window.__propPool || {};
      const vis = (o) => { for (let p = o; p; p = p.parent) if (!p.visible) return false; return true; };
      const isCard = (o) => o.material && o.material.map && o.material.map.image && o.material.map.image.getContext && o.material.alphaTest > 0;   // personagem (carta pintada)
      const meshes = []; scene.traverse((o) => { if (o.isMesh && vis(o) && !o.userData.sky && !o.userData.ndSkip && (!(o.material && o.material.transparent) || isCard(o))) meshes.push(o); });
      const solido = (h) => { if (!isCard(h.object)) return true; if (!h.uv) return false; const im = h.object.material.map.image; const fl = h.object.material.map.flipY !== false; const px = im.getContext('2d').getImageData(Math.min(im.width - 1, Math.max(0, Math.floor(h.uv.x * im.width))), Math.min(im.height - 1, Math.max(0, Math.floor((fl ? 1 - h.uv.y : h.uv.y) * im.height))), 1, 1).data; return px[3] > 60; };   // carta so' tapa onde o boneco esta pintado
      const chao = (h) => { if (isCard(h.object) || !h.face) return false; const nw = h.face.normal.clone().transformDirection(h.object.matrixWorld); return nw.y > 0.75; };   // chao/agua/convés: a parte do objeto abaixo dele (casco submerso) nao conta como escondida
      const hitAll = (rc_) => { const out = []; for (const m of meshes) { try { rc_.intersectObject(m, false, out); } catch (e) {} } return out.sort((a, b) => a.distance - b.distance); };   // objeto com geometria estranha nao derruba a checagem
      const first = (hs) => hs.find((h) => solido(h) && !chao(h));
      const rc = new THREE.Raycaster(); const cp = cam.position.clone();
      const top = (o) => { let p = o; while (p.parent && p.parent !== scene && p.parent.parent && p.parent.parent !== scene) p = p.parent; return p; };
      const R = { f, objs: [], bloq: null, dentro: null };
      for (const a of want) {
        const objs = (pool[a] || []).filter(vis); let best = { a, inq: 0, vis: 0, area: 0, cx: 9 };
        for (const o of objs) {
          const pts = []; o.updateMatrixWorld(true); o.traverse((m) => { if (!m.isMesh) return; const ps = m.geometry.attributes.position; const st = Math.max(1, Math.floor(ps.count / 30)); for (let i = 0; i < ps.count; i += st) pts.push(new THREE.Vector3().fromBufferAttribute(ps, i).applyMatrix4(m.matrixWorld)); });
          let inq = 0, ok = 0, x0 = 1, x1 = -1, y0 = 1, y1 = -1;
          for (const p of pts) { const n = p.clone().project(cam); if (n.z > 1 || Math.abs(n.x) > 1 || Math.abs(n.y) > 1) continue; inq++; x0 = Math.min(x0, n.x); x1 = Math.max(x1, n.x); y0 = Math.min(y0, n.y); y1 = Math.max(y1, n.y);
            const d = p.clone().sub(cp); const dist = d.length(); rc.set(cp, d.normalize()); rc.far = dist + 0.05; const h = first(hitAll(rc));
            if (!h || h.distance >= dist - Math.max(0.15, dist * 0.04)) { ok++; continue; } let q = h.object; while (q && q !== o) q = q.parent; if (q === o) ok++; }
          const area = inq ? Math.max(0, x1 - x0) * Math.max(0, y1 - y0) / 4 : 0; const r = { a, inq: pts.length ? inq / pts.length : 0, vis: inq ? ok / inq : 0, area, cx: inq ? (x0 + x1) / 2 : 9, alt: inq ? (Math.min(y1, 1) - Math.max(y0, -1)) / 2 : 0 };
          if (r.vis * r.area > best.vis * best.area) best = r;
          best.altmax = Math.max(best.altmax || 0, r.alt || 0);
          const bb = new THREE.Box3().setFromObject(o); if (bb.containsPoint(cp) && bb.getSize(new THREE.Vector3()).length() > 4) R.dentro = a;
        }
        R.objs.push(best);
      }
      // tapando a camera: grade de raios; o mesmo objeto (que nao e' chao) cobrindo >= 35% do quadro a menos de 3,5 m da lente
      const cnt = new Map(); let tot = 0;
      for (let i = 0; i < 6; i++) for (let j = 0; j < 10; j++) { tot++; rc.setFromCamera(new THREE.Vector2(-0.9 + i * 0.36, -0.9 + j * 0.2), cam); rc.far = 3.5; const h = first(hitAll(rc)); if (!h || isCard(h.object)) continue;
        const nw = h.face ? h.face.normal.clone().transformDirection(h.object.matrixWorld) : null; if (nw && nw.y > 0.75) continue; const t = top(h.object); cnt.set(t, (cnt.get(t) || 0) + 1); }
      // PAREDE: um mesmo objeto (navio, predio) cobrindo 60%+ do quadro a qualquer distancia = a camera so' ve um casco/parede
      const cnt2 = new Map(); let tot2 = 0;
      for (let i = 0; i < 6; i++) for (let j = 0; j < 10; j++) { tot2++; rc.setFromCamera(new THREE.Vector2(-0.9 + i * 0.36, -0.9 + j * 0.2), cam); rc.far = 400; const h = first(hitAll(rc)); if (!h || isCard(h.object)) continue; const nw = h.face ? h.face.normal.clone().transformDirection(h.object.matrixWorld) : null; if (nw && nw.y > 0.75) continue; const t = top(h.object); let nm = ''; for (const k in pool) if (pool[k].includes(t)) nm = k; if (nm) cnt2.set(nm, (cnt2.get(nm) || 0) + 1); }
      for (const [nm, c] of cnt2) if (c / tot2 >= 0.6 && !/^kit\/(room|porch|hospital|prison|rg_|marco_)/.test(nm) && (!/^buildings\//.test(nm) || want.includes(nm))) R.parede = { obj: nm, frac: c / tot2 };
      for (const [t, c] of cnt) if (c / tot >= 0.35) { let nm = ''; for (const k in pool) if (pool[k].includes(t)) nm = k; R.bloq = { obj: nm || t.name || t.type, frac: c / tot }; }
      // personagem cortado: carta de boneco grande (mais de 45% da altura da tela) atravessando a borda do quadro
      // personagem cortado: so' os PERSONAGENS DA CENA ("who"), nao figurante de multidao passando pela borda (24/11: Banquinho/Melancia/Post-it travavam por figurante)
      R.cortado = 0; { const I = window.inspectFrame(f); for (const a of (I.actors || [])) { if (a.i >= nWho || a.behind || !a.box) continue; const [x0, y0, x1, y1] = a.box; const alt = Math.min(y1, 1) - Math.max(y0, 0); const fr_ = (Math.min(x1, 1) - Math.max(x0, 0)) / Math.max(1e-6, x1 - x0); if (alt > 0.45 && fr_ < 0.65 && x1 > 0 && x0 < 1) R.cortado++; } window.INSPECT = false; }
      return R;
    }, [f, need[s.id] || [], ((B.beats || [])[+String(s.id).replace(/^b(\d+).*/, '$1')] || {}).who ? ((B.beats || [])[+String(s.id).replace(/^b(\d+).*/, '$1')].who.length) : 0]));
  }
  // ANIMAL CITADO (gansos, cavalos...): tem que aparecer GRANDE o bastante para se ler (>= 10% da altura da tela) em TODO take da cena
  { const k = +String(s.id).replace(/^b(\d+).*/, '$1'); const bt = (B.beats || [])[k] || {};
    const nrm = (x) => String(x || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    if ((bt.animals || []).length && ANIM_RX.test(nrm(bt.say))) { const bk = 'b' + k;
      const tk = []; for (const f of frs) { const h = await pg.evaluate(async ([f, nm3]) => { const THREE_ = await import('./lib/three.module.js'); const r = window.inspectFrame(f); let m = 0; for (const a of r.actors || []) if (a.animal3d || /^(bird|pig|cow|dog|cat|sheep|goat|donkey|deer|fox|wolf|rabbit|lion|elephant|duck|goose|rooster|gull)$/.test(String(a.id))) if (!a.behind && a.visible > 0.5) m = Math.max(m, a.heightFrac || 0);
          const cam = window.__cam, pool = window.__propPool || {};
          for (const nm of nm3) for (const o of (pool[nm] || [])) { let v = true; for (let p = o; p; p = p.parent) if (!p.visible) v = false; if (!v || !THREE_) continue; const bb = new THREE_.Box3().setFromObject(o); if (bb.isEmpty()) continue; let y0 = 9, y1 = -9, zz = false; for (const x of [bb.min.x, bb.max.x]) for (const y of [bb.min.y, bb.max.y]) for (const z of [bb.min.z, bb.max.z]) { const n = new THREE_.Vector3(x, y, z).project(cam); if (n.z > 1) zz = true; y0 = Math.min(y0, n.y); y1 = Math.max(y1, n.y); } if (!zz) m = Math.max(m, (Math.min(y1, 1) - Math.max(y0, -1)) / 2); }
          return m; }, [f, ['chicken', 'emu', 'horse', 'horse_sela', 'bear', 'dog', 'cat', 'cow', 'deer', 'donkey', 'elephant', 'fox', 'goat', 'lion', 'rabbit', 'sheep', 'wolf']]);
        tk.push(h); } (animCena[bk] = animCena[bk] || []).push(tk); } }
  const rep = { id: s.id, quadros: res };
  for (const a of need[s.id] || []) { const okT = (r) => r.objs.some((o) => o.a === a && o.vis >= 0.5 && (a !== String(B.heroi || '') || Math.abs(o.cx ?? 0) < 0.55) && o.area >= (/navio|ship|boat|submarino|aviao|airplane|tanque|tank|casa|house|predio|building|castelo|igreja|torre|ponte|trem|locomotiva|onibus|caminhao|truck|balloon|balao|foguete|rocket|roadster|carro|car_/i.test(a) ? 0.05 : 0.004)); const bk = String(s.id).replace(/^(b\d+).*/, '$1'); (porCena[bk + '|' + a] = porCena[bk + '|' + a] || []).push(res.filter(okT).length >= 1); (altCena[bk + '|' + a] = altCena[bk + '|' + a] || []).push(Math.max(0, ...res.map((r) => Math.max(0, ...r.objs.filter((o) => o.a === a).map((o) => o.alt || 0))))); continue;   /* 1 dos 3 quadros basta: o mapa do pais cobre a tela por 1-2 s */ const big = /navio|ship|boat|submarino|aviao|airplane|tanque|tank|casa|house|predio|building|castelo|igreja|torre|ponte|trem|locomotiva|onibus|caminhao|truck|balloon|balao|foguete|rocket|roadster|carro|car_/i.test(a); const ok = res.filter((r) => r.objs.some((o) => o.a === a && o.vis >= 0.5 && o.area >= (big ? 0.05 : 0.004))).length >= 2; if (!ok) falhas.push(`${s.id}: objeto citado "${a}" nao aparece na tela (escondido, fora do quadro ou pequeno demais)`); }
  const bl = res.filter((r) => r.bloq); if (bl.length >= 2) falhas.push(`${s.id}: "${bl[0].bloq.obj}" tapando a camera (${Math.round(bl[0].bloq.frac * 100)}% do quadro, colado na lente)`);
  if (!/_d$|_v$/.test(s.id) && res.filter((r) => r.cortado).length >= 2) falhas.push(`${s.id}: personagem CORTADO na borda do quadro (boneco grande saindo da tela)`);
  const pw = res.filter((r) => r.parede); if (pw.length >= 2) falhas.push(`${s.id}: "${pw[0].parede.obj}" cobrindo a tela (${Math.round(pw[0].parede.frac * 100)}% do quadro: so' se ve uma parede/casco)`);
  const dn = res.find((r) => r.dentro); if (dn) falhas.push(`${s.id}: camera DENTRO de "${dn.dentro}"`);
  out.push(rep);
}
for (const [k, v] of Object.entries(porCena)) if (!v.some(Boolean)) { const [bk, a] = k.split('|'); falhas.push(`${bk}: objeto citado "${a}" nao aparece na tela (escondido, fora do quadro ou pequeno demais)`); }
for (const [bk, tks] of Object.entries(animCena)) { const ruim = tks.findIndex((v) => v.filter((h) => h >= 0.10).length < 2); if (ruim >= 0) falhas.push(`${bk}: animal citado aparece pequeno demais no take ${ruim + 1} (${Math.round(Math.max(...tks[ruim]) * 100)}% da altura da tela; precisa de 10%+ em todo take): camera mais perto ou animal maior`); }
// OLHOS x FICHA DE CENA: o objeto apareceu do tamanho que a folha 2 planejou? (menos da metade do planejado = falha)
for (const [k_, v] of Object.entries(altCena)) { const [bk, a] = k_.split('|'); const bt = (B.beats || [])[+bk.slice(1)]; const q = bt && bt.quadro && (bt.quadro.objetos || []).find((o) => o.objeto === a); const pl = q ? parseInt(q.tela) / 100 : 0;
  if (pl > 0 && Math.max(...v) < pl * 0.5) falhas.push(`${bk}: objeto "${a}" saiu com ${Math.round(Math.max(...v) * 100)}% da altura da tela, a ficha de cena planejou ${Math.round(pl * 100)}%`); }
await br.close(); srv.close();
fs.writeFileSync(`stories/${id}/visibilidade.json`, JSON.stringify({ id, falhas, tomadas: out }, null, 1));
if (falhas.length) { console.log('VISIBILIDADE: ' + falhas.length + ' FALHA(S)'); falhas.forEach((x) => console.log('FALHA ' + x)); process.exit(3); }
console.log('VISIBILIDADE OK: objetos citados aparecem, nada tapando a camera, camera fora dos objetos (' + out.length + ' tomadas)');
