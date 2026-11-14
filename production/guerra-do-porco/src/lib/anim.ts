// Utilidades de animação determinística (funções puras do tempo).
export const clamp = (v: number, a = 0, b = 1) => Math.min(b, Math.max(a, v));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const smoother = (t: number) => { t = clamp(t); return t * t * t * (t * (t * 6 - 15) + 10); };
export const easeOut = (t: number) => 1 - Math.pow(1 - clamp(t), 3);
export const easeInOut = (t: number) => { t = clamp(t); return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
export const easeOutBack = (t: number, s = 1.9) => { t = clamp(t); const c3 = s + 1; return 1 + c3 * Math.pow(t - 1, 3) + s * Math.pow(t - 1, 2); };
export const easeIn = (t: number) => clamp(t) ** 2.2;
export type Ease = (t: number) => number;
export const prog = (t: number, a: number, b: number) => clamp((t - a) / (b - a));

/** Keyframes pose-a-pose: [[tempo, valor], ...] com easing por segmento (overshoot opcional). */
export const keys = (t: number, k: [number, number][], ease: Ease = easeOutBack): number => {
  if (t <= k[0][0]) return k[0][1];
  for (let i = 1; i < k.length; i++) {
    if (t <= k[i][0]) {
      const [t0, v0] = k[i - 1], [t1, v1] = k[i];
      return lerp(v0, v1, ease((t - t0) / (t1 - t0)));
    }
  }
  return k[k.length - 1][1];
};
// PRNG com seed — nada de Math.random.
export const rng = (seed: number) => () => {
  seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
  let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};
export const hex = (h: string): [number, number, number] => [parseInt(h.slice(1, 3), 16) / 255, parseInt(h.slice(3, 5), 16) / 255, parseInt(h.slice(5, 7), 16) / 255];
export const mixHex = (a: string, b: string, t: number): string => {
  const A = hex(a), B = hex(b);
  const c = (i: number) => Math.round(lerp(A[i], B[i], clamp(t)) * 255).toString(16).padStart(2, '0');
  return `#${c(0)}${c(1)}${c(2)}`;
};
