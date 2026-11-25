// Ferramentas para montar o mundo: fusão de geometrias, instâncias por chunk e colisões.
import * as THREE from 'three';
import { mergeGeometries } from './vendor/jsm/utils/BufferGeometryUtils.js';

export const TAU = Math.PI * 2;
export const rnd = (a, b) => a + Math.random() * (b - a);

// ---------- fusão de geometrias com cor por vértice ----------
export class Merge {
  constructor() {
    this.parts = [];
  }
  add(geo, color, o = {}) {
    const { x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0, sx = 1, sy = 1, sz = 1 } = o;
    const g = geo.index ? geo.toNonIndexed() : geo.clone();
    for (const k of Object.keys(g.attributes)) if (!['position', 'normal', 'uv'].includes(k)) g.deleteAttribute(k);
    g.applyMatrix4(new THREE.Matrix4().compose(new THREE.Vector3(x, y, z), new THREE.Quaternion().setFromEuler(new THREE.Euler(rx, ry, rz)), new THREE.Vector3(sx, sy, sz)));
    const n = g.attributes.position.count;
    const c = new Float32Array(n * 3);
    const col = new THREE.Color(color);
    for (let i = 0; i < n; i++) c.set([col.r, col.g, col.b], i * 3);
    g.setAttribute('color', new THREE.BufferAttribute(c, 3));
    this.parts.push(g);
    return this;
  }
  box(w, h, d, color, o) {
    return this.add(new THREE.BoxGeometry(w, h, d), color, o);
  }
  cyl(rt, rb, h, color, o, seg = 10) {
    return this.add(new THREE.CylinderGeometry(rt, rb, h, seg), color, o);
  }
  cone(r, h, color, o, seg = 8) {
    return this.add(new THREE.ConeGeometry(r, h, seg), color, o);
  }
  ball(r, color, o, seg = 10) {
    return this.add(new THREE.SphereGeometry(r, seg, Math.max(6, seg - 2)), color, o);
  }
  geometry() {
    return this.parts.length ? mergeGeometries(this.parts, false) : null;
  }
  mesh(material, { cast = true, receive = true } = {}) {
    const g = this.geometry();
    if (!g) return null;
    const m = new THREE.Mesh(g, material);
    m.castShadow = cast;
    m.receiveShadow = receive;
    return m;
  }
}
export const vcMat = (o = {}) => new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.85, metalness: 0, ...o });

// ---------- instâncias por chunk (culling por região) ----------
const CH = 90;
export class Instancer {
  constructor(geo, mat, { cast = true } = {}) {
    this.geo = geo;
    this.mat = mat;
    this.cast = cast;
    this.chunks = new Map();
    this.count = 0;
  }
  add(x, y, z, ry = 0, s = 1, color = null, sy = s) {
    const key = `${Math.floor((x + 400) / CH)},${Math.floor((z + 400) / CH)}`;
    let c = this.chunks.get(key);
    if (!c) this.chunks.set(key, (c = []));
    c.push([x, y, z, ry, s, color, sy]);
    this.count++;
  }
  build(group) {
    const m4 = new THREE.Matrix4();
    const q = new THREE.Quaternion();
    for (const list of this.chunks.values()) {
      const im = new THREE.InstancedMesh(this.geo, this.mat, list.length);
      list.forEach(([x, y, z, ry, s, color, sy], i) => {
        q.setFromEuler(new THREE.Euler(0, ry, 0));
        m4.compose(new THREE.Vector3(x, y, z), q, new THREE.Vector3(s, sy, s));
        im.setMatrixAt(i, m4);
        if (color) im.setColorAt(i, new THREE.Color(color));
      });
      im.castShadow = this.cast;
      im.receiveShadow = true;
      im.computeBoundingSphere();
      group.add(im);
    }
  }
}

// ---------- colisões (círculos em uma grade espacial) ----------
export class Colliders {
  constructor() {
    this.cells = new Map();
    this.walk = []; // superfícies caminháveis acima da água (docas, gelo)
  }
  add(x, z, r) {
    const key = `${Math.floor(x / 16)},${Math.floor(z / 16)}`;
    let c = this.cells.get(key);
    if (!c) this.cells.set(key, (c = []));
    c.push([x, z, r]);
  }
  wall(ax, az, bx, bz, r = 1.2) {
    const n = Math.max(1, Math.ceil(Math.hypot(bx - ax, bz - az) / (r * 1.4)));
    for (let i = 0; i <= n; i++) this.add(ax + ((bx - ax) * i) / n, az + ((bz - az) * i) / n, r);
  }
  // empurra o ponto para fora de qualquer círculo
  resolve(p, rad) {
    const cx = Math.floor(p.x / 16);
    const cz = Math.floor(p.z / 16);
    for (let i = -1; i <= 1; i++) {
      for (let j = -1; j <= 1; j++) {
        const list = this.cells.get(`${cx + i},${cz + j}`);
        if (!list) continue;
        for (const [x, z, r] of list) {
          const dx = p.x - x;
          const dz = p.z - z;
          const d = Math.hypot(dx, dz);
          const m = r + rad;
          if (d < m && d > 1e-4) {
            p.x = x + (dx / d) * m;
            p.z = z + (dz / d) * m;
          }
        }
      }
    }
  }
}

