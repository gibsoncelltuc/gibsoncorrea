// ---------- CORE: shared world helpers for every story (assets, flags, sea, sky decor, prop pool, wind grass, set registry) ----------
const DECK = 6;
const world = new THREE.Group(); scene.add(world);
const cvs = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return [c, c.getContext('2d')]; };
const clamp01 = (x) => Math.max(0, Math.min(1, x));
const rnd = P.rng(2024);
const UPD = [];                       // per-frame updaters registered by sets: (W, f, t) => {}
const SETS_BUILT = new Set();
// ---- GLB assets (library + legacy), re-skinned with toon materials ----
const gltf = new GLTFLoader(); const LIBA = {};
async function loadLib(names) { await Promise.all(names.map(async (n) => { if (LIBA[n]) return; const g = await gltf.loadAsync(n.startsWith('mk/') ? 'assets/library/megakit/' + n.slice(3) + '.gltf' : (n.includes('/') ? 'assets/library/' : 'assets/') + n + '.glb'); LIBA[n] = g.scene;
  g.scene.traverse((o) => { if (o.isMesh) { const c = o.material.color ? o.material.color.clone() : new THREE.Color('#aaaaaa'); const mp = o.material.map || null; const em = o.material.emissive && o.material.emissive.getHex() ? { emissive: o.material.emissive.clone(), emissiveIntensity: 2.6 } : {}; o.material = toon({ color: c, ...(mp ? { map: mp } : {}), ...em, side: o.name.startsWith('sail') || n.startsWith('mk/') ? THREE.DoubleSide : THREE.FrontSide }); o.castShadow = true; o.receiveShadow = true; o.userData.c0 = c.clone(); if (n === 'bear' || n.startsWith('vehicles/')) o.material.userData.noPaint = true; /* lataria lisa como no canal */ } }); })); }
const _rgN = (n, x, z) => { const R = globalThis.REGMAP && globalThis.REGMAP[n]; return R ? R[Math.abs(Math.round(x * 0.37 + z * 0.73)) % R.length] : n; };   // CIDADE DA REGIAO: troca o predio de fundo pelo do pais/epoca da historia
const libInst = (n, x, y, z, ry = 0, s = 1, parent = world, tint = null) => { n = _rgN(n, x, z); const o = LIBA[n].clone(true); o.position.set(x, y, z); o.rotation.y = ry; o.scale.setScalar(s);
  o.traverse((m) => { if (m.isMesh) { m.material = m.material.clone(); if (tint) m.material.color.set(tint); } }); parent.add(o); return o; };
// ---- materials ----
const MW = {
  grass: texM(P.grass(11), 30, 30), dirt: texM(P.dirt(5), 8, 8), sand: toon({ color: '#e9d7a4' }), rock: toon({ color: '#8d8a86' }), snow: toon({ color: '#6a92f6' }), ice: toon({ color: '#cfe8f5' }),
  pine: toon({ color: '#2f6a3c' }), pine2: toon({ color: '#3d8248' }), trunk: toon({ color: '#6a4a32' }), plank: texM(P.planks(3), 1, 1), plaster: texM(P.plaster(6, 38), 1, 1), roof: texM(P.roof(7), 2, 2),
  red: toon({ color: '#c8402f' }), white: toon({ color: '#f1ece0' }), floor: texM(P.planks(9), 1, 1), marble: texM(P.marble(10), 1, 1), stone: texM(P.stone(4), 1, 1), cobble: texM(P.stone(8, 36, 12, 58, 64, 64), 1, 1),
  flame: toon({ color: '#ff8a1f' }), flame2: toon({ color: '#ffd23a' }), log: toon({ color: '#5c3c24' }), gold: toon({ color: '#d8a93a' }), glass: toon({ color: '#9fd6e8' }), wood: toon({ color: '#8b5a34' }), dark: toon({ color: '#2b2430' }),
};
// ---- flags ----
const flagTexCache = {};
function flagTex(kind) {
  if (flagTexCache[kind]) return flagTexCache[kind]; const [c, g] = cvs(380, 200); const F = (col, x, y, w, h) => { g.fillStyle = col; g.fillRect(x, y, w, h); };
  const tri = (a, b, d, v) => { if (v) { F(a, 0, 0, 127, 200); F(b, 127, 0, 126, 200); F(d, 253, 0, 127, 200); } else { F(a, 0, 0, 380, 67); F(b, 0, 67, 380, 66); F(d, 0, 133, 380, 67); } };
  const K = {
    us: () => { for (let i = 0; i < 13; i++) F(i % 2 ? '#fff' : '#c8282f', 0, i * 200 / 13, 380, 200 / 13 + 1); F('#26397a', 0, 0, 160, 108); g.fillStyle = '#fff'; for (let r = 0; r < 5; r++) for (let k = 0; k < 6; k++) { g.beginPath(); g.arc(14 + k * 26, 14 + r * 20, 4.2, 0, 7); g.fill(); } },
    uk: () => { F('#1f3d8a', 0, 0, 380, 200); g.strokeStyle = '#fff'; g.lineWidth = 34; g.beginPath(); g.moveTo(0, 0); g.lineTo(380, 200); g.moveTo(380, 0); g.lineTo(0, 200); g.stroke(); g.strokeStyle = '#c8282f'; g.lineWidth = 12; g.stroke(); g.strokeStyle = '#fff'; g.lineWidth = 56; g.beginPath(); g.moveTo(190, 0); g.lineTo(190, 200); g.moveTo(0, 100); g.lineTo(380, 100); g.stroke(); g.strokeStyle = '#c8282f'; g.lineWidth = 32; g.stroke(); },
    france: () => tri('#2a4a9a', '#ffffff', '#d8282f', true), italy: () => tri('#2f8a4a', '#ffffff', '#d8282f', true), mexico: () => { tri('#1f7a4a', '#ffffff', '#d8282f', true); g.fillStyle = '#9a7a3a'; g.beginPath(); g.arc(190, 100, 22, 0, 7); g.fill(); },
    germany: () => tri('#1b1b1b', '#d8282f', '#f0c030', false), poland: () => { F('#ffffff', 0, 0, 380, 100); F('#d8282f', 0, 100, 380, 100); }, spain: () => { F('#d8282f', 0, 0, 380, 50); F('#f0c030', 0, 50, 380, 100); F('#d8282f', 0, 150, 380, 50); },
    denmark: () => { F('#d8282f', 0, 0, 380, 200); F('#fff', 110, 0, 36, 200); F('#fff', 0, 82, 380, 36); }, canada: () => { F('#d8282f', 0, 0, 95, 200); F('#fff', 95, 0, 190, 200); F('#d8282f', 285, 0, 95, 200); g.fillStyle = '#d8282f'; g.beginPath(); g.moveTo(190, 40); g.lineTo(212, 90); g.lineTo(250, 80); g.lineTo(220, 118); g.lineTo(232, 160); g.lineTo(190, 135); g.lineTo(148, 160); g.lineTo(160, 118); g.lineTo(130, 80); g.lineTo(168, 90); g.fill(); },
    japan: () => { F('#fff', 0, 0, 380, 200); g.fillStyle = '#d8282f'; g.beginPath(); g.arc(190, 100, 56, 0, 7); g.fill(); }, honduras: () => { F('#2a7ad8', 0, 0, 380, 67); F('#fff', 0, 67, 380, 66); F('#2a7ad8', 0, 133, 380, 67); g.fillStyle = '#2a7ad8'; for (const x of [150, 190, 230]) { g.beginPath(); g.arc(x, 100, 9, 0, 7); g.fill(); } },
    salvador: () => { F('#1f4aa8', 0, 0, 380, 67); F('#fff', 0, 67, 380, 66); F('#1f4aa8', 0, 133, 380, 67); g.fillStyle = '#6aa84a'; g.beginPath(); g.arc(190, 100, 20, 0, 7); g.fill(); }, red: () => F('#c8282f', 0, 0, 380, 200), white: () => F('#ffffff', 0, 0, 380, 200), blue: () => F('#2a4a9a', 0, 0, 380, 200),
    zanzibar: () => F('#c8282f', 0, 0, 380, 200), modena: () => { F('#ffffff', 0, 0, 380, 200); F('#d8282f', 0, 0, 380, 100); }, bologna: () => { F('#d8282f', 0, 0, 380, 200); F('#fff', 0, 0, 190, 200); }, black: () => F('#1b1b1b', 0, 0, 380, 200),
    jolly: () => { F('#1b1b1b', 0, 0, 380, 200); g.fillStyle = '#fff'; g.beginPath(); g.arc(190, 90, 36, 0, 7); g.fill(); F('#1b1b1b', 175, 86, 12, 10); F('#1b1b1b', 195, 86, 12, 10); F('#fff', 150, 150, 80, 10); },
  };
  (K[kind] || K.white)(); return (flagTexCache[kind] = c);
}
const flags = [];
function makeFlag(kind, x, y, z, w = 2.4, h = 1.26, pole = 0, ry = 0, mirror = false) {
  const g = new THREE.PlaneGeometry(w, h, 14, 8); g.translate(w / 2, 0, 0);
  const fm = new THREE.MeshToonMaterial({ gradientMap: grad, map: P.tex(flagTex(kind)), side: THREE.DoubleSide }); fm.userData.noPaint = true; const m = add(g, fm, x, y, z, world, { cast: true }); m.rotation.y = ry; if (mirror) m.scale.x = -1; m.userData.base = Float32Array.from(g.attributes.position.array); m.userData.w = w; flags.push(m);
  if (pole) m.userData.pole = add(new THREE.CylinderGeometry(0.06, 0.08, pole, 8), toon({ color: '#6b4226' }), x - 0.05, y - h / 2 - pole / 2 + h * 0.5, z, world); return m; }
// ---- sea, far hills, clouds ----
const waterU = { t: { value: 0 }, deep: { value: new THREE.Color('#2f6f8f') }, shal: { value: new THREE.Color('#5fa8bf') }, glint: { value: new THREE.Color('#e9f6ff') } };
const waterMat = new THREE.ShaderMaterial({ uniforms: { ...THREE.UniformsUtils.clone(THREE.UniformsLib.fog), ...waterU }, fog: true,
  vertexShader: `#include <fog_pars_vertex>
    varying vec3 vW; void main(){ vec4 w = modelMatrix*vec4(position,1.); vW = w.xyz; vec4 mvPosition = viewMatrix*w; gl_Position = projectionMatrix*mvPosition;
    #include <fog_vertex>
    }`,
  fragmentShader: `#include <fog_pars_fragment>
    uniform float t; uniform vec3 deep, shal, glint; varying vec3 vW;
    float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1,311.7)))*43758.5453); }
    float noise(vec2 p){ vec2 i=floor(p), f=fract(p); f=f*f*(3.-2.*f); return mix(mix(hash(i),hash(i+vec2(1,0)),f.x), mix(hash(i+vec2(0,1)),hash(i+vec2(1,1)),f.x), f.y); }
    void main(){ vec2 p = vW.xz*vec2(.22,.22) + vec2(t*.12, -t*.2); float n = noise(p) * .55 + noise(p*2.1 + 7.) * .3 + noise(p*4.3 - t*.3) * .15; vec3 c = mix(deep, shal, .25 + .55*n);
      float streak = smoothstep(.70, .76, noise(vW.xz*vec2(.55,.35) + vec2(t*.3, -t*.5))); float foam = smoothstep(.82, .9, noise(vW.xz*vec2(.9,.9) + t*.4)); c = mix(c, glint, streak*.55 + foam*.5); gl_FragColor = vec4(c,1.);
      #include <fog_fragment>
    }` });
const water = new THREE.Mesh(new THREE.PlaneGeometry(4000, 4000), waterMat); water.rotation.x = -Math.PI / 2; water.position.set(0, DECK - 1.4, 0); water.userData.nd = waterNd; scene.add(water);
function farHills(cx, cz, col1 = '#6f87ad', col2 = '#7d94b8', n = 14, d0 = 300) { for (let i = 0; i < n; i++) { const a = -2.9 + i * (5.8 / n), d = d0 + (i % 3) * 50, r = 70 + (i * 29) % 70, hh = 12 + (i * 13) % 26; const m = add(new THREE.SphereGeometry(1, 18, 9), toon({ color: i % 2 ? col1 : col2 }), cx + Math.cos(a) * d * 0.9, DECK - 3, cz - Math.abs(Math.sin(a)) * d - 60, world, { cast: false }); m.scale.set(r, hh, r * 0.6); } }
const clouds = [];
{ const r = P.rng(90); for (let i = 0; i < 12; i++) { const c = document.createElement('canvas'); c.width = 600; c.height = 400; const pen = new T.Pen(c.getContext('2d')); pen.ol = 0; pen.g.translate(300, 200); pen.g.scale(1.4, 1.2); pen.g.translate(-300, -200); T.fxCloud(pen, i + 1); { const cg = c.getContext('2d'); cg.save(); cg.globalCompositeOperation = 'source-atop'; const gr = cg.createLinearGradient(0, 120, 0, 330); gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(1, 'rgba(190,176,236,0.55)'); cg.fillStyle = gr; cg.fillRect(0, 0, 600, 400); cg.restore(); }
  const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 0.667), new THREE.MeshBasicMaterial({ map: P.tex(c), transparent: true, fog: false, depthWrite: false })); const a = -1.2 + r() * 2.4 - Math.PI / 2, d = 420 + r() * 300; m.position.set(Math.cos(a) * d, 90 + r() * 170, Math.sin(a) * d); m.scale.setScalar(70 + r() * 90); m.userData.x0 = m.position.x; m.userData.sp = 0.5 + r() * 0.9; m.userData.ndSkip = true; m.renderOrder = -1; scene.add(m); clouds.push(m); } }
// ---- helpers for sets ----
const _rgChao = {}; let _asfFeito = false; const groundPlane = (cx, cz, w, d, mat, y = DECK, rep = 8) => { if (globalThis.ASFALTO && mat === MW.cobble) { mat = _rgChao.a || (_rgChao.a = toon({ color: '#56575d' })); if (!_asfFeito) { _asfFeito = true; for (let i = -12; i <= 12; i++) add(box(3.2, 0.02, 0.28), toon({ color: '#f2f0e6' }), cx + i * 7, y + 0.012, cz + 6.5, world); add(box(w, 0.25, 2.6), toon({ color: '#a9a8a2' }), cx, y + 0.12, cz - 9.5, world); } } else if (globalThis.REGCHAO && (mat === MW.cobble || mat === MW.marble)) { const k = mat === MW.cobble ? 'c' : 'm'; mat = _rgChao[k] || (_rgChao[k] = mat.clone()); mat.color.set(globalThis.REGCHAO); } const g = new THREE.PlaneGeometry(w, d); const uv = g.attributes.uv; for (let i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) * w / rep, uv.getY(i) * d / rep); const m = add(g, mat, cx, y, cz, world, { cast: false }); m.rotation.x = -Math.PI / 2; return m; };
const pineAt = (x, y, z, s = 1, parent = world) => { const g = new THREE.Group(); g.position.set(x, y, z); parent.add(g); add(new THREE.CylinderGeometry(0.18 * s, 0.26 * s, 1.4 * s, 7), MW.trunk, 0, 0.7 * s, 0, g);
  for (let i = 0; i < 4; i++) add(new THREE.ConeGeometry((1.7 - i * 0.32) * s, 1.9 * s, 9), i % 2 ? MW.pine2 : MW.pine, 0, (1.7 + i * 1.05) * s, 0, g); g.userData.sw = rnd() * 6; trees.push(g); return g; };
const trees = [];
const tufts = []; let tuftMeshes = [];
function makeTufts(cx, cz, w, d, N, cols, keep = () => true, h = 0.5) {
  const geo = new THREE.ConeGeometry(0.045, h, 4); geo.translate(0, h / 2, 0); const mesh = new THREE.InstancedMesh(geo, toon({ color: '#ffffff' }), N); mesh.castShadow = false; mesh.receiveShadow = true; world.add(mesh); const rg = P.rng(31 + N); const list = [];
  for (let i = 0; i < N; i++) { let x, z, k = 0; do { x = cx - w / 2 + rg() * w; z = cz - d / 2 + rg() * d; k++; } while (!keep(x, z) && k < 20); list.push({ x, z, s: 0.7 + rg() * 1.0, ph: rg() * 6.28, ry: rg() * 6.28 }); mesh.setColorAt(i, new THREE.Color(cols[i % cols.length])); } mesh.instanceColor.needsUpdate = true; tuftMeshes.push({ mesh, list }); }
const _tm = new THREE.Matrix4(), _tq = new THREE.Quaternion(), _te = new THREE.Euler(), _tp = new THREE.Vector3(), _ts = new THREE.Vector3();
function updateTufts(t) { for (const { mesh, list } of tuftMeshes) { for (let i = 0; i < list.length; i++) { const u = list[i]; const wv = windAt(u.x, u.z, t); _te.set(Math.sin(t * 1.6 + u.ph) * 0.1 * (0.5 + wv) + wv * 0.55 * WX.dz, u.ry, Math.cos(t * 1.3 + u.ph) * 0.1 * (0.5 + wv) - wv * 0.55 * WX.dx); _tq.setFromEuler(_te); _tp.set(u.x, DECK, u.z); _ts.set(u.s, u.s, u.s); _tm.compose(_tp, _tq, _ts); mesh.setMatrixAt(i, _tm); } mesh.instanceMatrix.needsUpdate = true; } }
// ---- dynamic props pool (3D library objects driven by worldAt(f).props) ----
const propPool = {};
function placeProps(list) {
  for (const k in propPool) for (const o of propPool[k]) o.visible = false;
  const used = {};
  for (const p of list || []) { const n = p.asset; used[n] = (used[n] || 0); const i = used[n]++; propPool[n] = propPool[n] || []; if (!propPool[n][i]) { const o = libInst(n, 0, 0, 0); o.traverse((m) => { if (m.isMesh) m.userData.c0 = m.material.color.clone(); }); propPool[n][i] = o; }
    const o = propPool[n][i]; o.visible = true; o.position.set(p.x, p.y ?? DECK, p.z); o.rotation.set(0, p.ry || 0, 0); o.scale.set(p.s || 1, (p.s || 1) * (p.sy ?? 1), p.s || 1);
    o.traverse((m) => { if (m.isMesh) { if (p.tint) m.material.color.set(p.tint); else if (m.userData.c0) m.material.color.copy(m.userData.c0); } });
    const t = p.t || 0; o.traverse((c) => { const nm = c.name || '';
      if (nm.startsWith('wheel')) c.rotation.x = -(p.dist || 0) / 0.45; if (nm === 'propeller' || nm === 'blades') c.rotation.z = t * 28; if (nm === 'rotor') c.rotation.y = t * 24; if (nm === 'turret') c.rotation.y = p.turret || 0; if (nm === 'barrel') { c.rotation.y = p.turret || 0; c.rotation.x = p.pitch || 0; c.position.z = (p.recoil || 0) * 0.4; } if (nm === 'body' && p.bob) c.position.y = Math.sin(t * 9) * p.bob; if (p.walk) { if (nm === 'legL') c.rotation.x = Math.sin(t * p.walk) * 0.7; if (nm === 'legR') c.rotation.x = -Math.sin(t * p.walk) * 0.7; if (nm === 'head') c.rotation.x = 0.12 * Math.sin(t * p.walk * 2); } if (p.peck && nm === 'head') c.rotation.x = 0.9 * Math.max(0, Math.sin(t * 3.2 + (p.t0 || 0)));
      // emu novo (blender/make_emu.py): joelho, pescoco que balanca/bica, corpo que sacode
      if (nm === 'shinL' && p.walk) c.rotation.x = 0.85 * Math.max(0, -Math.cos(t * p.walk)); if (nm === 'shinR' && p.walk) c.rotation.x = 0.85 * Math.max(0, Math.cos(t * p.walk));
      if (nm === 'neckp') { const w = p.walk ? 1 : 0; c.rotation.x = -0.12 * w * Math.abs(Math.sin(t * p.walk)) + 0.1 * w * Math.sin(t * p.walk * 2) + (p.peck ? 0.8 * Math.max(0, Math.sin(t * 3.2 + (p.t0 || 0))) : 0.05 * Math.sin(t * 1.7 + (p.t0 || 0))); c.rotation.z = 0.12 * Math.sin(t * (p.walk ? p.walk * 0.5 : 1.3) + (p.t0 || 0)); }
      /* removido: mexer na posicao do no 'body' descolava o corpo do pescoco/pernas */ }); }
}
// ---- main per-frame world hook ----
function worldState(W, f) {
  const t = f / 30; waterU.t.value = t;
  flags.forEach((m, i) => { const b = m.userData.base, p = m.geometry.attributes.position, w = m.userData.w; const wd = windAt(m.position.x, m.position.z, t);
    for (let k = 0; k < p.count; k++) { const x = b[k * 3], y = b[k * 3 + 1]; p.setZ(k, Math.sin((x / w) * 5.0 - t * (3 + 5 * wd) + i) * (0.12 + 0.34 * wd) * (x / w)); p.setY(k, y - Math.abs(Math.sin((x / w) * 3 - t * (2 + 3 * wd) + i)) * (0.03 + 0.08 * wd) * (x / w)); } p.needsUpdate = true; m.geometry.computeVertexNormals(); });
  trees.forEach((g) => { const wd = windAt(g.position.x, g.position.z, t); g.rotation.z = Math.sin(t * 1.1 + g.userData.sw) * 0.012 * (0.5 + wd) - wd * 0.035 * WX.dx; g.rotation.x = Math.cos(t * 0.9 + g.userData.sw) * 0.01 * (0.5 + wd) + wd * 0.035 * WX.dz; });
  clouds.forEach((c) => { const sp = c.userData.sp * (0.8 + WX.wind * 0.6); let x = c.userData.x0 + f * sp * 0.33; x = ((x + 700) % 1400 + 1400) % 1400 - 700; c.userData.rx = x; if (c.userData.rz === undefined) c.userData.rz = c.position.z; c.material.opacity = 0.96; });
  updateTufts(t); for (const u of UPD) u(W, f, t); placeProps(W.props);
}
function sceneryUpdate() {}
const rx2 = 0;
