// Construções de cada região do mundo aberto (vila, coliseu, fazenda, floresta, deserto, neve, praia, castelo, ruínas).
import * as THREE from 'three';
import { Merge, vcMat, TAU } from './buildutil.js';
import { nameTag } from './avatar.js';
import { LOCATIONS, ROADS, ARENA_RADIUS, heightAt, roadDist } from './shared/world.js';

// Construtor em coordenadas locais (centro + rotação), para montar casas, celeiros, etc. virados para qualquer lado
class Local {
  constructor(m, cx, cy, cz, ry = 0) {
    Object.assign(this, { m, cx, cy, cz, ry });
  }
  p(lx, ly, lz) {
    const c = Math.cos(this.ry);
    const s = Math.sin(this.ry);
    return { x: this.cx + lx * c + lz * s, y: this.cy + ly, z: this.cz - lx * s + lz * c };
  }
  box(w, h, d, color, lx, ly, lz) {
    this.m.box(w, h, d, color, { ...this.p(lx, ly, lz), ry: this.ry });
    return this;
  }
  cyl(rt, rb, h, color, lx, ly, lz, seg = 10) {
    this.m.cyl(rt, rb, h, color, this.p(lx, ly, lz), seg);
    return this;
  }
  cone(r, h, color, lx, ly, lz, seg = 8) {
    this.m.cone(r, h, color, this.p(lx, ly, lz), seg);
    return this;
  }
  ball(r, color, lx, ly, lz, seg = 10, o = {}) {
    this.m.ball(r, color, { ...this.p(lx, ly, lz), ...o }, seg);
    return this;
  }
  roof(w, d, h, color, ly) {
    const g = new THREE.ConeGeometry(w / Math.SQRT2, h, 4);
    g.rotateY(Math.PI / 4);
    g.scale(1, 1, d / w);
    this.m.add(g, color, { ...this.p(0, ly + h / 2, 0), ry: this.ry });
    return this;
  }
  // telhado de duas águas (prisma)
  gable(w, d, h, color, ly) {
    const s = new THREE.Shape();
    s.moveTo(-d / 2 - 0.5, 0);
    s.lineTo(0, h);
    s.lineTo(d / 2 + 0.5, 0);
    s.closePath();
    const g = new THREE.ExtrudeGeometry(s, { depth: w + 1, bevelEnabled: false });
    g.translate(0, 0, -(w + 1) / 2);
    g.rotateY(Math.PI / 2);
    this.m.add(g, color, { ...this.p(0, ly, 0), ry: this.ry });
    return this;
  }
}

const ringGeo = (ro, ri, h, seg = 48) => {
  const s = new THREE.Shape();
  s.absarc(0, 0, ro, 0, TAU, false);
  const hole = new THREE.Path();
  hole.absarc(0, 0, ri, 0, TAU, true);
  s.holes.push(hole);
  const g = new THREE.ExtrudeGeometry(s, { depth: h, bevelEnabled: false, curveSegments: seg });
  g.rotateX(-Math.PI / 2);
  return g;
};

export function buildStructures(ctx) {
  const { root, col, api, upd } = ctx;
  const M = new Merge(); // paredes, telhados, madeira, pedra
  const G = new Merge(); // janelas (acendem à noite)
  const B = new Merge(); // lâmpadas/fogo emissivos
  const flames = [];
  const keep = (x, z, r) => (ctx.keepout ??= []).push({ x, z, r });
  const hy = (x, z) => heightAt(x, z);
  const baseY = (x, z, w, d) => Math.max(hy(x, z), hy(x + w / 2, z + d / 2), hy(x - w / 2, z - d / 2), hy(x + w / 2, z - d / 2), hy(x - w / 2, z + d / 2));
  const found = (x, z, w, d, ry, color = '#8d939e') => {
    const y = baseY(x, z, w, d);
    M.box(w + 0.8, 6, d + 0.8, color, { x, y: y - 2.9, z, ry });
    return y;
  };
  const rectCol = (cx, cz, w, d, ry, pad = 0.3) => {
    const long = Math.max(w, d);
    const sh = Math.min(w, d);
    const n = Math.max(1, Math.ceil(long / (sh * 0.8)));
    for (let i = 0; i < n; i++) {
      const t = n === 1 ? 0 : -long / 2 + sh / 2 + (i * (long - sh)) / (n - 1);
      const lx = w >= d ? t : 0;
      const lz = w >= d ? 0 : t;
      col.add(cx + lx * Math.cos(ry) + lz * Math.sin(ry), cz - lx * Math.sin(ry) + lz * Math.cos(ry), sh / 2 + pad);
    }
  };
  const flame = (x, y, z, s = 1, light = false, color = '#ff9a3a') => {
    const f = new THREE.Mesh(new THREE.ConeGeometry(0.4 * s, 1.1 * s, 7), new THREE.MeshBasicMaterial({ color: '#ffb347' }));
    f.position.set(x, y + 0.55 * s, z);
    const f2 = new THREE.Mesh(new THREE.ConeGeometry(0.22 * s, 0.7 * s, 7), new THREE.MeshBasicMaterial({ color: '#fff0a0' }));
    f2.position.set(x, y + 0.4 * s, z);
    root.add(f, f2);
    let l = null;
    if (light) {
      l = new THREE.PointLight(color, 70, 24, 2);
      l.position.set(x, y + 1.4 * s, z);
      root.add(l);
    }
    flames.push({ f, f2, l, ph: Math.random() * 6 });
  };
  const lamp = (x, z) => {
    const y = hy(x, z);
    M.cyl(0.12, 0.16, 4.2, '#3b3b46', { x, y: y + 2.1, z }, 6);
    M.box(0.7, 0.12, 0.7, '#3b3b46', { x, y: y + 4.3, z });
    B.ball(0.32, '#ffd890', { x, y: y + 4.6, z }, 8);
    col.add(x, z, 0.3);
  };
  const house = (x, z, w, d, h, wall, roof, ry, big = false) => {
    const y = found(x, z, w, d, ry, '#9a9488');
    const L = new Local(M, x, y, z, ry);
    L.box(w, h, d, wall, 0, h / 2, 0);
    L.box(w + 0.3, 0.5, d + 0.3, '#8d8478', 0, 0.25, 0);
    L.gable(w, d, h * 0.62, roof, h);
    L.box(1.5, 2.6, 0.18, '#6b432c', 0, 1.3, d / 2 + 0.04);
    L.box(2.4, 0.2, 1.4, '#a49c8a', 0, 0.1, d / 2 + 0.8);
    const W = new Local(G, x, y, z, ry);
    for (const sx of [-1, 1]) {
      W.box(1.3, 1.4, 0.14, '#ffe9a8', sx * (w / 2 - 1.8), h * 0.62, d / 2 + 0.05);
      L.box(1.6, 0.18, 0.2, '#6b432c', sx * (w / 2 - 1.8), h * 0.62 + 0.8, d / 2 + 0.06);
      L.box(1.6, 0.18, 0.2, '#6b432c', sx * (w / 2 - 1.8), h * 0.62 - 0.8, d / 2 + 0.06);
      W.box(1.3, 1.4, 0.14, '#ffe9a8', sx * (w / 2 - 1.8), h * 0.62, -d / 2 - 0.05);
    }
    if (big) for (const sx of [-1, 1]) W.box(0.14, 1.4, 1.3, '#ffe9a8', sx * (w / 2 + 0.05), h * 0.62, 0);
    L.box(0.9, 2.8, 0.9, '#8a5a4a', w / 4, h + 1.6, -d / 5);
    rectCol(x, z, w, d, ry);
    keep(x, z, Math.max(w, d) / 2 + 3);
    return { x, y, z };
  };

  // =================== VILA MOEDA ===================
  const T = LOCATIONS.town;
  {
    // praça e fonte
    M.cyl(15, 15.6, 0.3, '#bdb5a3', { x: 0, y: 0.15, z: 0 }, 40);
    M.cyl(11, 11, 0.34, '#a89f8c', { x: 0, y: 0.17, z: 0 }, 40);
    M.cyl(4.6, 4.8, 1.0, '#9ca3ad', { x: 0, y: 0.7, z: 0 }, 24);
    M.cyl(3.9, 3.9, 0.3, '#7ccdf5', { x: 0, y: 1.1, z: 0 }, 24);
    M.cyl(0.8, 1.0, 3.2, '#9ca3ad', { x: 0, y: 2.4, z: 0 }, 10);
    M.cyl(2.0, 0.6, 0.6, '#9ca3ad', { x: 0, y: 3.8, z: 0 }, 14);
    M.ball(0.7, '#7ccdf5', { x: 0, y: 4.4, z: 0 }, 10);
    col.add(0, 0, 5.2);
    keep(0, 0, 17);
    const wells = [[-14, 15], [16, -22]];
    for (const [wx, wz] of wells) {
      M.cyl(1.7, 1.8, 1.4, '#9a9488', { x: wx, y: 0.7, z: wz }, 12);
      M.cyl(1.1, 1.1, 0.1, '#2a4a6a', { x: wx, y: 1.35, z: wz }, 12);
      for (const sx of [-1, 1]) M.box(0.2, 3, 0.2, '#6b432c', { x: wx + sx * 1.6, y: 2.5, z: wz });
      M.box(4.2, 0.2, 1.4, '#8a5a3a', { x: wx, y: 4.1, z: wz });
      M.cone(2.6, 1.4, '#c0503f', { x: wx, y: 4.8, z: wz }, 4);
      col.add(wx, wz, 2.2);
      keep(wx, wz, 4);
    }
    // casas em dois anéis, desviando das estradas
    const walls = ['#f3e6c8', '#cfe6f5', '#f5c7b8', '#d4efd0', '#f6e08a', '#e8d0f0'];
    const roofs = ['#c0503f', '#6b7fa8', '#8a5a3a', '#3f7f5a', '#b0603f'];
    let n = 0;
    for (const [ring, count, off] of [[34, 11, 0.2], [50, 15, 0.1], [63, 19, 0.35]]) {
      for (let k = 0; k < count; k++) {
        const a = (k / count) * TAU + off;
        const x = Math.cos(a) * ring;
        const z = Math.sin(a) * ring;
        if (roadDist(x, z) < 11 || Math.hypot(x - 7, z + 24) < 18 || Math.hypot(x + 26, z + 14) < 12 || Math.hypot(x + 14, z - 15) < 6 || Math.hypot(x + 42, z - 32) < 17 || Math.hypot(x - LOCATIONS.colosseum.x, z - LOCATIONS.colosseum.z) < 40) continue;
        const w = 6.5 + ((n * 7) % 5);
        const d = 6 + ((n * 3) % 4);
        house(x, z, w, d, 4.2 + (n % 3) * 0.6, walls[n % 6], roofs[(n * 2) % 5], Math.atan2(-x, -z), n % 4 === 0);
        n++;
      }
    }
    // Prefeitura com torre do relógio
    {
      const x = 7;
      const z = -27;
      const y = found(x, z, 16, 11, 0);
      const L = new Local(M, x, y, z, 0);
      L.box(16, 8, 11, '#e9dcc0', 0, 4, 0);
      L.box(16.6, 0.8, 11.6, '#8d8478', 0, 0.4, 0);
      L.gable(16, 11, 4.6, '#6b7fa8', 8);
      L.box(5, 16, 5, '#e9dcc0', 0, 8, -1);
      L.cone(4.2, 5, '#6b7fa8', 0, 18.5, -1, 4);
      L.box(2.4, 3.6, 0.2, '#6b432c', 0, 1.8, 5.55);
      L.box(5, 0.3, 2.4, '#a49c8a', 0, 0.15, 6.6);
      for (const sx of [-1, 1]) {
        L.cyl(0.35, 0.35, 5, '#e9dcc0', sx * 2.6, 2.5, 6.4, 8);
        L.cyl(0.07, 0.07, 3.6, '#555', sx * 7.4, 9.8, 5.6, 5);
        L.box(1.8, 1.0, 0.05, sx > 0 ? '#d8404f' : '#2f8fd8', sx * 8.3, 10.8, 5.6);
      }
      const W = new Local(G, x, y, z, 0);
      for (const sx of [-5, -2.8, 2.8, 5]) W.box(1.3, 1.6, 0.14, '#ffe9a8', sx, 4.5, 5.55);
      const clock = new Local(M, x, y, z, 0);
      clock.cyl(1.5, 1.5, 0.2, '#fff6dc', 0, 12.5, 1.6, 20);
      M.box(0.12, 1.1, 0.1, '#2a2a30', { x, y: y + 12.8, z: z + 1.75 });
      M.box(0.9, 0.12, 0.1, '#2a2a30', { x: x + 0.4, y: y + 12.5, z: z + 1.75 });
      rectCol(x, z, 16, 11, 0);
      keep(x, z, 14);
    }
    // ferraria
    {
      const x = -30;
      const z = -16;
      const y = found(x, z, 10, 8, 0.3);
      const L = new Local(M, x, y, z, 0.3);
      L.box(10, 4.6, 8, '#9a8f84', 0, 2.3, 0);
      L.gable(10, 8, 2.8, '#5a4636', 4.6);
      L.box(2, 6, 2, '#777', 3.6, 3.5, -2);
      L.box(3, 1.4, 2, '#3a3a40', 0, 0.7, 5.6);
      L.box(1.4, 1, 0.9, '#2a2a30', -1.5, 0.5, 5.8);
      const f = new Local(B, x, y, z, 0.3);
      f.box(1.8, 0.6, 1.2, '#ff8a2a', 0, 1.7, 5.6);
      rectCol(x, z, 10, 8, 0.3);
      keep(x, z, 9);
    }
    // feira: barracas com toldos
    for (let i = 0; i < 5; i++) {
      const x = -54 + i * 6;
      const z = 30;
      const y = hy(x, z);
      const cA = ['#d8404f', '#2f8fd8', '#f0b429', '#3fae6a', '#a35cff'][i];
      for (const [sx, sz] of [[-1.8, -1.2], [1.8, -1.2], [-1.8, 1.2], [1.8, 1.2]]) M.cyl(0.1, 0.1, 3, '#6b432c', { x: x + sx, y: y + 1.5, z: z + sz }, 5);
      for (let k = 0; k < 4; k++) M.box(0.95, 0.12, 3.6, k % 2 ? '#fff6e6' : cA, { x: x - 1.5 + k, y: y + 3.1 - k * 0.0, z, rx: 0.22 });
      M.box(3.4, 1.0, 1.2, '#8a5a3a', { x, y: y + 0.5, z: z + 0.8 });
      for (let k = 0; k < 4; k++) M.ball(0.28, ['#d8404f', '#f0b429', '#7ccd5f', '#ff8a3d'][(i + k) % 4], { x: x - 1.1 + k * 0.7, y: y + 1.2, z: z + 0.8 }, 6);
      col.add(x, z + 0.4, 2.0);
      keep(x, z, 4);
    }
    for (const [x, z] of [[-58, 38], [-30, 38], [-44, 40]]) {
      M.cyl(0.7, 0.7, 1.2, '#8a5a3a', { x, y: hy(x, z) + 0.6, z }, 8);
      M.box(1.2, 1.2, 1.2, '#a8814f', { x: x + 1.4, y: hy(x, z) + 0.6, z });
      col.add(x, z, 1.0);
    }
    // postes ao longo das estradas dentro da vila e bancos
    for (const road of ROADS.slice(0, 6)) {
      for (let i = 0; i < road.length - 1; i++) {
        const [ax, az] = road[i];
        const [bx, bz] = road[i + 1];
        const len = Math.hypot(bx - ax, bz - az);
        for (let t = 0; t < len; t += 15) {
          const x = ax + ((bx - ax) * t) / len + ((bz - az) / len) * 3.4;
          const z = az + ((bz - az) * t) / len - ((bx - ax) / len) * 3.4;
          if (Math.hypot(x, z) < 70 && Math.hypot(x, z) > 17) lamp(x, z);
        }
      }
    }
    for (const a of [0.6, 2.2, 3.8, 5.4]) {
      const x = Math.cos(a) * 12.5;
      const z = Math.sin(a) * 12.5;
      M.box(2.2, 0.15, 0.7, '#8a5a3a', { x, y: 0.7, z, ry: -a });
      M.box(2.2, 0.7, 0.12, '#8a5a3a', { x: x + Math.cos(a) * 0.3, y: 1.1, z: z + Math.sin(a) * 0.3, ry: -a });
      lamp(Math.cos(a + 0.5) * 14.5, Math.sin(a + 0.5) * 14.5);
    }
  }

  // =================== COLISEU ===================
  {
    const C = LOCATIONS.colosseum;
    const gate = Math.atan2(0 - C.z, 0 - C.x); // abertura voltada para a vila
    const gap = 0.3;
    const inGap = (a) => Math.abs(Math.atan2(Math.sin(a - gate), Math.cos(a - gate))) < gap;
    const y0 = 0;
    M.cyl(ARENA_RADIUS + 1, ARENA_RADIUS + 1, 0.2, '#e6cf9a', { x: C.x, y: y0 + 0.1, z: C.z }, 48);
    M.cyl(8, 8, 0.24, '#d9b24a', { x: C.x, y: y0 + 0.12, z: C.z }, 32);
    M.cyl(7, 7, 0.28, '#e6cf9a', { x: C.x, y: y0 + 0.14, z: C.z }, 32);
    for (const [r, h, c] of [[27.6, 10, '#d8cdb4'], [25.4, 5.5, '#c9bfa6'], [23.3, 2.8, '#bdb299']]) {
      const n = 56;
      for (let i = 0; i < n; i++) {
        const a = (i / n) * TAU;
        if (inGap(a)) continue;
        const w = (TAU * r) / n + 0.25;
        M.box(w, h, 2.3, i % 2 && r < 26 ? '#b5aa90' : c, { x: C.x + Math.cos(a) * r, y: y0 + h / 2, z: C.z + Math.sin(a) * r, ry: -a + Math.PI / 2 });
        if (r > 27 && i % 2 === 0) M.box(w * 0.7, 1.2, 2.3, c, { x: C.x + Math.cos(a) * r, y: y0 + h + 0.6, z: C.z + Math.sin(a) * r, ry: -a + Math.PI / 2 });
      }
    }
    for (let i = 0; i < 28; i++) {
      const a = ((i + 0.5) / 28) * TAU;
      if (Math.abs(Math.atan2(Math.sin(a - gate), Math.cos(a - gate))) < gap + 0.1) continue;
      for (const [hy2, hh] of [[2.6, 4.2], [7.2, 3.2]]) {
        M.box(2.1, hh, 0.3, '#33291f', { x: C.x + Math.cos(a) * 28.0, y: y0 + hy2, z: C.z + Math.sin(a) * 28.0, ry: -a + Math.PI / 2 });
      }
      M.box(0.9, 10.4, 1.0, '#cfc4a8', { x: C.x + Math.cos(a + 0.116) * 28.7, y: y0 + 5.2, z: C.z + Math.sin(a + 0.116) * 28.7, ry: -a + Math.PI / 2 });
    }
    for (let i = 0; i < 40; i++) {
      const a = (i / 40) * TAU;
      if (!inGap(a)) col.add(C.x + Math.cos(a) * 24.6, C.z + Math.sin(a) * 24.6, 2.2);
      if (!inGap(a)) col.add(C.x + Math.cos(a) * 27.4, C.z + Math.sin(a) * 27.4, 2.4);
    }
    // portão com arco
    const gx = C.x + Math.cos(gate) * 27.6;
    const gz = C.z + Math.sin(gate) * 27.6;
    for (const s of [-1, 1]) {
      const px = gx + Math.cos(gate + Math.PI / 2) * s * 5.6;
      const pz = gz + Math.sin(gate + Math.PI / 2) * s * 5.6;
      M.cyl(1.3, 1.5, 12, '#e0d4b8', { x: px, y: 6, z: pz }, 10);
      M.ball(1.5, '#d9b24a', { x: px, y: 12.6, z: pz }, 8);
      col.add(px, pz, 1.8);
    }
    M.box(12.5, 2.6, 2.6, '#e0d4b8', { x: gx, y: 10.6, z: gz, ry: -gate + Math.PI / 2 + Math.PI / 2 });
    // bandeiras e tochas
    for (let i = 0; i < 12; i++) {
      const a = (i / 12) * TAU + 0.13;
      if (inGap(a)) continue;
      const x = C.x + Math.cos(a) * 22.2;
      const z = C.z + Math.sin(a) * 22.2;
      M.cyl(0.1, 0.1, 4.4, '#555', { x, y: 5, z }, 5);
      M.box(0.12, 2.4, 1.6, i % 2 ? '#d8404f' : '#2f8fd8', { x, y: 6.6, z, ry: -a });
      if (i % 3 === 0) {
        M.cyl(0.25, 0.3, 1.6, '#3a3a46', { x: C.x + Math.cos(a + 0.12) * 21.6, y: 0.8, z: C.z + Math.sin(a + 0.12) * 21.6 }, 6);
        flame(C.x + Math.cos(a + 0.12) * 21.6, 1.6, C.z + Math.sin(a + 0.12) * 21.6, 0.9, i % 6 === 0);
      }
    }
    keep(C.x, C.z, 40);
  }

  // =================== FAZENDA ===================
  {
    const F = LOCATIONS.farm;
    const fields = [[-135, 118, 20, 16, '#e8c84a'], [-135, 142, 20, 16, '#7fbf3a'], [-108, 100, 18, 14, '#d89a3a'], [-82, 112, 16, 16, '#9bd45a'], [-84, 138, 18, 14, '#e8c84a']];
    for (const [x, z, w, d, c] of fields) {
      const y = baseY(x, z, w, d) + 0.05;
      M.box(w, 0.2, d, '#7a5a3a', { x, y: y - 0.06, z });
      for (let r = 0; r < Math.floor(w / 2.2); r++) M.box(1.1, 0.5 + (r % 2) * 0.15, d - 1.2, c, { x: x - w / 2 + 1.4 + r * 2.2, y: y + 0.3, z });
      for (const [sx, sz, sw, sd] of [[0, d / 2, w, 0.15], [0, -d / 2, w, 0.15], [w / 2, 0, 0.15, d], [-w / 2, 0, 0.15, d]]) M.box(sw, 0.9, sd, '#8a5a3a', { x: x + sx, y: y + 0.45, z: z + sz });
      keep(x, z, Math.max(w, d) / 2 + 2);
    }
    // celeiro
    {
      const x = -108;
      const z = 128;
      const y = found(x, z, 14, 10, 0.4, '#7a6a5a');
      const L = new Local(M, x, y, z, 0.4);
      L.box(14, 7.5, 10, '#c0392b', 0, 3.75, 0);
      L.gable(14, 10, 4.6, '#7a2a22', 7.5);
      L.box(5, 5.2, 0.2, '#f6f0e4', 0, 2.6, 5.05);
      for (const s of [-1, 1]) L.box(0.3, 7, 0.22, '#f6f0e4', s * 1.2, 2.6, 5.14);
      L.box(2.4, 2.4, 0.2, '#f6f0e4', 0, 6.8, 5.05);
      rectCol(x, z, 14, 10, 0.4);
      keep(x, z, 11);
      // silo
      const sx = x + 11 * Math.cos(0.4) + 3;
      const sz = z - 11 * Math.sin(0.4);
      M.cyl(3, 3, 12, '#cfd6df', { x: sx, y: y + 6, z: sz }, 14);
      M.ball(3, '#9aa3b0', { x: sx, y: y + 12, z: sz }, 12);
      col.add(sx, sz, 3.4);
      keep(sx, sz, 5);
    }
    // moinho que gira
    {
      const x = -140;
      const z = 160;
      const y = found(x, z, 8, 8, 0);
      M.cyl(2.4, 3.6, 12, '#e9dcc0', { x, y: y + 6, z }, 8);
      M.cone(3.2, 4, '#8a3a2a', { x, y: y + 14, z }, 8);
      M.box(1.4, 2.4, 0.2, '#6b432c', { x, y: y + 1.2, z: z + 3.2 });
      const hub = new THREE.Group();
      hub.position.set(x, y + 11.5, z + 3.2);
      const blades = new THREE.Group();
      for (let k = 0; k < 4; k++) {
        const arm = new THREE.Group();
        const m = new Merge();
        m.box(0.35, 9, 0.18, '#8a5a3a', { y: 4.5 });
        m.box(2.0, 6.5, 0.1, '#f6f0e4', { x: 1.2, y: 5.2 });
        arm.add(m.mesh(vcMat()));
        arm.rotation.z = (k * Math.PI) / 2;
        blades.add(arm);
      }
      hub.add(blades);
      root.add(hub);
      upd.push((_t, dt) => (blades.rotation.z += dt * 0.5));
      col.add(x, z, 3.8);
      keep(x, z, 6);
    }
    for (const [x, z] of [[-122, 124], [-118, 148], [-96, 150], [-70, 128]]) {
      const y = hy(x, z);
      M.cyl(0.9, 0.9, 1.3, '#d8b85a', { x, y: y + 0.65, z, rz: 1.5708 }, 10);
      M.cyl(0.9, 0.9, 1.3, '#cfae4a', { x: x + 1.7, y: y + 0.65, z, rz: 1.5708 }, 10);
      col.add(x + 0.8, z, 1.4);
    }
    {
      const x = -100;
      const z = 114;
      const y = hy(x, z);
      M.cyl(0.1, 0.1, 3.2, '#6b432c', { x, y: y + 1.6, z }, 5);
      M.box(2.4, 0.12, 0.12, '#6b432c', { x, y: y + 2.5, z });
      M.ball(0.4, '#e8c97a', { x, y: y + 3.3, z }, 8);
      M.cone(0.55, 0.6, '#8a5a3a', { x, y: y + 3.8, z }, 8);
    }
  }

  // =================== ACAMPAMENTO NA FLORESTA ===================
  {
    const x = 28;
    const z = -165;
    const y = hy(x, z);
    M.cyl(2.6, 2.8, 0.25, '#8a8f98', { x: x - 8, y: y + 0.1, z }, 14);
    for (let k = 0; k < 8; k++) {
      const a = (k / 8) * TAU;
      M.ball(0.5, '#7a8088', { x: x - 8 + Math.cos(a) * 2.2, y: y + 0.3, z: z + Math.sin(a) * 2.2 }, 6);
    }
    for (let k = 0; k < 4; k++) {
      const a = (k / 4) * TAU;
      M.cyl(0.25, 0.25, 2.2, '#6b432c', { x: x - 8 + Math.cos(a) * 0.5, y: y + 0.4, z: z + Math.sin(a) * 0.5, rz: 1.1 * Math.cos(a), rx: -1.1 * Math.sin(a) }, 6);
    }
    flame(x - 8, y + 0.3, z, 1.5, true, '#ff8a3a');
    keep(x - 8, z, 5);
    col.add(x - 8, z, 2.6);
    for (const [bx, bz, ry] of [[x - 12, z + 4, 0.5], [x - 4, z + 5, -0.4]]) M.box(3, 0.5, 0.8, '#8a5a3a', { x: bx, y: hy(bx, bz) + 0.45, z: bz, ry });
    const L = new Local(M, x + 8, hy(x + 8, z), z - 4, -0.6);
    L.box(10, 4, 8, '#8a5a3a', 0, 2, 0);
    for (let k = 0; k < 7; k++) L.cyl(0.32, 0.32, 10.4, '#7a4c2a', 0, 0.6 + k * 0.6, 4.05, 8);
    L.gable(10, 8, 3.2, '#5a3a22', 4);
    L.box(1.5, 2.6, 0.2, '#4a2f1a', 0, 1.3, 4.1);
    new Local(G, x + 8, hy(x + 8, z), z - 4, -0.6).box(1.3, 1.3, 0.14, '#ffe9a8', 3, 2.4, 4.1);
    rectCol(x + 8, z - 4, 10, 8, -0.6);
    keep(x + 8, z - 4, 9);
    for (const [tx, tz, c] of [[x - 18, z - 8, '#d8404f'], [x - 22, z + 2, '#2f8fd8']]) {
      M.cone(2.6, 3.6, c, { x: tx, y: hy(tx, tz) + 1.8, z: tz }, 4);
      M.box(0.9, 1.8, 0.1, '#2a1a10', { x: tx, y: hy(tx, tz) + 0.9, z: tz + 1.4 });
      col.add(tx, tz, 2.2);
      keep(tx, tz, 4);
    }
    // círculo de pedras místico
    const sx = -40;
    const sz = -215;
    for (let k = 0; k < 7; k++) {
      const a = (k / 7) * TAU;
      const px = sx + Math.cos(a) * 7;
      const pz = sz + Math.sin(a) * 7;
      M.box(1.4, 4 + (k % 3), 1, '#8d96a2', { x: px, y: hy(px, pz) + 2.2, z: pz, ry: a });
      col.add(px, pz, 1.1);
    }
    M.cyl(1.2, 1.2, 0.6, '#8d96a2', { x: sx, y: hy(sx, sz) + 0.3, z: sz }, 10);
    B.ball(0.5, '#7fe8ff', { x: sx, y: hy(sx, sz) + 1.2, z: sz }, 8);
    keep(sx, sz, 10);
  }

  // =================== DESERTO ===================
  {
    const P = LOCATIONS.pyramid;
    const y = baseY(P.x, P.z, 34, 34);
    M.box(40, 6, 40, '#c9a45a', { x: P.x, y: y - 2, z: P.z });
    for (let i = 0; i < 9; i++) {
      const s = 34 - i * 3.6;
      M.box(s, 2.6, s, i % 2 ? '#e0bd70' : '#d8b567', { x: P.x, y: y + 1.3 + i * 2.6, z: P.z });
    }
    M.cone(2.5, 4.2, '#ffd24a', { x: P.x, y: y + 26, z: P.z }, 4);
    B.ball(0.5, '#ffe9a0', { x: P.x, y: y + 28.5, z: P.z }, 8);
    M.box(5, 5, 4, '#2a2218', { x: P.x, y: y + 2.5, z: P.z + 16.2 });
    rectCol(P.x, P.z, 34, 34, 0);
    keep(P.x, P.z, 26);
    for (const [ox, oz] of [[-24, 22], [24, 22], [-24, -22], [24, -22]]) {
      const x = P.x + ox;
      const z = P.z + oz;
      M.box(1.6, 12, 1.6, '#d8c08a', { x, y: hy(x, z) + 6, z });
      M.cone(1.2, 2, '#ffd24a', { x, y: hy(x, z) + 13, z }, 4);
      col.add(x, z, 1.2);
    }
    // oásis (palmeiras e rochas ao redor) e tendas
    const O = { x: 150, z: 45 };
    for (let k = 0; k < 6; k++) {
      const a = (k / 6) * TAU + 0.3;
      const px = O.x + Math.cos(a) * 15;
      const pz = O.z + Math.sin(a) * 15;
      const py = hy(px, pz);
      for (let s = 0; s < 6; s++) M.cyl(0.28 - s * 0.02, 0.32 - s * 0.02, 1.2, '#a8814f', { x: px + s * 0.12, y: py + 0.6 + s * 1.15, z: pz }, 7);
      for (let s = 0; s < 7; s++) {
        const b = (s / 7) * TAU;
        M.cone(0.45, 3.4, '#3fb25a', { x: px + 0.7 + Math.cos(b) * 1.4, y: py + 7.1, z: pz + Math.sin(b) * 1.4, rz: -Math.cos(b) * 1.2, rx: Math.sin(b) * 1.2 }, 4);
      }
      col.add(px, pz, 0.6);
    }
    for (const [tx, tz] of [[165, -65], [178, -72], [158, -75]]) {
      const ty = hy(tx, tz);
      M.cone(3.6, 4.4, '#e8d3a0', { x: tx, y: ty + 2.2, z: tz }, 7);
      M.box(1.2, 2.2, 0.1, '#3a2a1a', { x: tx, y: ty + 1.1, z: tz + 3.1 });
      col.add(tx, tz, 3.2);
      keep(tx, tz, 5);
    }
    for (const [ax, az] of [[200, 40], [230, 30]]) {
      const ay = hy(ax, az);
      for (const s of [-1, 1]) M.box(2, 8, 2, '#d8c08a', { x: ax + s * 4, y: ay + 4, z: az });
      M.box(10, 2, 2.4, '#d8c08a', { x: ax, y: ay + 8.6, z: az });
      col.add(ax - 4, az, 1.5);
      col.add(ax + 4, az, 1.5);
    }
  }

  // =================== MONTANHAS GELADAS ===================
  {
    for (const [x, z, s] of [[-190, -55, 1], [-214, -66, 0.9], [-178, -85, 1.1], [-228, -45, 0.8]]) {
      const y = hy(x, z);
      M.add(new THREE.SphereGeometry(4.6 * s, 18, 10, 0, TAU, 0, Math.PI / 2), '#f4f9ff', { x, y: y - 0.1, z });
      M.box(3 * s, 2.4 * s, 4 * s, '#f4f9ff', { x, y: y + 1.2 * s, z: z + 4.6 * s });
      B.box(1.6 * s, 1.8 * s, 0.1, '#6bb8e8', { x, y: y + 1 * s, z: z + 6.7 * s });
      col.add(x, z, 4.6 * s);
      keep(x, z, 7 * s);
    }
    for (const [x, z] of [[-196, -4], [-188, 6], [-232, -16]]) {
      const y = hy(x, z);
      M.ball(1.4, '#fdfdff', { x, y: y + 1.1, z }, 10);
      M.ball(1.0, '#fdfdff', { x, y: y + 2.9, z }, 10);
      M.ball(0.7, '#fdfdff', { x, y: y + 4.1, z }, 10);
      M.cone(0.18, 0.9, '#ff8a3d', { x, y: y + 4.1, z: z + 0.8, rx: 1.5708 }, 6);
      M.cyl(0.5, 0.5, 0.7, '#2a2a30', { x, y: y + 4.9, z }, 8);
      col.add(x, z, 1.4);
    }
    for (let k = 0; k < 14; k++) {
      const a = Math.random() * TAU;
      const d = 14 + Math.random() * 24;
      const x = -215 + Math.cos(a) * (d + 20);
      const z = 20 + Math.sin(a) * (d + 14);
      if (Math.hypot(x + 215, z - 20) < 29) continue;
      const y = hy(x, z);
      M.add(new THREE.OctahedronGeometry(1 + Math.random(), 0), '#9fd8ff', { x, y: y + 1.6, z, sy: 1.8 });
      col.add(x, z, 1.1);
    }
    const L = new Local(M, -176, hy(-176, -10), -10, 0.3);
    L.box(9, 3.8, 7, '#9b6f45', 0, 1.9, 0);
    L.gable(9, 7, 3, '#f4f9ff', 3.8);
    L.box(1.4, 2.4, 0.2, '#4a2f1a', 0, 1.2, 3.55);
    new Local(G, -176, hy(-176, -10), -10, 0.3).box(1.2, 1.2, 0.14, '#ffe9a8', 2.6, 2.3, 3.55);
    L.box(1.2, 3.4, 1.2, '#7a7a82', -3, 4.8, -1);
    rectCol(-176, -10, 9, 7, 0.3);
    keep(-176, -10, 8);
  }

  // =================== PRAIA ===================
  {
    const lx = 46;
    const lz = 184;
    const y = hy(lx, lz);
    for (let i = 0; i < 6; i++) M.cyl(3 - i * 0.28, 3.2 - i * 0.28, 3, i % 2 ? '#d8404f' : '#fdfdff', { x: lx, y: y + 1.5 + i * 3, z: lz }, 12);
    M.cyl(3, 2.6, 0.6, '#3a3a46', { x: lx, y: y + 18.3, z: lz }, 12);
    G.cyl(2.2, 2.2, 2.6, '#ffe9a8', { x: lx, y: y + 19.9, z: lz }, 10);
    M.cone(3, 2.6, '#d8404f', { x: lx, y: y + 22.5, z: lz }, 12);
    col.add(lx, lz, 3.6);
    keep(lx, lz, 7);
    const beam = new THREE.Mesh(new THREE.ConeGeometry(5, 40, 14, 1, true), new THREE.MeshBasicMaterial({ color: '#fff3b0', transparent: true, opacity: 0.18, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide }));
    beam.geometry.translate(0, -20, 0);
    beam.rotation.z = Math.PI / 2;
    const beamG = new THREE.Group();
    beamG.position.set(lx, y + 19.9, lz);
    beamG.add(beam);
    root.add(beamG);
    upd.push((_t, dt) => (beamG.rotation.y += dt * 0.7));
    // doca
    const dx0 = 11;
    const dx1 = 19;
    const dz0 = 176;
    const dz1 = 214;
    for (let z = dz0; z < dz1; z += 1.1) M.box(8, 0.3, 1.0, z % 2 < 1 ? '#a8814f' : '#9a7648', { x: 15, y: 0.5, z });
    for (let z = dz0 + 2; z < dz1; z += 6) for (const s of [-1, 1]) M.cyl(0.22, 0.22, 3.2, '#6b432c', { x: 15 + s * 3.9, y: -0.6, z }, 6);
    col.walk.push({ rect: true, x0: dx0, x1: dx1, z0: dz0, z1: dz1, y: 0.62 });
    // barcos
    for (const [bx, bz, ry] of [[26, 206, 0.3], [4, 212, -0.4]]) {
      const B2 = new Local(M, bx, -0.7, bz, ry);
      B2.box(3.4, 1.2, 8, '#8a5a3a', 0, 0.6, 0);
      B2.box(3.0, 0.2, 7.4, '#a8814f', 0, 1.2, 0);
      B2.cyl(0.14, 0.14, 8, '#6b432c', 0, 5, 0, 6);
      B2.box(0.1, 5, 3.4, '#fdfdff', 0, 5, -1.7);
    }
    // guarda-sóis, toalhas, cabana
    for (const [ux, uz, c] of [[-10, 172, '#d8404f'], [-18, 180, '#2f8fd8'], [-4, 184, '#f0b429'], [34, 168, '#a35cff']]) {
      const uy = hy(ux, uz);
      M.cyl(0.07, 0.07, 3.2, '#e8e0d0', { x: ux, y: uy + 1.6, z: uz }, 5);
      M.cone(2.2, 0.8, c, { x: ux, y: uy + 3.4, z: uz }, 10);
      M.box(2.4, 0.06, 1.2, '#fdf6e0', { x: ux + 1.4, y: uy + 0.06, z: uz + 0.8, ry: 0.4 });
      col.add(ux, uz, 0.5);
    }
    const hut = new Local(M, -28, hy(-28, 170), 170, 0.2);
    hut.box(7, 3.4, 6, '#f6e8c8', 0, 1.7, 0);
    hut.roof(8, 7, 2.6, '#c0503f', 3.4);
    hut.box(1.3, 2.4, 0.2, '#6b432c', 0, 1.2, 3.05);
    new Local(G, -28, hy(-28, 170), 170, 0.2).box(1.3, 1.2, 0.14, '#ffe9a8', 2.3, 2.1, 3.05);
    rectCol(-28, 170, 7, 6, 0.2);
    keep(-28, 170, 7);
  }

  // =================== CASTELO ===================
  {
    const C = LOCATIONS.castle;
    const y = 16;
    const S = 30;
    const wallC = '#a9b0bd';
    for (const [sx, sz, w, d] of [[0, -S, 2 * S, 3], [-S, 0, 3, 2 * S], [S, 0, 3, 2 * S], [-S / 2 - 6.5, S, S - 13, 3], [S / 2 + 6.5, S, S - 13, 3]]) {
      M.box(w, 11, d, wallC, { x: C.x + sx, y: y + 5.5, z: C.z + sz });
      const n = Math.floor(Math.max(w, d) / 2.6);
      for (let i = 0; i < n; i++) {
        const t = -Math.max(w, d) / 2 + 1.3 + i * 2.6;
        M.box(w > d ? 1.4 : d, 1.3, w > d ? d : 1.4, '#9aa1ae', { x: C.x + sx + (w > d ? t : 0), y: y + 11.6, z: C.z + sz + (w > d ? 0 : t) });
      }
      col.wall(C.x + sx - (w > d ? w / 2 : 0), C.z + sz - (w > d ? 0 : d / 2), C.x + sx + (w > d ? w / 2 : 0), C.z + sz + (w > d ? 0 : d / 2), 2.0);
    }
    for (const [sx, sz] of [[-S, -S], [S, -S], [-S, S], [S, S]]) {
      M.cyl(5.4, 5.8, 19, '#b4bbc8', { x: C.x + sx, y: y + 9.5, z: C.z + sz }, 14);
      M.cone(6.6, 8, sx < 0 ? '#2f6fb8' : '#c0392b', { x: C.x + sx, y: y + 23, z: C.z + sz }, 14);
      M.cyl(0.08, 0.08, 4, '#555', { x: C.x + sx, y: y + 29, z: C.z + sz }, 4);
      M.box(0.1, 1.4, 2.2, '#ffd24a', { x: C.x + sx, y: y + 30, z: C.z + sz + 1.1 });
      for (let k = 0; k < 3; k++) G.box(0.9, 1.6, 0.9, '#ffe9a8', { x: C.x + sx + Math.cos(k * 2) * 5.4, y: y + 10 + k * 3, z: C.z + sz + Math.sin(k * 2) * 5.4 });
      col.add(C.x + sx, C.z + sz, 6.2);
    }
    // portão (torres + arco)
    for (const s of [-1, 1]) {
      M.cyl(3.4, 3.8, 15, '#b4bbc8', { x: C.x + s * 7.5, y: y + 7.5, z: C.z + S }, 12);
      M.cone(4.4, 5.5, '#c0392b', { x: C.x + s * 7.5, y: y + 17.7, z: C.z + S }, 12);
      col.add(C.x + s * 7.5, C.z + S, 4.2);
      flame(C.x + s * 5, y + 4.4, C.z + S + 3.6, 1.0, true);
    }
    M.box(11, 3.4, 3.2, wallC, { x: C.x, y: y + 9.2, z: C.z + S });
    M.box(6, 7, 0.4, '#1a1410', { x: C.x, y: y + 3.5, z: C.z + S + 0.3 });
    // fortaleza central
    {
      const K = new Local(M, C.x, y, C.z - 6, 0);
      K.box(22, 24, 20, '#b4bbc8', 0, 12, 0);
      K.box(22.6, 1.2, 20.6, '#9aa1ae', 0, 24.6, 0);
      for (let i = 0; i < 8; i++) {
        K.box(1.6, 1.4, 1.6, '#9aa1ae', -9.6 + i * 2.75, 25.9, 10);
        K.box(1.6, 1.4, 1.6, '#9aa1ae', -9.6 + i * 2.75, 25.9, -10);
      }
      for (const [tx, tz] of [[-11, -10], [11, -10], [-11, 10], [11, 10]]) {
        K.cyl(3, 3.2, 28, '#bcc3d0', tx, 14, tz, 10);
        K.cone(3.8, 6, '#a35cff', tx, 31, tz, 10);
      }
      K.box(5.5, 8, 0.4, '#1a1410', 0, 4, 10.1);
      const W = new Local(G, C.x, y, C.z - 6, 0);
      for (const wx of [-7, 7]) for (const wy of [8, 14, 20]) W.box(1.6, 2.4, 0.2, '#ffe9a8', wx, wy, 10.1);
      rectCol(C.x, C.z - 6, 22, 20, 0, 0.6);
      keep(C.x, C.z, 42);
    }
    // ponte levadiça e fogueiras no pátio
    for (let z = 0; z < 16; z += 1.2) M.box(6, 0.4, 1.0, '#7a5a3a', { x: C.x, y: y + 0.4, z: C.z + S + 2 + z });
    flame(C.x - 10, y + 0.3, C.z + 14, 1.3, true);
    flame(C.x + 10, y + 0.3, C.z + 14, 1.3, true);
  }

  // =================== RUÍNAS ===================
  {
    const R = LOCATIONS.ruins;
    for (let k = 0; k < 14; k++) {
      const a = (k / 14) * TAU + (k % 3) * 0.1;
      const d = 12 + (k % 4) * 7;
      const x = R.x + Math.cos(a) * d;
      const z = R.z + Math.sin(a) * d;
      const h = 3 + (k % 5) * 2.2;
      const y = hy(x, z);
      M.cyl(1.1, 1.3, h, '#b4b9a4', { x, y: y + h / 2, z }, 10);
      M.box(2.8, 0.7, 2.8, '#a6ab97', { x, y: y + h + 0.3, z });
      if (k % 4 === 0) M.cyl(1.1, 1.1, 5, '#b4b9a4', { x: x + 4, y: y + 1, z: z + 2, rz: 1.45 }, 9);
      col.add(x, z, 1.5);
    }
    {
      const ax = R.x;
      const az = R.z - 22;
      const y = hy(ax, az);
      for (const s of [-1, 1]) M.box(3, 12, 3, '#aab09a', { x: ax + s * 6, y: y + 6, z: az });
      M.box(15, 3, 3.2, '#aab09a', { x: ax, y: y + 12.5, z: az });
      M.box(7, 5, 0.6, '#16161c', { x: ax, y: y + 2.5, z: az });
      col.add(ax - 6, az, 2.2);
      col.add(ax + 6, az, 2.2);
    }
    M.box(7, 1.6, 3.4, '#9ea48e', { x: R.x, y: hy(R.x, R.z) + 0.8, z: R.z });
    B.box(5, 0.1, 2, '#b06bff', { x: R.x, y: hy(R.x, R.z) + 1.66, z: R.z });
    col.add(R.x, R.z, 3);
    keep(R.x, R.z, 9);
    for (let k = 0; k < 20; k++) {
      const a = Math.random() * TAU;
      const d = 8 + Math.random() * 40;
      const x = R.x + Math.cos(a) * d;
      const z = R.z + Math.sin(a) * d;
      M.box(1 + Math.random() * 1.6, 0.8 + Math.random() * 1.2, 1 + Math.random() * 1.6, '#a7ad98', { x, y: hy(x, z) + 0.6, z, ry: Math.random() * 3 });
    }
  }

  // ---------- placas de sinalização nos cruzamentos ----------
  for (const [key, x, z] of [['forest', 6, -68], ['desert', 76, 6], ['snow', -76, -8], ['farm', -52, 58], ['beach', 6, 78], ['castle', 148, -22], ['colosseum', 52, 24]]) {
    const y = hy(x, z);
    M.cyl(0.14, 0.14, 4.4, '#6b432c', { x, y: y + 2.2, z }, 6);
    M.box(4.6, 1.2, 0.2, '#a8814f', { x, y: y + 4.3, z });
    const tag = nameTag('→ ' + LOCATIONS[key].name, '#fff2c8');
    tag.scale.set(3.4, 0.64, 1);
    tag.position.set(x, y + 5.7, z);
    root.add(tag);
    col.add(x, z, 0.4);
  }

  // ---------- materiais finais e animações ----------
  root.add(M.mesh(vcMat({ roughness: 0.9 })));
  const glass = new THREE.MeshStandardMaterial({ vertexColors: true, emissive: '#ffcf7a', emissiveIntensity: 0.05, roughness: 0.3 });
  const bulbs = new THREE.MeshStandardMaterial({ vertexColors: true, emissive: '#ffb04a', emissiveIntensity: 0.6, roughness: 0.3 });
  api.windowMats.push(glass, bulbs);
  const gm = G.mesh(glass, { cast: false });
  if (gm) root.add(gm);
  const bm = B.mesh(bulbs, { cast: false });
  if (bm) root.add(bm);
  upd.push((t) => {
    for (const f of flames) {
      const k = 1 + Math.sin(t * 14 + f.ph) * 0.13 + Math.sin(t * 23 + f.ph) * 0.07;
      f.f.scale.set(1, k, 1);
      f.f2.scale.set(1, k * 1.15, 1);
      if (f.l) f.l.intensity = 62 + Math.sin(t * 11 + f.ph) * 14;
    }
  });
  api.flames = flames;
}
