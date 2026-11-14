import React from 'react';

export const INK = '#2a2230';
export const HEAD = '#fbf6ee';
const Z = { back: -0.06, mid: 0, front: 0.07 };

export type Mouth = 'closed' | 'open' | 'smile' | 'smirk' | 'oh' | 'laugh' | 'worry';
export type Pose = {
  x: number; y: number; z: number; face: 1 | -1; scale: number;
  bob: number; lean: number; tilt: number;            // inclinação do tronco / cabeça
  armL: [number, number]; armR: [number, number];       // [ombro, cotovelo] em rad, 0 = pendurado
  legL: [number, number]; legR: [number, number];       // [quadril, joelho]
  look: [number, number]; blink: number; brows: [number, number];
  mouth: Mouth; open: number; squash: number;
};
export const P = (p: Partial<Pose> = {}): Pose => ({
  x: 0, y: 0, z: 0, face: 1, scale: 1, bob: 0, lean: 0, tilt: 0,
  armL: [0.1, 0.1], armR: [-0.1, 0.1], legL: [0, 0], legR: [0, 0],
  look: [0, 0], blink: 0, brows: [0, 0], mouth: 'closed', open: 0, squash: 0, ...p,
});

export type Look = {
  shirt: string; shirt2: string; pants: string; shoe: string;
  hat?: 'straw' | 'chef' | 'cap' | 'scarf'; hatColor?: string;
  beard?: string; mustache?: string; apron?: string; hair?: string; glasses?: boolean;
  build?: number; // 1 = normal, >1 = mais largo
};

const Capsule: React.FC<{ len: number; r: number; color: string; z?: number }> = ({ len, r, color, z = 0 }) => (
  <>
    <mesh position={[0, -len / 2, z - 0.02]}><capsuleGeometry args={[r + 0.04, len, 4, 10]} /><meshBasicMaterial color={INK} /></mesh>
    <mesh position={[0, -len / 2, z]}><capsuleGeometry args={[r, len, 4, 10]} /><meshBasicMaterial color={color} /></mesh>
  </>
);
const Disc: React.FC<{ p: [number, number, number]; s: [number, number]; color: string; rot?: number; seg?: number }> = ({ p, s, color, rot = 0, seg = 32 }) => (
  <mesh position={p} scale={[s[0], s[1], 1]} rotation={[0, 0, rot]}><circleGeometry args={[1, seg]} /><meshBasicMaterial color={color} /></mesh>
);
const Hand: React.FC<{ z: number; children?: React.ReactNode }> = ({ z, children }) => (
  <group position={[0, -0.02, z]}>
    <Disc p={[0, -0.08, -0.01]} s={[0.17, 0.17]} color={INK} seg={20} />
    <Disc p={[0, -0.08, 0]} s={[0.135, 0.135]} color="#ffffff" seg={20} />
    {children}
  </group>
);
const Arm: React.FC<{ at: [number, number, number]; a: [number, number]; color: string; hand?: React.ReactNode }> = ({ at, a, color, hand }) => (
  <group position={at} rotation={[0, 0, a[0]]}>
    <Capsule len={0.52} r={0.06} color={color} z={at[2]} />
    <group position={[0, -0.55, 0]} rotation={[0, 0, a[1]]}>
      <Capsule len={0.5} r={0.06} color={color} z={at[2]} />
      <group position={[0, -0.52, 0]}><Hand z={at[2] + 0.03}>{hand}</Hand></group>
    </group>
  </group>
);
const Leg: React.FC<{ at: [number, number, number]; a: [number, number]; color: string; shoe: string }> = ({ at, a, color, shoe }) => (
  <group position={at} rotation={[0, 0, a[0]]}>
    <Capsule len={0.58} r={0.075} color={color} z={at[2]} />
    <group position={[0, -0.6, 0]} rotation={[0, 0, a[1]]}>
      <Capsule len={0.56} r={0.075} color={color} z={at[2]} />
      <group position={[0, -0.64, 0]}>
        <Disc p={[0.1, 0.02, at[2] - 0.01]} s={[0.25, 0.14]} color={INK} seg={20} />
        <Disc p={[0.1, 0.02, at[2]]} s={[0.21, 0.1]} color={shoe} seg={20} />
      </group>
    </group>
  </group>
);

const Mouths: React.FC<{ m: Mouth; open: number }> = ({ m, open }) => {
  const o = Math.max(open, m === 'open' ? 0.4 : 0);
  if (m === 'closed') return <mesh position={[0, -0.2, 0.2]}><boxGeometry args={[0.2, 0.035, 0.01]} /><meshBasicMaterial color={INK} /></mesh>;
  if (m === 'smile' || m === 'smirk') {
    return (
      <mesh position={[m === 'smirk' ? 0.05 : 0, -0.14, 0.2]} rotation={[0, 0, Math.PI + (m === 'smirk' ? 0.25 : 0)]}>
        <torusGeometry args={[0.15, 0.022, 6, 20, Math.PI]} /><meshBasicMaterial color={INK} />
      </mesh>
    );
  }
  if (m === 'worry') {
    return (<mesh position={[0, -0.27, 0.2]}><torusGeometry args={[0.13, 0.022, 6, 20, Math.PI]} /><meshBasicMaterial color={INK} /></mesh>);
  }
  if (m === 'laugh') {
    return (
      <group position={[0, -0.16, 0.2]}>
        <mesh rotation={[0, 0, Math.PI]} scale={[1, 0.5 + 0.9 * o, 1]}><circleGeometry args={[0.22, 20, 0, Math.PI]} /><meshBasicMaterial color={INK} /></mesh>
        <mesh position={[0, -0.09 * (0.5 + o), 0.01]} scale={[1, 0.4 + 0.3 * o, 1]}><circleGeometry args={[0.1, 14]} /><meshBasicMaterial color="#d9625f" /></mesh>
      </group>
    );
  }
  const r = m === 'oh' ? 0.085 + 0.05 * o : 0.07 + 0.07 * o;
  return <Disc p={[0, -0.21, 0.2]} s={[r * (m === 'oh' ? 1 : 1.35), r * (1 + o * 0.9)]} color={INK} seg={20} />;
};

const Head: React.FC<{ pose: Pose; look: Look }> = ({ pose, look }) => {
  const [lx, ly] = pose.look; const bl = 1 - 0.92 * pose.blink;
  return (
    <group>
      <Disc p={[0, 0, -0.01]} s={[0.6, 0.6]} color={INK} seg={48} />
      <Disc p={[0, 0, 0.0]} s={[0.555, 0.555]} color={HEAD} seg={48} />
      {look.hair && <Disc p={[-0.38, 0.28, 0.0]} s={[0.15, 0.17]} color={look.hair} />}
      {look.beard && (
        <>
          <mesh position={[0, -0.3, 0.12]} rotation={[0, 0, Math.PI]} scale={[1.0, 0.95, 1]}><circleGeometry args={[0.4, 30, 0, Math.PI]} /><meshBasicMaterial color={INK} /></mesh>
          <mesh position={[0, -0.32, 0.13]} rotation={[0, 0, Math.PI]} scale={[0.93, 0.9, 1]}><circleGeometry args={[0.4, 30, 0, Math.PI]} /><meshBasicMaterial color={look.beard} /></mesh>
        </>
      )}
      {[-1, 1].map((s) => (
        <group key={s} position={[s * 0.2, 0.06, 0.18]}>
          <Disc p={[0, 0, 0]} s={[0.085, 0.1 * bl]} color="#ffffff" seg={18} />
          <Disc p={[lx * 0.025, ly * 0.025, 0.01]} s={[0.05, 0.065 * bl]} color={INK} seg={14} />
          <mesh position={[0, 0.17 + pose.brows[s === -1 ? 0 : 1] * 0.06, 0.01]} rotation={[0, 0, -s * (pose.brows[s === -1 ? 0 : 1] * -0.35) + s * -0.0]}>
            <boxGeometry args={[0.17, 0.038, 0.01]} /><meshBasicMaterial color={INK} />
          </mesh>
        </group>
      ))}
      {look.glasses && [-1, 1].map((s) => (
        <mesh key={s} position={[s * 0.2, 0.06, 0.21]}><torusGeometry args={[0.1, 0.015, 6, 20]} /><meshBasicMaterial color={INK} /></mesh>
      ))}
      {look.mustache && (
        <group position={[0, -0.09, 0.22]}>
          <Disc p={[-0.1, 0, 0]} s={[0.12, 0.05]} color={look.mustache} rot={0.25} />
          <Disc p={[0.1, 0, 0]} s={[0.12, 0.05]} color={look.mustache} rot={-0.25} />
        </group>
      )}
      <Mouths m={pose.mouth} open={pose.open} />
      {look.hat === 'straw' && (
        <group position={[0, 0.48, 0.1]}>
          <Disc p={[0, 0, -0.01]} s={[0.82, 0.2]} color={INK} seg={40} />
          <Disc p={[0, 0, 0]} s={[0.78, 0.165]} color={look.hatColor ?? '#e6b95e'} seg={40} />
          <Disc p={[0, 0.2, 0.01]} s={[0.42, 0.34]} color={INK} seg={32} />
          <Disc p={[0, 0.2, 0.02]} s={[0.38, 0.3]} color={look.hatColor ?? '#e6b95e'} seg={32} />
          <mesh position={[0, 0.06, 0.03]}><boxGeometry args={[0.7, 0.07, 0.01]} /><meshBasicMaterial color="#b9574e" /></mesh>
        </group>
      )}
      {look.hat === 'chef' && (
        <group position={[0, 0.58, 0.1]}>
          <Disc p={[0, 0.28, -0.01]} s={[0.46, 0.4]} color={INK} /><Disc p={[0, 0.28, 0]} s={[0.42, 0.36]} color="#ffffff" />
          <mesh position={[0, -0.05, 0.02]}><boxGeometry args={[0.7, 0.2, 0.01]} /><meshBasicMaterial color={INK} /></mesh>
          <mesh position={[0, -0.05, 0.03]}><boxGeometry args={[0.65, 0.15, 0.01]} /><meshBasicMaterial color="#ffffff" /></mesh>
        </group>
      )}
      {look.hat === 'cap' && (
        <group position={[0, 0.42, 0.1]}>
          <Disc p={[0, 0.06, 0]} s={[0.55, 0.3]} color={look.hatColor ?? '#5e6d9f'} seg={32} />
          <Disc p={[0.38, -0.05, 0.01]} s={[0.3, 0.07]} color={look.hatColor ?? '#5e6d9f'} seg={20} />
        </group>
      )}
      {look.hat === 'scarf' && (
        <group position={[0, 0.4, 0.1]}>
          <Disc p={[0, 0.05, -0.01]} s={[0.6, 0.3]} color={INK} /><Disc p={[0, 0.05, 0]} s={[0.56, 0.26]} color={look.hatColor ?? '#b9574e'} />
        </group>
      )}
    </group>
  );
};

export const Character: React.FC<{ pose: Pose; look: Look; handR?: React.ReactNode; handL?: React.ReactNode }> = ({ pose, look, handR, handL }) => {
  const b = look.build ?? 1;
  const sq = pose.squash;
  return (
    <group position={[pose.x, pose.y, pose.z]} scale={[pose.face * pose.scale, pose.scale * (1 - sq * 0.5), 1]}>
      {/* sombra de contato (roxa, nunca preta) */}
      <mesh position={[0, 0.03 - pose.y + 0.02, -0.2]} rotation={[-Math.PI / 2, 0, 0]} scale={[0.8 * b, 0.3, 1]}>
        <circleGeometry args={[1, 24]} /><meshBasicMaterial color="#3d2f5c" transparent opacity={0.35} depthWrite={false} />
      </mesh>
      <group position={[0, pose.bob, 0]}>
        <Leg at={[-0.2 * b, 1.38, Z.back]} a={pose.legL} color={look.pants} shoe={look.shoe} />
        <Leg at={[0.2 * b, 1.38, Z.mid]} a={pose.legR} color={look.pants} shoe={look.shoe} />
        <group position={[0, 1.38, 0]} rotation={[0, 0, pose.lean]}>
          <Arm at={[-0.42 * b, 0.86, Z.back]} a={pose.armL} color={look.shirt2} hand={handL} />
          <Disc p={[0, 0.5, -0.01]} s={[0.54 * b, 0.66]} color={INK} />
          <Disc p={[0, 0.5, 0.0]} s={[0.5 * b, 0.62]} color={look.shirt} />
          {look.apron && <Disc p={[0, 0.34, 0.02]} s={[0.36 * b, 0.46]} color={look.apron} />}
          {look.apron && <mesh position={[0, 0.7, 0.03]}><boxGeometry args={[0.7 * b, 0.07, 0.01]} /><meshBasicMaterial color="#b9574e" /></mesh>}
          <Arm at={[0.42 * b, 0.86, Z.front]} a={pose.armR} color={look.shirt2} hand={handR} />
          <group position={[0, 1.55, 0.04]} rotation={[0, 0, pose.tilt]}>
            <Head pose={pose} look={look} />
          </group>
        </group>
      </group>
    </group>
  );
};

/** Cinemática direta 2D: posição da mão no espaço local do personagem (sem escala/flip). */
export const handPos = (pose: Pose, side: 'L' | 'R', look?: Look): [number, number] => {
  const b = look?.build ?? 1;
  const a = side === 'R' ? pose.armR : pose.armL;
  const sx = (side === 'R' ? 0.42 : -0.42) * b, sy = 0.86;
  // ombro no referencial do quadril -> rotaciona pelo lean
  const rot = (x: number, y: number, ang: number): [number, number] => [x * Math.cos(ang) - y * Math.sin(ang), x * Math.sin(ang) + y * Math.cos(ang)];
  const e1 = rot(0, -0.55, a[0]); const e2 = rot(0, -0.57, a[0] + a[1]);
  const hand: [number, number] = [sx + e1[0] + e2[0], sy + e1[1] + e2[1]];
  const [hx, hy] = rot(hand[0], hand[1], pose.lean);
  return [pose.x + hx * pose.face * pose.scale, pose.y + pose.bob + 1.38 + hy];
};
