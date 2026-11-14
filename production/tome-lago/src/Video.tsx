import React from 'react';
import { AbsoluteFill, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { ThreeCanvas } from '@remotion/three';
import { shotAt, T } from './lib/timing';
import { Captions } from './captions/Captions';
import { ShotS1, ShotS2, ShotS3, ShotS4, ShotS5, ShotS6, ShotS7 } from './shots/Shots';

const Shot: React.FC<{ id: string; t: number }> = ({ id, t }) => {
  switch (id) {
    case 'S1': return <ShotS1 t={t} />; case 'S2': return <ShotS2 t={t} />; case 'S3': return <ShotS3 t={t} />;
    case 'S4': return <ShotS4 t={t} />; case 'S5': return <ShotS5 t={t} />; case 'S6': return <ShotS6 t={t} />;
    default: return <ShotS7 t={t} />;
  }
};
export const Video: React.FC = () => {
  const frame = useCurrentFrame(); const { fps, width, height } = useVideoConfig();
  const t = frame / fps; const shot = shotAt(t);
  return (
    <AbsoluteFill style={{ background: '#2a2230' }}>
      <ThreeCanvas width={width} height={height} camera={{ fov: 58, position: [0, 2, 10], near: 0.1, far: 600 }} gl={{ antialias: true }} linear={false}>
        <Shot id={shot.id} t={t} />
      </ThreeCanvas>
      {/* papel + vinheta + grade */}
      <AbsoluteFill style={{ backgroundImage: `url(${staticFile('paper.png')})`, backgroundSize: 'cover', mixBlendMode: 'multiply', opacity: 0.2 }} />
      <AbsoluteFill style={{ background: 'radial-gradient(ellipse at 50% 46%, rgba(0,0,0,0) 55%, rgba(42,34,48,0.30) 100%)' }} />
      <AbsoluteFill style={{ background: 'linear-gradient(180deg, rgba(255,194,122,0.07), rgba(113,133,192,0.10))', mixBlendMode: 'soft-light' }} />
      <Captions />
    </AbsoluteFill>
  );
};
