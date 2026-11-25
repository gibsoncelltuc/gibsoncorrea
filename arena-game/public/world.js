// Mundo aberto: terreno, água, céu com dia/noite, vegetação e as construções de cada região.
// Tudo procedural. Geometrias estáticas são fundidas (poucas chamadas de desenho) e a vegetação é instanciada por "chunks".
import * as THREE from 'three';
import { Merge, vcMat, Instancer, Colliders, rnd, TAU } from './buildutil.js';
import { buildNpc } from './avatar.js';
import { LOCATIONS, LAKES, SEA_LEVEL, CRYSTALS, WORLD_HALF, ROADS, heightAt, biomeWeights, roadDist, smooth } from './shared/world.js';
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
          float s = max(dot(d, normalize(sun)), 0.0); c += vec3(1.0,0.8,0.5) * pow(s, 12.0) * 0.55 * day; c += vec3(1.0,0.97,0.85) * smoothstep(0.9975, 0.9985, s) * day;
          float m = max(dot(d, normalize(-sun)), 0.0); c += vec3(0.8,0.85,1.0) * smoothstep(0.9985, 0.9992, m) * (1.0 - day);
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

  // ---------- terreno ----------
  const SZ = WORLD_HALF * 2 + 140;
  const tg = new THREE.PlaneGeometry(SZ, SZ, 250, 250);
  tg.rotateX(-Math.PI / 2);
  const pa = tg.attributes.position;
  const colors = new Float32Array(pa.count * 3);
  const C = (h) => new THREE.Color(h);
  const cGrass = C('#7ed35e');
  const cGrass2 = C('#5fb855');
  const cSand = C('#ecd391');
  const cSnow = C('#f4f9ff');
  const cForest = C('#3f9a4a');
  const cFarm = C('#a5d85f');
  const cRock = C('#8e96a3');
  const cRoad = C('#cdb07a');
  const cCastle = C('#8aa06a');
  const cRuins = C('#8fa17a');
  const cBeach = C('#f3e2a8');
  const cUnder = C('#cbb98a');
  const tmp = new THREE.Color();
  for (let i = 0; i < pa.count; i++) {
    const x = pa.getX(i);
    const z = pa.getZ(i);
    const h = heightAt(x, z);
    pa.setY(i, h);
    const w = biomeWeights(x, z);
    tmp.copy(cGrass).lerp(cGrass2, 0.5 + 0.5 * Math.sin(x * 0.07) * Math.cos(z * 0.06));
    tmp.lerp(cForest, w.forest * 0.9);
    tmp.lerp(cFarm, w.farm * 0.8);
    tmp.lerp(cSand, w.desert);
    tmp.lerp(cSnow, w.snow);
    tmp.lerp(cBeach, w.beach * 0.9);
    tmp.lerp(cCastle, w.castle * 0.6);
    tmp.lerp(cRuins, w.ruins * 0.7);
    tmp.lerp(cRock, smooth(11, 20, h) * 0.9);
    tmp.lerp(cSnow, smooth(24, 34, h));
    if (h < SEA_LEVEL + 0.9) tmp.lerp(cBeach, 0.85);
    if (h < SEA_LEVEL - 0.4) tmp.lerp(cUnder, 0.9);
    const rd = roadDist(x, z);
    if (rd < 3.4 && h > SEA_LEVEL) tmp.lerp(cRoad, smooth(3.4, 1.8, rd));
    colors.set([tmp.r, tmp.g, tmp.b], i * 3);
  }
  tg.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  tg.computeVertexNormals();
  const terrain = new THREE.Mesh(tg, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.95 }));
  terrain.receiveShadow = true;
  root.add(terrain);

  // ---------- água ----------
  const water = new THREE.Mesh(new THREE.PlaneGeometry(SZ + 400, SZ + 400), new THREE.MeshStandardMaterial({ color: '#3aa8e0', roughness: 0.08, metalness: 0.15, transparent: true, opacity: 0.82 }));
  water.rotation.x = -Math.PI / 2;
  water.position.y = SEA_LEVEL;
  water.receiveShadow = true;
  root.add(water);
  upd.push((t) => (water.material.opacity = 0.8 + Math.sin(t * 1.2) * 0.04));
  for (const k of LAKES) {
    if (!k.ice) continue;
    const ice = new THREE.Mesh(new THREE.CircleGeometry(k.r + 3, 40), new THREE.MeshStandardMaterial({ color: '#d4ecff', roughness: 0.12, metalness: 0.1 }));
    ice.rotation.x = -Math.PI / 2;
    ice.position.set(k.x, SEA_LEVEL + 0.3, k.z);
    ice.receiveShadow = true;
    root.add(ice);
    col.walk.push({ x: k.x, z: k.z, r: k.r + 2, y: SEA_LEVEL + 0.35 });
  }

  // ---------- nuvens ----------
  const clouds = [];
  const cloudMat = new THREE.MeshBasicMaterial({ color: '#ffffff', fog: false });
  for (let i = 0; i < 26; i++) {
    const c = new THREE.Group();
    const n = 4 + Math.floor(Math.random() * 3);
    for (let k = 0; k < n; k++) {
      const s = new THREE.Mesh(new THREE.SphereGeometry(rnd(6, 11), 12, 9), cloudMat);
      s.position.set(k * 7 - n * 3.5 + rnd(-2, 2), rnd(-1.5, 2), rnd(-3, 3));
      s.scale.y = 0.55;
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
  const geo = {
    oak: mk((m) => {
      m.cyl(0.35, 0.55, 3, '#7a5233', { y: 1.5 }, 7);
      for (const [x, y, z, s] of [[0, 4.2, 0, 2.1], [0.9, 3.5, 0.5, 1.5], [-0.9, 3.6, -0.4, 1.6], [0.1, 5.2, -0.3, 1.4]]) m.ball(s, y > 4 ? '#6fcf5f' : '#4aa84f', { x, y, z, sy: 0.85 }, 9);
    }),
    pine: mk((m) => {
      m.cyl(0.3, 0.5, 2.4, '#6b4a2b', { y: 1.2 }, 6);
      for (let k = 0; k < 4; k++) m.cone(2.4 - k * 0.5, 2.6, k % 2 ? '#2f7a4a' : '#357f50', { y: 3 + k * 1.4 }, 8);
    }),
    snowpine: mk((m) => {
      m.cyl(0.3, 0.5, 2.4, '#6b4a2b', { y: 1.2 }, 6);
      for (let k = 0; k < 4; k++) {
        m.cone(2.4 - k * 0.5, 2.6, '#2f6a52', { y: 3 + k * 1.4 }, 8);
        m.cone(1.8 - k * 0.42, 1.2, '#f4f9ff', { y: 3.5 + k * 1.4 }, 8);
      }
    }),
    palm: mk((m) => {
      for (let k = 0; k < 6; k++) m.cyl(0.28 - k * 0.02, 0.32 - k * 0.02, 1.2, '#a8814f', { x: k * 0.12, y: 0.6 + k * 1.15 }, 7);
      for (let k = 0; k < 7; k++) {
        const a = (k / 7) * TAU;
        m.cone(0.45, 3.4, '#3fb25a', { x: 0.7 + Math.cos(a) * 1.4, y: 7.1, z: Math.sin(a) * 1.4, rz: -Math.cos(a) * 1.2, rx: Math.sin(a) * 1.2 }, 4);
      }
      m.ball(0.3, '#7a5233', { x: 0.75, y: 6.9 }, 6);
    }),
    cactus: mk((m) => {
      m.cyl(0.5, 0.55, 4, '#4f9a55', { y: 2 }, 8);
      m.ball(0.5, '#4f9a55', { y: 4 }, 8);
      m.cyl(0.3, 0.3, 1.6, '#4f9a55', { x: 0.9, y: 2.2, rz: 0 }, 8);
      m.cyl(0.3, 0.3, 1.2, '#4f9a55', { x: 0.55, y: 1.6, rz: 1.5708 }, 8);
      m.cyl(0.28, 0.28, 1.2, '#4f9a55', { x: -0.9, y: 2.8 }, 8);
      m.cyl(0.28, 0.28, 1.0, '#4f9a55', { x: -0.55, y: 2.2, rz: 1.5708 }, 8);
    }),
    dead: mk((m) => {
      m.cyl(0.25, 0.5, 4, '#5a4636', { y: 2 }, 6);
      m.cyl(0.12, 0.2, 2.2, '#5a4636', { x: 0.8, y: 3.2, rz: -0.9 }, 5);
      m.cyl(0.1, 0.18, 1.8, '#5a4636', { x: -0.7, y: 3.6, rz: 0.9 }, 5);
    }),
    rock: mk((m) => m.add(new THREE.DodecahedronGeometry(1, 0), '#9aa3b0', { sy: 0.7 })),
    bush: mk((m) => {
      m.ball(1.0, '#3f9548', { y: 0.7, sy: 0.8 }, 8);
      m.ball(0.7, '#4aa84f', { x: 0.7, y: 0.5, sy: 0.8 }, 8);
    }),
    flower: mk((m) => {
      m.cyl(0.03, 0.03, 0.5, '#3f9548', { y: 0.25 }, 4);
      m.ball(0.17, '#ffffff', { y: 0.55 }, 6);
    }),
    tuft: mk((m) => {
      for (let k = 0; k < 5; k++) m.cone(0.07, 0.8 + (k % 3) * 0.12, k % 2 ? '#7fdc62' : '#5fc15a', { x: (k - 2) * 0.1, y: 0.4, z: ((k * 7) % 3 - 1) * 0.06, rz: (k - 2) * 0.16 }, 3);
    }),
    mushroom: mk((m) => {
      m.cyl(0.12, 0.16, 0.5, '#f2ead8', { y: 0.25 }, 6);
      m.ball(0.38, '#d8404f', { y: 0.55, sy: 0.6 }, 8);
    }),
    cactusSmall: mk((m) => {
      m.cyl(0.3, 0.34, 1.6, '#5aa860', { y: 0.8 }, 7);
      m.ball(0.3, '#5aa860', { y: 1.6 }, 7);
    }),
  };
  const mat = vcMat();
  const swayMat = vcMat({ roughness: 1 });
  swayMat.onBeforeCompile = (s) => {
    s.uniforms.uTime = ctx.timeU;
    s.vertexShader = 'uniform float uTime;\n' + s.vertexShader.replace('#include <begin_vertex>', `#include <begin_vertex>
      float sw = sin(uTime * 1.8 + instanceMatrix[3].x * 0.45 + instanceMatrix[3].z * 0.37) * 0.18 * position.y;
      transformed.x += sw; transformed.z += sw * 0.6;`);
  };
  const I = Object.fromEntries(Object.entries(geo).map(([k, g]) => [k, new Instancer(g, k === 'tuft' ? swayMat : mat, { cast: !['flower', 'tuft', 'mushroom'].includes(k) })]));
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
    I[kind].add(x, heightAt(x, z) - 0.1, z, Math.random() * TAU, s, color);
    if (r) col.add(x, z, r * s);
  };
  const N = 9000;
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
  for (let i = 0; i < 52000; i++) {
    const x = rnd(-WORLD_HALF, WORLD_HALF);
    const z = rnd(-WORLD_HALF, WORLD_HALF);
    const w = biomeWeights(x, z);
    if (w.desert > 0.3 || w.snow > 0.3 || w.beach > 0.4 || w.castle > 0.5) continue;
    if (!ok(x, z, 0.1) || Math.hypot(x, z) < 70) continue;
    I.tuft.add(x, heightAt(x, z) - 0.05, z, Math.random() * TAU, rnd(0.6, 1.2), ['#ffffff', '#e8ffe0', '#d8f8c8'][i % 3], rnd(0.7, 1.5));
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
    if (r < 0.62) I.flower.add(x, heightAt(x, z) - 0.05, z, Math.random() * TAU, rnd(0.9, 1.6), flowerCols[i % 6]);
    else if (r < 0.82) place('bush', x, z, rnd(0.7, 1.2), null);
    else if (r < 0.9) place('oak', x, z, rnd(0.8, 1.3), tint[i % 4], 0.5);
    else I.tuft.add(x, heightAt(x, z) - 0.05, z, Math.random() * TAU, rnd(0.7, 1.2), '#e8ffe0', rnd(0.8, 1.3));
  }
  for (const i of Object.values(I)) i.build(root);
}
