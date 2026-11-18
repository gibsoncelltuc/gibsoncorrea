// shared spec helpers (prepended to every spec)
const DK0 = 6;
const pp = (X, outfit, v, dx, z, expr = 'smile', ex = {}) => ({ outfit, v, at: [X + dx, z], pose: 'stand', look: dx > 0 ? -0.4 : 0.4, expr, ...ex });
const mv = (X, outfit, v, dx0, dx1, z, a, b, ex = {}) => ({ outfit, v, at: [X + dx0, z], move: [[X + dx1, z], a, b], pose: 'march', speed: 0.034, expr: 'neutral', ...ex });
const txt = (X, a, b, text, col = '#fff6e0', ol = '#27408b', h = 4.4, ex = {}) => ({ k: 'text', a, b, up: 0.42, at: [X, DK0 + h, 3.5], text, s: 1.3, col, ol, size: 120, ...ex });
const ctr = (o, X) => { let A = (o.actors || []).filter((q) => q.at); const P_ = A.filter((q) => q.outfit); if (A.length > 4 && P_.length) A = P_; if (!A.length) return [0, 0]; const fin = (q) => (q.arrive && q.move ? q.move[0] : q.at);   /* quem CHEGA andando conta pela posicao final: a camera ja espera no lugar */ return [A.reduce((s, q) => s + (fin(q)[0] - X), 0) / A.length, A.reduce((s, q) => s + fin(q)[1], 0) / A.length]; };
// standard shot: gentle push-in on a group; hero checks use 'any'/'none'
const S = (id, a, b, X, light, o = {}) => ({ id, a, b, light, shots: o.shots, trans: o.trans, nocut: o.nocut, vary: o.vary, lightMod: o.lightMod, exp: o.exp, hero: o.hero || (o.actors && o.actors.some((q) => q.outfit) ? { hero: 'any', frame: 'medium', minH: 0.06 } : { hero: 'none' }), weather: o.wx,
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
