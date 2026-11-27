// Formato "countryballs no mapa 3D": mapa-mundi com paises nomeados (kit/mapa_mundi.glb), bolas 2D (sprites desenhados em canvas), camera dirigida por keyframes, paises repintados por evento.
// Uso: index.html#<spec> carrega <spec>.json. renderFrame(f) e getFrameDataURL() como o motor principal; texto/legenda em DOM (screenshot).
import * as THREE from '../lib/three.module.js';
import { GLTFLoader } from '../lib/GLTFLoader.js';
const FPS = 30, W = 1080, H = 1920, K = Math.cos(50 * Math.PI / 180);   // K = achatamento de longitude (Europa nao fica esticada)
const spec = await (await fetch(location.hash.slice(1) + '.json')).json();
const norm = s => s.toLowerCase().replace(/[^a-z0-9]/g, '');
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('c'), antialias: true, preserveDrawingBuffer: true });
renderer.setSize(W, H, false); renderer.setPixelRatio(1);
const scene = new THREE.Scene(); scene.background = new THREE.Color(spec.sea || '#dff0ff');
const cam = new THREE.PerspectiveCamera(38, W / H, 1, 600);
scene.add(new THREE.HemisphereLight(0xffffff, 0x8899bb, 1.35)); const sun = new THREE.DirectionalLight(0xffffff, 1.1); sun.position.set(-30, 80, 40); scene.add(sun);
// ---------- mapa ----------
const gl = await new GLTFLoader().loadAsync('../assets/library/kit/mapa_mundi.glb');
const mapRoot = new THREE.Group(); mapRoot.scale.set(K, 1, 1); mapRoot.add(gl.scene); scene.add(mapRoot);
const C = {};   // pais -> {mesh, base, cur}
const LAND = new THREE.Color(spec.land || '#c9ced6');
gl.scene.traverse(o => {
  if (!o.isMesh) return;
  if (o.name.toLowerCase().startsWith('oceano')) { o.material = new THREE.MeshBasicMaterial({ color: new THREE.Color(spec.sea || '#dff0ff') }); o.visible = false; return; }
  o.material = new THREE.MeshStandardMaterial({ color: LAND.clone(), roughness: .6, metalness: 0 }); C[norm(o.name)] = { mesh: o, y0: o.position.y };
});
// pinta o mapa por eventos: lista ordenada; a cor vigente de cada pais e' a do ultimo evento (com transicao 0,45 s e "pulo" do azulejo)
const ev = [...(spec.colors || [])].sort((a, b) => a.t - b.t);
const colorAt = (name, t) => {
  let prev = LAND.clone(), cur = LAND.clone(), te = -99;
  for (const e of ev) { if (e.t > t) break; if (e.c.some(x => norm(x) === name) || (e.all && !(e.except || []).some(x => norm(x) === name))) { prev = cur; cur = new THREE.Color(e.col); te = e.t; } }
  return { col: prev.clone().lerp(cur, Math.min(1, Math.max(0, (t - te) / .45))), age: t - te };
};
// ---------- bolas ----------
const FLAGS = {
  DE: c => { stripes(c, ['#111', '#dd0000', '#ffce00'], 1); }, FR: c => { stripes(c, ['#0055a4', '#fff', '#ef4135'], 0); }, RU: c => { stripes(c, ['#fff', '#0039a6', '#d52b1e'], 1); },
  AT: c => { stripes(c, ['#ed2939', '#fff', '#ed2939'], 1); }, HU: c => { stripes(c, ['#ce2939', '#fff', '#477050'], 1); }, SR: c => { stripes(c, ['#c6363c', '#0c4076', '#fff'], 1); }, BE: c => { stripes(c, ['#111', '#fae042', '#ed2939'], 0); },
  IT: c => { stripes(c, ['#009246', '#fff', '#ce2b37'], 0); }, TR: c => { c.fillStyle = '#e30a17'; c.fillRect(0, 0, 256, 256); c.fillStyle = '#fff'; c.beginPath(); c.arc(110, 128, 52, 0, 7); c.fill(); c.fillStyle = '#e30a17'; c.beginPath(); c.arc(126, 128, 42, 0, 7); c.fill(); star(c, 165, 128, 26, '#fff'); },
  UK: c => { c.fillStyle = '#012169'; c.fillRect(0, 0, 256, 256); c.strokeStyle = '#fff'; c.lineWidth = 44; line(c, 0, 0, 256, 256); line(c, 256, 0, 0, 256); c.strokeStyle = '#c8102e'; c.lineWidth = 16; line(c, 0, 0, 256, 256); line(c, 256, 0, 0, 256); c.strokeStyle = '#fff'; c.lineWidth = 70; line(c, 128, 0, 128, 256); line(c, 0, 128, 256, 128); c.strokeStyle = '#c8102e'; c.lineWidth = 40; line(c, 128, 0, 128, 256); line(c, 0, 128, 256, 128); },
  US: c => { for (let i = 0; i < 13; i++) { c.fillStyle = i % 2 ? '#fff' : '#b22234'; c.fillRect(0, i * 256 / 13, 256, 256 / 13 + 1); } c.fillStyle = '#3c3b6e'; c.fillRect(0, 0, 120, 138); c.fillStyle = '#fff'; for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { c.beginPath(); c.arc(18 + j * 28, 20 + i * 30, 5, 0, 7); c.fill(); } },
  JP: c => { c.fillStyle = '#fff'; c.fillRect(0, 0, 256, 256); c.fillStyle = '#bc002d'; c.beginPath(); c.arc(128, 128, 62, 0, 7); c.fill(); },
  BG: c => { stripes(c, ['#fff', '#00966e', '#d62612'], 1); }, RO: c => { stripes(c, ['#002b7f', '#fcd116', '#ce1126'], 0); }, GR: c => { stripes(c, ['#0d5eaf', '#fff', '#0d5eaf', '#fff', '#0d5eaf', '#fff', '#0d5eaf', '#fff', '#0d5eaf'], 1); },
  SU: c => { c.fillStyle = '#cc0000'; c.fillRect(0, 0, 256, 256); star(c, 128, 128, 56, '#ffd700'); }, PL: c => { stripes(c, ['#fff', '#dc143c'], 1); }, CA: c => { c.fillStyle = '#fff'; c.fillRect(0, 0, 256, 256); c.fillStyle = '#d80621'; c.fillRect(0, 0, 64, 256); c.fillRect(192, 0, 64, 256); star(c, 128, 128, 48, '#d80621'); },
};
function stripes(c, cols, h) { const n = cols.length; cols.forEach((k, i) => { c.fillStyle = k; if (h) c.fillRect(0, i * 256 / n, 256, 256 / n + 1); else c.fillRect(i * 256 / n, 0, 256 / n + 1, 256); }); }
function line(c, a, b, d, e) { c.beginPath(); c.moveTo(a, b); c.lineTo(d, e); c.stroke(); }
function star(c, x, y, r, col) { c.fillStyle = col; c.beginPath(); for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, rr = i % 2 ? r * .42 : r; c.lineTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr); } c.closePath(); c.fill(); }
const ACC = {   // acessorios desenhados sobre a bola (coordenadas do canvas 256x256, bola = circulo r=100 em 128,138)
  pickel: c => { c.fillStyle = '#3a3a3a'; c.beginPath(); c.ellipse(128, 52, 70, 34, 0, Math.PI, 0); c.fill(); c.fillStyle = '#c9a227'; c.fillRect(60, 48, 136, 12); c.fillStyle = '#c9a227'; c.beginPath(); c.moveTo(121, 22); c.lineTo(128, -6); c.lineTo(135, 22); c.fill(); },
  tophat: c => { c.fillStyle = '#151515'; c.fillRect(82, -4, 92, 58); c.fillRect(58, 48, 140, 14); c.fillStyle = '#b00'; c.fillRect(82, 36, 92, 10); },
  brodie: c => { c.fillStyle = '#6b7a4b'; c.beginPath(); c.ellipse(128, 56, 84, 40, 0, Math.PI, 0); c.fill(); c.fillRect(44, 54, 168, 9); },
  beret: c => { c.fillStyle = '#111d4a'; c.beginPath(); c.ellipse(120, 44, 80, 30, -.12, 0, 7); c.fill(); c.fillRect(116, 6, 8, 12); },
  kepi: c => { c.fillStyle = '#1b3a8a'; c.fillRect(66, 22, 124, 34); c.fillStyle = '#e03'; c.fillRect(66, 22, 124, 8); c.fillStyle = '#111'; c.beginPath(); c.ellipse(128, 58, 82, 11, 0, 0, 7); c.fill(); },
  ushanka: c => { c.fillStyle = '#6b6b6b'; c.beginPath(); c.ellipse(128, 44, 86, 40, 0, Math.PI, 0); c.fill(); c.fillRect(42, 40, 172, 22); c.fillStyle = '#cc0000'; star(c, 128, 40, 14, '#cc0000'); },
  shades: c => { c.fillStyle = '#000'; c.fillRect(54, 112, 66, 30); c.fillRect(136, 112, 66, 30); c.fillRect(118, 118, 20, 8); },
  fez: c => { c.fillStyle = '#c0182f'; c.beginPath(); c.moveTo(78, 56); c.lineTo(94, 0); c.lineTo(162, 0); c.lineTo(178, 56); c.fill(); c.fillStyle = '#111'; c.fillRect(150, 0, 5, 40); },
  crown: c => { c.fillStyle = '#ffd23f'; c.beginPath(); c.moveTo(70, 56); c.lineTo(70, 14); c.lineTo(98, 34); c.lineTo(128, 6); c.lineTo(158, 34); c.lineTo(186, 14); c.lineTo(186, 56); c.closePath(); c.fill(); c.strokeStyle = '#111'; c.lineWidth = 6; c.stroke(); },
  helmetus: c => { c.fillStyle = '#7a8450'; c.beginPath(); c.ellipse(128, 54, 80, 36, 0, Math.PI, 0); c.fill(); c.fillRect(48, 52, 160, 9); },
  stache: c => { c.fillStyle = '#222'; c.beginPath(); c.ellipse(100, 164, 30, 10, .2, 0, 7); c.ellipse(156, 164, 30, 10, -.2, 0, 7); c.fill(); },
};
function drawBall(cv, b, st) {   // st: {e: expressao, blink, t}
  const c = cv.getContext('2d'); c.clearRect(0, 0, 256, 256); const cx = 128, cy = 138, R = 100;
  c.save(); c.beginPath(); c.arc(cx, cy, R, 0, 7); c.clip(); (FLAGS[b.flag] || FLAGS.UK)(c); c.restore();
  const g = c.createRadialGradient(cx - 34, cy - 40, 8, cx, cy, R); g.addColorStop(0, 'rgba(255,255,255,.30)'); g.addColorStop(.6, 'rgba(255,255,255,0)'); g.addColorStop(1, 'rgba(0,0,40,.28)'); c.fillStyle = g; c.beginPath(); c.arc(cx, cy, R, 0, 7); c.fill();
  c.lineWidth = 9; c.strokeStyle = '#111'; c.beginPath(); c.arc(cx, cy, R, 0, 7); c.stroke();
  const e = st.e || 'idle', eye = (x, y, w, h, px, py) => { c.fillStyle = '#fff'; c.strokeStyle = '#111'; c.lineWidth = 6; c.beginPath(); c.ellipse(x, y, w, h, 0, 0, 7); c.fill(); c.stroke(); c.fillStyle = '#111'; c.beginPath(); c.arc(x + px, y + py, Math.max(5, w * .32), 0, 7); c.fill(); };
  const ex = [100, 156], ey = 128, bl = st.blink ? .12 : 1;
  const look = st.look || [0, 0];
  if (e === 'happy') { c.strokeStyle = '#111'; c.lineWidth = 9; c.lineCap = 'round'; for (const x of ex) { c.beginPath(); c.arc(x, ey + 6, 18, Math.PI * 1.1, Math.PI * 1.9); c.stroke(); } c.fillStyle = '#7a0a0a'; c.beginPath(); c.arc(128, 168, 22, 0, Math.PI); c.fill(); c.stroke(); }
  else if (e === 'cry') { for (const x of ex) eye(x, ey, 19, 22 * bl, 0, 7); c.fillStyle = '#39a7ff'; for (const x of [88, 168]) { c.beginPath(); c.ellipse(x, 170, 7, 20, 0, 0, 7); c.fill(); } c.strokeStyle = '#111'; c.lineWidth = 7; c.beginPath(); c.arc(128, 186, 20, Math.PI * 1.15, Math.PI * 1.85); c.stroke(); }
  else if (e === 'scared') { for (const x of ex) eye(x, ey, 25, 30 * bl, 0, 0); c.fillStyle = '#7a0a0a'; c.strokeStyle = '#111'; c.lineWidth = 6; c.beginPath(); c.ellipse(128, 176, 14, 22, 0, 0, 7); c.fill(); c.stroke(); c.fillStyle = '#39a7ff'; c.beginPath(); c.ellipse(204, 98, 9, 15, .3, 0, 7); c.fill(); }
  else if (e === 'shout') { for (const x of ex) eye(x, ey, 20, 22 * bl, look[0] * 6, look[1] * 6); c.strokeStyle = '#111'; c.lineWidth = 11; c.lineCap = 'round'; line(c, 74, 96, 116, 112); line(c, 182, 96, 140, 112); c.fillStyle = '#7a0a0a'; c.beginPath(); c.ellipse(128, 176, 34, 26, 0, 0, 7); c.fill(); c.lineWidth = 6; c.stroke(); }
  else if (e === 'angry') { for (const x of ex) eye(x, ey + 4, 19, 17 * bl, look[0] * 6 + (x < 128 ? 4 : -4), 2); c.strokeStyle = '#111'; c.lineWidth = 11; c.lineCap = 'round'; line(c, 74, 98, 120, 116); line(c, 182, 98, 136, 116); c.beginPath(); c.arc(128, 188, 24, Math.PI * 1.15, Math.PI * 1.85); c.stroke(); }
  else if (e === 'smug') { for (const x of ex) { eye(x, ey, 19, 20 * bl, look[0] * 6 + 5, 3); c.fillStyle = 'rgba(0,0,0,.0)'; } c.fillStyle = (b.skin || '#00000000'); c.strokeStyle = '#111'; c.lineWidth = 9; line(c, 78, ey - 10, 122, ey - 10); line(c, 134, ey - 10, 178, ey - 10); c.beginPath(); c.arc(140, 172, 22, .1, Math.PI * .85); c.stroke(); }
  else { for (const x of ex) eye(x, ey, 19, 22 * bl, look[0] * 7, look[1] * 7); }
  if (b.acc) b.acc.split('+').forEach(k => ACC[k] && ACC[k](c));
}
const balls = {}, ballList = spec.balls || [];
const mkCanvas = () => { const cv = document.createElement('canvas'); cv.width = cv.height = 256; return cv; };
for (const b of ballList) {
  const cv = mkCanvas(), tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false }));
  const sh = new THREE.Mesh(new THREE.CircleGeometry(.5, 24), new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: .28, depthWrite: false })); sh.rotation.x = -Math.PI / 2;
  m.renderOrder = 10; scene.add(m); scene.add(sh); balls[b.id] = { b, cv, tex, m, sh, key: '', pos: [0, 0] };
}
const ease = x => x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2, clamp = (x, a, b) => Math.max(a, Math.min(b, x));
function track(arr, t, keys) {   // interpolacao por keyframes (arr ordenado por t) nos campos keys
  if (!arr || !arr.length) return null; if (t <= arr[0].t) return arr[0]; const l = arr[arr.length - 1]; if (t >= l.t) return l;
  let i = 0; while (arr[i + 1].t < t) i++; const a = arr[i], b = arr[i + 1], k = ease((t - a.t) / (b.t - a.t)); const o = {};
  for (const f of keys) o[f] = a[f] + (b[f] - a[f]) * k; return o;
}
const tween = (v, t, lonlat) => lonlat;
function ballPos(bl, t) {   // trajetoria: pontos [{t,lon,lat}] com interpolacao suave; pulinhos enquanto anda
  const p = track(bl.b.path, t, ['lon', 'lat']) || { lon: bl.b.lon, lat: bl.b.lat }; return p;
}
// ---------- efeitos ----------
const fxMeshes = [];
const fxTex = (draw) => { const cv = mkCanvas(), c = cv.getContext('2d'); draw(c); const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t; };
const TEX = {
  boom: fxTex(c => { const g = c.createRadialGradient(128, 128, 5, 128, 128, 124); g.addColorStop(0, '#fff'); g.addColorStop(.25, '#ffe14a'); g.addColorStop(.55, '#ff6a00'); g.addColorStop(1, 'rgba(255,0,0,0)'); c.fillStyle = g; c.beginPath(); for (let i = 0; i < 24; i++) { const a = i * Math.PI / 12, r = i % 2 ? 70 : 124; c.lineTo(128 + Math.cos(a) * r, 128 + Math.sin(a) * r); } c.closePath(); c.fill(); c.lineWidth = 7; c.strokeStyle = '#2b0a00'; c.stroke(); }),
  puff: fxTex(c => { c.fillStyle = '#fff'; for (const [x, y, r] of [[90, 140, 54], [150, 130, 62], [120, 96, 56], [170, 170, 44], [80, 176, 40]]) { c.beginPath(); c.arc(x, y, r, 0, 7); c.fill(); } }),
  dot: fxTex(c => { const g = c.createRadialGradient(128, 128, 0, 128, 128, 110); g.addColorStop(0, '#fff'); g.addColorStop(.35, '#fff6a0'); g.addColorStop(1, 'rgba(255,200,0,0)'); c.fillStyle = g; c.beginPath(); c.arc(128, 128, 120, 0, 7); c.fill(); }),
  skull: fxTex(c => { c.font = '200px serif'; c.textAlign = 'center'; c.fillText('💀', 128, 190); }),
  star: fxTex(c => { star(c, 128, 128, 120, '#ffd23f'); c.lineWidth = 8; c.strokeStyle = '#2b0a00'; c.stroke(); }),
};
const linkMat = c => new THREE.MeshBasicMaterial({ color: c, transparent: true, depthWrite: false });
function bpos(id, t) { const bl = balls[id]; const p = ballPos(bl, t); return new THREE.Vector3(p.lon * K, 0, -p.lat); }
let shakeAmp = 0;
// ---------- quadro ----------
const texts = [...(spec.texts || [])], textEls = texts.map(x => { const d = document.createElement('div'); d.className = 'tx ' + x.style; d.textContent = x.text; if (x.top) d.style.top = x.top + 'px'; if (x.color) d.style.color = x.color; if (x.size) d.style.fontSize = x.size + 'px'; document.getElementById('wrap').appendChild(d); return d; });
const fl = document.getElementById('fl');
window.renderFrame = f => {
  const t = f / FPS;
  // camera
  const k = track(spec.cam, t, ['lon', 'lat', 'h', 'tilt', 'roll']); let sx = 0, sz = 0;
  for (const s of spec.shake || []) if (t >= s.t && t < s.t + s.d) { const a = (s.a || 1.2) * (1 - (t - s.t) / s.d); sx += Math.sin(t * 90) * a; sz += Math.cos(t * 77) * a; }
  const cx = k.lon * K + sx * .4, cz = -k.lat + sz * .4; cam.position.set(cx, k.h, cz + k.h * Math.tan(k.tilt)); cam.up.set(0, 0, -1); cam.lookAt(cx, 0, cz); cam.rotateZ(k.roll || 0); cam.updateMatrixWorld();
  // paises
  for (const n in C) { const o = C[n], s = colorAt(n, t); o.mesh.material.color.copy(s.col); const pop = s.age >= 0 && s.age < .5 ? Math.sin(s.age / .5 * Math.PI) * 1.6 : 0; o.mesh.position.y = o.y0 + pop; }
  // bolas
  for (const id in balls) {
    const bl = balls[id], b = bl.b; const vis = t >= (b.in ?? 0) && t < (b.out ?? 1e9); bl.m.visible = bl.sh.visible = vis; if (!vis) continue;
    const p = ballPos(bl, t); const moving = b.path && b.path.some((q, i) => i && t > b.path[i - 1].t && t < q.t && (q.lon !== b.path[i - 1].lon || q.lat !== b.path[i - 1].lat));
    let e = 'idle', look = null; for (const x of b.faces || []) if (x.t <= t) { e = x.e; look = x.look || null; }
    const blink = (Math.floor(t * 10 + b.lon) % 31) === 0; const key = e + blink + (look ? look.join() : ''); if (key !== bl.key) { drawBall(bl.cv, b, { e, blink, look }); bl.tex.needsUpdate = true; bl.key = key; }
    const sz = (b.size || 6) * Math.min(1, (t - (b.in ?? 0)) / .25 + .0001), a = t - (b.in ?? 0), pin = a < .35 ? 1 + Math.sin(a / .35 * Math.PI) * .3 : 1;
    const hop = moving ? Math.abs(Math.sin(t * 11 + b.lon)) * sz * .22 : Math.sin(t * 4 + b.lon * 3) * sz * .04, sq = moving ? 1 + Math.cos(t * 11) * .06 : 1;
    let ox = 0, oz = 0, big = 1; for (const x of b.pulse || []) if (t >= x.t && t < x.t + .5) { big = 1 + Math.sin((t - x.t) / .5 * Math.PI) * (x.a || .35); ox += Math.sin(t * 70) * .3; }
    if (b.fall && t >= b.fall) { const q = clamp((t - b.fall) / .6, 0, 1); bl.m.rotation.z = q * 1.5; bl.m.material.opacity = 1 - clamp((t - b.fall - 1) / .8, 0, 1); } else { bl.m.rotation.z = 0; bl.m.material.opacity = 1; }
    bl.m.position.set(p.lon * K + ox, sz * .55 + 1.2 + hop, -p.lat + oz); bl.m.scale.set(sz * pin * big * (1 / sq), sz * pin * big * sq, 1);
    bl.m.quaternion.copy(cam.quaternion); if (b.fall && t >= b.fall) bl.m.rotateZ((t - b.fall > 0 ? Math.min(1.5, (t - b.fall) * 2.5) : 0));
    bl.sh.position.set(p.lon * K, .3, -p.lat); bl.sh.scale.set(sz * .75, sz * .3, 1); bl.sh.material.opacity = bl.m.material.opacity * .28;
  }
  // efeitos
  for (const m of fxMeshes) { scene.remove(m); m.geometry.dispose(); m.material.dispose(); } fxMeshes.length = 0;
  const add = (m) => { scene.add(m); fxMeshes.push(m); return m; };
  for (const x of spec.fx || []) {
    const a = t - x.t, d = x.d ?? .6; if (a < 0 || a > d) continue; const q = a / d;
    if (x.k === 'boom' || x.k === 'puff' || x.k === 'skull' || x.k === 'star') {
      const m = add(new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: TEX[x.k], transparent: true, depthWrite: false, opacity: x.k === 'boom' ? 1 - q * q : 1 - q, color: x.col ? new THREE.Color(x.col) : 0xffffff })));
      const s = (x.s || 7) * (x.k === 'puff' ? .6 + q : x.k === 'skull' ? 1 : .35 + Math.sin(Math.min(1, q * 1.4) * Math.PI / 2) * .9); m.scale.set(s, s, 1); m.position.set(x.lon * K, 4 + (x.k === 'skull' ? q * 4 : 0), -x.lat); m.quaternion.copy(cam.quaternion); m.renderOrder = 20;
    } else if (x.k === 'shot') {   // projetil de A para B (A/B = id de bola ou lon/lat)
      const A = x.a in balls ? bpos(x.a, t) : new THREE.Vector3(x.alon * K, 0, -x.alat), B = x.b in balls ? bpos(x.b, t) : new THREE.Vector3(x.blon * K, 0, -x.blat); const p = A.clone().lerp(B, clamp(q * 1.15, 0, 1)); p.y = 4.5;
      const m = add(new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: TEX.dot, transparent: true, depthWrite: false }))); m.scale.set(2.2, 2.2, 1); m.position.copy(p); m.quaternion.copy(cam.quaternion); m.renderOrder = 21;
    } else if (x.k === 'link') {   // seta/linha entre duas bolas (aliancas)
      const A = bpos(x.a, t), B = bpos(x.b, t), len = A.distanceTo(B), prog = clamp(a / .45, 0, 1) * (1 - clamp((a - (d - .3)) / .3, 0, 1) * 0);
      const m = add(new THREE.Mesh(new THREE.PlaneGeometry(1, 1), linkMat(x.col || '#ff2e63'))); m.rotation.x = -Math.PI / 2; const mid = A.clone().lerp(B, prog / 2); m.position.set(mid.x, 2.2, mid.z); m.scale.set(len * prog, x.w || .9, 1); m.rotation.z = Math.atan2(-(B.z - A.z), B.x - A.x) * 1; m.rotation.order = 'XZY'; m.rotation.set(-Math.PI / 2, 0, 0); m.rotateZ(Math.atan2(B.x - A.x, B.z - A.z) * 0); m.rotation.set(-Math.PI / 2, 0, Math.atan2(-(B.z - A.z), (B.x - A.x))); m.renderOrder = 15;
    }
  }
  // flash
  let fv = 0; for (const x of spec.flash || []) if (t >= x.t && t < x.t + (x.d ?? .25)) fv = Math.max(fv, (1 - (t - x.t) / (x.d ?? .25)) * (x.a ?? .75)); fl.style.opacity = fv; if (x => x) fl.style.background = '#fff';
  // textos (DOM)
  texts.forEach((x, i) => { const el = textEls[i], a = t - x.t, d = x.d ?? 2; if (a < 0 || a > d) { el.style.display = 'none'; return; } el.style.display = 'block'; const pin = clamp(a / .22, 0, 1), s = x.style === 'cap' ? 1 : (1 + (1 - ease(pin)) * .5) * (1 + Math.sin(clamp(a / .22, 0, 1) * Math.PI) * .12), o = clamp((d - a) / .18, 0, 1) * clamp(a / .06, 0, 1); el.style.opacity = o; el.style.transform = `scale(${s}) rotate(${x.style === 'cap' ? 0 : (x.rot ?? -3) * (1 - (1 - ease(pin)) * .5)}deg)`; });
  renderer.render(scene, cam);
};
window.getFrameDataURL = q => document.getElementById('c').toDataURL('image/jpeg', q);
window.SPEC = spec; window.ready = true;
