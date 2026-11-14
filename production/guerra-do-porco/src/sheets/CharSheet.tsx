import React from 'react';
import { AbsoluteFill } from 'remotion';
import { ThreeCanvas } from '@remotion/three';
import { Character, Pose, Look } from '../characters/Rig';
import { Pig } from '../characters/Pig';
import { CUTLAR, GRIFFIN, SOLDIER, BAYNES, AIDE } from '../characters/cast';
import { idle, march, aimFire, smug, shock, laugh, stopHand } from '../characters/poses';
import { Rifle, Note, Spyglass } from '../world/props';

type Cell = { name: string; look?: Look; pose?: Pose; extra?: (p: Pose) => React.ReactNode; hand?: React.ReactNode; pig?: boolean; mode?: 'eat' | 'dead' | 'trot' };
const T0 = 2.0;
const base = (o: Partial<Pose> = {}) => ({ ...idle(T0, { off: 0.3 }), ...o });
const cells: Cell[] = [
  { name: 'Cutlar — neutro/pálpebra pesada', look: CUTLAR, pose: base() },
  { name: 'Cutlar — raiva (dentes em grade)', look: CUTLAR, pose: base({ eye: 'lid', lid: 0.35, angry: 0.7, brows: [-0.2, -0.2], mouth: 'teeth' }) },
  { name: 'Cutlar — mira e tiro', look: CUTLAR, pose: aimFire(1.0, base(), { t0: 0, tFire: 1.0 }), hand: <group rotation={[0, 0, 0]}><Rifle /></group> },
  { name: 'Griffin — zombaria (smirk)', look: GRIFFIN, pose: smug(base()), hand: <group position={[0.3, 0.2, 0.1]}><Note label="$100" s={0.8} /></group> },
  { name: 'Griffin — riso', look: GRIFFIN, pose: laugh(T0, base()) },
  { name: 'Soldado — marcha', look: SOLDIER, pose: { ...base(), ...march(T0), lid: 0.4 } },
  { name: 'Almirante — "pare"', look: BAYNES, pose: stopHand(1.0, { ...base(), lid: 0.58, mouth: 'line' }, 0) },
  { name: 'Auxiliar — choque (suor)', look: AIDE, pose: shock(1.0, base(), 0.2) },
];
export const CharSheet: React.FC = () => {
  const Z = 66, cols = 5, dx = 5.4;
  const pos = (i: number) => ({ x: ((i % cols) - (cols - 1) / 2) * dx, y: i < cols ? 0.9 : -5.3 });
  const all = [...cells, { name: 'Porco — comer', pig: true, mode: 'eat' as const }, { name: 'Porco — morto (olho X)', pig: true, mode: 'dead' as const }];
  return (
    <AbsoluteFill style={{ background: 'linear-gradient(180deg,#f3dcc0,#e8b98c)', fontFamily: 'Montserrat, Arial, sans-serif' }}>
      <ThreeCanvas width={1920} height={1080} orthographic camera={{ zoom: Z, position: [0, 0, 50], near: 0.1, far: 200 }} linear={false}>
        {all.map((c, i) => { const p = pos(i); return c.pig ?
          <Pig key={i} pig={{ x: p.x - 0.2, y: p.y, z: 0, face: 1, scale: 1.3, t: T0, mode: c.mode!, flip: c.mode === 'dead' ? 1 : 0, hop: 0 }} /> :
          <Character key={i} pose={{ ...c.pose!, x: p.x, y: p.y }} look={c.look!} handR={c.hand} />; })}
      </ThreeCanvas>
      {all.map((c, i) => { const p = pos(i); return <div key={i} style={{ position: 'absolute', left: 960 + p.x * Z - 150, top: 540 - (p.y - 0.55) * Z, width: 300, textAlign: 'center', fontSize: 20, fontWeight: 700, color: '#2a2230' }}>{c.name}</div>; })}
      <div style={{ position: 'absolute', left: 30, top: 18, fontSize: 30, fontWeight: 800, color: '#2a2230' }}>Folha de personagens — A Guerra do Porco (rig v2)</div>
    </AbsoluteFill>
  );
};
