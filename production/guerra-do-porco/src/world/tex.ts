// Texturas procedurais (Canvas 2D, seed fixo) — dão o "detalhe pintado" dos cenários sem assets de terceiros.
import * as THREE from 'three';
import { rng } from '../lib/anim';

const cache = new Map<string, THREE.CanvasTexture>();
export const mk = (key: string, w: number, h: number, draw: (g: CanvasRenderingContext2D, r: () => number, w: number, h: number) => void,
  o: { repeat?: [number, number]; seed?: number; srgb?: boolean; wrap?: boolean } = {}): THREE.CanvasTexture => {
  const hit = cache.get(key); if (hit) return hit;
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  const g = c.getContext('2d')!; draw(g, rng(o.seed ?? 7), w, h);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
  if (o.wrap !== false) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(...(o.repeat ?? [1, 1])); }
  cache.set(key, t); return t;
};

export const grassTex = (a = '#c9a64a', b = '#8f8a3a', c = '#e6c460', rep: [number, number] = [20, 20]) => mk(`grass${a}${b}${c}`, 512, 512, (g, r, w, h) => {
  const grd = g.createLinearGradient(0, 0, w, h); grd.addColorStop(0, a); grd.addColorStop(1, b); g.fillStyle = grd; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 2600; i++) { const x = r() * w, y = r() * h, l = 5 + r() * 14; g.strokeStyle = r() < .5 ? c : (r() < .5 ? b : '#6f7a38'); g.globalAlpha = .35 + r() * .4; g.lineWidth = 1.2 + r() * 1.6;
    g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + (r() - .5) * 6, y - l * .5, x + (r() - .5) * 10, y - l); g.stroke(); }
  g.globalAlpha = 1;
}, { repeat: rep });
export const soilTex = () => mk('soil', 256, 256, (g, r, w, h) => {
  g.fillStyle = '#8c5e40'; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 1800; i++) { g.fillStyle = r() < .5 ? '#a47450' : '#6a432e'; g.globalAlpha = .5; g.beginPath(); g.arc(r() * w, r() * h, 1 + r() * 3, 0, 7); g.fill(); }
  g.globalAlpha = 1; for (let i = 0; i < 4; i++) { g.fillStyle = 'rgba(40,24,20,.35)'; g.fillRect(0, i * 64 + 26, w, 8); }
}, { repeat: [3, 1] });
export const planksTex = (base = '#b98a55', dark = '#6a4630', rep: [number, number] = [4, 4]) => mk(`planks${base}${dark}`, 512, 512, (g, r, w, h) => {
  const n = 8, ph = h / n;
  for (let i = 0; i < n; i++) {
    const shade = (r() - .5) * 28; g.fillStyle = base; g.fillRect(0, i * ph, w, ph);
    g.fillStyle = `rgba(${shade > 0 ? 255 : 0},${shade > 0 ? 220 : 0},${shade > 0 ? 170 : 0},${Math.abs(shade) / 120})`; g.fillRect(0, i * ph, w, ph);
    for (let k = 0; k < 26; k++) { g.strokeStyle = 'rgba(80,50,30,.22)'; g.lineWidth = 1; const y = i * ph + 3 + r() * (ph - 6); g.beginPath(); g.moveTo(r() * w * .3, y); g.lineTo(w * (.5 + r() * .5), y + (r() - .5) * 2); g.stroke(); }
    g.fillStyle = dark; g.fillRect(0, i * ph, w, 3);
    const sx = r() * w; g.fillRect(sx, i * ph, 3, ph);
    if (r() < .6) { g.strokeStyle = 'rgba(70,40,25,.5)'; g.lineWidth = 2; g.beginPath(); g.ellipse(r() * w, i * ph + ph / 2, 7, 4, 0, 0, 7); g.stroke(); }
  }
}, { repeat: rep });
export const logsTex = () => mk('logs', 256, 256, (g, r, w, h) => {
  const n = 6, ph = h / n;
  for (let i = 0; i < n; i++) { const grd = g.createLinearGradient(0, i * ph, 0, (i + 1) * ph); grd.addColorStop(0, '#a8744a'); grd.addColorStop(.5, '#c48b58'); grd.addColorStop(1, '#7b4f33'); g.fillStyle = grd; g.fillRect(0, i * ph, w, ph);
    g.fillStyle = '#4a2e22'; g.fillRect(0, (i + 1) * ph - 3, w, 3); for (let k = 0; k < 14; k++) { g.strokeStyle = 'rgba(70,40,25,.25)'; g.beginPath(); const y = i * ph + 4 + r() * (ph - 8); g.moveTo(r() * w, y); g.lineTo(r() * w, y); g.stroke(); } }
}, { repeat: [2, 1] });
export const shingleTex = (c1 = '#7a4a3a', c2 = '#a86a4a') => mk(`shingle${c1}`, 256, 256, (g, r, w, h) => {
  const n = 8, ph = h / n; for (let i = 0; i < n; i++) for (let k = -1; k < 8; k++) { g.fillStyle = r() < .5 ? c1 : c2; const x = k * 34 + (i % 2) * 17; g.fillRect(x, i * ph, 32, ph - 1); g.strokeStyle = 'rgba(40,20,20,.45)'; g.strokeRect(x, i * ph, 32, ph - 1); }
}, { repeat: [3, 2] });
export const sandTex = () => mk('sand', 256, 256, (g, r, w, h) => { g.fillStyle = '#e8cf95'; g.fillRect(0, 0, w, h); for (let i = 0; i < 1600; i++) { g.fillStyle = r() < .5 ? '#d1b57a' : '#f4e3b2'; g.fillRect(r() * w, r() * h, 2, 2); } }, { repeat: [10, 4] });
export const waterTex = (deep = '#1f7fc0', mid = '#3aa6dc', hi = '#bfe8ff') => mk(`water${deep}${mid}`, 512, 512, (g, r, w, h) => {
  const grd = g.createLinearGradient(0, 0, 0, h); grd.addColorStop(0, mid); grd.addColorStop(1, deep); g.fillStyle = grd; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 160; i++) { const x = r() * w, y = r() * h, l = 24 + r() * 70; g.strokeStyle = hi; g.globalAlpha = .12 + r() * .25; g.lineWidth = 2 + r() * 2;
    g.beginPath(); g.moveTo(x, y); g.bezierCurveTo(x + l * .3, y - 5, x + l * .7, y + 5, x + l, y); g.stroke(); } g.globalAlpha = 1;
}, { repeat: [18, 18] });
export const sailTex = () => mk('sail', 256, 256, (g, r, w, h) => {
  g.fillStyle = '#f4ead0'; g.fillRect(0, 0, w, h);
  for (let i = 1; i < 6; i++) { g.fillStyle = 'rgba(120,100,70,.3)'; g.fillRect(0, i * (h / 6), w, 2); }
  g.fillStyle = 'rgba(150,120,80,.18)'; g.fillRect(0, h * .75, w, h * .25);
  for (let i = 0; i < 220; i++) { g.fillStyle = 'rgba(160,130,90,.10)'; g.fillRect(r() * w, r() * h, 12, 2); }
});
export const hullTex = () => mk('hull', 512, 128, (g, r, w, h) => {
  g.fillStyle = '#1e1b2e'; g.fillRect(0, 0, w, h);
  g.fillStyle = '#e9b848'; g.fillRect(0, h * .30, w, h * .09); g.fillRect(0, h * .62, w, h * .09);
  for (let i = 0; i < 12; i++) { g.fillStyle = '#e9b848'; g.fillRect(i * (w / 12) + 12, h * .39, 26, h * .23); g.fillStyle = '#17141f'; g.fillRect(i * (w / 12) + 16, h * .43, 18, h * .15); }
  for (let i = 0; i < 400; i++) { g.fillStyle = 'rgba(255,255,255,.04)'; g.fillRect(r() * w, r() * h, 8, 1); }
}, { wrap: false });
export const flagUS = () => mk('flagUS', 256, 160, (g, r, w, h) => {
  const sh = h / 13; for (let i = 0; i < 13; i++) { g.fillStyle = i % 2 ? '#fbf6ee' : '#c8372f'; g.fillRect(0, i * sh, w, sh + 1); }
  g.fillStyle = '#26356b'; g.fillRect(0, 0, w * .42, sh * 7);
  g.fillStyle = '#fbf6ee'; for (let y = 0; y < 5; y++) for (let x = 0; x < 6; x++) { g.beginPath(); g.arc(w * .42 * (x + .6) / 6.2 + (y % 2) * 6, sh * 7 * (y + .6) / 5.2, 3.4, 0, 7); g.fill(); }
}, { wrap: false });
export const flagUK = () => mk('flagUK', 256, 160, (g, r, w, h) => {
  g.fillStyle = '#1d2f6f'; g.fillRect(0, 0, w, h);
  g.strokeStyle = '#fbf6ee'; g.lineWidth = 30; g.beginPath(); g.moveTo(0, 0); g.lineTo(w, h); g.moveTo(w, 0); g.lineTo(0, h); g.stroke();
  g.strokeStyle = '#c8372f'; g.lineWidth = 10; g.beginPath(); g.moveTo(0, 0); g.lineTo(w, h); g.moveTo(w, 0); g.lineTo(0, h); g.stroke();
  g.fillStyle = '#fbf6ee'; g.fillRect(w / 2 - 25, 0, 50, h); g.fillRect(0, h / 2 - 25, w, 50);
  g.fillStyle = '#c8372f'; g.fillRect(w / 2 - 15, 0, 30, h); g.fillRect(0, h / 2 - 15, w, 30);
}, { wrap: false });
export const noteTex = (label: string, tint = '#cfe3b4') => mk(`note${label}${tint}`, 256, 128, (g, r, w, h) => {
  g.fillStyle = tint; g.fillRect(0, 0, w, h); g.strokeStyle = '#3a5a3a'; g.lineWidth = 5; g.strokeRect(7, 7, w - 14, h - 14); g.lineWidth = 2; g.strokeRect(16, 16, w - 32, h - 32);
  g.fillStyle = '#2f4a30'; g.font = 'bold 66px "Liberation Sans", Arial, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(label, w / 2, h / 2 + 4);
  g.beginPath(); g.arc(30, 30, 8, 0, 7); g.arc(w - 30, h - 30, 8, 0, 7); g.stroke();
}, { wrap: false });
export const signTex = (text: string) => mk(`sign${text}`, 256, 128, (g, r, w, h) => {
  g.fillStyle = '#9a6a42'; g.fillRect(0, 0, w, h); for (let i = 0; i < 80; i++) { g.fillStyle = 'rgba(60,35,20,.2)'; g.fillRect(0, r() * h, w, 2); }
  g.strokeStyle = '#4a2e22'; g.lineWidth = 6; g.strokeRect(4, 4, w - 8, h - 8);
  g.fillStyle = '#f1e2bd'; const ls = text.split('\n'); g.font = `bold ${ls.length > 1 ? 40 : 46}px "Liberation Sans", Arial, sans-serif`; g.textAlign = 'center'; g.textBaseline = 'middle';
  ls.forEach((l, i) => g.fillText(l, w / 2, h / 2 + 3 + (i - (ls.length - 1) / 2) * 46));
}, { wrap: false });
export const cloudTex = () => mk('cloud', 256, 128, (g, r, w, h) => {
  for (let i = 0; i < 9; i++) { const x = w * (.2 + .6 * r()), y = h * (.45 + .2 * r()), rad = 24 + r() * 26; const grd = g.createRadialGradient(x, y, 2, x, y, rad); grd.addColorStop(0, 'rgba(255,255,255,.95)'); grd.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = grd; g.beginPath(); g.arc(x, y, rad, 0, 7); g.fill(); }
}, { wrap: false });
export const rayTex = () => mk('ray', 64, 256, (g, r, w, h) => { const grd = g.createLinearGradient(0, 0, 0, h); grd.addColorStop(0, 'rgba(255,230,170,.0)'); grd.addColorStop(.25, 'rgba(255,230,170,.55)'); grd.addColorStop(1, 'rgba(255,230,170,0)'); g.fillStyle = grd; g.fillRect(0, 0, w, h);
  const side = g.createLinearGradient(0, 0, w, 0); side.addColorStop(0, 'rgba(0,0,0,1)'); side.addColorStop(.5, 'rgba(0,0,0,0)'); side.addColorStop(1, 'rgba(0,0,0,1)'); g.globalCompositeOperation = 'destination-out'; g.fillStyle = side; g.fillRect(0, 0, w, h); }, { wrap: false });
export const dotTex = () => mk('dot', 64, 64, (g, r, w, h) => { const grd = g.createRadialGradient(32, 32, 1, 32, 32, 31); grd.addColorStop(0, 'rgba(255,255,255,1)'); grd.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = grd; g.fillRect(0, 0, w, h); }, { wrap: false });
// padrões de tecido para roupas (mapeamento planar no torso)
export const fabricTex = (kind: 'plaid' | 'stripes' | 'tweed' | 'denim' | 'uniform' | 'plain', c1: string, c2: string) => mk(`fab${kind}${c1}${c2}`, 128, 128, (g, r, w, h) => {
  g.fillStyle = c1; g.fillRect(0, 0, w, h);
  if (kind === 'plaid') { g.fillStyle = c2; g.globalAlpha = .55; for (let i = 0; i < 4; i++) { g.fillRect(i * 32 + 12, 0, 8, h); g.fillRect(0, i * 32 + 12, w, 8); } g.globalAlpha = 1; g.strokeStyle = 'rgba(40,20,40,.5)'; g.lineWidth = 2; for (let i = 0; i < 4; i++) { g.beginPath(); g.moveTo(i * 32 + 4, 0); g.lineTo(i * 32 + 4, h); g.moveTo(0, i * 32 + 4); g.lineTo(w, i * 32 + 4); g.stroke(); } }
  if (kind === 'stripes') { g.fillStyle = c2; for (let i = 0; i < 8; i++) g.fillRect(i * 16, 0, 7, h); }
  if (kind === 'tweed') { for (let i = 0; i < 700; i++) { g.fillStyle = r() < .5 ? c2 : 'rgba(0,0,0,.22)'; g.fillRect(r() * w, r() * h, 2, 2); } }
  if (kind === 'denim') { g.fillStyle = c2; g.globalAlpha = .5; for (let i = 0; i < 120; i++) g.fillRect(r() * w, r() * h, 6, 1); g.globalAlpha = 1; g.fillStyle = '#d8b06a'; g.fillRect(70, 70, 34, 30); g.strokeStyle = '#6a4a2a'; g.setLineDash([4, 3]); g.strokeRect(70, 70, 34, 30); }
  if (kind === 'uniform') { g.fillStyle = c2; g.globalAlpha = .25; g.fillRect(0, 0, w, 10); g.globalAlpha = 1; }
}, { repeat: [1, 1] });
