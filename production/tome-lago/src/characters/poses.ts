// Biblioteca de ações (atuação corporal) — todas funções puras de t (segundos).
import { P, Pose } from './Rig';
import { keys, easeInOut, easeOut, easeOutBack, clamp } from '../lib/anim';
import { mouthOpen } from '../lib/timing';

export const blinkAt = (t: number, off = 0) => { const p = (t + off) % 3.3; return p < 0.13 ? Math.sin((p / 0.13) * Math.PI) : 0; };

export const idle = (t: number, o: { off?: number; face?: 1 | -1; x?: number; y?: number; z?: number; scale?: number } = {}): Pose => {
  const off = o.off ?? 0;
  return P({
    x: o.x ?? 0, y: o.y ?? 0, z: o.z ?? 0, face: o.face ?? 1, scale: o.scale ?? 1,
    bob: Math.sin((t + off) * 2.1) * 0.025, lean: Math.sin((t + off) * 0.9) * 0.015,
    armL: [0.12 + Math.sin((t + off) * 1.3) * 0.03, 0.12], armR: [-0.12 - Math.sin((t + off) * 1.3) * 0.03, 0.12],
    blink: blinkAt(t, off), look: [Math.sin((t + off) * 0.5) * 0.6, 0],
  });
};

export const walk = (t: number, o: { speed?: number; off?: number } = {}): Partial<Pose> => {
  const f = (o.speed ?? 1.7), ph = (t + (o.off ?? 0)) * f * Math.PI * 2, s = Math.sin(ph), c = Math.cos(ph);
  return {
    bob: Math.abs(c) * 0.09 - 0.03,
    legL: [s * 0.55, Math.max(0, -Math.cos(ph)) * 0.6], legR: [-s * 0.55, Math.max(0, Math.cos(ph)) * 0.6],
    armL: [-s * 0.5, 0.25], armR: [s * 0.5, 0.25], lean: 0.04,
  };
};

export type ThrowInfo = { pose: Pose; held: boolean; release: number };
/** Arremesso da cadeira: antecipação → ação → overshoot → settle. t relativo ao início (s). */
export const throwChair = (t: number, base: Pose): ThrowInfo => {
  const rel = 0.95; // instante de soltar
  const lean = keys(t, [[0, 0], [0.7, 0.22], [rel, -0.3], [rel + 0.5, -0.05]], easeInOut);
  const sh = keys(t, [[0, 0.55], [0.55, -0.9], [0.85, -1.0], [rel, 1.6], [rel + 0.25, 1.95], [rel + 0.7, 0.3]], easeOutBack);
  const el = keys(t, [[0, 0.4], [0.55, 0.3], [rel, 0.05], [rel + 0.7, 0.2]], easeInOut);
  const pose = { ...base, lean, armR: [sh, el] as [number, number], armL: [sh * 0.97, el] as [number, number],
    legR: [keys(t, [[0, 0], [0.7, -0.25], [rel, 0.3], [rel + 0.5, 0]], easeInOut), 0.1] as [number, number],
    bob: base.bob - keys(t, [[0, 0], [0.7, 0.12], [rel, -0.02], [rel + 0.3, 0]], easeInOut),
    mouth: 'closed' as const, brows: [0.2, 0.2] as [number, number] };
  return { pose, held: t < rel, release: rel };
};

export const laugh = (t: number, base: Pose, o: { amp?: number } = {}): Pose => {
  const a = o.amp ?? 1, sh = Math.sin(t * 26) * 0.5 + 0.5;
  return { ...base,
    bob: base.bob + Math.abs(Math.sin(t * 13)) * 0.07 * a, lean: 0.12 + Math.sin(t * 13) * 0.025 * a, tilt: -0.14 + Math.sin(t * 6.5) * 0.04,
    armL: [0.9, 1.5], armR: [-0.7, 1.7 + sh * 0.1], mouth: 'laugh', open: 0.5 + 0.5 * sh, brows: [0.9, 0.9], blink: 0.6,
  };
};

export const speaking = (t: number, base: Pose, lines: string[], mouth: Pose['mouth'] = 'open'): Pose => {
  const o = mouthOpen(t, lines);
  return { ...base, mouth: o > 0.05 ? mouth : base.mouth, open: o };
};

export const gesture = (t: number, side: 'L' | 'R', t0: number, base: Pose, o: { up?: number } = {}): Pose => {
  const u = o.up ?? 1.2;
  const s = keys(t, [[t0, 0.1], [t0 + 0.35, u], [t0 + 1.4, u - 0.1], [t0 + 1.9, 0.12]], easeOutBack);
  const e = keys(t, [[t0, 0.1], [t0 + 0.35, 0.8], [t0 + 1.9, 0.12]], easeInOut);
  return side === 'R' ? { ...base, armR: [s, e] } : { ...base, armL: [s, e] };
};
export { clamp, easeOut };
