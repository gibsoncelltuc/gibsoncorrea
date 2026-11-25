// Minimapa: o terreno é desenhado uma vez (1 pixel = 2 unidades) e depois só se recorta ao redor do jogador.
import { WORLD_HALF, SEA_LEVEL, LOCATIONS, LAKES, heightAt, biomeWeights, roadDist, smooth } from './shared/world.js';

const RES = 2;
const SIDE = Math.ceil((WORLD_HALF * 2) / RES);

function renderTerrain() {
  const c = document.createElement('canvas');
  c.width = c.height = SIDE;
  const g = c.getContext('2d');
  const img = g.createImageData(SIDE, SIDE);
  const col = (h) => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
  const base = col('#6fc45a');
  const mix = (a, b, t) => a.map((v, i) => v + (b[i] - v) * t);
  const pal = { forest: col('#3b8f47'), farm: col('#b5d860'), desert: col('#e9cf8e'), snow: col('#f2f7ff'), beach: col('#f2e1a6'), castle: col('#8c9a78'), ruins: col('#8fa17a'), town: col('#b9b09a') };
  for (let j = 0; j < SIDE; j++) {
    for (let i = 0; i < SIDE; i++) {
      const x = i * RES - WORLD_HALF;
      const z = j * RES - WORLD_HALF;
      const h = heightAt(x, z);
      let c3;
      if (h < SEA_LEVEL) c3 = mix(col('#3aa0d8'), col('#1f6fa8'), smooth(-1, -6, h));
      else {
        const w = biomeWeights(x, z);
        c3 = base.slice();
        for (const [k, p] of Object.entries(pal)) c3 = mix(c3, p, Math.min(1, w[k] * 0.9));
        c3 = mix(c3, col('#8e96a3'), smooth(11, 20, h) * 0.8);
        c3 = mix(c3, col('#f4f9ff'), smooth(24, 34, h));
        if (roadDist(x, z) < 3) c3 = mix(c3, col('#cdb07a'), 0.9);
      }
      const k = (j * SIDE + i) * 4;
      img.data[k] = c3[0];
      img.data[k + 1] = c3[1];
      img.data[k + 2] = c3[2];
      img.data[k + 3] = 255;
    }
  }
  g.putImageData(img, 0, 0);
  for (const l of LAKES) {
    g.fillStyle = l.ice ? '#d4ecff' : '#3aa0d8';
    g.beginPath();
    g.arc((l.x + WORLD_HALF) / RES, (l.z + WORLD_HALF) / RES, l.r / RES, 0, Math.PI * 2);
    g.fill();
  }
  return c;
}

export class Minimap {
  constructor(canvas, terrain) {
    this.canvas = canvas;
    this.g = canvas.getContext('2d');
    this.terrain = terrain ?? renderTerrain();
    this.span = 130; // unidades visíveis em cada direção
    this.big = false;
  }
  setBig(v) {
    this.big = v;
  }
  draw({ x, z, yaw }, others, target, npcs) {
    const { g, canvas } = this;
    const S = canvas.width;
    const span = this.big ? WORLD_HALF + 10 : this.span;
    const k = S / (span * 2);
    g.clearRect(0, 0, S, S);
    g.save();
    g.beginPath();
    g.arc(S / 2, S / 2, S / 2 - 2, 0, Math.PI * 2);
    g.clip();
    g.fillStyle = '#1f6fa8';
    g.fillRect(0, 0, S, S);
    const cx = this.big ? 0 : x;
    const cz = this.big ? 0 : z;
    const sx = (cx - span + WORLD_HALF) / RES;
    const sz = (cz - span + WORLD_HALF) / RES;
    g.imageSmoothingEnabled = true;
    g.drawImage(this.terrain, sx, sz, (span * 2) / RES, (span * 2) / RES, 0, 0, S, S);
    const P = (wx, wz) => [(wx - cx + span) * k, (wz - cz + span) * k];
    g.font = `${this.big ? 11 : 9}px system-ui`;
    g.textAlign = 'center';
    for (const [key, l] of Object.entries(LOCATIONS)) {
      if (['mayor', 'pyramid'].includes(key)) continue;
      const [px, pz] = P(l.x, l.z);
      if (px < 0 || pz < 0 || px > S || pz > S) continue;
      g.fillStyle = 'rgba(10,10,20,0.75)';
      g.fillRect(px - g.measureText(l.name).width / 2 - 2, pz - 8, g.measureText(l.name).width + 4, 12);
      g.fillStyle = '#fff';
      g.fillText(l.name, px, pz + 1);
    }
    for (const n of npcs ?? []) {
      const [px, pz] = P(n.x, n.z);
      g.fillStyle = '#ffd24a';
      g.beginPath();
      g.arc(px, pz, 2.6, 0, Math.PI * 2);
      g.fill();
    }
    for (const o of others) {
      const [px, pz] = P(o.x, o.z);
      g.fillStyle = '#46e0ff';
      g.beginPath();
      g.arc(px, pz, 3.4, 0, Math.PI * 2);
      g.fill();
    }
    if (target) {
      const [px, pz] = P(target.x, target.z);
      const q = Math.max(8, Math.min(S - 8, px));
      const r = Math.max(8, Math.min(S - 8, pz));
      g.fillStyle = '#ff4d6d';
      g.strokeStyle = '#fff';
      g.lineWidth = 2;
      g.beginPath();
      for (let i = 0; i < 10; i++) {
        const a = (i / 10) * Math.PI * 2 - Math.PI / 2;
        const rr = i % 2 ? 4 : 8;
        g.lineTo(q + Math.cos(a) * rr, r + Math.sin(a) * rr);
      }
      g.closePath();
      g.fill();
      g.stroke();
    }
    const [mx, mz] = P(x, z);
    g.translate(mx, mz);
    g.rotate(-yaw + Math.PI);
    g.fillStyle = '#ffffff';
    g.strokeStyle = '#1b1426';
    g.lineWidth = 2;
    g.beginPath();
    g.moveTo(0, -7);
    g.lineTo(5, 6);
    g.lineTo(0, 3);
    g.lineTo(-5, 6);
    g.closePath();
    g.fill();
    g.stroke();
    g.restore();
    g.strokeStyle = 'rgba(255,255,255,0.8)';
    g.lineWidth = 3;
    g.beginPath();
    g.arc(S / 2, S / 2, S / 2 - 2, 0, Math.PI * 2);
    g.stroke();
  }
}
