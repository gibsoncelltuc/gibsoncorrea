import React from 'react';
import { Pose, Look, handFrame } from '../characters/Rig';
import { Rifle } from '../world/props';
import { Puff, MuzzleFlash } from '../world/common';
import { clamp, keys, easeInOut } from '../lib/anim';

/** Progresso de levantar o fuzil (0..1). */
export const aimUp = (t: number, t0: number, tFire: number) => keys(t, [[t0, 0], [tFire - 0.12, 1]], easeInOut);
/** Posição do cano (mundo) a partir do referencial da mão direita. */
export const muzzleWorld = (pose: Pose, look: Look, len = 1.85): [number, number, number] => {
  const hf = handFrame(pose, 'R', look); const dx = Math.sin(hf.ang) * pose.face, dy = -Math.cos(hf.ang);
  return [hf.pos[0] + dx * len * pose.scale, hf.pos[1] + dy * len * pose.scale, pose.z + 0.2];
};
export const RifleInHand: React.FC<{ up: number }> = ({ up }) => (<group rotation={[0, 0, Math.PI * (1 - up)]}><Rifle /></group>);
export const GunSmoke: React.FC<{ t: number; t0: number; at: [number, number, number] }> = ({ t, t0, at }) => (
  <>{[0, 1, 2, 3, 4].map((i) => <Puff key={i} p={[at[0] + i * 0.35, at[1] + i * 0.08, at[2]]} t={t} t0={t0 + i * 0.07} dur={1.7} r={0.5 + i * 0.12} color={i % 2 ? '#e6e1ea' : '#f6f3f6'} rise={1.4 + i * 0.3} drift={[1.2, 0.2]} />)}</>
);
export { MuzzleFlash, clamp };
