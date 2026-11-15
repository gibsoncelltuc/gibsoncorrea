// Montagem do piloto em Remotion: quadros 3D renderizados no Blender (Cycles) → sequências, dissolves de 0,4 s, legendas em React (Montserrat ExtraBold) e áudio mixado.
// A cor (grade, bloom, vinheta, grão) e o encode ficam no FFmpeg (blender/grade.py); aqui só edição/legendas/áudio — o papel do Remotion.
import React from 'react';
import { AbsoluteFill, Audio, Img, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import '@fontsource/montserrat/800.css';
import data from './data.json';

const pad = (n: number) => String(n).padStart(4, '0');
// Quadro de Blender a mostrar em `abs` (o mais recente que existe — com só a passada 1 repete o quadro anterior, como o FFmpeg fazia)
const pick = (have: number[], abs: number) => { let best = have[0]; for (const n of have) { if (n <= abs) best = n; else break; } return best; };

const Shot: React.FC<{ id: string; have: number[]; n0: number; fade: boolean }> = ({ id, have, n0, fade }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const n = pick(have, n0 + f);
  const opacity = fade ? interpolate(f, [0, Math.round(data.dissolve * fps)], [0, 1], { extrapolateRight: 'clamp' }) : 1;
  return <AbsoluteFill style={{ opacity }}><Img src={staticFile(`frames/${id}/f${pad(n)}.png`)} style={{ width: '100%', height: '100%' }} /></AbsoluteFill>;
};

// Legenda: 1–2 palavras, Montserrat ExtraBold, branca, contorno escuro fino + sombra suave; ascendente ≈ 5,4 % da altura, linha de base a 72,7 % (medido nas referências)
const Caption: React.FC<{ text: string }> = ({ text }) => {
  const f = useCurrentFrame(); const { height } = useVideoConfig();
  const k = height / 960; const pop = interpolate(f, [0, 3], [1.08, 1], { extrapolateRight: 'clamp' });
  return (
    <AbsoluteFill style={{ justifyContent: 'flex-start', alignItems: 'center' }}>
      <div style={{ position: 'absolute', top: `${71.4}%`, transform: `translateY(-50%) scale(${pop})`, fontFamily: 'Montserrat', fontWeight: 800, fontSize: 39.5 * k, lineHeight: 1, whiteSpace: 'nowrap', color: '#fff',
                    WebkitTextStroke: `${7 * k}px #120e1a`, paintOrder: 'stroke fill', textShadow: `${1.5 * k}px ${2 * k}px ${1.5 * k}px rgba(0,0,0,.55)` }}>{text}</div>
    </AbsoluteFill>
  );
};

const CaptionTrack: React.FC = () => {
  const { fps } = useVideoConfig();
  return <>{data.captions.map((c, i) => { const a = Math.round(c.start * fps), b = Math.max(a + 2, Math.round(c.end * fps)); return <Sequence key={i} from={a} durationInFrames={b - a}><Caption text={c.text} /></Sequence>; })}</>;
};

// Composição 1 — montagem: planos do Blender + dissolves + áudio (a grade de cor e as legendas entram depois, no FFmpeg, para as legendas ficarem nítidas)
export const Montage: React.FC = () => {
  const { fps } = useVideoConfig(); const total = Math.round(data.duration * fps);
  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      {data.shots.map((s, i) => <Sequence key={s.id} from={s.n0} durationInFrames={Math.max(1, total - s.n0)}><Shot id={s.id} have={s.frames} n0={s.n0} fade={i > 0} /></Sequence>)}
      <Audio src={staticFile('final_mix.wav')} />
    </AbsoluteFill>
  );
};
// Composição 2 — só as legendas, fundo transparente (render como sequência PNG com alfa)
export const Captions: React.FC = () => <AbsoluteFill><CaptionTrack /></AbsoluteFill>;
