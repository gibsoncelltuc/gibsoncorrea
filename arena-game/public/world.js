// Mundo aberto: terreno, água, céu com dia/noite, vegetação e as construções de cada região.
// Tudo procedural. Geometrias estáticas são fundidas (poucas chamadas de desenho) e a vegetação é instanciada por "chunks".
import * as THREE from 'three';
import { Merge, vcMat, Instancer, Colliders, rnd, TAU } from './buildutil.js';
import { buildNpc } from './avatar.js';
import { LOCATIONS, LAKES, SEA_LEVEL, CRYSTALS, WORLD_HALF, BLOCK, heightAt, biomeWeights, roadDist, smooth, colCenter, colOf } from './shared/world.js';
import { buildTerrain, voxelGeometry, makeAtlas, TILE } from './voxel.js';
import { buildStructures } from './structures.js';

export function buildOpenWorld(scene, fx) {
  const root = new THREE.Group();
  scene.add(root);
  const upd = [];
  const col = new Colliders();
  const timeU = { value: 0 };
  const api = { root, col, npcs: [], crystals: [], lights: [], windowMats: [], fx, tod: 0.3 };
  const horizon = new THREE.Color('#ffe6c8');
  scene.fog = new THREE.Fog(horizon, 90, 520);

  // ---------- céu com dia/noite ----------
  const skyU = { sun: { value: new THREE.Vector3(0.5, 0.6, 0.3) }, day: { value: 1 } };
  const sky = new THREE.Mesh(
    new THREE.SphereGeometry(900, 32, 16),
    new THREE.ShaderMaterial({
      side: THREE.BackSide,
      depthWrite: false,
      fog: false,
      uniforms: skyU,
      vertexShader: 'varying vec3 vP; void main(){ vP = position; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
      fragmentShader: `varying vec3 vP; uniform vec3 sun; uniform float day;
        float h21(vec2 p){ return fract(sin(dot(p, vec2(127.1,311.7))) * 43758.5453); }
        void main(){ vec3 d = normalize(vP); float h = clamp(d.y, -0.1, 1.0);
          vec3 top = mix(vec3(0.02,0.04,0.14), vec3(0.20,0.48,0.95), day); vec3 mid = mix(vec3(0.05,0.08,0.22), vec3(0.55,0.78,1.0), day); vec3 hor = mix(vec3(0.10,0.12,0.26), vec3(1.0,0.90,0.78), day);
          vec3 c = mix(hor, mid, smoothstep(0.0, 0.25, h)); c = mix(c, top, smoothstep(0.2, 0.9, h));
          vec3 sn = normalize(sun); float s = max(dot(d, sn), 0.0); c += vec3(1.0,0.8,0.5) * pow(s, 12.0) * 0.4 * day;
          vec3 t1 = normalize(cross(sn, vec3(0.0,0.0,1.0))); vec3 t2 = cross(sn, t1);
          if (dot(d, sn) > 0.0) { vec2 q = vec2(dot(d, t1), dot(d, t2)) / dot(d, sn); if (max(abs(q.x), abs(q.y)) < 0.07) c = mix(c, vec3(1.0,0.97,0.8), day); }
          if (dot(d, -sn) > 0.0) { vec2 q = vec2(dot(d, t1), dot(d, t2)) / dot(d, -sn); if (max(abs(q.x), abs(q.y)) < 0.05) c = mix(c, vec3(0.9,0.93,1.0), 1.0 - day); }
          vec2 g = floor(d.xz / (d.y + 1.2) * 90.0); float st = step(0.9965, h21(g)) * (1.0 - day) * smoothstep(0.05, 0.3, h); c += vec3(st);
          gl_FragColor = vec4(c, 1.0); }`,
    }),
  );
  root.add(sky);
  const hemi = new THREE.HemisphereLight('#bfe0ff', '#6a8a52', 1.1);
  root.add(hemi);
  const sun = new THREE.DirectionalLight('#fff0d0', 2.4);
  sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -70, right: 70, top: 70, bottom: -70, near: 1, far: 260 });
  sun.shadow.bias = -0.0004;
  sun.shadow.normalBias = 0.05;
  root.add(sun, sun.target);
  const moon = new THREE.DirectionalLight('#8fa8ff', 0);
  root.add(moon, moon.target);

  // ---------- terreno de blocos ----------
  const SZ = WORLD_HALF * 2 + 140;
  buildTerrain(root);
  const WATER_Y = -2.2; // um pouco abaixo do topo dos blocos de areia na beira
  // ---------- água ----------
  const water = new THREE.Mesh(new THREE.PlaneGeometry(SZ + 400, SZ + 400), new THREE.MeshStandardMaterial({ color: '#3a6fe0', roughness: 0.25, metalness: 0.05, transparent: true, opacity: 0.78 }));
  water.rotation.x = -Math.PI / 2;
  water.position.y = WATER_Y;
  water.receiveShadow = true;
  root.add(water);
  upd.push((t) => (water.material.opacity = 0.76 + Math.sin(t * 1.2) * 0.04));
  // lagos congelados: placas de gelo em blocos, caminháveis
  for (const k of LAKES) {
    if (!k.ice) continue;
    const m = new Merge();
    for (let cx = colOf(k.x - k.r - 4); cx <= colOf(k.x + k.r + 4); cx++) {
      for (let cz = colOf(k.z - k.r - 4); cz <= colOf(k.z + k.r + 4); cz++) {
        const x = colCenter(cx);
        const z = colCenter(cz);
        if (Math.hypot(x - k.x, z - k.z) < k.r + 2) m.box(BLOCK, 0.5, BLOCK, (cx + cz) % 2 ? '#b9e2fb' : '#a8d8f5', { x, y: WATER_Y + 0.15, z });
      }
    }
    const ice = m.mesh(vcMat({ roughness: 0.2, transparent: true, opacity: 0.9 }), { cast: false });
    root.add(ice);
    col.walk.push({ x: k.x, z: k.z, r: k.r + 2, y: WATER_Y + 0.4 });
  }

  // ---------- nuvens ----------
  const clouds = [];
  const cloudMat = new THREE.MeshBasicMaterial({ color: '#ffffff', fog: false });
  const cloudGeo = new THREE.BoxGeometry(1, 1, 1);
  for (let i = 0; i < 34; i++) {
    const c = new THREE.Group();
    const n = 5 + Math.floor(Math.random() * 6);
    for (let k = 0; k < n; k++) {
      const s = new THREE.Mesh(cloudGeo, cloudMat);
      s.scale.set(12 * (1 + Math.floor(Math.random() * 2)), 4, 12 * (1 + Math.floor(Math.random() * 2)));
      s.position.set(Math.round(Math.random() * 4 - 2) * 12, 0, Math.round(Math.random() * 3 - 1.5) * 12);
      c.add(s);
    }
    const a = Math.random() * TAU;
    const d = rnd(60, 380);
    c.userData = { a, d, y: rnd(95, 150), sp: rnd(0.002, 0.007) };
    root.add(c);
    clouds.push(c);
  }
  upd.push((_t, dt) => {
    for (const c of clouds) {
      c.userData.a += c.userData.sp * dt;
      c.position.set(Math.cos(c.userData.a) * c.userData.d, c.userData.y, Math.sin(c.userData.a) * c.userData.d);
    }
    const day = skyU.day.value;
    cloudMat.color.setRGB(0.25 + 0.75 * day, 0.27 + 0.73 * day, 0.4 + 0.6 * day);
  });

  // ---------- estruturas e vegetação ----------
  const ctx = { root, col, api, upd, rnd, TAU, timeU };
  buildStructures(ctx);
  buildVegetation(ctx);

  // ---------- NPCs ----------
  api.npcDefs = [
    { id: 'mayor', kind: 'mayor', x: LOCATIONS.mayor.x, z: LOCATIONS.mayor.z, yaw: Math.PI },
    { id: 'smith', kind: 'smith', x: -19, z: -9, yaw: 1.2 },
    { id: 'farmer', kind: 'farmer', x: -96, z: 120, yaw: 0.6 },
    { id: 'guard1', kind: 'guard', x: LOCATIONS.colosseum.x - 36, z: LOCATIONS.colosseum.z - 4, yaw: -Math.PI / 2 },
    { id: 'guard2', kind: 'guard', x: LOCATIONS.colosseum.x - 36, z: LOCATIONS.colosseum.z + 4, yaw: -Math.PI / 2 },
    { id: 'kid', kind: 'kid', x: 12, z: 8, yaw: 2.4 },
  ];
  let items = null;
  api.spawnNpcs = (catalogItems) => {
    items = catalogItems;
    for (const d of api.npcDefs) {
      const { rig, name } = buildNpc(d.kind, items);
      rig.root.position.set(d.x, heightAt(d.x, d.z), d.z);
      rig.root.rotation.y = d.yaw;
      root.add(rig.root);
      api.npcs.push({ ...d, rig, name });
      col.add(d.x, d.z, 0.7);
    }
  };

  // ---------- cristais coletáveis ----------
  const crystalGeo = new THREE.OctahedronGeometry(0.7, 0);
  for (const c of CRYSTALS) {
    const m = new THREE.Mesh(crystalGeo, new THREE.MeshStandardMaterial({ color: '#7fe8ff', emissive: '#2ac8ff', emissiveIntensity: 1.8, roughness: 0.15, transparent: true, opacity: 0.92 }));
    m.scale.y = 1.6;
    m.castShadow = true;
    m.position.set(c.x, heightAt(c.x, c.z) + 1.3, c.z);
    root.add(m);
    api.crystals.push({ ...c, mesh: m, taken: false });
  }
  upd.push((t) => {
    for (const c of api.crystals) {
      if (c.taken) continue;
      c.mesh.rotation.y = t * 1.5;
      c.mesh.position.y = heightAt(c.x, c.z) + 1.3 + Math.sin(t * 2 + c.x) * 0.2;
    }
  });

  // ---------- altura do chão e movimento ----------
  api.groundY = (x, z) => {
    let y = heightAt(x, z);
    for (const w of col.walk) {
      if (w.rect ? x >= w.x0 && x <= w.x1 && z >= w.z0 && z <= w.z1 : Math.hypot(x - w.x, z - w.z) <= w.r) y = Math.max(y, w.y);
    }
    return y;
  };
  api.isDeepWater = (x, z) => api.groundY(x, z) < SEA_LEVEL - 0.9;

  // ---------- ciclo dia/noite ----------
  api.setTime = (tod) => {
    api.tod = tod;
    const a = tod * TAU;
    const dir = new THREE.Vector3(Math.cos(a) * 0.85, Math.sin(a), 0.38).normalize();
    const dayK = smooth(-0.12, 0.22, dir.y);
    skyU.sun.value.copy(dir);
    skyU.day.value = dayK;
    sun.intensity = 2.4 * dayK;
    moon.intensity = 0.55 * (1 - dayK);
    hemi.intensity = 0.18 + 0.95 * dayK;
    hemi.color.set('#bfe0ff').lerp(new THREE.Color('#2a3a7a'), 1 - dayK);
    hemi.groundColor.set('#6a8a52').lerp(new THREE.Color('#10142a'), 1 - dayK);
    sun.color.set('#fff0d0').lerp(new THREE.Color('#ff9a5a'), smooth(0.35, 0.05, dir.y) * dayK);
    scene.fog.color.set('#ffe6c8').lerp(new THREE.Color('#0c1230'), 1 - dayK);
    water.material.color.set('#3aa8e0').lerp(new THREE.Color('#10305a'), 1 - dayK);
    for (const m of api.windowMats) m.emissiveIntensity = 2.2 * (1 - dayK) + 0.05;
    api.dayK = dayK;
    api.sunDir = dir;
  };
  api.update = (t, dt, playerPos) => {
    timeU.value = t;
    api.setTime((api.tod + dt / 720) % 1); // um dia inteiro = 12 minutos
    sky.position.copy(playerPos);
    sun.position.copy(playerPos).addScaledVector(api.sunDir, 90);
    sun.target.position.copy(playerPos);
    moon.position.copy(playerPos).addScaledVector(api.sunDir, -90);
    moon.target.position.copy(playerPos);
    for (const f of upd) f(t, dt, playerPos);
  };
  api.setTime(api.tod);
  return api;
}

// ---------- vegetação por bioma ----------
function buildVegetation(ctx) {
  const { root, col, rnd } = ctx;
  const M = (...a) => a;
  void M;
  const mk = (fn) => {
    const m = new Merge();
    fn(m);
    return m.geometry();
  };
  const T = TILE;
  const logCol = (k) => [0.92 + (k % 2) * 0.1, 0.92 + (k % 2) * 0.1, 0.92 + (k % 2) * 0.1];
  const leafLayer = (y, w, tile, tint, skipCorners = true, seed = 0) => {
    const out = [];
    const h = (w - 1) / 2;
    for (let i = -h; i <= h; i++) {
      for (let k = -h; k <= h; k++) {
        if (skipCorners && w >= 5 && Math.abs(i) === h && Math.abs(k) === h && (i * 3 + k * 5 + seed) % 2 === 0) continue;
        const j = 0.85 + (((i * 7 + k * 13 + y * 5 + seed) % 5) / 5) * 0.3;
        out.push([i, y, k, tile, { col: [tint[0] * j, tint[1] * j, tint[2] * j] }]);
      }
    }
    return out;
  };
  const trunk = (h, tile) => Array.from({ length: h }, (_, j) => [0, j, 0, { side: tile, top: T.logTop, bottom: T.logTop }, { col: logCol(j) }]);
  const geo = {
    oak: voxelGeometry([...trunk(4, T.log), ...leafLayer(3, 5, T.leaves, [0.85, 1, 0.8]).filter((b) => !(b[0] === 0 && b[2] === 0)), ...leafLayer(4, 5, T.leaves, [0.9, 1, 0.85], true, 1), ...leafLayer(5, 3, T.leaves, [0.95, 1.05, 0.9]), ...leafLayer(6, 1, T.leaves, [1, 1.1, 0.9])]),
    oakBig: voxelGeometry([...trunk(6, T.log), ...leafLayer(4, 7, T.leaves, [0.8, 0.95, 0.75], true, 2).filter((b) => !(b[0] === 0 && b[2] === 0)), ...leafLayer(5, 7, T.leaves, [0.85, 1, 0.8], true, 3).filter((b) => !(b[0] === 0 && b[2] === 0)), ...leafLayer(6, 5, T.leaves, [0.9, 1.05, 0.85], true, 4), ...leafLayer(7, 3, T.leaves, [1, 1.1, 0.9])]),
    birch: voxelGeometry([...trunk(5, T.birchLog), ...leafLayer(3, 5, T.leaves, [1.05, 1.25, 0.8]).filter((b) => !(b[0] === 0 && b[2] === 0)), ...leafLayer(4, 5, T.leaves, [1.1, 1.3, 0.85], true, 1).filter((b) => !(b[0] === 0 && b[2] === 0)), ...leafLayer(5, 3, T.leaves, [1.1, 1.3, 0.85]), ...leafLayer(6, 1, T.leaves, [1.15, 1.35, 0.9])]),
    pine: voxelGeometry([...trunk(6, T.log), ...leafLayer(2, 5, T.leaves, [0.45, 0.75, 0.55], true).filter((b) => !(b[0] === 0 && b[2] === 0)), ...leafLayer(3, 3, T.leaves, [0.5, 0.8, 0.6]).filter((b) => !(b[0] === 0 && b[2] === 0)), ...leafLayer(4, 5, T.leaves, [0.45, 0.75, 0.55]).filter((b) => !(b[0] === 0 && b[2] === 0)), ...leafLayer(5, 3, T.leaves, [0.5, 0.8, 0.6]).filter((b) => !(b[0] === 0 && b[2] === 0)), ...leafLayer(6, 3, T.leaves, [0.5, 0.82, 0.62]).filter((b) => !(b[0] === 0 && b[2] === 0)), ...leafLayer(7, 1, T.leaves, [0.55, 0.85, 0.65])]),
    snowpine: voxelGeometry([...trunk(6, T.log), ...leafLayer(2, 5, T.leaves, [0.4, 0.7, 0.55]).filter((b) => !(b[0] === 0 && b[2] === 0)), ...leafLayer(3, 3, T.snow, [1, 1, 1]).filter((b) => !(b[0] === 0 && b[2] === 0)), ...leafLayer(4, 5, T.leaves, [0.4, 0.7, 0.55]).filter((b) => !(b[0] === 0 && b[2] === 0)), ...leafLayer(5, 3, T.snow, [1, 1, 1]).filter((b) => !(b[0] === 0 && b[2] === 0)), ...leafLayer(6, 3, T.leaves, [0.45, 0.75, 0.6]).filter((b) => !(b[0] === 0 && b[2] === 0)), ...leafLayer(7, 1, T.snow, [1, 1, 1])]),
    palm: voxelGeometry([[0, 0, 0, T.log], [0, 1, 0, T.log], [0, 2, 0, T.log], [1, 3, 0, T.log], [1, 4, 0, T.log], [1, 5, 0, T.log], ...[[1, 6, 0], [2, 6, 0], [3, 5, 0], [0, 6, 0], [-1, 5, 0], [1, 6, 1], [1, 5, 2], [1, 6, -1], [1, 5, -2], [2, 7, 0], [0, 7, 0], [1, 7, 1], [1, 7, -1]].map(([i, j, k]) => [i, j, k, T.leaves, { col: [0.75, 1.15, 0.75] }])]),
    cactus: voxelGeometry([[0, 0, 0, T.cactus], [0, 1, 0, T.cactus], [0, 2, 0, T.cactus], [1, 1, 0, T.cactus], [1, 2, 0, T.cactus]]),
    cactusSmall: voxelGeometry([[0, 0, 0, T.cactus], [0, 1, 0, T.cactus]]),
    dead: voxelGeometry([[0, 0, 0, T.log, { col: [0.6, 0.55, 0.5] }], [0, 1, 0, T.log, { col: [0.6, 0.55, 0.5] }], [0, 2, 0, T.log, { col: [0.6, 0.55, 0.5] }], [1, 2, 0, T.log, { col: [0.6, 0.55, 0.5] }], [-1, 3, 0, T.log, { col: [0.6, 0.55, 0.5] }], [0, 3, 0, T.log, { col: [0.6, 0.55, 0.5] }]]),
    rock: voxelGeometry([[0, 0, 0, T.stone], [1, 0, 0, T.stone], [0, 0, 1, T.cobble], [0, 1, 0, T.stone], [-1, 0, 0, T.stone, { s: [1, 0.5, 1] }]]),
    bush: voxelGeometry([[0, 0, 0, T.leaves, { col: [0.8, 1, 0.8] }], [1, 0, 0, T.leaves, { col: [0.9, 1.05, 0.85], s: [1, 0.5, 1] }]]),
    flower: voxelGeometry([[0, 0, 0, T.leaves, { s: [0.12, 0.55, 0.12], col: [0.5, 1, 0.5] }], [0, 0, 0, T.snow, { s: [0.4, 0.2, 0.4], col: [1, 1, 1] }]].map((b, n) => (n === 1 ? [0, 0, 0, T.snow, { s: [0.45, 0.2, 0.45], col: [1, 1, 1] }] : b))),
    tuft: voxelGeometry([[0, 0, 0, T.tuft, { cross: true, s: [0.9, 0.5, 1] }]]),
    mushroom: voxelGeometry([[0, 0, 0, T.birchLog, { s: [0.2, 0.3, 0.2] }], [0, 0, 0, T.magma, { s: [0.5, 0.25, 0.5], col: [0.6, 0.2, 0.2] }]]),
    cactusSmall2: null,
  };
  delete geo.cactusSmall2;
  const FL = [[1, 0.35, 0.5], [1, 0.85, 0.2], [1, 1, 1], [0.45, 0.6, 1], [1, 0.6, 0.2], [0.75, 0.5, 1]];
  FL.forEach((c, n) => (geo['flower' + n] = voxelGeometry([[0, 0, 0, T.leaves, { s: [0.12, 0.5, 0.12], col: [0.5, 1, 0.5] }], [0, 0.5, 0, T.snow, { s: [0.42, 0.22, 0.42], col: c }]])));
  const atlas = makeAtlas();
  const mat = new THREE.MeshStandardMaterial({ map: atlas, vertexColors: true, roughness: 1 });
  const swayMat = new THREE.MeshStandardMaterial({ map: atlas, vertexColors: true, roughness: 1, alphaTest: 0.5, side: THREE.DoubleSide });
  swayMat.onBeforeCompile = (s) => {
    s.uniforms.uTime = ctx.timeU;
    s.vertexShader = 'uniform float uTime;\n' + s.vertexShader.replace('#include <begin_vertex>', `#include <begin_vertex>
      float sw = sin(uTime * 1.8 + instanceMatrix[3].x * 0.45 + instanceMatrix[3].z * 0.37) * 0.12 * position.y;
      transformed.x += sw; transformed.z += sw * 0.6;`);
  };
  const I = Object.fromEntries(Object.entries(geo).map(([k, g]) => [k, new Instancer(g, k === 'tuft' ? swayMat : mat, { cast: !(k.startsWith('flower') || k === 'tuft' || k === 'mushroom') })]));
  const tint = ['#ffffff', '#f2fff0', '#e8ffe0', '#fff4e0'];
  const flowerCols = ['#ff6b8b', '#ffd24a', '#ffffff', '#8fb6ff', '#ff9a4a', '#c08bff'];
  const ok = (x, z, minH = SEA_LEVEL + 0.6) => {
    const h = heightAt(x, z);
    if (h < minH || h > 15) return false;
    if (roadDist(x, z) < 5) return false;
    for (const k of LAKES) if (Math.hypot(x - k.x, z - k.z) < k.r + 6) return false;
    if (Math.hypot(x - LOCATIONS.town.x, z - LOCATIONS.town.z) < 66) return false;
    if (Math.hypot(x - LOCATIONS.colosseum.x, z - LOCATIONS.colosseum.z) < 40) return false;
    if (Math.hypot(x - LOCATIONS.castle.x, z - LOCATIONS.castle.z) < 66) return false;
    for (const c of ctx.api.crystals ?? []) if (Math.hypot(x - c.x, z - c.z) < 4) return false;
    return !(ctx.keepout ?? []).some((k) => Math.hypot(x - k.x, z - k.z) < k.r);
  };
  const place = (kind, x, z, s, color, r) => {
    if (kind === 'oak') {
      const q = Math.random();
      kind = q < 0.6 ? 'oak' : q < 0.82 ? 'oakBig' : 'birch';
    }
    if (kind === 'flower') kind = 'flower' + Math.floor(Math.random() * 6);
    x = colCenter(colOf(x));
    z = colCenter(colOf(z));
    I[kind].add(x, heightAt(x, z) - 0.05, z, 0, 1, color);
    if (r) col.add(x, z, 1.15);
  };
  const N = 6500;
  for (let i = 0; i < N; i++) {
    const x = rnd(-WORLD_HALF + 8, WORLD_HALF - 8);
    const z = rnd(-WORLD_HALF + 8, WORLD_HALF - 8);
    const w = biomeWeights(x, z);
    const dom = Object.entries(w).sort((a, b) => b[1] - a[1])[0];
    const b = dom[1] > 0.4 ? dom[0] : 'grass';
    if (b === 'town') continue;
    if (!ok(x, z)) continue;
    const r = Math.random();
    if (b === 'forest') {
      if (r < 0.55) place(r < 0.3 ? 'oak' : 'pine', x, z, rnd(0.9, 1.7), tint[i % 4], 0.5);
      else if (r < 0.7) place('bush', x, z, rnd(0.8, 1.4), null);
      else if (r < 0.78) place('mushroom', x, z, rnd(0.8, 1.6), null);
      else if (r < 0.84) place('rock', x, z, rnd(0.6, 1.6), null, 0.9);
    } else if (b === 'snow') {
      if (r < 0.4) place('snowpine', x, z, rnd(0.9, 1.7), null, 0.5);
      else if (r < 0.46) place('rock', x, z, rnd(0.8, 2.0), '#cfd8e6', 0.9);
    } else if (b === 'desert') {
      if (r < 0.1) place('cactus', x, z, rnd(0.8, 1.5), null, 0.6);
      else if (r < 0.2) place('cactusSmall', x, z, rnd(0.8, 1.4), null);
      else if (r < 0.24) place('dead', x, z, rnd(0.8, 1.3), null, 0.4);
      else if (r < 0.28) place('rock', x, z, rnd(0.7, 1.8), '#d8b887', 0.9);
    } else if (b === 'beach') {
      if (r < 0.1) place('palm', x, z, rnd(0.9, 1.3), null, 0.4);
      else if (r < 0.14) place('rock', x, z, rnd(0.6, 1.5), '#cfc7b0', 0.8);
    } else if (b === 'farm') {
      if (r < 0.04) place('oak', x, z, rnd(1, 1.5), tint[i % 4], 0.5);
      else if (r < 0.2) place('flower', x, z, rnd(0.8, 1.4), flowerCols[i % 6]);
    } else if (b === 'ruins') {
      if (r < 0.1) place('dead', x, z, rnd(0.9, 1.4), null, 0.4);
      else if (r < 0.22) place('rock', x, z, rnd(0.8, 2.2), '#b4b9a4', 0.9);
    } else if (b === 'castle') {
      if (r < 0.06) place('pine', x, z, rnd(0.9, 1.4), null, 0.5);
      else if (r < 0.12) place('rock', x, z, rnd(0.8, 2.4), '#aeb4bd', 0.9);
    } else {
      if (r < 0.06) place('oak', x, z, rnd(0.9, 1.8), tint[i % 4], 0.5);
      else if (r < 0.1) place('bush', x, z, rnd(0.8, 1.4), null);
      else if (r < 0.2) place('flower', x, z, rnd(0.8, 1.4), flowerCols[i % 6]);
      else if (r < 0.23) place('rock', x, z, rnd(0.6, 1.5), null, 0.9);
    }
  }
  // grama ao vento (só onde o chão é verde)
  for (let i = 0; i < 14000; i++) {
    const x = rnd(-WORLD_HALF, WORLD_HALF);
    const z = rnd(-WORLD_HALF, WORLD_HALF);
    const w = biomeWeights(x, z);
    if (w.desert > 0.3 || w.snow > 0.3 || w.beach > 0.4 || w.castle > 0.5) continue;
    if (!ok(x, z, 0.1) || Math.hypot(x, z) < 70) continue;
    I.tuft.add(x, heightAt(x, z) - 0.05, z, Math.random() * TAU, rnd(0.9, 1.3), ['#ffffff', '#e8ffe0', '#d8f8c8'][i % 3], rnd(0.8, 1.3));
  }
  // miolo da vila: flores, arbustos e algumas árvores entre as casas (longe de estradas e construções)
  for (let i = 0; i < 1800; i++) {
    const a = Math.random() * TAU;
    const d = 18 + Math.random() * 56;
    const x = Math.cos(a) * d;
    const z = Math.sin(a) * d;
    if (roadDist(x, z) < 6 || (ctx.keepout ?? []).some((k) => Math.hypot(x - k.x, z - k.z) < k.r)) continue;
    if (Math.hypot(x - LOCATIONS.colosseum.x, z - LOCATIONS.colosseum.z) < 40) continue;
    const r = Math.random();
    if (r < 0.62) I['flower' + (i % 6)].add(colCenter(colOf(x)) + rnd(-0.6, 0.6), heightAt(x, z) - 0.05, colCenter(colOf(z)) + rnd(-0.6, 0.6), 0, 1, null);
    else if (r < 0.82) place('bush', x, z, rnd(0.7, 1.2), null);
    else if (r < 0.9) place('oak', x, z, rnd(0.8, 1.3), tint[i % 4], 0.5);
    else I.tuft.add(x, heightAt(x, z) - 0.05, z, Math.random() * TAU, rnd(0.7, 1.2), '#e8ffe0', rnd(0.8, 1.3));
  }
  for (const i of Object.values(I)) i.build(root);
}
