// ===== STORY RUNTIME (generic): turns a declarative SPEC (stories/<id>.spec.js, concatenated before this file) into the story.js interface the engine expects =====
import { camFromKeys, clamp, lerp, ramp, q, blinkAt, idle, M } from './motion.js';
export const FPS = 30, TOTAL = SPEC.total, DECK = 6;
export const SPEC_DEBUG = SPEC;
// ---------- auto sub-cuts: long shots are split into ~2.2 s sub-takes, each with a different camera setup (Ricks Clips rhythm: new angle every phrase) ----------
const VARS = [{ az: 0, el: 0, d: 1, fov: 0, roll: 0 }, { az: 16, el: -5, d: 0.94, fov: 2, roll: -2 }, { az: -14, el: 7, d: 1.06, fov: 0, roll: 2.5 }, { az: 8, el: -3, d: 0.92, fov: -2, roll: 0 }, { az: -18, el: 11, d: 1.12, fov: 3, roll: -3 }, { az: 12, el: -6, d: 0.98, fov: 1, roll: 3 }];   /* sub-cortes suaves: ninguem sai do quadro */
const lk = (a, b, t) => ({ ...a, at: [0, 1, 2].map((i) => a.at[i] + (b.at[i] - a.at[i]) * t), d: a.d + (b.d - a.d) * t, az: (a.az ?? 0) + ((b.az ?? 0) - (a.az ?? 0)) * t, el: (a.el ?? 8) + ((b.el ?? 8) - (a.el ?? 8)) * t, fov: (a.fov ?? 34) + ((b.fov ?? 34) - (a.fov ?? 34)) * t });
SPEC.shots.forEach((s, i, A) => { if (i === 0) { s.trIn = null; return; } const ty = s.trans ?? (s.cut === false ? 'cut' : (A[i - 1].light !== s.light ? (SPEC.trans ?? 'dissolve') : 'cut')); s.trIn = { type: ty, N: ty === 'dissolve' ? (SPEC.dissolveN ?? 10) : ty === 'push' ? 4 : 0 }; });
if (SPEC.autocut !== false) SPEC.shots = SPEC.shots.flatMap((s) => { const len = s.b - s.a + 1, n = Math.max(1, Math.round(len / (SPEC.cutLen ?? 66))); if (n < 2 || !s.cam || s.cam.length < 2 || !s.cam[0].at || s.nocut) return [s];
  const out = [], k0 = s.cam[0], k1 = s.cam[s.cam.length - 1]; let a = s.a;
  for (let j = 0; j < n; j++) { const b = j === n - 1 ? s.b : Math.round(s.a + (j + 1) * len / n) - 1, v = VARS[((s.a / 66 | 0) + j + (SPEC.vseed || 0)) % VARS.length]; const t0 = (a - s.a) / Math.max(1, len - 1), t1 = (b - s.a) / Math.max(1, len - 1);
    const par = j % 2 ? -1 : 1; const mk = (t, f, s) => { const k0_ = lk(k0, k1, t); const azr = ((k0_.az ?? 0) + v.az * 0.9) * Math.PI / 180, amt = (s - 0.5) * 0.07 * k0_.d * par, dd = 1 + (s - 0.5) * 0.16 * (j % 2 ? 1 : -1);
      const k = { ...k0_, at: [k0_.at[0] + Math.cos(azr) * amt, k0_.at[1], k0_.at[2] - Math.sin(azr) * amt], d: k0_.d * dd }; return { ...k, f, az: k.az + v.az * 0.9, el: Math.max(-4, k.el + v.el), d: k.d * v.d, fov: k.fov + v.fov, roll: (k.roll || 0) + v.roll }; };
    out.push({ ...s, id: j === 0 ? s.id : s.id + '~' + j, a, b, cut: j === 0 ? s.cut : false, glide: j > 0, cam: [mk(t0, a, 0), mk(t1, b, 1)], trIn: j === 0 ? s.trIn : { type: 'glide', N: 0 } }); a = b + 1; }
  return out; });
const SETNEEDS = { outback: ['nature/rocks', 'nature/picket_fence', 'buildings/barn', 'buildings/windmill', 'buildings/house_small', 'nature/bush'], countryside: ['nature/tree_oak', 'nature/haybale', 'buildings/house_small', 'buildings/house_two', 'buildings/church', 'buildings/barn', 'buildings/windmill'], arctic: ['nature/rocks'], palace: ['nature/tree_palm', 'buildings/castle_tower', 'buildings/house_two', 'buildings/church'], jungle: ['nature/bush'], medieval: ['buildings/house_small', 'buildings/castle_tower', 'buildings/church', 'nature/tree_oak', 'nature/fountain'], street: ['buildings/shop', 'buildings/house_two', 'buildings/apartment', 'buildings/house_blue', 'nature/lamppost'], harbor: ['crate', 'ship', 'buildings/lighthouse', 'nature/tree_palm'], mountain: ['nature/rocks', 'war/sandbags', 'buildings/castle_tower', 'buildings/church'], hall: [], stadium: [] };   // assets each set builder needs (auto-loaded)
export const ASSETS = [...new Set([...(SPEC.assets || []), ...(SPEC.sets || []).flatMap((s) => SETNEEDS[s] || [])])].concat(['bear', 'horse', 'horse_sela', 'dog', 'cat', 'cow', 'deer', 'donkey', 'elephant', 'fox', 'goat', 'lion', 'rabbit', 'sheep', 'wolf'].filter((n) => JSON.stringify(SPEC.shots).includes('"animal":"' + n + '"'))).concat(['emu', 'chicken'].filter((n) => JSON.stringify(SPEC.shots).includes('"bird":"' + n + '"'))), SETS_USED = SPEC.sets || [], SETX = SPEC.setx || {};
export const SHOTS = SPEC.shots.map((s) => ({ id: s.id, a: s.a, b: s.b, light: s.light, tr: s.trIn || null }));
export const HEROES = Object.fromEntries(SPEC.shots.map((s) => [s.id, s.hero || { hero: 'any', frame: 'medium' }]));
export const shotAt = (f) => SHOTS.find((s) => f >= s.a && f <= s.b) || SHOTS[SHOTS.length - 1];
let FORCE = null; if (typeof window !== 'undefined') window.__force = (i) => { FORCE = i; };
const SP = (f) => (FORCE !== null ? SPEC.shots[FORCE] : (SPEC.shots.find((s) => f >= s.a && f <= s.b) || SPEC.shots[SPEC.shots.length - 1]));
export const smooth = M.smooth;
export const fitD = (h, frac, fov) => h / (frac * 2 * Math.tan(fov * Math.PI / 360));   // camera distance so an object of height h fills `frac` of the frame height
// ---------- lights (shared presets; a story may add/override in SPEC.lights) ----------
const LIB_LIGHTS = {
  dawn: { exp: 0.72, cloud: '#ffd9c4', az: 95, el: 16, sky: '#ffdca8', ground: '#7a6a4a', hemi: 1.1, sun: '#ffc98a', sunI: 2.9, fog: '#ffd8a8', fogNear: 90, fogFar: 650, skyTop: '#7ea4e0', skyHor: '#ffd6a0', sunDisc: '#fff0c8', sunSize: 0.004, sat: 1.15, gain: '#fff1e0', vig: 0.26, shadowExt: 18, rimC: '#8fb4ff', rimI: 0.55, glow: 0.9, shafts: 0.5 },
  day: { az: 140, el: 50, sky: '#c9d0f6', ground: '#8a8262', hemi: 1.2, sun: '#fff3dc', sunI: 2.5, fog: '#cfe0f2', fogNear: 120, fogFar: 800, skyTop: '#3f80d4', skyHor: '#c9def4', sat: 1.12, vig: 0.2, shadowExt: 22, rimC: '#bcd8ff', rimI: 0.3 },
  noon: { az: 160, el: 68, sky: '#d9defa', ground: '#a29a72', hemi: 1.3, sun: '#fffaf0', sunI: 2.7, fog: '#dfeaf6', fogNear: 150, fogFar: 900, skyTop: '#3a86e0', skyHor: '#cfe4f8', sat: 1.12, vig: 0.18, shadowExt: 22, rimC: '#cfe2ff', rimI: 0.25 },
  tense: { cloud: '#d8b8a8', az: 8, el: 9, sky: '#b090b8', ground: '#6a4c40', hemi: 0.95, sun: '#ff8a50', sunI: 3.0, fog: '#e8906a', fogNear: 70, fogFar: 600, skyTop: '#5a4a9a', skyHor: '#ff9a62', sunDisc: '#ffe0b0', sunSize: 0.0045, sat: 1.18, gain: '#ffe6d2', vig: 0.32, shadowExt: 26, rimC: '#6a7cff', rimI: 0.75, glow: 1.0 },
  storm: { cloud: '#6f7a8c', az: 200, el: 30, sky: '#8f9db8', ground: '#4a5060', hemi: 1.0, sun: '#d8e2f0', sunI: 1.9, fog: '#8f9db4', fogNear: 60, fogFar: 520, skyTop: '#46567a', skyHor: '#a4b2c8', sat: 1.0, vig: 0.34, shadowExt: 30, rimC: '#a0c0ff', rimI: 0.4 },
  overcast: { cloud: '#c2c8d2', az: 180, el: 45, sky: '#c8d0da', ground: '#7a7a72', hemi: 1.25, sun: '#e8eef4', sunI: 1.4, fog: '#c4ccd6', fogNear: 60, fogFar: 520, skyTop: '#8a98ac', skyHor: '#c9d2dc', sat: 0.95, vig: 0.28, shadowExt: 24, rimC: '#bcd0ee', rimI: 0.3 },
  space: { stars: 1.6, noClouds: 1, exp: 1.15, cloud: '#05060f', az: 200, el: 30, sky: '#2a2c38', ground: '#3a3a44', hemi: 0.9, sun: '#ffffff', sunI: 2.6, fog: '#05060f', fogNear: 120, fogFar: 900, skyTop: '#020308', skyHor: '#0a0c1a', sat: 0.9, gain: '#e8ecf4', vig: 0.45, shadowExt: 24, rimC: '#8aa8ff', rimI: 0.8 },   /* ESPACO (19/11): ceu preto estrelado, sem nuvem, luz branca forte */
  night: { stars: 1, exp: 1.08, cloud: '#3c4a80', az: 220, el: 38, sky: '#33447c', ground: '#222c52', hemi: 0.98, sun: '#b4c0ff', sunI: 1.35, fog: '#101a3a', fogNear: 40, fogFar: 420, skyTop: '#0b1438', skyHor: '#263a74', sat: 0.6, gain: '#a9b8f0', vig: 0.4, shadowExt: 24, rimC: '#6a8aff', rimI: 0.7 },
  deck: { az: 150, el: 40, sky: '#d6e6f8', ground: '#8a7a5a', hemi: 1.2, sun: '#fff1d4', sunI: 2.5, fog: '#d3e3f2', fogNear: 100, fogFar: 700, skyTop: '#4d88d8', skyHor: '#cfe2f5', sat: 1.1, vig: 0.24, shadowExt: 22, rimC: '#bcd8ff', rimI: 0.3 },
  study_dark: { exp: 0.82, az: 250, el: 38, sky: '#3a3550', ground: '#2a2230', hemi: 0.6, sun: '#ffc890', sunI: 0.75, fog: '#151020', fogNear: 30, fogFar: 220, skyTop: '#100c1c', skyHor: '#1c1830', sat: 0.85, gain: '#c4b4e6', vig: 0.58, shadowExt: 18, rimC: '#9ab0ff', rimI: 0.85 },   /* SALA NO ESCURO (luz apagada / noite dentro de casa) */
  study: { az: 250, el: 38, sky: '#ffe9c4', ground: '#8a6a4a', hemi: 1.15, sun: '#ffe2b0', sunI: 2.1, fog: '#7a5a46', fogNear: 60, fogFar: 400, skyTop: '#3a2a36', skyHor: '#5a3a3a', sat: 1.12, gain: '#fff0dc', vig: 0.34, shadowExt: 18, rimC: '#ffc880', rimI: 0.55, shafts: 0.55 },
  dusk: { cloud: '#ffc9a8', az: 275, el: 7, sky: '#b498c8', ground: '#5a4658', hemi: 0.95, sun: '#ff9060', sunI: 2.8, fog: '#d88a78', fogNear: 80, fogFar: 600, skyTop: '#5a4a94', skyHor: '#ff9a6a', sunDisc: '#ffd8a0', sunSize: 0.0045, sat: 1.2, gain: '#ffe2d0', vig: 0.34, shadowExt: 26, rimC: '#7a8cff', rimI: 0.65, glow: 1.0 },
  arctic: { exp: 0.80, az: 200, el: 12, sky: '#c9b8ec', ground: '#7a8cc8', hemi: 0.9, sun: '#ffd9a8', sunI: 3.1, fog: '#f2d2c8', fogNear: 120, fogFar: 800, skyTop: '#3a58e0', skyHor: '#ffc3a0', sunDisc: '#fff0c8', sunSize: 0.006, glow: 0.9, sat: 1.9, gain: '#fff0e0', vig: 0.24, shadowExt: 26, rimC: '#ffc890', rimI: 0.6, shafts: 0.6, gsel: 1 },
  golden: { az: 225, el: 30, sky: '#cdb0e8', ground: '#a8785a', hemi: 1.55, sun: '#ffd8a0', sunI: 2.6, fog: '#f4c8a0', fogNear: 120, fogFar: 800, skyTop: '#6a5aa8', skyHor: '#ffb070', sunDisc: '#fff0c0', sunSize: 0.006, glow: 0.8, sat: 1.1, gain: '#fff2e0', vig: 0.26, shadowExt: 26, rimC: '#ffc890', rimI: 0.6, shafts: 0.6 },
  desert: { az: 150, el: 62, sky: '#e8dcf2', ground: '#b88a5a', hemi: 1.2, sun: '#fff0d0', sunI: 3.0, fog: '#f0dcb8', fogNear: 120, fogFar: 800, skyTop: '#4f94e0', skyHor: '#f6e4c0', sat: 1.15, gain: '#fff2de', vig: 0.24, shadowExt: 24, rimC: '#ffe0b0', rimI: 0.3 },
  grave: { cloud: '#c8a8b0', az: 280, el: 6, sky: '#c0a0c8', ground: '#5a4a58', hemi: 1.0, sun: '#ffa070', sunI: 2.6, fog: '#e0988a', fogNear: 80, fogFar: 600, skyTop: '#4a4090', skyHor: '#ffa878', sunDisc: '#ffe0b0', sunSize: 0.005, sat: 1.2, gain: '#ffe6d6', vig: 0.36, shadowExt: 20, rimC: '#8a9cff', rimI: 0.65, glow: 1.0 },
};
export const LIGHTS = { ...LIB_LIGHTS, ...(SPEC.lights || {}) };
export const lightFor = (S, f) => { const sp = SP(f); const L = { ...LIGHTS[sp.light] }; if (sp.lightMod) Object.assign(L, typeof sp.lightMod === 'function' ? sp.lightMod(f, L) : sp.lightMod); L.exp = (L.exp ?? 1) * (SPEC.exp ?? 1) * (sp.exp ?? 1); if (L.gsel === undefined) L.gsel = ['dusk', 'dawn', 'golden', 'tense', 'grave'].includes(sp.light) ? 1 : 0; if (L.shafts === undefined) L.shafts = ['day', 'noon', 'dusk', 'dawn', 'desert', 'study', 'deck', 'arctic'].includes(sp.light) ? 0.5 : 0; return L; };
// ---------- cameras ----------
const VAR_EL = [4, -5, 12, 0, -8, 9, 2, -4, 15, -2], VAR_AZ = [-10, 14, -4, 20, -16, 8, 0, -22, 12, -6], VAR_ROLL = [0, 3, -2.5, 0, 4, -3, 0, 2.5, -4, 0];
const resolveKey = (k, si = 0, S = {}) => { if (k.at) { const vv = SPEC.vary !== false && S.vary !== false, j = (si * 7 + 3) % 10; const el = ((k.el ?? 8) + (vv ? VAR_EL[j] : 0)) * Math.PI / 180, az = ((k.az ?? 0) + (vv ? VAR_AZ[j] : 0)) * Math.PI / 180, d = k.d; return { f: k.f, pos: [k.at[0] + d * Math.sin(az) * Math.cos(el), k.at[1] + d * Math.sin(el), k.at[2] + d * Math.cos(az) * Math.cos(el)], look: k.look || k.at, fov: k.fov ?? 34, roll: (k.roll || 0) + (vv ? VAR_ROLL[(j + 3) % 10] : 0), ease: k.ease, path: k.path }; } return { roll: 0, ...k }; };
const CAMKEYS = SPEC.shots.map((s, si) => (s.cam || []).map((k) => resolveKey(k, si, s)));
const KICKS = (SPEC.kicks || []);
const CUTS = SPEC.shots.map((s) => s.a).filter((a, i) => i > 0 && SPEC.shots[i].cut !== false);
export const camAt = (f) => {
  const si0 = FORCE !== null ? FORCE : SPEC.shots.findIndex((s) => f >= s.a && f <= s.b), si = si0 < 0 ? SPEC.shots.length - 1 : si0, S = SPEC.shots[si], K = CAMKEYS[si];
  let c = camFromKeys(K, f, { creep: S.creep ?? SPEC.creep ?? 0.0045, kicks: KICKS.filter((k) => k.f >= S.a && k.f <= S.b + 8) });
  // v9: ACTION PUNCH-IN (micro zoom-in dinamico estilo Ricks Clips sincronizado com picos de acao)
  if (S.punches && S.punches.length) { let pz = 0; for (const pn of S.punches) { const dt = f - pn.f; if (dt >= -6 && dt <= (pn.dur || 22)) { const t = dt < 0 ? (dt + 6) / 6 : Math.max(0, 1 - dt / (pn.dur || 22)); pz = Math.max(pz, (pn.amt || 0.14) * t * t * (3 - 2 * t)); } } if (pz > 0.005) c.fov = Math.max(22, c.fov * (1 - pz)); }
  if (S.glide && si > 0 && f < S.a + (S.glideN ?? SPEC.glideN ?? 26)) { const G = S.glideN ?? SPEC.glideN ?? 26, ps = SPEC.shots[si - 1], pc = camFromKeys(CAMKEYS[si - 1], ps.b, { creep: ps.creep ?? SPEC.creep ?? 0.0045, kicks: [] }); const x = Math.min(1, Math.max(0, (f - S.a + 1) / (G + 1))), t = x * x * x * (x * (x * 6 - 15) + 10); const L3 = (p, q) => [0, 1, 2].map((i) => p[i] + (q[i] - p[i]) * t);
    c = { ...c, pos: L3(pc.pos, c.pos), look: L3(pc.look, c.look), fov: pc.fov + (c.fov - pc.fov) * t, roll: (pc.roll || 0) + ((c.roll || 0) - (pc.roll || 0)) * t }; }
  { const kf = (typeof window !== 'undefined' && window.KFIT && window.KFIT[S.id]) || (SPEC.fit && SPEC.fit[S.id]) || 1; if (kf !== 1) c.pos = [c.look[0] + (c.pos[0] - c.look[0]) * kf, c.look[1] + (c.pos[1] - c.look[1]) * kf, c.look[2] + (c.pos[2] - c.look[2]) * kf]; }
  { const k = SPEC.lens ?? 1.32; if (k !== 1) { const f2 = Math.min(78, c.fov * k), q = Math.tan(c.fov * Math.PI / 360) / Math.tan(f2 * Math.PI / 360); c.pos = [c.look[0] + (c.pos[0] - c.look[0]) * q, c.look[1] + (c.pos[1] - c.look[1]) * q, c.look[2] + (c.pos[2] - c.look[2]) * q]; c.fov = f2; } }
  const cut = CUTS.find((cf) => f >= cf && f < cf + 4), fl = (SPEC.flashes || []).find((x) => f >= x.f && f < x.f + (x.n || 5));
  { const nx = SPEC.shots[si + 1], M_ = 7, ZM = SPEC.pushZoom ?? 2.6, e01 = (t) => { t = Math.min(1, Math.max(0, t)); return t * t * (3 - 2 * t); }; let z = 1, zb = 0;
    if (nx && nx.trIn && nx.trIn.type === 'push' && f >= nx.a - M_) { const t = e01((f - (nx.a - M_)) / M_); z *= 1 + (ZM - 1) * t; zb = Math.max(zb, t); }
    if (S.trIn && S.trIn.type === 'whip' && f < S.a + 6) { const tw = 1 - (f - S.a) / 6; c.pos = [c.pos[0] + tw * tw * 4.5, c.pos[1], c.pos[2]]; c.zb = Math.max(c.zb || 0, tw * 0.9); }
    if (S.trIn && S.trIn.type === 'push' && f < S.a + M_) { const t = 1 - e01((f - S.a + 1) / M_); z *= 1 + (ZM - 1) * t; zb = Math.max(zb, t); }
    if (z !== 1) c.fov = 2 * Math.atan(Math.tan(c.fov * Math.PI / 360) / z) * 180 / Math.PI; c.zb = zb; }
  if (SPEC.camFloor !== false) { const FLR = DECK + (SPEC.camFloor ?? 0.55), kk = 0.22, dy = c.pos[1] - FLR; c.pos = [c.pos[0], FLR + 0.5 * (dy + Math.sqrt(dy * dy + kk * kk)), c.pos[2]]; }   // never below the ground: smooth floor (no kinks), look target untouched
  c.flash = fl ? (fl.a ?? 0.8) * (1 - (f - fl.f) / (fl.n || 5)) : cut !== undefined ? (SPEC.cutFlash ?? 0) * (1 - (f - cut) / 4) : 0; return c;
};
const dist3 = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
export const dofAt = (f) => { const S = SP(f), C = camAt(f); const d = S.dof || {}, dd = dist3(C.pos, C.look); return { focus: d.focus ?? dd, cinf: (typeof window !== 'undefined' && window.CINF !== undefined) ? window.CINF : (d.cinf ?? S.cinf ?? SPEC.cinf ?? (((SPEC.shots.indexOf(S) % 3) === 1) ? Math.max(5, Math.min(14, 16 - 0.8 * (dd - 4))) : Math.max(1.5, Math.min(4, 6 - 0.3 * (dd - 4))))) }; };   // soft focus on ~1/3 of the takes (MS/CU 10-16 px), the rest nearly sharp   // reference: MS/CU 10-16 px, wides ~0-4
// ---------- world state (weather + 3D props) ----------
const lerp2 = (a, b, t) => [lerp(a[0], b[0], t), lerp(a[1], b[1], t)];
const moveAt = (base, mv, f) => { if (!mv) return base; const [to, a, b, mode] = mv; const t = mode === 'lin' ? ramp(f, a, b) : M.smooth(ramp(f, a, b)); return lerp2(base, to, t); };
const G3D = ['bear', 'horse', 'horse_sela', 'dog', 'cat', 'cow', 'deer', 'donkey', 'elephant', 'fox', 'goat', 'lion', 'rabbit', 'sheep', 'wolf'];   /* animais 3D arredondados (o desenho 2D saia quadrado) */ const is3 = (a) => G3D.includes(a.animal) || a.bird === 'emu' || a.bird === 'chicken';   /* 19/11: galinha 3D com anatomia; o PORCO fica 2D (ordem do Gibson: cartunesco e engracado; pig.glb 3D fica guardado) */
export const worldAt = (f) => {
  const S = SP(f), W = { props: [], weather: { wind: 0.5, dx: 1, dz: 0.3, ...(typeof S.weather === 'function' ? S.weather(f) : S.weather || {}) } };
  W.weather.wind = Math.max(0, (W.weather.wind ?? 0.5) + (S.light === 'study' ? 0 : 0.1 * Math.sin(f / 30 * 0.5) + 0.06 * Math.sin(f / 30 * 1.7)));
  for (const p of (S.props || [])) { if (p.a !== undefined && (f < p.a || f > p.b)) continue; const base = p.at, pos = moveAt(base, p.move, f), prev = moveAt(base, p.move, f - 1), dx = pos[0] - prev[0], dz = pos[1] - prev[1]; const sp = Math.hypot(dx, dz) * 30; const dir = p.move ? Math.atan2(pos[0] - base[0], pos[1] - base[1]) : 0;
    const tw = typeof p.turret === 'function' ? p.turret(f) : p.turret; W.props.push({ sy: typeof p.sy === 'function' ? p.sy(f) : p.sy, asset: p.asset, x: pos[0], z: pos[1], y: typeof p.y === 'function' ? p.y(f) : (p.y ?? DECK), ry: p.move && p.align !== false ? dir + (p.ry || 0) : (p.ry || 0) + (p.spinY ? f / 30 * p.spinY : 0), s: typeof p.s === 'function' ? p.s(f) : (p.s || 1), tint: p.tint, t: f / 30, dist: p.move ? Math.hypot(pos[0] - base[0], pos[1] - base[1]) : 0, dxw: p.move ? pos[0] - base[0] : 0, dzw: p.move ? pos[1] - base[1] : 0, turret: tw || 0, pitch: p.pitch || 0, recoil: p.fire ? Math.max(0, 1 - (f - p.fire) / 8) * (f >= p.fire ? 1 : 0) : 0, bob: sp > 0.1 ? 0.04 : 0 }); }
  for (const a of (S.actors || [])) if (is3(a) && !(a.a !== undefined && (f < a.a || f > a.b))) { const sp3 = a.animal || a.bird || 'emu'; const st3 = typeof a.state === 'function' ? a.state(f) : (a.state || 'stand'); const fal3 = a.fall ? a.fall(f) : (st3 === 'fall' ? 1 : 0);   /* TIRO: o bicho 3D deita de lado; FUCA: abaixa o focinho */ const pos = moveAt(a.at, a.move, f); const trot = (st3 === 'trot' || st3 === 'walk' || st3 === 'run') && a.move && f >= a.move[1] && f <= a.move[2] && !fal3; const sc = (a.s || 1) * ({ horse: 1.7, horse_sela: 1.7, emu: 0.62, chicken: 0.62, pig: 1.5, bear: 1.5, dog: 1.25, cat: 1.15, cow: 1.5, deer: 1.4, donkey: 1.4, elephant: 1.9, fox: 1.15, goat: 1.25, lion: 1.5, rabbit: 1.1, sheep: 1.3, wolf: 1.35 }[sp3] ?? 0.78);
    W.props.push({ asset: sp3, walk: (st3 === 'walk' || trot) ? (sp3 === 'emu' ? 10 : sp3 === 'chicken' ? 16 : 0) : 0, peck: st3 === 'peck', rz: fal3 * 1.5 * (a.flip ? -1 : 1), rx: st3 === 'root' ? 0.18 + 0.1 * Math.sin(f * 0.35) : 0, t0: (a.seed || 0), x: pos[0], z: pos[1], y: DECK + fal3 * 0.25 * sc + (trot ? 0.08 * Math.abs(Math.sin(f * 0.55)) : 0.015 * Math.sin(f * 0.12)), ry: (a.ry ?? ((a.bird === 'emu' || a.bird === 'chicken') && !a.move ? (a.flip ? 1.1 : -1.1) : a.move ? Math.atan2(a.move[0][0] - a.at[0], a.move[0][1] - a.at[1])  : 0.95)) + (trot ? 0.12 * Math.sin(f * 0.28) : 0.05 * Math.sin(f * 0.04)), s: sc, sy: 1 + (trot ? 0.04 : 0.025) * Math.sin(f * (trot ? 0.55 : 0.1)), tint: null }); }
  if (S.world) Object.assign(W, S.world(f));
  return W;
};
// ---------- cast ----------
const SK = ['#ffe2c2', '#f5c9a0', '#ecd0b6', '#c99067'];
export const OUT = Object.assign({
  US: (v = 0, e = {}) => ({ _id: 'US', jacket: '#27408b', pants: '#7d9fd0', boots: '#1b1b1f', hat: 'shako', belt: '#f1efe6', buttons: '#e8c45a', rifle: true, skin: SK[v % 4], ...(v % 3 === 1 ? { moustache: '#4a3426' } : {}), ...e }),
  UK: (v = 0, e = {}) => ({ _id: 'UK', jacket: '#c0262d', pants: '#f1efe6', boots: '#1b1b1f', hat: 'shako', belt: '#f1efe6', buttons: '#e8c45a', rifle: true, skin: SK[(v + 1) % 4], ...(v % 3 === 0 ? { moustache: '#3a2a1f' } : {}), ...e }),
  GI: (v = 0, e = {}) => ({ _id: 'GI', jacket: '#6a7440', pants: '#5a6334', boots: '#2a2218', hat: 'cap', cap: '#5a6334', belt: '#8a7a50', skin: SK[v % 4], rifle: false, ...e }),
  OFFICER: (v = 0, e = {}) => ({ _id: 'officer', jacket: '#6a7440', pants: '#8a7a50', boots: '#2a2218', hat: 'shako_tall', buttons: '#e8c45a', sash: null, moustache: '#4a3020', build: 'stout', skin: SK[v % 4], rifle: false, ...e }),
  GER: (v = 0, e = {}) => ({ _id: 'GER', jacket: '#6c7078', pants: '#4a4e56', boots: '#1b1b1f', hat: 'shako', belt: '#2a2a2a', buttons: '#c9ccd2', rifle: false, skin: SK[v % 4], ...e }),
  CIV: (v = 0, e = {}) => ({ _id: 'civ', jacket: ['#3f6fb5', '#8c3b4a', '#5d7a3a', '#b5653f', '#2f5f6a', '#7b5ac9'][v % 6], pants: '#3b3f52', boots: '#4a3426', skin: SK[v % 4], ...(v % 2 ? { hat: 'bonnet', dress: ['#d9a441', '#c25a7a', '#5a8fc2'][v % 3] } : { hat: 'tophat' }), ...e }),
  ARTIST: (v = 0, e = {}) => ({ _id: 'artist', jacket: ['#d9a441', '#b5653f', '#7b5ac9', '#5a8fc2'][v % 4], pants: '#3b3f52', boots: '#4a3426', hat: 'cap', cap: ['#8a3a3a', '#2f5f6a', '#d9a441'][v % 3], skin: SK[v % 4], ...(v % 2 ? { moustache: '#4a3020' } : {}), ...e }),
}, SPEC.outfits || {});
const B = (T, o0, opts, pos, extra = {}) => { const o = { ...o0, ...(o0.build === undefined && !SPEC.noLanky ? { build: 'lanky' } : {}), ...(SPEC.keepSkin ? {} : { skin: o0.pele || '#fffdf8' }) }; return B2(T, o, opts, pos, extra); };
const B2 = (T, o, opts, pos, extra = {}) => ({ id: extra.id || o._id || 'person', key: (extra.sideWalk ? 'bs' : 'b') + JSON.stringify([o, opts]), draw: (p) => (extra.sideWalk ? T.bodySide(p, o, { blink: false, ...opts, mode: 'march', ...(opts.mode === 'stroll' ? { stride: 0.72, stomp: 0.8 } : {}) }) : T.bodyFront(p, o, { blink: false, ...opts })), x: pos[0], y: pos[1] ?? DECK, z: pos[2], ...extra });
const qq = (x, n = 2) => Math.round(x * 10 ** n) / 10 ** n;
/* INTERACAO FISICA entre personagens: avancar, recuar, inclinar-se, empurrar, cambalear, dar um passo, pular, reverencia (a.inter = { k, a, b, dir, n, ph }) */
const interAt = (a, f) => { const I = (a.inters && a.inters.find((x) => f >= x.a && f <= x.b)) || a.inter; if (!I || f < I.a || f > I.b) return null; const t = (f - I.a) / Math.max(1, I.b - I.a), d = I.dir || 1, n = I.n || 2, bell = Math.sin(Math.PI * t), pu = Math.max(0, Math.sin(t * Math.PI * 2 * n + (I.ph || 0))) ** 0.7, sm = (x) => { x = Math.max(0, Math.min(1, x)); return x * x * (3 - 2 * x); };
  switch (I.k) {
    case 'lunge': return { dx: d * 0.5 * pu, tilt: d * 10 * pu, hop: 0 };
    case 'recoil': return { dx: -d * 0.45 * pu, tilt: -d * 9 * pu, hop: 0.05 * pu };
    case 'lean': return { dx: d * 0.4 * bell, tilt: d * 9 * bell, hop: 0 };
    case 'step': { const k = sm(t / 0.3) * (1 - sm((t - 0.8) / 0.2)); return { dx: d * 0.6 * k, tilt: d * 4 * k, hop: 0.04 * Math.abs(Math.sin(t * 40)) * (t < 0.3 || t > 0.8 ? 1 : 0) }; }
    case 'shove': { const k = Math.exp(-(((t - 0.45) / 0.09) ** 2)); return { dx: d * 0.6 * k, tilt: d * 14 * k, hop: 0 }; }
    case 'stagger': { const k = sm((t - 0.45) / 0.12) * (1 - sm((t - 0.85) / 0.15)), w = t > 0.45 ? Math.sin((t - 0.45) * 30) * Math.exp(-(t - 0.45) * 5) : 0; return { dx: -d * 0.45 * k, tilt: -d * (14 * k + 8 * w), hop: 0.12 * Math.max(0, w) }; }
    case 'hug': { const k = sm((t - 0.25) / 0.2) * (1 - sm((t - 0.85) / 0.15)); return { dx: d * 0.95 * k, tilt: d * 7 * k, hop: 0.03 * k * Math.abs(Math.sin(t * 30)) }; }   /* ABRACO: os dois andam um ate o outro e ficam colados, inclinados */
    case 'shiver': return { dx: 0.035 * Math.sin(f * 2.4), tilt: 1.5 * Math.sin(f * 1.9), hop: 0 };   /* FRIO: tremendo */
    case 'hop': return { dx: 0, tilt: 0, hop: 0.3 * Math.abs(Math.sin(t * Math.PI * 2 * n)) };
    case 'bow': return { dx: 0, tilt: d * 20 * bell, hop: 0 };
    case 'nod': return { dx: d * 0.1 * bell, tilt: d * 3 * Math.sin(t * Math.PI * 6), hop: 0.03 * Math.abs(Math.sin(t * Math.PI * 6)) };
  } return null; };
const PO = (f, a, seed, exo = {}) => { const mode = a.pose || 'stand'; const base = { seed, blink: blinkAt(f, seed) > 0, expr: (typeof a.expr === 'function' ? a.expr(f) : a.expr) || 'neutral', look: a.look ?? 0.2, ...exo };
  if (mode === 'talk' && exo.spk === 0) { const q = f * 0.5; return { mode: 'stand', phase: 0, tilt: 0, headTilt: qq(4 * Math.sin(q) * (Math.floor(f / 38) % 2 ? 1 : 0.3), 0), ...base, ...exo }; }   /* OUVINDO: parado, acena com a cabeca */
  if (mode === 'talk') { const q = f * 0.22 + seed * 1.9, st = (Math.floor(f / 26) + seed) % 4; return { mode: 'stand', phase: 0, tilt: qq(3 * Math.sin(q), 0), headTilt: qq(-5 * Math.sin(q + 0.7), 0), ...base, ...exo, ...(st === 0 || st === 2 ? { gest: st ? 'shrug' : 'point', gk: 0.8, gt: qq(f / 30, 1) } : {}) }; }   /* CONVERSAR: gesticula de leve enquanto fala, alternando com pausa */
  if (mode === 'cheer') { const q = f * 0.4 + seed * 1.3; return { mode: 'stand', phase: 0, tilt: qq(6 * Math.sin(q), 0), headTilt: qq(5 * Math.sin(q + 0.5), 0), ...base, ...exo, gest: (Math.floor(f / 14) + seed) % 3 ? 'up' : 'wave2', gk: 1, gt: qq(f / 30, 1) }; }   /* COMEMORAR: bracos para cima, pulando */
  if (mode === 'react') { const k = (f + seed * 11) % 96; return { mode: 'stand', phase: 0, tilt: qq((k < 30 ? -6 : 2.5 * Math.sin(f * 0.06)), 0), headTilt: qq(4 * Math.sin(f * 0.05 + seed), 0), ...base, ...exo, ...(k < 34 ? { gest: 'scared', gk: 1, gt: qq(f / 30, 1) } : k > 60 && k < 80 ? { gest: 'think', gk: 0.9, gt: qq(f / 30, 1) } : {}) }; }   /* REAGIR: susto (maos no rosto, recua), depois pensa */
  if (mode === 'argue' && exo.spk === 0) { return { mode: 'stand', phase: 0, tilt: qq(seed % 2 ? 2 : -2, 0), headTilt: qq(3 * Math.sin(f * 0.3), 0), ...base, ...exo, gest: (Math.floor(f / 38) + seed) % 2 ? 'cross' : 'hips', gk: 1, gt: qq(f / 30, 1) }; }   /* OUVINDO a bronca: braco cruzado ou mao na cintura */
  if (mode === 'argue') { const q = f * 0.3 + seed * 2.1, st = (Math.floor(f / 22) + seed) % 4; return { mode: 'stand', phase: 0, tilt: qq(5 * Math.sin(q) + (seed % 2 ? 3 : -3), 0), headTilt: qq(-6 * Math.sin(q + 0.8), 0), ...base, ...exo, gest: ['point', 'shrug', 'hips', 'point'][st], gk: 1, gt: qq(f / 30, 1) }; }   /* DISCUTIR: inclina para o outro, aponta, da de ombros, poe a mao na cintura */
  if (mode === 'dance') { const q = f * 0.36 + seed * 1.7; return { mode: 'stand', phase: 0, tilt: qq(9 * Math.sin(q), 0), headTilt: qq(-8 * Math.sin(q + 0.6), 0), ...base, ...exo, gest: (Math.floor(f / 16) + seed) % 2 ? 'up' : 'wave2', gk: 1, gt: qq(f / 30, 1) }; }   /* DANCAR: corpo balanca, bracos para cima alternando, pulinho */
  if (mode === 'stand' && exo.__acted) return { mode: 'stand', phase: 0, tilt: qq(2.4 * Math.sin((f + seed * 7) * 0.05), 1), headTilt: qq(3.2 * Math.sin((f + seed * 5) * 0.037 + 1), 1), lift: a.lift, ...base };
  if (mode === 'stand') { const cyc = 84, ph = (f + seed * 23) % cyc, g = a.gesture !== false && SPEC.gestures !== false && ph < 30 && (Math.floor((f + seed * 23) / cyc) + seed) % 3 !== 0; const ex = base.expr;
    const em = (typeof a.expr === 'function') ? ex : ({ smile: ph > 50 && ph < 66 ? 'grin' : ex, stern: ph > 56 && ph < 70 ? 'neutral' : ex, neutral: ph > 40 && ph < 52 ? 'smile_closed' : ex, nervous: ph > 40 && ph < 56 ? 'pained' : ex, grin: ph > 60 && ph < 72 ? 'laugh' : ex, shock: ph > 40 && ph < 60 ? 'nervous' : ex }[ex] || ex);
    return { mode: 'stand', phase: 0, tilt: qq(3.2 * Math.sin((f + seed * 7) * 0.06), 1), headTilt: qq(4.5 * Math.sin((f + seed * 5) * 0.045 + 1), 1), lift: a.lift, ...base, expr: em, ...(g ? { wave: qq(Math.sin(ph * 0.42), 2) } : {}) }; }
  /* passo casado com a velocidade no chao (sem pe deslizando): ciclos/quadro = velocidade / comprimento da passada */
  const stepSp = (stride, def) => (a.move && a.move[0] && a.at && a.autoStep !== false) ? Math.min(0.06, Math.max(0.012, Math.hypot(a.move[0][0] - a.at[0], a.move[0][1] - a.at[1]) / Math.max(1, a.move[2] - a.move[1]) / stride)) : (a.speed || def);
  if (mode === 'run') return { mode: 'march', phase: qq(((f * 0.075 + seed * 0.17) % 1), 2), tilt: 13, headTilt: qq(5 * Math.sin(f * 0.9 + seed), 0), ...base };   /* CORRIDA: passo bem rapido, corpo jogado para a frente, cabeca balancando */
  if (mode === 'march') return { mode: 'march', phase: qq(((f * stepSp(2.5, 0.033) + seed * 0.17) % 1), 2), ...base };
  if (mode === 'stroll') return { mode: 'stroll', phase: qq(((f * stepSp(2.1, 0.02) + seed * 0.13) % 1), 2), ...base };
  return { mode, phase: 0, ...base }; };
export const actorsAt = (f, T) => {
  const S = SP(f), out = []; const tint = ['tense', 'dusk', 'grave'].includes(S.light) ? '#ffd9c0' : S.light === 'storm' ? '#c8d4e8' : S.light === 'night' ? '#e4e9fb' : '#ffffff';
  (S.actors || []).forEach((a, i) => { if (a.a !== undefined && (f < a.a || f > a.b)) return; const seed = a.seed ?? (i * 7 + 3); let _curAt = a.at, _curMv = a.move, _mvPose = null;
    if (a.moves && a.moves.length) {
      for (const mv_ of a.moves) {
        if (f < mv_[1]) break;
        if (f <= mv_[2]) { _curMv = mv_; _mvPose = mv_[4] || null; break; }
        _curAt = mv_[0]; _curMv = null;
      }
    }
    const at = moveAt(_curAt, _curMv, f); let x = at[0]; const z = at[1]; const IN = interAt(a, f); if (IN) x += IN.dx; const moving = _curMv && f >= _curMv[1] && f <= _curMv[2];
    const exc = ['laugh', 'grin', 'shock'].includes(typeof a.expr === 'function' ? a.expr(f) : a.expr) ? 0.07 : 0; const bob = a.pose === 'cheer' ? Math.abs(Math.sin(f * 0.4 + seed * 1.3)) * 0.2 : a.pose === 'dance' ? Math.abs(Math.sin(f * 0.36 + seed * 1.7)) * 0.16 : (a.bobY || exc) ? Math.abs(Math.sin(f * (a.bobY ? 0.4 : 0.33) + seed)) * (a.bobY || exc) : 0;
    if (is3(a)) return;
    if (a.animal) { const st = typeof a.state === 'function' ? a.state(f) : (a.state || 'stand'); const o = { species: a.animal, state: st, phase: qq(((f * (a.spd || 0.03) + seed * 0.1) % 1), 2), blink: blinkAt(f, seed) > 0 ? 1 : 0, ear: qq(Math.sin(f / 30 * 5 + seed), 1), tail: qq(Math.sin(f / 30 * 8 + seed) * 0.5, 1), expr: a.expr || 'normal', fall: qq(a.fall ? a.fall(f) : (st === 'fall' ? (() => { let k_ = 0; while (k_ < 9 && typeof a.state === 'function' && a.state(f - k_ - 1) === 'fall') k_++; return typeof a.state === 'function' ? (k_ + 1) / 10 : 1; })() : 0), 2),   /* 19/11: estado 'fall' sem curva = o bicho CAI de verdade (deitado, patas para cima), nao fica em pe com olho de X */ t: qq(f / 30 + seed, 2), angel: !!a.angel };
      out.push({ id: a.id || a.animal, key: 'an' + JSON.stringify(o), draw: (p) => (a.animal === 'pig' ? T.pigSide(p, o) : T.animalSide(p, o)), x, y: DECK + (a.y || 0), z, s: (a.s || 1.2) * (SPEC.cs ?? 1.4), flip: !!a.flip, keepColor: a.animal === 'pig', tint, order: 3 }); return; }
    if (a.bird) { const st = typeof a.state === 'function' ? a.state(f) : (a.state || 'stand'); const o = { species: a.bird, state: st, phase: qq(((f * (a.spd || 0.03) + seed * 0.1) % 1), 2), blink: 0, t: qq(f / 30 + seed, 1) };
      out.push({ id: a.id || 'bird', key: 'bd' + JSON.stringify(o), draw: (p) => T.birdSide(p, o), x, y: DECK + (a.y || 0), z, s: (a.s || 0.7) * (SPEC.cs ?? 1.4), flip: !!a.flip, tint, order: 2 }); return; }
    if ((S.hero && S.hero.detalhe) || (/_v$/.test(S.id || '') && f < S.a + 30)) { const C_ = camAt(f); if (Math.hypot(C_.pos[0] - x, C_.pos[2] - z) < Math.max(3.4, 0.62 * Math.hypot(C_.pos[0] - C_.look[0], C_.pos[2] - C_.look[2]) + 0.8)) return; }   /* CLOSE NO OBJETO: quem estiver entre a lente e o objeto (ficaria gigante e cortado) nao e' desenhado nesse trecho */
    let o = typeof a.outfit === 'object' ? a.outfit : OUT[a.outfit](a.v ?? 0, a.over || {});
    if (o.faceId === undefined) { let h = 0; for (const ch of String(o._id || '')) h = (h * 31 + ch.charCodeAt(0)) % 997; o = { ...o, faceId: (h + (a.v ?? 0) * 3 + (a.seed ?? 0) * 5) % 8 }; }   /* rosto proprio por personagem (estavel entre as cenas) */
    const persons = (S.actors || []).filter((q) => q.outfit && !(q.a !== undefined && (f < q.a || f > q.b)));
    const ac = (SPEC.acting === false || a.acting === false) ? null : actFor(f, a, i, S, persons, seed);
    const opts = PO(f, moving ? { ...a, pose: _mvPose || a.walk || a.pose || 'stroll' } : a, seed, { ...(a.opts || {}), ...(ac || {}) });
    /* CAMINHADA NATURAL: quem atravessa a tela e' desenhado de perfil, com o ciclo de passos completo (pernas e bracos alternando) */
    const sideW = (moving && _curMv && _curMv[0] && a.sideWalk !== false && (opts.mode === 'march' || opts.mode === 'stroll' || opts.mode === 'run') && Math.abs(_curMv[0][0] - _curAt[0]) > 1.2 * Math.abs(_curMv[0][1] - _curAt[1])) ? Math.sign(_curMv[0][0] - _curAt[0]) : 0;
    // v9: MULTI-ACAO COM CORPO INTEIRO (ramp-in rapido de 3 frames + inclinacao + avanco + pulo)
    let _gDx = 0, _gHop = 0, _gTilt = 0;
    if (a.gests) {
      let _actG = null;
      for (const g_ of a.gests) if (f >= g_[0] && f <= g_[1]) _actG = g_;
      if (_actG) {
        const dur_ = Math.max(6, _actG[1] - _actG[0]), el_ = f - _actG[0], rem_ = _actG[1] - f;
        const k_ = Math.min(1, el_ / 3, rem_ / 4 + 0.25);
        opts.gest = _actG[2]; opts.gk = qq(Math.max(0, k_), 2); opts.gt = qq(el_ / 30, 2); opts._gx = 1;
        const _gd = a.flip ? -1 : 1, _pu = Math.sin(Math.min(1, el_ / 14) * Math.PI);
        if (_actG[2] === 'punch') { _gDx = _gd * 0.58 * _pu; _gTilt = _gd * 17 * _pu; _gHop = 0.10 * _pu; opts.speedLines = _pu > 0.35; opts.fx = { ...(opts.fx || {}), rage: 1 }; }
        else if (_actG[2] === 'push') { _gDx = _gd * 0.52 * _pu; _gTilt = _gd * 15 * _pu; opts.speedLines = _pu > 0.35; opts.fx = { ...(opts.fx || {}), rage: 1 }; }
        else if (_actG[2] === 'up') { _gHop = 0.22 * Math.abs(Math.sin(el_ * 0.45)) * k_; _gTilt = 6 * Math.sin(el_ * 0.38) * k_; }
        else if (_actG[2] === 'throw' || _actG[2] === 'hammer') { _gTilt = _gd * (-8 + 20 * Math.min(1, el_ / 10)) * k_; }
        else if (_actG[2] === 'scared') { _gDx = -_gd * 0.35 * _pu; _gTilt = -_gd * 12 * _pu; _gHop = 0.12 * _pu; }
      }
    }
    x += _gDx;
    if (a.poses) for (const p_ of a.poses) if (f >= p_[0] && f <= p_[1]) {
      if (p_[2] === 'kneel') { opts.mode = 'kneel'; opts.gest = 'plead'; opts.gk = 1; opts.gt = qq((f - p_[0]) / 30, 2); continue; }
      opts.gest = null;
      if (p_[2] === 'fall') { const _ft = Math.min(1, (f - p_[0]) / 6); opts._fall = qq(_ft, 2); opts.blink = true; opts.expr = 'pained'; _gHop = _ft < 1 ? 0.18 * Math.sin(_ft * Math.PI) : 0; continue; }
      if (p_[2] === 'sleep') { opts.mode = 'sit'; opts.blink = true; opts.expr = 'bored'; } else opts.mode = p_[2];
    }
    if (opts.gest && o.rifle && !opts._gx) opts.gest = null;
    if (opts.gest && (opts.gk || 0) > 0.2 && o.rifle && !['point', 'up'].includes(opts.gest)) o = { ...o, rifle: false };
    delete opts._gx;
    if (IN || _gTilt) opts.tilt = qq((opts.tilt || 0) + (IN ? IN.tilt : 0) + _gTilt, 0);
    // v9: Mira antecipada (16 frames antes) + recuo fisico no disparo + qualquer soldado armado mira
    if (S.shots && o.rifle) { let am = 0, rec = 0; for (const t of S.shots) { am = Math.max(am, f >= t - 16 && f <= t + 16 ? Math.min(1, (f - (t - 16)) / 6, (t + 16 - f) / 6 + 0.35) : 0); if (f >= t && f <= t + 6) rec = Math.max(rec, 1 - (f - t) / 6); } if (am > 0) { opts.aim = qq(am, 1); opts.gest = null; opts.tilt = qq((opts.tilt || 0) - 11 * rec, 0); x -= (a.flip ? -1 : 1) * 0.22 * rec; if (opts.expr === 'angry' || opts.expr === 'shout') opts.fx = { ...(opts.fx || {}), rage: 1 }; } }
    if (o.hold) opts.hp = qq(Math.max(0, Math.sin(f * 0.075 + seed * 2)), 1);   /* usa o objeto de tempos em tempos */
    const _fl = opts._fall; delete opts._fall;
    out.push(B(T, o, opts, [x, DECK + (typeof a.y === 'function' ? a.y(f) : (a.y || 0)) + (a.yFns ? a.yFns.reduce((acc, fn) => acc + fn(f), 0) : 0) + bob + _gHop + (IN ? IN.hop : 0), z], { id: a.id || o._id, tint, s: (a.s || 1) * (SPEC.cs ?? 1.4) * (1 + 0.07 * (opts.lean || 0)), flip: sideW ? sideW < 0 : !!a.flip, ...(a.roll !== undefined ? { roll: typeof a.roll === 'function' ? a.roll(f) : a.roll } : {}), ...(_fl ? { roll: -1.45 * M.easeIn(_fl) * (a.flip ? -1 : 1) } : {}), ...(a.shadow === false ? { shadow: false, blob: false } : {}), ...(sideW ? { sideWalk: sideW } : {}), ...(a.crop ? { crop: a.crop, shadow: false, blob: false } : {}) })); });
  return out;
};
// ---------- 2D effects ----------
const FX = (key, draw, pos, s, extra = {}) => ({ key, draw, x: pos[0], y: pos[1], z: pos[2], s, blob: false, shadow: false, order: 5, ...extra });
const TXT = (key, txt, pos, s, col = '#fff6e0', ol = '#241726', size = 150, ex = {}) => FX(key + txt, (p) => { const g = p.g; g.font = `900 ${size}px Impact, "Arial Black", sans-serif`; { const w = g.measureText(txt).width; if (w > 520) { size = Math.floor(size * 520 / w); g.font = `900 ${size}px Impact, "Arial Black", sans-serif`; } } g.textAlign = 'center'; g.textBaseline = 'middle'; g.lineJoin = 'round'; if (ex.board) { /* placa de madeira fincada no chao (canal: texto em placas/objetos da cena) */ const w = Math.min(540, g.measureText(txt).width + 70), h = size * 1.5, y0 = 330 - h / 2; g.lineWidth = 12; g.strokeStyle = '#241726'; g.fillStyle = '#8a5a34'; for (const px of [300 - w * 0.3, 300 + w * 0.3]) { g.fillRect(px - 13, y0 + h - 6, 26, 975 - y0 - h); g.strokeRect(px - 13, y0 + h - 6, 26, 975 - y0 - h); } g.fillStyle = ex.board === true ? '#f3e2b4' : ex.board; g.beginPath(); g.roundRect(300 - w / 2, y0, w, h, 14); g.fill(); g.stroke(); g.lineWidth = 3; g.strokeStyle = 'rgba(90,60,30,.35)'; g.beginPath(); g.moveTo(300 - w / 2 + 14, y0 + h * 0.2); g.lineTo(300 + w / 2 - 14, y0 + h * 0.2); g.moveTo(300 - w / 2 + 14, y0 + h * 0.82); g.lineTo(300 + w / 2 - 14, y0 + h * 0.82); g.stroke(); g.fillStyle = col; g.fillText(txt, 300, 336); return; } g.lineWidth = 22; g.strokeStyle = ol; g.strokeText(txt, 300, 500); g.fillStyle = col; g.fillText(txt, 300, 500); }, pos, s, ex);
export const fxAt = (f, T) => { const out = [];
  for (const S of [SP(f)]) for (let e of (S.fx || [])) { if (f < e.a || f > e.b) continue; const t = qq((f - e.a) / Math.max(1, e.b - e.a), 2);
    if (e.follow !== undefined && S.actors && S.actors[e.follow]) { const A_ = S.actors[e.follow], p_ = moveAt(A_.at, A_.move, f), dir_ = A_.move && A_.move[0] ? Math.sign(A_.move[0][0] - A_.at[0]) || 1 : 1; e = { ...e, at: [p_[0] + (e.dx || 0) * dir_, e.at[1], p_[1] + (e.dz || 0)] }; }   /* efeito que acompanha quem corre (clarao no cano de quem atira correndo) */
    if (e.k === 'burst') out.push(FX('bu' + e.a + t, (p) => T.fxBurst(p, t, e.col || '#fff3b0', 12, 30, 220), e.at, e.s || 1));
    else if (e.k === 'map') { /* MAPA DIDATICO: corta para um mapa de pergaminho com alfinete e o nome do lugar, colado na frente da camera */
      const pop = M.back(ramp(f, e.a, e.a + 9)) * (1 - ramp(f, e.b - 6, e.b)); if (pop > 0.02) { const C = camAt(f); const fw = [C.look[0] - C.pos[0], C.look[1] - C.pos[1], C.look[2] - C.pos[2]]; const L = Math.hypot(...fw); const dd = Math.min(L * 0.55, 4); const hh = dd * Math.tan(C.fov * Math.PI / 360), s = 0.9 * (2 * hh * 0.5625) / 1.35 * (0.6 + 0.4 * pop);
        let hsh = 0; for (const ch of e.text) hsh = (hsh * 31 + ch.charCodeAt(0)) % 9973; const rr = (i) => ((Math.sin(hsh * 0.37 + i * 12.9898) * 43758.5453) % 1 + 1) % 1;
        out.push(FX('map' + e.text, (p) => { const g = p.g; g.lineJoin = 'round'; g.lineCap = 'round';
          g.fillStyle = '#f1dfb0'; g.strokeStyle = '#241726'; g.lineWidth = 12; g.beginPath(); g.roundRect(34, 170, 532, 660, 18); g.fill(); g.stroke();
          g.save(); g.beginPath(); g.roundRect(46, 182, 508, 520, 10); g.clip(); g.fillStyle = '#9fd0e6'; g.fillRect(46, 182, 508, 520);
          g.strokeStyle = 'rgba(255,255,255,.55)'; g.lineWidth = 4; for (let i = 0; i < 9; i++) { const y = 205 + i * 58, x = 70 + rr(i) * 380; g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + 18, y - 9, x + 36, y); g.stroke(); }
          if (e.geo) {   /* MAPA DE VERDADE: contorno real dos paises, o lugar em destaque e o alfinete no ponto certo */
            const G = e.geo, hl = new Set(G.hl);
            G.polys.forEach((pp, i) => { if (hl.has(i)) return; g.beginPath(); for (let k = 0; k < pp.length; k += 2) { const x = 46 + pp[k], y = 182 + pp[k + 1]; k ? g.lineTo(x, y) : g.moveTo(x, y); } g.closePath(); g.fillStyle = '#ece0b8'; g.fill(); g.strokeStyle = '#8a7a5a'; g.lineWidth = 2.5; g.stroke(); });
            G.polys.forEach((pp, i) => { if (!hl.has(i)) return; g.beginPath(); for (let k = 0; k < pp.length; k += 2) { const x = 46 + pp[k], y = 182 + pp[k + 1]; k ? g.lineTo(x, y) : g.moveTo(x, y); } g.closePath(); g.fillStyle = '#9fcf6a'; g.fill(); g.strokeStyle = '#241726'; g.lineWidth = 5; g.stroke(); });
            const px = 46 + G.pin[0], py = 182 + G.pin[1]; g.restore();
            g.fillStyle = '#d8282f'; g.strokeStyle = '#241726'; g.lineWidth = 6; g.beginPath(); g.arc(px, py - 48, 26, Math.PI, 0); g.lineTo(px, py); g.closePath(); g.fill(); g.stroke(); g.fillStyle = '#fff6e0'; g.beginPath(); g.arc(px, py - 50, 9, 0, 6.2832); g.fill();
          } else {
          const blob = (cx, cy, R, k) => { g.beginPath(); for (let i = 0; i <= 14; i++) { const a = i / 14 * 6.2832, r = R * (0.72 + 0.5 * rr(k * 20 + i % 14)); const x = cx + Math.cos(a) * r * 1.15, y = cy + Math.sin(a) * r * 0.9; i ? g.lineTo(x, y) : g.moveTo(x, y); } g.closePath(); g.fillStyle = '#b9d98a'; g.fill(); g.strokeStyle = '#241726'; g.lineWidth = 7; g.stroke(); };
          blob(300, 440, 170, 1); blob(120 + rr(3) * 60, 260, 62, 2); blob(470, 610, 54, 3);
          g.strokeStyle = '#7fa860'; g.lineWidth = 5; for (let i = 0; i < 5; i++) { const x = 220 + rr(40 + i) * 170, y = 380 + rr(50 + i) * 130; g.beginPath(); g.moveTo(x - 14, y + 8); g.lineTo(x, y - 12); g.lineTo(x + 14, y + 8); g.stroke(); }
          g.setLineDash([14, 12]); g.strokeStyle = '#b3262d'; g.lineWidth = 6; g.beginPath(); g.moveTo(90, 650); g.quadraticCurveTo(160, 470, 300, 430); g.stroke(); g.setLineDash([]); g.restore();
          g.fillStyle = '#d8282f'; g.strokeStyle = '#241726'; g.lineWidth = 6; g.beginPath(); g.arc(300, 392, 26, Math.PI, 0); g.lineTo(300, 440); g.closePath(); g.fill(); g.stroke(); g.fillStyle = '#fff6e0'; g.beginPath(); g.arc(300, 390, 9, 0, 6.2832); g.fill();
          }
          g.strokeStyle = '#241726'; g.lineWidth = 5; g.beginPath(); g.arc(500, 240, 26, 0, 6.2832); g.stroke(); g.beginPath(); g.moveTo(500, 206); g.lineTo(508, 240); g.lineTo(500, 274); g.lineTo(492, 240); g.closePath(); g.fillStyle = '#241726'; g.fill();
          let size = 84; g.font = `900 ${size}px Impact, "Arial Black", sans-serif`; const w = g.measureText(e.text).width; if (w > 470) { size = Math.floor(size * 470 / w); g.font = `900 ${size}px Impact, "Arial Black", sans-serif`; } g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = '#3a2416'; g.fillText(e.text, 300, 766);
        }, [C.pos[0] + fw[0] / L * dd, C.pos[1] + fw[1] / L * dd - 0.72 * s, C.pos[2] + fw[2] / L * dd], s, { front: true, shadow: false, order: 9 })); } }   /* mapa um pouco acima do centro: nao cobre a legenda */
    else if (e.k === 'birds') { /* bando de passaros cruzando o ceu (silhuetas em "m" batendo asa) */ const n = e.n || 5, ph = Math.floor(f / 5) % 4, dir = e.dir || 1, span = 30, x = (e.at ? e.at[0] : 0) + dir * (((f - e.a) * 0.07 + (e.off || 0)) % span - span / 2);
      out.push(FX('bd' + n + ph + dir, (p) => { const g = p.g; g.strokeStyle = '#241726'; g.lineCap = 'round'; g.lineJoin = 'round'; for (let i = 0; i < n; i++) { const bx = 300 + dir * (-(i % 2 ? 1 : -1) * Math.ceil(i / 2) * 120 - Math.ceil(i / 2) * 50) * 0.9, by = 380 + Math.ceil(i / 2) * 70 + (i * 37 % 23), w = 62 - (i % 3) * 9, up = [30, 8, -16, 8][(ph + i) % 4]; g.lineWidth = 11; g.beginPath(); g.moveTo(bx - w, by - up); g.quadraticCurveTo(bx - w * 0.45, by - up * 0.2 - 9, bx, by); g.quadraticCurveTo(bx + w * 0.45, by - up * 0.2 - 9, bx + w, by - up); g.stroke(); } }, [x, (e.at ? e.at[1] : DECK + 15) + Math.sin(f * 0.03) * 0.6, e.at ? e.at[2] : -38], e.s || 13, { shadow: false, order: 1 })); }
    else if (e.k === 'flash') out.push(FX('fl' + e.a + t, (p) => { const g = p.g, k = t < 0.35 ? t / 0.35 : 1 - (t - 0.35) / 0.65 * 0.6, R = 150 * (0.45 + 0.55 * k); const star = (r, n, col) => { g.beginPath(); for (let i = 0; i < n * 2; i++) { const a = Math.PI * i / n + 0.3, rr = i % 2 ? r * 0.45 : r; g.lineTo(300 + rr * Math.cos(a), 250 + rr * Math.sin(a)); } g.closePath(); g.fillStyle = col; g.fill(); };
      g.lineJoin = 'round'; g.lineWidth = 16; g.strokeStyle = '#3a1c14'; star(R, 7, '#ff8a1e'); g.stroke(); star(R * 0.68, 7, '#ffd23a'); star(R * 0.34, 6, '#fffbe6'); }, e.at, e.s || 1, { keepColor: true }));   // clarao de tiro cartunesco
    else if (e.k === 'puff') out.push(FX('pf' + e.a + t, (p) => { p.g.translate(150, 700); T.fxPuff(p, t); }, e.at, e.s || 1));
    else if (e.k === 'dust') out.push(FX('du' + e.a + t, (p) => T.fxDust(p, t, e.col || '#d8c8a0'), e.at, e.s || 1));
    else if (e.k === 'splash') out.push(FX('sp' + e.a + t, (p) => T.fxSplash(p, t), e.at, e.s || 1));
    else if (e.k === 'stars') out.push(FX('st' + e.a + t, (p) => T.fxStars(p, t), e.at, e.s || 1));
    else if (e.k === 'creak') out.push(FX('cr' + e.a + t, (p) => T.fxCreak(p, t), e.at, e.s || 1));
    else if (e.k === 'ring') out.push(FX('rg' + e.a + t, (p) => T.fxRing(p, t), e.at, e.s || 1));
    else if (e.k === 'text') { const pop = ramp(f, e.a, e.a + 12); let at = e.at, sc = 1, fr = {}; if (e.up !== undefined) { const C = camAt(f); const fw = [C.look[0] - C.pos[0], C.look[1] - C.pos[1], C.look[2] - C.pos[2]]; const L = Math.hypot(...fw); const dd = L * 0.8; const hh = dd * Math.tan(C.fov * Math.PI / 360); const nlen = e.text.length, fw_ = 2 * hh * 0.5625, frac = Math.min(0.8, 0.12 + 0.055 * nlen), est = Math.min(0.867, 0.116 * nlen); const sb = frac * fw_ / (1.35 * est); at = [C.pos[0] + fw[0] / L * dd, C.pos[1] + fw[1] / L * dd + e.up * hh - 1.07 * sb * M.back(pop), C.pos[2] + fw[2] / L * dd]; sc = sb / (e.s || 1.2); fr = { front: true }; } out.push(TXT('tx' + (e.board ? 'b' : ''), e.text, at, (e.board ? 0.9 + 0.1 * M.back(pop) : M.back(pop)) * (e.s || 1.2) * sc, e.col || '#fff6e0', e.ol || '#241726', e.size || 150, { ...(e.roll ? { roll: e.roll } : {}), ...(e.board ? { board: e.board, shadow: true } : {}), ...fr })); } }
  return out; };
