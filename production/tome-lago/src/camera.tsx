import React, { useLayoutEffect } from 'react';
import { useThree } from '@react-three/fiber';
import { smoother, lerp } from './lib/anim';
type V3 = [number, number, number];
export type CamKey = { t: number; pos: V3; look: V3; fov: number; roll?: number };
export type CamSpec = { pos: V3; look: V3; fov: number; roll: number };
const mix = (a: V3, b: V3, u: number): V3 => [lerp(a[0], b[0], u), lerp(a[1], b[1], u), lerp(a[2], b[2], u)];
/** Interpola chaves com smootherstep, leve arco e sway de câmera na mão (determinístico). */
export const camAt = (t: number, ks: CamKey[]): CamSpec => {
  let i = 0; while (i < ks.length - 2 && t > ks[i + 1].t) i++;
  const a = ks[i], b = ks[Math.min(i + 1, ks.length - 1)];
  const u = b.t === a.t ? 1 : smoother((t - a.t) / (b.t - a.t));
  const pos = mix(a.pos, b.pos, u); const arc = Math.sin(Math.PI * u) * 0.12;
  pos[1] += arc; pos[0] += Math.sin(t * 0.7) * 0.05; pos[1] += Math.sin(t * 0.9 + 1) * 0.035;
  return { pos, look: mix(a.look, b.look, u), fov: lerp(a.fov, b.fov, u), roll: lerp(a.roll ?? 0, b.roll ?? 0, u) };
};
export const CameraRig: React.FC<{ spec: CamSpec }> = ({ spec }) => {
  const { camera } = useThree();
  useLayoutEffect(() => {
    const c = camera as any;
    c.position.set(...spec.pos); c.up.set(0, 1, 0); c.lookAt(...spec.look); c.rotateZ(spec.roll);
    c.fov = spec.fov; c.near = 0.1; c.far = 600; c.updateProjectionMatrix();
  });
  return null;
};
