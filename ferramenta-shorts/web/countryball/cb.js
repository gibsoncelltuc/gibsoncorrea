// Formato "countryballs no mapa 3D" v2: mapa-mundi 3D (kit/mapa_mundi.glb) com sombras, paises repintados em ONDA de invasao (cor de vertice), bolas com rosto parametrico
// (olhos/sobrancelhas/boca/pupilas que se interpolam), olhar que segue o alvo, arma com recuo, squash&stretch, camera Catmull-Rom com punch e tremor.
// Uso: index.html#<spec> carrega <spec>.json. renderFrame(f) e getFrameDataURL() como o motor principal; texto/legenda em DOM (screenshot).
import * as THREE from '../lib/three.module.js';
import { GLTFLoader } from '../lib/GLTFLoader.js';
const FPS = 30, W = 1080, H = 1920, K = Math.cos(50 * Math.PI / 180);   // K = achatamento de longitude (Europa nao fica esticada)
const spec = await (await fetch(location.hash.slice(1) + '.json')).json();
const norm = s => s.toLowerCase().replace(/[^a-z0-9]/g, '');
const clamp = (x, a, b) => Math.max(a, Math.min(b, x)), lerp = (a, b, k) => a + (b - a) * k, ease = x => x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2;
const outBack = x => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); }, outElastic = x => x <= 0 ? 0 : x >= 1 ? 1 : Math.pow(2, -9 * x) * Math.sin((x * 10 - .75) * (2 * Math.PI) / 3) + 1;
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('c'), antialias: true, preserveDrawingBuffer: true });
renderer.setSize(W, H, false); renderer.setPixelRatio(1); renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
const scene = new THREE.Scene(); scene.background = new THREE.Color(spec.sea || '#dff0ff');
const cam = new THREE.PerspectiveCamera(38, W / H, 1, 700);
scene.add(new THREE.HemisphereLight(0xffffff, 0x7f8fb8, 1.25));
const sun = new THREE.DirectionalLight(0xffffff, 1.35); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); const sc_ = sun.shadow.camera; sc_.left = -60; sc_.right = 60; sc_.top = 60; sc_.bottom = -60; sc_.near = 1; sc_.far = 400; sun.shadow.bias = -.0006; sun.shadow.radius = 4; scene.add(sun, sun.target);
// ---------- mar (textura de ondas que desliza) ----------
const seaCv = document.createElement('canvas'); seaCv.width = seaCv.height = 512; { const c = seaCv.getContext('2d'); c.fillStyle = spec.sea || '#dff0ff'; c.fillRect(0, 0, 512, 512); c.strokeStyle = 'rgba(255,255,255,.55)'; c.lineWidth = 5; c.lineCap = 'round'; for (let i = 0; i < 26; i++) { const x = (i * 97) % 512, y = (i * 61) % 512; c.beginPath(); c.moveTo(x, y); c.quadraticCurveTo(x + 18, y - 9, x + 36, y); c.quadraticCurveTo(x + 54, y + 9, x + 72, y); c.stroke(); } }
const seaTex = new THREE.CanvasTexture(seaCv); seaTex.wrapS = seaTex.wrapT = THREE.RepeatWrapping; seaTex.repeat.set(26, 26); seaTex.colorSpace = THREE.SRGBColorSpace;
const sea = new THREE.Mesh(new THREE.PlaneGeometry(900, 900), new THREE.MeshStandardMaterial({ map: seaTex, roughness: .5 })); sea.rotation.x = -Math.PI / 2; sea.position.y = -.9; sea.receiveShadow = true; scene.add(sea);
// ---------- mapa ----------
const gl = await new GLTFLoader().loadAsync('../assets/library/kit/mapa_mundi.glb');
const mapRoot = new THREE.Group(); mapRoot.scale.set(K, 1.5, 1); mapRoot.add(gl.scene); scene.add(mapRoot);
const C = {}, LAND = new THREE.Color(spec.land || '#c9ced6');
gl.scene.traverse(o => {
  if (!o.isMesh) return;
  if (o.name.toLowerCase().startsWith('oceano')) { o.visible = false; return; }
  const pos = o.geometry.attributes.position, n = pos.count, col = new Float32Array(n * 3); for (let i = 0; i < n; i++) { col[i * 3] = LAND.r; col[i * 3 + 1] = LAND.g; col[i * 3 + 2] = LAND.b; }
  o.geometry.setAttribute('color', new THREE.BufferAttribute(col, 3)); o.material = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: .5, metalness: 0 }); o.castShadow = o.receiveShadow = true;
  let cx = 0, cz = 0; for (let i = 0; i < n; i++) { cx += pos.getX(i); cz += pos.getZ(i); } C[norm(o.name)] = { mesh: o, n, cx: cx / n, cz: cz / n, key: '' };
});
// pinta o mapa por eventos: o ultimo evento que cita o pais vale; a cor nova ENTRA EM ONDA (a partir de e.from=[lon,lat] ou do centro do pais) em e.dur s
const ev = [...(spec.colors || [])].sort((a, b) => a.t - b.t);
const hex = new THREE.Color();
function stateAt(name, t) {
  let prev = LAND.clone(), cur = LAND.clone(), e0 = null;
  for (const e of ev) { if (e.t > t) break; if (e.c.some(x => norm(x) === name) || (e.all && !(e.except || []).some(x => norm(x) === name))) { prev = cur; cur = hex.set(e.col).clone(); e0 = e; } }
  return { prev, cur, e: e0 };
}
function paintCountry(name, t) {
  const o = C[name], s = stateAt(name, t), e = s.e, col = o.mesh.geometry.attributes.color; const dur = e ? (e.dur ?? .9) : 0, age = e ? t - e.t : 99, done = age >= dur + .3;
  const key = e ? `${e.t}|${done ? 'f' : Math.round(age * FPS)}` : 'base'; if (o.key === key) return; o.key = key;
  const pos = o.mesh.geometry.attributes.position, fx = e && e.from ? e.from[0] : o.cx, fz = e && e.from ? -e.from[1] : o.cz;
  let R = 1e-6; if (!done && e) for (let i = 0; i < o.n; i++) R = Math.max(R, Math.hypot((pos.getX(i) - fx) * K, pos.getZ(i) - fz));
  for (let i = 0; i < o.n; i++) {
    let p = 1; if (!done && e) { const d = Math.hypot((pos.getX(i) - fx) * K, pos.getZ(i) - fz) / R; p = clamp((age - d * dur * .75) / .3, 0, 1); p = p * p * (3 - 2 * p); }
    const k = e ? p : 1, c = e ? s.prev : s.cur; col.setXYZ(i, lerp(c.r, s.cur.r, k), lerp(c.g, s.cur.g, k), lerp(c.b, s.cur.b, k));
  }
  col.needsUpdate = true;
}
// ---------- bolas ----------
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
// ---- rosto parametrico: P = {eo,br,bh,mo,mc,pu,sw,ar,te,sp}; cada expressao e' um vetor; a transicao entre expressoes e' interpolada com "outBack" (leve exagero, natural)
const EXPR = {
  idle: { eo: 1, br: 0, bh: 0, mo: 0, mc: .2, pu: 1, sw: 0, ar: 0, te: 0, sp: 0 }, happy: { eo: .2, br: -.1, bh: .2, mo: .6, mc: 1, pu: 1, sw: 0, ar: 1, te: 0, sp: 0 },
  angry: { eo: .8, br: .6, bh: -.1, mo: .3, mc: -.8, pu: .9, sw: 0, ar: 0, te: 0, sp: 0 }, shout: { eo: .88, br: .65, bh: -.1, mo: 1, mc: -.2, pu: .8, sw: 0, ar: 0, te: 0, sp: 0 },
  scared: { eo: 1.3, br: -.35, bh: .55, mo: .5, mc: -.4, pu: .5, sw: 1, ar: 0, te: 0, sp: 0 }, cry: { eo: .85, br: -.55, bh: .1, mo: .4, mc: -1, pu: 1.1, sw: 0, ar: 0, te: 1, sp: 0 },
  smug: { eo: .5, br: .2, bh: -.05, mo: 0, mc: .8, pu: 1, sw: 0, ar: 0, te: 0, sp: 0 }, sad: { eo: .9, br: -.5, bh: .1, mo: 0, mc: -.7, pu: 1, sw: 0, ar: 0, te: 0, sp: 0 },
  dizzy: { eo: 1, br: 0, bh: 0, mo: .3, mc: 0, pu: 1, sw: 0, ar: 0, te: 0, sp: 1 }, wow: { eo: 1.25, br: -.2, bh: .5, mo: .7, mc: 0, pu: 1, sw: 0, ar: 0, te: 0, sp: 0 },
};
const PK = Object.keys(EXPR.idle);
function faceAt(b, t) {   // expressao interpolada no instante t + alvo do olhar
  const fs = b.faces || []; let i = -1; for (let k = 0; k < fs.length; k++) if (fs[k].t <= t) i = k;
  const cur = EXPR[(i >= 0 ? fs[i].e : 'idle')] || EXPR.idle, prev = EXPR[(i > 0 ? fs[i - 1].e : 'idle')] || EXPR.idle, q = i >= 0 ? clamp((t - fs[i].t) / .3, 0, 1) : 1, k = outBack(q);
  const P = {}; for (const p of PK) P[p] = lerp(prev[p], cur[p], k); return { P, at: i >= 0 ? fs[i].at : null, e: i >= 0 ? fs[i].e : 'idle' };
}
function drawBall(cv, b, P, look, blink, t, aim, weapon, flash) {   // canvas 384: a bola (r=100) fica em (128,138)+64 para caber chapeus e arma
  const c = cv.getContext('2d'); c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, 384, 384); c.translate(64, 64); const cx = 128, cy = 138, R = 100;
  c.save(); c.beginPath(); c.arc(cx, cy, R, 0, 7); c.clip(); (FLAGS[b.flag] || FLAGS.UK)(c); c.restore();
  const g = c.createRadialGradient(cx - 34, cy - 40, 8, cx, cy, R); g.addColorStop(0, 'rgba(255,255,255,.34)'); g.addColorStop(.55, 'rgba(255,255,255,0)'); g.addColorStop(1, 'rgba(0,0,50,.30)'); c.fillStyle = g; c.beginPath(); c.arc(cx, cy, R, 0, 7); c.fill();
  c.lineWidth = 9; c.strokeStyle = '#111'; c.beginPath(); c.arc(cx, cy, R, 0, 7); c.stroke();
  // olhos (seguem o olhar; o conjunto todo desliza um pouco na bola = sensacao de volume)
  const lx = look[0], ly = look[1], gx = lx * 11, gy = ly * 8, ex = [97 + gx, 159 + gx], ey = 126 + gy, bl = 1 - blink * .92; c.lineCap = 'round'; c.lineJoin = 'round';
  for (let s = 0; s < 2; s++) {
    const x = ex[s], w = 23 * (1 + (P.eo - 1) * .25), h = Math.max(1, 28 * clamp(P.eo, 0, 1.4) * bl * (1 - P.ar)), side = s ? 1 : -1;
    if (h > 3.5) { c.fillStyle = '#fff'; c.strokeStyle = '#111'; c.lineWidth = 6; c.beginPath(); c.ellipse(x, ey, w, h, 0, 0, 7); c.fill(); c.stroke();
      c.save(); c.beginPath(); c.ellipse(x, ey, w, h, 0, 0, 7); c.clip(); const pr = Math.max(5, w * .44 * P.pu); c.fillStyle = '#111'; c.beginPath(); c.arc(x + lx * (w - pr) * .9, ey + ly * Math.max(0, h - pr) * .9, pr, 0, 7); c.fill(); c.fillStyle = '#fff'; c.beginPath(); c.arc(x + lx * (w - pr) * .9 - pr * .3, ey + ly * Math.max(0, h - pr) * .9 - pr * .3, pr * .28, 0, 7); c.fill();
      if (P.sp > .5) { c.strokeStyle = '#fff'; c.lineWidth = 3; c.beginPath(); for (let a = 0; a < 18; a += .3) c.lineTo(x + Math.cos(a + t * 12) * a * 1.1, ey + Math.sin(a + t * 12) * a * 1.1); c.stroke(); }
      c.restore(); }
    if (P.ar > .02) { c.globalAlpha = clamp(P.ar * 1.2, 0, 1); c.strokeStyle = '#111'; c.lineWidth = 9; c.beginPath(); c.arc(x, ey + 10, 18, Math.PI * 1.1, Math.PI * 1.9); c.stroke(); c.globalAlpha = 1; }
    if (h <= 3.5 && P.ar <= .02) { c.strokeStyle = '#111'; c.lineWidth = 8; c.beginPath(); c.moveTo(x - w, ey); c.lineTo(x + w, ey); c.stroke(); }
    // sobrancelha: inclina (br>0 bravo = ponta interna para baixo, br<0 triste), sobe/desce (bh)
    const by = ey - 30 - P.bh * 26 - (1 - clamp(P.eo, 0, 1.4)) * 2, tilt = P.br * 15; if (Math.abs(P.br) > .04 || Math.abs(P.bh) > .04) { c.strokeStyle = '#111'; c.lineWidth = 10; c.beginPath(); c.moveTo(x - side * 24, by - tilt); c.lineTo(x + side * 24, by + tilt); c.stroke(); }
  }
  // boca: linha curva (sorriso/tristeza) que ABRE continuamente em forma de boca
  const mx = 128 + gx * .8, my = 176 + gy * .6, mw = 26 + P.mo * 14, op = Math.max(0, P.mo - .08) * 40, cv_ = P.mc * 16;
  c.strokeStyle = '#111'; c.lineWidth = 8;
  if (op > 3) { c.fillStyle = '#7a0a0a'; c.beginPath(); c.moveTo(mx - mw, my - cv_ * .3); c.quadraticCurveTo(mx, my + cv_ - op * .15, mx + mw, my - cv_ * .3); c.quadraticCurveTo(mx, my + op + cv_ * .6, mx - mw, my - cv_ * .3); c.fill(); c.stroke(); c.fillStyle = '#ff6a8a'; c.beginPath(); c.ellipse(mx, my + op * .8, mw * .45, op * .3, 0, 0, 7); c.fill(); }
  else { c.beginPath(); c.moveTo(mx - mw, my - cv_ * .4); c.quadraticCurveTo(mx, my + cv_, mx + mw, my - cv_ * .4); c.stroke(); }
  if (P.sw > .05) { c.fillStyle = '#6cc7ff'; c.strokeStyle = '#111'; c.lineWidth = 4; const sy = 86 + ((t * 60) % 26) * P.sw; c.beginPath(); c.moveTo(206, sy - 16); c.quadraticCurveTo(222, sy + 6, 206, sy + 10); c.quadraticCurveTo(190, sy + 6, 206, sy - 16); c.fill(); c.stroke(); }
  if (P.te > .05) { c.fillStyle = '#4db8ff'; for (const x of [ex[0] - 6, ex[1] + 6]) { const o = (t * 90) % 50; c.beginPath(); c.ellipse(x, 152 + o, 7, 14, 0, 0, 7); c.fill(); } }
  if (b.acc) b.acc.split('+').forEach(k => ACC[k] && ACC[k](c));
  if (weapon) {   // arma presa na lateral, apontando para o alvo; "flash" = clarao do tiro
    c.save(); c.translate(cx, cy + 22); c.rotate(aim); const kick = flash.recoil * 14; c.translate(R * .55 - kick, 0);
    c.fillStyle = '#5a3a1e'; c.fillRect(-6, -7, 38, 14); c.fillStyle = '#2a2a2a'; c.fillRect(28, -5, 74, 10); c.fillStyle = '#111'; c.fillRect(98, -7, 10, 14);
    if (flash.on) { c.fillStyle = '#fff3a0'; c.beginPath(); for (let i = 0; i < 10; i++) { const a = i * Math.PI / 5, r = i % 2 ? 12 : 34; c.lineTo(122 + Math.cos(a) * r, Math.sin(a) * r); } c.fill(); c.fillStyle = '#ff9d00'; c.beginPath(); c.arc(122, 0, 11, 0, 7); c.fill(); }
    c.restore();
  }
}
const balls = {}, ballList = spec.balls || [], mkCanvas = (n = 256) => { const cv = document.createElement('canvas'); cv.width = cv.height = n; return cv; };
for (const b of ballList) {
  const cv = mkCanvas(384), tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  const m = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 1.5), new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false }));
  const sh = new THREE.Mesh(new THREE.CircleGeometry(.5, 28), new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: .3, depthWrite: false })); sh.rotation.x = -Math.PI / 2;
  m.renderOrder = 10; sh.renderOrder = 5; scene.add(m, sh); balls[b.id] = { b, cv, tex, m, sh, seed: (b.lon * 7.13 + b.lat * 3.7) % 10, last: new THREE.Vector3() };
}
function track(arr, t, keys, mode) {   // keyframes (ordenados por t); mode 'back' = chega com leve overshoot, 'cr' = Catmull-Rom (camera)
  if (!arr || !arr.length) return null; if (t <= arr[0].t) return arr[0]; const l = arr[arr.length - 1]; if (t >= l.t) return l;
  let i = 0; while (arr[i + 1].t < t) i++; const a = arr[i], b = arr[i + 1], u = (t - a.t) / (b.t - a.t), o = {};
  if (mode === 'cr') { const p0 = arr[Math.max(0, i - 1)], p3 = arr[Math.min(arr.length - 1, i + 2)], s = u * u * (3 - 2 * u); for (const f of keys) { const m1 = (b[f] - p0[f]) * .5 * 0, m2 = 0; o[f] = lerp(a[f] ?? 0, b[f] ?? 0, s); } return o; }
  const k = mode === 'back' ? outBack(clamp(u, 0, 1)) * (u < .15 ? ease(u / .15) : 1) : ease(u); for (const f of keys) o[f] = a[f] + (b[f] - a[f]) * (mode === 'back' ? (u < .25 ? ease(u / .25) * .12 * 0 + ease(u) * 0 + ease(clamp(u * 1.25, 0, 1)) : outBack(u)) : k); return o;
}
const ballPos = (bl, t) => track(bl.b.path, t, ['lon', 'lat'], 'back') || { lon: bl.b.lon, lat: bl.b.lat };
// ---------- efeitos ----------
const fxMeshes = [], fxTex = (draw) => { const cv = mkCanvas(), c = cv.getContext('2d'); draw(c); const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t; };
const TEX = {
  boom: fxTex(c => { const g = c.createRadialGradient(128, 128, 5, 128, 128, 124); g.addColorStop(0, '#fff'); g.addColorStop(.25, '#ffe14a'); g.addColorStop(.55, '#ff6a00'); g.addColorStop(1, 'rgba(255,0,0,0)'); c.fillStyle = g; c.beginPath(); for (let i = 0; i < 24; i++) { const a = i * Math.PI / 12, r = i % 2 ? 70 : 124; c.lineTo(128 + Math.cos(a) * r, 128 + Math.sin(a) * r); } c.closePath(); c.fill(); c.lineWidth = 7; c.strokeStyle = '#2b0a00'; c.stroke(); }),
  puff: fxTex(c => { c.fillStyle = '#fff'; for (const [x, y, r] of [[90, 140, 54], [150, 130, 62], [120, 96, 56], [170, 170, 44], [80, 176, 40]]) { c.beginPath(); c.arc(x, y, r, 0, 7); c.fill(); } }),
  dot: fxTex(c => { const g = c.createRadialGradient(128, 128, 0, 128, 128, 110); g.addColorStop(0, '#fff'); g.addColorStop(.35, '#fff6a0'); g.addColorStop(1, 'rgba(255,200,0,0)'); c.fillStyle = g; c.beginPath(); c.arc(128, 128, 120, 0, 7); c.fill(); }),
  skull: fxTex(c => { c.font = '200px serif'; c.textAlign = 'center'; c.fillText('💀', 128, 190); }),
  star: fxTex(c => { star(c, 128, 128, 120, '#ffd23f'); c.lineWidth = 8; c.strokeStyle = '#2b0a00'; c.stroke(); }),
};
const linkMat = c => new THREE.MeshBasicMaterial({ color: c, transparent: true, depthWrite: false });
const bpos = (id, t) => { const p = ballPos(balls[id], t); return new THREE.Vector3(p.lon * K, 0, -p.lat); };
const texts = [...(spec.texts || [])], textEls = texts.map(x => { const d = document.createElement('div'); d.className = 'tx ' + x.style; d.textContent = x.text; if (x.top) d.style.top = x.top + 'px'; if (x.color) d.style.color = x.color; if (x.size) d.style.fontSize = x.size + 'px'; document.getElementById('wrap').appendChild(d); return d; });
const fl = document.getElementById('fl'), shots = {};   // tiros por bola (para o recuo da arma)
for (const x of spec.fx || []) if (x.k === 'shot' && x.a in balls) (shots[x.a] = shots[x.a] || []).push(x.t);

// ---- coreografia de luta: cada "lunge" = {t,dur,foe}: recua (antecipacao) -> avanca rapido -> volta com mola; o golpe (t+.4*dur) bate no alvo
const LUNGE = ph => ph < .28 ? -ease(ph / .28) * .2 : ph < .4 ? lerp(-.2, 1, ease((ph - .28) / .12)) : Math.max(0, 1 - ease((ph - .4) / .6)) * (1 + Math.sin((ph - .4) * 26) * .06 * (1 - ph));
const impulses = {};   // por bola: instantes de "pancada" (chegada, golpe dado/recebido, pulso)
for (const id in balls) impulses[id] = [];
for (const id in balls) { const b = balls[id].b; for (const l of b.lunges || []) { const th = l.t + .4 * (l.dur || 1); impulses[id].push([th, .9]); if (l.foe in impulses) impulses[l.foe].push([th, 1.3]); } for (const x of b.pulse || []) impulses[id].push([x.t, .8]); for (let i = 1; i < (b.path || []).length; i++) if (b.path[i].lon !== b.path[i - 1].lon || b.path[i].lat !== b.path[i - 1].lat) impulses[id].push([b.path[i].t, .7]); impulses[id].push([b.in ?? 0, .5]); }
const wobble = (id, t) => { let w = 0; for (const [ti, a] of impulses[id]) { const q = t - ti; if (q >= 0 && q < 1.4) w += a * Math.exp(-q * 4.2) * Math.sin(q * 19); } return clamp(w, -1.4, 1.4); };
function lungeOff(id, t, proj3) {   // deslocamento (unidades do mapa) em direcao ao alvo
  const b = balls[id].b; let ox = 0, oz = 0; for (const l of b.lunges || []) { const d = l.dur || 1, ph = (t - l.t) / d; if (ph < 0 || ph > 1) continue; const A = proj3(id), B = proj3(l.foe); const dx = B.x - A.x, dz = B.z - A.z, L = Math.hypot(dx, dz) || 1, amp = Math.max(0, L - (balls[id].b.size + balls[l.foe].b.size) * .45) * (l.reach ?? .85) + (balls[id].b.size * .15); const k = LUNGE(ph); ox += dx / L * amp * k; oz += dz / L * amp * k; }
  return [ox, oz];
}
const toScreen = (v) => { const p = v.clone().project(cam); return [p.x, -p.y]; };
window.renderFrame = f => {
  const t = f / FPS;
  // ---- camera: keyframes suaves + respiracao + tremor + punch (zoom-in rapido nos impactos)
  const k = { ...track(spec.cam, t, ['lon', 'lat', 'h', 'tilt', 'roll', 'fw'], 'cr') }; let kf = null; for (const c_ of spec.cam) if (c_.t <= t) kf = c_;
  if (kf && kf.fo && (k.fw ?? 0) > 0) { let fx_ = 0, fz_ = 0, n_ = 0; for (const id of kf.fo) { if (!(id in balls)) continue; const q = ballPos(balls[id], t - .3); fx_ += q.lon; fz_ += q.lat; n_++; } if (n_) { k.lon = lerp(k.lon, fx_ / n_, k.fw); k.lat = lerp(k.lat, fz_ / n_, k.fw); } } let sx = 0, sz = 0, punch = 0;
  for (const s of spec.shake || []) if (t >= s.t && t < s.t + s.d) { const a = (s.a || 1.2) * Math.pow(1 - (t - s.t) / s.d, 2); sx += Math.sin(t * 95) * a; sz += Math.cos(t * 81) * a; }
  for (const p of spec.punch || []) if (t >= p.t) punch += (p.a || 3) * Math.exp(-(t - p.t) * 6); for (const id in balls) for (const l of balls[id].b.lunges || []) { const q = t - (l.t + .4 * (l.dur || 1)); if (q >= 0) punch += 1.2 * Math.exp(-q * 8); if (q >= 0 && q < .25) { sx += Math.sin(t * 90) * .9 * (1 - q / .25); sz += Math.cos(t * 77) * .9 * (1 - q / .25); } }
  cam.fov = 38 - punch; cam.updateProjectionMatrix();
  const drift = [Math.sin(t * .7) * .35, Math.cos(t * .53) * .25]; const cx = (k.lon * K) + sx * .4 + drift[0], cz = -k.lat + sz * .4 + drift[1], h = k.h * (1 + Math.sin(t * .9) * .008);
  cam.position.set(cx, h, cz + h * Math.tan(k.tilt)); cam.up.set(0, 0, -1); cam.lookAt(cx, 0, cz); cam.rotateZ((k.roll || 0) + Math.sin(t * .6) * .006); cam.updateMatrixWorld();
  sun.position.set(cx - 30, 90, cz + 40); sun.target.position.set(cx, 0, cz); sun.target.updateMatrixWorld(); seaTex.offset.set(t * .012, t * .007);
  // ---- paises (onda de invasao + azulejo "salta" enquanto muda)
  for (const n in C) { const o = C[n]; paintCountry(n, t); const s = stateAt(n, t); const age = s.e ? t - s.e.t : 99, d = s.e ? (s.e.dur ?? .9) + .3 : 1; o.mesh.position.y = age >= 0 && age < d ? Math.sin(age / d * Math.PI) * 1.8 : 0; }
  // ---- bolas
  const proj = {}; for (const id in balls) { const p = ballPos(balls[id], t); proj[id] = toScreen(new THREE.Vector3(p.lon * K, 4, -p.lat)); }
  for (const id in balls) {
    const bl = balls[id], b = bl.b; let w0 = b.in ?? 0, vis; if (b.vis) { const w = b.vis.find(v => t >= v[0] && t < v[1]); vis = !!w; w0 = w ? w[0] : 0; } const a0 = t - w0; if (!b.vis) vis = a0 >= 0 && t < (b.out ?? 1e9); bl.m.visible = bl.sh.visible = vis; if (!vis) continue;
    const p = ballPos(bl, t), p2 = ballPos(bl, t + .05), p1 = ballPos(bl, t - .05), vx = (p2.lon - p1.lon) * K / .1, vz = -(p2.lat - p1.lat) / .1, speed = Math.hypot(vx, vz);
    // squash & stretch: antecipacao (encolhe antes de sair), estica andando, "bate" ao chegar
    let sq = 1, hop = 0; const pa = b.path || []; for (let i = 1; i < pa.length; i++) { const A = pa[i - 1], B = pa[i]; if (A.lon === B.lon && A.lat === B.lat) continue; if (t >= A.t - .22 && t < A.t) sq *= 1 - .16 * Math.sin((t - (A.t - .22)) / .22 * Math.PI / 2); else if (t >= B.t && t < B.t + .35) sq *= 1 - .18 * Math.exp(-(t - B.t) * 9) * Math.cos((t - B.t) * 22); }
    const mv = clamp(speed / 6, 0, 1); hop = mv * Math.abs(Math.sin(t * 10 + bl.seed)) * (b.size || 6) * .2; const S_ = b.size || 6, em = faceAt(b, t).e;
    hop += Math.abs(Math.sin(t * 3.4 + bl.seed)) * S_ * .06; if (em === 'happy') hop += Math.abs(Math.sin(t * 7 + bl.seed)) * S_ * .22; if (em === 'cry') hop += Math.abs(Math.sin(t * 8)) * S_ * .05; const wb = wobble(id, t); sq *= 1 + mv * .06 * Math.cos(t * 20 + bl.seed) + wb * .16 + (em === 'angry' || em === 'shout' ? Math.sin(t * 14) * .025 : 0); const breathe = 1 + Math.sin(t * 3 + bl.seed) * .015;
    const fc = faceAt(b, t), foe = fc.at && fc.at in proj ? proj[fc.at] : null; const me = proj[id]; let look = [Math.sin(t * 1.3 + bl.seed) * .25, Math.cos(t * .9 + bl.seed * 2) * .15];
    if (foe) { const dx = foe[0] - me[0], dy = (foe[1] - me[1]) * (H / W), m = Math.hypot(dx, dy) || 1; look = [dx / m * .95, dy / m * .8]; } else if (mv > .1) { look = [clamp(vx * .08, -.9, .9), clamp(vz * .08, -.7, .7)]; }
    const blink = ((t * 2.3 + bl.seed) % 3.1) < .09 ? 1 - Math.abs(((t * 2.3 + bl.seed) % 3.1) / .09 * 2 - 1) : 0;
    let aim = 0, flash = { on: false, recoil: 0 }; if (b.weapon) { const tgt = foe || [me[0] + 1, me[1]]; aim = Math.atan2((tgt[1] - me[1]) * (H / W), tgt[0] - me[0]); for (const st of shots[id] || []) { const q = t - st; if (q >= 0 && q < .5) { flash.recoil = Math.max(flash.recoil, Math.exp(-q * 16)); if (q < .09) flash.on = true; } } }
    const face = { ...fc.P }; if (fc.e === 'angry' || fc.e === 'shout') face.bh += Math.sin(t * 9 + bl.seed) * .08; if (fc.e === 'scared') face.mo += Math.abs(Math.sin(t * 12)) * .12; if (fc.e === 'cry') face.mo += Math.sin(t * 8) * .12; face.br += Math.sin(t * 2.3 + bl.seed) * .05; face.eo *= 1 + Math.sin(t * 1.7 + bl.seed) * .03; if (fc.e === 'shout') face.mo = clamp(fc.P.mo * (.65 + .35 * Math.abs(Math.sin(t * 16))), 0, 1);
    drawBall(bl.cv, b, face, look, blink, t, aim, b.weapon, flash); bl.tex.needsUpdate = true;
    const sz0 = (b.size || 6), pin = outElastic(clamp(a0 / .6, 0, 1)), sz = sz0 * pin; let big = 1; for (const x of b.pulse || []) if (t >= x.t && t < x.t + .5) big = 1 + Math.sin((t - x.t) / .5 * Math.PI) * (x.a || .35) * (1 + Math.sin((t - x.t) * 40) * .25);
    // empurrao (knockback) quando atingida: deslocamento curto oposto ao agressor
    const p3 = i_ => { const q = ballPos(balls[i_], t); return new THREE.Vector3(q.lon * K, 0, -q.lat); }; let [ox, oz] = lungeOff(id, t, p3); for (const x of b.knock || []) { const q = t - x.t; if (q >= 0 && q < .6) { const amp = (x.a || 2.5) * Math.exp(-q * 6) * Math.sin(q * 14); ox += (x.dx || 1) * amp; oz += (x.dz || 0) * amp; } }
    if (b.fall && t >= b.fall) { const q = clamp((t - b.fall) / .6, 0, 1); bl.m.material.opacity = 1 - clamp((t - b.fall - 1) / .8, 0, 1); bl.m.userData.fall = q * 1.5; } else { bl.m.material.opacity = 1; bl.m.userData.fall = 0; }
    const wand = [Math.sin(t * 1.9 + bl.seed) * .07 * sz + (em === 'scared' ? Math.sin(t * 61) * .04 * sz : 0), Math.cos(t * 1.5 + bl.seed * 1.7) * .06 * sz]; ox += wand[0]; oz += wand[1];
    bl.m.position.set(p.lon * K + ox, sz * .6 + 1.4 + hop, -p.lat + oz); bl.m.scale.set(sz * big * breathe / sq, sz * big * breathe * sq, 1); bl.m.quaternion.copy(cam.quaternion);
    bl.m.rotateZ(-clamp(vx * .045, -.4, .4) + bl.m.userData.fall + (flash.recoil * -.08) + wb * .22 + Math.sin(t * 2.1 + bl.seed) * .05); bl.m.updateMatrixWorld();
    bl.sh.position.set(p.lon * K + ox, .1, -p.lat + oz); const sa = 1 - clamp(hop / (sz0 * .6), 0, .6); bl.sh.scale.set(sz * .72 * sa, sz * .28 * sa, 1); bl.sh.material.opacity = bl.m.material.opacity * .3 * sa;
  }
  // ---- efeitos
  for (const m of fxMeshes) { scene.remove(m); m.geometry.dispose(); m.material.dispose(); } fxMeshes.length = 0;
  const add = m => { scene.add(m); fxMeshes.push(m); return m; };
  for (const x of spec.fx || []) {
    const a = t - x.t, d = x.d ?? .6; if (a < 0 || a > d) continue; const q = a / d;
    if (x.k === 'boom' || x.k === 'puff' || x.k === 'skull' || x.k === 'star') {
      const m = add(new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: TEX[x.k], transparent: true, depthWrite: false, opacity: x.k === 'boom' ? 1 - q * q : 1 - q, color: x.col ? new THREE.Color(x.col) : 0xffffff })));
      const s = (x.s || 7) * (x.k === 'puff' ? .6 + q : x.k === 'skull' ? 1 : .35 + Math.sin(Math.min(1, q * 1.4) * Math.PI / 2) * .9); m.scale.set(s, s, 1); m.position.set(x.lon * K, 4 + (x.k === 'skull' ? q * 4 : 0), -x.lat); m.quaternion.copy(cam.quaternion); m.rotateZ(x.k === 'boom' ? q * .6 : 0); m.renderOrder = 20;
    } else if (x.k === 'shot') {
      const A = x.a in balls ? bpos(x.a, t) : new THREE.Vector3(x.alon * K, 0, -x.alat), B = x.b in balls ? bpos(x.b, t) : new THREE.Vector3(x.blon * K, 0, -x.blat); const p = A.clone().lerp(B, clamp(q * 1.15, 0, 1)); p.y = 5;
      const m = add(new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: TEX.dot, transparent: true, depthWrite: false }))); m.scale.set(2.4, 2.4, 1); m.position.copy(p); m.quaternion.copy(cam.quaternion); m.renderOrder = 21;
    } else if (x.k === 'link') {
      const A = bpos(x.a, t), B = bpos(x.b, t), len = A.distanceTo(B), prog = clamp(a / .45, 0, 1), m = add(new THREE.Mesh(new THREE.PlaneGeometry(1, 1), linkMat(x.col || '#ff2e63'))), mid = A.clone().lerp(B, prog / 2);
      m.position.set(mid.x, 2.2, mid.z); m.scale.set(len * prog, x.w || .9, 1); m.rotation.set(-Math.PI / 2, 0, Math.atan2(-(B.z - A.z), (B.x - A.x))); m.renderOrder = 15;
    }
  }
  for (const id in balls) for (const l of balls[id].b.lunges || []) { const th = l.t + .4 * (l.dur || 1), a = t - th; if (a < 0 || a > .35) continue; const A = bpos(id, t), B = bpos(l.foe, t), mid = A.clone().lerp(B, .62); const m = add(new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: TEX.boom, transparent: true, depthWrite: false, opacity: 1 - a / .35 }))); const sz = 3.5 + Math.sin(a / .35 * Math.PI / 2) * 2.5; m.scale.set(sz, sz, 1); m.position.set(mid.x, 6, mid.z); m.quaternion.copy(cam.quaternion); m.rotateZ(a * 3); m.renderOrder = 22; }
  let fv = 0; for (const x of spec.flash || []) if (t >= x.t && t < x.t + (x.d ?? .25)) fv = Math.max(fv, (1 - (t - x.t) / (x.d ?? .25)) * (x.a ?? .75)); fl.style.opacity = fv;
  texts.forEach((x, i) => { const el = textEls[i], a = t - x.t, d = x.d ?? 2; if (a < 0 || a > d) { el.style.display = 'none'; return; } el.style.display = 'block'; const pin = clamp(a / .3, 0, 1), cap = x.style === 'cap', s = cap ? 1 : (1 + (1 - outBack(pin)) * .55), o = clamp((d - a) / .18, 0, 1) * clamp(a / .06, 0, 1); el.style.opacity = o; el.style.transform = `scale(${s}) rotate(${cap ? 0 : (x.rot ?? -3) * outBack(pin)}deg)`; });
  renderer.render(scene, cam);
};
window.getFrameDataURL = q => document.getElementById('c').toDataURL('image/jpeg', q);
window.SPEC = spec; window.ready = true;
