import timings from '../../script/word-timings.json';
export type Word = { line: string; text: string; start: number; end: number };
export type Line = { id: string; shot: string; beat: string; text: string; start: number; end: number };
export const T = timings as unknown as { total: number; lines: Line[]; words: Word[] };
export const lineStart = (id: string) => T.lines.find((l) => l.id === id)!.start;
export const lineEnd = (id: string) => T.lines.find((l) => l.id === id)!.end;
/** Shots: início = 1ª fala do shot (menos 0.25s), fim = início do próximo. */
const order = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7'];
export const SHOTS = order.map((id, i) => {
  const first = T.lines.find((l) => l.shot === id)!;
  const nxt = T.lines.find((l) => l.shot === order[i + 1]);
  return { id, start: i === 0 ? 0 : first.start - 0.3, end: nxt ? nxt.start - 0.3 : T.total };
});
export const shotAt = (t: number) => SHOTS.find((s) => t >= s.start && t < s.end) ?? SHOTS[SHOTS.length - 1];
/** Amplitude de boca (0..1) a partir de intervalos reais de palavras. */
export const mouthOpen = (t: number, lineIds?: string[]): number => {
  for (const w of T.words) {
    if (lineIds && !lineIds.includes(w.line)) continue;
    if (t >= w.start - 0.02 && t <= w.end + 0.03) {
      const ph = (t - w.start) * 11;
      return 0.35 + 0.65 * Math.abs(Math.sin(ph * 1.7 + w.text.length));
    }
  }
  return 0;
};
/** Início da primeira palavra da linha cujo texto (sem pontuação) começa com `prefix`. */
const norm = (s: string) => s.toLowerCase().replace(/[.,!?:;—-]/g, '');
export const wordStart = (line: string, prefix: string, nth = 0): number => {
  const ws = T.words.filter((w) => w.line === line && norm(w.text).startsWith(norm(prefix)));
  if (!ws[nth]) throw new Error(`palavra ${prefix} não encontrada em ${line}`);
  return ws[nth].start;
};
export const wordEnd = (line: string, prefix: string, nth = 0): number => {
  const ws = T.words.filter((w) => w.line === line && norm(w.text).startsWith(norm(prefix)));
  return ws[nth].end;
};
/** Amplitude de boca só para palavras a partir de `fromWord` na linha (fala dentro de aspas). */
export const quoteOpen = (t: number, line: string, fromWord: string): number => {
  const t0 = wordStart(line, fromWord);
  return t >= t0 - 0.02 ? mouthOpen(t, [line]) : 0;
};
