// fit.sh em UM navegador so' (antes: 1 navegador novo por iteracao, ate 15). Mesma logica: fase 1 afasta takes cortados/escondidos; fase 2 aproxima takes minusculos.
// usage: node fit_fast.mjs <id>   -> stories/<id>/fit.js
import fs from 'fs'; import { openStory, inspect } from './qa_core.mjs';
const id = process.argv[2]; const t0 = Date.now(); const S = await openStory(); const K = {}; let shots = null;
const state = {}; const upd = (R, scope) => { for (const sh of (scope || S.SHOTS.map((x) => x.id))) state[sh] = false; for (const f of R.fails) state[f.shot] = true; };
const BADW = ['cropped', 'CROPPED', 'inside geometry', 'HIDDEN', 'too close', 'empty', 'below-ground'];
for (let it = 0; it < 10; it++) {
  const R = await inspect(S, { step: 4, only: shots, kfit: { ...K } });
  upd(R, shots);
  const bad = [...new Set(R.fails.filter((f) => f.why.some((x) => BADW.some((w) => x.includes(w)))).map((f) => f.shot))].sort(); const other = [...new Set(R.fails.map((f) => f.shot))].filter((s) => !bad.includes(s));
  console.log('iter', it, 'widen', JSON.stringify(bad), 'other', JSON.stringify(other)); if (!bad.length) break;
  for (const s of bad) K[s] = Math.round((K[s] ?? 1) * 1.12 * 1000) / 1000; shots = bad;
}
let R = await inspect(S, { step: 4, kfit: { ...K } }); upd(R, null); let tiny = [...R.tiny];
for (let it = 0; it < 5 && tiny.length; it++) {
  const prev = { ...K }; for (const s of tiny) K[s] = Math.round(Math.max(0.55, (K[s] ?? 1) * 0.89) * 1000) / 1000;
  R = await inspect(S, { step: 4, only: tiny, kfit: { ...K } }); const scope = [...tiny]; upd(R, scope); const badshots = new Set(R.fails.map((f) => f.shot));
  for (const s of [...tiny]) if (badshots.has(s)) { state[s] = false; if (s in prev) K[s] = prev[s]; else delete K[s]; tiny.splice(tiny.indexOf(s), 1); console.log('  tighten reverted', s); }
  tiny = R.tiny.filter((s) => tiny.includes(s) && (K[s] ?? 1) > 0.55); console.log('tighten iter', it, 'still tiny', JSON.stringify(tiny));
}
const out = {}; for (const [k, v] of Object.entries(K)) if (Math.abs(v - 1) > 1e-6) out[k] = v;
fs.writeFileSync(`stories/${id}/fit.js`, 'SPEC.fit = ' + JSON.stringify(out) + ';\n'); const failing = Object.keys(state).filter((k) => state[k]); fs.rmSync(`stories/${id}/takes_ok`, { force: true }); if (!failing.length) fs.writeFileSync(`stories/${id}/takes_ok`, 'ok'); else console.log('TAKES COM FALHA:', JSON.stringify(failing));
console.log('fit', JSON.stringify(out), `(${((Date.now() - t0) / 1000).toFixed(0)} s)`); await S.close();
