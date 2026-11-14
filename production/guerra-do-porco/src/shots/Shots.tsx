import React from 'react';
import * as THREE from 'three';
import { Island } from '../world/island';
import { ShipDeck, DECK_AT } from '../world/ships';
import { Soldiers } from '../world/soldiers';
import { ENVS, envAt } from '../world/common';
import { Character, Pose, Look, handFrame, Disc, INK } from '../characters/Rig';
import { Pig, PigPose } from '../characters/Pig';
import { CUTLAR, GRIFFIN, SOLDIER, BAYNES, AIDE } from '../characters/cast';
import { idle, march, aimFire, smug, shock, laugh, stopHand, point } from '../characters/poses';
import { camAt, CameraRig } from '../camera';
import { shot, wordStart, wordEnd, lineStart, BANG1, BANG2, T } from '../lib/timing';
import { Note, Spyglass, Grave } from '../world/props';
import { aimUp, muzzleWorld, RifleInHand, GunSmoke, MuzzleFlash } from './helpers';
import { clamp, lerp, keys, easeInOut, easeOut, smoother } from '../lib/anim';

const S = shot;
const PIG0 = { x: 1.4, z: 1.2 }; const CUT = { x: -0.5, z: 5.0 };                    // lugar do porco no gancho (e do túmulo no fim → loop)
const CAM_LOOP = { pos: [1.8, 1.1, 11.4] as [number, number, number], look: [0.9, 1.9, 2.6] as [number, number, number], fov: 56 };
const flipU = (t: number, t0: number) => clamp((t - t0) / 0.5);
const pigPose = (t: number, o: Partial<PigPose>): PigPose => ({ x: 0, y: 0, z: PIG0.z, face: -1, scale: 1.25, t, mode: 'eat', flip: 0, hop: 0, ...o });

// ---------------------------------------------------------------- S1 — gancho (tiro + revelação da guerra)
export const camS1 = (t: number) => camAt(t, [
  { t: 0, pos: CAM_LOOP.pos, look: CAM_LOOP.look, fov: CAM_LOOP.fov },
  { t: 1.5, pos: [1.4, 0.95, 9.2], look: [0.9, 1.7, 2.2], fov: 52 },
  { t: 2.2, pos: [1.6, 2.4, 9.8], look: [0.8, 3.0, -10], fov: 58 },
  { t: S('S1').end + 0.3, pos: [4.5, 7.0, 15.5], look: [-6, 3.6, -70], fov: 64 },
]);
export const ShotS1: React.FC<{ t: number }> = ({ t }) => {
  const env = ENVS.golden, tr = BANG1 - 1.0;
  const base = idle(t, { x: CUT.x, y: 0, z: CUT.z, face: 1 });
  const up = aimUp(t, -0.9, BANG1);
  let c: Pose = aimFire(t, base, { t0: -0.9, tFire: BANG1 });
  if (t > BANG1 + 0.45) c = { ...c, lid: 0.55, brows: [0.2, -0.3], mouth: 'smirk' };
  const u = flipU(t, BANG1 + 0.04), dead = t > BANG1 + 0.04;
  const pig = pigPose(t, { x: PIG0.x, mode: dead ? 'dead' : 'eat', flip: easeOut(u), hop: dead ? 2.1 * Math.sin(Math.min(1, u) * Math.PI) : 0, shock: 0 });
  const m = muzzleWorld(c, CUTLAR, 1.85);
  return (
    <>
      <Island env={env} t={t} garden={{ eaten: { x: PIG0.x - 0.8, z: PIG0.z, r: 2.0 } }} fleet={t > 2.2} fleetU={smoother((t - 2.2) / 1.0)} />
      <Character pose={c} look={CUTLAR} handR={<RifleInHand up={up} />} />
      <Pig pig={pig} />
      <MuzzleFlash p={m} t={t} t0={BANG1} s={1.1} /><GunSmoke t={t} t0={BANG1 + 0.05} at={[m[0] + 0.4, m[1], m[2]]} />
      <CameraRig spec={camS1(t)} />
    </>
  );
};

// ---------------------------------------------------------------- S2 — setup (o porco invade a horta; "Ele atirou")
const T_GAP = 4.95, T_EAT = 6.0, CUT2 = CUT, PIG2 = { x: 2.7, z: 0.9 };
export const camS2 = (t: number) => camAt(t, [
  { t: S('S2').start - 0.2, pos: [21.5, 2.0, 7.0], look: [22, 8.6, -8], fov: 66, roll: 0.05 },
  { t: 4.55, pos: [16.2, 1.8, 10.0], look: [11.2, 2.7, 3.4], fov: 58, roll: -0.03 },
  { t: wordStart('L2', 'horta') + 0.2, pos: [6.5, 1.5, 11.6], look: [2.2, 2.4, 2.4], fov: 57 },
  { t: S('S2').end + 0.3, pos: [1.3, 1.5, 11.8], look: [1.0, 2.6, 2.6], fov: 54, roll: 0.05 },
]);
export const ShotS2: React.FC<{ t: number }> = ({ t }) => {
  const env = ENVS.golden;
  const tNotice = wordStart('L2', 'horta') + 0.1, t0 = BANG2 - 1.0;
  const trot = clamp((t - 3.9) / (T_EAT - 3.9));
  const px = lerp(14.5, PIG2.x, easeInOut(trot)), pz = lerp(2.6, PIG2.z, easeInOut(clamp((t - 5.3) / 0.9)));
  const pig = pigPose(t, { x: px, z: pz, mode: trot < 1 ? 'trot' : 'eat' });
  const base = idle(t, { x: CUT2.x, y: 0, z: CUT2.z, face: 1 });
  let c: Pose = aimFire(t, base, { t0, tFire: BANG2 });
  if (t > tNotice - 0.1 && t < t0) c = { ...shock(t, c, tNotice), mouth: 'line' };
  const up = aimUp(t, t0, BANG2); const m = muzzleWorld(c, CUTLAR, 1.85);
  return (
    <>
      <Island env={env} t={t} garden={{ eaten: t > T_EAT ? { x: px - 0.8, z: pz, r: 2.2 } : undefined }} />
      <Character pose={c} look={CUTLAR} handR={<RifleInHand up={up} />} />
      <Pig pig={pig} />
      <MuzzleFlash p={m} t={t} t0={BANG2} s={1.2} /><GunSmoke t={t} t0={BANG2 + 0.05} at={[m[0] + 0.4, m[1], m[2]]} />
      <CameraRig spec={camS2(t)} />
    </>
  );
};

// ---------------------------------------------------------------- S3 — o zombador (cem dólares × dez)
const X_C = 4.7, X_G = 6.9, X_P = 5.8, Z3 = 2.4;
export const camS3 = (t: number) => camAt(t, [
  { t: S('S3').start - 0.2, pos: [5.4, 0.8, 10.2], look: [5.8, 2.7, 2.4], fov: 56, roll: 0.13 },
  { t: S('S3').end + 0.3, pos: [5.7, 1.3, 8.0], look: [5.9, 2.9, 2.4], fov: 52, roll: 0.09 },
]);
export const ShotS3: React.FC<{ t: number }> = ({ t }) => {
  const env = ENVS.golden;
  const tCem = wordStart('L3', 'cem') - 0.35, tDez = wordStart('L3', 'ofereceu') - 0.2, tLaugh = wordStart('L3', 'dez') - 0.05;
  let g = idle(t, { x: X_G, y: 0, z: Z3, face: -1, off: 0.7 });
  g = smug(g);
  const gUp = keys(t, [[tCem, 0], [tCem + 0.3, 1]], easeInOut);
  g = { ...g, armR: [lerp(-0.1, 1.75, gUp), lerp(0.12, 0.9, gUp)], armL: [lerp(0.1, 1.3, keys(t, [[S('S3').start + 0.3, 0], [S('S3').start + 0.6, 1]], easeInOut)), 0.1] };
  if (t > tLaugh) g = laugh(t, { ...g, armR: g.armR }, { amp: 0.8 });
  let c = idle(t, { x: X_C, y: 0, z: Z3, face: 1, off: 0.2 });
  const cUp = keys(t, [[tDez, 0], [tDez + 0.3, 1]], easeInOut);
  c = { ...c, eye: 'lid', lid: 0.35, angry: 0.7, brows: [-0.2, -0.2], mouth: 'teeth', armR: [lerp(-0.1, 1.6, cUp), lerp(0.12, 0.8, cUp)], sweat: t > tDez ? (t - tDez) * 1.1 : 0 };
  const pig = pigPose(t, { x: X_P, face: 1, mode: 'dead', flip: 1, z: Z3 + 0.4, scale: 1.2 });
  // a mão levantada gira o referencial: contra-gira a nota (e pré-espelha se o personagem está espelhado) para o texto ficar legível
  const angG = handFrame(g, 'R', GRIFFIN).ang, angC = handFrame(c, 'R', CUTLAR).ang;
  const hn = <group position={[0.1, -0.25, 0.1]} rotation={[0, 0, -angG + 0.1]} scale={[-1, 1, 1]}><group position={[0.75, 0, 0]}><Note label="$100" s={1.05} /></group></group>;
  const hc = <group position={[0.05, -0.2, 0.1]} rotation={[0, 0, -angC - 0.12]}><group position={[0.5, 0, 0]}><Note label="$10" s={0.68} /></group></group>;
  return (
    <>
      <Island env={env} t={t} garden={{ eaten: { x: 3.0, z: PIG0.z, r: 2.0 } }} />
      <Pig pig={pig} />
      <Character pose={g} look={GRIFFIN} handR={t > tCem ? hn : null} />
      <Character pose={c} look={CUTLAR} handR={t > tDez ? hc : null} />
      <CameraRig spec={camS3(t)} />
    </>
  );
};

// ---------------------------------------------------------------- S4 — escalada (soldados e navios)
const SPEED4 = 4.9;
const bx = (t: number) => -52 + SPEED4 * (t - S('S4').start);
export const camS4 = (t: number) => {
  const tn = wordStart('L4', 'navios') - 0.5, u = smoother((t - tn) / 1.0);
  const b = bx(t);
  const a = { pos: [b - 6.5, 1.15, -18.5] as [number, number, number], look: [b + 1.5, 2.5, -30] as [number, number, number], fov: 62 };
  const ship = { pos: [b - 1.5, 6.4, -21] as [number, number, number], look: [8, 3.0, -80] as [number, number, number], fov: 60 };
  const mix = (p: number[], q: number[]) => p.map((v, i) => lerp(v, q[i], u)) as [number, number, number];
  return camAt(t, [{ t: 0, pos: mix(a.pos, ship.pos), look: mix(a.look, ship.look), fov: lerp(a.fov, ship.fov, u), roll: 0.02 }, { t: 999, pos: mix(a.pos, ship.pos), look: mix(a.look, ship.look), fov: lerp(a.fov, ship.fov, u), roll: 0.02 }]);
};
export const ShotS4: React.FC<{ t: number }> = ({ t }) => {
  const env = ENVS.golden; const b = bx(t);
  const lead = { ...idle(t, { x: b + 5.3, y: 0, z: -22.5, face: 1 }), ...march(t), eye: 'lid' as const, lid: 0.4, angry: 0.3, brows: [0.1, 0.1] as [number, number], mouth: 'line' as const, armR: [0.3, 0.2] as [number, number] };
  return (
    <>
      <Island env={env} t={t} fleet={t > wordStart('L4', 'navios') - 1.0} fleetU={smoother((t - (wordStart('L4', 'navios') - 0.95)) / 1.0)} />
      <Soldiers t={t} xc={b} z={-27} cols={8} rows={5} />
      <Character pose={lead} look={SOLDIER} />
      <CameraRig spec={camS4(t)} />
    </>
  );
};

// ---------------------------------------------------------------- S5 — o almirante recusa (convés)
export const camS5 = (t: number) => { const X = DECK_AT[0]; return camAt(t, [
  { t: S('S5').start - 0.2, pos: [X + 0.9, 1.1, 9.2], look: [X - 0.1, 2.8, 0], fov: 54, roll: -0.1 },
  { t: wordStart('L5', 'recusou') + 0.2, pos: [X + 0.6, 1.3, 7.6], look: [X + 0.2, 3.0, 0], fov: 50, roll: -0.07 },
  { t: S('S5').end + 0.3, pos: [X + 0.9, 1.6, 5.4], look: [X + 1.0, 3.3, 0], fov: 46, roll: -0.04 },
]); };
export const ShotS5: React.FC<{ t: number }> = ({ t }) => {
  const X = DECK_AT[0]; const tR = wordStart('L5', 'recusou') - 0.1;
  let b = idle(t, { x: X + 1.0, y: 0, z: 0, face: -1 }); b = { ...b, eye: 'lid', lid: 0.58, brows: [0.15, 0.15], mouth: 'line', armL: [0.2, 0.5] };
  if (t > tR) b = stopHand(t, b, tR);
  let a = idle(t, { x: X - 1.3, y: 0, z: 0.4, face: 1, off: 1 });
  a = { ...a, eye: 'wide', brows: [0.6, 0.6], mouth: 'shout', open: 0.6, armR: [lerp(-0.1, 2.2, keys(t, [[S('S5').start, 0], [S('S5').start + 0.4, 1]], easeInOut)), 0.1] };
  if (t > tR + 0.25) a = shock(t, { ...a, armR: [0.3, 0.3], mouth: 'oh' }, tR + 0.25);
  return (
    <>
      <ShipDeck env={ENVS.bright} t={t} />
      <Character pose={a} look={AIDE} handR={t < tR + 0.25 ? <group position={[0, -0.1, 0.05]} rotation={[0, 0, Math.PI]}><Spyglass /></group> : null} />
      <Character pose={b} look={BAYNES} />
      <CameraRig spec={camS5(t)} />
    </>
  );
};

// ---------------------------------------------------------------- S6 — o túmulo (loop com o 1º quadro)
export const camS6 = (t: number) => camAt(t, [
  { t: S('S6').start - 0.2, pos: [1.6, 0.8, 6.6], look: [1.3, 1.5, 1.2], fov: 50 },
  { t: T.total - 0.3, pos: CAM_LOOP.pos, look: CAM_LOOP.look, fov: CAM_LOOP.fov },
  { t: 999, pos: CAM_LOOP.pos, look: CAM_LOOP.look, fov: CAM_LOOP.fov },
]);
export const ShotS6: React.FC<{ t: number }> = ({ t }) => {
  const env = ENVS.dusk; const tHat = wordStart('L5', 'só') - 0.15;
  const hat = (c: string) => <group position={[0.0, -0.05, 0.1]}><Disc p={[0, 0, 0]} s={[0.4, 0.12]} color={INK} /><Disc p={[0, 0, 0.01]} s={[0.36, 0.09]} color={c} /></group>;
  const off = (b: Pose, f: Pose): Pose => ({ ...b, armR: [lerp(b.armR[0], 0.95, keys(t, [[tHat, 0], [tHat + 0.3, 1]], easeInOut)), lerp(b.armR[1], 2.2, keys(t, [[tHat, 0], [tHat + 0.3, 1]], easeInOut))], tilt: b.tilt + 0.12 * keys(t, [[tHat, 0], [tHat + 0.4, 1]], easeInOut), mouth: 'frown', lid: 0.6, brows: [-0.3, -0.3], angry: -0.5 });
  const hatOff = t > tHat + 0.1;
  const c = off(idle(t, { x: -0.3, y: 0, z: 3.7, face: 1, off: 0.3 }), {} as Pose);
  const g = off(idle(t, { x: 2.9, y: 0, z: 3.7, face: -1, off: 0.9 }), {} as Pose);
  return (
    <>
      <Island env={env} t={t} garden={{ eaten: { x: PIG0.x, z: PIG0.z, r: 1.6 } }} />
      <Grave p={[PIG0.x, 0, PIG0.z]} t={t} />
      <Character pose={c} look={hatOff ? { ...CUTLAR, hat: undefined } : CUTLAR} handR={hatOff ? hat('#e8c068') : null} />
      <Character pose={g} look={hatOff ? { ...GRIFFIN, hat: undefined } : GRIFFIN} handR={hatOff ? hat('#8c7a58') : null} />
      <CameraRig spec={camS6(t)} />
    </>
  );
};
