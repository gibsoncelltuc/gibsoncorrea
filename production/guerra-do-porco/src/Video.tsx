import React from 'react';
import { AbsoluteFill, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { ThreeCanvas } from '@remotion/three';
import { SHOTS, DIS, BANGS } from './lib/timing';
import { Captions } from './captions/Captions';
import { ModeCtx } from './characters/Rig';
import { ShotS1, ShotS2, ShotS3, ShotS4, ShotS5, ShotS6 } from './shots/Shots';
import { clamp } from './lib/anim';

const Shot: React.FC<{ id: string; t: number }> = ({ id, t }) => {
  switch (id) {
    case 'S1': return <ShotS1 t={t} />; case 'S2': return <ShotS2 t={t} />; case 'S3': return <ShotS3 t={t} />;
    case 'S4': return <ShotS4 t={t} />; case 'S5': return <ShotS5 t={t} />; default: return <ShotS6 t={t} />;
  }
};
// grade: saturação alta + contraste (observado no canal); bloom/raios/papel por overlays
const GRADE = 'saturate(1.28) contrast(1.06)';
export const Video: React.FC<{ animatic?: boolean }> = ({ animatic = false }) => {
  const frame = useCurrentFrame(); const { fps, width, height } = useVideoConfig();
  const t = frame / fps;
  const layers = SHOTS.map((s, i) => ({ id: s.id, vis: t >= s.start - DIS / 2 && t < s.end + DIS / 2, op: i === 0 ? 1 : clamp((t - (s.start - DIS / 2)) / DIS) })).filter((l) => l.vis);
  const flash = Math.max(0, ...BANGS.map((b) => (t >= b && t < b + 0.14 ? 0.85 * (1 - (t - b) / 0.14) : 0)));
  return (
    <AbsoluteFill style={{ background: '#2a2230' }}>
      {layers.map((l) => (
        <AbsoluteFill key={l.id} style={{ opacity: l.op, filter: animatic ? 'none' : GRADE }}>
          <ThreeCanvas width={width} height={height} camera={{ fov: 58, position: [0, 2, 10], near: 0.1, far: 900 }} gl={{ antialias: true }} linear={false}>
            <ModeCtx.Provider value={{ animatic }}><Shot id={l.id} t={t} /></ModeCtx.Provider>
          </ThreeCanvas>
        </AbsoluteFill>
      ))}
      {!animatic && <>
        <AbsoluteFill style={{ background: 'radial-gradient(ellipse at 76% 16%, rgba(255,214,150,0.22), rgba(255,214,150,0) 48%)', mixBlendMode: 'screen' }} />
        <AbsoluteFill style={{ backgroundImage: `url(${staticFile('paper.png')})`, backgroundSize: 'cover', mixBlendMode: 'multiply', opacity: 0.16 }} />
        <AbsoluteFill style={{ background: 'radial-gradient(ellipse at 50% 46%, rgba(0,0,0,0) 52%, rgba(34,26,54,0.34) 100%)' }} />
        <AbsoluteFill style={{ background: 'linear-gradient(180deg, rgba(255,194,122,0.08), rgba(113,133,192,0.12))', mixBlendMode: 'soft-light' }} />
      </>}
      {flash > 0 && <AbsoluteFill style={{ background: '#fff4d6', opacity: flash }} />}
      <Captions />
    </AbsoluteFill>
  );
};
