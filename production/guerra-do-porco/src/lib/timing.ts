import timings from '../../script/word-timings.json';
export type Word = { line: string; text: string; start: number; end: number };
export type Line = { id: string; shot: string; beat: string; text: string; start: number; end: number };
export const T = timings as unknown as { total: number; lines: Line[]; words: Word[] };
const norm = (s: string) => s.toLowerCase().replace(/[.,!?:;—-]/g, '');
export const wordStart = (line: string, prefix: string, nth = 0): number => {
  const ws = T.words.filter((w) => w.line === line && norm(w.text).startsWith(norm(prefix)));
  if (!ws[nth]) throw new Error(`palavra ${prefix} não encontrada em ${line}`); return ws[nth].start;
};
export const wordEnd = (line: string, prefix: string, nth = 0): number => {
  const ws = T.words.filter((w) => w.line === line && norm(w.text).startsWith(norm(prefix))); return ws[nth].end;
};
export const lineStart = (id: string) => T.lines.find((l) => l.id === id)!.start;
export const lineEnd = (id: string) => T.lines.find((l) => l.id === id)!.end;

/** Eventos sonoros/visuais ancorados nas palavras reais da narração. */
export const BANG1 = wordStart('L1', 'matou') + 0.1;     // tiro do gancho
export const BANG2 = wordStart('L2', 'atirou') + 0.05;   // tiro do setup
export const BANGS = [BANG1, BANG2];

/** Planos: início = 1ª fala do plano − 0.3 s (exceto S1/S6, ancorados). Dissolve de DIS s centrado no início. */
export const DIS = 0.4;
const starts: [string, number][] = [
  ['S1', 0], ['S2', lineStart('L2') - 0.3], ['S3', lineStart('L3') - 0.3], ['S4', lineStart('L4') - 0.3],
  ['S5', lineStart('L5') - 0.3], ['S6', wordStart('L5', 'ninguém') - 0.3],
];
export const SHOTS = starts.map(([id, start], i) => ({ id, start, end: i + 1 < starts.length ? starts[i + 1][1] : T.total }));
export const shot = (id: string) => SHOTS.find((s) => s.id === id)!;
