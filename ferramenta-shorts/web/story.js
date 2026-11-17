const TIMING = {"total": 657, "words": [[5, 8, "Um"], [8, 16, "homem"], [16, 27, "dirigia"], [27, 39, "tranquilo"], [39, 46, "pela"], [46, 61, "avenida,"], [68, 77, "quando"], [77, 82, "viu"], [82, 92, "algo"], [92, 106, "imposs\u00edvel."], [131, 141, "\"Isso"], [141, 146, "n\u00e3o"], [146, 151, "pode"], [151, 160, "estar"], [160, 170, "certo\","], [178, 184, "disse"], [184, 189, "o"], [189, 201, "guarda,"], [208, 218, "co\u00e7ando"], [218, 223, "a"], [223, 234, "cabe\u00e7a."], [259, 268, "Ent\u00e3o"], [268, 276, "ele"], [276, 284, "entrou"], [284, 289, "na"], [289, 301, "floresta,"], [309, 314, "onde"], [314, 319, "os"], [319, 333, "animais"], [333, 352, "observavam"], [352, 357, "em"], [357, 367, "sil\u00eancio."], [393, 398, "No"], [398, 409, "sal\u00e3o"], [409, 414, "do"], [414, 425, "pal\u00e1cio,"], [432, 441, "todos"], [441, 459, "esperavam"], [459, 464, "a"], [464, 477, "resposta."], [503, 518, "Acontece"], [518, 523, "que"], [523, 528, "a"], [528, 543, "resposta"], [543, 552, "era"], [552, 562, "simples."], [588, 596, "Ningu\u00e9m"], [596, 604, "tinha"], [604, 617, "olhado"], [617, 625, "para"], [625, 634, "cima."]], "phrases": [[5, 61, "Um homem dirigia tranquilo pela avenida,"], [68, 106, "quando viu algo imposs\u00edvel."], [131, 170, "\"Isso n\u00e3o pode estar certo\","], [178, 201, "disse o guarda,"], [208, 234, "co\u00e7ando a cabe\u00e7a."], [259, 301, "Ent\u00e3o ele entrou na floresta,"], [309, 367, "onde os animais observavam em sil\u00eancio."], [393, 425, "No sal\u00e3o do pal\u00e1cio,"], [432, 477, "todos esperavam a resposta."], [503, 562, "Acontece que a resposta era simples."], [588, 634, "Ningu\u00e9m tinha olhado para cima."]]};
// shared spec helpers (prepended to every spec)
const DK0 = 6;
const pp = (X, outfit, v, dx, z, expr = 'smile', ex = {}) => ({ outfit, v, at: [X + dx, z], pose: 'stand', look: dx > 0 ? -0.4 : 0.4, expr, ...ex });
const mv = (X, outfit, v, dx0, dx1, z, a, b, ex = {}) => ({ outfit, v, at: [X + dx0, z], move: [[X + dx1, z], a, b], pose: 'march', speed: 0.034, expr: 'neutral', ...ex });
const txt = (X, a, b, text, col = '#fff6e0', ol = '#27408b', h = 4.4, ex = {}) => ({ k: 'text', a, b, up: 0.42, at: [X, DK0 + h, 3.5], text, s: 1.3, col, ol, size: 120, ...ex });
const ctr = (o, X) => { let A = (o.actors || []).filter((q) => q.at); const P_ = A.filter((q) => q.outfit); if (A.length > 4 && P_.length) A = P_; if (!A.length) return [0, 0]; return [A.reduce((s, q) => s + (q.at[0] - X), 0) / A.length, A.reduce((s, q) => s + q.at[1], 0) / A.length]; };
// standard shot: gentle push-in on a group; hero checks use 'any'/'none'
const S = (id, a, b, X, light, o = {}) => ({ id, a, b, light, trans: o.trans, nocut: o.nocut, vary: o.vary, lightMod: o.lightMod, exp: o.exp, hero: o.hero || (o.actors && o.actors.some((q) => q.outfit) ? { hero: 'any', frame: 'medium', minH: 0.06 } : { hero: 'none' }), weather: o.wx,
  cam: [{ f: a, at: [X + (o.cx ?? ctr(o, X)[0]), DK0 + (o.h || (o.actors && o.actors.length ? 2.3 : 1.8)), o.cz ?? ctr(o, X)[1]], d: o.d0 || 11, az: o.az0 ?? -6, el: o.el ?? 4, fov: o.fov || 46 }, { f: b, at: [X + (o.cx ?? ctr(o, X)[0]), DK0 + (o.h || (o.actors && o.actors.length ? 2.3 : 1.8)), o.cz ?? ctr(o, X)[1]], d: o.d1 || 8.5, az: o.az1 ?? 4, el: o.el ?? 4, fov: o.fov || 46 }],
  actors: o.actors || [], props: (o.props || []).map((p, i) => (p.y === undefined && !p.move && p.drop !== false && !globalThis.NOGRAV ? { ...p, y: dropY(a + 2 + i * 3, DK0, 2.4 + 0.6 * (i % 3)) } : p)), fx: o.fx || [] });

// gravity: props fall into place at the start of the shot and bounce (restitution e)
const dropY = (a, y1 = DK0, H = 3.2, e = 0.34, g = 22) => (f) => { let t = (f - a) / 30; if (t <= 0) return y1 + H; const t0 = Math.sqrt(2 * H / g); if (t < t0) return y1 + H - 0.5 * g * t * t; t -= t0; let v = g * t0 * e; for (let k = 0; k < 4; k++) { const T = 2 * v / g; if (t < T) return y1 + v * t - 0.5 * g * t * t; t -= T; v *= e; } return y1; };

// ---- timing anchors: shots / texts / effects are tied to WORDS of the narration (any language, any voice) ----
const _nrm = (s) => String(s).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]/g, '');
const WI = (token, nth = 1) => { let c = 0; const T = TIMING.words; for (let i = 0; i < T.length; i++) if (_nrm(T[i][2]) === _nrm(token) && ++c === nth) return i; throw new Error('anchor word not found: ' + token + ' #' + nth); };
const W = (token, nth = 1, off = 0) => TIMING.words[WI(token, nth)][0] + off;     // frame where the word starts
const WE = (token, nth = 1, off = 0) => TIMING.words[WI(token, nth)][1] + off;    // frame where the word ends
const TOTAL_F = () => TIMING.total || Math.round(TIMING.words[TIMING.words.length - 1][1] + 40);   // frames of the voice track
// Teste de Cenarios -- GERADO por mkvideo.py a partir de videos/teste_cenarios/beats.json (edite o beats.json, nao este arquivo)
const X = 12000, DK = 6; const X_hall = 8000; const X_jungle = 6000;
const WS = (i, off = 0) => TIMING.words[Math.min(i, TIMING.words.length - 1)][0] + off;   // frame em que a palavra de indice i comeca
const A = [0, WS(10, -3), WS(21, -3), WS(32, -3), WS(40, -3), TOTAL_F()];
const SPEC = {
  id: "teste_cenarios", total: TOTAL_F(), sets: ["street", "hall", "jungle"], setx: { street: X, hall: X_hall, jungle: X_jungle },
  outfits: { CID: (v = 0, e = {}) => ({ _id: "cid", jacket: "#3b6fb5", pants: "#2d3550", boots: "#2a2218", hat: "hair", hair: "#4a3020", skin: ["#ffe2c2", "#f5c9a0", "#ecd0b6", "#c99067"][v % 4], ...(v % 7 === 4 ? { glasses: true } : {}), ...(v % 7 === 5 || v % 7 === 6 ? { beard: ['#3a2a1f', '#6b4a2a', '#8a8a86'][v % 3] } : {}), ...e }),
    GUA: (v = 0, e = {}) => ({ _id: "gua", jacket: "#2f4aa0", pants: "#1f2a50", boots: "#1b1b1f", hat: "cap", cap: "#1f2a50", skin: ["#ffe2c2", "#f5c9a0", "#ecd0b6", "#c99067"][v % 4], ...(v % 7 === 4 ? { glasses: true } : {}), ...(v % 7 === 5 || v % 7 === 6 ? { beard: ['#3a2a1f', '#6b4a2a', '#8a8a86'][v % 3] } : {}), ...e }) },
  assets: ["vehicles/car"],
  kicks: [], flashes: [],
  shots: [
    S('b0', A[0], A[1] - 1, X, "day", { h: 2.5, d0: 9.0, d1: 7.4, hero: { hero: 'none' }, actors: [pp(X, "CID", 1, 0.0, 2.4, "neutral"), { outfit: "CID", v: 0, at: [X + -7, 0.85], move: [[X + 7, 0.85], A[0], A[1] - 1, 'lin'], pose: 'stand', expr: "smile", s: 0.8 }], props: [{ asset: "vehicles/car", at: [X + -7, 1.2], move: [[X + 7, 1.2], A[0], A[1] - 1, 'lin'], s: 1.0, bob: 0.03 }] }),
    S('b1', A[1], A[2] - 1, X, "day", { h: 2.3, d0: 7.0, d1: 5.8, hero: { hero: 'any', frame: 'medium', minH: 0.07 }, actors: [pp(X, "CID", 4, -1.15, 2.4, "nervous"), pp(X, "GUA", 5, 1.15, 2.0, "stern")] }),
    { ...S('b2', A[2], A[3] - 1, X_jungle, "day", { h: 2.8, d0: 30, d1: 24, el: 14, fov: 46, cx: 0.0, cz: -1.5, hero: { hero: 'none', wide: true }, vary: false, actors: [pp(X_jungle, "CID", 0, 0.0, -0.4, "shock"), { animal: "bear", at: [X_jungle + 3.0, 0.5], state: "stand", s: 1.0, flip: true, seed: 1 }, pp(X_jungle, "CID", 0, -8.05, 0.84, "neutral", { look: -0.25, seed: 0 }), pp(X_jungle, "CID", 1, -5.79, 1.32, "neutral", { look: 0.25, seed: 1 }), pp(X_jungle, "CID", 2, -3.53, 0.96, "neutral", { look: 0.0, seed: 2 }), pp(X_jungle, "CID", 3, -2.26, 1.44, "neutral", { look: 0.15, seed: 3 }), pp(X_jungle, "CID", 0, 0.0, 1.08, "neutral", { look: -0.25, seed: 0 }), pp(X_jungle, "CID", 1, 2.26, 1.56, "neutral", { look: 0.25, seed: 1 })] }), nocut: true },
    { ...S('b3', A[3], A[4] - 1, X_hall, "day", { h: 2.6, d0: 27.0, d1: 22.0, el: 14, fov: 46, az0: -38, az1: 32, cx: 0.0, cz: -1.5, hero: { hero: 'none', wide: true }, vary: false, actors: [pp(X_hall, "GUA", 0, -2.1, -0.4, "stern"), pp(X_hall, "CID", 6, 0.0, 0.2, "smile"), pp(X_hall, "GUA", 1, 2.1, -0.8, "neutral"), pp(X_hall, "GUA", 0, -8.05, 0.84, "neutral", { look: -0.25, seed: 0 }), pp(X_hall, "CID", 1, -5.79, 1.32, "neutral", { look: 0.25, seed: 1 }), pp(X_hall, "GUA", 2, -3.53, 0.96, "neutral", { look: 0.0, seed: 2 }), pp(X_hall, "GUA", 3, -2.26, 1.44, "neutral", { look: 0.15, seed: 3 }), pp(X_hall, "CID", 0, 0.0, 1.08, "neutral", { look: -0.25, seed: 0 }), pp(X_hall, "GUA", 1, 2.26, 1.56, "neutral", { look: 0.25, seed: 1 }), pp(X_hall, "GUA", 2, 3.53, 1.2, "neutral", { look: 0.0, seed: 2 }), pp(X_hall, "CID", 3, 5.79, 0.84, "neutral", { look: 0.15, seed: 3 }), pp(X_hall, "GUA", 0, 8.05, 1.32, "neutral", { look: -0.25, seed: 0 }), pp(X_hall, "GUA", 1, -6.88, -1.14, "neutral", { look: 0.25, seed: 1 }), pp(X_hall, "CID", 2, -4.62, -0.66, "neutral", { look: 0.0, seed: 2 }), pp(X_hall, "GUA", 3, -3.35, -1.02, "neutral", { look: 0.15, seed: 3 })] }), nocut: true },
    { ...S('b4', A[4], A[5] - 1, X, "day", { h: 2.6, d0: 15.0, d1: 36.0, el: 12, fov: 46, cx: 0.0, cz: -1.5, hero: { hero: 'none', wide: true }, vary: false, actors: [pp(X, "CID", 0, -1.15, -0.4, "grin"), pp(X, "GUA", 0, 1.15, 0.2, "pained"), pp(X, "CID", 0, -8.05, 0.84, "neutral", { look: -0.25, seed: 0 }), pp(X, "GUA", 1, -5.79, 1.32, "neutral", { look: 0.25, seed: 1 }), pp(X, "CID", 2, -3.53, 0.96, "neutral", { look: 0.0, seed: 2 }), pp(X, "GUA", 3, -2.26, 1.44, "neutral", { look: 0.15, seed: 3 }), pp(X, "CID", 0, 0.0, 1.08, "neutral", { look: -0.25, seed: 0 }), pp(X, "GUA", 1, 2.26, 1.56, "neutral", { look: 0.25, seed: 1 })] }), nocut: true }
  ],
};
SPEC.fit = {"b0":1.761,"b0~1":3.104,"b1":1.572,"b1~1":1.254};
// ===== STORY RUNTIME (generic): turns a declarative SPEC (stories/<id>.spec.js, concatenated before this file) into the story.js interface the engine expects =====
import { camFromKeys, clamp, lerp, ramp, q, blinkAt, idle, M } from './motion.js';
export const FPS = 30, TOTAL = SPEC.total, DECK = 6;
export const SPEC_DEBUG = SPEC;
// ---------- auto sub-cuts: long shots are split into ~2.2 s sub-takes, each with a different camera setup (Ricks Clips rhythm: new angle every phrase) ----------
const VARS = [{ az: 0, el: 0, d: 1, fov: 0, roll: 0 }, { az: 26, el: -7, d: 0.9, fov: 2, roll: -2 }, { az: -22, el: 9, d: 1.08, fov: 0, roll: 2.5 }, { az: 12, el: -3, d: 0.84, fov: -2, roll: 0 }, { az: -30, el: 15, d: 1.18, fov: 3, roll: -3.5 }, { az: 18, el: -9, d: 0.96, fov: 1, roll: 3 }];
const lk = (a, b, t) => ({ ...a, at: [0, 1, 2].map((i) => a.at[i] + (b.at[i] - a.at[i]) * t), d: a.d + (b.d - a.d) * t, az: (a.az ?? 0) + ((b.az ?? 0) - (a.az ?? 0)) * t, el: (a.el ?? 8) + ((b.el ?? 8) - (a.el ?? 8)) * t, fov: (a.fov ?? 34) + ((b.fov ?? 34) - (a.fov ?? 34)) * t });
SPEC.shots.forEach((s, i, A) => { if (i === 0) { s.trIn = null; return; } const ty = s.trans ?? (s.cut === false ? 'cut' : (A[i - 1].light !== s.light ? (SPEC.trans ?? 'dissolve') : 'cut')); s.trIn = { type: ty, N: ty === 'dissolve' ? (SPEC.dissolveN ?? 10) : ty === 'push' ? 4 : 0 }; });
if (SPEC.autocut !== false) SPEC.shots = SPEC.shots.flatMap((s) => { const len = s.b - s.a + 1, n = Math.max(1, Math.round(len / (SPEC.cutLen ?? 66))); if (n < 2 || !s.cam || s.cam.length < 2 || !s.cam[0].at || s.nocut) return [s];
  const out = [], k0 = s.cam[0], k1 = s.cam[s.cam.length - 1]; let a = s.a;
  for (let j = 0; j < n; j++) { const b = j === n - 1 ? s.b : Math.round(s.a + (j + 1) * len / n) - 1, v = VARS[((s.a / 66 | 0) + j) % VARS.length]; const t0 = (a - s.a) / Math.max(1, len - 1), t1 = (b - s.a) / Math.max(1, len - 1);
    const par = j % 2 ? -1 : 1; const mk = (t, f, s) => { const k0_ = lk(k0, k1, t); const azr = ((k0_.az ?? 0) + v.az * 0.9) * Math.PI / 180, amt = (s - 0.5) * 0.16 * k0_.d * par, dd = 1 + (s - 0.5) * 0.16 * (j % 2 ? 1 : -1);
      const k = { ...k0_, at: [k0_.at[0] + Math.cos(azr) * amt, k0_.at[1], k0_.at[2] - Math.sin(azr) * amt], d: k0_.d * dd }; return { ...k, f, az: k.az + v.az * 0.9, el: Math.max(-4, k.el + v.el), d: k.d * v.d, fov: k.fov + v.fov, roll: (k.roll || 0) + v.roll }; };
    out.push({ ...s, id: j === 0 ? s.id : s.id + '~' + j, a, b, cut: j === 0 ? s.cut : false, glide: j > 0, cam: [mk(t0, a, 0), mk(t1, b, 1)], trIn: j === 0 ? s.trIn : { type: 'glide', N: 0 } }); a = b + 1; }
  return out; });
const SETNEEDS = { outback: ['nature/rocks', 'nature/picket_fence', 'buildings/barn', 'buildings/windmill', 'buildings/house_small', 'nature/bush'], countryside: ['nature/tree_oak', 'nature/haybale', 'buildings/house_small', 'buildings/house_two', 'buildings/church', 'buildings/barn', 'buildings/windmill'], arctic: ['nature/rocks'], palace: ['nature/tree_palm', 'buildings/castle_tower', 'buildings/house_two', 'buildings/church'], jungle: ['nature/bush'], medieval: ['buildings/house_small', 'buildings/castle_tower', 'buildings/church', 'nature/tree_oak', 'nature/fountain'], street: ['buildings/shop', 'buildings/house_two', 'buildings/apartment', 'buildings/house_blue', 'nature/lamppost'], harbor: ['crate', 'ship', 'buildings/lighthouse'], mountain: ['nature/rocks', 'war/sandbags', 'buildings/castle_tower', 'buildings/church'], hall: [], stadium: [] };   // assets each set builder needs (auto-loaded)
export const ASSETS = [...new Set([...(SPEC.assets || []), ...(SPEC.sets || []).flatMap((s) => SETNEEDS[s] || [])])].concat(['bear', 'horse'].filter((n) => JSON.stringify(SPEC.shots).includes('"animal":"' + n + '"'))).concat(JSON.stringify(SPEC.shots).includes('"bird":"emu"') ? ['emu'] : []), SETS_USED = SPEC.sets || [], SETX = SPEC.setx || {};
export const SHOTS = SPEC.shots.map((s) => ({ id: s.id, a: s.a, b: s.b, light: s.light, tr: s.trIn || null }));
export const HEROES = Object.fromEntries(SPEC.shots.map((s) => [s.id, s.hero || { hero: 'any', frame: 'medium' }]));
export const shotAt = (f) => SHOTS.find((s) => f >= s.a && f <= s.b) || SHOTS[SHOTS.length - 1];
let FORCE = null; if (typeof window !== 'undefined') window.__force = (i) => { FORCE = i; };
const SP = (f) => (FORCE !== null ? SPEC.shots[FORCE] : (SPEC.shots.find((s) => f >= s.a && f <= s.b) || SPEC.shots[SPEC.shots.length - 1]));
export const smooth = M.smooth;
export const fitD = (h, frac, fov) => h / (frac * 2 * Math.tan(fov * Math.PI / 360));   // camera distance so an object of height h fills `frac` of the frame height
// ---------- lights (shared presets; a story may add/override in SPEC.lights) ----------
const LIB_LIGHTS = {
  dawn: { az: 95, el: 16, sky: '#ffdca8', ground: '#7a6a4a', hemi: 1.1, sun: '#ffc98a', sunI: 2.9, fog: '#ffd8a8', fogNear: 90, fogFar: 650, skyTop: '#7ea4e0', skyHor: '#ffd6a0', sunDisc: '#fff0c8', sunSize: 0.004, sat: 1.15, gain: '#fff1e0', vig: 0.26, shadowExt: 18, rimC: '#8fb4ff', rimI: 0.55, glow: 0.9, shafts: 0.5 },
  day: { az: 140, el: 50, sky: '#c9d0f6', ground: '#8a8262', hemi: 1.2, sun: '#fff3dc', sunI: 2.5, fog: '#cfe0f2', fogNear: 120, fogFar: 800, skyTop: '#3f80d4', skyHor: '#c9def4', sat: 1.12, vig: 0.2, shadowExt: 22, rimC: '#bcd8ff', rimI: 0.3 },
  noon: { az: 160, el: 68, sky: '#d9defa', ground: '#a29a72', hemi: 1.3, sun: '#fffaf0', sunI: 2.7, fog: '#dfeaf6', fogNear: 150, fogFar: 900, skyTop: '#3a86e0', skyHor: '#cfe4f8', sat: 1.12, vig: 0.18, shadowExt: 22, rimC: '#cfe2ff', rimI: 0.25 },
  tense: { az: 8, el: 9, sky: '#b090b8', ground: '#6a4c40', hemi: 0.95, sun: '#ff8a50', sunI: 3.0, fog: '#e8906a', fogNear: 70, fogFar: 600, skyTop: '#5a4a9a', skyHor: '#ff9a62', sunDisc: '#ffe0b0', sunSize: 0.0045, sat: 1.18, gain: '#ffe6d2', vig: 0.32, shadowExt: 26, rimC: '#6a7cff', rimI: 0.75, glow: 1.0 },
  storm: { az: 200, el: 30, sky: '#8f9db8', ground: '#4a5060', hemi: 1.0, sun: '#d8e2f0', sunI: 1.9, fog: '#8f9db4', fogNear: 60, fogFar: 520, skyTop: '#46567a', skyHor: '#a4b2c8', sat: 1.0, vig: 0.34, shadowExt: 30, rimC: '#a0c0ff', rimI: 0.4 },
  overcast: { az: 180, el: 45, sky: '#c8d0da', ground: '#7a7a72', hemi: 1.25, sun: '#e8eef4', sunI: 1.4, fog: '#c4ccd6', fogNear: 60, fogFar: 520, skyTop: '#8a98ac', skyHor: '#c9d2dc', sat: 0.95, vig: 0.28, shadowExt: 24, rimC: '#bcd0ee', rimI: 0.3 },
  night: { az: 220, el: 38, sky: '#2c3a66', ground: '#1c2440', hemi: 0.55, sun: '#8fa8ff', sunI: 1.1, fog: '#101a3a', fogNear: 40, fogFar: 420, skyTop: '#060c24', skyHor: '#1c2c5a', sat: 1.0, gain: '#b8c8ff', vig: 0.4, shadowExt: 24, rimC: '#6a8aff', rimI: 0.7 },
  deck: { az: 150, el: 40, sky: '#d6e6f8', ground: '#8a7a5a', hemi: 1.2, sun: '#fff1d4', sunI: 2.5, fog: '#d3e3f2', fogNear: 100, fogFar: 700, skyTop: '#4d88d8', skyHor: '#cfe2f5', sat: 1.1, vig: 0.24, shadowExt: 22, rimC: '#bcd8ff', rimI: 0.3 },
  study: { az: 250, el: 38, sky: '#ffe9c4', ground: '#8a6a4a', hemi: 1.15, sun: '#ffe2b0', sunI: 2.1, fog: '#7a5a46', fogNear: 60, fogFar: 400, skyTop: '#3a2a36', skyHor: '#5a3a3a', sat: 1.12, gain: '#fff0dc', vig: 0.34, shadowExt: 18, rimC: '#ffc880', rimI: 0.55, shafts: 0.55 },
  dusk: { az: 275, el: 7, sky: '#b498c8', ground: '#5a4658', hemi: 0.95, sun: '#ff9060', sunI: 2.8, fog: '#d88a78', fogNear: 80, fogFar: 600, skyTop: '#5a4a94', skyHor: '#ff9a6a', sunDisc: '#ffd8a0', sunSize: 0.0045, sat: 1.2, gain: '#ffe2d0', vig: 0.34, shadowExt: 26, rimC: '#7a8cff', rimI: 0.65, glow: 1.0 },
  arctic: { exp: 0.80, az: 200, el: 12, sky: '#c9b8ec', ground: '#7a8cc8', hemi: 0.9, sun: '#ffd9a8', sunI: 3.1, fog: '#f2d2c8', fogNear: 120, fogFar: 800, skyTop: '#3a58e0', skyHor: '#ffc3a0', sunDisc: '#fff0c8', sunSize: 0.006, glow: 0.9, sat: 1.9, gain: '#fff0e0', vig: 0.24, shadowExt: 26, rimC: '#ffc890', rimI: 0.6, shafts: 0.6, gsel: 1 },
  golden: { az: 225, el: 30, sky: '#cdb0e8', ground: '#a8785a', hemi: 1.55, sun: '#ffd8a0', sunI: 2.6, fog: '#f4c8a0', fogNear: 120, fogFar: 800, skyTop: '#6a5aa8', skyHor: '#ffb070', sunDisc: '#fff0c0', sunSize: 0.006, glow: 0.8, sat: 1.1, gain: '#fff2e0', vig: 0.26, shadowExt: 26, rimC: '#ffc890', rimI: 0.6, shafts: 0.6 },
  desert: { az: 150, el: 62, sky: '#e8dcf2', ground: '#b88a5a', hemi: 1.2, sun: '#fff0d0', sunI: 3.0, fog: '#f0dcb8', fogNear: 120, fogFar: 800, skyTop: '#4f94e0', skyHor: '#f6e4c0', sat: 1.15, gain: '#fff2de', vig: 0.24, shadowExt: 24, rimC: '#ffe0b0', rimI: 0.3 },
  grave: { az: 280, el: 6, sky: '#c0a0c8', ground: '#5a4a58', hemi: 1.0, sun: '#ffa070', sunI: 2.6, fog: '#e0988a', fogNear: 80, fogFar: 600, skyTop: '#4a4090', skyHor: '#ffa878', sunDisc: '#ffe0b0', sunSize: 0.005, sat: 1.2, gain: '#ffe6d6', vig: 0.36, shadowExt: 20, rimC: '#8a9cff', rimI: 0.65, glow: 1.0 },
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
  if (S.glide && si > 0 && f < S.a + (SPEC.glideN ?? 26)) { const G = SPEC.glideN ?? 26, ps = SPEC.shots[si - 1], pc = camFromKeys(CAMKEYS[si - 1], ps.b, { creep: ps.creep ?? SPEC.creep ?? 0.0045, kicks: [] }); const x = Math.min(1, Math.max(0, (f - S.a + 1) / (G + 1))), t = x * x * x * (x * (x * 6 - 15) + 10); const L3 = (p, q) => [0, 1, 2].map((i) => p[i] + (q[i] - p[i]) * t);
    c = { ...c, pos: L3(pc.pos, c.pos), look: L3(pc.look, c.look), fov: pc.fov + (c.fov - pc.fov) * t, roll: (pc.roll || 0) + ((c.roll || 0) - (pc.roll || 0)) * t }; }
  { const kf = (typeof window !== 'undefined' && window.KFIT && window.KFIT[S.id]) || (SPEC.fit && SPEC.fit[S.id]) || 1; if (kf !== 1) c.pos = [c.look[0] + (c.pos[0] - c.look[0]) * kf, c.look[1] + (c.pos[1] - c.look[1]) * kf, c.look[2] + (c.pos[2] - c.look[2]) * kf]; }
  { const k = SPEC.lens ?? 1.32; if (k !== 1) { const f2 = Math.min(78, c.fov * k), q = Math.tan(c.fov * Math.PI / 360) / Math.tan(f2 * Math.PI / 360); c.pos = [c.look[0] + (c.pos[0] - c.look[0]) * q, c.look[1] + (c.pos[1] - c.look[1]) * q, c.look[2] + (c.pos[2] - c.look[2]) * q]; c.fov = f2; } }
  const cut = CUTS.find((cf) => f >= cf && f < cf + 4), fl = (SPEC.flashes || []).find((x) => f >= x.f && f < x.f + (x.n || 5));
  { const nx = SPEC.shots[si + 1], M_ = 7, ZM = SPEC.pushZoom ?? 2.6, e01 = (t) => { t = Math.min(1, Math.max(0, t)); return t * t * (3 - 2 * t); }; let z = 1, zb = 0;
    if (nx && nx.trIn && nx.trIn.type === 'push' && f >= nx.a - M_) { const t = e01((f - (nx.a - M_)) / M_); z *= 1 + (ZM - 1) * t; zb = Math.max(zb, t); }
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
const G3D = ['bear', 'horse']; const is3 = (a) => G3D.includes(a.animal) || a.bird === 'emu';
export const worldAt = (f) => {
  const S = SP(f), W = { props: [], weather: { wind: 0.5, dx: 1, dz: 0.3, ...(typeof S.weather === 'function' ? S.weather(f) : S.weather || {}) } };
  W.weather.wind = Math.max(0, (W.weather.wind ?? 0.5) + (S.light === 'study' ? 0 : 0.1 * Math.sin(f / 30 * 0.5) + 0.06 * Math.sin(f / 30 * 1.7)));
  for (const p of (S.props || [])) { if (p.a !== undefined && (f < p.a || f > p.b)) continue; const base = p.at, pos = moveAt(base, p.move, f), prev = moveAt(base, p.move, f - 1), dx = pos[0] - prev[0], dz = pos[1] - prev[1]; const sp = Math.hypot(dx, dz) * 30; const dir = p.move ? Math.atan2(pos[0] - base[0], pos[1] - base[1]) : 0;
    const tw = typeof p.turret === 'function' ? p.turret(f) : p.turret; W.props.push({ sy: typeof p.sy === 'function' ? p.sy(f) : p.sy, asset: p.asset, x: pos[0], z: pos[1], y: typeof p.y === 'function' ? p.y(f) : (p.y ?? DECK), ry: p.move && p.align !== false ? dir + (p.ry || 0) : (p.ry || 0) + (p.spinY ? f / 30 * p.spinY : 0), s: p.s || 1, tint: p.tint, t: f / 30, dist: p.move ? Math.hypot(pos[0] - base[0], pos[1] - base[1]) : 0, turret: tw || 0, pitch: p.pitch || 0, recoil: p.fire ? Math.max(0, 1 - (f - p.fire) / 8) * (f >= p.fire ? 1 : 0) : 0, bob: sp > 0.1 ? 0.04 : 0 }); }
  for (const a of (S.actors || [])) if (is3(a) && !(a.a !== undefined && (f < a.a || f > a.b))) { const sp3 = a.animal || 'emu'; const pos = moveAt(a.at, a.move, f); const trot = (a.state === 'trot' || a.state === 'walk') && a.move && f >= a.move[1] && f <= a.move[2]; const sc = (a.s || 1) * (sp3 === 'horse' ? 1.7 : sp3 === 'emu' ? 0.62 : 0.78);
    W.props.push({ asset: sp3, walk: (a.state === 'walk' || trot) ? (sp3 === 'emu' ? 10 : 0) : 0, peck: a.state === 'peck', t0: (a.seed || 0), x: pos[0], z: pos[1], y: DECK + (trot ? 0.08 * Math.abs(Math.sin(f * 0.55)) : 0.015 * Math.sin(f * 0.12)), ry: (a.ry ?? (a.bird === 'emu' && !a.move ? (a.flip ? 1.1 : -1.1) : a.move ? Math.atan2(a.move[0][0] - a.at[0], a.move[0][1] - a.at[1]) + (sp3 === 'horse' ? 3.14159 : 0) : 0.95)) + (trot ? 0.12 * Math.sin(f * 0.28) : 0.05 * Math.sin(f * 0.04)), s: sc, sy: 1 + (trot ? 0.04 : 0.025) * Math.sin(f * (trot ? 0.55 : 0.1)), tint: null }); }
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
const B = (T, o0, opts, pos, extra = {}) => { const o = { ...o0, ...(o0.build === undefined && !SPEC.noLanky ? { build: 'lanky' } : {}), ...(SPEC.keepSkin ? {} : { skin: '#f6f0e6' }) }; return B2(T, o, opts, pos, extra); };
const B2 = (T, o, opts, pos, extra = {}) => ({ id: extra.id || o._id || 'person', key: 'b' + JSON.stringify([o, opts]), draw: (p) => T.bodyFront(p, o, { blink: false, ...opts }), x: pos[0], y: pos[1] ?? DECK, z: pos[2], ...extra });
const qq = (x, n = 2) => Math.round(x * 10 ** n) / 10 ** n;
const PO = (f, a, seed, exo = {}) => { const mode = a.pose || 'stand'; const base = { seed, blink: blinkAt(f, seed) > 0, expr: (typeof a.expr === 'function' ? a.expr(f) : a.expr) || 'neutral', look: a.look ?? 0.2, ...exo };
  if (mode === 'stand' && exo.__acted) return { mode: 'stand', phase: 0, tilt: qq(2.4 * Math.sin((f + seed * 7) * 0.05), 1), headTilt: qq(3.2 * Math.sin((f + seed * 5) * 0.037 + 1), 1), lift: a.lift, ...base };
  if (mode === 'stand') { const cyc = 84, ph = (f + seed * 23) % cyc, g = a.gesture !== false && SPEC.gestures !== false && ph < 30 && (Math.floor((f + seed * 23) / cyc) + seed) % 3 !== 0; const ex = base.expr;
    const em = (typeof a.expr === 'function') ? ex : ({ smile: ph > 50 && ph < 66 ? 'grin' : ex, stern: ph > 56 && ph < 70 ? 'neutral' : ex, neutral: ph > 40 && ph < 52 ? 'smile_closed' : ex, nervous: ph > 40 && ph < 56 ? 'pained' : ex, grin: ph > 60 && ph < 72 ? 'laugh' : ex, shock: ph > 40 && ph < 60 ? 'nervous' : ex }[ex] || ex);
    return { mode: 'stand', phase: 0, tilt: qq(3.2 * Math.sin((f + seed * 7) * 0.06), 1), headTilt: qq(4.5 * Math.sin((f + seed * 5) * 0.045 + 1), 1), lift: a.lift, ...base, expr: em, ...(g ? { wave: qq(Math.sin(ph * 0.42), 2) } : {}) }; }
  if (mode === 'march') return { mode: 'march', phase: qq(((f * (a.speed || 0.033) + seed * 0.17) % 1), 2), ...base };
  if (mode === 'stroll') return { mode: 'stroll', phase: qq(((f * (a.speed || 0.02) + seed * 0.13) % 1), 2), ...base };
  return { mode, phase: 0, ...base }; };
export const actorsAt = (f, T) => {
  const S = SP(f), out = []; const tint = ['tense', 'dusk', 'grave'].includes(S.light) ? '#ffd9c0' : S.light === 'storm' ? '#c8d4e8' : S.light === 'night' ? '#b8c4ee' : '#ffffff';
  (S.actors || []).forEach((a, i) => { if (a.a !== undefined && (f < a.a || f > a.b)) return; const seed = a.seed ?? (i * 7 + 3); const at = moveAt(a.at, a.move, f); const x = at[0], z = at[1]; const moving = a.move && f >= a.move[1] && f <= a.move[2];
    const exc = ['laugh', 'grin', 'shock'].includes(typeof a.expr === 'function' ? a.expr(f) : a.expr) ? 0.07 : 0; const bob = (a.bobY || exc) ? Math.abs(Math.sin(f * (a.bobY ? 0.4 : 0.33) + seed)) * (a.bobY || exc) : 0;
    if (is3(a)) return;
    if (a.animal) { const st = typeof a.state === 'function' ? a.state(f) : (a.state || 'stand'); const o = { species: a.animal, state: st, phase: qq(((f * (a.spd || 0.03) + seed * 0.1) % 1), 2), blink: blinkAt(f, seed) > 0 ? 1 : 0, ear: qq(Math.sin(f / 30 * 5 + seed), 1), tail: qq(Math.sin(f / 30 * 8 + seed) * 0.5, 1), expr: a.expr || 'normal', fall: qq(a.fall ? a.fall(f) : 0, 2), t: qq(f / 30 + seed, 2), angel: !!a.angel };
      out.push({ id: a.id || a.animal, key: 'an' + JSON.stringify(o), draw: (p) => (a.animal === 'pig' ? T.pigSide(p, o) : T.animalSide(p, o)), x, y: DECK + (a.y || 0), z, s: (a.s || 1.2) * (SPEC.cs ?? 1.4), flip: !!a.flip, keepColor: a.animal === 'pig', tint, order: 3 }); return; }
    if (a.bird) { const st = typeof a.state === 'function' ? a.state(f) : (a.state || 'stand'); const o = { species: a.bird, state: st, phase: qq(((f * (a.spd || 0.03) + seed * 0.1) % 1), 2), blink: 0, t: qq(f / 30 + seed, 1) };
      out.push({ id: a.id || 'bird', key: 'bd' + JSON.stringify(o), draw: (p) => T.birdSide(p, o), x, y: DECK + (a.y || 0), z, s: (a.s || 0.7) * (SPEC.cs ?? 1.4), flip: !!a.flip, tint, order: 2 }); return; }
    let o = typeof a.outfit === 'object' ? a.outfit : OUT[a.outfit](a.v ?? 0, a.over || {});
    const persons = (S.actors || []).filter((q) => q.outfit && !(q.a !== undefined && (f < q.a || f > q.b)));
    const ac = (SPEC.acting === false || a.acting === false) ? null : actFor(f, a, i, S, persons, seed);
    const opts = PO(f, moving && !a.pose ? { ...a, pose: a.walk || 'stroll' } : a, seed, { ...(a.opts || {}), ...(ac || {}) });
    if (opts.gest && (opts.gk || 0) > 0.2 && o.rifle) o = { ...o, rifle: false };
    out.push(B(T, o, opts, [x, DECK + (typeof a.y === 'function' ? a.y(f) : (a.y || 0)) + bob, z], { id: a.id || o._id, tint, s: (a.s || 1) * (SPEC.cs ?? 1.4) * (1 + 0.07 * (opts.lean || 0)), flip: !!a.flip, ...(a.crop ? { crop: a.crop, shadow: false, blob: false } : {}) })); });
  return out;
};
// ---------- 2D effects ----------
const FX = (key, draw, pos, s, extra = {}) => ({ key, draw, x: pos[0], y: pos[1], z: pos[2], s, blob: false, shadow: false, order: 5, ...extra });
const TXT = (key, txt, pos, s, col = '#fff6e0', ol = '#241726', size = 150, ex = {}) => FX(key + txt, (p) => { const g = p.g; g.font = `900 ${size}px Impact, "Arial Black", sans-serif`; { const w = g.measureText(txt).width; if (w > 520) { size = Math.floor(size * 520 / w); g.font = `900 ${size}px Impact, "Arial Black", sans-serif`; } } g.textAlign = 'center'; g.textBaseline = 'middle'; g.lineJoin = 'round'; g.lineWidth = 22; g.strokeStyle = ol; g.strokeText(txt, 300, 500); g.fillStyle = col; g.fillText(txt, 300, 500); }, pos, s, ex);
export const fxAt = (f, T) => { const out = [];
  for (const S of [SP(f)]) for (const e of (S.fx || [])) { if (f < e.a || f > e.b) continue; const t = qq((f - e.a) / Math.max(1, e.b - e.a), 2);
    if (e.k === 'burst') out.push(FX('bu' + e.a + t, (p) => T.fxBurst(p, t, e.col || '#fff3b0', 12, 30, 220), e.at, e.s || 1));
    else if (e.k === 'flash') out.push(FX('fl' + e.a + t, (p) => { const g = p.g, k = t < 0.35 ? t / 0.35 : 1 - (t - 0.35) / 0.65 * 0.6, R = 150 * (0.45 + 0.55 * k); const star = (r, n, col) => { g.beginPath(); for (let i = 0; i < n * 2; i++) { const a = Math.PI * i / n + 0.3, rr = i % 2 ? r * 0.45 : r; g.lineTo(300 + rr * Math.cos(a), 250 + rr * Math.sin(a)); } g.closePath(); g.fillStyle = col; g.fill(); };
      g.lineJoin = 'round'; g.lineWidth = 16; g.strokeStyle = '#3a1c14'; star(R, 7, '#ff8a1e'); g.stroke(); star(R * 0.68, 7, '#ffd23a'); star(R * 0.34, 6, '#fffbe6'); }, e.at, e.s || 1, { keepColor: true }));   // clarao de tiro cartunesco
    else if (e.k === 'puff') out.push(FX('pf' + e.a + t, (p) => { p.g.translate(150, 700); T.fxPuff(p, t); }, e.at, e.s || 1));
    else if (e.k === 'dust') out.push(FX('du' + e.a + t, (p) => T.fxDust(p, t, e.col || '#d8c8a0'), e.at, e.s || 1));
    else if (e.k === 'splash') out.push(FX('sp' + e.a + t, (p) => T.fxSplash(p, t), e.at, e.s || 1));
    else if (e.k === 'stars') out.push(FX('st' + e.a + t, (p) => T.fxStars(p, t), e.at, e.s || 1));
    else if (e.k === 'creak') out.push(FX('cr' + e.a + t, (p) => T.fxCreak(p, t), e.at, e.s || 1));
    else if (e.k === 'ring') out.push(FX('rg' + e.a + t, (p) => T.fxRing(p, t), e.at, e.s || 1));
    else if (e.k === 'text') { const pop = ramp(f, e.a, e.a + 12); let at = e.at, sc = 1, fr = {}; if (e.up !== undefined) { const C = camAt(f); const fw = [C.look[0] - C.pos[0], C.look[1] - C.pos[1], C.look[2] - C.pos[2]]; const L = Math.hypot(...fw); const dd = L * 0.8; const hh = dd * Math.tan(C.fov * Math.PI / 360); const nlen = e.text.length, fw_ = 2 * hh * 0.5625, frac = Math.min(0.8, 0.12 + 0.055 * nlen), est = Math.min(0.867, 0.116 * nlen); const sb = frac * fw_ / (1.35 * est); at = [C.pos[0] + fw[0] / L * dd, C.pos[1] + fw[1] / L * dd + e.up * hh - 1.07 * sb * M.back(pop), C.pos[2] + fw[2] / L * dd]; sc = sb / (e.s || 1.2); fr = { front: true }; } out.push(TXT('tx', e.text, at, M.back(pop) * (e.s || 1.2) * sc, e.col || '#fff6e0', e.ol || '#241726', e.size || 150, { ...(e.roll ? { roll: e.roll } : {}), ...fr })); } }
  return out; };
// ===== ACTING DIRECTOR: expression beats tied to the narration, gaze (partner / straight into the lens = "4th wall"), gestures, irregular blinks =====
// Data: TIMING = { words: [[s,e,'word'],...], phrases: [[s,e,'text'],...] } in frames @30 (generated by build3.sh from work/words.json + phrases.json).
const TM = (typeof TIMING !== 'undefined') ? TIMING : { words: [], phrases: [] };
const LEX = [
  ['shock', /^(never|thousands?|millions?|only|suddenly|wait|gone|died|dead|killed|impossible|twenty|eleven|hundred|seconds|minutes|nineteen|eighteen|seventeen|thirty|forty|fifty|sixty|seventy|nine|ten|\d+)$/i],
  ['laugh', /^(laugh\w*|jokes?|funny|friendliest|party|haha)$/i],
  ['grin', /^(plan|tricks?|clever|secret|sneak\w*|stole|fooled|wins?|won|winner|victory|triumph\w*|bounty|trophy|record|ghost|artists?|painters?)$/i],
  ['stern', /^(war|army|attack\w*|refus\w*|ultimatum|orders?|ordered|demand\w*|furious|angry|enem\w*|guns?|bullets|cannon|battle|fought|blockad\w*|bombard\w*|spies|spy|soldiers?|sultan|king)$/i],
  ['nervous', /^(hid|hide|hiding|watch\w*|afraid|trouble|problem|escap\w*|ran|pulled|defeat\w*|lost|cross\w*|flee|fled|stares|trap|locked|missing|missed|lie|lied)$/i],
  ['pained', /^(ear|cut|hurt|leg|wounded|trashed|broken|jar|beer)$/i],
  ['dazed', /^(confused|dazed|heard)$/i],
  ['smile', /^(friend\w*|peace|share\w*|safe|home|zoo|help|gift|proud|cake|cakes|pastry|whisky|schnapps)$/i],
];
// PT lexicon (accents stripped before matching)
LEX.push(['shock', /^(nunca|mil|milhoes?|apenas|so|esperem|morreu|morreram|impossivel|vinte|trinta|quarenta|cinquenta|sessenta|setenta|cem|onze|dez|nove|segundos|minutos|zero)$/],
  ['laugh', /^(riu|riram|rindo|piadas?|engracado|festa|haha)$/], ['grin', /^(plano|truques?|esperto|segredo|roubou|enganou|ganhou|venceu|vencedor|vitoria|trofeu|recorde|artistas|pintores|fantasma)$/],
  ['stern', /^(guerra|exercito|ataque|atacar|recusou|ultimato|ordem|ordenou|exigiu|furioso|raiva|inimigos?|armas?|balas?|canhao|batalha|lutou|bloqueou|bombardeou|espioes|espiao|soldados|sultao|rei|metralhadoras?)$/],
  ['nervous', /^(escondeu|esconder|escondidos|vigiando|medo|problema|escapou|fugiu|correu|derrota|perdeu|cruzou|armadilha|trancou|errava|errou|desistiram|retiraram)$/],
  ['pained', /^(orelha|cortou|machucou|perna|ferido|quebrado|pote|cerveja)$/], ['dazed', /^(confuso|atordoado|ouviu)$/],
  ['smile', /^(amigos?|paz|dividiu|seguro|casa|zoologico|ajuda|presente|orgulho|bolos?|docel?|doces|uisque|whisky)$/]);
const ALT = { stern: 'neutral', shock: 'nervous', laugh: 'grin', grin: 'smile_closed', nervous: 'pained', pained: 'nervous', dazed: 'neutral', smile: 'grin', neutral: 'smile_closed', smile_closed: 'smile', whistle: 'smile', relief: 'smile', relief_open: 'grin', lick: 'smile' };
const REACT = { stern: 'nervous', shock: 'shock', laugh: 'laugh', grin: 'smile', nervous: 'nervous', pained: 'pained', dazed: 'dazed', smile: 'smile' };
const GMAP = { stern: ['point', 'hips', 'cross'], shock: ['up', 'scared', 'hold'], laugh: ['hips', 'up'], grin: ['hips', 'point', 'wave2'], nervous: ['scared', 'shrug', 'hold'], pained: ['facepalm', 'think', 'hold'], dazed: ['shrug', 'think'], smile: ['wave2', 'hold', 'hips'], neutral: ['shrug', 'think', 'hips'] };
let LEAD = null;
const buildLead = () => {
  LEAD = Array.from({ length: TOTAL + 60 }, () => ({}));
  TM.phrases.forEach((P, pi) => { const [s, e, text] = P; const ws = TM.words.filter((w) => w[0] >= s - 1 && w[1] <= e + 3);
    { let inq = false; for (const w of ws) { const raw = String(w[2] || ''); const op = /^["“«]/.test(raw), cl = /["”»][.,!?]*$/.test(raw); if (op) inq = true; if (inq) for (let f = w[0] - 1; f <= w[1] + 1; f++) if (LEAD[f]) LEAD[f].talk = 1; if (cl) inq = false; } }   // FALA de personagem: palavras entre aspas
    const keys = []; for (const w of ws) { const wd = String(w[2] || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]/g, ''); for (const [m, re] of LEX) if (re.test(wd)) { keys.push({ f: w[0], m }); break; } }
    const qm = /\?$/.test(text), ex = /!$/.test(text); if (!keys.length && (qm || ex)) keys.push({ f: Math.max(s, e - 20), m: qm ? 'nervous' : 'shock' });
    const main = keys.length ? keys[0].m : 'neutral';
    for (let f = Math.max(0, s - 2); f <= Math.min(TOTAL + 50, e + 6); f++) { const L = LEAD[f]; L.ph = pi; const cyc = (f - s + 400) % 52; L.alt = cyc >= 30 && cyc < 40; L.cam = f >= e - 22; L.start = f < s + 14; }
    keys.slice(0, 3).forEach((k) => { for (let f = k.f - 2; f <= k.f + 18; f++) { const L = LEAD[f]; if (!L) continue; L.key = k.m; const t = Math.min(1, (f - (k.f - 2)) / 5) * (1 - Math.max(0, (f - (k.f + 12)) / 7)); L.kk = Math.max(L.kk || 0, t); } });
    if (keys.length || pi % 2 === 0) { const gk0 = keys.length ? keys[0].f : s + 8, gl = GMAP[main] || GMAP.neutral, g = gl[pi % gl.length];
      for (let f = gk0 - 4; f <= gk0 + 34; f++) { const L = LEAD[f]; if (!L) continue; const t = (f - (gk0 - 4)) / 38; const ease = Math.min(1, t * 38 / 7, (1 - t) * 38 / 9); if (ease > (L.gk || 0)) { L.g = g; L.gk = ease; L.gt = f / 30; } } }
  });
};
const BLS = {};
const blinkLid = (f, seed) => { if (!BLS[seed]) { let t = 6 + (seed * 11) % 25, r = 1234 + seed * 77; const L = []; while (t < TOTAL + 80) { L.push(t); r = (r * 1664525 + 1013904223) >>> 0; t += 15 + (r >>> 8) % 55; } BLS[seed] = L; }
  for (const s of BLS[seed]) { const d = f - s; if (d >= 0 && d < 4) return [0.5, 1, 1, 0.5][d]; if (d < 0) break; } return 0; };
const camRightAt = (f, ax, az) => { const C = camAt(f); return [C.pos[2] - az, -(C.pos[0] - ax)]; };
const exprOf = (f, a, ai, persons) => { const lead = persons[0] === a, r = lead ? 0 : Math.max(1, persons.indexOf(a)); const base = typeof a.expr === 'function' ? a.expr(f) : (a.expr || 'neutral');
  const L = (LEAD && LEAD[Math.max(0, Math.min(TOTAL + 50, lead ? f : f - 6 * r))]) || {}; let e = base, up = 0, lean = 0;
  if (L.key && (L.kk || 0) > 0.2) { e = lead ? L.key : (REACT[L.key] || base); up = -3.5 * L.kk; lean = L.kk; } else if (L.alt && typeof a.expr !== 'function') e = ALT[base] || base;
  return { e, up, lean, L, base }; };
// returns the acting options for actor `a` (a person) at frame f
const actFor = (f, a, ai, S, persons, seed) => {
  if (!LEAD) buildLead();
  const lead = persons[0] === a, r = lead ? 0 : Math.max(1, persons.indexOf(a)), cur = exprOf(f, a, ai, persons);
  let swap = -1; for (let k = 1; k < 4; k++) { if (exprOf(f - k, a, ai, persons).e !== exprOf(f - k - 1, a, ai, persons).e) { swap = k; break; } }
  let lid = blinkLid(f, seed); if (swap >= 0) lid = Math.max(lid, [0.5, 1, 1, 0.5][swap - 1] ?? 0);
  if (typeof a.expr === 'function' || a.acting === 'low') return { expr: cur.e, blink: lid, __acted: 1 };
  const partner = persons.find((p) => p !== a); let toward = (a.look ?? 0.4) >= 0 ? 1 : -1;
  if (partner) { const pp = partner.move ? [partner.at[0] + (partner.move[0][0] - partner.at[0]) * Math.max(0, Math.min(1, (f - partner.move[1]) / Math.max(1, partner.move[2] - partner.move[1]))), partner.at[1]] : partner.at; const ap = a.at; const rt = camRightAt(f, ap[0], ap[1]); const d = (pp[0] - ap[0]) * rt[0] + (pp[1] - ap[1]) * rt[1]; toward = d >= 0 ? 1 : -1; if (a.flip) toward = -toward; }
  const L = cur.L; let face = 0, look = 0;
  const camGaze = lead ? !!L.cam : (!!(L.key && (L.kk || 0) > 0.4) || (L.cam && r % 2 === 1));
  if (camGaze) { face = 0; look = 0; } else if (lead && L.start) { face = 0.5 * toward; look = 1.1 * toward; } else { face = 0.42 * toward; look = 0.8 * toward; }
  const fx = { browUp: qq(cur.up, 1), skeptic: !lead && !!L.alt, lookY: camGaze ? 0 : 0.2, sweat: cur.e === 'shock' || cur.e === 'nervous' };
  { const spk = persons.length > 1 ? 1 : 0; if (L.talk && r === spk) fx.talk = qq(0.3 + 0.7 * Math.abs(Math.sin(f * 1.7)), 1); }   // quem fala: o 2o personagem da cena (ou o unico)
  const o = { expr: cur.e, blink: lid, look: qq(look, 1), facing: qq(face, 1), fx, lean: qq(cur.lean, 1), __acted: 1 };
  const GL = lead ? L : (LEAD[Math.max(0, f - 9 * r)] || {});
  if (!a.pose || a.pose === 'stand') { if (GL.g && (GL.gk || 0) > 0.02 && (lead || r === 1) && !a.rifleKeep) { o.gest = GL.g; o.gk = qq(GL.gk, 1); o.gt = qq(f / 30, 2); } }
  return o; };
