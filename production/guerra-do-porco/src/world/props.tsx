import React, { useLayoutEffect, useMemo, useRef } from 'react';
import * as THREE from 'three';
import { Toon, Shadow, Tufts, Flag } from './common';
import { noteTex, signTex, sailTex, logsTex, shingleTex, planksTex, soilTex } from './tex';
import { rng, mixHex, clamp } from '../lib/anim';

const Box: React.FC<{ p: [number, number, number]; s: [number, number, number]; c: string; r?: [number, number, number]; map?: THREE.Texture }> = ({ p, s, c, r, map }) => (
  <mesh position={p} scale={s} rotation={r}><boxGeometry args={[1, 1, 1]} /><Toon color={c} map={map} /></mesh>
);
export { Box };

/** Mosquete (cano ao longo de −y local; coronha em +y). Muzzle em (0,−1.8). */
export const Rifle: React.FC = () => (
  <group position={[0, -0.1, 0.06]}>
    <mesh position={[0, -0.2, 0]}><boxGeometry args={[0.075, 3.2, 0.075]} /><meshBasicMaterial color="#4a4a58" toneMapped={false} /></mesh>
    <mesh position={[0, -0.2, -0.01]}><boxGeometry args={[0.12, 3.25, 0.05]} /><meshBasicMaterial color="#2a2230" toneMapped={false} /></mesh>
    {[-1.2, -0.5, 0.2].map((y, i) => <mesh key={i} position={[0, y, 0.01]}><boxGeometry args={[0.13, 0.09, 0.09]} /><meshBasicMaterial color="#f0c250" toneMapped={false} /></mesh>)}
    <mesh position={[0, 0.95, 0]} rotation={[0, 0, 0.04]}><boxGeometry args={[0.22, 1.25, 0.09]} /><meshBasicMaterial color="#9a6038" toneMapped={false} /></mesh>
    <mesh position={[0, 0.95, -0.01]} rotation={[0, 0, 0.04]}><boxGeometry args={[0.28, 1.31, 0.05]} /><meshBasicMaterial color="#2a2230" toneMapped={false} /></mesh>
  </group>
);
export const Spyglass: React.FC = () => (
  <group>
    {[[0.35, 0.12, 1.1], [0.62, 0.15, 0.9], [0.9, 0.18, 0.6]].map(([w, r, l], i) => <mesh key={i} position={[0, -0.5 - i * 0.6, 0.05]}><cylinderGeometry args={[r as number, r as number, l as number, 10]} /><meshBasicMaterial color={i === 1 ? '#c9a24a' : '#f0c250'} toneMapped={false} /></mesh>)}
  </group>
);
export const Note: React.FC<{ label: string; s?: number }> = ({ label, s = 1 }) => (
  <mesh scale={[1.5 * s, 0.75 * s, 1]}><planeGeometry args={[1, 1]} /><meshBasicMaterial map={noteTex(label)} side={THREE.DoubleSide} toneMapped={false} /></mesh>
);
export const Cannon: React.FC<{ rot?: number }> = ({ rot = 0 }) => (
  <group rotation={[0, rot, 0]}>
    <mesh position={[0.4, 1.35, 0]} rotation={[0, 0, Math.PI / 2 - 0.1]}><cylinderGeometry args={[0.46, 0.7, 4.6, 14]} /><Toon color="#3a3a4c" /></mesh>
    <mesh position={[2.55, 1.5, 0]} rotation={[0, 0, Math.PI / 2 - 0.1]}><cylinderGeometry args={[0.56, 0.5, 0.3, 14]} /><Toon color="#2a2a3a" /></mesh>
    <Box p={[-0.3, 0.7, 0]} s={[3.4, 0.6, 1.5]} c="#9a6038" r={[0, 0, 0.06]} />
    {[0.9, -0.9].map((z) => <mesh key={z} position={[-0.2, 0.9, z]} rotation={[Math.PI / 2, 0, 0]}><cylinderGeometry args={[0.95, 0.95, 0.22, 16]} /><Toon color="#b9743e" /></mesh>)}
    {[0.9, -0.9].map((z) => <mesh key={`h${z}`} position={[-0.2, 0.9, z * 1.08]} rotation={[Math.PI / 2, 0, 0]}><cylinderGeometry args={[0.22, 0.22, 0.3, 10]} /><Toon color="#2a2a3a" /></mesh>)}
    {[[-1.9, 0.3, 1.9], [-2.7, 0.3, 2.2], [-1.6, 0.3, 2.9]].map((b, i) => <mesh key={i} position={[b[0], b[1], b[2]]}><sphereGeometry args={[0.32, 10, 8]} /><Toon color="#262634" /></mesh>)}
  </group>
);
export const Tent: React.FC<{ p: [number, number, number]; s?: number; rot?: number }> = ({ p, s = 1, rot = 0 }) => (
  <group position={p} scale={s} rotation={[0, rot, 0]}>
    <mesh position={[0, 1.7, 0]} rotation={[0, Math.PI / 4, 0]} scale={[1.45, 1, 1.15]}><coneGeometry args={[2.6, 3.4, 4]} /><Toon color="#f1e6cc" map={sailTex()} /></mesh>
    <mesh position={[0, 0.06, 1.55]}><planeGeometry args={[1.1, 1.8]} /><meshBasicMaterial color="#3a2f4c" /></mesh>
    <mesh position={[0, 3.7, 0]}><cylinderGeometry args={[0.05, 0.05, 0.7, 6]} /><Toon color="#7a5440" /></mesh>
  </group>
);
export const Fir: React.FC<{ p: [number, number, number]; s?: number; leaf: string; leaf2?: string }> = ({ p, s = 1, leaf, leaf2 }) => (
  <group position={p} scale={s}>
    <mesh position={[0, 1.2, 0]}><cylinderGeometry args={[0.28, 0.4, 2.4, 6]} /><Toon color="#7a4a3a" /></mesh>
    {[[3.4, 2.1, 3.2], [5.3, 1.7, 2.6], [7.0, 1.25, 2.0]].map(([y, r, h], i) => <mesh key={i} position={[0, y as number, 0]}><coneGeometry args={[r as number, h as number, 7]} /><Toon color={i % 2 ? (leaf2 ?? leaf) : leaf} /></mesh>)}
  </group>
);
export const Sheep: React.FC<{ p: [number, number, number]; t: number; face?: 1 | -1; ph?: number }> = ({ p, t, face = 1, ph = 0 }) => {
  const g = Math.max(0, Math.sin((t + ph) * 1.6));
  return (
    <group position={p} scale={[face, 1, 1]}>
      <Shadow p={[0, 0.04, 0]} s={[1.5, 0.6]} />
      {[[-0.5, 0.2], [-0.5, -0.25], [0.5, 0.2], [0.5, -0.25]].map(([x, z], i) => <mesh key={i} position={[x as number, 0.35, z as number]}><cylinderGeometry args={[0.07, 0.07, 0.7, 6]} /><Toon color="#2a2230" /></mesh>)}
      <mesh position={[0, 1.0, 0]} scale={[1.35, 0.85, 0.9]}><icosahedronGeometry args={[0.8, 1]} /><Toon color="#f7f0e2" /></mesh>
      <mesh position={[0.95, 1.05 - g * 0.55, 0]} rotation={[0, 0, -g * 0.4]} scale={[0.75, 0.62, 0.55]}><sphereGeometry args={[0.55, 12, 10]} /><Toon color="#3a3350" /></mesh>
    </group>
  );
};
export const Cabin: React.FC<{ p: [number, number, number]; t: number; glow?: number }> = ({ p, t, glow = 1 }) => (
  <group position={p}>
    <Box p={[0, 2.3, 0]} s={[9, 4.6, 6.4]} c="#c48b58" map={logsTex()} />
    {[1, -1].map((s) => <mesh key={s} position={[0, 5.6, s * 1.75]} rotation={[s * -0.62, 0, 0]}><boxGeometry args={[10.2, 0.28, 4.4]} /><Toon color="#a0634a" map={shingleTex()} /></mesh>)}
    <Box p={[3.2, 6.6, -0.8]} s={[1.3, 3.8, 1.3]} c="#a89a92" />
    <Box p={[-1.5, 1.6, 3.26]} s={[1.5, 3.2, 0.14]} c="#5a3a2a" />
    <Box p={[2.0, 2.6, 3.24]} s={[1.9, 1.7, 0.14]} c="#3a2a22" />
    <mesh position={[2.0, 2.6, 3.33]}><planeGeometry args={[1.6, 1.4]} /><meshBasicMaterial color="#ffd27a" toneMapped={false} /></mesh>
    {[[-0.5], [0.5]].map(([x], i) => <mesh key={i} position={[2.0 + (x as number) * 0.6, 2.6, 3.36]}><planeGeometry args={[0.07, 1.45]} /><meshBasicMaterial color="#3a2a22" /></mesh>)}
    {Array.from({ length: 5 }, (_, i) => { const u = ((t * 0.3 + i / 5) % 1); return <mesh key={i} position={[3.2 + Math.sin(u * 5 + i) * 0.4 + u * 1.2, 8.6 + u * 4.2, -0.8]} scale={0.5 + u * 1.3}><sphereGeometry args={[1, 10, 8]} /><meshBasicMaterial color="#f4eff2" transparent opacity={0.8 * (1 - u)} depthWrite={false} toneMapped={false} /></mesh>; })}
  </group>
);
export const Fence: React.FC<{ a: [number, number]; b: [number, number]; gap?: [number, number] }> = ({ a, b, gap }) => {
  const len = Math.hypot(b[0] - a[0], b[1] - a[1]), n = Math.max(1, Math.round(len / 3)), ang = Math.atan2(b[1] - a[1], b[0] - a[0]);
  const items = Array.from({ length: n + 1 }, (_, i) => ({ x: a[0] + (b[0] - a[0]) * (i / n), z: a[1] + (b[1] - a[1]) * (i / n) }));
  const inGap = (x: number, z: number) => gap && (Math.hypot(x - gap[0], z - gap[1]) < 1.35);
  return (
    <group>
      {items.map((p, i) => !inGap(p.x, p.z) && <mesh key={i} position={[p.x, 1.1, p.z]}><cylinderGeometry args={[0.14, 0.18, 2.2, 6]} /><Toon color="#8a5a3a" /></mesh>)}
      {items.slice(0, -1).map((p, i) => { const q = items[i + 1]; const mx = (p.x + q.x) / 2, mz = (p.z + q.z) / 2; if (inGap(mx, mz)) return null;
        return [0.9, 1.6].map((y, k) => <mesh key={`${i}${k}`} position={[mx, y, mz]} rotation={[0, -ang, 0]}><boxGeometry args={[len / n, 0.18, 0.16]} /><Toon color="#b17a4c" /></mesh>); })}
    </group>
  );
};
/** Horta: canteiros de terra com folhagem instanciada (verde puxado a ouro, regra v3.1). */
export const Garden: React.FC<{ x0?: number; x1?: number; z0?: number; z1?: number; seed?: number; eaten?: { x: number; z: number; r: number } }> = ({ x0 = -8, x1 = 8, z0 = -4, z1 = 5, seed = 3, eaten }) => {
  const rowsZ = useMemo(() => { const n = 6; return Array.from({ length: n }, (_, i) => z0 + 0.6 + (i * (z1 - z0 - 1.2)) / (n - 1)); }, [z0, z1]);
  const ref = useRef<THREE.InstancedMesh>(null!);
  const leaves = useMemo(() => { const r = rng(seed); const out: { x: number; z: number; s: number; c: number; a: number; px: number; pz: number }[] = [];
    rowsZ.forEach((z) => { for (let x = x0 + 0.8; x < x1; x += 1.3) { const px = x + (r() - 0.5) * 0.4, pz = z + (r() - 0.5) * 0.3, ps = 0.7 + r() * 0.5;
      for (let k = 0; k < 6; k++) { const a = (k / 6) * Math.PI * 2 + r() * 0.5; out.push({ x: px + Math.cos(a) * 0.22 * ps, z: pz + Math.sin(a) * 0.22 * ps, s: ps * (0.8 + r() * 0.4), c: r(), a, px, pz }); } } }); return out; }, [rowsZ, x0, x1, seed]);
  useLayoutEffect(() => {
    const m = new THREE.Object3D(), ca = new THREE.Color('#7f9a38'), cb = new THREE.Color('#e0c24e'), c = new THREE.Color();
    leaves.forEach((p, i) => { const d = eaten ? Math.hypot(p.px - eaten.x, p.pz - eaten.z) : 99; const sc = eaten && d < eaten.r ? 0.12 : 1;
      m.position.set(p.x, 0.45 + 0.35 * p.s * sc, p.z); m.rotation.set(Math.sin(p.a) * 0.6, 0, -Math.cos(p.a) * 0.6); m.scale.set(0.3 * p.s * sc, 0.9 * p.s * sc, 0.3 * p.s * sc); m.updateMatrix(); ref.current.setMatrixAt(i, m.matrix);
      c.copy(ca).lerp(cb, 0.3 + p.c * 0.55); ref.current.setColorAt(i, c); });
    ref.current.instanceMatrix.needsUpdate = true; if (ref.current.instanceColor) ref.current.instanceColor.needsUpdate = true;
  });
  return (
    <group>
      {rowsZ.map((z, i) => <mesh key={i} position={[(x0 + x1) / 2, 0.2, z]}><boxGeometry args={[x1 - x0, 0.45, 0.95]} /><Toon color="#ffffff" map={soilTex()} /></mesh>)}
      <instancedMesh ref={ref} args={[undefined, undefined, leaves.length]}><coneGeometry args={[0.5, 1, 5]} /><Toon color="#ffffff" /></instancedMesh>
    </group>
  );
};
export const SignPost: React.FC<{ p: [number, number, number]; text: string; rot?: number }> = ({ p, text, rot = 0 }) => (
  <group position={p} rotation={[0, rot, 0]}>
    <mesh position={[0, 1.8, 0]}><cylinderGeometry args={[0.13, 0.17, 3.6, 6]} /><Toon color="#7a5440" /></mesh>
    <mesh position={[0, 3.5, 0.15]}><boxGeometry args={[2.6, 1.3, 0.14]} /><meshBasicMaterial map={signTex(text)} toneMapped={false} /></mesh>
  </group>
);
export const Grave: React.FC<{ p: [number, number, number]; t: number }> = ({ p, t }) => (
  <group position={p}>
    <mesh position={[0, 0.25, 0]} scale={[1.6, 0.55, 1.1]}><sphereGeometry args={[0.8, 14, 10]} /><Toon color="#ffffff" map={soilTex()} /></mesh>
    <Box p={[0, 1.2, -0.45]} s={[0.18, 1.7, 0.1]} c="#e8dcc0" /><Box p={[0, 1.55, -0.45]} s={[1.0, 0.18, 0.1]} c="#e8dcc0" />
    {[[-0.7, 0.3, '#ff7aa0'], [0.65, 0.35, '#ffd24a'], [0.1, 0.45, '#ff9a4a']].map(([x, z, col], i) => <group key={i} position={[x as number, 0.55, (z as number) + 0.35]} rotation={[0, 0, Math.sin(t * 2 + i) * 0.08]}>
      <mesh position={[0, 0.2, 0]}><cylinderGeometry args={[0.025, 0.025, 0.5, 5]} /><Toon color="#6a8a3a" /></mesh><mesh position={[0, 0.5, 0]}><sphereGeometry args={[0.15, 8, 6]} /><meshBasicMaterial color={col as string} toneMapped={false} /></mesh></group>)}
  </group>
);
