import React from 'react';
import { Character, Pose, Look, handPos } from '../characters/Rig';
import { throwChair } from '../characters/poses';
import { Chair, Table, Bed, Door, Ripple, Droplets } from '../world/common';
import { clamp } from '../lib/anim';

export type PropKind = 'chair' | 'table' | 'bed' | 'door';
export const PropMesh: React.FC<{ kind: PropKind }> = ({ kind }) => (kind === 'chair' ? <Chair /> : kind === 'table' ? <Table /> : kind === 'bed' ? <Bed /> : <Door />);
export const propScale: Record<PropKind, number> = { chair: 1, table: 0.62, bed: 0.55, door: 0.8 };
export const propOffset: Record<PropKind, [number, number]> = { chair: [0.35, -0.55], table: [0.5, -0.5], bed: [0.5, -0.4], door: [0.2, -0.6] };

export type ThrowSpec = { t0: number; prop: PropKind; target: [number, number, number] };
const FLIGHT = 0.95;

export type ThrowOut = { pose: Pose; handR: React.ReactNode; fly: React.ReactNode; impactAge: number; landed: boolean; releaseT: number };
/** Coreografia completa de um arremesso: pose do personagem, objeto na mão, voo balístico, respingo. */
export const throwSeq = (t: number, th: ThrowSpec, base: Pose, look: Look, pickAt = 0.25): ThrowOut => {
  const rel = t - th.t0;
  const { pose, held, release } = throwChair(Math.max(rel, 0), base);
  const k = propScale[th.prop]; const [ox, oy] = propOffset[th.prop];
  const inHand = rel >= pickAt && held;
  const handR = inHand ? (
    <group position={[ox * 0.4, oy * 0.4, 0.05]} rotation={[0, 1.1, -0.5]} scale={k}><PropMesh kind={th.prop} /></group>
  ) : null;
  let fly: React.ReactNode = null;
  const flyU = (rel - release) / FLIGHT;
  const rp = throwChair(release, base).pose;
  const hp = handPos(rp, 'R', look);
  if (flyU > 0 && flyU < 1) {
    const x = hp[0] + (th.target[0] - hp[0]) * flyU, z = th.target[2] * flyU;
    const y = hp[1] + (th.target[1] - hp[1]) * flyU + 4 * flyU * (1 - flyU) * 4.2;
    fly = <group position={[x, y, z]} rotation={[flyU * 6, 1.1 + flyU * 3, flyU * 8]} scale={k * 1.15}><PropMesh kind={th.prop} /></group>;
  }
  const impactAge = rel - release - FLIGHT;
  return { pose, handR, fly, impactAge, landed: impactAge >= 0, releaseT: th.t0 + release };
};
export const Splash: React.FC<{ at: [number, number, number]; age: number }> = ({ at, age }) => (
  <>
    <Ripple p={[at[0], 0, at[2]]} age={age} />
    <Droplets p={[at[0], 0, at[2]]} age={age} />
  </>
);
export const Pawn: React.FC<{ pose: Pose; look: Look; handR?: React.ReactNode; handL?: React.ReactNode }> = (p) => <Character {...p} />;
export { clamp };
