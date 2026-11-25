// Visual do jogo: cel-shading com contorno, personagem estilizado, inimigos, cenário e partículas.
// Tudo procedural (sem modelos externos). Cores e formas ficam aqui para facilitar ajustes.
import * as THREE from 'three';

export const ARENA = 34;
const rnd = (a, b) => a + Math.random() * (b - a);
const TAU = Math.PI * 2;

// ---------- materiais e contorno ----------
const gradient = (() => {
  const t = new THREE.DataTexture(new Uint8Array([95, 95, 120, 255, 165, 165, 185, 255, 225, 225, 235, 255, 255, 255, 255, 255]), 4, 1, THREE.RGBAFormat);
  t.minFilter = t.magFilter = THREE.NearestFilter;
  t.needsUpdate = true;
  return t;
})();
export const toon = (color, o = {}) => new THREE.MeshToonMaterial({ color, gradientMap: gradient, ...o });
const glow = (color, k = 1) => toon(color, { emissive: color, emissiveIntensity: k });
const outlines = new Map();
function outlineMat(th, color = '#1b1426') {
  const key = `${th}|${color}`;
  if (!outlines.has(key)) {
    const m = new THREE.MeshBasicMaterial({ color, side: THREE.BackSide });
    m.onBeforeCompile = (s) => (s.vertexShader = s.vertexShader.replace('#include <begin_vertex>', `#include <begin_vertex>\n transformed += normalize(normal) * ${th.toFixed(4)};`));
    outlines.set(key, m);
  }
  return outlines.get(key);
}
// malha com sombra e contorno (casca invertida)
export function mk(geo, mat, { outline = 0.028, color } = {}) {
  const m = new THREE.Mesh(geo, mat);
  m.castShadow = true;
  if (outline) {
    const o = new THREE.Mesh(geo, outlineMat(outline, color));
    o.raycast = () => {};
    m.add(o);
  }
  return m;
}
const at = (o, x, y, z) => (o.position.set(x, y, z), o);
const add = (parent, o) => (parent.add(o), o);
const sphere = (r, w = 20, h = 14) => new THREE.SphereGeometry(r, w, h);
const caps = (r, l) => new THREE.CapsuleGeometry(r, l, 6, 14);

function blob(r) {
  const m = new THREE.Mesh(new THREE.CircleGeometry(r, 20), new THREE.MeshBasicMaterial({ color: '#000', transparent: true, opacity: 0.28, depthWrite: false }));
  m.rotation.x = -Math.PI / 2;
  m.position.y = 0.04;
  return m;
}

function bladeGeo(w, len, tip) {
  const s = new THREE.Shape();
  s.moveTo(-w, 0);
  s.lineTo(-w, len);
  s.lineTo(0, len + tip);
  s.lineTo(w, len);
  s.lineTo(w, 0);
  s.closePath();
  const g = new THREE.ExtrudeGeometry(s, { depth: 0.035, bevelEnabled: true, bevelSize: 0.012, bevelThickness: 0.012, bevelSegments: 1 });
  g.translate(0, 0, -0.0175);
  return g;
}

function hashStr(s) {
  let h = 7;
  for (const c of s) h = (Math.imul(h, 31) + c.charCodeAt(0)) | 0;
  return Math.abs(h);
}
const HAIR = ['#5a3822', '#2b2118', '#d98b2b', '#c4453f', '#7a5ad6', '#2f8f83', '#e8d27a'];

// ---------- herói ----------
export function buildHero(equip, items, name = 'x') {
  const it = (slot) => (equip[slot] ? items[equip[slot]] : null);
  const body = it('body');
  const head = it('head');
  const weapon = it('weapon');
  const tool = it('tool');
  const skin = '#ffd3b4';
  const cloth = body ? body.color : '#4f86f7';
  const root = new THREE.Group();
  const rig = { root, hasCape: false, flame: !!weapon && equip.weapon === 'sword_flame', glowTool: null };
  root.add(blob(0.55));

  // pernas
  const leg = (x) => {
    const pv = at(new THREE.Group(), x, 0.62, 0);
    add(pv, at(mk(caps(0.095, 0.26), toon('#35406b')), 0, -0.27, 0));
    add(pv, at(mk(new THREE.SphereGeometry(0.13, 14, 10).scale(1, 0.75, 1.35), toon('#6b432c')), 0, -0.55, 0.05));
    root.add(pv);
    return pv;
  };
  rig.legL = leg(-0.15);
  rig.legR = leg(0.15);

  // tronco
  const torso = at(new THREE.Group(), 0, 0.98, 0);
  root.add(torso);
  rig.torso = torso;
  const metalBody = body && /armor/.test(equip.body);
  add(torso, mk(caps(0.3, 0.34), toon(cloth)));
  add(torso, at(mk(new THREE.TorusGeometry(0.315, 0.045, 8, 24), toon('#6b432c'), { outline: 0.02 }), 0, -0.12, 0)).rotation.x = Math.PI / 2;
  add(torso, at(mk(new THREE.BoxGeometry(0.1, 0.09, 0.05), glow('#ffd24a', 0.4), { outline: 0.015 }), 0, -0.12, 0.32));
  if (equip.body === 'armor_iron') {
    add(torso, at(mk(new THREE.SphereGeometry(0.36, 18, 12).scale(1, 0.78, 0.62), toon('#c9d1df')), 0, 0.08, 0.1));
    for (const sx of [-1, 1]) add(torso, at(mk(sphere(0.16, 14, 10), toon('#d7deea')), sx * 0.4, 0.34, 0));
  } else if (equip.body === 'armor_shadow') {
    add(torso, at(mk(new THREE.TorusGeometry(0.3, 0.035, 8, 24), glow('#9b6bff', 0.9), { outline: 0 }), 0, 0.27, 0)).rotation.x = Math.PI / 2;
    const hood = add(torso, at(mk(new THREE.SphereGeometry(0.3, 14, 10, 0, TAU, 0, Math.PI * 0.6), toon('#4a3f94')), 0, 0.45, -0.18));
    add(torso, at(new THREE.Mesh(new THREE.OctahedronGeometry(0.075), glow('#b79bff', 1.6)), 0, 0.14, 0.31));
    hood.rotation.x = 0.7;
    const cg = new THREE.PlaneGeometry(0.78, 0.95, 6, 8);
    const cape = new THREE.Mesh(cg, toon('#4a3f94', { side: THREE.DoubleSide }));
    cape.position.set(0, 0.1, -0.3);
    cape.castShadow = true;
    torso.add(cape);
    rig.cape = cape;
    rig.capeBase = Float32Array.from(cg.attributes.position.array);
  } else {
    add(torso, at(mk(new THREE.TorusGeometry(0.27, 0.06, 8, 20), toon('#e8564f'), { outline: 0.02 }), 0, 0.3, 0)).rotation.x = Math.PI / 2;
    const tail = add(torso, at(mk(new THREE.BoxGeometry(0.1, 0.34, 0.04), toon('#e8564f'), { outline: 0.018 }), 0.1, 0.12, -0.27));
    tail.rotation.z = 0.15;
    rig.scarf = tail;
  }

  // braços
  const arm = (x) => {
    const pv = at(new THREE.Group(), x, 1.2, 0);
    add(pv, at(mk(caps(0.075, 0.24), toon(cloth)), 0, -0.22, 0));
    add(pv, at(mk(sphere(0.1, 12, 10), toon(metalBody ? '#c9d1df' : skin)), 0, -0.45, 0));
    torso.parent.add(pv);
    return pv;
  };
  rig.armL = arm(-0.4);
  rig.armR = arm(0.4);

  // cabeça
  const headG = at(new THREE.Group(), 0, 1.78, 0);
  root.add(headG);
  rig.head = headG;
  add(headG, mk(sphere(0.43, 24, 18), toon(skin)));
  const eyes = [];
  for (const sx of [-1, 1]) {
    const eye = at(new THREE.Group(), sx * 0.16, 0.0, 0.38);
    add(eye, mk(new THREE.SphereGeometry(0.09, 12, 10).scale(1, 1.35, 0.5), toon('#1b1426'), { outline: 0 }));
    add(eye, at(new THREE.Mesh(sphere(0.032, 8, 6), new THREE.MeshBasicMaterial({ color: '#fff' })), 0.03, 0.05, 0.05));
    add(eye, at(new THREE.Mesh(sphere(0.016, 6, 5), new THREE.MeshBasicMaterial({ color: '#fff' })), -0.025, -0.04, 0.05));
    add(headG, eye);
    eyes.push(eye);
    add(headG, at(new THREE.Mesh(new THREE.SphereGeometry(0.07, 10, 8).scale(1.2, 0.7, 0.4), new THREE.MeshBasicMaterial({ color: '#ff8fa3', transparent: true, opacity: 0.55 })), sx * 0.27, -0.1, 0.33));
  }
  rig.eyes = eyes;
  const smile = add(headG, at(new THREE.Mesh(new THREE.TorusGeometry(0.05, 0.011, 6, 12, Math.PI), new THREE.MeshBasicMaterial({ color: '#7a3b3b' })), 0, -0.1, 0.41));
  smile.rotation.z = Math.PI;
  const hair = toon(HAIR[hashStr(name) % HAIR.length]);
  const cap = add(headG, mk(new THREE.SphereGeometry(0.455, 22, 14, 0, TAU, 0, Math.PI * 0.52), hair));
  cap.rotation.x = -0.28;
  for (const [x, z, r] of head ? [] : [[-0.2, 0.36, 0.2], [0, 0.4, 0.15], [0.2, 0.36, -0.2]]) {
    const bang = add(headG, at(mk(new THREE.ConeGeometry(0.1, 0.26, 6), hair, { outline: 0.02 }), x, 0.27, z));
    bang.rotation.set(Math.PI, 0, r);
  }
  const ahoge = add(headG, at(mk(new THREE.ConeGeometry(0.05, 0.3, 6), hair, { outline: 0.02 }), 0.02, head ? 0.3 : 0.56, 0.03));
  ahoge.rotation.z = -0.5;
  rig.ahoge = ahoge;
  add(headG, at(mk(caps(0.1, 0.22), hair), 0, -0.02, -0.42)).rotation.x = 0.4;

  // itens de cabeça
  if (equip.head === 'hat_cloth') {
    add(headG, at(mk(new THREE.CylinderGeometry(0.62, 0.62, 0.05, 24), toon(head.color)), 0, 0.3, 0));
    const cone = add(headG, at(mk(new THREE.ConeGeometry(0.36, 0.78, 16), toon(head.color)), 0, 0.7, 0));
    cone.rotation.z = -0.12;
    add(headG, at(mk(new THREE.CylinderGeometry(0.37, 0.4, 0.1, 16), toon('#5b3aa0'), { outline: 0.015 }), 0, 0.38, 0));
    add(headG, at(mk(new THREE.OctahedronGeometry(0.09), glow('#ffe066', 0.9), { outline: 0 }), 0.0, 0.38, 0.4));
  } else if (equip.head === 'helm_iron') {
    add(headG, mk(new THREE.SphereGeometry(0.5, 20, 12, 0, TAU, 0, Math.PI * 0.4), toon(head.color)));
    add(headG, at(mk(new THREE.BoxGeometry(0.07, 0.22, 0.06), toon('#c9d1df'), { outline: 0.015 }), 0, 0.22, 0.45));
    add(headG, at(mk(new THREE.BoxGeometry(0.06, 0.2, 0.5), toon('#e8564f'), { outline: 0.015 }), 0, 0.5, 0));
  } else if (equip.head === 'crown_gold') {
    const gold = glow(head.color, 0.35);
    add(headG, at(mk(new THREE.CylinderGeometry(0.4, 0.43, 0.2, 14, 1, true), gold, { outline: 0.02 }), 0, 0.38, 0)).material.side = THREE.DoubleSide;
    for (let i = 0; i < 6; i++) {
      const a = (i / 6) * TAU;
      add(headG, at(mk(new THREE.ConeGeometry(0.075, 0.26, 5), gold, { outline: 0.018 }), Math.cos(a) * 0.4, 0.62, Math.sin(a) * 0.4));
      add(headG, at(new THREE.Mesh(sphere(0.04, 8, 6), glow(i % 2 ? '#ff4d6d' : '#4dd2ff', 1.4)), Math.cos(a) * 0.41, 0.46, Math.sin(a) * 0.41));
    }
  }

  // arma na mão direita
  if (weapon) {
    const w = new THREE.Group();
    const id = equip.weapon;
    add(w, at(mk(new THREE.CylinderGeometry(0.035, 0.035, 0.26, 8), toon('#6b432c'), { outline: 0.015 }), 0, 0.02, 0));
    if (id === 'axe_titan') {
      add(w, at(mk(new THREE.CylinderGeometry(0.04, 0.04, 1.25, 8), toon('#5a3a1e'), { outline: 0.018 }), 0, 0.55, 0));
      for (const s of [-1, 1]) {
        const head2 = add(w, at(mk(new THREE.CylinderGeometry(0.3, 0.3, 0.06, 16, 1, false, 0, Math.PI), glow(weapon.color, 0.55), { outline: 0.02 }), s * 0.03, 1.05, 0));
        head2.rotation.set(Math.PI / 2, 0, s * Math.PI / 2);
      }
      add(w, at(new THREE.Mesh(sphere(0.06, 8, 6), glow('#c9b8ff', 2)), 0, 1.05, 0));
    } else {
      add(w, at(mk(new THREE.BoxGeometry(0.34, 0.06, 0.09), toon('#d9b24a'), { outline: 0.018 }), 0, 0.2, 0));
      const flame = id === 'sword_flame';
      const bm = id === 'sword_wood' ? toon(weapon.color) : flame ? glow('#ff7a2a', 0.8) : toon('#e3e8f2');
      add(w, at(mk(bladeGeo(id === 'sword_wood' ? 0.085 : 0.07, id === 'sword_wood' ? 0.72 : 0.9, 0.14), bm), 0, 0.23, 0));
      add(w, at(new THREE.Mesh(sphere(0.045, 8, 6), toon('#d9b24a')), 0, -0.12, 0));
    }
    w.position.set(0.1, -0.45, 0.08);
    w.rotation.set(0.5, 0, -0.18);
    rig.armR.add(w);
    rig.weapon = w;
  }
  // ferramenta
  if (tool) {
    const id = equip.tool;
    if (id === 'lantern') {
      const t = at(new THREE.Group(), 0, -0.52, 0.06);
      add(t, mk(new THREE.CylinderGeometry(0.1, 0.1, 0.24, 8), toon('#3a3a48'), { outline: 0.015 })).material.wireframe = false;
      const core = add(t, new THREE.Mesh(sphere(0.085, 10, 8), glow('#ffe08a', 1.6)));
      add(t, at(mk(new THREE.TorusGeometry(0.07, 0.012, 6, 10, Math.PI), toon('#222'), { outline: 0 }), 0, 0.15, 0));
      rig.armL.add(t);
      rig.glowTool = core;
    } else if (id === 'magnet') {
      const t = at(new THREE.Group(), 0, -0.52, 0.06);
      const u = add(t, mk(new THREE.TorusGeometry(0.15, 0.055, 8, 14, Math.PI), toon('#e8564f'), { outline: 0.02 }));
      u.rotation.z = Math.PI;
      for (const sx of [-1, 1]) add(t, at(mk(new THREE.CylinderGeometry(0.056, 0.056, 0.08, 8), toon('#e8eef8'), { outline: 0.015 }), sx * 0.15, 0.04, 0));
      rig.armL.add(t);
    } else {
      rig.charm = at(mk(new THREE.OctahedronGeometry(0.17), glow('#46e0a0', 1.3), { outline: 0.02 }), -0.75, 2.2, 0);
      root.add(rig.charm);
    }
  }
  return rig;
}

// animação do herói. s = { moving, swing (0..1 progresso, 0 = sem ataque), spin, t, dt }
export function animateHero(rig, s) {
  const t = s.t;
  const w = s.moving ? Math.sin(t * 11) * 0.85 : 0;
  rig.legL.rotation.x = w;
  rig.legR.rotation.x = -w;
  rig.armL.rotation.x = -w * 0.8;
  rig.armR.rotation.x = s.swing > 0 ? -2.4 + s.swing * 2.9 : w * 0.8;
  rig.armL.rotation.z = 0.12;
  rig.armR.rotation.z = -0.12;
  const breathe = 1 + Math.sin(t * 2.2) * 0.018;
  rig.torso.scale.set(1, breathe, 1);
  rig.torso.rotation.y = s.swing > 0 ? (0.5 - s.swing) * 0.6 : 0;
  rig.head.position.y = 1.78 + (s.moving ? Math.abs(Math.sin(t * 11)) * 0.035 : Math.sin(t * 2.2) * 0.012);
  rig.head.rotation.x = s.moving ? 0.08 : 0;
  rig.ahoge.rotation.z = -0.5 + Math.sin(t * 3) * 0.15;
  const blink = Math.sin(t * 0.9 + 1) > 0.985 ? 0.1 : 1;
  for (const e of rig.eyes) e.scale.y = blink;
  if (rig.scarf) rig.scarf.rotation.x = Math.sin(t * 6) * 0.25 * (s.moving ? 1 : 0.3);
  if (rig.cape) {
    const p = rig.cape.geometry.attributes.position;
    for (let i = 0; i < p.count; i++) {
      const y = rig.capeBase[i * 3 + 1];
      const k = (0.45 - y) * 0.5;
      p.setZ(i, rig.capeBase[i * 3 + 2] - k * (s.moving ? 0.5 + Math.sin(t * 9 + y * 5) * 0.2 : 0.1 + Math.sin(t * 2 + y * 3) * 0.04));
    }
    p.needsUpdate = true;
  }
  if (rig.charm) {
    rig.charm.rotation.y += s.dt * 2;
    rig.charm.position.y = 2.25 + Math.sin(t * 3) * 0.08;
  }
  if (rig.glowTool) rig.glowTool.material.emissiveIntensity = 1.4 + Math.sin(t * 9) * 0.3;
  rig.root.position.y = s.moving ? Math.abs(Math.sin(t * 11)) * 0.05 : 0;
}

// ---------- inimigos ----------
export function buildEnemy(type) {
  const g = new THREE.Group();
  const rig = { g, type };
  if (type === 'slime') {
    const body = mk(new THREE.SphereGeometry(0.75, 24, 16).scale(1, 0.82, 1), toon('#22b655', { emissive: '#0a7a33', emissiveIntensity: 0.35 }), { outline: 0.035 });
    body.position.y = 0.6;
    g.add(body);
    rig.body = body;
    add(body, at(new THREE.Mesh(new THREE.SphereGeometry(0.2, 10, 8).scale(1, 0.55, 0.6), new THREE.MeshBasicMaterial({ color: '#d6ffe0', transparent: true, opacity: 0.55 })), -0.3, 0.42, 0.4));
    for (const sx of [-1, 1]) {
      const eye = at(new THREE.Group(), sx * 0.26, 0.12, 0.62);
      add(eye, new THREE.Mesh(new THREE.SphereGeometry(0.17, 12, 10).scale(1, 1.2, 0.5), new THREE.MeshBasicMaterial({ color: '#fff' })));
      add(eye, at(new THREE.Mesh(sphere(0.085, 8, 6), new THREE.MeshBasicMaterial({ color: '#1b1426' })), 0, 0, 0.07));
      add(eye, at(new THREE.Mesh(sphere(0.03, 6, 5), new THREE.MeshBasicMaterial({ color: '#fff' })), 0.03, 0.04, 0.12));
      body.add(eye);
      body.add(at(new THREE.Mesh(new THREE.SphereGeometry(0.08, 8, 6).scale(1.3, 0.7, 0.4), new THREE.MeshBasicMaterial({ color: '#ff8fa3', transparent: true, opacity: 0.5 })), sx * 0.45, -0.05, 0.56));
    }
    const mouth = add(body, at(new THREE.Mesh(new THREE.TorusGeometry(0.07, 0.014, 6, 12, Math.PI), new THREE.MeshBasicMaterial({ color: '#1b3a22' })), 0, -0.12, 0.7));
    mouth.rotation.z = Math.PI;
    const leaf = add(body, at(mk(new THREE.ConeGeometry(0.1, 0.3, 5), toon('#3fae6a'), { outline: 0.02 }), 0, 0.72, 0));
    leaf.rotation.z = 0.3;
    rig.r = 0.8;
    rig.barY = 1.7;
    g.add(blob(0.8));
  } else {
    const body = mk(new THREE.SphereGeometry(1.0, 22, 16).scale(1.1, 1, 1), toon('#cf5a45'), { outline: 0.04 });
    body.position.y = 1.15;
    g.add(body);
    rig.body = body;
    add(body, at(new THREE.Mesh(new THREE.SphereGeometry(0.62, 14, 10).scale(1, 1, 0.5), toon('#f0b894')), 0, -0.15, 0.8));
    const head = add(body, at(mk(sphere(0.5, 18, 14), toon('#cf5a45')), 0, 1.05, 0.2));
    for (const sx of [-1, 1]) {
      const horn = add(head, at(mk(new THREE.ConeGeometry(0.16, 0.6, 7), toon('#efe6cf'), { outline: 0.025 }), sx * 0.34, 0.5, 0));
      horn.rotation.z = -sx * 0.5;
      add(head, at(new THREE.Mesh(new THREE.SphereGeometry(0.1, 10, 8).scale(1.2, 0.8, 0.5), glow('#ffd23a', 1.6)), sx * 0.18, 0.08, 0.44));
      const brow = add(head, at(new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.05, 0.05), toon('#2a1410')), sx * 0.18, 0.22, 0.46));
      brow.rotation.z = sx * 0.4;
      const tusk = add(head, at(mk(new THREE.ConeGeometry(0.06, 0.2, 6), toon('#fff6e0'), { outline: 0.012 }), sx * 0.15, -0.28, 0.44));
      tusk.rotation.x = Math.PI;
    }
    rig.armL = at(new THREE.Group(), -1.1, 1.5, 0);
    rig.armR = at(new THREE.Group(), 1.1, 1.5, 0);
    for (const a of [rig.armL, rig.armR]) {
      add(a, at(mk(caps(0.2, 0.5), toon('#cf5a45')), 0, -0.4, 0));
      add(a, at(mk(sphere(0.26, 12, 10), toon('#b04535')), 0, -0.85, 0));
      g.add(a);
    }
    const club = add(rig.armR, at(new THREE.Group(), 0, -0.85, 0.2));
    add(club, at(mk(new THREE.CylinderGeometry(0.12, 0.2, 1.3, 8), toon('#6b432c'), { outline: 0.03 }), 0, 0.5, 0));
    for (let i = 0; i < 6; i++) {
      const a = (i / 6) * TAU;
      const sp = add(club, at(mk(new THREE.ConeGeometry(0.06, 0.2, 5), toon('#c9d1df'), { outline: 0.012 }), Math.cos(a) * 0.2, 0.9 + (i % 2) * 0.2, Math.sin(a) * 0.2));
      sp.rotation.set(Math.sin(a) * 1.4, 0, -Math.cos(a) * 1.4);
    }
    club.rotation.x = 0.6;
    add(g, at(mk(caps(0.22, 0.4), toon('#b04535')), -0.45, 0.45, 0));
    add(g, at(mk(caps(0.22, 0.4), toon('#b04535')), 0.45, 0.45, 0));
    g.scale.setScalar(0.82);
    rig.r = 1.05;
    rig.barY = 3.1;
    g.add(blob(1.3));
  }
  return rig;
}

// ---------- partículas ----------
export class Fx {
  constructor(scene, cap = 900) {
    this.cap = cap;
    this.n = 0;
    this.p = [];
    const geo = (this.geo = new THREE.BufferGeometry());
    geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(cap * 3), 3));
    geo.setAttribute('color', new THREE.BufferAttribute(new Float32Array(cap * 3), 3));
    geo.setAttribute('size', new THREE.BufferAttribute(new Float32Array(cap), 1));
    geo.setAttribute('alpha', new THREE.BufferAttribute(new Float32Array(cap), 1));
    const mat = new THREE.ShaderMaterial({
      transparent: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
      vertexColors: true,
      vertexShader: `attribute float size; attribute float alpha; varying vec3 vC; varying float vA;
        void main(){ vC = color; vA = alpha; vec4 mv = modelViewMatrix * vec4(position,1.0); gl_PointSize = size * (320.0 / -mv.z); gl_Position = projectionMatrix * mv; }`,
      fragmentShader: `varying vec3 vC; varying float vA;
        void main(){ float d = length(gl_PointCoord - 0.5); float a = smoothstep(0.5, 0.0, d) * vA; if (a < 0.01) discard; gl_FragColor = vec4(vC, a); }`,
    });
    this.points = new THREE.Points(geo, mat);
    this.points.frustumCulled = false;
    scene.add(this.points);
  }
  burst(pos, { color = '#fff', count = 12, speed = 4, life = 0.6, size = 0.35, gravity = -6, up = 1 } = {}) {
    const c = new THREE.Color(color);
    for (let i = 0; i < count && this.p.length < this.cap; i++) {
      const a = Math.random() * TAU;
      const e = Math.random() * 1.2 - 0.2;
      this.p.push({ x: pos.x, y: pos.y, z: pos.z, vx: Math.cos(a) * speed * rnd(0.3, 1), vy: up * (e + 0.4) * speed * rnd(0.4, 1), vz: Math.sin(a) * speed * rnd(0.3, 1), life, max: life, size, g: gravity, c });
    }
  }
  update(dt) {
    const pos = this.geo.attributes.position;
    const col = this.geo.attributes.color;
    const siz = this.geo.attributes.size;
    const alp = this.geo.attributes.alpha;
    let n = 0;
    for (let i = this.p.length - 1; i >= 0; i--) {
      const q = this.p[i];
      q.life -= dt;
      if (q.life <= 0) {
        this.p[i] = this.p[this.p.length - 1];
        this.p.pop();
        continue;
      }
      q.vy += q.g * dt;
      q.x += q.vx * dt;
      q.y += q.vy * dt;
      q.z += q.vz * dt;
    }
    for (const q of this.p) {
      pos.setXYZ(n, q.x, q.y, q.z);
      col.setXYZ(n, q.c.r, q.c.g, q.c.b);
      const k = q.life / q.max;
      siz.setX(n, q.size * (0.4 + k));
      alp.setX(n, Math.min(1, k * 1.6));
      n++;
    }
    this.geo.setDrawRange(0, n);
    for (const a of [pos, col, siz, alp]) a.needsUpdate = true;
  }
}

// ---------- cenário ----------
const smooth = (a, b, x) => {
  const t = Math.min(1, Math.max(0, (x - a) / (b - a)));
  return t * t * (3 - 2 * t);
};
const noise = (x, z) => Math.sin(x * 0.11 + 1.3) * Math.cos(z * 0.09 - 0.7) * 0.6 + Math.sin(x * 0.043 + z * 0.037) * 0.8 + Math.sin(x * 0.21 - z * 0.17) * 0.25;
const LAKE = { x: 62, z: -34, r: 24 };
export function heightAt(x, z) {
  const r = Math.hypot(x, z);
  let h = smooth(ARENA + 8, ARENA + 70, r) * (noise(x, z) * 5 + 6);
  const d = Math.hypot(x - LAKE.x, z - LAKE.z);
  h -= (1 - smooth(LAKE.r * 0.55, LAKE.r + 7, d)) * 3.4;
  return h;
}

function tex(size, draw) {
  const c = document.createElement('canvas');
  c.width = c.height = size;
  draw(c.getContext('2d'), size);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 4;
  return t;
}

export function buildWorld(scene) {
  const upd = [];
  const timeU = { value: 0 };
  const horizon = new THREE.Color('#ffe6c8');
  scene.fog = new THREE.Fog(horizon, 80, 480);

  // céu
  const sunDir = new THREE.Vector3(0.5, 0.55, 0.35).normalize();
  const sky = new THREE.Mesh(
    new THREE.SphereGeometry(520, 32, 16),
    new THREE.ShaderMaterial({
      side: THREE.BackSide,
      depthWrite: false,
      fog: false,
      uniforms: { sun: { value: sunDir } },
      vertexShader: 'varying vec3 vP; void main(){ vP = position; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
      fragmentShader: `varying vec3 vP; uniform vec3 sun;
        void main(){ vec3 d = normalize(vP); float h = clamp(d.y, -0.1, 1.0);
          vec3 top = vec3(0.22,0.50,0.95); vec3 mid = vec3(0.55,0.78,1.0); vec3 hor = vec3(1.0,0.90,0.78);
          vec3 c = mix(hor, mid, smoothstep(0.0, 0.25, h)); c = mix(c, top, smoothstep(0.2, 0.9, h));
          float s = max(dot(d, normalize(sun)), 0.0); c += vec3(1.0,0.8,0.5) * pow(s, 12.0) * 0.55; c += vec3(1.0,0.97,0.85) * smoothstep(0.9975, 0.9985, s);
          gl_FragColor = vec4(c, 1.0); }`,
    }),
  );
  scene.add(sky);

  // luzes
  scene.add(new THREE.HemisphereLight('#bfe0ff', '#6a8a52', 1.15));
  const sun = new THREE.DirectionalLight('#fff0d0', 2.4);
  sun.position.copy(sunDir).multiplyScalar(70);
  sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -52, right: 52, top: 52, bottom: -52, near: 1, far: 160 });
  sun.shadow.bias = -0.0004;
  sun.shadow.normalBias = 0.04;
  scene.add(sun);

  // terreno com colinas, margem do lago e cores por altura
  const tg = new THREE.PlaneGeometry(560, 560, 180, 180);
  tg.rotateX(-Math.PI / 2);
  const pa = tg.attributes.position;
  const colors = new Float32Array(pa.count * 3);
  const c1 = new THREE.Color('#7fcf62');
  const c2 = new THREE.Color('#4d9a4c');
  const sandC = new THREE.Color('#ead9a0');
  const rock = new THREE.Color('#8b9a82');
  const tmp = new THREE.Color();
  for (let i = 0; i < pa.count; i++) {
    const x = pa.getX(i);
    const z = pa.getZ(i);
    const h = heightAt(x, z);
    pa.setY(i, h);
    tmp.copy(c1).lerp(c2, 0.5 + 0.5 * Math.sin(x * 0.13) * Math.cos(z * 0.11));
    const d = Math.hypot(x - LAKE.x, z - LAKE.z);
    if (h < -0.2) tmp.lerp(sandC, smooth(-0.2, -1.4, h) * 0.9 + 0.1);
    tmp.lerp(rock, smooth(7, 14, h) * 0.7);
    if (Math.hypot(x, z) < ARENA + 6) tmp.set('#8fd06b');
    colors.set([tmp.r, tmp.g, tmp.b], i * 3);
    void d;
  }
  tg.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  tg.computeVertexNormals();
  const terrain = new THREE.Mesh(tg, toon('#ffffff', { vertexColors: true }));
  terrain.receiveShadow = true;
  scene.add(terrain);

  // lago
  const water = new THREE.Mesh(new THREE.CircleGeometry(LAKE.r + 4, 56), new THREE.MeshStandardMaterial({ color: '#4cb4ea', roughness: 0.08, metalness: 0.2, transparent: true, opacity: 0.82 }));
  water.rotation.x = -Math.PI / 2;
  water.position.set(LAKE.x, -1.3, LAKE.z);
  water.receiveShadow = true;
  scene.add(water);
  upd.push((t) => (water.material.opacity = 0.8 + Math.sin(t * 1.3) * 0.04));

  // piso da arena (pedra com anéis dourados)
  const floorTex = tex(1024, (g, S) => {
    const R = S / 2;
    g.fillStyle = '#cdbf9a';
    g.fillRect(0, 0, S, S);
    for (let i = 0; i < 420; i++) {
      const a = Math.random() * TAU;
      const r = Math.random() * R * 0.97;
      g.fillStyle = `hsla(${38 + Math.random() * 14},${22 + Math.random() * 14}%,${62 + Math.random() * 16}%,0.35)`;
      g.beginPath();
      g.arc(R + Math.cos(a) * r, R + Math.sin(a) * r, 8 + Math.random() * 26, 0, TAU);
      g.fill();
    }
    g.translate(R, R);
    g.strokeStyle = 'rgba(70,56,40,0.16)';
    g.lineWidth = 1.5;
    for (let r = 60; r < R; r += 52) {
      g.beginPath();
      g.arc(0, 0, r, 0, TAU);
      g.stroke();
    }
    for (let a = 0; a < 360; a += 15) {
      g.save();
      g.rotate((a * Math.PI) / 180);
      g.beginPath();
      g.moveTo(80, 0);
      g.lineTo(R, 0);
      g.stroke();
      g.restore();
    }
    for (const [r, w] of [[150, 7], [300, 6], [462, 10]]) {
      g.strokeStyle = '#d9a82a';
      g.lineWidth = w;
      g.beginPath();
      g.arc(0, 0, r, 0, TAU);
      g.stroke();
      g.strokeStyle = '#f6dc7a';
      g.lineWidth = 2;
      g.beginPath();
      g.arc(0, 0, r, 0, TAU);
      g.stroke();
    }
  });
  const floor = new THREE.Mesh(new THREE.CircleGeometry(ARENA + 2, 96), toon('#ffffff', { map: floorTex }));
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = 0.03;
  floor.receiveShadow = true;
  scene.add(floor);
  const rim = new THREE.Mesh(new THREE.TorusGeometry(ARENA + 2.4, 0.5, 8, 96), toon('#b9ad90'));
  rim.rotation.x = Math.PI / 2;
  rim.position.y = 0.1;
  rim.receiveShadow = true;
  scene.add(rim);

  // plataforma central com runas brilhantes
  const runeTex = tex(512, (g, S) => {
    g.fillStyle = '#242a3c';
    g.fillRect(0, 0, S, S);
    g.translate(S / 2, S / 2);
    g.strokeStyle = '#59e0ff';
    g.lineWidth = 6;
    for (const r of [235, 180, 120]) {
      g.beginPath();
      g.arc(0, 0, r, 0, TAU);
      g.stroke();
    }
    g.lineWidth = 5;
    for (let i = 0; i < 8; i++) {
      const a = (i / 8) * TAU;
      g.beginPath();
      g.moveTo(Math.cos(a) * 125, Math.sin(a) * 125);
      g.lineTo(Math.cos(a) * 232, Math.sin(a) * 232);
      g.stroke();
    }
    g.beginPath();
    for (let i = 0; i <= 8; i++) {
      const a = ((i + 0.5) / 8) * TAU;
      g[i ? 'lineTo' : 'moveTo'](Math.cos(a) * 118, Math.sin(a) * 118);
    }
    g.stroke();
    g.fillStyle = '#59e0ff';
    g.beginPath();
    g.arc(0, 0, 22, 0, TAU);
    g.fill();
    g.fillStyle = '#59e0ff';
    for (let i = 0; i < 24; i++) {
      const a = (i / 24) * TAU;
      g.save();
      g.translate(Math.cos(a) * 208, Math.sin(a) * 208);
      g.rotate(a);
      g.fillRect(-4, -12, 8, 24);
      g.restore();
    }
  });
  const plat = mk(new THREE.CylinderGeometry(5.2, 5.6, 0.45, 40), [toon('#8e97ad'), toon('#ffffff', { map: runeTex, emissive: '#59e0ff', emissiveMap: runeTex, emissiveIntensity: 0.9 }), toon('#8e97ad')], { outline: 0.05 });
  plat.position.y = 0.22;
  plat.receiveShadow = true;
  scene.add(plat);

  // pilares, muretas, bandeiras e tochas
  const lights = [];
  const N = 20;
  const PR = ARENA + 2.2;
  for (let i = 0; i < N; i++) {
    const a = (i / N) * TAU;
    const px = Math.cos(a) * PR;
    const pz = Math.sin(a) * PR;
    const g = new THREE.Group();
    g.position.set(px, 0, pz);
    add(g, at(mk(new THREE.CylinderGeometry(1.25, 1.45, 0.7, 10), toon('#aeb4c4')), 0, 0.35, 0));
    add(g, at(mk(new THREE.CylinderGeometry(0.85, 1.0, 5.4, 10), toon('#c9cfdc')), 0, 3.3, 0));
    add(g, at(mk(new THREE.CylinderGeometry(1.2, 0.95, 0.6, 10), toon('#aeb4c4')), 0, 6.3, 0));
    add(g, at(mk(new THREE.BoxGeometry(2.1, 0.35, 2.1), toon('#9aa1b3')), 0, 6.75, 0));
    const orb = add(g, at(mk(sphere(0.5, 14, 10), glow('#ffd24a', 0.7), { outline: 0.03 }), 0, 7.4, 0));
    upd.push((t) => (orb.material.emissiveIntensity = 0.6 + Math.sin(t * 2 + i) * 0.25));
    g.rotation.y = -a;
    scene.add(g);
    // mureta até o próximo pilar
    const a2 = ((i + 0.5) / N) * TAU;
    const wall = mk(new THREE.BoxGeometry(2.0, 1.7, (TAU * PR) / N - 1.6), toon('#b3b9c9'));
    wall.position.set(Math.cos(a2) * PR, 0.85, Math.sin(a2) * PR);
    wall.rotation.y = -a2;
    scene.add(wall);
    // bandeira
    if (i % 2 === 0) {
      const flag = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 3.2, 4, 8), toon(i % 4 === 0 ? '#d8404f' : '#2f8fd8', { side: THREE.DoubleSide }));
      flag.position.set(Math.cos(a) * (PR - 1.15), 4.4, Math.sin(a) * (PR - 1.15));
      flag.rotation.y = -a + Math.PI / 2;
      flag.castShadow = true;
      scene.add(flag);
      const base = Float32Array.from(flag.geometry.attributes.position.array);
      upd.push((t) => {
        const p = flag.geometry.attributes.position;
        for (let k = 0; k < p.count; k++) p.setZ(k, base[k * 3 + 2] + Math.sin(t * 3 + base[k * 3 + 1] * 1.3 + i) * 0.12 * (1.6 - base[k * 3 + 1] * 0.5));
        p.needsUpdate = true;
      });
      const emblem = new THREE.Mesh(new THREE.CircleGeometry(0.4, 16), new THREE.MeshBasicMaterial({ color: '#ffe38a' }));
      emblem.position.set(0, 0.3, 0.02);
      flag.add(emblem);
    }
  }
  for (const a of [0, Math.PI / 2, Math.PI, (3 * Math.PI) / 2]) {
    const tx = Math.cos(a) * (ARENA - 3);
    const tz = Math.sin(a) * (ARENA - 3);
    const t = new THREE.Group();
    t.position.set(tx, 0, tz);
    add(t, at(mk(new THREE.CylinderGeometry(0.2, 0.3, 3.2, 8), toon('#6b432c')), 0, 1.6, 0));
    add(t, at(mk(new THREE.CylinderGeometry(0.6, 0.35, 0.5, 10), toon('#3a3a48')), 0, 3.3, 0));
    const fl = add(t, at(new THREE.Mesh(new THREE.ConeGeometry(0.42, 1.2, 8), glow('#ff9a2a', 2.2)), 0, 4.1, 0));
    const fl2 = add(t, at(new THREE.Mesh(new THREE.ConeGeometry(0.24, 0.8, 8), glow('#ffe07a', 2.6)), 0, 3.95, 0));
    const pl = new THREE.PointLight('#ff9a4a', 90, 26, 2);
    pl.position.set(0, 4.2, 0);
    t.add(pl);
    scene.add(t);
    upd.push((tm) => {
      const f = 1 + Math.sin(tm * 14 + a * 3) * 0.12 + Math.sin(tm * 23) * 0.06;
      fl.scale.set(1, f, 1);
      fl2.scale.set(1, f * 1.1, 1);
      pl.intensity = 80 + Math.sin(tm * 11 + a) * 14;
    });
    lights.push(pl);
  }

  // árvores, arbustos, pedras
  const treeGeo = { trunk: new THREE.CylinderGeometry(0.35, 0.6, 3, 7), blob: new THREE.IcosahedronGeometry(1, 1) };
  const greens = ['#4aa84f', '#5cbd57', '#3f9548', '#6fcf5f'];
  const placeOK = (x, z) => Math.hypot(x, z) > ARENA + 10 && Math.hypot(x - LAKE.x, z - LAKE.z) > LAKE.r + 6;
  for (let i = 0; i < 90; i++) {
    const a = Math.random() * TAU;
    const d = rnd(ARENA + 12, 130);
    const x = Math.cos(a) * d;
    const z = Math.sin(a) * d;
    if (!placeOK(x, z)) continue;
    const t = new THREE.Group();
    const s = rnd(0.8, 1.7);
    add(t, at(mk(treeGeo.trunk, toon('#7a5233'), { outline: 0.03 }), 0, 1.5, 0));
    for (let k = 0; k < 3; k++) {
      const b = add(t, at(mk(treeGeo.blob, toon(greens[(i + k) % 4]), { outline: 0.04 }), rnd(-0.6, 0.6), 3.6 + k * 0.7, rnd(-0.6, 0.6)));
      b.scale.setScalar(1.9 - k * 0.35);
      b.scale.y *= 0.85;
    }
    t.position.set(x, heightAt(x, z) - 0.1, z);
    t.scale.setScalar(s);
    t.rotation.y = Math.random() * TAU;
    scene.add(t);
  }
  const bushColors = ['#4aa84f', '#5cbd57', '#3f9548'];
  for (let i = 0; i < 60; i++) {
    const a = Math.random() * TAU;
    const d = rnd(ARENA + 6, 100);
    const x = Math.cos(a) * d;
    const z = Math.sin(a) * d;
    if (!placeOK(x, z)) continue;
    const b = mk(treeGeo.blob, toon(bushColors[i % 3]), { outline: 0.05 });
    b.scale.set(rnd(0.9, 1.5), rnd(0.7, 1.0), rnd(0.9, 1.5));
    b.position.set(x, heightAt(x, z) + 0.45, z);
    scene.add(b);
  }
  const rockGeo = new THREE.DodecahedronGeometry(1, 0);
  for (let i = 0; i < 46; i++) {
    const a = Math.random() * TAU;
    const d = rnd(ARENA + 5, 120);
    const x = Math.cos(a) * d;
    const z = Math.sin(a) * d;
    if (!placeOK(x, z)) continue;
    const r = mk(rockGeo, toon(['#8f98a6', '#a1a9b5', '#7d8794'][i % 3]), { outline: 0.05 });
    r.scale.set(rnd(0.7, 2.2), rnd(0.6, 1.6), rnd(0.7, 2.2));
    r.position.set(x, heightAt(x, z) + 0.3, z);
    r.rotation.set(Math.random(), Math.random() * TAU, Math.random());
    scene.add(r);
  }

  // flores e grama ao vento (instanciadas)
  const flowerGeo = new THREE.SphereGeometry(0.16, 8, 6);
  const flowers = new THREE.InstancedMesh(flowerGeo, toon('#ffffff'), 1400);
  const fc = ['#ff6b8b', '#ffd24a', '#ffffff', '#8fb6ff', '#ff9a4a', '#c08bff'];
  const m4 = new THREE.Matrix4();
  for (let i = 0; i < 1400; i++) {
    const a = Math.random() * TAU;
    const d = rnd(ARENA + 4, 95);
    const x = Math.cos(a) * d;
    const z = Math.sin(a) * d;
    if (!placeOK(x, z) && Math.hypot(x, z) > ARENA + 10) {
      m4.makeScale(0, 0, 0);
    } else m4.makeTranslation(x, heightAt(x, z) + 0.45, z);
    flowers.setMatrixAt(i, m4);
    flowers.setColorAt(i, new THREE.Color(fc[i % fc.length]));
  }
  scene.add(flowers);
  const grassMat = toon('#ffffff');
  grassMat.onBeforeCompile = (s) => {
    s.uniforms.uTime = timeU;
    s.vertexShader = 'uniform float uTime;\n' + s.vertexShader.replace('#include <begin_vertex>', `#include <begin_vertex>
      float sw = sin(uTime * 1.8 + instanceMatrix[3].x * 0.45 + instanceMatrix[3].z * 0.37) * 0.16 * (position.y + 0.3);
      transformed.x += sw; transformed.z += sw * 0.6;`);
  };
  const grassGeo = new THREE.ConeGeometry(0.1, 0.9, 4, 1, true);
  grassGeo.translate(0, 0.45, 0);
  const NG = 9000;
  const grass = new THREE.InstancedMesh(grassGeo, grassMat, NG);
  const gc = ['#5fc15a', '#76d864', '#4aa84f', '#8be06f'];
  for (let i = 0; i < NG; i++) {
    const a = Math.random() * TAU;
    const d = ARENA + 3 + Math.pow(Math.random(), 0.7) * 75;
    const x = Math.cos(a) * d;
    const z = Math.sin(a) * d;
    const h = heightAt(x, z);
    if (h < -0.3 || Math.hypot(x - LAKE.x, z - LAKE.z) < LAKE.r) m4.makeScale(0, 0, 0);
    else m4.compose(new THREE.Vector3(x, h, z), new THREE.Quaternion().setFromEuler(new THREE.Euler(0, Math.random() * TAU, 0)), new THREE.Vector3(rnd(0.8, 1.6), rnd(0.7, 1.8), rnd(0.8, 1.6)));
    grass.setMatrixAt(i, m4);
    grass.setColorAt(i, new THREE.Color(gc[i % 4]));
  }
  grass.receiveShadow = true;
  scene.add(grass);

  // montanhas distantes
  for (let i = 0; i < 18; i++) {
    const a = (i / 18) * TAU + Math.random() * 0.2;
    const d = rnd(235, 290);
    const h = rnd(50, 110);
    const m = new THREE.Group();
    add(m, at(new THREE.Mesh(new THREE.ConeGeometry(rnd(42, 70), h, 7), toon('#5c78bd', { fog: true })), 0, h / 2, 0));
    add(m, at(new THREE.Mesh(new THREE.ConeGeometry(h * 0.2, h * 0.35, 7), toon('#f4f8ff')), 0, h * 0.83, 0));
    m.position.set(Math.cos(a) * d, -2, Math.sin(a) * d);
    scene.add(m);
  }

  // nuvens
  const clouds = [];
  const cloudMat = new THREE.MeshBasicMaterial({ color: '#ffffff', fog: false });
  for (let i = 0; i < 18; i++) {
    const c = new THREE.Group();
    const n = 4 + Math.floor(Math.random() * 3);
    for (let k = 0; k < n; k++) {
      const s = new THREE.Mesh(new THREE.SphereGeometry(rnd(5, 9), 12, 9), cloudMat);
      s.position.set(k * 6 - n * 3 + rnd(-2, 2), rnd(-1.5, 2), rnd(-3, 3));
      s.scale.y = 0.6;
      c.add(s);
    }
    const a = Math.random() * TAU;
    const d = rnd(90, 240);
    c.position.set(Math.cos(a) * d, rnd(70, 110), Math.sin(a) * d);
    c.userData = { a, d, y: c.position.y, sp: rnd(0.004, 0.012) };
    scene.add(c);
    clouds.push(c);
  }
  upd.push((_t, dt) => {
    for (const c of clouds) {
      c.userData.a += c.userData.sp * dt;
      c.position.set(Math.cos(c.userData.a) * c.userData.d, c.userData.y, Math.sin(c.userData.a) * c.userData.d);
    }
  });

  return {
    update(t, dt) {
      timeU.value = t;
      for (const f of upd) f(t, dt);
    },
    sun,
  };
}

// ---------- pós-processamento ----------
export async function createComposer(renderer, scene, camera) {
  const [{ EffectComposer }, { RenderPass }, { UnrealBloomPass }, { OutputPass }] = await Promise.all([
    import('./vendor/jsm/postprocessing/EffectComposer.js'),
    import('./vendor/jsm/postprocessing/RenderPass.js'),
    import('./vendor/jsm/postprocessing/UnrealBloomPass.js'),
    import('./vendor/jsm/postprocessing/OutputPass.js'),
  ]);
  const size = renderer.getSize(new THREE.Vector2());
  const rt = new THREE.WebGLRenderTarget(size.x, size.y, { type: THREE.HalfFloatType, samples: 4 });
  const composer = new EffectComposer(renderer, rt);
  composer.addPass(new RenderPass(scene, camera));
  const bloom = new UnrealBloomPass(new THREE.Vector2(size.x, size.y), 0.26, 0.5, 0.95);
  composer.addPass(bloom);
  composer.addPass(new OutputPass());
  return composer;
}
