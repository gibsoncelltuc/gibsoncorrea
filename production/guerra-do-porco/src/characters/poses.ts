// Biblioteca de atuação (funções puras do tempo) — rig v2.
import { P, Pose } from './Rig';
import { keys, easeInOut, easeOut, easeOutBack, clamp, lerp, smoother } from '../lib/anim';

export const blinkAt = (t: number, off = 0) => { const p = (t + off) % 3.1; return p < 0.12 ? Math.sin((p / 0.12) * Math.PI) : 0; };

export const idle = (t: number, o: { off?: number; face?: 1 | -1; x?: number; y?: number; z?: number; scale?: number } = {}): Pose => {
  const off = o.off ?? 0;
  return P({
    x: o.x ?? 0, y: o.y ?? 0, z: o.z ?? 0, face: o.face ?? 1, scale: o.scale ?? 1,
    bob: Math.sin((t + off) * 2.1) * 0.022, lean: Math.sin((t + off) * 0.9) * 0.012,
    armL: [0.1 + Math.sin((t + off) * 1.3) * 0.03, 0.12], armR: [-0.1 - Math.sin((t + off) * 1.3) * 0.03, 0.12],
    blink: blinkAt(t, off), look: [Math.sin((t + off) * 0.5) * 0.5, 0],
  });
};
/** Ciclo de caminhada: velocidade de deslocamento ≈ 2.5 × speed (u/s) para os pés não escorregarem. */
export const walk = (t: number, o: { speed?: number; off?: number } = {}): Partial<Pose> => {
  const f = o.speed ?? 1.7, ph = (t + (o.off ?? 0)) * f * Math.PI * 2, s = Math.sin(ph), c = Math.cos(ph);
  return { bob: Math.abs(c) * 0.09 - 0.03, legL: [s * 0.55, Math.max(0, -c) * 0.6], legR: [-s * 0.55, Math.max(0, c) * 0.6], armL: [-s * 0.5, 0.25], armR: [s * 0.5, 0.25], lean: -0.04 };
};
/** Marcha militar: braços firmes, joelhos altos. */
export const march = (t: number, o: { off?: number } = {}): Partial<Pose> => {
  const ph = (t + (o.off ?? 0)) * 1.9 * Math.PI * 2, s = Math.sin(ph), c = Math.cos(ph);
  return { bob: Math.abs(c) * 0.07, legL: [s * 0.62, Math.max(0, -c) * 0.8], legR: [-s * 0.62, Math.max(0, c) * 0.8], armL: [-s * 0.25 + 0.2, 0.9], armR: [s * 0.25 + 0.2, 0.9], lean: 0 };
};
/** Mira e tiro com fuzil: sobe a arma (t0..t0+dur), segura, dispara em tFire e sofre o coice. */
export const aimFire = (t: number, base: Pose, o: { t0: number; tFire: number }): Pose => {
  const up = keys(t, [[o.t0, 0], [o.tFire - 0.12, 1]], easeInOut);
  const rec = t >= o.tFire ? Math.exp(-(t - o.tFire) * 7) : 0;
  return { ...base,
    armR: [lerp(-0.1, 1.5, up) + rec * 0.35, lerp(0.12, 0.18, up)], armL: [lerp(0.1, 1.55, up) + rec * 0.3, lerp(0.12, 0.35, up)],
    lean: -0.04 * up + rec * 0.16, bob: base.bob - 0.04 * up, tilt: 0.1 * up - rec * 0.1,
    lid: lerp(0.42, 0.78 - rec * 0.5, up), brows: [-0.2 * up, -0.2 * up], angry: 0.35 * up, mouth: up > 0.5 ? 'line' : base.mouth,
  };
};
export const smug = (base: Pose): Pose => ({ ...base, eye: 'lid', lid: 0.55, brows: [0.35, -0.4], mouth: 'smirk', tilt: base.tilt + 0.04 });
export const shock = (t: number, base: Pose, t0: number): Pose => {
  const u = clamp((t - t0) / 0.18), pop = easeOutBack(u, 2.5);
  return { ...base, eye: u > 0 ? 'wide' : base.eye, brows: [0.9, 0.9], mouth: u > 0 ? 'oh' : base.mouth, open: 0.5, sweat: u > 0 ? (t - t0) * 1.2 : 0,
    squash: 0.1 * Math.sin(u * Math.PI) * (1 - u * 0.2), bob: base.bob + 0.08 * Math.sin(pop * Math.PI * 0.5), lean: base.lean * (1 - u) };
};
export const laugh = (t: number, base: Pose, o: { amp?: number } = {}): Pose => {
  const a = o.amp ?? 1, sh = Math.sin(t * 24) * 0.5 + 0.5;
  return { ...base, eye: 'arc', mouth: 'laugh', open: 0.4 + 0.6 * sh, brows: [0.7, 0.7],
    bob: base.bob + Math.abs(Math.sin(t * 12)) * 0.08 * a, lean: 0.1 + Math.sin(t * 12) * 0.03 * a, tilt: -0.12 + Math.sin(t * 6) * 0.05,
    armL: [0.9, 1.5], armR: [-0.6, 1.6] };
};
/** Mão levantada em “pare” (palma pra frente) + abanar a cabeça. */
export const stopHand = (t: number, base: Pose, t0: number): Pose => {
  const up = keys(t, [[t0, 0], [t0 + 0.3, 1]], easeOutBack), shake = t > t0 + 0.2 ? Math.sin((t - t0 - 0.2) * 10) * 0.08 * Math.exp(-(t - t0 - 0.2) * 1.2) : 0;
  return { ...base, armR: [lerp(-0.1, 2.55, up), lerp(0.12, -0.15, up)], tilt: base.tilt + shake, eye: 'lid', lid: 0.6, brows: [0.1, 0.1], mouth: 'line' };
};
export const point = (t: number, base: Pose, t0: number, o: { side?: 'L' | 'R'; up?: number } = {}): Pose => {
  const u = keys(t, [[t0, 0], [t0 + 0.25, 1]], easeOutBack), a = lerp(0.1, o.up ?? 1.45, u);
  return o.side === 'L' ? { ...base, armL: [a, lerp(0.1, 0.05, u)] } : { ...base, armR: [a, lerp(0.1, 0.05, u)] };
};
export { clamp, easeOut, smoother };
