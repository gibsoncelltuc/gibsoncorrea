// ===== RETIME: the spec is authored on the SOURCE-language timeline; every frame-valued field is warped onto the new voice (anchors = sentence/clause starts & ends) =====
if (typeof RETIME !== 'undefined') (() => {
  const A = RETIME.anchors;
  const mapx = (x, from, to) => { if (x <= A[0][from]) return x - A[0][from] + A[0][to]; for (let i = 0; i < A.length - 1; i++) { const a0 = A[i][from], a1 = A[i + 1][from]; if (x <= a1) { const t = a1 === a0 ? 1 : (x - a0) / (a1 - a0); return A[i][to] + (A[i + 1][to] - A[i][to]) * t; } } const L = A[A.length - 1]; return x - L[from] + L[to]; };
  const wf = (f) => Math.round(mapx(f, 0, 1)), unwarp = (f) => mapx(f, 1, 0);
  const fnw = (fn) => (f, ...r) => fn(unwarp(f), ...r);
  const tr = (t) => (RETIME.i18n && RETIME.i18n[t] !== undefined ? RETIME.i18n[t] : t);
  const ent = (e) => { const o = { ...e }; for (const k of ['a', 'b', 'fire']) if (typeof o[k] === 'number') o[k] = wf(o[k]); if (Array.isArray(o.move)) o.move = [o.move[0], wf(o.move[1]), wf(o.move[2]), ...o.move.slice(3)];
    for (const k of ['y', 'expr', 'state', 'fall', 'turret', 'pitch', 'sy', 'lightMod', 'weather', 'world']) if (typeof o[k] === 'function') o[k] = fnw(o[k]); if (typeof o.text === 'string') o.text = tr(o.text); return o; };
  SPEC.total = RETIME.ptTotal;
  SPEC.kicks = (SPEC.kicks || []).map((k) => ({ ...k, f: wf(k.f) })); SPEC.flashes = (SPEC.flashes || []).map((k) => ({ ...k, f: wf(k.f) }));
  SPEC.shots = SPEC.shots.map((s) => { const o = ent(s); o.a = wf(s.a); o.cam = (s.cam || []).map((k) => ({ ...k, f: wf(k.f) })); o.props = (s.props || []).map(ent); o.actors = (s.actors || []).map(ent); o.fx = (s.fx || []).map(ent); return o; });
  SPEC.shots.forEach((s, i, L) => { if (i === 0) s.a = 0; s.b = i < L.length - 1 ? Math.max(s.a, L[i + 1].a - 1) : SPEC.total - 1; if (i < L.length - 1 && L[i + 1].a <= s.a) L[i + 1].a = s.a + 1; });
  SPEC.shots.forEach((s) => { s.cam = s.cam.map((k, ki, ca) => ({ ...k, f: Math.min(Math.max(k.f, s.a), s.b) })); if (s.cam.length >= 2) { s.cam[0].f = s.a; s.cam[s.cam.length - 1].f = s.b; } });
})();
