import React from 'react';
import { Composition } from 'remotion';
import { Video } from './Video';
import { T } from './lib/timing';

export const FPS = 30;
export const Root: React.FC = () => (
  <Composition id="Tome" component={Video} durationInFrames={Math.ceil(T.total * FPS)} fps={FPS} width={1080} height={1920} />
);
