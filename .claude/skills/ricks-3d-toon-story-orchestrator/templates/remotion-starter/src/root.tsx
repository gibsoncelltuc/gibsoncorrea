import React from 'react';
import { Composition } from 'remotion';
import { ToonStarter } from './toon-starter';

export const Root: React.FC = () => (
  <Composition
    id="ToonStarter"
    component={ToonStarter}
    durationInFrames={65 * 30}
    fps={30}
    width={1080}
    height={1920}
  />
);
