import * as THREE from './lib/three.module.js';
import * as T from './toon.js';
import * as P from './paint.js';
import { GLTFLoader } from './lib/GLTFLoader.js';
import { SHOTS, TOTAL, shotAt, camAt, dofAt, LIGHTS, lightFor, actorsAt, worldAt, fxAt, ASSETS, SETS_USED, SETX, HEROES } from './story.js';

const W = (typeof window !== 'undefined' && window.RENDER_W) || 1080, H = (typeof window !== 'undefined' && window.RENDER_H) || 1920;   // previews may render smaller
const canvas = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(W, H, false);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.NoToneMapping;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(40, W / H, 0.08, 1500);
const rx = (a) => a * Math.PI / 180;

// ---------- materials ----------
const grad = (() => { /* v11: 3 degraus suaves para volume 3D rico estilo Ricks Clips */ const d = new Uint8Array([134, 130, 152, 255, 208, 204, 214, 255, 255, 255, 255, 255]); const t = new THREE.DataTexture(d, 3, 1); t.minFilter = t.magFilter = THREE.LinearFilter; t.needsUpdate = true; return t; })();

// ---- PAINTED 3D look: world-space brush-stroke pigment variation on every toon material ----
THREE.MeshToonMaterial.prototype.customProgramCacheKey = function () { return this.userData && this.userData.noPaint ? 'liso' : 'pintado'; };   // sem isto o three reaproveitava o shader pintado e o noPaint nao valia
THREE.MeshToonMaterial.prototype.onBeforeCompile = function (sh) {
  if (this.userData && this.userData.noPaint) return;
  sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vWP; varying vec3 vWN;').replace('#include <begin_vertex>', '#include <begin_vertex>\n{ vec4 wp_ = modelMatrix * vec4(transformed,1.0);\n#ifdef USE_INSTANCING\n wp_ = modelMatrix * instanceMatrix * vec4(transformed,1.0);\n#endif\n vWP = wp_.xyz; vWN = normalize(mat3(modelMatrix) * objectNormal); }');
  sh.fragmentShader = sh.fragmentShader.replace('#include <common>', `#include <common>
varying vec3 vWP; varying vec3 vWN;
float h21(vec2 p){ vec3 p3 = fract(vec3(p.xyx)*.1031); p3 += dot(p3, p3.yzx+33.33); return fract((p3.x+p3.y)*p3.z); }
float vn(vec2 p){ vec2 i=floor(p), f=fract(p); f=f*f*(3.-2.*f); return mix(mix(h21(i),h21(i+vec2(1,0)),f.x), mix(h21(i+vec2(0,1)),h21(i+vec2(1,1)),f.x), f.y); }
float stroke(vec2 p, float ang, float len){ float c=cos(ang), s=sin(ang); vec2 q = vec2(c*p.x+s*p.y, -s*p.x+c*p.y); q.x /= len; return vn(q*vec2(3.2,3.9))*.6 + vn(q*vec2(7.,8.)+7.)*.4; }
vec3 paintMod(vec3 col, vec3 p, vec3 n){
  vec3 w = pow(abs(n), vec3(4.)); w /= (w.x+w.y+w.z+1e-4);
  float a = stroke(p.zy*.7, .55, 1.0)*w.x + stroke(p.xz*.7, -.35, 1.0)*w.y + stroke(p.xy*.7, .2, 1.0)*w.z;
  float b = vn(p.xz*.25+p.y*.11)*w.y + vn(p.zy*.25)*w.x + vn(p.xy*.25)*w.z;
  col *= .965 + .055*a;                        // visible brush strokes
  col += (b-.5) * vec3(.014,.005,-.013);       // pigment drift warm<->cool
  float g = vn(p.xz*9.+p.y*5.)*w.y + vn(p.zy*9.)*w.x + vn(p.xy*9.)*w.z; col *= .993 + .012*g; // fine grain (canal: campos chapados, ruido < 2%)
  return col; }
float hgt(vec3 p, vec3 n){ vec3 w = pow(abs(n), vec3(4.)); w /= (w.x+w.y+w.z+1e-4);
  float h = 0.; vec2 a = p.xz, b = p.zy, c = p.xy;
  h += (vn(a*3.1)*.5 + vn(a*8.7)*.3 + vn(a*23.)*.2)*w.y; h += (vn(b*3.1)*.5 + vn(b*8.7)*.3 + vn(b*23.)*.2)*w.x; h += (vn(c*3.1)*.5 + vn(c*8.7)*.3 + vn(c*23.)*.2)*w.z; return h; }`).replace('#include <map_fragment>', '#include <map_fragment>\n diffuseColor.rgb = paintMod(diffuseColor.rgb, vWP, normalize(vWN));').replace('#include <normal_fragment_maps>', `#include <normal_fragment_maps>
 { float h0 = hgt(vWP, normalize(vWN)); float dhx = dFdx(h0), dhy = dFdy(h0); vec3 q0 = dFdx(vViewPosition), q1 = dFdy(vViewPosition); vec3 R1 = cross(q1, normal), R2 = cross(normal, q0); float fDet = dot(q0, R1);
   float fade = 1. / (1. + .035*length(vViewPosition)); vec3 grad = sign(fDet) * (dhx*R1 + dhy*R2); normal = normalize(abs(fDet)*normal - 0.18*fade*grad); }`);
};
const toon = (opts) => new THREE.MeshToonMaterial({ gradientMap: grad, ...opts });
const texM = (c, rx_ = 1, ry_ = 1, color = '#ffffff') => toon({ map: P.tex(c, rx_, ry_), color });
const M = {
  plank: texM(P.planks(1), 1, 6), beam: texM(P.beam(2), 1, 2), beamDark: texM(P.beam(3, [28, 36, 30]), 1, 2),
  rot: texM(P.rotten(4), 1, 1), rotB: texM(P.rotten(14), 1, 1),
  stone: texM(P.stone(4), 1, 1), stoneMoss: texM(P.mossy(P.stone(4), 5, 1.2), 1, 1),
  grass: texM(P.grass(6), 40, 40), dirt: texM(P.dirt(7), 6, 30), plaster: texM(P.plaster(8), 1, 1), plaster2: texM(P.plaster(18, 28), 1, 1),
  roof: texM(P.roof(9), 2, 2), marble: texM(P.marble(10), 1, 1), marbleTop: toon({ color: '#ece2cf' }),
  trunk: toon({ color: '#6a4a32' }), cypress: toon({ color: '#3f6b36' }), pine: toon({ color: '#4c6835' }), bush: toon({ color: '#57733c' }),
  hill: toon({ color: '#647d43' }), hillFar: toon({ color: '#748a5b' }), mount: toon({ color: '#8fa7b8' }), snow: toon({ color: '#f4f6fa' }),
  iron: toon({ color: '#5c5a57' }), bronze: toon({ color: '#b08a4a' }), wood: toon({ color: '#7a5434' }), door: toon({ color: '#5a3a24' }),
  window: toon({ color: '#2b2430' }), red: toon({ color: '#b8282b' }),
};
M.banner = new THREE.MeshToonMaterial({ gradientMap: grad, map: P.tex(P.banner()), alphaTest: 0.5, side: THREE.DoubleSide });
// helmet
const helmetIn = P.tex(P.helmetInside()); helmetIn.wrapS = helmetIn.wrapT = THREE.ClampToEdgeWrapping;
M.helmIn = new THREE.MeshToonMaterial({ gradientMap: grad, map: helmetIn, side: THREE.BackSide });
M.helmOut = toon({ color: '#8f8a7e' });

// ---------- ink / normal-depth contract ----------
const NOINK = 'noink'; // userData flag: never outlined (cards, fx, water handled specially)
const ndMat = new THREE.ShaderMaterial({
  vertexShader: `varying vec3 vN; varying float vD; void main(){ vN = normalize(normalMatrix*normal); vec4 mv = modelViewMatrix*vec4(position,1.); vD = -mv.z; gl_Position = projectionMatrix*mv; }`,
  fragmentShader: `varying vec3 vN; varying float vD; void main(){ vec3 n = normalize(vN); if(!gl_FrontFacing) n = -n; gl_FragColor = vec4(n*.5+.5, vD); }`,
  side: THREE.DoubleSide,
});
const cardNd = (map) => new THREE.ShaderMaterial({
  uniforms: { map: { value: map } },
  vertexShader: `varying vec2 vUv; varying float vD; void main(){ vUv=uv; vec4 mv = modelViewMatrix*vec4(position,1.); vD=-mv.z; gl_Position=projectionMatrix*mv; }`,
  fragmentShader: `uniform sampler2D map; varying vec2 vUv; varying float vD; void main(){ if(texture2D(map,vUv).a<.5) discard; gl_FragColor=vec4(0.,0.,0.,vD); }`,
  side: THREE.DoubleSide,
});
const waterNd = new THREE.ShaderMaterial({
  vertexShader: `varying float vD; void main(){ vec4 mv = modelViewMatrix*vec4(position,1.); vD=-mv.z; gl_Position=projectionMatrix*mv; }`,
  fragmentShader: `varying float vD; void main(){ gl_FragColor=vec4(.5,1.,.5,vD); }`,
});

// ---------- helpers ----------
const add = (geo, mat, x = 0, y = 0, z = 0, parent = scene, opts = {}) => {
  const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.castShadow = opts.cast ?? true; m.receiveShadow = true; parent.add(m); return m;
};
const box = (w, h, d) => new THREE.BoxGeometry(w, h, d);
const uvScale = (geo, su, sv) => { const uv = geo.attributes.uv; for (let i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) * su, uv.getY(i) * sv); return geo; };
/** box with world-scaled UVs per face (texel density 1 tile per `t` metres) */
const tbox = (w, h, d, t = 2) => {
  const g = box(w, h, d), uv = g.attributes.uv;
  const dims = [[d, h], [d, h], [w, d], [w, d], [w, h], [w, h]];
  for (let f = 0; f < 6; f++) for (let k = 0; k < 4; k++) { const i = f * 4 + k; uv.setXY(i, uv.getX(i) * dims[f][0] / t, uv.getY(i) * dims[f][1] / t); }
  return g;
};

// ---------- sky ----------
const skyU = { top: { value: new THREE.Color() }, hor: { value: new THREE.Color() }, sunDir: { value: new THREE.Vector3() }, sunCol: { value: new THREE.Color() }, sunSize: { value: 0 }, stars: { value: 0 } };
const sky = new THREE.Mesh(new THREE.SphereGeometry(1200, 32, 16), new THREE.ShaderMaterial({
  uniforms: skyU, side: THREE.BackSide, depthWrite: false, fog: false,
  vertexShader: `varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
  fragmentShader: `uniform vec3 top, hor, sunDir, sunCol; uniform float sunSize, stars; varying vec3 vP;
    void main(){ float h = clamp(vP.y,0.,1.); vec3 c = mix(hor, top, pow(h, .42)); if(vP.y<0.) c = hor;
      float s = dot(normalize(vP), normalize(sunDir)); c += sunCol * (smoothstep(1.-sunSize, 1.-sunSize*.6, s) + .35*pow(max(s,0.), 24.)*step(.001,sunSize));
      if (stars > 0.) { vec3 d = normalize(vP); vec2 uv = vec2(atan(d.z, d.x) * 70., d.y * 140.); vec2 g = floor(uv); float r = fract(sin(dot(g, vec2(12.9898, 78.233))) * 43758.5453);   /* CEU ESTRELADO a noite (19/11) */
        vec2 f = fract(uv) - .5; float st = step(.982, r) * smoothstep(.22, .0, length(f)) * smoothstep(.04, .22, d.y); c += vec3(1., .97, .88) * st * stars * (.55 + .45 * fract(r * 91.)); }
      gl_FragColor = vec4(c,1.); }`,
}));
sky.userData.sky = true; scene.add(sky);

// ---------- lights ----------
const hemi = new THREE.HemisphereLight('#ffffff', '#ffffff', 1); scene.add(hemi);
const sun = new THREE.DirectionalLight('#ffffff', 2); sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048); sun.shadow.bias = -0.0006; sun.shadow.normalBias = 0.03; sun.shadow.radius = 2;
scene.add(sun); scene.add(sun.target);
scene.fog = new THREE.Fog('#ffffff', 40, 600);

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
  grass: texM(P.grass(11), 16, 16), dirt: texM(P.dirt(5), 8, 8), sand: toon({ color: '#e9d7a4' }), rock: toon({ color: '#8d8a86' }), snow: toon({ color: '#6a92f6' }), ice: toon({ color: '#cfe8f5' }),
  pine: toon({ color: '#3a582d' }), pine2: toon({ color: '#496838' }), trunk: toon({ color: '#6a4a32' }), plank: texM(P.planks(3), 1, 1), plaster: texM(P.plaster(6, 38), 1, 1), roof: texM(P.roof(7), 2, 2),
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
  const geo = new THREE.ConeGeometry(0.055, h * 0.36, 4); geo.translate(0, h * 0.17, 0); const mesh = new THREE.InstancedMesh(geo, toon({ color: '#ffffff' }), N); mesh.castShadow = false; mesh.receiveShadow = true; world.add(mesh); const rg = P.rng(31 + N); const list = [];
  for (let i = 0; i < N; i++) { let x, z, k = 0; do { x = cx - w / 2 + rg() * w; z = cz - d / 2 + rg() * d; k++; } while (!keep(x, z) && k < 20); list.push({ x, z, s: 0.45 + rg() * 0.55, ph: rg() * 6.28, ry: rg() * 6.28 }); mesh.setColorAt(i, new THREE.Color(cols[i % cols.length])); } mesh.instanceColor.needsUpdate = true; tuftMeshes.push({ mesh, list }); }
const _tm = new THREE.Matrix4(), _tq = new THREE.Quaternion(), _te = new THREE.Euler(), _tp = new THREE.Vector3(), _ts = new THREE.Vector3();
function updateTufts(t) { for (const { mesh, list } of tuftMeshes) { for (let i = 0; i < list.length; i++) { const u = list[i]; const wv = windAt(u.x, u.z, t); _te.set(Math.sin(t * 1.6 + u.ph) * 0.1 * (0.5 + wv) + wv * 0.55 * WX.dz, u.ry, Math.cos(t * 1.3 + u.ph) * 0.1 * (0.5 + wv) - wv * 0.55 * WX.dx); _tq.setFromEuler(_te); _tp.set(u.x, DECK, u.z); _ts.set(u.s, u.s, u.s); _tm.compose(_tp, _tq, _ts); mesh.setMatrixAt(i, _tm); } mesh.instanceMatrix.needsUpdate = true; } }
// ---- dynamic props pool (3D library objects driven by worldAt(f).props) ----
const propPool = {};
function placeProps(list) {
  for (const k in propPool) for (const o of propPool[k]) o.visible = false;
  const used = {};
  for (const p of list || []) { const n = p.asset; used[n] = (used[n] || 0); const i = used[n]++; propPool[n] = propPool[n] || []; if (!propPool[n][i]) { const o = libInst(n, 0, 0, 0); o.traverse((m) => { if (m.isMesh) m.userData.c0 = m.material.color.clone(); }); propPool[n][i] = o; }
    const o = propPool[n][i]; o.visible = true; o.position.set(p.x, p.y ?? DECK, p.z); o.rotation.set(p.rx || 0, p.ry || 0, p.rz || 0); o.scale.set(p.s || 1, (p.s || 1) * (p.sy ?? 1), p.s || 1);
    o.traverse((m) => { if (m.isMesh) { if (p.tint) m.material.color.set(p.tint); else if (m.userData.c0) m.material.color.copy(m.userData.c0); } });
    /* v13 RAIO-X: o objeto fica translucido (ve-se o que tem dentro: tanque, propulsor...). Volta ao normal quando a cena acaba. */ { const xr = p.xray || 0; if (xr || o.userData.xr) { o.userData.xr = xr; o.traverse((m) => { if (!m.isMesh) return; if (xr && !m.userData.matX) { m.userData.mat0x = m.material; m.userData.matX = m.material.clone(); m.userData.matX.transparent = true; m.userData.matX.depthWrite = false; m.userData.matX.color.set('#7fc8ff'); } if (xr) { m.material = m.userData.matX; m.material.opacity = 1 - 0.62 * xr; m.castShadow = false; } else if (m.userData.mat0x) { m.material = m.userData.mat0x; m.castShadow = true; } }); } }
    const t = p.t || 0; o.traverse((c) => { const nm = c.name || '';
      if (nm.startsWith('wheelz')) c.rotation.z = -(((p.dxw || 0) * Math.cos(p.ry || 0)) - ((p.dzw || 0) * Math.sin(p.ry || 0))) / 0.42; else if (nm.startsWith('wheel')) c.rotation.x = -(p.dist || 0) / 0.45; if (nm === 'propeller' || nm === 'blades') c.rotation.z = t * 28; if (nm === 'rotor') c.rotation.y = t * 24; if (nm === 'turret') c.rotation.y = p.turret || 0; if (nm === 'barrel') { c.rotation.y = p.turret || 0; c.rotation.x = p.pitch || 0; c.position.z = (p.recoil || 0) * 0.4; } if (nm === 'body' && p.bob) c.position.y = Math.sin(t * 9) * p.bob; if (p.walk) { if (nm === 'legL') c.rotation.x = Math.sin(t * p.walk) * 0.7; if (nm === 'legR') c.rotation.x = -Math.sin(t * p.walk) * 0.7; if (nm === 'head') c.rotation.x = 0.12 * Math.sin(t * p.walk * 2); } if (p.peck && nm === 'head') c.rotation.x = 0.9 * Math.max(0, Math.sin(t * 3.2 + (p.t0 || 0)));
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
const SETDEF = {};
// SET countryside: meadows, dirt road, hedgerows, forest backdrop, a hill, a river with a pontoon bridge, a village, haystacks. Flat ground at DECK.
SETDEF.countryside = (X) => {
  const G = (cx, cz, w, d, mat, y = DECK, rep = 8) => groundPlane(X + cx, cz, w, d, mat, y, rep);
  G(0, 20, 220, 60, MW.grass); G(0, -22, 220, 56, MW.grass); G(0, -76, 220, 52, MW.grass);            // south bank | middle | north bank (river gap between z -50..-62 -> see water below)
  G(0, 14, 220, 6.5, MW.dirt, DECK + 0.03, 6);                                                         // road
  for (const s of [-1, 1]) add(box(220, 1.6, 1.2), toon({ color: '#6b5a3a' }), X, DECK - 0.8, -50.6 - (s > 0 ? 12.2 : 0), world, { cast: false });   // river banks
  // pontoon bridge across the river (along z) at x = +10
  for (let i = 0; i < 12; i++) add(box(4.6, 0.25, 1.05), MW.plank, X + 10, DECK + 0.05, -50.2 - i * 1.0, world); for (let i = 0; i < 6; i++) add(new THREE.CylinderGeometry(0.7, 0.7, 5, 10), toon({ color: '#6a6e5a' }), X + 10, DECK - 0.35, -51 - i * 2.2, world).rotation.z = Math.PI / 2;
  // hill with trees for the spy
  const hill = add(new THREE.SphereGeometry(1, 20, 12), MW.grass, X - 22, DECK - 0.2, -30, world); hill.scale.set(9, 3.4, 8);
  // hedgerows + oaks + pines
  for (let i = 0; i < 34; i++) { const x = -52 + i * 3.1; add(new THREE.SphereGeometry(1.1 + (i % 3) * 0.2, 9, 7), toon({ color: ['#486630', '#3f5a2a', '#55733a'][i % 3] }), X + x, DECK + 0.6, -36, world).scale.y = 0.8; }
  const rf = P.rng(66); for (let i = 0; i < 26; i++) { const x = -70 + rf() * 140, z = -80 - rf() * 40; pineAt(X + x, DECK, z, 1.1 + rf() * 0.9); }
  for (let i = 0; i < 14; i++) { const sgn = i % 2 ? 1 : -1, x = sgn * (50 + rf() * 40), z = 20 + rf() * 40; const o = libInst('nature/tree_oak', X + x, DECK, z, rf() * 6, 1.1 + rf() * 0.5); o.userData.sw = rf() * 6; trees.push(o); }
  for (const [x, z, n] of [[22, -44, 'buildings/house_small'], [30, -46, 'buildings/house_two'], [40, -45, 'buildings/church'], [-50, -90, 'buildings/barn'], [-42, -92, 'buildings/windmill']]) libInst(n, X + x, DECK, z, 0.2, 1.4);
  for (let i = 0; i < 5; i++) libInst('nature/haybale', X + 30 + i * 2.6, DECK, 4 + (i % 2) * 3, rf() * 6, 1.2);
  makeTufts(X, -4, 140, 80, 2200, ['#4d682d', '#5c7838', '#6b8542', '#3f5724', '#768c48'], (x, z) => !(z > 10.5 && z < 17.5) && !(z < -49 && z > -63), 0.5);
  farHills(X, -150, '#7d93b8', '#8aa0c4', 14, 260);
  // inflation yard: compressor + hose, tire tracks layer
  const yard = new THREE.Group(); world.add(yard); const comp = new THREE.Group(); comp.position.set(X + 3.4, DECK, 3.4); yard.add(comp); add(box(1.3, 0.9, 0.9), toon({ color: '#d9822b' }), 0, 0.7, 0, comp); add(new THREE.CylinderGeometry(0.28, 0.28, 0.16, 12), MW.dark, 0.6, 0.3, 0.5, comp).rotation.z = Math.PI / 2; add(new THREE.CylinderGeometry(0.28, 0.28, 0.16, 12), MW.dark, -0.6, 0.3, 0.5, comp).rotation.z = Math.PI / 2; add(box(0.9, 0.18, 0.5), MW.dark, 0, 1.25, 0, comp);
  const hose = (x0, z0, x1, z1) => { const a = new THREE.Vector3(x0, 0.2, z0), b = new THREE.Vector3(x1, 1.0, z1), d = b.clone().sub(a), len = d.length(); const m = add(new THREE.CylinderGeometry(0.07, 0.07, len, 6), toon({ color: '#2b2b30' }), 0, 0, 0, world, { cast: false }); m.position.copy(a.clone().add(b).multiplyScalar(0.5)); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize()); m.position.y += DECK; yard.add(m); return m; };
  hose(X + 3.4, 3.4, X + 0.8, 1.0);
  const trk = []; for (const dx of [-0.95, 0.95]) { const m = add(box(0.5, 0.03, 1), toon({ color: '#4a3b2a' }), X + dx, DECK + 0.05, 8, world, { cast: false }); trk.push(m); }
  SETDEF._cs = { X, trk, yard };
  UPD.push((W, f, t) => { const k = SETDEF._cs; k.yard.visible = !!W.yard; const tr = W.tracks || 0; k.trk.forEach((m) => { m.scale.z = Math.max(0.001, tr * 14); m.position.z = 8 - 0 - tr * 7 + 7; m.visible = tr > 0.01; }); });

  };
// SET harbor: wooden pier over open sea (the water plane shows), crates, a ship, lighthouse.
SETDEF.harbor = (X) => {
  groundPlane(X, -80, 600, 340, toon({ color: '#2f86b8' }), DECK - 1.2, 8); for (let i = 0; i < 24; i++) { const w = add(box(5 + (i % 3) * 2, 0.04, 0.12), toon({ color: '#e8f6ff' }), X - 40 + (i * 7) % 90, DECK - 1.15, -6 - (i * 13) % 70, world, { cast: false }); w.userData.wv = i; }
  if (globalThis.PRAIA) {   /* PRAIA DE AREIA (desembarque, batalha na praia): areia ate a agua, espuma das ondas, dunas atras; sem pier */
    groundPlane(X, 12, 600, 64, toon({ color: '#ead6a0' }), DECK, 8); groundPlane(X, -21.5, 600, 3, toon({ color: '#d8c084' }), DECK - 0.02, 8);
    for (let i = 0; i < 30; i++) { const w = add(box(6 + (i % 4) * 2, 0.05, 0.35), toon({ color: '#f4fbff' }), X - 60 + i * 4.3, DECK - 0.6, -23.5 - (i % 3) * 1.2, world, { cast: false }); w.userData.wv = i; }
    for (let i = 0; i < 12; i++) { const d = add(new THREE.SphereGeometry(1, 16, 10), toon({ color: i % 2 ? '#e2cc92' : '#dcc489' }), X - 60 + i * 11, DECK - 2.2, 34 + (i % 3) * 6, world); d.scale.set(9, 4, 6); }
    for (let i = 0; i < 9; i++) libInst('nature/tree_palm', X - 56 + i * 14, DECK, 30 + (i % 2) * 8, i, 1.3);
    farHills(X, -150, '#7d93b8', '#8aa0c4', 12, 300); return; }
  for (let i = 0; i < 40; i++) add(box(3.2, 0.25, 7), MW.plank, X - 38 + i * 3.25, DECK - 0.05, 4, world);
  add(box(130, 1.4, 22), toon({ color: '#b9b3a6' }), X + 26, DECK - 0.75, -10.4, world); add(box(130, 0.3, 0.6), toon({ color: '#8f897c' }), X + 26, DECK + 0.1, -21.2, world);   /* cais de pedra atras do pier: tropa e multidao nao pisam na agua */
  for (let i = 0; i < 14; i++) add(new THREE.CylinderGeometry(0.3, 0.3, 3.0, 8), MW.trunk, X - 36 + i * 5.6, DECK - 1.6, 7.2, world);
  for (let i = 0; i < 6; i++) libInst('crate', X - 30 + i * 11, DECK, -3 - (i % 2) * 1.5, 0.1 * i, 1.1);
  if (!globalThis.SEM_NAVIO) libInst('ship', X + 4, DECK - 1.2, -26, 0.1, 0.8);   /* 19/11: historia moderna sem navio na narracao nao ganha navio de guerra no cais */ libInst('buildings/lighthouse', X - 48, DECK - 0.3, -10, 0, 1.4);
  farHills(X, -150, '#7d93b8', '#8aa0c4', 12, 300);
};
UPD.push((W, f, t) => { world.children.forEach((m) => { if (m.userData && m.userData.wv !== undefined) { m.position.x += Math.sin(t * 0.6 + m.userData.wv) * 0.01; m.scale.x = 1 + 0.25 * Math.sin(t * 1.3 + m.userData.wv * 2); } }); });
// ===== LOCACOES LIMPAS (v13, 24/11): cenarios SEM tema de outro video. Nada de celeiro, moinho, trigo, saco de areia, barril:
// so' chao + horizonte + o que a pesquisa visual (DOSSIE) mandar por em "itens". Cada uma tem seu X (mkvideo SETS_X).
// globalThis.LOCCFG = { loc_pista: { chao: '#333', itens: [[asset, dx, z, s, ry], ...], linhas: false, horizonte: 'nenhum' }, ... }  (vem do roteiro: "locacao")
const _locCfg = (n) => (globalThis.LOCCFG && globalThis.LOCCFG[n]) || {};
const _locItens = (n, X) => { for (const it of (_locCfg(n).itens || [])) { if (!LIBA[it[0]]) continue; libInst(it[0], X + (it[1] || 0), DECK, it[2] || -12, it[4] || 0, it[3] || 1); } };
const _locBoxCity = (X, z0, cols, n = 16, seed = 31) => { const r = P.rng(seed); for (let i = 0; i < n; i++) { const w = 7 + r() * 9, h = 10 + r() * 34, x = X - 130 + i * (260 / n) + r() * 6; const g = new THREE.Group(); g.position.set(x, DECK, z0 - r() * 30); world.add(g);
    add(box(w, h, w * 0.8), toon({ color: cols[i % cols.length] }), 0, h / 2, 0, g); const wm = new THREE.MeshBasicMaterial({ color: globalThis.LOC_NOITE ? '#ffe9a8' : '#cfe3f2' });
    for (let a = 0; a < Math.floor(h / 3.2); a++) for (let b = 0; b < 3; b++) { if (globalThis.LOC_NOITE && r() < 0.45) continue; const m = add(box(w * 0.2, 1.2, 0.08), wm, (b - 1) * w * 0.3, 2.2 + a * 3.2, w * 0.4 + 0.05, g); m.castShadow = false; } } };
SETDEF.loc_pista = (X) => {   // pista de testes / patio de evento moderno: asfalto escuro, faixas, sem nada rural
  const c = _locCfg('loc_pista'); groundPlane(X, 0, 320, 240, toon({ color: c.chao || '#3a3d45' }), DECK, 8);
  if (c.linhas !== false) { const wl = toon({ color: '#e9e9e2' }), yl = toon({ color: '#e8c33a' }); for (let i = -14; i <= 14; i++) { const m = add(box(3.4, 0.02, 0.22), wl, X + i * 7, DECK + 0.03, 3.2, world); m.castShadow = false; }
    for (const z of [-7.5, 8.5]) { const m = add(box(260, 0.02, 0.2), yl, X, DECK + 0.03, z, world); m.castShadow = false; } }
  if ((c.horizonte || 'colinas') === 'colinas') farHills(X, -150, c.cor_horizonte || '#2c3140', '#343a4c', 14, 300);
  else if (c.horizonte === 'cidade') _locBoxCity(X, -90, ['#4b5568', '#5a6478', '#3f4858', '#667189']);
  _locItens('loc_pista', X);
};
SETDEF.loc_patio = (X) => {   // patio de fabrica / area industrial moderna: concreto claro e galpoes lisos ao fundo
  const c = _locCfg('loc_patio'); groundPlane(X, 0, 320, 240, toon({ color: c.chao || '#9a9c9f' }), DECK, 8);
  const jm = toon({ color: '#85878b' }); for (let i = -10; i <= 10; i++) { const m = add(box(0.12, 0.02, 60), jm, X + i * 8, DECK + 0.02, -6, world); m.castShadow = false; }
  if (c.horizonte !== 'nenhum') { const r = P.rng(57); for (let i = 0; i < 7; i++) { const w = 26 + r() * 16, h = 9 + r() * 5, g = new THREE.Group(); g.position.set(X - 120 + i * 40, DECK, -70 - r() * 14); world.add(g); add(box(w, h, 22), toon({ color: ['#c9cdd3', '#b7bcc4', '#d6d9dd'][i % 3] }), 0, h / 2, 0, g); add(box(w + 0.6, 0.7, 22.6), toon({ color: '#6d7480' }), 0, h + 0.35, 0, g); add(box(5, 5, 0.2), toon({ color: '#58606c' }), 0, 2.5, 11.05, g); } }
  farHills(X, -190, c.cor_horizonte || '#9fb1c4', '#aebdcd', 12, 330); _locItens('loc_patio', X);
};
SETDEF.loc_deserto = (X) => {   // deserto limpo: areia, dunas e pedras. SEM fazenda, SEM trigo, SEM cerca
  const c = _locCfg('loc_deserto'); groundPlane(X, 0, 320, 240, toon({ color: c.chao || '#dcbf85' }), DECK, 8);
  const r = P.rng(71), dn = [toon({ color: '#d3b477' }), toon({ color: '#e3c992' })];
  for (let i = 0; i < 16; i++) { const m = add(new THREE.SphereGeometry(1, 16, 8), dn[i % 2], X + (r() - 0.5) * 300, DECK - 0.5, -60 - r() * 70, world); m.scale.set(22 + r() * 26, 3 + r() * 5, 14 + r() * 12); m.castShadow = false; }
  if (LIBA['nature/rocks']) for (let i = 0; i < 12; i++) libInst('nature/rocks', X + (r() - 0.5) * 200, DECK, -34 - r() * 40, r() * 6, 1.2 + r() * 1.6);
  farHills(X, -150, c.cor_horizonte || '#c9a26e', '#d6b381', 14, 290); _locItens('loc_deserto', X);
};
SETDEF.loc_campo = (X) => {   // campo aberto limpo: grama, arvores longe e colinas. SEM casa, SEM celeiro, SEM moinho
  const c = _locCfg('loc_campo'); groundPlane(X, 0, 320, 240, toon({ color: c.chao || '#86b35a' }), DECK, 8);
  makeTufts(X, 0, 200, 70, 2200, ['#7fae52', '#93bf63', '#6f9f48'], () => true, 0.32);
  const r = P.rng(93); if (LIBA['nature/tree_oak']) for (let i = 0; i < 18; i++) libInst('nature/tree_oak', X + (r() - 0.5) * 260, DECK, -42 - r() * 50, r() * 6, 1.3 + r() * 0.9);
  farHills(X, -150, c.cor_horizonte || '#6f9a66', '#80a977', 14, 290); _locItens('loc_campo', X);
};
SETDEF.loc_montanha = (X) => {   // montanha limpa: chao de pedra, picos. SEM saco de areia, SEM castelo, SEM igreja
  const c = _locCfg('loc_montanha'); groundPlane(X, 0, 320, 240, toon({ color: c.chao || '#8d8a80' }), DECK, 8);
  const r = P.rng(41), pk = [toon({ color: '#75727a' }), toon({ color: '#8a8790' }), toon({ color: '#e9edf2' })];
  for (let i = 0; i < 11; i++) { const h = 40 + r() * 50, x = X - 170 + i * 34 + r() * 10, z = -120 - r() * 50; const m = add(new THREE.ConeGeometry(26 + r() * 16, h, 7), pk[i % 2], x, DECK + h / 2 - 2, z, world); m.castShadow = false; const s = add(new THREE.ConeGeometry(9, h * 0.28, 7), pk[2], x, DECK + h * 0.86 - 2, z, world); s.castShadow = false; }
  if (LIBA['nature/rocks']) for (let i = 0; i < 16; i++) libInst('nature/rocks', X + (r() - 0.5) * 180, DECK, -22 - r() * 40, r() * 6, 1.3 + r() * 2.2);
  _locItens('loc_montanha', X);
};
SETDEF.loc_cidade = (X) => {   // cidade moderna (depois de 1950): asfalto, calcada, predios de vidro/concreto. SEM lampiao, SEM barril
  const c = _locCfg('loc_cidade'); groundPlane(X, 0, 320, 240, toon({ color: c.chao || '#50535a' }), DECK, 8);
  const cal = add(box(300, 0.16, 6), toon({ color: '#b9bcc0' }), X, DECK + 0.08, -9.5, world); cal.castShadow = false;
  const wl = toon({ color: '#e9e9e2' }); for (let i = -14; i <= 14; i++) { const m = add(box(3.0, 0.02, 0.2), wl, X + i * 7, DECK + 0.03, 4.2, world); m.castShadow = false; }
  _locBoxCity(X, -22, ['#8fa3b8', '#a9b7c6', '#7b8fa6', '#c4ccd6', '#6d7f96'], 18, 33); _locBoxCity(X, -70, ['#75869c', '#8b9ab0', '#63748b'], 14, 35); _locItens('loc_cidade', X);
};
SETDEF.loc_estudio = (X) => {   // ESTUDIO DE EXPLICACAO (cena de ciencia sem personagem): chao escuro com grade, fundo liso, nada mais
  const c = _locCfg('loc_estudio'); groundPlane(X, 0, 400, 400, new THREE.MeshBasicMaterial({ color: c.chao || '#2a5fa8', fog: false }), DECK, 8);
  const gm = new THREE.MeshBasicMaterial({ color: c.grade || '#6fb0f0', fog: false }); for (let i = -30; i <= 30; i++) { const a = add(box(0.05, 0.01, 140), gm, X + i * 2, DECK + 0.015, -20, world), b = add(box(140, 0.01, 0.05), gm, X, DECK + 0.015, -20 + i * 2, world); a.castShadow = b.castShadow = false; a.userData.ndSkip = b.userData.ndSkip = true; }
  const bk = add(new THREE.PlaneGeometry(600, 240), new THREE.MeshBasicMaterial({ color: c.fundo || '#3273c4', fog: false }), X, DECK + 100, -95, world); bk.castShadow = false; bk.userData.ndSkip = true;
};
// More sets: arctic, palace (Zanzibar shore), jungle, medieval, street, hall, stadium.
SETDEF.arctic = (X) => {
  groundPlane(X, 0, 300, 220, MW.snow, DECK, 8); groundPlane(X, -30, 120, 60, toon({ color: '#a9c2f2' }), DECK + 0.02, 8);
  const rf = P.rng(21); for (let i = 0; i < 22; i++) libInst('nature/rocks', X + (rf() - 0.5) * 180, DECK, -10 - rf() * 70, rf() * 6, 1.6 + rf() * 2.2);
  const h = add(new THREE.SphereGeometry(1, 20, 12), toon({ color: '#92aee6' }), X, DECK - 1, -80, world); h.scale.set(60, 14, 30);
  if (typeof SPEC_FLAGS !== 'undefined' && SPEC_FLAGS) { makeFlag('canada', X - 9, DECK + 3.4, -3, 2.2, 1.2, 3.4, 0); makeFlag('denmark', X + 9, DECK + 3.4, -3, 2.2, 1.2, 3.4, 0); }   /* bandeiras so' quando o roteiro pede (elas apareciam em qualquer cena de neve) */ makeTufts(X, 0, 200, 120, 500, ['#e8f0f8', '#d6e4f0'], () => true, 0.2); farHills(X, -150, '#a9bfd8', '#b9cde4', 18, 300);
};
SETDEF.palace = (X) => {
  groundPlane(X, 0, 300, 220, MW.sand, DECK, 8); groundPlane(X, 40, 300, 60, toon({ color: '#d4bd88' }), DECK + 0.02, 8);
  const rf = P.rng(33); for (let i = 0; i < 16; i++) libInst('nature/tree_palm', X + (rf() - 0.5) * 160, DECK, -30 - rf() * 40, rf() * 6, 1.6);
  libInst('buildings/castle_tower', X - 12, DECK, -55, 0, 1.6); libInst('buildings/house_two', X + 6, DECK, -56, 0, 1.3); libInst('buildings/house_two', X + 22, DECK, -58, 0, 1.2);
  libInst('buildings/church', X - 34, DECK, -60, 0.2, 1.2); farHills(X, -150, '#9ab8b0', '#aac8c0', 10, 300);
};
SETDEF.jungle = (X) => {
  groundPlane(X, 0, 300, 220, toon({ color: '#3a6a2e' }), DECK, 8); groundPlane(X, 10, 300, 8, toon({ color: '#6a5a3a' }), DECK + 0.03, 6);
  const rf = P.rng(44);
  for (let i = 0; i < 44; i++) { const g = new THREE.Group(); const x = (rf() - 0.5) * 140, z = -10 - rf() * 80 + (i % 6 === 0 ? 46 : 0); g.position.set(X + x, DECK, z); world.add(g); const s = 1.1 + rf() * 1.0;
    add(new THREE.CylinderGeometry(0.22 * s, 0.34 * s, 5 * s, 7), toon({ color: '#6a4a32' }), 0, 2.5 * s, 0, g);
    for (let k = 0; k < 4; k++) add(new THREE.SphereGeometry((1.5 + (k % 2) * 0.5) * s, 9, 7), toon({ color: ['#2f7a30', '#3f8a3a', '#25702c', '#4a9a40'][k] }), (k - 1.5) * 1.1 * s, 5.4 * s + (k % 2) * 0.7 * s, (k % 3 - 1) * 0.8 * s, g); }
  for (let i = 0; i < 28; i++) libInst('nature/bush', X + (rf() - 0.5) * 120, DECK, -10 - rf() * 40 + (i % 3 === 0 ? 30 : 0), rf() * 6, 1.6 + rf());
  makeTufts(X, 0, 200, 140, 2600, ['#3f8a3a', '#2f7a30', '#52a044'], () => true, 0.6); farHills(X, -150, '#5a8a6a', '#6a9a7a', 16, 300);
};
SETDEF.medieval = (X) => {
  const cobW = MW.cobble.clone(); cobW.color.set('#ffd9bd');   // warm the grey cobbles (the square was the least colourful ground)
  groundPlane(X, 0, 300, 220, cobW, DECK, 10); groundPlane(X, -60, 300, 100, MW.grass, DECK + 0.01, 10); makeFlag('modena', X - 10, DECK + 3.4, -6, 2.2, 1.2, 3.4, 0); makeFlag('bologna', X + 10, DECK + 3.4, -6, 2.2, 1.2, 3.4, 0); libInst('nature/fountain', X + 12, DECK, 2, 0, 0.8);
  for (let i = 0; i < 9; i++) libInst('buildings/house_small', X - 70 + i * 17, DECK, -50 - (i % 2) * 6, 0.1 * i, 1.0);
  libInst('buildings/castle_tower', X - 34, DECK, -80, 0, 1.0); libInst('buildings/castle_tower', X + 40, DECK, -84, 0, 1.0); libInst('buildings/church', X + 4, DECK, -78, 0, 1.0);
  for (let i = 0; i < 16; i++) libInst('nature/tree_oak', X + (i % 2 ? 1 : -1) * (30 + (i * 7) % 40), DECK, -20 - (i * 5) % 30, i, 1.2);
  makeTufts(X, -60, 200, 60, 600, ['#6fae43', '#5fa03a'], () => true, 0.45); farHills(X, -150, '#7d93b8', '#8aa0c4', 14, 300);
};
SETDEF.street = (X) => {
  groundPlane(X, 0, 300, 220, MW.cobble, DECK, 10);
  for (let i = 0; i < 9; i++) { libInst(i % 3 === 0 ? 'buildings/shop' : 'buildings/house_two', X - 60 + i * 14, DECK, -36 - (i % 2) * 4, 0, 1.0); libInst(i % 2 ? 'buildings/apartment' : 'buildings/house_blue', X - 60 + i * 14, DECK, -70, 0, 1.0); }
  for (let i = 0; i < 6; i++) libInst('nature/lamppost', X - 30 + i * 12, DECK, -14, 0, 1.2);
  farHills(X, -150, '#9aa4b8', '#aab4c8', 8, 300);
};
SETDEF.hall = (X) => {
  groundPlane(X, 0, 120, 100, MW.marble, DECK, 8);
  for (const sx of [-1, 1]) for (let i = 0; i < 6; i++) { add(new THREE.CylinderGeometry(0.6, 0.6, 9, 14), MW.stone, X + sx * 12, DECK + 4.5, 8 - i * 9, world); }
  add(box(120, 14, 1), MW.stone, X, DECK + 7, -44, world); add(box(1, 14, 100), MW.stone, X - 24, DECK + 7, 0, world); add(box(1, 14, 100), MW.stone, X + 24, DECK + 7, 0, world);
  for (let i = 0; i < 6; i++) { add(box(8, 0.3, 2.2), MW.wood, X - 16 + (i % 2) * 28 - 6, DECK + 0.6, -6 - Math.floor(i / 2) * 5, world); }
  add(box(6, 0.4, 3), MW.wood, X, DECK + 0.6, -18, world); add(box(6, 6, 0.5), toon({ color: '#7a1c1c' }), X, DECK + 4, -22, world);
};
SETDEF.stadium = (X) => {
  groundPlane(X, 0, 200, 140, MW.grass, DECK, 4); groundPlane(X, 0, 200, 4, MW.white, DECK + 0.03, 4);
  const NR = 8, Z0 = -18, DZ = 2.7, DY = 1.8;   /* ARQUIBANCADA LOTADA (ordem do Gibson 19/11): 9 degraus altos e perto do campo */
  for (let r = 0; r < NR; r++) add(box(170, DY, DZ + 0.05), toon({ color: r % 2 ? '#8e8e96' : '#9a9aa2' }), X, DECK + DY / 2 + r * DY, Z0 - r * DZ, world);
  add(box(170, 3.5, 1), toon({ color: '#c8c8d0' }), X, DECK + 0.6, Z0 + DZ / 2 + 0.6, world);   /* mureta na beira do campo */
  add(box(170, 2.2, 0.6), toon({ color: '#27408b' }), X, DECK + NR * DY + 1.6, Z0 - NR * DZ, world);   /* faixa do alto */
  for (const sx of [-1, 1]) { add(new THREE.CylinderGeometry(0.1, 0.1, 3, 8), MW.white, X + sx * 24, DECK + 1.5, 0, world); add(new THREE.CylinderGeometry(0.1, 0.1, 3, 8), MW.white, X + sx * 24, DECK + 3, 3, world).rotation.x = Math.PI / 2; }
  /* TORCIDA: atlas com 10 torcedores x 2 quadros (bracos para cima / acenando, gritando, rindo) desenhados com o MESMO tracado dos personagens; centenas de copias na GPU pulando fora de fase */
  const NV = 10, CWp = 300, CHp = 500, cv = document.createElement('canvas'); cv.width = NV * CWp; cv.height = 2 * CHp; const g = cv.getContext('2d');
  const camis = ['#d8282f', '#27408b', '#f1ece0', '#e8c45a', '#2f8a4a', '#7b5ac9', '#e07a2a', '#1f2f5c', '#c25a7a', '#3aa0c8'], cab = ['#2b2018', '#5a3a24', '#e8c45a', '#1b1b1f', '#8a4f1c'];
  for (let v = 0; v < NV; v++) for (let q = 0; q < 2; q++) {
    const o = { jacket: camis[v], pants: ['#3b3f52', '#2a2a30', '#4a5a7a'][v % 3], boots: '#2a2a30', skin: T.SKINS[v % T.SKINS.length], hat: v % 4 === 3 ? 'cap' : 'hair', hair: cab[v % 5], hatColor: camis[(v + 3) % NV] };
    g.setTransform(CWp / 600, 0, 0, CHp / 1000, v * CWp, q * CHp);
    try { T.bodyFront(new T.Pen(g), o, { blink: false, mode: 'stand', phase: 0, expr: q ? (v % 2 ? 'shout' : 'laugh') : (v % 2 ? 'laugh' : 'grin'), gest: q ? 'wave2' : 'up', gk: 1, gt: v * 0.3, tilt: (v % 3 - 1) * 5 }); } catch (e) { console.warn('torcida', e); }
  }
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  const FH = 2.5, geo = new THREE.PlaneGeometry(FH * 0.6, FH); geo.translate(0, FH / 2, 0);
  const pos = [], cell = [], ph = []; const rf = P.rng(77);
  for (let r = 0; r < NR; r++) for (let x = -84; x <= 84; x += 0.95) { pos.push(X + x + (rf() - 0.5) * 0.3, DECK + (r + 1) * DY - 0.15, Z0 - r * DZ + 0.2 + (rf() - 0.5) * 0.3); cell.push(Math.floor(rf() * NV)); ph.push(rf() * 6.283); }
  const N = cell.length, ig = new THREE.InstancedBufferGeometry(); ig.index = geo.index; ig.setAttribute('position', geo.attributes.position); ig.setAttribute('uv', geo.attributes.uv);
  ig.setAttribute('ofs', new THREE.InstancedBufferAttribute(new Float32Array(pos), 3)); ig.setAttribute('cell', new THREE.InstancedBufferAttribute(new Float32Array(cell), 1)); ig.setAttribute('ph', new THREE.InstancedBufferAttribute(new Float32Array(ph), 1)); ig.instanceCount = N;
  const uT = { value: 0 }, VS = `attribute vec3 ofs; attribute float cell, ph; uniform float tt; varying vec2 vUv; varying float vD;
    void main(){ float k = step(.5, fract(tt * .9 + ph / 6.283)); vUv = vec2((cell + uv.x) / ${NV}.0, (uv.y + (1. - k)) / 2.);
      vec3 p = position; float sw = sin(tt * 5. + ph) * .09; p.x += sw * p.y * .25;
      vec4 mv = modelViewMatrix * vec4(ofs + vec3(0., abs(sin(tt * 7. + ph)) * .32, 0.), 1.); mv.xy += p.xy; vD = -mv.z; gl_Position = projectionMatrix * mv; }`;
  const mat = new THREE.ShaderMaterial({ uniforms: { map: { value: tex }, tt: uT }, vertexShader: VS, side: THREE.DoubleSide,
    fragmentShader: `uniform sampler2D map; varying vec2 vUv; varying float vD; void main(){ vec4 c = texture2D(map, vUv); if (c.a < .5) discard; gl_FragColor = vec4(c.rgb * .96, 1.); }` });
  mat.toneMapped = false;
  const nd = new THREE.ShaderMaterial({ uniforms: { map: { value: tex }, tt: uT }, vertexShader: VS, side: THREE.DoubleSide,
    fragmentShader: `uniform sampler2D map; varying vec2 vUv; varying float vD; void main(){ if (texture2D(map, vUv).a < .5) discard; gl_FragColor = vec4(0., 0., 0., vD); }` });
  const crowd = new THREE.Mesh(ig, mat); crowd.frustumCulled = false; crowd.userData.nd = nd; crowd.castShadow = false; world.add(crowd);
  UPD.push((W, f, t) => { uT.value = t; });
  makeTufts(X, 0, 190, 130, 1800, ['#4f9a3e', '#5aa844'], () => true, 0.2); farHills(X, -150, '#8a96b8', '#9aa6c8', 8, 300);
};
// SET mountain: rocky war-torn slope (Monte Cassino): grey-brown rock ground, boulders, dead trees, ruins, sandbags, smoke-grey sky.
SETDEF.mountain = (X) => {
  groundPlane(X, 0, 300, 220, toon({ color: '#8c8478' }), DECK, 8); groundPlane(X, 12, 300, 10, toon({ color: '#7a6e5e' }), DECK + 0.03, 6);
  const rf = P.rng(55); makeTufts(X, 0, 240, 160, 900, ['#7f8a5a', '#6e7a4e', '#8c9660'], () => true, 0.3);
  for (let i = 0; i < 70; i++) libInst('nature/rocks', X + (rf() - 0.5) * 120, DECK, -12 - rf() * 50 + (i % 3 === 0 ? 40 : 0), rf() * 6, 0.7 + rf() * 1.6);
  for (let i = 0; i < 18; i++) { const w = add(box(1.6 + rf(), 0.5 + rf() * 0.6, 0.5), toon({ color: '#9a9488' }), X + (rf() - 0.5) * 70, DECK + 0.3, -6 - rf() * 22, world); w.rotation.y = rf() * 3; }
  for (let i = 0; i < 14; i++) { const g = new THREE.Group(); g.position.set(X + (rf() - 0.5) * 160, DECK, -16 - rf() * 40); world.add(g); add(new THREE.CylinderGeometry(0.1, 0.2, 2.6, 6), toon({ color: '#4a3a30' }), 0, 1.3, 0, g); }
  for (let i = 0; i < 6; i++) libInst('war/sandbags', X - 14 + i * 5, DECK, 8 + (i % 2) * 2, 0, 1.4);
  const hill = add(new THREE.SphereGeometry(1, 20, 12), toon({ color: '#8f8576' }), X, DECK - 1, -90, world); hill.scale.set(70, 26, 40);
  libInst('buildings/castle_tower', X + 8, DECK + 20, -86, 0, 1.6); libInst('buildings/church', X - 12, DECK + 18, -88, 0.3, 1.4);
  farHills(X, -170, '#8a8c92', '#9a9ca2', 18, 300);
};
// SET outback: red dirt, wheat fields (wind), eucalyptus, fences, rocks, windmill pump, farm, distant red ranges.
SETDEF.outback = (X) => {
  const red = toon({ color: '#b87a52' }), red2 = toon({ color: '#a86a44' });
  groundPlane(X, 0, 300, 220, red, DECK, 8);
  groundPlane(X, -22, 90, 34, toon({ color: '#d8a640' }), DECK + 0.02, 8);                         // wheat field bed
  groundPlane(X, 22, 300, 8, red2, DECK + 0.03, 6);                                                // dirt track
  const rf = P.rng(88);
  makeTufts(X, -22, 90, 34, 5200, ['#e8c14a', '#f0cd5a', '#d9a93a', '#f3d96e'], () => true, 0.9);   // wheat, wind-driven
  makeTufts(X, 10, 240, 60, 1800, ['#b9a25a', '#a8934e', '#c9b36a'], (x, z) => !(z > 18 && z < 26), 0.45);
  for (let i = 0; i < 16; i++) { const sg = i % 2 ? 1 : -1, x = sg * (14 + rf() * 70), z = -50 - rf() * 40 + (rf() > 0.7 ? 80 : 0); const g = new THREE.Group(); g.position.set(X + x, DECK, z); world.add(g); const s = 1 + rf() * 0.8;
    add(new THREE.CylinderGeometry(0.2 * s, 0.32 * s, 3.4 * s, 7), toon({ color: '#9a8a78' }), 0, 1.7 * s, 0, g);
    for (let k = 0; k < 3; k++) add(new THREE.SphereGeometry(1.2 * s, 9, 7), toon({ color: ['#7d9a6a', '#6f8c5e', '#8aa874'][k] }), (k - 1) * 1.0 * s, 3.8 * s + (k % 2) * 0.5, (k % 2) * 0.6, g); }
  for (let i = 0; i < 14; i++) { const o = libInst('nature/rocks', X + (rf() - 0.5) * 200, DECK, -40 - rf() * 40 + (i % 3 ? 70 : 0), rf() * 6, 1.4 + rf() * 1.6); o.userData.c0 = o.userData.c0; }
  for (let i = 0; i < 24; i++) libInst('nature/picket_fence', X - 46 + i * 3.8, DECK, -5.6, 0, 1.6);
  for (const [x, z, n] of [[-30, -60, 'buildings/barn'], [-18, -62, 'buildings/windmill'], [34, -58, 'buildings/house_small']]) libInst(n, X + x, DECK, z, 0.2, 1.5);
  for (let i = 0; i < 10; i++) libInst('nature/bush', X + (rf() - 0.5) * 160, DECK, 28 + rf() * 20, rf() * 6, 1.1);
  farHills(X, -140, '#c8845a', '#d49a6a', 16, 280);
};
// Set dressing: scatters small foreground/mid-ground props (barrels, crates, lanterns, signs, hay, rocks, bushes) so every take has layered depth.
const DRESS = {
  countryside: ['nature/haybale', 'crate', 'barrel', 'tools/bucket', 'nature/bush', 'tools/lantern', 'nature/rocks'],
  outback: ['nature/rocks', 'crate', 'barrel', 'nature/bush', 'tools/shovel', 'nature/haybale', 'tools/bucket'],
  arctic: ['nature/rocks', 'crate', 'barrel', 'tools/lantern', 'nature/rocks'],
  palace: ['crate', 'barrel', 'tools/lantern', 'nature/bush', 'war/drum'],
  jungle: ['nature/bush', 'nature/rocks', 'crate', 'barrel', 'tools/lantern', 'tools/axe'],
  medieval: ['barrel', 'crate', 'tools/lantern', 'war/shield', 'war/sandbags', 'tools/anvil', 'nature/haybale'],
  street: ['barrel', 'crate', 'tools/lantern', 'nature/bench', 'nature/bush', 'tools/ladder'],
  hall: ['barrel', 'crate', 'tools/lantern', 'war/drum', 'mk/Bench'],
  stadium: ['nature/bench'],
  harbor: ['crate', 'barrel', 'tools/lantern', 'war/cannonballs', 'tools/bucket'],
  mountain: ['nature/rocks', 'war/sandbags', 'crate', 'barrel', 'tools/shovel', 'tools/lantern'],
  loc_pista: ['kit/cone_transito', 'kit/barreira_jersey'], loc_patio: ['kit/cone_transito', 'kit/barreira_jersey', 'kit/palete'], loc_cidade: ['nature/bench', 'kit/cone_transito'],
  loc_deserto: ['nature/rocks'], loc_campo: ['nature/bush', 'nature/rocks'], loc_montanha: ['nature/rocks'], loc_estudio: [],
};
// ===== ENFEITE POR EPOCA (v13, 24/11, Gibson: "objeto antigo em video de 2026"): cada enfeite so' existe entre o ano [de, ate]. globalThis.ERA_ANO vem do roteiro.
// globalThis.DRESS_OFF = ['barrel', ...] (proibidos da pesquisa visual) tira o que sobrar; guerra so' com globalThis.ERA_GUERRA.
const DRESS_ERA = { barrel: [-9999, 1945], crate: [-9999, 1965], 'tools/lantern': [-9999, 1925], 'war/drum': [-9999, 1900], 'war/shield': [-9999, 1600], 'war/cannonballs': [1300, 1880], 'tools/anvil': [-9999, 1930],
  'tools/bucket': [-9999, 1975], 'tools/shovel': [-9999, 1990], 'tools/axe': [-9999, 1960], 'tools/ladder': [-9999, 1990], 'nature/haybale': [-9999, 1990], 'mk/Bench': [-9999, 1900], 'kit/cone_transito': [1950, 9999], 'kit/barreira_jersey': [1960, 9999], 'kit/palete': [1950, 9999] };
const _dressOk = (n) => { const y = globalThis.ERA_ANO, e = DRESS_ERA[n]; if (y && e && (y < e[0] || y > e[1])) return false; if (n === 'war/sandbags' && (!globalThis.ERA_GUERRA || (y && (y < 1850 || y > 1975)))) return false; if ((globalThis.DRESS_OFF || []).some((k) => n.includes(k))) return false; return true; };
for (const k of Object.keys(DRESS)) DRESS[k] = DRESS[k].filter(_dressOk);
const SWAY = []; let _swayInit = false;
function dressSet(name, X) {
  if (!_swayInit) { _swayInit = true; UPD.push((W, f, t) => { SWAY.forEach((o) => { const wd = windAt(o.position.x, o.position.z, t); o.rotation.z = Math.sin(t * (1.6 + 1.4 * wd) + o.userData.sw) * o.userData.swA * (0.5 + WX.wind * 1.4 + wd); o.rotation.x = Math.sin(t * 1.3 + o.userData.sw * 2) * o.userData.swA * 0.5; }); }); }
  const list = DRESS[name]; if (!list || !list.length) return;
  if (!['hall', 'stadium', 'harbor', 'arctic', 'loc_pista', 'loc_patio', 'loc_cidade', 'loc_estudio'].includes(name)) { const N = 110, g = new THREE.IcosahedronGeometry(1, 0), im = new THREE.InstancedMesh(g, toon({ color: '#ffffff' }), N), rq = P.rng(5 + name.length), mx = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler(), v = new THREE.Vector3(), sc = new THREE.Vector3();
    const cols = ['#8a8178', '#a39a8c', '#6f675e', '#b3a898', '#7d7468'];
    for (let i = 0; i < N; i++) { const s = 0.04 + rq() * 0.13; v.set(X + (rq() - 0.5) * 34, DECK + s * 0.3, -14 + rq() * 28); e.set(rq() * 6, rq() * 6, rq() * 6); q.setFromEuler(e); sc.set(s * (1 + rq()), s, s * (1 + rq())); mx.compose(v, q, sc); im.setMatrixAt(i, mx); im.setColorAt(i, new THREE.Color(cols[i % 5])); }
    im.castShadow = false; im.receiveShadow = true; world.add(im); } const rf = P.rng(900 + name.length * 13);
  const put = (n, x, z, s) => { if (!LIBA[n]) return; const o = libInst(n, X + x, DECK, z, rf() * 6.28, s); if (/bush|tree|lantern|haybale|scarecrow|flowerbed/.test(n)) { o.userData.sw = rf() * 6; o.userData.swA = n.includes('lantern') ? 0.09 : 0.035; SWAY.push(o); } return o; };
  if (name.startsWith('loc_')) { for (const sd of [-1, 1]) for (let i = 0; i < 5; i++) { const n = list[Math.floor(rf() * list.length)]; put(n, sd * (8.5 + rf() * 9), -7 - rf() * 9, 0.95 + rf() * 0.25); } return; }   /* v13 locacao limpa: poucos objetos, so' nas LATERAIS e ao fundo (o centro e' do objeto/da acao) */
  const fg = list.filter((n) => !/bucket|haybale|bush|tree|palm|ladder|bench|flowerbed|sandbags/.test(n)); const fgl = fg.length ? fg : list;
  for (const k of [-1, 0, 1]) for (let i = 0; i < 5; i++) { const n = fgl[Math.floor(rf() * fgl.length)]; const side = rf() < 0.5 ? -1 : 1; const x = k * 8 + side * (2.6 + rf() * 2.8); put(n, x, 5.2 + rf() * 3.0, 0.42 + rf() * 0.3); }
  for (const k of [-1, 0, 1]) for (let i = 0; i < 4; i++) { const n = list[Math.floor(rf() * list.length)]; const side = rf() < 0.5 ? -1 : 1; const x = k * 8 + side * (3.2 + rf() * 5); put(n, x, -2.5 - rf() * 5, 0.9 + rf() * 0.6); }
}
// ---------- boot: load assets, build the sets this story uses ----------
const DRESS_ASSETS = [...new Set(SETS_USED.flatMap((s) => DRESS[s] || []))];
await loadLib([...new Set([...ASSETS, ...DRESS_ASSETS, ...Object.values(globalThis.REGMAP || {}).flat()])]);
for (const s of SETS_USED) { SETDEF[s](SETX[s] ?? 0); SETS_BUILT.add(s); if (!window.NODRESS) dressSet(s, SETX[s] ?? 0); }
// ---------- weather + lighting extras (shared by every story): rim light, sun glow, light shafts, WEATHER (wind/rain/snow/fog/leaves) ----------
const rimLight = new THREE.DirectionalLight('#8fb4ff', 0); rimLight.castShadow = false; scene.add(rimLight); scene.add(rimLight.target);
const ND_SKIP = (m) => { m.userData.ndSkip = true; return m; };

// ---- dust motes floating in the light (Ricks Clips: specks drifting in the sunbeams) ----
const MOTES = 220, moteGeo = new THREE.BufferGeometry(); moteGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(MOTES * 3), 3));
const moteMat = new THREE.PointsMaterial({ size: 0.075, color: '#fff0c4', transparent: true, opacity: 0.6, depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: true, fog: false });
const motes = ND_SKIP(new THREE.Points(moteGeo, moteMat)); motes.frustumCulled = false; motes.renderOrder = 6; scene.add(motes);
const moteSeed = Array.from({ length: MOTES }, (_, i) => { const r = P.rng(700 + i); return [r(), r(), r(), r(), r(), r()]; });
function updateMotes(f, C, on) {
  motes.visible = on; if (!on) return; const px = C.pos, lk = C.look; let fx = lk[0] - px[0], fy = lk[1] - px[1], fz = lk[2] - px[2]; const fl = Math.hypot(fx, fy, fz) || 1; fx /= fl; fy /= fl; fz /= fl;
  let rx_ = fz, rz_ = -fx; const rl = Math.hypot(rx_, rz_) || 1; rx_ /= rl; rz_ /= rl; const ux = -fy * rx_, uy = fx * rz_ - fz * rx_, uz = fy * rz_; const t = f / 30; const pos = moteGeo.attributes.position;
  for (let i = 0; i < MOTES; i++) { const s = moteSeed[i], d = 2.5 + s[0] * 14, ox = (s[1] - 0.5) * d * 0.9, oy = (s[2] - 0.5) * d * 1.5;
    const dx = Math.sin(t * (0.4 + s[3]) + s[4] * 6) * 0.5, dy = Math.sin(t * (0.3 + s[5] * 0.5) + s[3] * 6) * 0.45 - ((t * 0.15 * (0.4 + s[4])) % 1.2), dz = Math.cos(t * (0.35 + s[4]) + s[1] * 6) * 0.5;
    pos.setXYZ(i, px[0] + fx * d + rx_ * ox + ux * oy + dx, px[1] + fy * d + uy * oy + dy, px[2] + fz * d + rz_ * ox + uz * oy + dz); }
  pos.needsUpdate = true; moteMat.opacity = 0.16 + 0.14 * Math.min(1, (C.moteK ?? 1)); }
// sun glow + light shafts
const glowTex = (() => { const [c, g] = cvs(256, 256); const gr = g.createRadialGradient(128, 128, 4, 128, 128, 128); gr.addColorStop(0, 'rgba(255,240,200,1)'); gr.addColorStop(0.25, 'rgba(255,220,160,.5)'); gr.addColorStop(1, 'rgba(255,200,120,0)'); g.fillStyle = gr; g.fillRect(0, 0, 256, 256); return c; })();
const sunGlow = ND_SKIP(new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: P.tex(glowTex), transparent: true, depthWrite: false, fog: false, blending: THREE.AdditiveBlending }))); sunGlow.renderOrder = -1; scene.add(sunGlow);
const shaftTex = (() => { const [c, g] = cvs(64, 256); const gr = g.createLinearGradient(0, 0, 64, 0); gr.addColorStop(0, 'rgba(255,230,170,0)'); gr.addColorStop(0.5, 'rgba(255,230,170,.9)'); gr.addColorStop(1, 'rgba(255,230,170,0)'); g.fillStyle = gr; g.fillRect(0, 0, 64, 256); const g2 = g.createLinearGradient(0, 0, 0, 256); g2.addColorStop(0, 'rgba(0,0,0,0)'); g2.addColorStop(1, 'rgba(0,0,0,1)'); g.globalCompositeOperation = 'destination-in'; g.fillStyle = g2; g.fillRect(0, 0, 64, 256); return c; })();
const shafts = []; for (let i = 0; i < 7; i++) { const m = ND_SKIP(new THREE.Mesh(new THREE.PlaneGeometry(2.6, 22), new THREE.MeshBasicMaterial({ map: P.tex(shaftTex), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0.0, side: THREE.DoubleSide }))); m.renderOrder = 3; scene.add(m); shafts.push(m); }
// ---------- WEATHER SYSTEM (always on in the engine): wind, gusts, rain, snow, fog, leaves, lightning ----------
// W.weather = { wind: 0..1.5, dx, dz (wind direction), rain: 0..1, snow: 0..1, fog: 0..1, leaves: 0..1 }. Defaults: light breeze.
const WX = { wind: 0.5, dx: 1, dz: 0.25, rain: 0, snow: 0, fog: 0, leaves: 0, gust: 0 };
const WX_DEFAULT = { wind: 0.5, dx: 1, dz: 0.25, rain: 0, snow: 0, fog: 0, leaves: 0 };
const windAt = (x, z, t) => { const g = 0.5 + 0.5 * Math.sin(t * 1.3 - (x * WX.dx + z * WX.dz) * 0.09 + Math.sin(z * 0.05) * 2); return WX.wind * (0.55 + 0.9 * g * (0.4 + 0.6 * WX.wind)); };   // traveling gust wave
const RAIN_N = 3000, SNOW_N = 1500, LEAF_N = 70;
const rainMesh = new THREE.InstancedMesh(new THREE.BoxGeometry(0.016, 1.0, 0.016), new THREE.MeshBasicMaterial({ color: '#cfe4ff', transparent: true, opacity: 0.55, depthWrite: false, fog: false }), RAIN_N); rainMesh.userData.ndSkip = true; rainMesh.frustumCulled = false; rainMesh.renderOrder = 4; scene.add(rainMesh);
const snowMesh = new THREE.InstancedMesh(new THREE.SphereGeometry(0.035, 5, 4), new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: 0.95, depthWrite: false, fog: false }), SNOW_N); snowMesh.userData.ndSkip = true; snowMesh.frustumCulled = false; snowMesh.renderOrder = 4; scene.add(snowMesh);
const leafMesh = new THREE.InstancedMesh(new THREE.PlaneGeometry(0.16, 0.1), new THREE.MeshBasicMaterial({ color: '#ffffff', side: THREE.DoubleSide, transparent: true, depthWrite: false }), LEAF_N); leafMesh.userData.ndSkip = true; leafMesh.frustumCulled = false; leafMesh.renderOrder = 4; scene.add(leafMesh);
{ const c = ['#e0a13a', '#c4572c', '#8fb54a', '#f1c85a', '#b8743a']; for (let i = 0; i < LEAF_N; i++) leafMesh.setColorAt(i, new THREE.Color(c[i % c.length])); leafMesh.instanceColor.needsUpdate = true; }
const rp = P.rng(404), RSEED = [], SSEED = [], LSEED = []; for (let i = 0; i < RAIN_N; i++) RSEED.push([rp(), rp(), rp()]); for (let i = 0; i < SNOW_N; i++) SSEED.push([rp(), rp(), rp(), rp()]); for (let i = 0; i < LEAF_N; i++) LSEED.push([rp(), rp(), rp(), rp()]);
const _qq = new THREE.Quaternion(), _ee = new THREE.Euler(), _pp = new THREE.Vector3(), _ss = new THREE.Vector3(), _mm = new THREE.Matrix4();
function weatherParticles(f, camPos) {
  const t = f / 30, R = 10;
  rainMesh.visible = WX.rain > 0.02; if (rainMesh.visible) {
    const n = Math.floor(RAIN_N * Math.min(1, WX.rain)), slant = Math.atan2(WX.wind * 0.9, 1); rainMesh.count = n;
    for (let i = 0; i < n; i++) { const r = RSEED[i]; const y = ((r[1] * 16 - t * 15 * (0.8 + r[2] * 0.4)) % 16 + 16) % 16; _pp.set(camPos.x + (r[0] - 0.5) * 2 * R + (16 - y) * 0.3 * WX.wind * WX.dx, camPos.y - 4 + y, camPos.z + (r[2] - 0.5) * 2 * R + (16 - y) * 0.3 * WX.wind * WX.dz); _ee.set(0.0, 0, -slant * WX.dx); _qq.setFromEuler(_ee); { const nr = Math.hypot(_pp.x - camPos.x, _pp.z - camPos.z) < 3.4 ? 0 : 1; _ss.set(nr, nr, nr); } /* sem riscos gigantes colados na lente */ _mm.compose(_pp, _qq, _ss); rainMesh.setMatrixAt(i, _mm); } rainMesh.instanceMatrix.needsUpdate = true; }
  snowMesh.visible = WX.snow > 0.02; if (snowMesh.visible) {
    const n = Math.floor(SNOW_N * Math.min(1, WX.snow)); snowMesh.count = n;
    for (let i = 0; i < n; i++) { const r = SSEED[i]; const y = ((r[1] * 14 - t * (1.0 + r[3] * 1.2)) % 14 + 14) % 14; _pp.set(camPos.x + (r[0] - 0.5) * 2 * R + Math.sin(t * 1.3 + r[3] * 9) * 0.6 + (14 - y) * 0.5 * WX.wind * WX.dx, camPos.y - 3 + y, camPos.z + (r[2] - 0.5) * 2 * R + Math.cos(t * 1.1 + r[3] * 7) * 0.5 + (14 - y) * 0.5 * WX.wind * WX.dz); _ss.setScalar(0.7 + r[3]); _mm.compose(_pp, _qq.identity(), _ss); snowMesh.setMatrixAt(i, _mm); } snowMesh.instanceMatrix.needsUpdate = true; }
  leafMesh.visible = WX.leaves > 0.02; if (leafMesh.visible) {
    const n = Math.floor(LEAF_N * Math.min(1, WX.leaves)); leafMesh.count = n;
    for (let i = 0; i < n; i++) { const r = LSEED[i]; const u = ((r[0] + t * (0.05 + 0.05 * WX.wind) * (0.6 + r[3])) % 1 + 1) % 1; _pp.set(camPos.x - 16 + u * 32 * WX.dx + Math.sin(t * 2 + r[1] * 9) * 0.8, camPos.y - 1.5 + r[2] * 6 + Math.sin(t * 1.5 + r[3] * 7) * 0.8, camPos.z - 14 + r[1] * 20); _ee.set(t * 3 + r[3] * 9, t * 2 + r[1] * 5, t * 4); _qq.setFromEuler(_ee); _ss.setScalar(1); _mm.compose(_pp, _qq, _ss); leafMesh.setMatrixAt(i, _mm); } leafMesh.instanceMatrix.needsUpdate = true; }
}

function setWeather(W) { const w = window.WXO || W.weather || WX_DEFAULT; WX.wind = w.wind ?? 0.5; WX.dx = w.dx ?? 1; WX.dz = w.dz ?? 0.25; WX.rain = w.rain || 0; WX.snow = w.snow || 0; WX.fog = w.fog || 0; WX.leaves = w.leaves || 0; }
function sceneryLights(L, f, C, focus) {
  if (WX.fog > 0) { scene.fog.near = Math.max(8, scene.fog.near * (1 - 0.85 * WX.fog)); scene.fog.far = Math.max(60, scene.fog.far * (1 - 0.7 * WX.fog)); scene.fog.color.lerp(new THREE.Color('#c9d2dc'), 0.6 * WX.fog); }
  if (WX.rain > 0.02) { scene.fog.color.lerp(new THREE.Color('#7f8da0'), 0.5 * WX.rain); scene.fog.far *= 1 - 0.4 * WX.rain; hemi.intensity *= 1 - 0.25 * WX.rain; sun.intensity *= 1 - 0.45 * WX.rain; }
  // rim light: opposite the sun, colored; sun glow in the sky; volumetric shafts on request
  const az = (L.az + 180) * Math.PI / 180, el = Math.max(8, L.el * 0.7) * Math.PI / 180;
  rimLight.color.set(L.rimC || '#9fc0ff'); rimLight.intensity = L.rimI ?? 0.55; rimLight.position.set(focus.x + Math.cos(el) * Math.cos(az) * 60, focus.y + Math.sin(el) * 60, focus.z + Math.cos(el) * Math.sin(az) * 60); rimLight.target.position.copy(focus);
  const sa = L.az * Math.PI / 180, se = L.el * Math.PI / 180; sunGlow.position.set(C.pos[0] + Math.cos(se) * Math.cos(sa) * 1000, C.pos[1] + Math.sin(se) * 1000, C.pos[2] + Math.cos(se) * Math.sin(sa) * 1000); sunGlow.lookAt(C.pos[0], C.pos[1], C.pos[2]); sunGlow.scale.setScalar(L.glow ? 520 : 0.0001); sunGlow.material.opacity = L.glow || 0;
  updateMotes(f, C, !!L.shafts);
  shafts.forEach((m, i) => { m.visible = !!L.shafts; if (!L.shafts) return; const k = i / (shafts.length - 1) - 0.5; m.material.opacity = L.shafts * (0.35 + 0.25 * Math.sin(f * 0.03 + i)); m.position.set(C.look[0] + k * 9 + Math.sin(f * 0.01 + i) * 0.4, C.look[1] + 8, C.look[2] - 3 - Math.abs(k) * 4); m.rotation.set(0, Math.atan2(C.pos[0] - m.position.x, C.pos[2] - m.position.z), -0.35); });
}// ===== VFX 3D ANCORADO NO OBJETO (v13, 24/11, Gibson: "a fumaca, a propulsao funcionando", "voce economiza na animacao") =====
// Particulas deterministicas (funcao pura do quadro): cada uma nasce na pose que o objeto tinha no quadro em que nasceu e segue a fisica do tipo dela.
// Entrada: W.vfx (web/runtime.js worldAt). Tipos: jato (propulsor de gas frio: sai de baixo, bate no chao e se espalha), pneu, poeira, fogo, faisca, vapor, velocidade, onda, brilho.
const VFXN = 900, _vh = (n) => { const x = Math.sin(n * 12.9898 + 4.1414) * 43758.5453; return x - Math.floor(x); };
const vfxPuff = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(1, 1), toon({ color: '#ffffff' }), VFXN); vfxPuff.frustumCulled = false; vfxPuff.castShadow = false; vfxPuff.receiveShadow = false; vfxPuff.instanceColor = new THREE.InstancedBufferAttribute(new Float32Array(VFXN * 3).fill(1), 3); scene.add(vfxPuff);
const vfxGlow = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(1, 1), new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: 0.85, depthWrite: false, blending: THREE.AdditiveBlending, fog: false }), VFXN); vfxGlow.frustumCulled = false; vfxGlow.userData.ndSkip = true; vfxGlow.renderOrder = 5; vfxGlow.instanceColor = new THREE.InstancedBufferAttribute(new Float32Array(VFXN * 3).fill(1), 3); scene.add(vfxGlow);
const vfxCone = new THREE.InstancedMesh(new THREE.ConeGeometry(1, 1, 12, 1, true), new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: 0.8, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, fog: false }), 64); vfxCone.frustumCulled = false; vfxCone.userData.ndSkip = true; vfxCone.renderOrder = 5; vfxCone.instanceColor = new THREE.InstancedBufferAttribute(new Float32Array(64 * 3).fill(1), 3); scene.add(vfxCone);
const vfxLine = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: 0.75, depthWrite: false, fog: false }), 160); vfxLine.frustumCulled = false; vfxLine.userData.ndSkip = true; vfxLine.renderOrder = 5; scene.add(vfxLine);
const vfxRing = new THREE.InstancedMesh(new THREE.TorusGeometry(1, 0.06, 6, 40), new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: 0.8, depthWrite: false, fog: false }), 24); vfxRing.frustumCulled = false; vfxRing.userData.ndSkip = true; vfxRing.renderOrder = 5; scene.add(vfxRing);
const vfxLight = new THREE.PointLight('#bfe6ff', 0, 14, 1.6); vfxLight.castShadow = false; scene.add(vfxLight);
const _vD = new THREE.Object3D(), _vM = new THREE.Matrix4(), _vQ = new THREE.Quaternion(), _vS = new THREE.Vector3(), _vP = new THREE.Vector3(), _vC = new THREE.Color(), _vUp = new THREE.Vector3(0, 1, 0), _vDir = new THREE.Vector3(), _vBB = {};
const vfxBox = (asset) => { if (_vBB[asset]) return _vBB[asset]; const o = LIBA[asset]; if (!o) return (_vBB[asset] = { min: new THREE.Vector3(-1, 0, -1), max: new THREE.Vector3(1, 1, 1) }); const s0 = o.scale.clone(), p0 = o.position.clone(), r0 = o.rotation.clone(); o.position.set(0, 0, 0); o.rotation.set(0, 0, 0); o.scale.setScalar(1); o.updateMatrixWorld(true); const b = new THREE.Box3().setFromObject(o); o.position.copy(p0); o.rotation.copy(r0); o.scale.copy(s0); o.updateMatrixWorld(true); return (_vBB[asset] = b); };
const vfxPts = (e) => { if (Array.isArray(e.pts)) return e.pts; const b = vfxBox(e.asset), cx = (b.min.x + b.max.x) / 2, cz = (b.min.z + b.max.z) / 2, hx = (b.max.x - b.min.x) * 0.33, hz = (b.max.z - b.min.z) * 0.33, y0 = b.min.y + (b.max.y - b.min.y) * 0.12;
  if (e.pts === 'centro') return [[cx, y0, cz]]; if (e.pts === 'topo') return [[cx, b.max.y, cz]]; if (e.pts === 'meio') return [[cx, (b.min.y + b.max.y) / 2, cz]];
  return [[cx - hx, y0, cz - hz], [cx + hx, y0, cz - hz], [cx - hx, y0, cz + hz], [cx + hx, y0, cz + hz]]; };
const vfxPose = (ps) => { _vD.position.set(ps[0], ps[1], ps[2]); _vD.rotation.set(ps[3], ps[4], ps[5]); _vD.scale.setScalar(ps[6]); _vD.updateMatrix(); return _vD.matrix; };
function vfxUpdate(W, f) {
  let nP = 0, nG = 0, nC = 0, nL = 0, nR = 0, lightI = 0; const lp = [0, 0, 0];
  const puff = (x, y, z, s, col, sy = 1) => { if (nP >= VFXN || s <= 0.01) return; _vS.set(s, s * sy, s); _vP.set(x, y, z); _vQ.identity(); _vM.compose(_vP, _vQ, _vS); vfxPuff.setMatrixAt(nP, _vM); vfxPuff.setColorAt(nP, _vC.set(col)); nP++; };
  const glow = (x, y, z, s, col) => { if (nG >= VFXN || s <= 0.01) return; _vS.set(s, s, s); _vP.set(x, y, z); _vQ.identity(); _vM.compose(_vP, _vQ, _vS); vfxGlow.setMatrixAt(nG, _vM); vfxGlow.setColorAt(nG, _vC.set(col)); nG++; };
  for (const e of (W.vfx || [])) { const pts = vfxPts(e), pot = e.pot || 1, on = f >= e.a && f <= e.b, K = e.k;
    if (K === 'jato' || K === 'pneu' || K === 'poeira' || K === 'fogo' || K === 'faisca' || K === 'vapor') {
      for (let j = 0; j < e.L; j++) { const ps = e.trail[j]; if (!ps) continue; const g = f - j, u = j / e.L, m = vfxPose(ps).clone(), sc = ps[6];
        pts.forEach((pt, pi) => { const reps = K === 'faisca' ? 3 : (K === 'jato' || K === 'pneu') ? 2 : 1; for (let r = 0; r < reps; r++) { const sd = g * 7.13 + pi * 31.7 + r * 3.3, h1 = _vh(sd), h2 = _vh(sd + 1.7), h3 = _vh(sd + 5.1);
          _vP.set(pt[0], pt[1], pt[2]).applyMatrix4(m); let x = _vP.x, y = _vP.y, z = _vP.z; const t = j / 30;
          if (K === 'jato') { _vDir.set(0, -1, 0).transformDirection(m); const v = 11 * pot, tr = v * t * (1 - 0.45 * u), jx = (h1 - 0.5) * 0.9 * u * 2.2, jz = (h2 - 0.5) * 0.9 * u * 2.2; x += _vDir.x * tr + jx; y += _vDir.y * tr; z += _vDir.z * tr + jz;
            const gy = DECK + 0.18; if (y < gy) { const ex = gy - y, a = h3 * 6.2832; x += Math.cos(a) * ex * 0.9; z += Math.sin(a) * ex * 0.9 * 0.6; y = gy + 0.12 * ex * h1; }   /* bate no chao e se espalha em anel (downwash) */
            puff(x, y, z, (0.16 + 0.62 * u) * pot * sc * 0.55 * (u > 0.7 ? (1 - u) / 0.3 : 1), u < 0.25 ? '#ffffff' : u < 0.6 ? '#e6eef5' : '#cdd8e2'); if (j < 3 && r === 0) glow(x, y, z, 0.3 * pot * sc * 0.55, e.col || '#9fdcff'); }
          else if (K === 'pneu') { x += (h1 - 0.5) * 1.6 * u; z += (h2 - 0.5) * 1.6 * u; y = DECK + 0.2 + 1.5 * u * (0.5 + h3); puff(x, y, z, (0.13 + 0.42 * u) * pot * (u > 0.65 ? (1 - u) / 0.35 : 1), u < 0.4 ? '#f2f2ee' : '#d4d4d0'); }
          else if (K === 'poeira') { x += (h1 - 0.5) * 2.4 * u; z += (h2 - 0.5) * 1.2 * u; y = DECK + 0.15 + 0.9 * u * h3; puff(x, y, z, (0.18 + 0.6 * u) * pot * (u > 0.6 ? (1 - u) / 0.4 : 1), e.col || '#d8c39a', 0.7); }
          else if (K === 'vapor') { x += (h1 - 0.5) * 0.8 * u; z += (h2 - 0.5) * 0.8 * u; y += 2.2 * u * (0.6 + 0.4 * h3); puff(x, y, z, (0.12 + 0.4 * u) * pot * (1 - u), '#f4f6f8'); }
          else if (K === 'fogo') { x += (h1 - 0.5) * 0.7 * (0.3 + u); z += (h2 - 0.5) * 0.7 * (0.3 + u); y += 2.6 * u * (0.6 + 0.5 * h3) * pot; if (u < 0.6) glow(x, y, z, (0.34 - 0.3 * u) * pot * (0.7 + 0.5 * h3), u < 0.2 ? '#fff2a8' : u < 0.4 ? '#ffb02e' : '#f0531c'); else puff(x, y, z, (0.2 + 0.4 * (u - 0.6)) * pot * (1 - u) / 0.4, '#4a4744'); }
          else if (K === 'faisca') { const a = h1 * 6.2832, v = 3 + 5 * h2; x += Math.cos(a) * v * t; z += Math.sin(a) * v * t * 0.6; y += (2 + 4 * h3) * t - 9.8 * t * t; if (y > DECK) glow(x, y, z, 0.06 * pot * (1 - u), r % 2 ? (e.col || '#ffe98a') : '#ffffff'); } } }); }
      if (K === 'jato' && on) { const m = vfxPose(e.now).clone(), sc = e.now[6]; _vDir.set(0, -1, 0).transformDirection(m); pts.forEach((pt, pi) => { if (nC >= 64) return; const fl = 0.8 + 0.4 * _vh(f * 3.7 + pi), len = 1.5 * pot * sc * fl; _vP.set(pt[0], pt[1], pt[2]).applyMatrix4(m); lp[0] += _vP.x; lp[1] += _vP.y; lp[2] += _vP.z; _vP.addScaledVector(_vDir, len / 2); _vQ.setFromUnitVectors(_vUp, _vDir.clone().negate()); _vS.set(0.26 * pot * sc, len, 0.26 * pot * sc); _vM.compose(_vP, _vQ, _vS); vfxCone.setMatrixAt(nC, _vM); vfxCone.setColorAt(nC, _vC.set(e.col || '#bfe9ff')); nC++; }); lightI = Math.max(lightI, 6 * pot); lp[0] /= pts.length; lp[1] /= pts.length; lp[2] /= pts.length; lp[1] -= 0.6; }
      if (K === 'fogo' && on) { lightI = Math.max(lightI, 5 * pot); const m = vfxPose(e.now); _vP.set(pts[0][0], pts[0][1], pts[0][2]).applyMatrix4(m); lp[0] = _vP.x; lp[1] = _vP.y + 1; lp[2] = _vP.z; vfxLight.color.set('#ffb060'); } else if (K === 'jato') vfxLight.color.set('#bfe6ff');
    } else if (K === 'velocidade' && on) { const dx = e.now[0] - e.prev[0], dy = 0, dz = e.now[2] - e.prev[2], sp = Math.hypot(dx, dz);   /* riscos de velocidade sempre na horizontal, colados atras do objeto */ if (sp > 0.05) { const b = vfxBox(e.asset), sc = e.now[6], R = Math.max(b.max.x - b.min.x, b.max.z - b.min.z) * sc * 0.5; _vDir.set(dx / sp, dy / sp, dz / sp);
        for (let i = 0; i < 14 && nL < 160; i++) { const h1 = _vh(i * 9.1 + Math.floor(f / 2) * 3.3), h2 = _vh(i * 5.7 + 2), h3 = _vh(i * 3.3 + Math.floor(f / 2)); const len = (1.2 + 2.6 * h1) * Math.min(1.6, sp * 1.5) * pot; _vP.set(e.now[0], e.now[1] + (b.max.y - b.min.y) * sc * (0.15 + 0.8 * h2), e.now[2] + (h3 - 0.5) * 1.6).addScaledVector(_vDir, -(R + 0.15 + len / 2 + h3 * 0.8)); _vQ.setFromUnitVectors(new THREE.Vector3(1, 0, 0), _vDir); _vS.set(len, 0.035, 0.035); _vM.compose(_vP, _vQ, _vS); vfxLine.setMatrixAt(nL++, _vM); } } }
    else if (K === 'onda') { const n = e.n || 3, T = e.dur || 26; for (let i = 0; i < n && nR < 24; i++) { const u = (f - e.a - i * (e.cada || 9)) / T; if (u < 0 || u > 1) continue; const R = (0.6 + (e.raio || 6) * u) * pot; _vP.set(e.now[0], DECK + 0.12, e.now[2]); _vQ.setFromAxisAngle(new THREE.Vector3(1, 0, 0), Math.PI / 2); _vS.set(R, R, 1 + 2 * (1 - u)); _vM.compose(_vP, _vQ, _vS); vfxRing.setMatrixAt(nR++, _vM); } }
    else if (K === 'brilho' && on) { const b = vfxBox(e.asset), sc = e.now[6], m = vfxPose(e.now); _vP.set((b.min.x + b.max.x) / 2, (b.min.y + b.max.y) / 2, (b.min.z + b.max.z) / 2).applyMatrix4(m); const pu = 0.85 + 0.15 * Math.sin(f * 0.5); glow(_vP.x, _vP.y, _vP.z, Math.max(b.max.x - b.min.x, b.max.y - b.min.y, b.max.z - b.min.z) * sc * 0.62 * pu * pot, e.col || '#7fd4ff'); lightI = Math.max(lightI, 3 * pot); lp[0] = _vP.x; lp[1] = _vP.y; lp[2] = _vP.z; vfxLight.color.set(e.col || '#7fd4ff'); } }
  vfxPuff.count = nP; vfxGlow.count = nG; vfxCone.count = nC; vfxLine.count = nL; vfxRing.count = nR;
  for (const im of [vfxPuff, vfxGlow, vfxCone, vfxLine, vfxRing]) { im.visible = im.count > 0; im.instanceMatrix.needsUpdate = true; if (im.instanceColor) im.instanceColor.needsUpdate = true; }
  vfxLight.intensity = lightI; if (lightI > 0) vfxLight.position.set(lp[0], lp[1], lp[2]);
}
UPD.push((W, f) => vfxUpdate(W, f));
// ---------- cards ----------
const CW = 1200, CH = 2000, CM = 2.25; // canvas px, card height in metres (design 600x1000 -> 2.25 m)
const cardGeo = new THREE.PlaneGeometry(CM * 0.6, CM); cardGeo.translate(0, CM / 2 - CM * 0.025, 0);
const blobTex = P.tex(P.radial('20,14,30', 0.6));
const cardWind = { t: { value: 0 }, a: { value: 0.05 } }; const cardLight = { side: { value: 0 }, head: { value: 0.10 }, body: { value: 0.16 } };
class Card {
  constructor(scale = 1, idx = 0) { this.idx = idx;   // semente do vento pelo INDICE da carta (antes Math.random: cada navegador sorteava outra e os personagens/textos tremiam entre quadros)
    [this.c, this.g] = (() => { const c = document.createElement('canvas'); c.width = CW; c.height = CH; return [c, c.getContext('2d')]; })(); this.cw = CW; this.ch = CH;
    this.t = new THREE.CanvasTexture(this.c); this.t.colorSpace = THREE.SRGBColorSpace; this.t.anisotropy = 4;
    this.mat = new THREE.MeshBasicMaterial({ map: this.t, transparent: true, alphaTest: 0.02, side: THREE.DoubleSide, fog: true });
    this.uFlip = { value: 1 }; this.mat.onBeforeCompile = (sh) => { sh.uniforms.wT = cardWind.t; sh.uniforms.wA = cardWind.a; sh.uniforms.wS = this.seed = { value: (this.idx * 2.399963) % 6.2832 }; sh.uniforms.cSide = cardLight.side; sh.uniforms.cHead = cardLight.head; sh.uniforms.cBody = cardLight.body; sh.uniforms.cFlip = this.uFlip;
      sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nuniform float cSide, cHead, cBody, cFlip;').replace('#include <aomap_fragment>', `#include <aomap_fragment>
      #ifdef USE_MAP
      { float hd = smoothstep(.565, .6, vMapUv.y); float hw = mix(.15, .2, hd); float uu = clamp((vMapUv.x - .5) / hw, -1., 1.) * cFlip; float tt = uu * cSide; float dk = smoothstep(-.15, .9, -tt); float g = mix(cBody, cHead, hd);
        reflectedLight.indirectDiffuse *= (1. - g * dk) * mix(vec3(1.), vec3(.9, .87, 1.), dk * .55); }
      #endif`);
      sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nuniform float wT, wA, wS;').replace('#include <begin_vertex>', `#include <begin_vertex>
      float hh_ = clamp((position.y + .056) / 2.25, 0., 1.); float top_ = hh_ * hh_; float hem_ = smoothstep(.55, .0, hh_) * smoothstep(0., .12, hh_);
      transformed.x += wA * (top_ * (.55 * sin(wT * 1.9 + wS) + .35 * sin(wT * 4.3 + wS * 2.)) + hem_ * .5 * sin(wT * 7. + hh_ * 11. + wS));
      transformed.y -= wA * top_ * .15 * (1. + sin(wT * 2.3 + wS));`); };
    this.mesh = new THREE.Mesh(cardGeo, this.mat); this.mesh.userData.card = true; this.mesh.userData.nd = cardNd(this.t); this.mesh.castShadow = true;
    this.mesh.customDepthMaterial = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking, map: this.t, alphaTest: 0.5 });
    this.blob = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: blobTex, transparent: true, depthWrite: false, fog: true }));
    this.blob.rotation.x = -Math.PI / 2; this.blob.userData.ndSkip = true; this.blob.renderOrder = 1;
    scene.add(this.mesh); scene.add(this.blob); this.key = ''; this.mesh.visible = this.blob.visible = false;
  }
  draw(key, fn, th = CH, crop = 0) {   // crop = fracao do alto da carta que fica visivel (0 = tudo): motorista dentro do carro mostra so' cabeca e ombros
    // th = altura (px) do canvas desta carta. Escolhida pelo tamanho do ator na tela (ver cardTier): multidao distante nao precisa de 1200x2000.
    if (key === this.key && th === this.ch && crop === this.crop) return; this.key = key; this.crop = crop;
    if (th !== this.ch) { this.ch = th; this.cw = Math.round(th * CW / CH); this.c.width = this.cw; this.c.height = this.ch; this.t.dispose(); }
    const g = this.g; g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, this.cw, this.ch); g.setTransform(this.cw / 600, 0, 0, this.ch / 1000, 0, 0);
    if (crop) { g.save(); g.beginPath(); g.rect(0, 0, 600, 1000 * crop); g.clip(); }
    const p = new T.Pen(g); fn(p); if (crop) g.restore(); this.t.needsUpdate = true;
    this.bbox = window.INSPECT ? contentBox(this.c) : null;
  }
}
const _cb = document.createElement('canvas'); _cb.width = 120; _cb.height = 200; const _cbg = _cb.getContext('2d', { willReadFrequently: true });
function contentBox(src) { _cbg.clearRect(0, 0, 120, 200); _cbg.drawImage(src, 0, 0, 120, 200); const d = _cbg.getImageData(0, 0, 120, 200).data; let x0 = 120, x1 = 0, y0 = 200, y1 = 0;
  for (let y = 0; y < 200; y++) for (let x = 0; x < 120; x++) if (d[(y * 120 + x) * 4 + 3] > 40) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
  return x1 < x0 ? null : { x0: x0 / 120, x1: (x1 + 1) / 120, y0: y0 / 200, y1: (y1 + 1) / 200 }; }
const cards = []; const getCard = (i) => cards[i] || (cards[i] = new Card(1, i));

// ---------- render targets & post ----------
const rtColor = new THREE.WebGLRenderTarget(W, H, { samples: (window.MSAA ?? 0), type: THREE.HalfFloatType });
const rtNd = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, minFilter: THREE.NearestFilter, magFilter: THREE.NearestFilter });
const rtInk = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType });
const fsCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1), fsGeo = new THREE.PlaneGeometry(2, 2);
const fs = (mat) => { const s = new THREE.Scene(); s.add(new THREE.Mesh(fsGeo, mat)); return s; };
const inkU = { col: { value: rtColor.texture }, nd: { value: rtNd.texture }, res: { value: new THREE.Vector2(W, H) }, focus: { value: 5 }, cinf: { value: 0 }, near: { value: 1 }, px: { value: 1.6 }, fogCol: { value: new THREE.Color() },
  sat: { value: 0.98 }, lift: { value: new THREE.Color(0, 0, 0) }, gain: { value: new THREE.Color(1, 1, 1) }, vig: { value: 0.22 }, flash: { value: 0 }, expo: { value: 1 }, zbl: { value: 0 }, gamt: { value: 1 }, gky: { value: [0.0345, 0.1828, 0.3812, 0.6605, 0.8814, 0.9631, 1] }, gkm: { value: [1.483, 1.404, 1.22, 0.987, 0.661, 0.435, 0.369] }, gsat: { value: new THREE.Vector3(0.92, 1.02, 1.06) }, gtS: { value: new THREE.Vector3(0.0647, -0.0137, -0.0541) }, gtM: { value: new THREE.Vector3(-0.0165, -0.0024, 0.0698) }, gtH: { value: new THREE.Vector3(-0.0075, -0.0004, 0.0267) }, gvig: { value: new THREE.Vector2(0.14, 0.42) } };
const inkScene = fs(new THREE.ShaderMaterial({ uniforms: inkU, vertexShader: `varying vec2 vUv; void main(){ vUv=uv; gl_Position=vec4(position.xy,0.,1.); }`,
  fragmentShader: `uniform sampler2D col, nd; uniform vec2 res; uniform float focus, cinf, near; uniform float px, sat, vig, flash, expo, zbl, gamt; uniform float gky[7], gkm[7]; uniform vec3 gsat, gtS, gtM, gtH; uniform vec2 gvig; uniform vec3 fogCol, lift, gain; varying vec2 vUv;

  vec3 srgb2lin(vec3 c){ return mix(c/12.92, pow((c+.055)/1.055, vec3(2.4)), step(.04045, c)); }
  vec3 lin2srgb(vec3 c){ return mix(c*12.92, 1.055*pow(max(c,0.), vec3(1./2.4))-.055, step(.0031308, c)); }
  vec3 rgb2lab(vec3 c){ vec3 l = srgb2lin(c); vec3 xyz = mat3(.4124,.2126,.0193, .3576,.7152,.1192, .1805,.0722,.9505) * l / vec3(.95047,1.,1.08883);
    vec3 f = mix(7.787*xyz + 16./116., pow(max(xyz,1e-5), vec3(1./3.)), step(.008856, xyz)); return vec3(116.*f.y-16., 500.*(f.x-f.y), 200.*(f.y-f.z)); }
  vec3 lab2rgb(vec3 L){ float fy = (L.x+16.)/116., fx = fy + L.y/500., fz = fy - L.z/200.; vec3 f = vec3(fx,fy,fz); vec3 t3 = f*f*f; vec3 xyz = mix((f-16./116.)/7.787, t3, step(.008856, t3)) * vec3(.95047,1.,1.08883);
    vec3 l = mat3(3.2406,-.9689,.0557, -1.5372,1.8758,-.2040, -.4986,.0415,1.0570) * xyz; return clamp(lin2srgb(l), 0., 1.); }
  // Reference-fitted display grade (tone curve through 7 knots, saturation by zone, 3-way tint, vignette) -- numbers measured on 20 reference shorts
  const float gx[7] = float[7](0., .1, .25, .5, .75, .9, 1.);
  float gradeCurve(float x){ x = clamp(x, 0., 1.); int i = 0; if (x > gx[1]) i = 1; if (x > gx[2]) i = 2; if (x > gx[3]) i = 3; if (x > gx[4]) i = 4; if (x > gx[5]) i = 5;
    float x0 = gx[i], h = gx[i+1] - x0, t = (x - x0) / h, t2 = t*t, t3 = t2*t;
    return (2.*t3 - 3.*t2 + 1.) * gky[i] + (t3 - 2.*t2 + t) * h * gkm[i] + (-2.*t3 + 3.*t2) * gky[i+1] + (t3 - t2) * h * gkm[i+1]; }
  vec3 gradeRC(vec3 src, vec2 uv){
    vec3 c = vec3(gradeCurve(src.r), gradeCurve(src.g), gradeCurve(src.b));
    float y = dot(c, vec3(.2126, .7152, .0722)); float wS = 1. - smoothstep(0., .55, y), wH = smoothstep(.45, 1., y), wM = 1. - wS - wH;
    float s = gsat.y + (gsat.x - gsat.y) * wS + (gsat.z - gsat.y) * wH; c = vec3(y) + s * (c - vec3(y));
    c += wS * gtS + wM * gtM + wH * gtH;
    float r = length(uv * 2. - 1.) * .70710678; c *= 1. - gvig.x * smoothstep(gvig.y, 1., r);
    return mix(src, clamp(c, 0., 1.), gamt); }
  float edgeAt(vec2 uv, float r){
    vec4 c = texture2D(nd, uv); if (dot(c.rgb,c.rgb) < .01) return 0.; float d = c.a; vec3 n = c.rgb*2.-1.;
    float e = 0.; float rr = r * clamp(7./d, .62, 1.25); float i0 = 1./d;
    for (int i=0;i<16;i++){ float a = float(i)*.785398 + (i>7 ? .39 : 0.); float k = i>7 ? .5 : 1.;
      vec2 o = vec2(cos(a), sin(a))*rr*k/res; vec4 s = texture2D(nd, uv+o);
      float ds = s.a; bool card = dot(s.rgb,s.rgb) < .01;
      if (card && ds > 0.) continue;            // character cards: never outlined by the world ink
      if (card) ds = 1e4;                        // sky
      vec3 ns = s.rgb*2.-1.;
      // depth jump, near side only -- measured against the local PLANE: on a flat surface 1/depth is affine on screen, so the opposite tap
      // predicts this one (2/d - 1/d2).  A plain depth ratio inked ground seen at a grazing angle as a huge black band at the horizon.
      float ip = i0; vec4 s2 = texture2D(nd, uv-o); if (dot(s2.rgb,s2.rgb) >= .01) ip = max(2.*i0 - 1./s2.a, 0.);
      e = max(e, smoothstep(.006, .02, (ip - 1./ds)/i0));
      if (!card && abs(ds-d)/d < .06) e = max(e, smoothstep(.93, .80, dot(n, ns)) * .9); // crease
    }
    return e * (1. - smoothstep(150., 450., d)*.3);
  }
  void main(){
    vec3 c = texture2D(col, vUv).rgb;
    if (zbl > .01) { vec3 acc = c; vec2 dir = (vec2(.5) - vUv); for (int i = 1; i < 9; i++) { acc += texture2D(col, vUv + dir * (float(i) / 8.) * zbl * .22).rgb; } c = acc / 9.; }
    { vec3 bl = vec3(0.); for (int i=0;i<12;i++){ float a_ = float(i)*.5236; vec2 o = vec2(cos(a_),sin(a_)) * (i<6 ? 14. : 34.) / res; vec3 s_ = texture2D(col, vUv+o).rgb; bl += max(s_ - .82, 0.); } c += bl * .09 * vec3(1.,.92,.78); }
    float e = edgeAt(vUv, px) * (1. - .75*zbl);
    c = mix(c, vec3(.012,.01,.014), e);
    if (flash < -0.5) c = vec3(e);
    c = c*gain + lift; c *= expo; c = clamp(c, 0., 1.); { vec3 d_ = gradeRC(lin2srgb(c), vUv); d_ = mix(d_, d_*d_*(3.-2.*d_), .24); c = srgb2lin(d_); }   // contraste medido no canal: mais preto profundo (4% dos pixels), mesma media
    c = mix(c, vec3(1.), flash);
    float dd = texture2D(nd, vUv).a; if (dd <= 0.) dd = 2000.; float kk = 1. - focus/dd; float coc_ = kk > 0. ? cinf*kk : min(-kk*cinf*near, cinf*1.4);
    gl_FragColor = vec4(c, coc_); }` }));
const dofU = { src: { value: rtInk.texture }, nd: { value: rtNd.texture }, res: { value: new THREE.Vector2(W, H) }, focus: { value: 5 }, cinf: { value: 0 }, near: { value: 1 } };
const dofScene = fs(new THREE.ShaderMaterial({ uniforms: dofU, vertexShader: `varying vec2 vUv; void main(){ vUv=uv; gl_Position=vec4(position.xy,0.,1.); }`,
  fragmentShader: `uniform sampler2D src, nd; uniform vec2 res; uniform float focus, cinf, near; varying vec2 vUv;
  // O CoC vem pronto no alfa de src (calculado no passe de tinta): 1 leitura por amostra em vez de 2. Numero de amostras proporcional a area do disco (min 8, max 48).
  void main(){
    vec4 s0 = texture2D(src, vUv); float c0 = s0.a;
    if (cinf < .5 || c0 < .6) { gl_FragColor = linearToOutputTexel(vec4(s0.rgb, 1.)); return; }
    int n = int(clamp(c0*c0*.9, 10., 48.));
    vec3 acc = vec3(0.); float wsum = 0.;
    for (int i=0;i<48;i++){ if (i >= n) break; float fi = float(i); float r = sqrt((fi+.5)/float(n)); float a = fi*2.39996;
      vec2 o = vec2(cos(a), sin(a))*r*c0/res; vec4 t = texture2D(src, vUv+o);
      float w = smoothstep(r*c0-1.5, r*c0+.5, t.a + .5);
      acc += t.rgb*w; wsum += w; }
    gl_FragColor = linearToOutputTexel(vec4(acc/max(wsum,1e-3), 1.)); }` }));
// final copy with sRGB handled by the renderer output (we render to screen with linear->sRGB in the shader chunk)
dofScene.children[0].material.toneMapped = false;

// ---------- per-frame state ----------
const tmpV = new THREE.Vector3();
function applyLight(L, f) {
  hemi.color.set(L.sky); hemi.groundColor.set(L.ground); hemi.intensity = L.hemi;
  sun.color.set(L.sun); sun.intensity = L.sunI;
  scene.fog.color.set(L.fog); scene.fog.near = L.fogNear; scene.fog.far = L.fogFar;
  skyU.top.value.set(L.skyTop); skyU.hor.value.set(L.skyHor); skyU.sunCol.value.set(L.sunDisc || '#000'); skyU.sunSize.value = L.sunSize || 0; skyU.stars.value = L.stars || 0;
  inkU.sat.value = L.sat; inkU.gain.value.set(L.gain || '#ffffff'); inkU.lift.value.set(L.lift || '#000000');
}
function placeSun(L, focus) {
  // sun direction from azimuth/elevation in world space
  const az = rx(L.az), el = rx(L.el); tmpV.set(Math.cos(el) * Math.cos(az), Math.sin(el), Math.cos(el) * Math.sin(az));
  skyU.sunDir.value.copy(tmpV);
  sun.position.copy(focus).addScaledVector(tmpV, 80); sun.target.position.copy(focus);
  const ext = L.shadowExt || 30, sc = sun.shadow.camera; sc.left = -ext; sc.right = ext; sc.top = ext; sc.bottom = -ext; sc.near = 1; sc.far = 200; sc.updateProjectionMatrix();
}

// ---- resolucao adaptativa das cartas (otimizacao de render): altura do canvas = altura do ator na tela (+folga), em degraus de ~1.25x.
// Deterministico (depende so' do quadro, nunca do estado anterior) => shards/retomadas geram exatamente a mesma imagem. CARD_FULL=1 desliga.
const CARD_TIERS = [256, 320, 400, 500, 640, 800, 1000, 1280, 1600, 2000];
function cardTier(a, cam) {
  if (window.CARD_FULL) return CH;
  const s = a.s || 1, dx = a.x - cam.position.x, dy = a.y + 1.1 * s - cam.position.y, dz = a.z - cam.position.z;
  const d = Math.max(0.4, Math.hypot(dx, dy, dz)), px = (CM * s) / (2 * d * Math.tan(rx(cam.fov) / 2)) * H;
  const need = Math.min(CH, px * (window.CARD_HEADROOM || 1.2)); for (const t of CARD_TIERS) if (t >= need) return t; return CH;
}
function drawActors(list, cam) {
  cards.forEach((c) => { c.mesh.visible = c.blob.visible = false; });
  list.forEach((a, i) => {
    const c = getCard(i);
    c.draw(a.key, a.draw, cardTier(a, cam), a.crop || 0);
    c.mesh.visible = true; c.mesh.position.set(a.x, a.y, a.z);
    const s = a.s || 1; c.mesh.scale.set(s * (a.flip ? -1 : 1), s, s); c.uFlip.value = a.flip ? -1 : 1;
    c.mesh.rotation.set(0, Math.atan2(cam.position.x - a.x, cam.position.z - a.z) + (a.yaw || 0), a.roll || 0);
    if (a.keepColor) { const gn = inkU.gain.value; c.mat.color.setRGB(Math.min(1.5, 1.06 / Math.max(0.5, gn.r)), Math.min(1.5, 1.03 / Math.max(0.5, gn.g)), Math.min(1.5, 1.3 / Math.max(0.5, gn.b))); if (c.mat.fog) { c.mat.fog = false; c.mat.needsUpdate = true; } } else { if (a.tint) c.mat.color.set(a.tint); else { const gn = inkU.gain.value, k = 0.55, f_ = (v) => 1 + k * (Math.min(1.4, 1 / Math.max(0.6, v)) - 1); c.mat.color.setRGB(f_(gn.r), f_(gn.g), f_(gn.b)); }   /* compensa 55% da cor da luz: rosto continua branco (canal), sem virar laranja no por do sol */ if (!c.mat.fog) { c.mat.fog = true; c.mat.needsUpdate = true; } }
    if (c.mat.depthTest === !!a.front) { c.mat.depthTest = !a.front; c.mat.depthWrite = !a.front; c.mat.needsUpdate = true; }
    c.mat.opacity = a.alpha ?? 1;
    c.mesh.castShadow = a.shadow !== false;
    c.mesh.renderOrder = a.order || 2;
    if (a.blob !== false && !a.crop && a.y < DECK + 0.5) { c.blob.visible = true; c.blob.position.set(a.x, (a.ground ?? DECK) + 0.02, a.z); c.blob.scale.set(0.95 * s, 0.6 * s, 1); }
  });
}

const swapForNd = (on) => {
  scene.traverse((o) => {
    if (o.isPoints) { if (on) { o.userData.vis0 = o.visible; o.visible = false; } else if (o.userData.vis0 !== undefined) { o.visible = o.userData.vis0; delete o.userData.vis0; } return; }
    if (!o.isMesh) return;
    if (on) {
      o.userData.mat0 = o.material;
      if (o.userData.ndSkip) { o.userData.vis0 = o.visible; o.visible = false; return; }
      if (o === sky || o.userData.sky) { o.userData.vis0 = o.visible; o.visible = false; return; }
      o.material = o.userData.nd || ndMat;
    } else {
      o.material = o.userData.mat0; if (o.userData.vis0 !== undefined) { o.visible = o.userData.vis0; delete o.userData.vis0; }
    }
  });
};

window.inspectFrame = (f) => {
  window.INSPECT = true;
  const S = shotAt(f), C = window.TESTCAM ? { flash: 0, ...window.TESTCAM } : camAt(f), W_ = worldAt(f);
  setWeather(W_); worldState(W_, f); sceneryUpdate(W_, f);
  camera.position.set(...C.pos); camera.up.set(0, 1, 0); camera.lookAt(...C.look); camera.rotateZ(rx(C.roll || 0)); camera.fov = C.fov; camera.updateProjectionMatrix(); scene.updateMatrixWorld(true); camera.updateMatrixWorld(true);
  const acts = actorsAt(f, T), out = { f, shot: S.id, cam: { pos: C.pos, look: C.look, fov: C.fov }, actors: [] };
  const occl = []; scene.traverse((o) => { if (o.isMesh && o.visible && !o.userData.ndSkip && !o.userData.card && !o.userData.sky && !o.isInstancedMesh && o !== sky && o.material !== undefined) { let v = true, p = o; while (p) { if (!p.visible) v = false; p = p.parent; } if (v && !o.userData.nd) occl.push(o); } });
  const ray = new THREE.Raycaster(), cp = camera.position.clone();
  // camera inside geometry: short rays in 6 directions
  let inside = null; for (const d of [[0, 0, -1], [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]]) { const dir = new THREE.Vector3(...d).applyQuaternion(camera.quaternion); ray.set(cp, dir); ray.far = 0.35; const h = ray.intersectObjects(occl, false); if (h.length) { inside = (h[0].object.name || h[0].object.geometry.type) + '@' + h[0].distance.toFixed(2); break; } }
  if (!inside && C.pos[1] < DECK + 0.3) inside = 'below-ground@' + (C.pos[1] - DECK).toFixed(2);
  if (!inside) { // camera INSIDE a closed solid (house, truck, tank...): prefilter by the mesh's local bounding box, then confirm with double-sided rays (first hit is a back face from >=4 of 6 directions)
    const lp = new THREE.Vector3(), dirs = [[0, 0, -1], [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1]], ws = new THREE.Vector3(), sz = new THREE.Vector3();
    for (const o of occl) { const m = o.material; if (!m || m.side !== THREE.FrontSide || !o.geometry) continue; const g = o.geometry; if (!g.boundingBox) g.computeBoundingBox(); const bb = g.boundingBox; lp.copy(cp); o.worldToLocal(lp);
      if (!(lp.x > bb.min.x && lp.x < bb.max.x && lp.y > bb.min.y && lp.y < bb.max.y && lp.z > bb.min.z && lp.z < bb.max.z)) continue;
      o.getWorldScale(ws); bb.getSize(sz); if (Math.min(sz.x * Math.abs(ws.x), sz.y * Math.abs(ws.y), sz.z * Math.abs(ws.z)) < 0.7) continue;
      m.side = THREE.DoubleSide; let back = 0; for (const d of dirs) { ray.set(cp, new THREE.Vector3(...d)); ray.far = 80; const hs = ray.intersectObject(o, false); if (hs.length && hs[0].face && hs[0].face.normal.clone().transformDirection(o.matrixWorld).dot(ray.ray.direction) > 0) back++; } m.side = THREE.FrontSide;
      if (back >= 4) { inside = 'inside solid ' + (o.name || o.geometry.type); break; } } }
  out.cameraInside = inside;
  acts.forEach((a, i) => {
    const c = getCard(i); c.draw(a.key, a.draw); const bb = c.bbox; if (!bb) return;
    const s = a.s || 1, top = a.y + 2.194 * s, hgt = 2.25 * s;
    const right = new THREE.Vector3(cp.z - a.z, 0, -(cp.x - a.x)).normalize().multiplyScalar(0.675 * s * (a.flip ? -1 : 1));
    const P = (fx, fy) => new THREE.Vector3(a.x + right.x * (2 * fx - 1), top - fy * hgt, a.z + right.z * (2 * fx - 1)).project(camera);
    const pts = [P(bb.x0, bb.y0), P(bb.x1, bb.y0), P(bb.x0, bb.y1), P(bb.x1, bb.y1)];
    const xs = pts.map((p) => (p.x + 1) / 2), ys = pts.map((p) => (1 - p.y) / 2), behind = pts.some((p) => p.z > 1 || p.z < -1);
    const bx0 = Math.min(...xs), bx1 = Math.max(...xs), by0 = Math.min(...ys), by1 = Math.max(...ys);
    const ix = Math.max(0, Math.min(1, bx1) - Math.max(0, bx0)), iy = Math.max(0, Math.min(1, by1) - Math.max(0, by0)), area = (bx1 - bx0) * (by1 - by0), vis = area > 0 ? (ix * iy) / area : 0;
    // occlusion: rays to head / chest / feet of the drawn content
    const hits = []; for (const fy of [bb.y0 + 0.12 * (bb.y1 - bb.y0), bb.y0 + 0.38 * (bb.y1 - bb.y0)]) { const tgt = new THREE.Vector3(a.x, top - fy * hgt, a.z); const dir = tgt.clone().sub(cp); const dist = dir.length(); ray.set(cp, dir.normalize()); ray.far = dist - 0.3; const h = ray.intersectObjects(occl, false); hits.push(h.length ? { by: (h[0].object.name || h[0].object.geometry.type) + '/' + (h[0].object.material.color ? '#' + h[0].object.material.color.getHexString() : '?'), d: +h[0].distance.toFixed(2) } : null); }
    out.actors.push({ i, id: a.id || (a.key || '').slice(0, 8), x: +a.x.toFixed(2), z: +a.z.toFixed(2), dist: +cp.distanceTo(new THREE.Vector3(a.x, a.y, a.z)).toFixed(2), box: [+bx0.toFixed(3), +by0.toFixed(3), +bx1.toFixed(3), +by1.toFixed(3)], visible: +vis.toFixed(3), heightFrac: +(by1 - by0).toFixed(3), behind, occluded: hits.filter(Boolean).length, occluder: (hits.find(Boolean) || {}).by || null });
  });
  /* PLACAS (texto em placa de madeira): entram no inspetor como 'placa' para o enquadramento garantir a placa INTEIRA no quadro */
  for (const e of fxAt(f, T)) { if (!e || typeof e.key !== 'string' || !e.key.startsWith('txb')) continue; const s = e.s || 1, top = e.y + 2.194 * s, hgt = 2.25 * s;
    const right = new THREE.Vector3(cp.z - e.z, 0, -(cp.x - e.x)).normalize().multiplyScalar(0.675 * s);
    const P = (fx, fy) => new THREE.Vector3(e.x + right.x * (2 * fx - 1), top - fy * hgt, e.z + right.z * (2 * fx - 1)).project(camera);
    const pts = [P(0.08, 0.2), P(0.92, 0.2), P(0.08, 0.46), P(0.92, 0.46)], xs = pts.map((p) => (p.x + 1) / 2), ys = pts.map((p) => (1 - p.y) / 2), behind = pts.some((p) => p.z > 1 || p.z < -1);
    const bx0 = Math.min(...xs), bx1 = Math.max(...xs), by0 = Math.min(...ys), by1 = Math.max(...ys), ix = Math.max(0, Math.min(1, bx1) - Math.max(0, bx0)), iy = Math.max(0, Math.min(1, by1) - Math.max(0, by0)), area = (bx1 - bx0) * (by1 - by0);
    out.placas = out.placas || []; out.placas.push({ box: [+bx0.toFixed(3), +by0.toFixed(3), +bx1.toFixed(3), +by1.toFixed(3)], visible: +(area > 0 ? (ix * iy) / area : 0).toFixed(3), behind }); }
  // 3D animals (props from the pool): project their world bounding boxes so the take inspector covers them too
  for (const nm of ['bear', 'horse', 'horse_sela', 'emu']) for (const o of (propPool[nm] || [])) { if (!o.visible) continue; const bb3 = new THREE.Box3().setFromObject(o); if (bb3.isEmpty()) continue;
    const cs = []; for (const x of [bb3.min.x, bb3.max.x]) for (const y of [bb3.min.y, bb3.max.y]) for (const z of [bb3.min.z, bb3.max.z]) cs.push(new THREE.Vector3(x, y, z).project(camera));
    const behind = cs.every((p) => p.z > 1 || p.z < -1), xs = cs.map((p) => (p.x + 1) / 2), ys = cs.map((p) => (1 - p.y) / 2), bx0 = Math.min(...xs), bx1 = Math.max(...xs), by0 = Math.min(...ys), by1 = Math.max(...ys);
    const ix = Math.max(0, Math.min(1, bx1) - Math.max(0, bx0)), iy = Math.max(0, Math.min(1, by1) - Math.max(0, by0)), area = (bx1 - bx0) * (by1 - by0), vis = area > 0 ? (ix * iy) / area : 0;
    out.actors.push({ i: 900, id: nm, animal3d: true, x: +o.position.x.toFixed(2), z: +o.position.z.toFixed(2), dist: +cp.distanceTo(o.position).toFixed(2), box: [+bx0.toFixed(3), +by0.toFixed(3), +bx1.toFixed(3), +by1.toFixed(3)], visible: +vis.toFixed(3), heightFrac: +(by1 - by0).toFixed(3), behind, occluded: 0, occluder: '' }); }
  return out;
};
const renderCore = (f) => {
  const S = shotAt(f), L = lightFor(S, f), C = window.TESTCAM ? { flash: 0, ...window.TESTCAM } : camAt(f);
  const W_ = worldAt(f); setWeather(W_);
  applyLight(L, f);
  sceneryLights(L, f, C, new THREE.Vector3(...C.look), null);
  weatherParticles(f, { x: C.pos[0], y: C.pos[1], z: C.pos[2] });
  camera.position.set(...C.pos); camera.up.set(0, 1, 0); camera.lookAt(...C.look); camera.rotateZ(rx(C.roll || 0));
  camera.fov = C.fov; camera.updateProjectionMatrix(); camera.updateMatrixWorld();
  worldState(W_, f); sceneryUpdate(W_, f);
  placeSun(L, new THREE.Vector3(...(C.shadowAt || C.look)));
  { const sd = sun.position.clone().sub(sun.target.position).normalize().transformDirection(camera.matrixWorldInverse); const ax = Math.abs(sd.x), k = Math.min(1, Math.max(0, ax / 0.35)); cardLight.side.value = Math.sign(sd.x) * k * k * (3 - 2 * k); }
  cardWind.t.value = f / 30; cardWind.a.value = (window.NOWIND ? 0 : 0.035 + 0.11 * WX.wind);
  const ACTS = actorsAt(f, T);
  drawActors([...ACTS, ...fxAt(f, T)], camera);
  sky.position.copy(camera.position);
  clouds.forEach((c) => { c.position.x = camera.position.x + (c.userData.rx ?? 0); c.position.z = camera.position.z + (c.userData.rz ?? -400); c.visible = !L.noClouds; c.material.color.set(L.cloud || '#ffffff'); });   /* nuvem acompanha a luz (escura de noite e na chuva) */
  // pass A: colour
  renderer.setRenderTarget(rtColor); renderer.setClearColor(0x000000, 1); renderer.clear(); renderer.render(scene, camera);
  // pass B: normal + depth
  const fog = scene.fog; scene.fog = null; const sm = renderer.shadowMap.enabled; renderer.shadowMap.enabled = false; renderer.shadowMap.autoUpdate = false;
  swapForNd(true); renderer.setRenderTarget(rtNd); renderer.setClearColor(0x000000, 0); renderer.clear(); renderer.render(scene, camera); swapForNd(false);
  scene.fog = fog; renderer.shadowMap.enabled = sm; renderer.shadowMap.autoUpdate = true;
  if (window.DEBUG_ND) { const dm = new THREE.MeshBasicMaterial({ map: rtNd.texture }); const ds = fs(dm); renderer.setRenderTarget(null); renderer.render(ds, fsCam); return true; }
  // ink + grade
  const D = window.TESTCAM ? { focus: window.TESTCAM.focus || 5, cinf: window.TESTCAM.cinf || 4 } : dofAt(f);
  if (!window.TESTCAM && !(S.dof && S.dof.focus !== undefined)) {   // the lens always focuses on the NEAREST character in the middle of the frame (faces never go soft); only the background / foreground props blur
    const fw = new THREE.Vector3(); camera.getWorldDirection(fw); const cp_ = camera.position; let best = Infinity;
    const cand = [...ACTS.map((a) => [a.x, a.y + 1.1 * (a.s || 1), a.z]), ...(W_.props || []).filter((p) => p.asset === 'bear' || p.asset === 'horse' || p.asset === 'horse_sela' || p.asset === 'emu').map((p) => [p.x, p.y + 1.0, p.z])];
    for (const q of cand) { const v = new THREE.Vector3(q[0] - cp_.x, q[1] - cp_.y, q[2] - cp_.z), dep = v.dot(fw); if (dep < 0.6) continue; const pr = new THREE.Vector3(q[0], q[1], q[2]).project(camera); if (Math.abs(pr.x) > 0.85 || Math.abs(pr.y) > 0.92) continue; if (dep < best) best = dep; }
    if (best < Infinity && best < D.focus * 1.05) D.focus = best; else if (best < Infinity) D.focus = Math.min(D.focus, Math.max(best, D.focus * 0.6));
    D.near = 0.45; }
  { const G = (L.gsel ?? 0), mx = (a, b) => a + (b - a) * G;
    const D = { ky: [0, 0.1, 0.25, 0.5, 0.75, 0.9, 1], km: [1, 1, 1, 1, 1, 1, 1], sat: [1.05, 1.2, 1.15], tS: [-0.012, -0.018, 0.04], tM: [-0.006, -0.01, 0.036], tH: [0, 0, 0], vg: [0.10, 0.45], amt: 1 };
    const Gd = { ky: [0, 0.1, 0.25, 0.5, 0.75, 0.9, 1], km: [1, 1, 1, 1, 1, 1, 1], sat: [0.98, 1.1, 1.2], tS: [-0.01, -0.03, 0.07], tM: [-0.006, -0.02, 0.05], tH: [0, 0, 0], vg: [0.16, 0.40], amt: 1 };
    inkU.gky.value = D.ky.map((v, i) => mx(v, Gd.ky[i])); inkU.gkm.value = D.km.map((v, i) => mx(v, Gd.km[i])); inkU.gsat.value.set(...D.sat.map((v, i) => mx(v, Gd.sat[i]))); inkU.gtS.value.set(...D.tS.map((v, i) => mx(v, Gd.tS[i]))); inkU.gtM.value.set(...D.tM.map((v, i) => mx(v, Gd.tM[i]))); inkU.gtH.value.set(...D.tH.map((v, i) => mx(v, Gd.tH[i]))); inkU.gvig.value.set(mx(D.vg[0], Gd.vg[0]), mx(D.vg[1], Gd.vg[1])); inkU.gamt.value = window.GRADE_OFF ? 0 : (L.gamt ?? mx(D.amt, Gd.amt)); }
  inkU.zbl.value = C.zb || 0; inkU.px.value = 3.6; inkU.expo.value = L.exp ?? 1; inkU.sat.value = Math.max((L.sat ?? 1.14) * 1.08, 1.18); inkU.flash.value = window.DEBUG_E ? -1 : (C.flash || 0); inkU.vig.value = L.vig ?? 0.22;
  D.cinf *= (window.DOF_K ?? 0.6);   /* canal: fundo nitido ou so' levemente desfocado em 96% dos quadros */ inkU.focus.value = D.focus; inkU.cinf.value = D.cinf; inkU.near.value = D.near ?? 1;
  renderer.setRenderTarget(rtInk); renderer.render(inkScene, fsCam);
  // lens
  dofU.focus.value = D.focus; dofU.cinf.value = D.cinf; dofU.near.value = D.near ?? 1;
  renderer.setRenderTarget(null); renderer.render(dofScene, fsCam);
  return true;
};
// ---- transitions: cross-dissolve between shots (outgoing shot is re-rendered past its end and blended) ----
const compA = document.createElement('canvas'), compB = document.createElement('canvas'); compA.width = compB.width = canvas.width; compA.height = compB.height = canvas.height;
const cgA = compA.getContext('2d'), cgB = compB.getContext('2d'); let compOn = false;
window.renderFrame = (f) => {
  compOn = false; const si = SHOTS.findIndex((s) => f >= s.a && f <= s.b), S = SHOTS[si];
  if (S && S.tr && S.tr.type !== 'cut' && S.tr.N > 0 && si > 0 && f < S.a + S.tr.N && !window.NOTRANS && !window.TESTCAM) {
    const k = (f - S.a + 1) / (S.tr.N + 1), t = k * k * (3 - 2 * k);
    window.__force(si - 1); renderCore(f); window.__force(null); cgA.clearRect(0, 0, compA.width, compA.height); cgA.drawImage(canvas, 0, 0);
    renderCore(f); cgB.clearRect(0, 0, compB.width, compB.height); cgB.drawImage(canvas, 0, 0);
    cgA.globalAlpha = t; cgA.drawImage(compB, 0, 0); cgA.globalAlpha = 1; compOn = true; return true;
  }
  return renderCore(f);
};
window.getFrameDataURL = (q = 0.92) => (compOn ? compA : canvas).toDataURL('image/jpeg', q);
window.TOTAL = TOTAL; window.__scene = scene; window.__cam = camera;
window.ready = true;
