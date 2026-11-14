import React, { useMemo } from 'react';
import { Env, Toon, Lights, Sky, Clouds, Tufts, Tree, House, Shadow } from './common';
import { rng, mixHex } from '../lib/anim';
export const PLAZA_AT: [number, number, number] = [300, 0, 0];

const Puff: React.FC<{ t: number }> = ({ t }) => (
  <group>{Array.from({ length: 6 }, (_, i) => { const a = (((t * 0.35 + i / 6) % 1) + 1) % 1; return <mesh key={i} position={[Math.sin(a * 6 + i) * 0.5 + a * 1.0, a * 5, 0]} scale={0.5 + a * 1.2}><sphereGeometry args={[1, 10, 8]} /><meshBasicMaterial color="#fff6ee" transparent opacity={0.8 * (1 - a)} /></mesh>; })}</group>
);

export const Plaza: React.FC<{ env: Env; t: number }> = ({ env, t }) => {
  const at = PLAZA_AT;
  const cob = useMemo(() => { const r = rng(12); return Array.from({ length: 80 }, () => ({ x: (r() - 0.5) * 40, z: -6 + r() * 22, s: 0.5 + r() * 0.8 })); }, []);
  return (
    <group position={at}>
      <Lights env={env} />
      <Sky env={env} />
      <Clouds t={t} tint={mixHex('#fff0e0', env.mid, 0.3)} seed={11} />
      <mesh position={[0, -0.3, 4]}><boxGeometry args={[90, 0.6, 60]} /><Toon color="#c4a888" /></mesh>
      {cob.map((c, i) => <mesh key={i} position={[c.x, 0.02, c.z]} rotation={[-Math.PI / 2, 0, 0]} scale={[c.s, c.s * 0.7, 1]}><circleGeometry args={[1, 7]} /><meshBasicMaterial color="#a88c86" transparent opacity={0.55} /></mesh>)}
      {/* padaria */}
      <group position={[0, 0, -9]}>
        <mesh position={[0, 3.2, 0]}><boxGeometry args={[14, 6.4, 6]} /><Toon color="#f1dcb4" /></mesh>
        <mesh position={[0, 7.6, 0]} rotation={[0, Math.PI / 4, 0]} scale={[1.38, 1, 0.55]}><coneGeometry args={[7.2, 3.2, 4]} /><Toon color="#a64f4a" /></mesh>
        <mesh position={[0, 4.9, 3.5]} rotation={[0.45, 0, 0]}><boxGeometry args={[14.8, 0.2, 3.2]} /><Toon color="#d9625f" /></mesh>
        {[-6, -4, -2, 0, 2, 4, 6].map((x, i) => <mesh key={i} position={[x * 1.0, 4.88, 3.52]} rotation={[0.45, 0, 0]}><boxGeometry args={[0.9, 0.22, 3.2]} /><Toon color="#f6ecd8" /></mesh>)}
        <mesh position={[0, 1.7, 3.05]}><boxGeometry args={[2.2, 3.4, 0.2]} /><Toon color="#6a4a3a" /></mesh>
        {[-4.2, 4.2].map((x) => <mesh key={x} position={[x, 2.6, 3.05]}><boxGeometry args={[2.6, 2.2, 0.2]} /><meshBasicMaterial color="#ffd68a" /></mesh>)}
        <mesh position={[5.2, 9.4, -1]}><boxGeometry args={[1.4, 3.6, 1.4]} /><Toon color="#b9a6a0" /></mesh>
        <group position={[5.2, 11.4, -1]}><Puff t={t} /></group>
        <mesh position={[0, 5.9, 3.2]}><boxGeometry args={[5, 1.2, 0.15]} /><Toon color="#7a4a3a" /></mesh>
        <mesh position={[-1.6, 5.9, 3.3]}><circleGeometry args={[0.38, 14]} /><meshBasicMaterial color="#f0c56a" /></mesh>
        <mesh position={[0, 5.9, 3.3]}><circleGeometry args={[0.38, 14]} /><meshBasicMaterial color="#f0c56a" /></mesh>
        <mesh position={[1.6, 5.9, 3.3]}><circleGeometry args={[0.38, 14]} /><meshBasicMaterial color="#f0c56a" /></mesh>
      </group>
      <House p={[-20, 0, -8]} wall="#e8d2aa" roof="#8a5a8a" snow={0} />
      <House p={[20, 0, -10]} wall="#d4b894" roof="#c97a4a" w={6} snow={0} />
      <Tree p={[-12, 0, -4]} leaf={env.foliage} />
      <Tree p={[14, 0, -3]} leaf={env.foliage} s={1.2} />
      {/* barris e carrinho de pão */}
      {[[-7, 0, -2], [-8.2, 0, -1.4]].map((p, i) => <mesh key={i} position={[p[0], 0.75, p[2]]}><cylinderGeometry args={[0.7, 0.62, 1.5, 12]} /><Toon color="#9a6a46" /></mesh>)}
      <group position={[7, 0, 1.5]}>
        <mesh position={[0, 1.1, 0]}><boxGeometry args={[3, 0.9, 1.6]} /><Toon color="#a4663a" /></mesh>
        {[-0.8, 0, 0.8].map((x, i) => <mesh key={i} position={[x, 1.8, 0]} scale={[1, 0.6, 0.8]}><sphereGeometry args={[0.45, 10, 8]} /><Toon color="#e4a352" /></mesh>)}
        {[-1.2, 1.2].map((x) => <mesh key={x} position={[x, 0.45, 0.9]} rotation={[0, 0, 0]}><cylinderGeometry args={[0.5, 0.5, 0.15, 14]} /><Toon color="#7a5440" /></mesh>)}
      </group>
      <Tufts n={500} area={[-30, 30, 8, 20]} y={0} color="#d9a45a" seed={21} sway={0.1} t={t} />
    </group>
  );
};
