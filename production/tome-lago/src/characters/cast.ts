import type { Look } from './Rig';
export const TOME: Look = { shirt: '#6f87c6', shirt2: '#6f87c6', pants: '#8a6a52', shoe: '#6a4a3a', hat: 'straw', hatColor: '#e6b95e', beard: '#d8d2e4', build: 0.95 };
export const ZECA: Look = { shirt: '#d9724f', shirt2: '#d9724f', pants: '#4a4a78', shoe: '#3a2f48', hat: 'chef', mustache: INK_(), apron: '#fbf6ee', build: 1.25 };
export const ANA: Look = { shirt: '#4c9292', shirt2: '#4c9292', pants: '#5e6d9f', shoe: '#7a4a3a', hat: 'scarf', hatColor: '#b9574e', hair: '#7a4a3a', build: 0.92 };
export const VIL = (i: number): Look => ([
  { shirt: '#b9574e', shirt2: '#b9574e', pants: '#5e6d9f', shoe: '#3a2f48', hat: 'cap', hatColor: '#4c6a9a' },
  { shirt: '#8274a7', shirt2: '#8274a7', pants: '#6a5a4a', shoe: '#3a2f48', hat: 'scarf', hatColor: '#e8b04a', hair: '#4a3a3a' },
  { shirt: '#e8b04a', shirt2: '#e8b04a', pants: '#3d4a78', shoe: '#5a3a3a', glasses: true, build: 1.1 },
  { shirt: '#4c9292', shirt2: '#4c9292', pants: '#8a6a52', shoe: '#3a2f48', hat: 'cap', hatColor: '#d9724f' },
  { shirt: '#c97a4a', shirt2: '#c97a4a', pants: '#4a4a78', shoe: '#3a2f48', hair: '#d8d2e4' },
] as Look[])[i % 5];
function INK_() { return '#2a2230'; }
