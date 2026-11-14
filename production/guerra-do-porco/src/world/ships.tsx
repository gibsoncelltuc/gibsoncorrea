import React, { useLayoutEffect, useMemo } from 'react';
import * as THREE from 'three';
import { Toon, Flag, Env, Lights, Sky, Clouds, Shafts, Dust } from './common';
import { Box, Cannon } from './props';
import { hullTex, sailTex, flagUK, waterTex, planksTex } from './tex';
import { rng, mixHex, clamp } from '../lib/anim';

const Sail: React.FC<{ p: [number, number, number]; w: number; h: number; t: number; ph: number; bulge?: number }> = ({ p, w, h, t, ph, bulge = 0.7 }) => {
  const geo = useMemo(() => new THREE.PlaneGeometry(w, h, 8, 6), [w, h]);
  useLayoutEffect(() => {
    const pos = geo.attributes.position;
    for (let i = 0; i < pos.count; i++) { const u = (pos.getX(i) + w / 2) / w, v = (pos.getY(i) + h / 2) / h; pos.setZ(i, Math.sin(u * Math.PI) * Math.sin(v * Math.PI * 0.9 + 0.2) * bulge + Math.sin(u * 5 + t * 2.2 + ph) * 0.06 * v); }
    pos.needsUpdate = true;
  });
  return (<mesh geometry={geo} position={p}><meshBasicMaterial map={sailTex()} side={THREE.DoubleSide} color="#fff0d2" toneMapped={false} /></mesh>);
};

/** Fragata genérica (não é um navio específico): casco com portinholas e xadrez amarelo, 3 mastros, velas, bandeira. */
export const Ship: React.FC<{ t: number; ph?: number; scale?: number; rotY?: number; pos: [number, number, number]; foam?: boolean }> = ({ t, ph = 0, scale = 1, rotY = -0.5, pos, foam = true }) => {
  const hull = hullTex();
  const bow = useMemo(() => { const s = new THREE.Shape(); s.moveTo(0, -2.1); s.lineTo(0, 2.1); s.lineTo(3.6, 0.0); s.closePath(); return new THREE.ExtrudeGeometry(s, { depth: 2.4, bevelEnabled: false }); }, []);
  const bob = Math.sin(t * 1.3 + ph) * 0.14, roll = Math.sin(t * 0.9 + ph) * 0.035;
  const masts: [number, number, number, number][] = [[4.6, 11.5, 6.2, 3], [-0.4, 13.5, 7.4, 3], [-5.2, 9.5, 5.2, 2]];
  return (
    <group position={[pos[0], pos[1] + bob, pos[2]]} rotation={[0, rotY, roll]} scale={scale}>
      <mesh position={[0, 0.6, 0]}>
        <boxGeometry args={[16, 2.4, 4.2]} />
        {[0, 1, 2, 3, 4, 5].map((i) => (i === 4 || i === 5 ? <meshToonMaterial key={i} attach={`material-${i}`} map={hull} color="#ffffff" /> : <meshToonMaterial key={i} attach={`material-${i}`} color={i === 2 ? '#b98a55' : '#1e1b2e'} />))}
      </mesh>
      <mesh geometry={bow} position={[8, -0.6, 0]} rotation={[-Math.PI / 2, 0, 0]}><meshToonMaterial color="#1e1b2e" /></mesh>
      <Box p={[-6.3, 2.2, 0]} s={[3.4, 1.5, 4.0]} c="#2a2640" />
      <Box p={[-6.3, 3.05, 0]} s={[3.6, 0.2, 4.2]} c="#e9b848" />
      {[1, -1].map((s) => <Box key={s} p={[0, 1.95, s * 2.05]} s={[15.6, 0.45, 0.14]} c="#e9b848" />)}
      {masts.map(([x, h, w, n], i) => (
        <group key={i} position={[x, 1.8, 0]}>
          <mesh position={[0, h / 2, 0]}><cylinderGeometry args={[0.16, 0.24, h, 8]} /><Toon color="#8a5a3a" /></mesh>
          {Array.from({ length: n }, (_, k) => { const y = 2.6 + k * ((h - 3.2) / n); const ww = w * (1 - k * 0.2);
            return (<group key={k}><mesh position={[0, y + 1.5, 0]} rotation={[Math.PI / 2, 0, 0]}><cylinderGeometry args={[0.1, 0.1, ww + 0.6, 6]} /><Toon color="#7a4a32" /></mesh><Sail p={[0, y + 0.2, 0.0]} w={ww} h={2.5} t={t} ph={ph + i + k} /></group>); })}
        </group>
      ))}
      {[-5.8, -3.6, -1.4, 0.8, 3.0, 5.2].map((x, i) => [1, -1].map((s) => <mesh key={`${i}${s}`} position={[x, 0.65, s * 2.28]} rotation={[Math.PI / 2, 0, 0]}><cylinderGeometry args={[0.2, 0.26, 0.7, 8]} /><Toon color="#14121c" /></mesh>))}
      <group position={[-7.9, 3.1, 0]}><mesh position={[0, 1.1, 0]}><cylinderGeometry args={[0.07, 0.07, 2.4, 6]} /><Toon color="#8a5a3a" /></mesh><group position={[0.05, 1.8, 0]}><Flag tex={flagUK()} t={t} w={2.6} h={1.6} amp={0.3} phase={ph} /></group></group>
      {foam && [0, 1, 2].map((i) => <mesh key={i} position={[-9.5 - i * 2.2, -0.45, (i - 1) * 0.6]} rotation={[-Math.PI / 2, 0, 0]} scale={[1.8 + i * 0.7, 0.8 + i * 0.4, 1]}><circleGeometry args={[1, 16]} /><meshBasicMaterial color="#ffffff" transparent opacity={0.45 - i * 0.12} depthWrite={false} toneMapped={false} /></mesh>)}
    </group>
  );
};
export const Sea: React.FC<{ env: Env; t: number; y?: number; size?: [number, number]; at?: [number, number, number] }> = ({ env, t, y = -0.55, size = [900, 700], at = [0, 0, -300] }) => {
  const tex = waterTex(...env.water); tex.offset.set((t * 0.012) % 1, (-t * 0.02) % 1);
  return <mesh position={[at[0], y, at[2]]} rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[size[0], size[1]]} /><meshToonMaterial map={tex} color="#ffffff" /></mesh>;
};
export const Fleet: React.FC<{ t: number; x0?: number; speed?: number; appear?: number }> = ({ t, x0 = 0, speed = 1.0, appear = 1 }) => {
  // cinco navios em escalão, proa para a praia (aproximando-se lentamente na direção da proa)
  const cfg = [[-28, -92, 1.5, 0.0], [-16, -98, 1.6, 1.3], [-4, -90, 1.45, 2.1], [8, -97, 1.6, 3.4], [20, -93, 1.5, 4.2]];
  return <>{cfg.map(([x, z, s, ph], i) => { const rot = -1.0 + (i % 2) * 0.1; return <Ship key={i} t={t} ph={ph} scale={s * (0.15 + 0.85 * appear)} pos={[x + x0 + Math.cos(rot) * speed * t, 0, z - Math.sin(rot) * speed * t - (1 - appear) * 70]} rotY={rot} foam />; })}</>;
};

export const DECK_AT: [number, number, number] = [600, 0, 0];
export const ShipDeck: React.FC<{ env: Env; t: number }> = ({ env, t }) => {
  const X = DECK_AT[0];
  return (
    <group position={DECK_AT}>
      <Lights env={env} /><Sky env={env} /><Clouds t={t} seed={9} z={-330} />
      <fog attach="fog" args={[new THREE.Color(env.fog), 60, 320]} />
      <mesh position={[0, 0, 0]} rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[34, 26]} /><meshToonMaterial map={planksTex('#c89a62', '#6a4630', [7, 6])} color="#ffffff" /></mesh>
      <Box p={[0, 0.9, -8.6]} s={[34, 1.8, 0.7]} c="#b9743e" /><Box p={[0, 1.9, -8.6]} s={[34, 0.22, 0.9]} c="#e9b848" />
      {[-13, -7, 7, 13].map((x) => <Box key={x} p={[x, 1.2, -8.6]} s={[0.5, 2.4, 0.9]} c="#8a5a3a" />)}
      {[[-3.2, 0], [3.4, 0]].map(([x]) => <group key={x} position={[x as number, 0, -7.1]}><Cannon rot={-Math.PI / 2} /></group>)}
      <mesh position={[-9, 8, -3]}><cylinderGeometry args={[0.55, 0.75, 16, 10]} /><Toon color="#8a5a3a" /></mesh>
      {[0, 1, 2].map((i) => <mesh key={i} position={[-9, 0.35 + i * 0.22, -3]} rotation={[Math.PI / 2, 0, 0]}><torusGeometry args={[1.0 - i * 0.12, 0.14, 6, 18]} /><Toon color="#d8c08a" /></mesh>)}
      <mesh position={[0, -3.2, -40]} rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[600, 200]} /><meshToonMaterial map={waterTex(...env.water)} color="#ffffff" /></mesh>
      <Ship t={t} ph={1} scale={0.8} pos={[-34, -3.1, -80]} rotY={-1.0} foam={false} /><Ship t={t} ph={2} scale={0.7} pos={[20, -3.1, -110]} rotY={-1.1} foam={false} />
      <group position={[12.5, 0, -6]}><mesh position={[0, 6, 0]}><cylinderGeometry args={[0.13, 0.17, 12, 8]} /><Toon color="#c9b48a" /></mesh><group position={[0.1, 10.2, 0]}><Flag tex={flagUK()} t={t} w={4.6} h={2.9} amp={0.42} phase={1} /></group></group>
      <Shafts t={t} at={[-4, 0, 2]} yaw={0.2} n={4} strength={0.7} /><Dust t={t} center={[0, 0.5, 5]} />
    </group>
  );
};
