import React from 'react';
import { Composition } from 'remotion';
import { Montage, Captions } from './Montage';
import data from './data.json';
const base = { durationInFrames: Math.round(data.duration * data.fps), fps: data.fps, width: data.width, height: data.height };
export const Root: React.FC = () => (
  <>
    <Composition id="Montage" component={Montage} {...base} />
    <Composition id="Captions" component={Captions} {...base} />
  </>
);
