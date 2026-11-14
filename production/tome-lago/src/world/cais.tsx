import React, { useMemo } from 'react';
import * as THREE from 'three';
import { Env, Toon, Tree, Mountain, House, Tufts, FURN, Shadow, Chair, Lights, Sky, Clouds, Snow } from './common';
import { rng, mixHex, clamp, lerp } from '../lib/anim';

export const ISLAND_X = 38;
export const PILE_N = 36;
export type PileItem = { x: number; z: number; ry: number; rz: number; k: number; kind: number };
export const PILE: PileItem[] = (() => {
  const r = rng(2024);
  return Array.from({ length: PILE_N }, (_, i) => ({
    x: 3.2 + (i / (PILE_N - 1)) * (ISLAND_X - 8 - 3.2) + (r() - 0.5) * 0.4, z: (r() - 0.5) * 0.9, ry: r() * 6.28, rz: (r() - 0.5) * 0.5,
    k: 1.25 + r() * 0.4, kind: i % FURN.length,
  }));
})();

const Dock: React.FC = () => (
  <group>
    <mesh position={[-5, 0.35, 0]}><boxGeometry args={[12.5, 0.3, 3.2]} /><Toon color="#b88a5a" /></mesh>
    {Array.from({ length: 12 }, (_, i) => <mesh key={i} position={[-10.5 + i * 1.05, 0.52, 0]}><boxGeometry args={[0.05, 0.02, 3.2]} /><meshBasicMaterial color="#6a4a52" /></mesh>)}
    {[-1.4, 1.4].flatMap((z) => [0.2, -4, -8].map((x) => <mesh key={`${x}${z}`} position={[x, 0.2, z]}><cylinderGeometry args={[0.2, 0.24, 1.6, 6]} /><Toon color="#7a5440" /></mesh>))}
    <mesh position={[0.1, 1.0, 1.5]}><cylinderGeometry args={[0.18, 0.22, 1.4, 6]} /><Toon color="#7a5440" /></mesh>
    <mesh position={[0.1, 1.0, -1.5]}><cylinderGeometry args={[0.18, 0.22, 1.4, 6]} /><Toon color="#7a5440" /></mesh>
  </group>
);

const Market: React.FC<{ lit: number; t: number }> = ({ lit, t }) => (
  <group position={[ISLAND_X, 0, -3]}>
    <mesh position={[0, -1.6, 0]} scale={[1, 0.22, 0.8]}><sphereGeometry args={[11, 20, 14]} /><Toon color="#c9a46a" /></mesh>
    {[[-5, 0.6, '#d9625f'], [0, 1.2, '#e8b04a'], [5, 0.2, '#5aa0a4']].map(([x, z, c], i) => (
      <group key={i} position={[x as number, 0.5, z as number]}>
        <mesh position={[0, 0.9, 0]}><boxGeometry args={[2.6, 1.6, 1.4]} /><Toon color="#9a6a46" /></mesh>
        <mesh position={[0, 2.1, 0.5]} rotation={[0.4, 0, 0]}><boxGeometry args={[3.1, 0.14, 1.8]} /><Toon color={c as string} /></mesh>
        <mesh position={[1.1, 2.6, 0.9]}><sphereGeometry args={[0.16, 8, 6]} /><meshBasicMaterial color={lit ? '#ffd88a' : '#d9c08a'} /></mesh>
      </group>
    ))}
    <mesh position={[0, 6, -3]}><cylinderGeometry args={[0.8, 1.1, 8, 6]} /><Toon color="#b9a6a0" /></mesh>
    <mesh position={[0, 11, -3]}><coneGeometry args={[1.5, 3.4, 6]} /><Toon color="#b9574e" /></mesh>
  </group>
);

export const Boat: React.FC<{ p: [number, number, number]; sink: number; t: number }> = ({ p, sink, t }) => {
  const s = clamp(sink);
  return (
    <group position={[p[0], p[1] - s * 3.2 + Math.sin(t * 1.4) * 0.06 * (1 - s), p[2]]} rotation={[s * 0.55, 0.15, s * 0.9 + Math.sin(t * 1.4) * 0.03]}>
      <mesh position={[0, 0.3, 0]}><boxGeometry args={[6, 0.9, 2.2]} /><Toon color="#a65a3a" /></mesh>
      <mesh position={[-0.5, 1.2, 0]}><boxGeometry args={[2.2, 1.1, 1.8]} /><Toon color="#e8dcc6" /></mesh>
      <mesh position={[2.9, 0.5, 0]} rotation={[0, 0, -0.4]}><boxGeometry args={[1.4, 0.8, 2.0]} /><Toon color="#a65a3a" /></mesh>
    </group>
  );
};

export const Cais: React.FC<{ env: Env; t: number; pile: number; boatSink?: number; boatVisible?: boolean; lit?: number; hideDock?: boolean }> = ({ env, t, pile, boatSink = 0, boatVisible = false, lit = 0, hideDock = false }) => {
  const mount = useMemo(() => [-150, -105, -62, -20, 28, 70, 112, 150].map((x, i) => ({ x, r: 26 + (i % 3) * 9, h: 17 + ((i * 7) % 5) * 5 })), []);
  const stripes = useMemo(() => { const r = rng(9); return Array.from({ length: 46 }, () => ({ x: -20 + r() * 80, z: -45 + r() * 50, w: 0.8 + r() * 1.8, sp: 0.2 + r() * 0.35, ph: r() * 6 })); }, []);
  const snow = env.snow;
  const fogCol = new THREE.Color(env.fog);
  const trees = useMemo(() => { const r = rng(5); return Array.from({ length: 16 }, () => ({ x: -62 + r() * 44, z: -22 + r() * 18, s: 0.8 + r() * 0.7 })); }, []);
  return (
    <group>
      <fog attach="fog" args={[fogCol, 70, 190]} />
      <Lights env={env} />
      <Sky env={env} />
      <Clouds t={t} tint={mixHex('#fff0e0', env.mid, 0.35)} />
      {mount.map((m, i) => <Mountain key={i} p={[m.x, -2, -100 - (i % 2) * 16]} r={m.r} h={m.h} c={mixHex(mixHex('#7a6aa8', env.fog, 0.5), '#ffffff', snow * 0.25)} snow={snow} />)}
      {/* lago */}
      <mesh position={[40, 0, -50]} rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[300, 180]} /><Toon color={env.water} opacity={0.62} /></mesh>
      <mesh position={[40, -2.4, -50]} rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[300, 180]} /><meshBasicMaterial color={mixHex(env.water, '#6a64a8', 0.45)} /></mesh>
      {stripes.map((s, i) => { const x = ((s.x + t * s.sp + 30) % 100) - 28; return <mesh key={i} position={[x, 0.05, s.z]} rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[s.w, 0.07]} /><meshBasicMaterial color={env.sun} transparent opacity={0.45 * (0.6 + 0.4 * Math.sin(t * 1.4 + s.ph))} depthWrite={false} /></mesh>; })}
      {/* margem */}
      <mesh position={[-45, -0.2, -2]}><boxGeometry args={[68, 1.4, 54]} /><Toon color={mixHex(env.ground, '#ffffff', snow * 0.5)} /></mesh>
      <mesh position={[-45, 0.55, -26]} scale={[1, 1, 1]}><boxGeometry args={[68, 0.2, 10]} /><Toon color={mixHex(env.ground, '#9a7a5a', 0.3 * (1 - snow))} /></mesh>
      <Tufts n={700} area={[-40, -12, -4, 18]} y={0.5} color={mixHex(env.foliage, '#e0b050', 0.4 + snow * 0.2)} seed={3} sway={0.12} t={t} />
      <Tufts n={420} area={[-40, -12, -26, -4]} y={0.5} color={mixHex(env.foliage, '#c88a40', 0.2)} seed={8} sway={0.08} t={t} />
      {trees.map((tr, i) => <Tree key={i} p={[tr.x, 0.5, tr.z]} s={tr.s} leaf={env.foliage} snow={snow} />)}
      <House p={[-24, 0.5, -10]} wall="#e8d2aa" roof="#b9574e" snow={snow} lit={lit} />
      <House p={[-34, 0.5, -16]} wall="#d4b894" roof="#8a5a8a" w={6} h={3.8} snow={snow} lit={lit} />
      <House p={[-16, 0.5, -17]} wall="#f0dcb4" roof="#c97a4a" w={4.4} snow={snow} lit={lit} />
      {!hideDock && <Dock />}
      <Market lit={lit} t={t} />
      {/* móveis afundados: pilha/ponte */}
      {PILE.map((it, i) => {
        const vis = clamp(pile - i); if (vis <= 0) return null; const Comp = FURN[it.kind];
        const HT = [1.35, 0.95, 0.95, 0.15, 1.35, 1.35, 0.95][it.kind]; const door = it.kind === 3;
        return <group key={i} position={[it.x, -0.22 - HT * it.k * 0.9 + (1 - vis) * -1.5, it.z]} rotation={[door ? -Math.PI / 2 + 0.05 : 0.04, it.ry, it.rz * 0.3]} scale={it.k * 0.9 * vis}><Comp /></group>;
      })}
      {boatVisible && <Boat p={[17, 0.1, -6]} sink={boatSink} t={t} />}
      <Snow t={t} amount={snow} at={[-8, 0, 0]} />
    </group>
  );
};
