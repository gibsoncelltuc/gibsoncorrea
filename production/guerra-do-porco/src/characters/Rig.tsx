// Rig 2D cut-out v2 (estilo Ricks Clips, observado): cabeça branca sombreada, contorno grosso, olhos de pálpebra pesada,
// sobrancelhas grossas, corpo feijão com tecido padronizado, membros macarrão, mãos redondas.
import React, { createContext, useContext, useMemo } from 'react';
import * as THREE from 'three';
import { fabricTex } from '../world/tex';

export const INK = '#2a2230';
export const ModeCtx = createContext<{ animatic: boolean }>({ animatic: false });
const gray = (c: string) => { if (c === INK) return INK; const k = new THREE.Color(c); const l = Math.pow(0.2126 * k.r + 0.7152 * k.g + 0.0722 * k.b, 1 / 2.2); const v = Math.round((0.35 + 0.5 * l) * 255); return `rgb(${v},${v},${v + 6})`; };
export const MB: React.FC<{ color: string; opacity?: number; map?: THREE.Texture; depthWrite?: boolean }> = ({ color, opacity = 1, map, depthWrite = true }) => {
  const { animatic } = useContext(ModeCtx);
  return <meshBasicMaterial color={animatic ? gray(color) : color} map={animatic ? undefined : map} transparent={opacity < 1} opacity={opacity} depthWrite={depthWrite} toneMapped={false} />;
};

export type Eye = 'lid' | 'wide' | 'arc' | 'dot' | 'x';
export type Mouth = 'line' | 'smirk' | 'smile' | 'grin' | 'laugh' | 'oh' | 'shout' | 'frown' | 'teeth';
export type Pose = {
  x: number; y: number; z: number; face: 1 | -1; scale: number;
  bob: number; lean: number; tilt: number;
  armL: [number, number]; armR: [number, number]; legL: [number, number]; legR: [number, number];
  look: [number, number]; blink: number; lid: number; eye: Eye; brows: [number, number]; angry: number;
  mouth: Mouth; open: number; sweat: number; squash: number;
};
export const P = (p: Partial<Pose> = {}): Pose => ({
  x: 0, y: 0, z: 0, face: 1, scale: 1, bob: 0, lean: 0, tilt: 0,
  armL: [0.1, 0.1], armR: [-0.1, 0.1], legL: [0, 0], legR: [0, 0],
  look: [0, 0], blink: 0, lid: 0.42, eye: 'lid', brows: [0, 0], angry: 0, mouth: 'line', open: 0, sweat: 0, squash: 0, ...p,
});
export type Look = {
  shirt: string; shirt2?: string; pattern?: 'plaid' | 'stripes' | 'tweed' | 'denim' | 'uniform' | 'plain';
  outfit?: 'plain' | 'overalls' | 'waistcoat' | 'uniform' | 'admiral';
  trim?: string; pants: string; sleeve?: string; shoe: string;
  hat?: 'straw' | 'kepi' | 'flatcap' | 'bicorn' | 'peaked'; hatColor?: string; hatBand?: string;
  sideburns?: string; mustache?: string; beard?: string; glasses?: boolean; blush?: boolean; scarf?: string;
  build?: number; headScale?: number; tint?: string;
};

const Z = 0.012;
export const Disc: React.FC<{ p: [number, number, number]; s: [number, number]; color: string; rot?: number; seg?: number; opacity?: number; map?: THREE.Texture }> = ({ p, s, color, rot = 0, seg = 32, opacity, map }) => (
  <mesh position={p} scale={[s[0], s[1], 1]} rotation={[0, 0, rot]}><circleGeometry args={[1, seg]} /><MB color={color} opacity={opacity} map={map} /></mesh>
);
export const Bar: React.FC<{ p: [number, number, number]; s: [number, number]; color: string; rot?: number }> = ({ p, s, color, rot = 0 }) => (
  <mesh position={p} rotation={[0, 0, rot]}><boxGeometry args={[s[0], s[1], 0.004]} /><MB color={color} /></mesh>
);
export const Arc: React.FC<{ p: [number, number, number]; r: number; t: number; color: string; rot?: number; arc?: number }> = ({ p, r, t, color, rot = 0, arc = Math.PI }) => (
  <mesh position={p} rotation={[0, 0, rot]}><torusGeometry args={[r, t, 6, 20, arc]} /><MB color={color} /></mesh>
);
const stadium = (w: number, h: number) => {
  const r = w / 2, hh = Math.max(0, (h - w) / 2), s = new THREE.Shape();
  s.absarc(0, hh, r, 0, Math.PI, false); s.lineTo(-r, -hh); s.absarc(0, -hh, r, Math.PI, Math.PI * 2, false); s.closePath(); return new THREE.ShapeGeometry(s, 20);
};
const Limb: React.FC<{ len: number; r: number; color: string; z: number }> = ({ len, r, color, z }) => (
  <>
    <mesh position={[0, -len / 2, z - Z]}><capsuleGeometry args={[r + 0.04, len, 4, 10]} /><MB color={INK} /></mesh>
    <mesh position={[0, -len / 2, z]}><capsuleGeometry args={[r, len, 4, 10]} /><MB color={color} /></mesh>
  </>
);
const Hand: React.FC<{ z: number; children?: React.ReactNode }> = ({ z, children }) => (
  <group position={[0, -0.03, z]}>
    <Disc p={[0, -0.07, 0]} s={[0.125, 0.125]} color={INK} seg={20} />
    <Disc p={[0, -0.07, Z]} s={[0.088, 0.088]} color="#fbf8ff" seg={20} />
    {children}
  </group>
);
const Arm: React.FC<{ at: [number, number, number]; a: [number, number]; color: string; hand?: React.ReactNode }> = ({ at, a, color, hand }) => (
  <group position={at} rotation={[0, 0, a[0]]}>
    <Limb len={0.5} r={0.04} color={color} z={0} />
    <group position={[0, -0.52, 0]} rotation={[0, 0, a[1]]}>
      <Limb len={0.46} r={0.04} color={color} z={0} />
      <group position={[0, -0.48, 0]}><Hand z={0.02}>{hand}</Hand></group>
    </group>
  </group>
);
const Leg: React.FC<{ at: [number, number, number]; a: [number, number]; color: string; shoe: string }> = ({ at, a, color, shoe }) => (
  <group position={at} rotation={[0, 0, a[0]]}>
    <Limb len={0.56} r={0.045} color={color} z={0} />
    <group position={[0, -0.58, 0]} rotation={[0, 0, a[1]]}>
      <Limb len={0.55} r={0.045} color={color} z={0} />
      <group position={[0, -0.62, 0]}>
        <Disc p={[0.1, 0.02, -Z]} s={[0.2, 0.115]} color={INK} seg={20} />
        <Disc p={[0.1, 0.02, 0]} s={[0.16, 0.08]} color={shoe} seg={20} />
      </group>
    </group>
  </group>
);

const Drop: React.FC<{ p: [number, number]; ph: number }> = ({ p, ph }) => {
  const f = ((ph % 1) + 1) % 1;
  return (
    <group position={[p[0], p[1] - f * 0.35, 0.3]} scale={1 - f * 0.4}>
      <Disc p={[0, -0.03, 0]} s={[0.075, 0.075]} color={INK} seg={16} /><Disc p={[0, -0.03, Z]} s={[0.055, 0.055]} color="#a9dcff" seg={16} />
      <mesh position={[0, 0.06, 0]}><circleGeometry args={[0.06, 3]} /><MB color={INK} /></mesh>
      <mesh position={[0, 0.058, Z]} scale={0.75}><circleGeometry args={[0.06, 3]} /><MB color="#a9dcff" /></mesh>
    </group>
  );
};

const Eyes: React.FC<{ pose: Pose }> = ({ pose }) => {
  const [lx, ly] = pose.look; const lid = Math.min(1, pose.lid + pose.blink * 0.9);
  return (
    <>
      {[-1, 1].map((s) => {
        const b = pose.brows[s === -1 ? 0 : 1];
        return (
          <group key={s} position={[s * 0.2, 0.04, 0.2]}>
            {pose.eye === 'lid' && (
              <>
                {lid < 0.92 && <Disc p={[lx * 0.03, -0.012 + ly * 0.02, 0]} s={[0.05, 0.056]} color={INK} seg={14} />}
                <Bar p={[0, 0.048 - lid * 0.075, Z]} s={[0.215, 0.052]} color={INK} rot={s * pose.angry * -0.2} />
                <Arc p={[0, -0.015, 0]} r={0.085} t={0.012} color={INK} rot={Math.PI} arc={Math.PI * 0.7} />
              </>
            )}
            {pose.eye === 'wide' && (
              <>
                <Disc p={[0, 0, 0]} s={[0.125, 0.125]} color={INK} seg={22} /><Disc p={[0, 0, Z]} s={[0.1, 0.1]} color="#ffffff" seg={22} />
                <Disc p={[lx * 0.03, ly * 0.03, 2 * Z]} s={[0.03, 0.03]} color={INK} seg={12} />
              </>
            )}
            {pose.eye === 'arc' && <Arc p={[0, -0.03, 0]} r={0.085} t={0.03} color={INK} rot={0} />}
            {pose.eye === 'dot' && <Disc p={[0, 0, 0]} s={[0.05, 0.06]} color={INK} seg={14} />}
            {pose.eye === 'x' && (<><Bar p={[0, 0, 0]} s={[0.17, 0.035]} color={INK} rot={0.8} /><Bar p={[0, 0, 0]} s={[0.17, 0.035]} color={INK} rot={-0.8} /></>)}
            <mesh position={[0, 0.17 + b * 0.07, Z]} rotation={[0, 0, s * pose.angry * 0.5 + (pose.eye === 'wide' ? -s * 0.0 : 0)]}>
              <boxGeometry args={[0.2, 0.045, 0.004]} /><MB color={INK} />
            </mesh>
          </group>
        );
      })}
    </>
  );
};

const Mouths: React.FC<{ m: Mouth; open: number }> = ({ m, open }) => {
  const o = Math.max(0, Math.min(1, open));
  const teeth = (w: number, h: number, cols: number, y: number) => (
    <group position={[0, y, 0]}>
      <Bar p={[0, 0, 0]} s={[w + 0.05, h + 0.05]} color={INK} /><Bar p={[0, 0, Z]} s={[w, h]} color="#fbf8ff" />
      {Array.from({ length: cols - 1 }, (_, i) => <Bar key={i} p={[-w / 2 + (i + 1) * (w / cols), 0, 2 * Z]} s={[0.012, h]} color={INK} />)}
      <Bar p={[0, 0, 2 * Z]} s={[w, 0.012]} color={INK} />
    </group>
  );
  if (m === 'line') return <Bar p={[0, -0.21, 0.2]} s={[0.17, 0.034]} color={INK} />;
  if (m === 'smirk') return <Arc p={[0.05, -0.15, 0.2]} r={0.13} t={0.022} color={INK} rot={Math.PI + 0.3} arc={Math.PI * 0.75} />;
  if (m === 'smile') return <Arc p={[0, -0.14, 0.2]} r={0.15} t={0.024} color={INK} rot={Math.PI} />;
  if (m === 'frown') return <Arc p={[0, -0.3, 0.2]} r={0.13} t={0.024} color={INK} />;
  if (m === 'teeth') return <group position={[0, 0, 0.2]}>{teeth(0.3, 0.1, 5, -0.22)}</group>;
  if (m === 'grin') return <group position={[0, 0, 0.2]}><Arc p={[0, -0.12, 0]} r={0.2} t={0.026} color={INK} rot={Math.PI} />{teeth(0.26, 0.07, 4, -0.21)}</group>;
  if (m === 'laugh') {
    return (
      <group position={[0, -0.14, 0.2]}>
        <mesh rotation={[0, 0, Math.PI]} scale={[1, 0.7 + 0.5 * o, 1]}><circleGeometry args={[0.26, 24, 0, Math.PI]} /><MB color={INK} /></mesh>
        <Bar p={[0, -0.02, Z]} s={[0.38, 0.07]} color="#fbf8ff" />
        <mesh position={[0, -0.18 * (0.7 + 0.5 * o), Z]} scale={[1, 0.45, 1]}><circleGeometry args={[0.12, 14]} /><MB color="#e0646a" /></mesh>
      </group>
    );
  }
  if (m === 'shout') return <Disc p={[0, -0.24, 0.2]} s={[0.12 + 0.03 * o, 0.1 + 0.08 * o]} color={INK} seg={22} />;
  return <Disc p={[0, -0.22, 0.2]} s={[0.065 + 0.03 * o, 0.075 + 0.03 * o]} color={INK} seg={18} />;
};

const Head: React.FC<{ pose: Pose; look: Look }> = ({ pose, look }) => {
  const R = 0.56, tint = look.tint ?? '#ffffff';
  return (
    <group scale={look.headScale ?? 1}>
      <Disc p={[0, 0, -2 * Z]} s={[R + 0.047, R + 0.047]} color={INK} seg={56} />
      <Disc p={[0, 0, -Z]} s={[R, R]} color="#d6d2ee" seg={56} />
      <Disc p={[0.04, 0.045, 0]} s={[R - 0.052, R - 0.052]} color={tint === '#ffffff' ? '#fbf8ff' : tint} seg={56} />
      {look.blush && [-1, 1].map((s) => <Disc key={s} p={[s * 0.36, -0.1, 0.1]} s={[0.075, 0.055]} color="#f3a2ae" opacity={0.85} seg={16} />)}
      {look.sideburns && [-1, 1].map((s) => <Disc key={s} p={[s * 0.47, -0.02, 0.1]} s={[0.085, 0.2]} color={look.sideburns!} rot={s * -0.15} seg={16} />)}
      {look.beard && <mesh position={[0, -0.12, 0.13]} rotation={[0, 0, Math.PI]}><circleGeometry args={[0.43, 28, 0, Math.PI]} /><MB color={look.beard} /></mesh>}
      <Eyes pose={pose} />
      {look.glasses && [-1, 1].map((s) => <Arc key={s} p={[s * 0.2, 0.04, 0.24]} r={0.115} t={0.014} color={INK} arc={Math.PI * 2} />)}
      {look.mustache && <group position={[0, -0.085, 0.24]}><Disc p={[-0.1, 0, 0]} s={[0.12, 0.05]} color={look.mustache} rot={0.3} /><Disc p={[0.1, 0, 0]} s={[0.12, 0.05]} color={look.mustache} rot={-0.3} /></group>}
      <Mouths m={pose.mouth} open={pose.open} />
      {pose.sweat > 0 && (<><Drop p={[0.46, 0.2]} ph={pose.sweat} /><Drop p={[-0.5, 0.12]} ph={pose.sweat + 0.5} /></>)}
      {look.hat === 'straw' && (
        <group position={[0, 0.47, 0.14]}>
          <Disc p={[0, 0, -Z]} s={[0.86, 0.2]} color={INK} seg={40} /><Disc p={[0, 0, 0]} s={[0.81, 0.165]} color={look.hatColor ?? '#e8c068'} seg={40} />
          <Disc p={[0, 0.2, 0]} s={[0.44, 0.34]} color={INK} /><Disc p={[0, 0.2, Z]} s={[0.4, 0.3]} color={look.hatColor ?? '#e8c068'} />
          <Bar p={[0, 0.06, 2 * Z]} s={[0.74, 0.08]} color={look.hatBand ?? '#3a6aa8'} />
        </group>
      )}
      {look.hat === 'kepi' && (
        <group position={[0, 0.46, 0.14]} rotation={[0, 0, 0.06]}>
          <Disc p={[0.02, 0.08, 0]} s={[0.5, 0.27]} color={INK} /><Disc p={[0.02, 0.08, Z]} s={[0.46, 0.235]} color={look.hatColor ?? '#2f4f8a'} />
          <Disc p={[0.36, -0.07, 0]} s={[0.34, 0.075]} color={INK} /><Disc p={[0.36, -0.07, Z]} s={[0.3, 0.05]} color="#1f2f55" />
          <Disc p={[0, 0.08, 3 * Z]} s={[0.07, 0.07]} color="#f0c250" seg={14} />
        </group>
      )}
      {look.hat === 'flatcap' && (
        <group position={[0, 0.42, 0.14]}>
          <Disc p={[0, 0.07, 0]} s={[0.62, 0.3]} color={INK} /><Disc p={[0, 0.07, Z]} s={[0.575, 0.262]} color={look.hatColor ?? '#7a6a52'} map={fabricTex('tweed', look.hatColor ?? '#7a6a52', '#b9a27a')} />
          <Disc p={[0.42, -0.06, 0]} s={[0.3, 0.07]} color={INK} /><Disc p={[0.42, -0.06, Z]} s={[0.26, 0.045]} color={look.hatColor ?? '#7a6a52'} />
        </group>
      )}
      {look.hat === 'bicorn' && (
        <group position={[0, 0.5, 0.14]}>
          <Disc p={[0, 0.05, 0]} s={[0.78, 0.26]} color={INK} seg={40} /><Disc p={[0, 0.05, Z]} s={[0.73, 0.22]} color="#1c1a2c" seg={40} />
          <Arc p={[0, 0.0, 2 * Z]} r={0.7} t={0.022} color="#f0c250" rot={0} arc={Math.PI * 0.22} />
          <Disc p={[-0.62, 0.1, 0]} s={[0.15, 0.18]} color={INK} /><Disc p={[0.62, 0.1, 0]} s={[0.15, 0.18]} color={INK} />
          <Disc p={[0, 0.1, 3 * Z]} s={[0.07, 0.07]} color="#c8372f" seg={14} /><Bar p={[0, 0.0, 2 * Z]} s={[0.95, 0.04]} color="#f0c250" />
        </group>
      )}
      {look.hat === 'peaked' && (
        <group position={[0, 0.44, 0.14]}>
          <Disc p={[0, 0.08, 0]} s={[0.56, 0.28]} color={INK} /><Disc p={[0, 0.08, Z]} s={[0.52, 0.245]} color={look.hatColor ?? '#1f2f55'} />
          <Bar p={[0, -0.02, 2 * Z]} s={[0.78, 0.09]} color="#f6f1e6" /><Disc p={[0.38, -0.08, 0]} s={[0.3, 0.07]} color="#1a1a2a" />
          <Disc p={[0, 0.04, 3 * Z]} s={[0.07, 0.07]} color="#f0c250" seg={14} />
        </group>
      )}
    </group>
  );
};

export const Character: React.FC<{ pose: Pose; look: Look; handR?: React.ReactNode; handL?: React.ReactNode }> = ({ pose, look, handR, handL }) => {
  const b = look.build ?? 1, o = look.outfit ?? 'plain';
  const torsoG = useMemo(() => stadium(0.9 * b, 1.4), [b]);
  const torsoO = useMemo(() => stadium(0.9 * b + 0.1, 1.5), [b]);
  const map = useMemo(() => (look.pattern && look.pattern !== 'plain' ? fabricTex(look.pattern, look.shirt, look.shirt2 ?? '#ffffff') : undefined), [look.pattern, look.shirt, look.shirt2]);
  const sleeve = look.sleeve ?? '#2f2a46';
  const sq = pose.squash;
  return (
    <group position={[pose.x, pose.y, pose.z]} scale={[pose.face * pose.scale, pose.scale * (1 - sq * 0.5), 1]}>
      <mesh position={[0, 0.03 - pose.y + 0.02, -0.25]} rotation={[-Math.PI / 2, 0, 0]} scale={[0.85 * b, 0.32, 1]}><circleGeometry args={[1, 24]} /><MB color="#3a2f5c" opacity={0.38} depthWrite={false} /></mesh>
      <group position={[0, pose.bob, 0]}>
        <Leg at={[-0.2 * b, 1.38, -0.08]} a={pose.legL} color={look.pants} shoe={look.shoe} />
        <Leg at={[0.2 * b, 1.38, 0.0]} a={pose.legR} color={look.pants} shoe={look.shoe} />
        <group position={[0, 1.38, 0]} rotation={[0, 0, pose.lean]}>
          <Arm at={[-0.45 * b, 0.95, -0.1]} a={pose.armL} color={sleeve} hand={handL} />
          <mesh geometry={torsoO} position={[0, 0.55, -0.02]}><MB color={INK} /></mesh>
          <mesh geometry={torsoG} position={[0, 0.55, 0]}><MB color={look.shirt} map={map} /></mesh>
          {o === 'overalls' && (<>
            <Bar p={[0, 0.45, 0.02]} s={[0.62 * b, 0.62]} color="#3a62a8" /><Bar p={[-0.2 * b, 0.95, 0.025]} s={[0.07, 0.5]} color="#3a62a8" /><Bar p={[0.2 * b, 0.95, 0.025]} s={[0.07, 0.5]} color="#3a62a8" />
            <Disc p={[-0.2 * b, 0.7, 0.04]} s={[0.05, 0.05]} color="#f0c250" seg={12} /><Disc p={[0.2 * b, 0.7, 0.04]} s={[0.05, 0.05]} color="#f0c250" seg={12} />
            <Bar p={[0.12, 0.38, 0.04]} s={[0.22, 0.2]} color="#d8b06a" />
          </>)}
          {o === 'waistcoat' && (<>
            <mesh position={[0, 0.5, 0.02]}><circleGeometry args={[0.43 * b, 3]} /><MB color={look.trim ?? '#5a7a52'} /></mesh>
            <Disc p={[0, 0.05, 0.04]} s={[0.045, 0.045]} color="#f0c250" seg={10} /><Disc p={[0, 0.25, 0.04]} s={[0.045, 0.045]} color="#f0c250" seg={10} />
            <Bar p={[0, 0.78, 0.04]} s={[0.1, 0.34]} color="#b9363a" />
          </>)}
          {(o === 'uniform' || o === 'admiral') && (<>
            <Bar p={[0, 0.55, 0.02]} s={[0.1, 1.2]} color={look.trim ?? '#f0c250'} />
            {[0.95, 0.72, 0.49, 0.26, 0.03].map((y, i) => <Disc key={i} p={[0.0, y, 0.04]} s={[0.052, 0.052]} color="#f6cf5a" seg={12} />)}
            {o === 'uniform' && <Bar p={[0, 0.55, 0.05]} s={[0.15, 1.15]} color="#f6f1e6" rot={0.7} />}
            {o === 'admiral' && (<>
              <Disc p={[-0.38 * b, 1.13, 0.04]} s={[0.17, 0.09]} color={INK} rot={0.2} /><Disc p={[-0.38 * b, 1.13, 0.05]} s={[0.145, 0.07]} color="#f0c250" rot={0.2} />
              <Disc p={[0.38 * b, 1.13, 0.04]} s={[0.17, 0.09]} color={INK} rot={-0.2} /><Disc p={[0.38 * b, 1.13, 0.05]} s={[0.145, 0.07]} color="#f0c250" rot={-0.2} />
              <Disc p={[0.22 * b, 0.82, 0.05]} s={[0.075, 0.075]} color="#c8372f" seg={14} /><Bar p={[0, 0.2, 0.04]} s={[0.78 * b, 0.07]} color="#c8372f" />
            </>)}
          </>)}
          {look.scarf && <Bar p={[0, 1.08, 0.06]} s={[0.55 * b, 0.1]} color={look.scarf} />}
          <Arm at={[0.45 * b, 0.95, 0.1]} a={pose.armR} color={sleeve} hand={handR} />
          <group position={[0, 1.79, 0.06]} rotation={[0, 0, pose.tilt]}><Head pose={pose} look={look} /></group>
        </group>
      </group>
    </group>
  );
};

/** Cinemática direta 2D: posição e ângulo da mão no referencial do mundo (para ligar props, tiro, etc.). */
export const handFrame = (pose: Pose, side: 'L' | 'R', look?: Look): { pos: [number, number]; ang: number } => {
  const b = look?.build ?? 1, a = side === 'R' ? pose.armR : pose.armL;
  const sx = (side === 'R' ? 0.45 : -0.45) * b, sy = 0.95;
  const rot = (x: number, y: number, t: number): [number, number] => [x * Math.cos(t) - y * Math.sin(t), x * Math.sin(t) + y * Math.cos(t)];
  const e1 = rot(0, -0.52 - 0.03, a[0]), e2 = rot(0, -0.46 - 0.08, a[0] + a[1]);
  const [hx, hy] = rot(sx + e1[0] + e2[0], sy + e1[1] + e2[1], pose.lean);
  return { pos: [pose.x + hx * pose.face * pose.scale, pose.y + pose.bob + 1.38 + hy * pose.scale], ang: a[0] + a[1] + pose.lean };
};
export const handPos = (pose: Pose, side: 'L' | 'R', look?: Look): [number, number] => handFrame(pose, side, look).pos;
