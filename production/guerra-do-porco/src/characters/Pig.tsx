import React from 'react';
import { Disc, Bar, Arc, INK, MB } from './Rig';
import { clamp, easeInOut, easeOutBack, lerp } from '../lib/anim';

export type PigPose = { x: number; y: number; z: number; face: 1 | -1; scale: number; t: number; mode: 'eat' | 'trot' | 'dead'; flip: number; hop: number; shock?: number };
const PINK = '#f7a2b6', PINK2 = '#e98aa2', PINK3 = '#ffd0da';
/** Porco 2D cut-out (mesmo vocabulário do rig humano): contorno grosso, olho de pálpebra, nariz com narinas, rabo em espiral. */
export const Pig: React.FC<{ pig: PigPose }> = ({ pig }) => {
  const { t, mode } = pig;
  const eat = mode === 'eat', trot = mode === 'trot', dead = mode === 'dead';
  const chew = eat ? Math.sin(t * 13) * 0.05 : 0;
  const headRot = eat ? -0.62 + chew : trot ? Math.sin(t * 7) * 0.04 : 0;
  const swing = trot ? Math.sin(t * 11) : 0;
  const flipA = pig.flip * Math.PI;
  const tail = dead ? 0 : Math.sin(t * (eat ? 9 : 5)) * 0.25;
  return (
    <group position={[pig.x, pig.y + pig.hop, pig.z]} scale={[pig.face * pig.scale, pig.scale, 1]}>
      <mesh position={[0, 0.04 - pig.hop - pig.y, -0.4]} rotation={[-Math.PI / 2, 0, 0]} scale={[1.5 * (1 - pig.hop * 0.15), 0.5, 1]}><circleGeometry args={[1, 24]} /><MB color="#3a2f5c" opacity={0.38} depthWrite={false} /></mesh>
      <group position={[0, 0.88, 0]} rotation={[0, 0, flipA]}>
        <group position={[0, -0.88, 0]}>
          {[[-0.62, -1], [-0.34, 1], [0.42, 1], [0.7, -1]].map(([x, d], i) => (
            <group key={i} position={[x as number, 0.68, i % 2 ? 0.02 : -0.06]} rotation={[0, 0, (d as number) * swing * 0.5 + (dead ? (i % 2 ? 0.1 : -0.1) : 0)]}>
              <mesh position={[0, -0.3, -0.01]}><capsuleGeometry args={[0.135, 0.38, 4, 8]} /><MB color={INK} /></mesh>
              <mesh position={[0, -0.3, 0]}><capsuleGeometry args={[0.095, 0.38, 4, 8]} /><MB color={PINK2} /></mesh>
              <Disc p={[0.03, -0.66, 0]} s={[0.13, 0.08]} color={INK} seg={14} />
            </group>
          ))}
          <group position={[-1.05, 1.05, -0.03]} rotation={[0, 0, tail]}>
            <Arc p={[0, 0, 0]} r={0.14} t={0.07} color={INK} rot={0.6} arc={Math.PI * 1.6} />
            <Arc p={[0, 0, 0.01]} r={0.14} t={0.035} color={PINK2} rot={0.6} arc={Math.PI * 1.6} />
          </group>
          <Disc p={[0, 0.88, -0.02]} s={[1.14, 0.74]} color={INK} seg={40} />
          <Disc p={[0, 0.88, 0]} s={[1.07, 0.67]} color={PINK} seg={40} />
          <Disc p={[-0.05, 0.66, 0.01]} s={[0.82, 0.34]} color={PINK3} seg={32} opacity={0.75} />
          <Disc p={[-0.4, 1.12, 0.02]} s={[0.3, 0.2]} color="#7d4f66" seg={20} opacity={0.9} />
          <group position={[0.98, 0.98, 0.03]} rotation={[0, 0, headRot]}>
            <Disc p={[0, 0, -0.02]} s={[0.52, 0.5]} color={INK} seg={36} />
            <Disc p={[0, 0, 0]} s={[0.47, 0.45]} color={PINK} seg={36} />
            <group rotation={[0, 0, dead ? 0.6 : Math.sin(t * 6) * 0.07]}>
              <mesh position={[-0.12, 0.48, -0.01]} rotation={[0, 0, 0.25]}><circleGeometry args={[0.3, 3]} /><MB color={INK} /></mesh>
              <mesh position={[-0.12, 0.47, 0]} rotation={[0, 0, 0.25]} scale={0.8}><circleGeometry args={[0.3, 3]} /><MB color={PINK2} /></mesh>
            </group>
            <Disc p={[0.46, -0.12, 0.02]} s={[0.25, 0.2]} color={INK} seg={22} />
            <Disc p={[0.46, -0.12, 0.03]} s={[0.215, 0.165]} color={PINK3} seg={22} />
            <Disc p={[0.43, -0.1, 0.04]} s={[0.034, 0.055]} color={INK} seg={10} /><Disc p={[0.54, -0.1, 0.04]} s={[0.034, 0.055]} color={INK} seg={10} />
            <Disc p={[0.0, -0.12, 0.03]} s={[0.07, 0.05]} color="#f26a8a" opacity={0.8} seg={12} />
            {dead || (pig.shock ?? 0) > 0 ? (
              <group position={[0.1, 0.13, 0.05]}>{[[0.8], [-0.8]].map(([r], i) => <Bar key={i} p={[0, 0, 0]} s={[0.2, 0.045]} color={INK} rot={r as number} />)}</group>
            ) : (
              <group position={[0.14, 0.12, 0.05]}>
                <Disc p={[0, 0, 0]} s={[0.05, 0.058]} color={INK} seg={12} />
                <Bar p={[0, 0.055 - (eat ? 0.03 : 0), 0.01]} s={[0.16, 0.04]} color={INK} rot={-0.08} />
              </group>
            )}
            {dead && <Disc p={[0.36, -0.34, 0.04]} s={[0.07, 0.13]} color="#e0646a" seg={12} />}
          </group>
        </group>
      </group>
    </group>
  );
};
