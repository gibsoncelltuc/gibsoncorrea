import React, { useLayoutEffect, useMemo, useRef } from 'react';
import * as THREE from 'three';
import { Env, Toon, Lights, Sky, Clouds, Tufts, Shafts, Dust, FlagPole, Shadow } from './common';
import { Fir, Cabin, Fence, Garden, Sheep, Tent, SignPost, Cannon, Box } from './props';
import { Sea, Fleet } from './ships';
import { grassTex, sandTex, flagUS, flagUK } from './tex';
import { rng, mixHex } from '../lib/anim';

export const SHORE_Z = -56;
/** Ilha (San Juan, 1859): horta do americano + cabana, pasto britânico com ovelhas, fronteira (cerca com brecha), acampamento, praia, mar, Mount Baker. */
export const Island: React.FC<{ env: Env; t: number; garden?: { eaten?: { x: number; z: number; r: number } }; fleet?: boolean; fleetU?: number; foam?: boolean; shafts?: boolean }> = ({ env, t, garden, fleet = false, fleetU = 1, shafts = true }) => {
  const trees = useMemo(() => { const r = rng(21); return [
    ...Array.from({ length: 16 }, () => ({ x: -110 + r() * 46, z: -34 + r() * 40, s: 0.7 + r() * 0.5 })),
    ...Array.from({ length: 14 }, () => ({ x: 38 + r() * 70, z: -36 + r() * 40, s: 0.7 + r() * 0.6 })),
  ]; }, []);
  const sheep = useMemo(() => { const r = rng(8); return Array.from({ length: 6 }, () => ({ x: 14 + r() * 16, z: -2 + r() * 14, f: r() < 0.5 ? 1 : -1, ph: r() * 6 })); }, []);
  const leafA = mixHex('#2f5a58', '#9a8a3a', 0.35), leafB = mixHex('#3a6a5a', '#b8963a', 0.4);
  return (
    <group>
      <fog attach="fog" args={[new THREE.Color(env.fog), 90, 420]} />
      <Lights env={env} /><Sky env={env} /><Clouds t={t} />
      <mesh position={[0, 0, 22]} rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[560, 160]} /><meshToonMaterial map={grassTex(...env.grass)} color="#ffffff" /></mesh>
      <mesh position={[0, -0.12, SHORE_Z - 4]} rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[560, 9]} /><meshToonMaterial map={sandTex()} color="#ffffff" /></mesh>
      <Sea env={env} t={t} />
      {/* ilhotas e montanhas distantes */}
      {[[-120, -260, 60, 22], [-40, -300, 80, 26], [150, -280, 70, 24], [210, -330, 90, 30]].map(([x, z, r, h], i) => <mesh key={i} position={[x, h * 0.25 - 1, z]} scale={[r, h, r * 0.5]}><sphereGeometry args={[1, 14, 10]} /><Toon color={mixHex('#6a8a58', env.fog, 0.45)} /></mesh>)}
      <group position={[80, 0, -430]}><mesh position={[0, 70, 0]}><coneGeometry args={[130, 150, 7]} /><Toon color={mixHex('#6a78b8', env.fog, 0.4)} /></mesh><mesh position={[0, 128, 0]}><coneGeometry args={[46, 56, 7]} /><meshBasicMaterial color="#f4f0fa" toneMapped={false} /></mesh></group>
      <group position={[-230, 0, -400]}><mesh position={[0, 50, 0]}><coneGeometry args={[110, 110, 6]} /><Toon color={mixHex('#7a6ab0', env.fog, 0.4)} /></mesh></group>
      {trees.map((tr, i) => <Fir key={i} p={[tr.x, 0, tr.z]} s={tr.s} leaf={leafA} leaf2={leafB} />)}
      {/* horta + cabana (EUA) */}
      <Garden eaten={garden?.eaten} />
      <Cabin p={[-15, 0, -4]} t={t} />
      <FlagPole p={[-8.8, 0, -7.2]} h={9} tex={flagUS()} t={t} phase={0.6} />
      <Fence a={[-9.5, -6.6]} b={[9.5, -6.6]} /><Fence a={[-9.5, -6.6]} b={[-9.5, 6.4]} /><Fence a={[9.5, -6.6]} b={[9.5, 6.4]} gap={[9.5, 2.4]} />
      <SignPost p={[11.9, 0, 4.6]} text={'SAN JUAN\n1859'} rot={0.28} />
      {/* pasto britânico */}
      <FlagPole p={[22, 0, -8]} h={11} tex={flagUK()} t={t} phase={2.0} />
      <Box p={[30, 2.2, -10]} s={[8, 4.4, 5.4]} c="#d9c29a" /><mesh position={[30, 5.5, -10]} rotation={[0, Math.PI / 4, 0]} scale={[1.2, 1, 0.8]}><coneGeometry args={[5.6, 2.8, 4]} /><Toon color="#8a4a42" /></mesh>
      {sheep.map((s, i) => <Sheep key={i} p={[s.x, 0, s.z]} t={t} face={s.f as 1 | -1} ph={s.ph} />)}
      {/* acampamento americano na praia */}
      <Tent p={[-46, 0, -36]} s={1.2} rot={0.2} /><Tent p={[-38, 0, -40]} s={1.1} rot={-0.3} /><Tent p={[-30, 0, -37]} s={1.3} rot={0.1} /><Tent p={[-54, 0, -32]} s={1.0} rot={0.5} />
      <FlagPole p={[-34, 0, -46]} h={12} tex={flagUS()} t={t} phase={1.2} />
      <group position={[-20, 0, -44]}><Cannon rot={Math.PI * 0.12} /></group>
      <Tufts n={2600} area={[-70, 70, -50, 40]} y={0} color={env.grass[2]} color2={env.grass[1]} seed={3} sway={0.14} t={t} h={0.7} />
      <Tufts n={1800} area={[-16, 16, 4, 18]} y={0} color={env.grass[0]} color2={env.grass[2]} seed={9} sway={0.16} t={t} h={0.6} />
      {fleet && fleetU > 0.01 && <Fleet t={t} appear={fleetU} />}
      {shafts && <Shafts t={t} at={[-6, 0, 6]} yaw={0.35} n={6} />}
    </group>
  );
};
