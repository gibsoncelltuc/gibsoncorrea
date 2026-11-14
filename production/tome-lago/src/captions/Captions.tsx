import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import '@fontsource/montserrat/800.css';
import { T } from '../lib/timing';

type Chunk = { text: string; start: number; end: number };
const clean = (s: string) => s.replace(/[.,!?:;—"]+$/g, '').replace(/^["—]+/, '');
export const CHUNKS: Chunk[] = (() => {
  const out: Chunk[] = []; const w = T.words;
  for (let i = 0; i < w.length; i++) {
    const a = w[i], b = w[i + 1];
    const endsSentence = /[.!?:]$/.test(a.text);
    const merge = b && b.line === a.line && !endsSentence && (a.text.length <= 3 || (b.text.length <= 3 && a.text.length <= 6));
    if (merge) { out.push({ text: `${clean(a.text)} ${clean(b.text)}`, start: a.start, end: b.end }); i++; }
    else out.push({ text: clean(a.text), start: a.start, end: a.end });
  }
  return out;
})();

export const Captions: React.FC = () => {
  const frame = useCurrentFrame(); const { fps, width, height } = useVideoConfig();
  const t = frame / fps;
  let idx = -1; for (let i = 0; i < CHUNKS.length; i++) if (t >= CHUNKS[i].start - 0.1) idx = i; else break;
  if (idx < 0) return null;
  const c = CHUNKS[idx]; const next = CHUNKS[idx + 1];
  if (t > c.end + 0.35 && (!next || t < next.start - 0.1)) return null;
  const age = t - (c.start - 0.1);
  const pop = age < 0.09 ? 1.08 - 0.08 * (age / 0.09) : 1;
  const k = width / 1080;
  return (
    <div style={{ position: 'absolute', left: 0, right: 0, top: height * (1345 / 1920) - 60 * k, height: 120 * k, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
      <div style={{ fontFamily: 'Montserrat, sans-serif', fontWeight: 800, fontSize: 76 * k, color: '#fff', WebkitTextStroke: `${15 * k}px #120e1a`, paintOrder: 'stroke fill', transform: `scale(${pop})`, letterSpacing: 1 * k, textAlign: 'center', whiteSpace: 'nowrap' }}>
        {c.text}
      </div>
    </div>
  );
};
