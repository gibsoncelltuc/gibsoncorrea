// Terreno de blocos (estilo Minecraft): atlas de texturas desenhado por código + malha por chunk com faces visíveis.
// Cada coluna do mundo tem 2x2 unidades; heightAt() (shared/world.js) dá o topo do bloco e este arquivo desenha tudo.
import * as THREE from 'three';
import { BLOCK, WORLD_HALF, SEA_LEVEL, LAKES, heightAt, biomeWeights, roadDist, colCenter } from './shared/world.js';

// ---------- atlas de texturas 16x16 ----------
export const TILE = { grass: 0, grassSide: 1, dirt: 2, stone: 3, sand: 4, sandstone: 5, snow: 6, snowSide: 7, gravel: 8, cobble: 9, path: 10, farm: 11, ice: 12, mossy: 13, bricks: 14, planks: 15, log: 16, logTop: 17, leaves: 18, cactus: 19, water: 20, magma: 21, birchLog: 22, ore: 23, tuft: 24 };
const COLS = 8;
const ROWS = 4;
let atlasTex = null;
function seeded(seed) {
  let s = seed >>> 0;
  return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
}
export function makeAtlas() {
  if (atlasTex) return atlasTex;
  const c = document.createElement('canvas');
  c.width = COLS * 16;
  c.height = ROWS * 16;
  const g = c.getContext('2d');
  const hex = (h) => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
  // preenche um tile com cor base + ruído por pixel (o "jeitão" de pixel-art do Minecraft)
  const tile = (id, base, jit = 18, fn = null, seed = id * 977 + 13) => {
    const r = seeded(seed);
    const [br, bg, bb] = hex(base);
    const ox = (id % COLS) * 16;
    const oy = Math.floor(id / COLS) * 16;
    for (let y = 0; y < 16; y++) {
      for (let x = 0; x < 16; x++) {
        const k = (r() - 0.5) * 2 * jit;
        let col = [br + k, bg + k, bb + k];
        if (fn) col = fn(x, y, col, r) ?? col;
        g.fillStyle = `rgb(${col.map((v) => Math.max(0, Math.min(255, v | 0))).join(',')})`;
        g.fillRect(ox + x, oy + y, 1, 1);
      }
    }
  };
  tile(TILE.grass, '#79b94a', 22);
  tile(TILE.dirt, '#8a5f3b', 20, (x, y, c, r) => (r() < 0.07 ? [c[0] - 40, c[1] - 30, c[2] - 20] : null));
  tile(TILE.grassSide, '#8a5f3b', 20, (x, y, c, r) => {
    const edge = 3 + ((x * 7) % 3 === 0 ? 1 : 0) + (r() < 0.3 ? 1 : 0);
    return y < edge ? [96 + (r() - 0.5) * 36, 170 + (r() - 0.5) * 36, 62] : null;
  });
  tile(TILE.stone, '#8b8b8b', 16, (x, y, c, r) => (r() < 0.1 ? [c[0] - 30, c[1] - 30, c[2] - 30] : null));
  tile(TILE.sand, '#e2d39a', 10);
  tile(TILE.sandstone, '#d6c283', 9, (x, y, c) => (y % 5 === 4 ? [c[0] - 22, c[1] - 22, c[2] - 20] : null));
  tile(TILE.snow, '#f7fbff', 6);
  tile(TILE.snowSide, '#8a5f3b', 20, (x, y, c, r) => (y < 4 + (r() < 0.4 ? 1 : 0) ? [245, 250, 255 - r() * 8] : null));
  tile(TILE.gravel, '#8d8a88', 28, (x, y, c, r) => (r() < 0.12 ? [c[0] + 30, c[1] + 28, c[2] + 26] : null));
  tile(TILE.cobble, '#7c7c7c', 20, (x, y, c) => ((x + (y >> 2 & 1) * 3) % 8 === 0 || y % 4 === 0 ? [c[0] - 32, c[1] - 32, c[2] - 32] : null));
  tile(TILE.path, '#a98b55', 14, (x, y, c, r) => (r() < 0.12 ? [c[0] - 26, c[1] - 24, c[2] - 20] : null));
  tile(TILE.farm, '#6b4428', 10, (x, y, c) => (x % 4 === 1 ? [c[0] - 24, c[1] - 18, c[2] - 12] : null));
  tile(TILE.ice, '#a8d8f5', 12, (x, y, c, r) => (r() < 0.08 ? [235, 248, 255] : null));
  tile(TILE.mossy, '#6f7f5f', 22, (x, y, c, r) => (r() < 0.25 ? [80, 130 + r() * 30, 60] : null));
  tile(TILE.bricks, '#9a5a4a', 12, (x, y, c) => (y % 4 === 3 || (x + (y >> 2 & 1) * 4) % 8 === 0 ? [185, 175, 165] : null));
  tile(TILE.planks, '#b08850', 10, (x, y, c) => (y % 4 === 3 ? [c[0] - 40, c[1] - 36, c[2] - 28] : null));
  tile(TILE.log, '#6a4a2a', 16, (x, y, c) => (x % 4 === 0 ? [c[0] - 22, c[1] - 18, c[2] - 12] : null));
  tile(TILE.logTop, '#a9834f', 12, (x, y, c) => (Math.max(Math.abs(x - 7.5), Math.abs(y - 7.5)) % 4 < 1.2 ? [c[0] - 30, c[1] - 26, c[2] - 20] : null));
  tile(TILE.leaves, '#3f8f35', 32, (x, y, c, r) => (r() < 0.2 ? [30, 90, 30] : null));
  tile(TILE.cactus, '#3e8a3e', 14, (x, y, c) => (x % 5 === 2 ? [c[0] - 20, c[1] - 24, c[2] - 20] : null));
  tile(TILE.water, '#2f6fe0', 14);
  tile(TILE.magma, '#d84a14', 40, (x, y, c, r) => (r() < 0.25 ? [255, 190 + r() * 60, 40] : null));
  tile(TILE.birchLog, '#e6e2d6', 12, (x, y, c, r) => (r() < 0.12 && y % 3 === 0 ? [40, 40, 40] : null));
  tile(TILE.ore, '#8b8b8b', 14, (x, y, c, r) => (r() < 0.14 ? [240, 200, 60] : null));
  // capim: só as lâminas verdes, o resto transparente
  {
    const ox = (TILE.tuft % COLS) * 16;
    const oy = Math.floor(TILE.tuft / COLS) * 16;
    const r = seeded(4242);
    g.clearRect(ox, oy, 16, 16);
    for (let x = 1; x < 15; x += 2) {
      const h = 6 + Math.floor(r() * 9);
      for (let y = 16 - h; y < 16; y++) {
        g.fillStyle = `rgb(${70 + r() * 30 | 0},${150 + r() * 60 | 0},${50 + r() * 20 | 0})`;
        g.fillRect(ox + x, oy + y, 1 + (r() < 0.3 ? 1 : 0), 1);
      }
    }
  }
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.magFilter = THREE.NearestFilter;
  t.minFilter = THREE.NearestMipmapLinearFilter;
  t.generateMipmaps = true;
  atlasTex = t;
  return t;
}
const uvRect = (id) => {
  const e = 0.0015;
  const u0 = (id % COLS) / COLS + e;
  const v1 = 1 - Math.floor(id / COLS) / ROWS - e;
  return [u0, v1 - 1 / ROWS + 2 * e, u0 + 1 / COLS - 2 * e, v1];
};

// ---------- o que cada coluna é feita ----------
const rnd2 = (a, b) => {
  const s = Math.sin(a * 127.1 + b * 311.7) * 43758.5453;
  return s - Math.floor(s);
};
function surface(x, z, q) {
  const w = biomeWeights(x, z);
  const r = rnd2(x, z);
  let top = TILE.grass;
  let side = TILE.grassSide;
  let under = TILE.dirt;
  let tint = [1, 1, 1];
  if (w.forest > 0.45) tint = [0.62, 0.86, 0.6];
  else if (w.farm > 0.5) {
    tint = [1.12, 1.05, 0.7];
    if (r < 0.4 && roadDist(x, z) > 4) (top = TILE.farm), (side = TILE.dirt);
  } else if (w.castle > 0.5) (top = TILE.cobble), (side = TILE.cobble), (under = TILE.stone), (tint = [0.9, 0.95, 0.9]);
  else if (w.ruins > 0.5) {
    top = r < 0.45 ? TILE.mossy : TILE.gravel;
    side = r < 0.45 ? TILE.mossy : TILE.gravel;
    under = TILE.stone;
    tint = [1, 1, 1];
  } else if (w.desert > 0.45) (top = TILE.sand), (side = TILE.sand), (under = TILE.sandstone);
  else if (w.snow > 0.5) (top = TILE.snow), (side = TILE.snowSide), (under = TILE.dirt);
  else if (w.beach > 0.5 && q < 6) (top = TILE.sand), (side = TILE.sand), (under = TILE.sandstone);
  if (q >= 12 && w.castle < 0.5 && w.town < 0.5) {
    // serras e montanhas altas
    if (q >= 26) (top = TILE.snow), (side = TILE.snowSide), (under = TILE.stone);
    else (top = TILE.stone), (side = TILE.stone), (under = TILE.stone), (tint = [1, 1, 1]);
  }
  if (q <= SEA_LEVEL + 0.9) (top = TILE.sand), (side = TILE.sand), (under = TILE.sandstone), (tint = [1, 1, 1]);
  if (q <= SEA_LEVEL - 2) (top = TILE.gravel), (side = TILE.gravel), (under = TILE.gravel);
  if (q > SEA_LEVEL && roadDist(x, z) < 2.6 && w.castle < 0.5) (top = TILE.path), (side = TILE.dirt), (under = TILE.dirt), (tint = [1, 1, 1]);
  return { top, side, under, tint };
}

// ---------- malha ----------
const CH = 16; // colunas por chunk (32 unidades)
export function buildTerrain(root) {
  const N = Math.ceil((WORLD_HALF + 70) / BLOCK); // colunas de cada lado a partir do centro
  const size = N * 2;
  const idx = (cx, cz) => (cx + N) + (cz + N) * size;
  const H = new Int16Array(size * size);
  const S = new Array(size * size);
  const hAt = (cx, cz) => (cx < -N || cz < -N || cx >= N || cz >= N ? 40 : H[idx(cx, cz)]);
  for (let cz = -N; cz < N; cz++) {
    for (let cx = -N; cx < N; cx++) {
      const x = colCenter(cx);
      const z = colCenter(cz);
      const q = heightAt(x, z);
      H[idx(cx, cz)] = q / BLOCK;
      S[idx(cx, cz)] = surface(x, z, q);
    }
  }
  const mat = new THREE.MeshStandardMaterial({ map: makeAtlas(), vertexColors: true, roughness: 1, metalness: 0 });
  const group = new THREE.Group();
  root.add(group);
  const nChunks = Math.ceil(size / CH);
  for (let kz = 0; kz < nChunks; kz++) {
    for (let kx = 0; kx < nChunks; kx++) {
      const P = [];
      const Nn = [];
      const U = [];
      const C = [];
      const I = [];
      let vi = 0;
      const quad = (a, b, c, d, n, tile, col) => {
        const [u0, v0, u1, v1] = uvRect(tile);
        P.push(...a, ...b, ...c, ...d);
        for (let i = 0; i < 4; i++) Nn.push(...n), C.push(...col);
        U.push(u0, v0, u1, v0, u1, v1, u0, v1);
        I.push(vi, vi + 1, vi + 2, vi, vi + 2, vi + 3);
        vi += 4;
      };
      for (let lz = 0; lz < CH; lz++) {
        for (let lx = 0; lx < CH; lx++) {
          const cx = kx * CH + lx - N;
          const cz = kz * CH + lz - N;
          if (cx >= N || cz >= N) continue;
          const n = hAt(cx, cz);
          const s = S[idx(cx, cz)];
          const x0 = cx * BLOCK;
          const z0 = cz * BLOCK;
          const x1 = x0 + BLOCK;
          const z1 = z0 + BLOCK;
          const y = n * BLOCK;
          const j = 0.9 + rnd2(cx * 1.7, cz * 2.3) * 0.2; // variação de brilho por bloco, como a grama do Minecraft
          const tcol = [s.tint[0] * j, s.tint[1] * j, s.tint[2] * j];
          // topo (CCW visto de cima)
          quad([x0, y, z1], [x1, y, z1], [x1, y, z0], [x0, y, z0], [0, 1, 0], s.top, tcol);
          // laterais onde o vizinho é mais baixo: um quadrado por bloco de altura
          const sides = [
            [cx + 1, cz, [x1, 0, z1], [x1, 0, z0], [1, 0, 0]],
            [cx - 1, cz, [x0, 0, z0], [x0, 0, z1], [-1, 0, 0]],
            [cx, cz + 1, [x0, 0, z1], [x1, 0, z1], [0, 0, 1]],
            [cx, cz - 1, [x1, 0, z0], [x0, 0, z0], [0, 0, -1]],
          ];
          for (const [ax, az, p0, p1, nrm] of sides) {
            const nh = hAt(ax, az);
            for (let k = n - 1; k >= nh && k >= n - 40; k--) {
              const depth = n - 1 - k;
              const tile = depth === 0 ? s.side : depth <= 2 ? s.under : TILE.stone;
              const yb = k * BLOCK;
              const yt = yb + BLOCK;
              const sh = 0.8 + rnd2(cx * 3.1 + k, cz * 1.3) * 0.1;
              quad([p0[0], yb, p0[2]], [p1[0], yb, p1[2]], [p1[0], yt, p1[2]], [p0[0], yt, p0[2]], nrm, tile, [sh, sh, sh]);
            }
          }
        }
      }
      if (!P.length) continue;
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3));
      g.setAttribute('normal', new THREE.Float32BufferAttribute(Nn, 3));
      g.setAttribute('uv', new THREE.Float32BufferAttribute(U, 2));
      g.setAttribute('color', new THREE.Float32BufferAttribute(C, 3));
      g.setIndex(I);
      g.computeBoundingSphere();
      g.computeBoundingBox();
      const m = new THREE.Mesh(g, mat);
      m.receiveShadow = true;
      m.castShadow = true;
      group.add(m);
    }
  }
  void LAKES;
  return { group, material: mat };
}

// ---------- objetos feitos de blocos (árvores, pedras, cactos...) ----------
// blocos: [i, j, k, tile, {col:[r,g,b], s:[sx,sy,sz], cross:true}]; a célula (0,0,0) fica centrada no chão (x,z de -1 a 1, y de 0 a 2)
export function voxelGeometry(blocks) {
  const key = (i, j, k) => `${i},${j},${k}`;
  const full = new Set(blocks.filter((b) => !b[4]?.s && !b[4]?.cross).map((b) => key(b[0], b[1], b[2])));
  const P = [];
  const Nn = [];
  const U = [];
  const C = [];
  const I = [];
  let vi = 0;
  const quad = (a, b, c, d, n, tile, col) => {
    const [u0, v0, u1, v1] = uvRect(tile);
    P.push(...a, ...b, ...c, ...d);
    for (let i = 0; i < 4; i++) Nn.push(...n), C.push(...col);
    U.push(u0, v0, u1, v0, u1, v1, u0, v1);
    I.push(vi, vi + 1, vi + 2, vi, vi + 2, vi + 3);
    vi += 4;
  };
  for (const [i, j, k, tile, o = {}] of blocks) {
    const col = o.col ?? [1, 1, 1];
    const cx = i * BLOCK;
    const cz = k * BLOCK;
    const y0 = j * BLOCK;
    if (o.cross) {
      const w = BLOCK * 0.5 * (o.s?.[0] ?? 1);
      const h = BLOCK * (o.s?.[1] ?? 1);
      quad([cx - w, y0, cz - w], [cx + w, y0, cz + w], [cx + w, y0 + h, cz + w], [cx - w, y0 + h, cz - w], [0, 0, 1], tile, col);
      quad([cx + w, y0, cz - w], [cx - w, y0, cz + w], [cx - w, y0 + h, cz + w], [cx + w, y0 + h, cz - w], [0, 0, 1], tile, col);
      continue;
    }
    const sx = (o.s?.[0] ?? 1) * BLOCK * 0.5;
    const sy = (o.s?.[1] ?? 1) * BLOCK;
    const sz = (o.s?.[2] ?? 1) * BLOCK * 0.5;
    const part = !!o.s;
    const x0 = cx - sx;
    const x1 = cx + sx;
    const z0 = cz - sz;
    const z1 = cz + sz;
    const y1 = y0 + sy;
    const tl = (face) => (typeof tile === 'object' ? (tile[face] ?? tile.side) : tile);
    if (part || !full.has(key(i, j + 1, k))) quad([x0, y1, z1], [x1, y1, z1], [x1, y1, z0], [x0, y1, z0], [0, 1, 0], tl('top'), col);
    if (part || !full.has(key(i, j - 1, k))) quad([x0, y0, z0], [x1, y0, z0], [x1, y0, z1], [x0, y0, z1], [0, -1, 0], tl('bottom'), col);
    if (part || !full.has(key(i + 1, j, k))) quad([x1, y0, z1], [x1, y0, z0], [x1, y1, z0], [x1, y1, z1], [1, 0, 0], tl('side'), col);
    if (part || !full.has(key(i - 1, j, k))) quad([x0, y0, z0], [x0, y0, z1], [x0, y1, z1], [x0, y1, z0], [-1, 0, 0], tl('side'), col);
    if (part || !full.has(key(i, j, k + 1))) quad([x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1], [0, 0, 1], tl('side'), col);
    if (part || !full.has(key(i, j, k - 1))) quad([x1, y0, z0], [x0, y0, z0], [x0, y1, z0], [x1, y1, z0], [0, 0, -1], tl('side'), col);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3));
  g.setAttribute('normal', new THREE.Float32BufferAttribute(Nn, 3));
  g.setAttribute('uv', new THREE.Float32BufferAttribute(U, 2));
  g.setAttribute('color', new THREE.Float32BufferAttribute(C, 3));
  g.setIndex(I);
  return g;
}
