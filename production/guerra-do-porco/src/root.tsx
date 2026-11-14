import React from 'react';
import { Composition } from 'remotion';
import { Video } from './Video';
import { T } from './lib/timing';
import { CharSheet } from './sheets/CharSheet';
export const FPS = 30;
export const Root: React.FC = () => (
  <>
    <Composition id="Porco" component={Video} durationInFrames={Math.ceil(T.total * FPS)} fps={FPS} width={1080} height={1920} defaultProps={{ animatic: false }} />
    <Composition id="CharSheet" component={CharSheet} durationInFrames={1} fps={30} width={1920} height={1080} />
  </>
);
