import React from 'react';
import * as THREE from 'three';
import { Cais, PILE } from '../world/cais';
import { Plaza, PLAZA_AT } from '../world/plaza';
import { Env, ENVS, envAt, Lights, Sky, Clouds, Toon, Chair, Shadow, Tufts, toonGrad } from '../world/common';
import { Character, Pose, P, handPos } from '../characters/Rig';
import { TOME, ZECA, ANA, VIL } from '../characters/cast';
import { idle, walk, laugh, speaking, gesture, blinkAt } from '../characters/poses';
import { throwSeq, Splash, PropMesh, ThrowSpec } from './helpers';
import { camAt, CameraRig, CamKey } from '../camera';
import { SHOTS, lineStart, wordStart, wordEnd, quoteOpen, T } from '../lib/timing';
import { clamp, lerp, keys, easeInOut, smoother, easeOutBack, rng, prog } from '../lib/anim';

const S = (id: string) => SHOTS.find((s) => s.id === id)!;
const DOCK_Y = 0.52;

// ---------------------------------------------------------------- S1: gancho + setup
const t1a = Math.max(0.35, wordStart('L1', 'jogava') - 0.95 + 0.05);
const t1b = wordStart('L2', 'jogava') - 0.95 + 0.05;
const TH1: ThrowSpec = { t0: t1a, prop: 'chair', target: [7.2, -0.3, 0.4] };
const TH2: ThrowSpec = { t0: t1b, prop: 'chair', target: [8.4, -0.3, -0.6] };

export const camS1 = (t: number) => camAt(t, [
  { t: 0, pos: [-6.6, 1.2, 7.8], look: [-0.4, 2.9, 0], fov: 58 },
  { t: 6, pos: [-4.8, 1.8, 6.4], look: [1.4, 3.0, 0], fov: 54 },
  { t: S('S1').end, pos: [-2.6, 2.2, 6.4], look: [3.8, 2.0, 0], fov: 54 },
]);
const StackedChairs: React.FC<{ n: number }> = ({ n }) => (
  <group position={[-3.6, DOCK_Y, -0.7]}>{Array.from({ length: n }, (_, i) => <group key={i} position={[0, i * 0.78, 0]} rotation={[0, 1.1 + i * 0.08, 0]}><Chair /></group>)}</group>
);
export const ShotS1: React.FC<{ t: number }> = ({ t }) => {
  const env = ENVS.dawn;
  const base = idle(t, { x: -1.3, y: DOCK_Y, face: 1 });
  const a = throwSeq(t, TH1, { ...base, mouth: 'smile' as const }, TOME, 0);
  const b = throwSeq(t, TH2, { ...base, mouth: 'smile' as const }, TOME, 0.2);
  const useB = t >= TH2.t0 - 0.3;
  const o = useB ? b : a;
  const pile = (a.landed ? 1 : 0) * 1 + (b.landed ? 1 : 0);
  return (
    <>
      <Cais env={env} t={t} pile={Math.min(2, (a.impactAge > 0 ? 1 : 0) + (b.impactAge > 0 ? 1 : 0))} />
      <StackedChairs n={useB && !b.landed ? 3 : 4} />
      <Character pose={o.pose} look={TOME} handR={o.handR} handL={null} />
      {a.fly}{b.fly}
      <Splash at={TH1.target} age={a.impactAge} /><Splash at={TH2.target} age={b.impactAge} />
      <CameraRig spec={camS1(t)} />
    </>
  );
};

// ---------------------------------------------------------------- S2: o zombador (praça)
export const camS2 = (t: number) => { const P0 = PLAZA_AT[0]; return camAt(t, [
  { t: S('S2').start, pos: [P0 + 2.4, 0.9, 7.4], look: [P0 - 0.2, 3.6, 0], fov: 52, roll: 0.11 },
  { t: S('S2').end, pos: [P0 + 1.0, 1.6, 4.6], look: [P0, 3.7, 0], fov: 50, roll: 0.07 },
]); };
export const ShotS2: React.FC<{ t: number }> = ({ t }) => {
  const env = ENVS.morning; const X = PLAZA_AT[0];
  const q0 = wordStart('L3', 'tomé');
  const laughing = t < q0 - 0.1;
  let zb = idle(t, { x: X, y: 0, face: -1, scale: 1.12 });
  zb = laughing ? laugh(t, zb) : { ...speaking(t, zb, ['L3'], 'open'), ...gesture(t, 'R', q0 - 0.1, zb, { up: 1.5 }), brows: [0.6, 0.6] as [number, number] };
  if (!laughing) zb = { ...zb, mouth: quoteOpen(t, 'L3', 'tomé') > 0.05 ? 'open' : 'smirk', open: quoteOpen(t, 'L3', 'tomé') };
  const ex1 = laugh(t + 0.3, idle(t, { x: X + 6.5, z: -3, face: -1, off: 1 }), { amp: 0.6 });
  const ex2 = laugh(t + 0.8, idle(t, { x: X - 6.2, z: -3.5, face: 1, off: 2 }), { amp: 0.8 });
  return (
    <>
      <Plaza env={env} t={t} />
      <Character pose={ex1} look={VIL(1)} /><Character pose={ex2} look={VIL(3)} />
      <Character pose={zb} look={ZECA} />
      <CameraRig spec={camS2(t)} />
    </>
  );
};

// ---------------------------------------------------------------- S3: o herói calmo
export const camS3 = (t: number) => camAt(t, [
  { t: S('S3').start, pos: [-3.6, 1.1, 5.8], look: [-0.9, 3.0, 0], fov: 54 },
  { t: S('S3').end, pos: [-2.9, 1.6, 4.2], look: [-0.8, 3.1, 0], fov: 50 },
]);
export const ShotS3: React.FC<{ t: number }> = ({ t }) => {
  const env = envAt(t, [[S('S3').start, 'dawn'], [S('S3').end, 'morning']]);
  const nod = Math.sin(t * 1.6) * 0.03;
  const smileT = wordStart('L4', 'sorria');
  const base = idle(t, { x: -1.3, y: DOCK_Y, face: 1 });
  const pose: Pose = { ...base, mouth: t > smileT - 0.2 ? 'smile' : 'closed', tilt: nod + (t > smileT ? 0.06 : 0), brows: [0.3, 0.3], look: [0.7, 0.1],
    ...(t > wordStart('L4', 'voltava') ? gesture(t, 'R', wordStart('L4', 'voltava'), base, { up: 0.6 }) : {}) };
  return (
    <>
      <Cais env={env} t={t} pile={2 + clamp((t - S('S3').start) / 6)} />
      <StackedChairs n={4} />
      <Character pose={pose} look={TOME} />
      <CameraRig spec={camS3(t)} />
    </>
  );
};

// ---------------------------------------------------------------- S4: escalada (estações)
const ws = (l: string, w: string) => wordStart(l, w) - 0.95 + 0.05;
const TH_MESA: ThrowSpec = { t0: ws('L5', 'mesa') - 0.2, prop: 'table', target: [6.4, -0.3, 0.2] };
const TH_CAMA: ThrowSpec = { t0: ws('L5', 'cama') - 0.2, prop: 'bed', target: [7.6, -0.3, -0.5] };
const TH_PORTA: ThrowSpec = { t0: ws('L6', 'porta') - 0.2, prop: 'door', target: [8.8, -0.3, 0.3] };
export const camS4 = (t: number) => camAt(t, [
  { t: S('S4').start, pos: [-5.8, 2.3, 9.8], look: [0.6, 2.7, 0], fov: 64 },
  { t: wordStart('L6', 'inverno'), pos: [-5.2, 2.5, 9.4], look: [1.4, 2.5, -0.3], fov: 64 },
  { t: S('S4').end, pos: [-4.7, 2.8, 9.2], look: [2.0, 2.3, -0.5], fov: 64 },
]);
export const ShotS4: React.FC<{ t: number }> = ({ t }) => {
  const a = S('S4').start, e = S('S4').end;
  const env = envAt(t, [[a, 'autumn'], [wordStart('L5', 'cama'), 'dusk'], [wordStart('L6', 'inverno') + 0.5, 'winter'], [e, 'winter']]);
  const base0 = idle(t, { x: -1.3, y: DOCK_Y, face: 1 });
  const th = [TH_MESA, TH_CAMA, TH_PORTA];
  const outs = th.map((s) => throwSeq(t, s, { ...base0, mouth: 'smile' as const }, TOME, 0.15));
  let active = outs[0]; th.forEach((s, i) => { if (t >= s.t0 - 0.3) active = outs[i]; });
  const pile = 3 + (outs[0].landed ? 5 : 0) + (outs[1].landed ? 6 : 0) + (outs[2].landed ? 6 : 0) + clamp((t - a) / 5) * 3;
  const crowdT = wordStart('L6', 'louco') - 0.8;
  const crowd = [[-3.5, 0, 2.2, 0], [-4.5, 1, 2.9, 1], [-5.5, 2, 3.4, 2], [-2.7, 3, 3.0, 3], [-3.9, 4, 3.8, 4]];
  return (
    <>
      <Cais env={env} t={t} pile={pile} lit={env.snow > 0.5 ? 1 : 0} />
      <StackedChairs n={3} />
      <Character pose={active.pose} look={TOME} handR={active.handR} />
      {outs.map((o, i) => <React.Fragment key={i}>{o.fly}<Splash at={th[i].target} age={o.impactAge} /></React.Fragment>)}
      {t > crowdT - 2.5 && crowd.map(([x, k, z, off], i) => {
        const appear = clamp((t - (crowdT - 2.5 + i * 0.25)) / 0.3); if (appear <= 0) return null;
        let p = idle(t, { x, y: DOCK_Y, z, face: 1, off, scale: 0.78 * appear });
        p = t > crowdT ? laugh(t + off * 0.2, p, { amp: 0.6 }) : { ...p, ...gesture(t, 'R', crowdT - 2.0 + i * 0.1, p), mouth: 'smirk' as const };
        return <Character key={i} pose={p} look={VIL(k)} />;
      })}
      <CameraRig spec={camS4(t)} />
    </>
  );
};

// ---------------------------------------------------------------- S5: "você sabe" (quarto-metáfora)
export const ROOM_AT: [number, number, number] = [600, 0, 0];
const jarCoins = (n: number) => Array.from({ length: n }, (_, i) => ({ x: ((i * 7) % 5 - 2) * 0.19, y: 0.12 + Math.floor(i / 5) * 0.12, z: (((i * 3) % 4) - 1.5) * 0.15 }));
const S5 = () => {
  const R = ROOM_AT[0], a = S('S5').start;
  const tBreak = wordStart('L8', 'quebra'), tFix = wordStart('L8', 'único');
  const w0 = tBreak + 0.5, w1 = tFix - 0.3;
  return { R, a, tBreak, tFix, w0, w1, coin0: a + 0.7, dt: 0.28 };
};
export const camS5 = (t: number) => {
  const { R, a, tBreak, w0, w1, tFix } = S5();
  const u = smoother((t - w0) / (w1 - w0));
  const cx = lerp(R + 1.9, R + 11.2, u);
  const zoom = smoother((t - a) / (tBreak - a)); const end = smoother((t - tFix) / 1.5);
  return camAt(t, [{ t: 0, pos: [cx, lerp(2.9, 2.6, zoom), lerp(8.6, 7.2, zoom) - end * 0.6], look: [cx + 0.1, 2.7, 0], fov: lerp(56, 52, zoom) }, { t: 999, pos: [cx, 2.6, 7], look: [cx + 0.1, 2.7, 0], fov: 52 }]);
};
export const ShotS5: React.FC<{ t: number }> = ({ t }) => {
  const env = ENVS.room; const { R, a, tBreak, tFix, w0, w1, coin0, dt } = S5();
  const walkU = smoother((t - w0) / (w1 - w0));
  const jarPos: [number, number, number] = [R + 2.3, 1.65, -0.2];
  const mouth: [number, number, number] = [jarPos[0], jarPos[1] + 1.7, jarPos[2]];
  const landed = (i: number) => t >= coin0 + i * dt + 0.26;
  const nCoins = t < tBreak ? Array.from({ length: 30 }, (_, i) => i).filter(landed).length : 24;
  const carried = t > w0 - 0.3;
  // Ana
  const anaBase = idle(t, { x: R + 0.5, y: 0, face: 1 });
  let ana: Pose;
  if (t < tBreak + 0.1) {
    const ph = ((t - coin0) % dt) / dt;
    ana = { ...anaBase, armR: [2.0 + Math.sin(ph * Math.PI * 2) * 0.12, 0.35], armL: [0.2, 0.2], mouth: 'smile', bob: anaBase.bob + Math.abs(Math.sin(ph * Math.PI)) * 0.04, look: [0.9, 0.4] };
  } else if (t < w1) {
    ana = { ...anaBase, ...walk(t, { speed: 1.6 }), x: R + 0.5 + walkU * 9.9, mouth: 'worry', brows: [-0.5, -0.5] };
    ana = { ...ana, armR: [0.9, 1.1], armL: [0.7, 1.0] };
  } else {
    const rest = idle(t, { x: R + 10.4, y: 0, face: 1 });
    ana = { ...gesture(t, 'R', tFix + 0.9, rest, { up: 1.3 }), mouth: 'smile' as const, brows: [0.5, 0.5] };
  }
  const anaHand = handPos(ana, 'R', ANA);
  const ex = (x: number, off: number) => { const base = idle(t, { x, z: -2.5, face: -1, off, y: 0, scale: 0.88 }); const sh = Math.sin((t + off) * 4.2) * 0.12;
    return { ...base, tilt: sh, mouth: 'smirk' as const, brows: [-0.6, 0.6] as [number, number], armL: [0.6 + Math.sin(t * 3 + off) * 0.1, 1.5] as [number, number], armR: [0.7, 1.4] as [number, number] }; };
  // carro
  const carX = R + 12.7; const brokenU = clamp((t - tBreak) / 0.35); const fixed = clamp((t - tFix - 0.5) / 0.3);
  const wheelOut = brokenU * (1 - fixed);
  const carBounce = fixed > 0 ? Math.abs(Math.sin((t - tFix - 0.5) * 9)) * 0.25 * clamp(1 - (t - tFix - 0.8) / 1.2) : 0;
  const calAngle = t < tBreak ? -clamp(((t - a) % 0.5) * 6) * 1.4 : 0;
  const coinIdx = Math.floor((t - coin0) / dt);
  const cu = ((t - coin0) - coinIdx * dt) / dt;
  const coinHand = handPos({ ...anaBase, armR: [2.0, 0.35] }, 'R', ANA);
  return (
    <>
      <fog attach="fog" args={[new THREE.Color('#f1d6ae'), 40, 120]} />
      <Lights env={env} at={ROOM_AT} />
      <mesh position={[R + 6, 0, -4]} rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[80, 40]} /><Toon color="#d8b88e" /></mesh>
      <mesh position={[R + 6, 7, -6]}><boxGeometry args={[60, 16, 0.4]} /><Toon color="#f1d6ae" /></mesh>
      <mesh position={[R + 6, 0.5, -5.7]}><boxGeometry args={[60, 1, 0.3]} /><Toon color="#c9986a" /></mesh>
      <mesh position={[R + 1.4, 6.2, -5.7]}><boxGeometry args={[4.0, 4.4, 0.1]} /><meshBasicMaterial color="#ffe3a8" /></mesh>
      {[-1, 0, 1].map((i) => <mesh key={i} position={[R + 1.4 + i * 1.3, 6.2, -5.62]}><boxGeometry args={[0.1, 4.4, 0.1]} /><Toon color="#8a5a3a" /></mesh>)}
      <mesh position={[R + 1.4, 6.2, -5.62]}><boxGeometry args={[4.0, 0.1, 0.1]} /><Toon color="#8a5a3a" /></mesh>
      <mesh position={[R + 1.4, 3.2, -2]} rotation={[-0.6, 0, 0]}><planeGeometry args={[3.4, 8]} /><meshBasicMaterial color="#ffe3a8" transparent opacity={0.15} depthWrite={false} /></mesh>
      <group position={[R + 5.2, 6, -5.5]}>
        <mesh><boxGeometry args={[2.4, 2.8, 0.1]} /><Toon color="#fbf6ee" /></mesh>
        <mesh position={[0, 1.1, 0.07]}><boxGeometry args={[2.4, 0.6, 0.05]} /><Toon color="#d9625f" /></mesh>
        <group position={[0, 0.8, 0.1]} rotation={[calAngle, 0, 0]}><mesh position={[0, -0.7, 0]}><boxGeometry args={[2.2, 1.4, 0.03]} /><Toon color="#ffffff" /></mesh></group>
      </group>
      {/* mesa + pote */}
      <group position={[R + 2.3, 0, -0.2]}>
        <mesh position={[0, 1.55, 0]}><boxGeometry args={[2.4, 0.2, 1.5]} /><Toon color="#c48650" /></mesh>
        {[[-1.0, -0.55], [1.0, -0.55], [-1.0, 0.55], [1.0, 0.55]].map((l, i) => <mesh key={i} position={[l[0], 0.75, l[1]]}><boxGeometry args={[0.16, 1.5, 0.16]} /><Toon color="#c48650" /></mesh>)}
      </group>
      {!carried && (
        <group position={jarPos}>
          <mesh position={[0, 0.8, 0]}><cylinderGeometry args={[0.7, 0.64, 1.6, 16]} /><meshToonMaterial color="#cfe6f2" transparent opacity={0.45} gradientMap={toonGrad} /></mesh>
          {jarCoins(nCoins).map((c, i) => <mesh key={i} position={[c.x, c.y, c.z]} rotation={[Math.PI / 2, 0, 0]}><cylinderGeometry args={[0.2, 0.2, 0.06, 12]} /><meshBasicMaterial color="#f6c34a" /></mesh>)}
        </group>
      )}
      {t >= coin0 && t < tBreak && coinIdx >= 0 && (
        <mesh position={[lerp(coinHand[0], mouth[0], cu), lerp(coinHand[1], mouth[1], cu) + 1.6 * Math.sin(cu * Math.PI), jarPos[2]]} rotation={[Math.PI / 2, 0, t * 14]}><cylinderGeometry args={[0.2, 0.2, 0.06, 12]} /><meshBasicMaterial color="#f6c34a" /></mesh>
      )}
      {/* carro de brinquedo */}
      <group position={[carX, carBounce, -0.5]} scale={0.72} rotation={[0, 0, -brokenU * 0.14 * (1 - fixed)]}>
        <Shadow p={[0, 0.03 - carBounce, 0]} s={[3.2, 1.2]} />
        <mesh position={[0, 1.5, 0]}><boxGeometry args={[5.4, 1.3, 2.4]} /><Toon color="#d9625f" /></mesh>
        <mesh position={[-0.4, 2.55, 0]}><boxGeometry args={[2.8, 1.1, 2.1]} /><Toon color="#e8dcc6" /></mesh>
        {[[-1.8, 1], [1.8, 1], [-1.8, -1], [1.8, -1]].map((w, i) => {
          const isFront = i === 1; const off = isFront ? wheelOut : 0;
          return <mesh key={i} position={[w[0] + off * 3.5, 0.65 + (isFront ? Math.sin(Math.min(off, 1) * 3) * 1.4 - off * 0.5 : 0), w[1] * 1.3 + (isFront ? off * 1.8 : 0)]} rotation={[Math.PI / 2, 0, off * 9]}><cylinderGeometry args={[0.68, 0.68, 0.45, 16]} /><Toon color="#3a3050" /></mesh>;
        })}
        {brokenU > 0 && fixed < 1 && Array.from({ length: 5 }, (_, i) => { const a2 = clamp((t - tBreak - i * 0.18) / 1.6); return <mesh key={i} position={[1.6 + Math.sin(i) * 0.3, 3 + a2 * 3, 0.6]} scale={0.4 + a2 * 1.0}><sphereGeometry args={[1, 10, 8]} /><meshBasicMaterial color="#b5a6c4" transparent opacity={0.7 * (1 - a2)} /></mesh>; })}
      </group>
      <Character pose={ana} look={ANA} handR={carried && t < tFix + 0.9 ? (
        <group position={[0.1, -0.35, 0.05]} scale={0.62}><mesh position={[0, 0.6, 0]}><cylinderGeometry args={[0.7, 0.64, 1.6, 16]} /><meshToonMaterial color="#cfe6f2" transparent opacity={0.55} gradientMap={toonGrad} /></mesh>
          {jarCoins(24).map((c, i) => <mesh key={i} position={[c.x, c.y - 0.1, c.z]} rotation={[Math.PI / 2, 0, 0]}><cylinderGeometry args={[0.2, 0.2, 0.06, 12]} /><meshBasicMaterial color="#f6c34a" /></mesh>)}</group>) : null} />
      <Character pose={ex(R + 4.4, 0.4)} look={VIL(0)} />
      <Character pose={ex(R + 5.9, 1.1)} look={VIL(2)} />
      <CameraRig spec={camS5(t)} />
    </>
  );
};

// ---------------------------------------------------------------- S6: pagamento (a ponte)
const tSink = wordStart('L9', 'afundou') - 0.5;
const tWalk6 = wordStart('L10', 'caminhou');
const tZ6 = wordStart('L11', 'zeca');
const TOME_DUR = 7.0;
const yWater = (x: number) => lerp(DOCK_Y, -0.08, smoother((x - 1.0) / 1.0));
const tomeX6 = (t: number) => lerp(0.2, 30.5, easeInOut(clamp((t - tWalk6) / TOME_DUR)));
const zecaX6 = (t: number) => lerp(1.5, 29, easeInOut(clamp((t - (tZ6 - 1.2)) / 4.6)));
export const camS6 = (t: number) => {
  const t0 = tWalk6 - 0.9;
  if (t < t0) return camAt(t, [
    { t: S('S6').start, pos: [-4, 2.4, 11], look: [8, 1.4, -3], fov: 60 },
    { t: wordStart('L9', 'ilha'), pos: [4, 3, 15], look: [18, 0.6, -6], fov: 60 },
    { t: t0, pos: [-3.3, 2.1, 8.8], look: [1.2, 2.4, 0], fov: 56 },
  ]);
  const tx = t < tZ6 - 0.8 ? tomeX6(t) : lerp(tomeX6(t), zecaX6(t) + 1.2, smoother((t - (tZ6 - 0.8)) / 1.2));
  return camAt(t, [{ t: 0, pos: [tx - 3.3, 2.1 + 0.2 * smoother((t - t0) / 1.5), 8.8], look: [tx + 1.5, 2.4, 0], fov: 56 }, { t: 999, pos: [tx - 3.3, 2.3, 8.8], look: [tx + 1.5, 2.4, 0], fov: 56 }]);
};
export const ShotS6: React.FC<{ t: number }> = ({ t }) => {
  const a = S('S6').start;
  const env = envAt(t, [[a, 'dusk'], [S('S6').end, 'dusk']]);
  const tx = tomeX6(t); const walking = t > tWalk6 && t < tWalk6 + TOME_DUR;
  let tome = idle(t, { x: -1.3, y: DOCK_Y, face: 1 });
  tome = { ...tome, mouth: 'smile' as const };
  if (t >= tWalk6 - 0.6 && t < tWalk6) tome = { ...tome, x: lerp(-1.3, 0.2, smoother((t - tWalk6 + 0.6) / 0.6)) };
  if (walking) tome = { ...tome, ...walk(t, { speed: 1.7 }), x: tx, y: yWater(tx) };
  if (t >= tWalk6 + TOME_DUR) tome = { ...gesture(t, 'R', tWalk6 + TOME_DUR + 0.3, idle(t, { x: tx, y: -0.08, face: -1 }), { up: 1.0 }), mouth: 'smile' as const };
  const zx = zecaX6(t); const zRun = t > tZ6 - 1.2 && t < tZ6 + 3.4;
  let zeca = { ...idle(t, { x: zx, y: yWater(zx), face: 1, off: 1.3 }) };
  if (zRun) zeca = { ...zeca, ...walk(t, { speed: 2.3, off: 0.3 }), x: zx, y: yWater(zx), armL: [2.6, 0.2], armR: [2.6, 0.2], mouth: 'smile' as const };
  else if (t >= tZ6 + 3.4) zeca = { ...zeca, face: -1, armL: [2.6, 0.2], armR: [2.6, 0.2], mouth: 'laugh' as const, open: 0.6 };
  const sink = clamp((t - tSink) / 2.2);
  const reveal = wordStart('L10', 'eram') - 0.2;
  const pileShow = t < reveal ? 26 : lerp(26, PILE.length, clamp((t - reveal) / 1.2));
  const showZ = t > tZ6 - 1.2;
  return (
    <>
      <Cais env={env} t={t} pile={pileShow} boatVisible boatSink={sink} lit={1} />
      <Character pose={tome} look={TOME} />
      {showZ && <Character pose={zeca} look={ZECA} />}
      {showZ && <group position={[zx, zeca.y + 4.75 + zeca.bob, 0.1]}><mesh rotation={[0, 0, 1.45]} scale={[1, 1.6, 1]}><capsuleGeometry args={[0.22, 1.5, 4, 10]} /><Toon color="#e4a352" /></mesh></group>}
      {sink > 0 && sink < 1 && Array.from({ length: 10 }, (_, i) => { const r = rng(i + 3)(); const u = clamp((t - tSink - r * 0.8) / 1.2); return <mesh key={i} position={[16.4 + r * 2.5, 0.1 + u * 2.0, -6 + (i % 3) * 0.5]} scale={0.12 + r * 0.14}><sphereGeometry args={[1, 8, 6]} /><meshBasicMaterial color="#ffffff" transparent opacity={0.8 * (1 - u)} /></mesh>; })}
      <CameraRig spec={camS6(t)} />
    </>
  );
};

// ---------------------------------------------------------------- S7: loop
export const camS7 = (t: number) => camAt(t, [
  { t: S('S7').start, pos: [-7.8, 1.5, 8.4], look: [-1.4, 2.9, 0], fov: 59 },
  { t: S('S7').end, pos: [-6.6, 1.2, 7.8], look: [-0.4, 2.9, 0], fov: 58 },
]);
export const ShotS7: React.FC<{ t: number }> = ({ t }) => {
  const env = envAt(t, [[S('S7').start, 'dusk'], [S('S7').start + 1.2, 'dawn']]);
  const a = S('S7').start;
  const zx = lerp(-17, -3.1, easeInOut((t - a) / 4.4));
  const moving = t - a < 4.4;
  let zeca = { ...idle(t, { x: zx, y: zx < -11 ? 0.5 : DOCK_Y, face: 1, off: 0.6 }), ...(moving ? walk(t, { speed: 1.5 }) : {}), x: zx, y: zx < -11 ? 0.5 : DOCK_Y, armL: [1.0, 0.6] as [number, number], armR: [1.05, 0.55] as [number, number], mouth: 'closed' as const };
  const tome = { ...idle(t, { x: -1.3, y: DOCK_Y, face: 1 }), mouth: 'smile' as const, tilt: moving ? 0.0 : -0.08, look: [-0.6, 0] as [number, number] };
  return (
    <>
      <Cais env={env} t={t} pile={PILE.length} />
      <Character pose={{ ...tome, face: -1, x: -0.4 }} look={TOME} />
      <Character pose={zeca} look={ZECA} handR={<group position={[0.15, -0.35, 0.05]} rotation={[0, 1.1, -0.5]} scale={0.85}><Chair /></group>} />
      <CameraRig spec={camS7(t)} />
    </>
  );
};
