// Avatares e criaturas em estilo "bonequinho de blocos arredondados" (tipo Roblox), tudo gerado por código.
import * as THREE from 'three';
import { RoundedBoxGeometry } from './vendor/jsm/geometries/RoundedBoxGeometry.js';
import { SKIN, HAIR_COLOR, SHIRT, PANTS } from './shared/world.js';

const TAU = Math.PI * 2;
const mats = new Map();
export const std = (color, o = {}) => {
  const key = color + JSON.stringify(o);
  if (!mats.has(key)) mats.set(key, new THREE.MeshStandardMaterial({ color, roughness: 0.55, metalness: 0, ...o }));
  return mats.get(key);
};
const geos = new Map();
export const rb = (w, h, d, r = 0.1) => {
  const key = [w, h, d, r].join();
  if (!geos.has(key)) geos.set(key, new RoundedBoxGeometry(w, h, d, 3, Math.min(r, w / 2 - 0.001, h / 2 - 0.001, d / 2 - 0.001)));
  return geos.get(key);
};
const mesh = (geo, mat, x = 0, y = 0, z = 0, parent) => {
  const m = new THREE.Mesh(geo, mat);
  m.position.set(x, y, z);
  m.castShadow = true;
  m.receiveShadow = true;
  parent?.add(m);
  return m;
};
const glow = (color, k = 1.5) => std(color, { emissive: color, emissiveIntensity: k, roughness: 0.4 });

// ---------- rostos ----------
const faceTex = new Map();
function faceTexture(idx) {
  if (faceTex.has(idx)) return faceTex.get(idx);
  const c = document.createElement('canvas');
  c.width = c.height = 128;
  const g = c.getContext('2d');
  g.lineCap = 'round';
  g.strokeStyle = g.fillStyle = '#2a1a14';
  const eye = (x) => {
    g.fillStyle = '#2a1a14';
    g.beginPath();
    g.ellipse(x, 56, 7.5, 12, 0, 0, TAU);
    g.fill();
    g.fillStyle = '#fff';
    g.beginPath();
    g.arc(x + 2.5, 50, 3, 0, TAU);
    g.fill();
    g.beginPath();
    g.arc(x - 2, 62, 1.5, 0, TAU);
    g.fill();
  };
  const smile = () => {
    g.lineWidth = 5;
    g.beginPath();
    g.arc(64, 72, 17, 0.15 * Math.PI, 0.85 * Math.PI);
    g.stroke();
  };
  g.fillStyle = 'rgba(255,120,140,0.5)';
  for (const x of [26, 102]) {
    g.beginPath();
    g.ellipse(x, 78, 10, 6, 0, 0, TAU);
    g.fill();
  }
  g.fillStyle = g.strokeStyle = '#2a1a14';
  if (idx === 0) (eye(44), eye(84), smile());
  else if (idx === 1) {
    eye(44);
    g.lineWidth = 5;
    g.beginPath();
    g.arc(84, 62, 9, Math.PI * 1.1, Math.PI * 1.9);
    g.stroke();
    smile();
  } else if (idx === 2) {
    g.lineWidth = 5;
    for (const x of [44, 84]) {
      g.beginPath();
      g.arc(x, 62, 10, Math.PI * 1.1, Math.PI * 1.9);
      g.stroke();
    }
    g.fillStyle = '#7a2230';
    g.beginPath();
    g.arc(64, 70, 15, 0, Math.PI);
    g.fill();
    g.fillStyle = '#ff8fa3';
    g.beginPath();
    g.arc(64, 82, 8, Math.PI, TAU);
    g.fill();
  } else {
    g.fillStyle = '#16161c';
    for (const x of [24, 68]) {
      g.beginPath();
      g.roundRect(x, 44, 38, 24, 6);
      g.fill();
    }
    g.fillRect(58, 50, 12, 5);
    g.fillStyle = 'rgba(255,255,255,0.35)';
    g.fillRect(30, 49, 14, 4);
    g.fillRect(74, 49, 14, 4);
    g.strokeStyle = '#2a1a14';
    smile();
  }
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  faceTex.set(idx, t);
  return t;
}
const faceMat = (idx) => new THREE.MeshBasicMaterial({ map: faceTexture(idx), transparent: true, polygonOffset: true, polygonOffsetFactor: -2 });

export function nameTag(text, color = '#ffffff') {
  const c = document.createElement('canvas');
  c.width = 512;
  c.height = 96;
  const g = c.getContext('2d');
  g.font = 'bold 54px system-ui, sans-serif';
  g.textAlign = 'center';
  g.textBaseline = 'middle';
  g.lineWidth = 10;
  g.strokeStyle = 'rgba(10,8,20,0.85)';
  g.strokeText(text, 256, 50);
  g.fillStyle = color;
  g.fillText(text, 256, 50);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, transparent: true, depthWrite: false }));
  s.scale.set(2.6, 0.49, 1);
  s.renderOrder = 20;
  return s;
}

// ---------- avatar do jogador / NPC ----------
export function buildAvatar(ap, eq, items, name = '', tagColor = '#ffffff') {
  const skin = SKIN[ap.skin] ?? SKIN[1];
  const hairC = HAIR_COLOR[ap.hairColor] ?? HAIR_COLOR[1];
  const body = eq.body ? items[eq.body] : null;
  const shirtC = eq.body === 'tunic_green' ? body.color : SHIRT[ap.shirt] ?? SHIRT[0];
  const pantsC = PANTS[ap.pants] ?? PANTS[0];
  const root = new THREE.Group();
  const rig = { root };
  const blob = new THREE.Mesh(new THREE.CircleGeometry(0.6, 20), new THREE.MeshBasicMaterial({ color: '#000', transparent: true, opacity: 0.25, depthWrite: false }));
  blob.rotation.x = -Math.PI / 2;
  blob.position.y = 0.03;
  root.add(blob);

  // pernas (pivô no quadril)
  const leg = (x) => {
    const pv = new THREE.Group();
    pv.position.set(x, 0.9, 0);
    mesh(rb(0.43, 0.6, 0.43, 0.12), std(pantsC), 0, -0.3, 0, pv);
    mesh(rb(0.46, 0.3, 0.54, 0.12), std('#4a3426'), 0, -0.75, 0.05, pv);
    root.add(pv);
    return pv;
  };
  rig.legL = leg(-0.22);
  rig.legR = leg(0.22);

  // tronco
  const torso = new THREE.Group();
  torso.position.set(0, 1.35, 0);
  root.add(torso);
  rig.torso = torso;
  mesh(rb(0.92, 0.92, 0.48, 0.16), std(shirtC), 0, 0, 0, torso);
  mesh(rb(0.94, 0.12, 0.5, 0.05), std('#2d2430'), 0, -0.38, 0, torso);
  mesh(rb(0.14, 0.12, 0.04, 0.02), glow('#ffd24a', 0.5), 0, -0.38, 0.26, torso);
  if (eq.body === 'armor_iron') {
    mesh(rb(1.0, 0.8, 0.56, 0.16), std('#c9d1df', { metalness: 0.55, roughness: 0.3 }), 0, 0.06, 0.02, torso);
    mesh(rb(0.5, 0.3, 0.06, 0.05), glow('#ffd24a', 0.4), 0, 0.12, 0.31, torso);
    for (const sx of [-1, 1]) mesh(rb(0.46, 0.3, 0.5, 0.14), std('#d7deea', { metalness: 0.55, roughness: 0.3 }), sx * 0.62, 0.4, 0, torso);
  } else if (eq.body === 'armor_shadow') {
    mesh(rb(1.0, 0.82, 0.54, 0.16), std('#2f2a5e', { roughness: 0.4 }), 0, 0.05, 0.01, torso);
    mesh(new THREE.OctahedronGeometry(0.1), glow('#b79bff', 1.8), 0, 0.12, 0.3, torso);
    mesh(rb(1.02, 0.07, 0.56, 0.03), glow('#9b6bff', 1.2), 0, 0.46, 0, torso);
  }

  // braços (manga na cor da camisa, antebraço na cor da pele)
  const arm = (x) => {
    const pv = new THREE.Group();
    pv.position.set(x, 1.72, 0);
    mesh(rb(0.38, 0.46, 0.38, 0.12), std(eq.body === 'armor_iron' ? '#c9d1df' : shirtC, eq.body === 'armor_iron' ? { metalness: 0.5, roughness: 0.3 } : {}), 0, -0.23, 0, pv);
    mesh(rb(0.36, 0.5, 0.36, 0.12), std(skin), 0, -0.6, 0, pv);
    root.add(pv);
    return pv;
  };
  rig.armL = arm(-0.67);
  rig.armR = arm(0.67);

  // cabeça
  const head = new THREE.Group();
  head.position.set(0, 2.2, 0);
  root.add(head);
  rig.head = head;
  mesh(rb(0.72, 0.68, 0.68, 0.24), std(skin), 0, 0, 0, head);
  const face = new THREE.Mesh(new THREE.PlaneGeometry(0.62, 0.62), faceMat(ap.face));
  face.position.set(0, -0.02, 0.347);
  head.add(face);
  const hc = std(hairC, { roughness: 0.7 });
  const hasHat = !!eq.head;
  const hs = ap.hair;
  if (!hasHat || hs === 2) {
    if (hs !== 4) mesh(rb(0.78, 0.26, 0.76, 0.12), hc, 0, 0.3, -0.01, head);
    if (hs === 0) {
      mesh(rb(0.78, 0.4, 0.2, 0.1), hc, 0, 0.1, -0.32, head);
      mesh(rb(0.7, 0.12, 0.14, 0.05), hc, 0, 0.26, 0.3, head);
    }
    if (hs === 1) for (let i = 0; i < 5; i++) mesh(new THREE.ConeGeometry(0.1, 0.34, 6), hc, -0.28 + i * 0.14, 0.52, -0.02 + (i % 2) * 0.06, head);
    if (hs === 2) {
      mesh(rb(0.8, 0.95, 0.22, 0.1), hc, 0, -0.18, -0.33, head);
      for (const sx of [-1, 1]) mesh(rb(0.12, 0.7, 0.5, 0.05), hc, sx * 0.4, -0.08, -0.1, head);
    }
    if (hs === 3) {
      mesh(rb(0.78, 0.4, 0.2, 0.1), hc, 0, 0.1, -0.32, head);
      mesh(new THREE.SphereGeometry(0.22, 12, 10), hc, 0, 0.58, -0.05, head);
    }
  }

  // acessórios de cabeça
  const ih = eq.head;
  if (ih === 'hat_cloth') {
    mesh(new THREE.CylinderGeometry(0.62, 0.62, 0.05, 24), std('#9b6bd6'), 0, 0.34, 0, head);
    const cone = mesh(new THREE.ConeGeometry(0.4, 0.85, 16), std('#9b6bd6'), 0, 0.78, 0, head);
    cone.rotation.z = -0.1;
    mesh(new THREE.CylinderGeometry(0.41, 0.44, 0.12, 16), std('#5b3aa0'), 0, 0.42, 0, head);
    mesh(new THREE.OctahedronGeometry(0.09), glow('#ffe066', 1.6), 0, 0.44, 0.42, head);
  } else if (ih === 'helm_iron') {
    mesh(rb(0.84, 0.62, 0.8, 0.28), std('#c4ccda', { metalness: 0.6, roughness: 0.3 }), 0, 0.14, 0, head);
    mesh(rb(0.1, 0.3, 0.06, 0.03), std('#c4ccda', { metalness: 0.6, roughness: 0.3 }), 0, 0.08, 0.42, head);
    mesh(rb(0.08, 0.26, 0.74, 0.03), std('#e8564f'), 0, 0.52, 0, head);
  } else if (ih === 'crown_gold' || ih === 'crown_hero') {
    const big = ih === 'crown_hero';
    const gold = glow('#ffd24a', 0.5);
    mesh(new THREE.CylinderGeometry(0.4, 0.43, 0.2, 14, 1, true), gold, 0, 0.44, 0, head).material.side = THREE.DoubleSide;
    for (let i = 0; i < 6; i++) {
      const a = (i / 6) * TAU;
      mesh(new THREE.ConeGeometry(0.075, big ? 0.38 : 0.26, 5), gold, Math.cos(a) * 0.4, 0.66 + (big ? 0.06 : 0), Math.sin(a) * 0.4, head);
      mesh(new THREE.SphereGeometry(0.045, 8, 6), glow(i % 2 ? '#ff4d6d' : '#4dd2ff', 1.6), Math.cos(a) * 0.41, 0.52, Math.sin(a) * 0.41, head);
    }
  } else if (ih === 'cap_red') {
    mesh(rb(0.78, 0.3, 0.76, 0.16), std('#e8564f'), 0, 0.32, 0, head);
    mesh(rb(0.62, 0.06, 0.34, 0.03), std('#c8403a'), 0, 0.2, 0.5, head);
  } else if (ih === 'bunny_ears') {
    for (const sx of [-1, 1]) {
      const e = mesh(new THREE.CapsuleGeometry(0.1, 0.5, 6, 10), std('#ffd0e6'), sx * 0.2, 0.75, 0, head);
      e.rotation.z = -sx * 0.18;
      mesh(new THREE.CapsuleGeometry(0.05, 0.36, 4, 8), std('#ff9fc0'), sx * 0.2, 0.75, 0.07, head).rotation.z = -sx * 0.18;
    }
  } else if (ih === 'top_hat') {
    mesh(new THREE.CylinderGeometry(0.55, 0.55, 0.06, 20), std('#2b2f4a'), 0, 0.36, 0, head);
    mesh(new THREE.CylinderGeometry(0.34, 0.36, 0.55, 18), std('#2b2f4a'), 0, 0.66, 0, head);
    mesh(new THREE.CylinderGeometry(0.365, 0.365, 0.1, 18), std('#d8404f'), 0, 0.5, 0, head);
  }

  // capa / asas / mochila
  const eb = eq.back;
  rig.hasCape = false;
  if (eb === 'cape_red' || eq.body === 'armor_shadow') {
    const cg = new THREE.PlaneGeometry(0.95, 1.25, 6, 8);
    const cape = new THREE.Mesh(cg, std(eb === 'cape_red' ? '#d8404f' : '#4a3f94', { side: THREE.DoubleSide, roughness: 0.8 }));
    cape.position.set(0, -0.1, -0.3);
    cape.castShadow = true;
    torso.add(cape);
    rig.cape = cape;
    rig.capeBase = Float32Array.from(cg.attributes.position.array);
  }
  if (eb === 'wings_angel') {
    rig.wings = [];
    for (const sx of [-1, 1]) {
      const w = new THREE.Group();
      w.position.set(sx * 0.2, 0.2, -0.3);
      for (let i = 0; i < 4; i++) {
        const f = mesh(rb(0.2, 0.95 - i * 0.12, 0.06, 0.06), std('#ffffff', { emissive: '#bfe9ff', emissiveIntensity: 0.25 }), sx * (0.2 + i * 0.2), 0.2 - i * 0.05, 0, w);
        f.rotation.z = -sx * (0.25 + i * 0.1);
      }
      torso.add(w);
      rig.wings.push([w, sx]);
    }
  }
  if (eb === 'backpack') {
    mesh(rb(0.7, 0.8, 0.34, 0.1), std('#8a5a3a'), 0, -0.02, -0.4, torso);
    mesh(rb(0.5, 0.3, 0.1, 0.05), std('#6b432c'), 0, -0.1, -0.6, torso);
    for (const sx of [-1, 1]) mesh(rb(0.1, 0.8, 0.06, 0.03), std('#3a2a20'), sx * 0.26, 0.04, 0.26, torso);
  }

  // arma (mão direita) e ferramenta (mão esquerda)
  const wp = eq.weapon;
  if (wp) {
    const w = new THREE.Group();
    const col = items[wp].color;
    mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.3, 8), std('#5a3a1e'), 0, 0.02, 0, w);
    if (wp === 'axe_titan') {
      mesh(new THREE.CylinderGeometry(0.05, 0.05, 1.4, 8), std('#5a3a1e'), 0, 0.6, 0, w);
      for (const s of [-1, 1]) mesh(rb(0.5, 0.5, 0.08, 0.1), glow('#7b5cff', 0.7), s * 0.28, 1.15, 0, w);
      mesh(new THREE.SphereGeometry(0.07, 8, 6), glow('#c9b8ff', 2), 0, 1.15, 0, w);
    } else {
      mesh(rb(0.4, 0.08, 0.12, 0.03), std('#d9b24a', { metalness: 0.7 }), 0, 0.22, 0, w);
      const bc = wp === 'sword_wood' ? std(col) : wp === 'sword_flame' ? glow('#ff7a2a', 1.0) : std('#e3e8f2', { metalness: 0.8, roughness: 0.25 });
      const len = wp === 'sword_wood' ? 0.85 : 1.1;
      mesh(rb(0.14, len, 0.05, 0.02), bc, 0, 0.26 + len / 2, 0, w);
      mesh(new THREE.ConeGeometry(0.09, 0.2, 4), bc, 0, 0.26 + len + 0.08, 0, w).rotation.y = Math.PI / 4;
    }
    w.position.set(0.04, -0.82, 0.12);
    w.rotation.set(0.5, 0, -0.1);
    rig.armR.add(w);
    rig.weapon = w;
    rig.flame = wp === 'sword_flame';
  }
  const tl = eq.tool;
  if (tl === 'lantern') {
    const t = new THREE.Group();
    t.position.set(0, -0.85, 0.12);
    mesh(rb(0.26, 0.34, 0.26, 0.06), std('#3a3a48'), 0, 0, 0, t);
    rig.glowTool = mesh(new THREE.SphereGeometry(0.1, 10, 8), glow('#ffe08a', 2), 0, 0, 0, t);
    rig.armL.add(t);
  } else if (tl === 'magnet') {
    const t = new THREE.Group();
    t.position.set(0, -0.85, 0.12);
    const u = mesh(new THREE.TorusGeometry(0.17, 0.06, 8, 14, Math.PI), std('#e8564f'), 0, 0, 0, t);
    u.rotation.z = Math.PI;
    for (const sx of [-1, 1]) mesh(new THREE.CylinderGeometry(0.062, 0.062, 0.1, 8), std('#eef2f8'), sx * 0.17, 0.05, 0, t);
    rig.armL.add(t);
  } else if (tl === 'lucky_charm') {
    rig.charm = mesh(new THREE.OctahedronGeometry(0.2), glow('#46e0a0', 1.6), -0.95, 2.5, 0, root);
  }

  if (name) {
    const tag = nameTag(name, tagColor);
    tag.position.set(0, 3.25, 0);
    root.add(tag);
    rig.tag = tag;
  }
  return rig;
}

// s: { moving, air, swing(0..1, 0 = parado), t, dt }
export function animateAvatar(rig, s) {
  const t = s.t;
  const w = s.moving && !s.air ? Math.sin(t * 10) * 0.95 : 0;
  if (s.air) {
    rig.legL.rotation.x = -0.5;
    rig.legR.rotation.x = 0.5;
    rig.armL.rotation.x = -2.4;
    rig.armR.rotation.x = s.swing > 0 ? -2.6 + s.swing * 3 : -2.4;
  } else {
    rig.legL.rotation.x = w;
    rig.legR.rotation.x = -w;
    rig.armL.rotation.x = -w * 0.9;
    rig.armR.rotation.x = s.swing > 0 ? -2.6 + s.swing * 3 : w * 0.9;
  }
  rig.armL.rotation.z = 0.08;
  rig.armR.rotation.z = -0.08;
  rig.torso.rotation.y = s.swing > 0 ? (0.5 - s.swing) * 0.6 : 0;
  rig.torso.position.y = 1.35 + (s.moving && !s.air ? Math.abs(Math.sin(t * 10)) * 0.05 : Math.sin(t * 2) * 0.012);
  rig.head.position.y = rig.torso.position.y + 0.85;
  rig.head.rotation.x = s.moving ? 0.06 : 0;
  if (rig.cape) {
    const p = rig.cape.geometry.attributes.position;
    for (let i = 0; i < p.count; i++) {
      const y = rig.capeBase[i * 3 + 1];
      const k = (0.65 - y) * 0.45;
      p.setZ(i, rig.capeBase[i * 3 + 2] - k * (s.moving ? 0.6 + Math.sin(t * 9 + y * 5) * 0.2 : 0.12 + Math.sin(t * 2 + y * 3) * 0.04));
    }
    p.needsUpdate = true;
  }
  if (rig.wings) for (const [w2, sx] of rig.wings) w2.rotation.y = sx * (0.35 + Math.sin(t * (s.air ? 12 : 2.4)) * (s.air ? 0.45 : 0.1));
  if (rig.charm) {
    rig.charm.rotation.y += s.dt * 2;
    rig.charm.position.y = 2.55 + Math.sin(t * 3) * 0.08;
  }
  if (rig.glowTool) rig.glowTool.material.emissiveIntensity = 1.6 + Math.sin(t * 9) * 0.3;
}

// ---------- criaturas ----------
function buildBase(type) {
  const g = new THREE.Group();
  const rig = { g, type, legs: [] };
  const blob = (r) => {
    const m = new THREE.Mesh(new THREE.CircleGeometry(r, 20), new THREE.MeshBasicMaterial({ color: '#000', transparent: true, opacity: 0.28, depthWrite: false }));
    m.rotation.x = -Math.PI / 2;
    m.position.y = 0.04;
    g.add(m);
  };
  const faceOn = (parent, w, h, x, y, z, draw) => {
    const c = document.createElement('canvas');
    c.width = c.height = 128;
    draw(c.getContext('2d'));
    const t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace;
    const f = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: t, transparent: true, polygonOffset: true, polygonOffsetFactor: -2 }));
    f.position.set(x, y, z);
    parent.add(f);
    return f;
  };
  const eyesHappy = (g2) => {
    g2.fillStyle = '#fff';
    for (const x of [40, 88]) {
      g2.beginPath();
      g2.ellipse(x, 56, 15, 19, 0, 0, TAU);
      g2.fill();
    }
    g2.fillStyle = '#1b1426';
    for (const x of [42, 90]) {
      g2.beginPath();
      g2.arc(x, 60, 8, 0, TAU);
      g2.fill();
    }
    g2.fillStyle = '#fff';
    for (const x of [45, 93]) {
      g2.beginPath();
      g2.arc(x, 56, 3, 0, TAU);
      g2.fill();
    }
    g2.strokeStyle = '#1b3a22';
    g2.lineWidth = 5;
    g2.lineCap = 'round';
    g2.beginPath();
    g2.arc(64, 84, 14, 0.15 * Math.PI, 0.85 * Math.PI);
    g2.stroke();
    g2.fillStyle = 'rgba(255,120,140,0.55)';
    for (const x of [18, 110]) {
      g2.beginPath();
      g2.ellipse(x, 84, 9, 5, 0, 0, TAU);
      g2.fill();
    }
  };
  const eyesAngry = (g2, col = '#ffd23a') => {
    g2.fillStyle = col;
    for (const x of [40, 88]) {
      g2.beginPath();
      g2.ellipse(x, 62, 13, 10, 0, 0, TAU);
      g2.fill();
    }
    g2.fillStyle = '#1b1426';
    for (const x of [40, 88]) {
      g2.beginPath();
      g2.arc(x, 62, 5, 0, TAU);
      g2.fill();
    }
    g2.strokeStyle = '#1b1426';
    g2.lineWidth = 8;
    g2.lineCap = 'round';
    g2.beginPath();
    g2.moveTo(22, 40);
    g2.lineTo(56, 52);
    g2.moveTo(106, 40);
    g2.lineTo(72, 52);
    g2.stroke();
    g2.lineWidth = 5;
    g2.beginPath();
    g2.arc(64, 106, 16, 1.15 * Math.PI, 1.85 * Math.PI);
    g2.stroke();
  };

  if (type === 'slime' || type === 'kingslime') {
    const king = type === 'kingslime';
    const sc = king ? 3.4 : 1;
    const body = mesh(rb(1.3 * sc, 1.0 * sc, 1.3 * sc, 0.45 * sc), std(king ? '#3ec7a8' : '#35c96a', { roughness: 0.25, emissive: king ? '#0a6a5a' : '#0a7a33', emissiveIntensity: 0.3 }), 0, 0.55 * sc, 0, g);
    rig.body = body;
    faceOn(body, 1.0 * sc, 1.0 * sc, 0, 0.02 * sc, 0.66 * sc, king ? (g2) => eyesAngry(g2, '#ff6a3a') : eyesHappy);
    mesh(new THREE.ConeGeometry(0.12 * sc, 0.32 * sc, 5), std('#2fa85a'), 0, 0.62 * sc, 0, body).rotation.z = 0.3;
    mesh(new THREE.SphereGeometry(0.16 * sc, 10, 8).scale(1, 0.5, 0.6), new THREE.MeshBasicMaterial({ color: '#d6ffe0', transparent: true, opacity: 0.55 }), -0.34 * sc, 0.34 * sc, 0.5 * sc, body);
    if (king) {
      const gold = glow('#ffd24a', 0.6);
      mesh(new THREE.CylinderGeometry(0.9, 1.0, 0.5, 12, 1, true), gold, 0, 1.48 * sc * 0.5 + 1.2, 0, body).material.side = THREE.DoubleSide;
      for (let i = 0; i < 7; i++) {
        const a = (i / 7) * TAU;
        mesh(new THREE.ConeGeometry(0.2, 0.7, 5), gold, Math.cos(a) * 0.95, 2.4, Math.sin(a) * 0.95, body);
        mesh(new THREE.SphereGeometry(0.1, 8, 6), glow(i % 2 ? '#ff4d6d' : '#4dd2ff', 2), Math.cos(a) * 0.98, 1.95, Math.sin(a) * 0.98, body);
      }
    }
    rig.r = 0.85 * sc;
    rig.barY = 1.8 * sc + (king ? 1.2 : 0);
    rig.baseY = 0.55 * sc;
    blob(0.9 * sc);
  } else if (type === 'brute') {
    const body = mesh(rb(1.9, 1.6, 1.2, 0.4), std('#cf5a45'), 0, 1.5, 0, g);
    rig.body = body;
    mesh(rb(1.2, 0.9, 0.2, 0.1), std('#f0b894'), 0, -0.1, 0.55, body);
    const head = mesh(rb(1.0, 0.85, 0.85, 0.3), std('#cf5a45'), 0, 1.35, 0.1, body);
    faceOn(head, 0.9, 0.9, 0, 0, 0.435, (g2) => eyesAngry(g2));
    for (const sx of [-1, 1]) {
      mesh(new THREE.ConeGeometry(0.17, 0.6, 7), std('#efe6cf'), sx * 0.4, 0.62, 0, head).rotation.z = -sx * 0.4;
      mesh(new THREE.ConeGeometry(0.07, 0.24, 6), std('#fff6e0'), sx * 0.22, -0.34, 0.44, head).rotation.x = Math.PI;
    }
    rig.armL = new THREE.Group();
    rig.armR = new THREE.Group();
    for (const [a, x] of [[rig.armL, -1.2], [rig.armR, 1.2]]) {
      a.position.set(x, 2.1, 0);
      mesh(rb(0.55, 1.2, 0.55, 0.2), std('#cf5a45'), 0, -0.55, 0, a);
      mesh(new THREE.SphereGeometry(0.34, 10, 8), std('#b04535'), 0, -1.2, 0, a);
      g.add(a);
    }
    const club = new THREE.Group();
    club.position.set(0, -1.2, 0.2);
    mesh(new THREE.CylinderGeometry(0.13, 0.22, 1.5, 8), std('#6b432c'), 0, 0.6, 0, club);
    for (let i = 0; i < 6; i++) {
      const a = (i / 6) * TAU;
      const sp = mesh(new THREE.ConeGeometry(0.07, 0.24, 5), std('#c9d1df', { metalness: 0.7 }), Math.cos(a) * 0.22, 1.1 + (i % 2) * 0.22, Math.sin(a) * 0.22, club);
      sp.rotation.set(Math.sin(a) * 1.4, 0, -Math.cos(a) * 1.4);
    }
    club.rotation.x = 0.5;
    rig.armR.add(club);
    for (const sx of [-1, 1]) mesh(rb(0.6, 0.8, 0.6, 0.2), std('#b04535'), sx * 0.5, 0.4, 0, g);
    g.scale.setScalar(0.85);
    rig.r = 1.15;
    rig.barY = 3.4;
    rig.baseY = 1.5;
    blob(1.3);
  } else if (type === 'wolf') {
    const fur = std('#8e949f');
    const body = mesh(rb(0.9, 0.9, 1.9, 0.3), fur, 0, 1.0, 0, g);
    rig.body = body;
    mesh(rb(0.7, 0.5, 0.8, 0.2), std('#d9dde4'), 0, -0.2, 0.3, body);
    const head = mesh(rb(0.8, 0.7, 0.8, 0.25), fur, 0, 0.35, 1.0, body);
    mesh(rb(0.42, 0.34, 0.5, 0.12), std('#d9dde4'), 0, -0.12, 0.55, head);
    mesh(new THREE.SphereGeometry(0.09, 8, 6), std('#16161c'), 0, -0.02, 0.82, head);
    faceOn(head, 0.7, 0.7, 0, 0.05, 0.405, (g2) => {
      g2.fillStyle = '#ffd23a';
      for (const x of [34, 94]) {
        g2.beginPath();
        g2.ellipse(x, 48, 11, 8, 0, 0, TAU);
        g2.fill();
      }
      g2.fillStyle = '#16161c';
      for (const x of [34, 94]) {
        g2.beginPath();
        g2.arc(x, 48, 4, 0, TAU);
        g2.fill();
      }
      g2.strokeStyle = '#16161c';
      g2.lineWidth = 7;
      g2.lineCap = 'round';
      g2.beginPath();
      g2.moveTo(14, 26);
      g2.lineTo(48, 40);
      g2.moveTo(114, 26);
      g2.lineTo(80, 40);
      g2.stroke();
    });
    for (const sx of [-1, 1]) mesh(new THREE.ConeGeometry(0.17, 0.4, 4), fur, sx * 0.26, 0.5, -0.05, head);
    const tail = mesh(rb(0.3, 0.3, 0.9, 0.12), fur, 0, 0.3, -1.2, body);
    tail.rotation.x = -0.5;
    for (const [x, z] of [[-0.3, 0.7], [0.3, 0.7], [-0.3, -0.7], [0.3, -0.7]]) {
      const pv = new THREE.Group();
      pv.position.set(x, 0.55, z);
      mesh(rb(0.26, 0.6, 0.28, 0.1), fur, 0, -0.3, 0, pv);
      g.add(pv);
      rig.legs.push(pv);
    }
    rig.r = 1.0;
    rig.barY = 2.3;
    rig.baseY = 1.0;
    blob(1.0);
  } else if (type === 'scorpion') {
    const shell = std('#c8643a');
    const body = mesh(rb(1.3, 0.55, 1.7, 0.22), shell, 0, 0.7, 0, g);
    rig.body = body;
    faceOn(body, 0.8, 0.5, 0, 0.12, 0.865, (g2) => eyesAngry(g2, '#ffe066'));
    for (const sx of [-1, 1]) {
      const claw = new THREE.Group();
      claw.position.set(sx * 0.8, 0.05, 1.0);
      mesh(rb(0.22, 0.22, 0.6, 0.08), shell, 0, 0, 0.1, claw);
      mesh(rb(0.5, 0.3, 0.45, 0.1), std('#a84f2c'), 0, 0, 0.55, claw);
      body.add(claw);
    }
    let y = 0.1;
    let z = -0.8;
    for (let i = 0; i < 5; i++) {
      const seg = mesh(rb(0.42 - i * 0.04, 0.42 - i * 0.04, 0.46, 0.14), shell, 0, y, z, body);
      seg.rotation.x = -0.5 - i * 0.15;
      y += 0.28;
      z -= 0.2 - i * 0.03;
    }
    mesh(new THREE.ConeGeometry(0.12, 0.4, 5), glow('#ff4d2a', 1.2), 0, y + 0.15, z + 0.1, body).rotation.x = -2.4;
    for (const sx of [-1, 1]) {
      for (const lz of [-0.5, -0.1, 0.3, 0.7]) {
        const pv = new THREE.Group();
        pv.position.set(sx * 0.62, 0.55, lz);
        mesh(rb(0.5, 0.12, 0.12, 0.04), std('#a84f2c'), sx * 0.25, -0.1, 0, pv).rotation.z = sx * -0.5;
        g.add(pv);
        rig.legs.push(pv);
      }
    }
    rig.r = 0.9;
    rig.barY = 1.8;
    rig.baseY = 0.7;
    blob(0.95);
  } else if (type === 'skeleton') {
    const bone = std('#ece7d8');
    const body = mesh(rb(0.8, 0.9, 0.42, 0.12), bone, 0, 1.4, 0, g);
    rig.body = body;
    for (let i = 0; i < 3; i++) mesh(rb(0.6, 0.06, 0.44, 0.02), std('#8a8473'), 0, 0.18 - i * 0.2, 0.01, body);
    const head = mesh(rb(0.66, 0.62, 0.6, 0.2), bone, 0, 0.82, 0, body);
    faceOn(head, 0.6, 0.6, 0, 0, 0.31, (g2) => {
      g2.fillStyle = '#16161c';
      for (const x of [40, 88]) {
        g2.beginPath();
        g2.ellipse(x, 52, 15, 17, 0, 0, TAU);
        g2.fill();
      }
      g2.fillStyle = '#ff5a3a';
      for (const x of [40, 88]) {
        g2.beginPath();
        g2.arc(x, 54, 5, 0, TAU);
        g2.fill();
      }
      g2.fillStyle = '#16161c';
      g2.fillRect(46, 92, 36, 6);
      g2.fillStyle = '#ece7d8';
      for (let i = 0; i < 4; i++) g2.fillRect(50 + i * 9, 90, 3, 10);
    });
    rig.armL = new THREE.Group();
    rig.armR = new THREE.Group();
    for (const [a, x] of [[rig.armL, -0.58], [rig.armR, 0.58]]) {
      a.position.set(x, 1.8, 0);
      mesh(rb(0.22, 0.85, 0.22, 0.08), bone, 0, -0.4, 0, a);
      g.add(a);
    }
    const sw = new THREE.Group();
    sw.position.set(0, -0.85, 0.1);
    mesh(rb(0.12, 0.9, 0.04, 0.02), std('#8a8a92', { metalness: 0.6 }), 0, 0.55, 0, sw);
    mesh(rb(0.3, 0.07, 0.08, 0.02), std('#6b432c'), 0, 0.1, 0, sw);
    sw.rotation.x = 0.6;
    rig.armR.add(sw);
    for (const x of [-0.2, 0.2]) {
      const pv = new THREE.Group();
      pv.position.set(x, 0.95, 0);
      mesh(rb(0.22, 0.95, 0.22, 0.08), bone, 0, -0.47, 0, pv);
      g.add(pv);
      rig.legs.push(pv);
    }
    rig.r = 0.8;
    rig.barY = 2.9;
    rig.baseY = 1.4;
    blob(0.8);
  } else if (type === 'bat') {
    const fur = std('#5b4a78');
    const body = mesh(rb(0.75, 0.7, 0.8, 0.28), fur, 0, 1.9, 0, g);
    rig.body = body;
    faceOn(body, 0.7, 0.7, 0, 0.04, 0.405, (g2) => eyesAngry(g2, '#ff6a6a'));
    for (const sx of [-1, 1]) {
      mesh(new THREE.ConeGeometry(0.14, 0.4, 4), fur, sx * 0.24, 0.5, 0, body);
      mesh(new THREE.ConeGeometry(0.05, 0.2, 4), std('#f2f0e8'), sx * 0.12, -0.38, 0.36, body).rotation.x = Math.PI;
    }
    rig.wings = [];
    for (const sx of [-1, 1]) {
      const w = new THREE.Group();
      w.position.set(sx * 0.35, 0.1, 0);
      mesh(rb(1.5, 0.05, 0.9, 0.02), std('#3d3254'), sx * 0.75, 0, -0.1, w);
      mesh(rb(1.5, 0.07, 0.07, 0.02), fur, sx * 0.75, 0.03, 0.3, w);
      body.add(w);
      rig.wings.push([w, sx]);
    }
    rig.r = 0.8;
    rig.barY = 2.9;
    rig.baseY = 1.9;
    rig.hover = 1.6;
    blob(0.6);
  } else if (type === 'spider') {
    const hide = std('#3b3347');
    const body = mesh(rb(1.0, 0.7, 1.1, 0.3), hide, 0, 0.85, 0.35, g);
    rig.body = body;
    const abd = mesh(rb(1.2, 1.0, 1.4, 0.4), std('#2b2536'), 0, 0.15, -1.2, body);
    mesh(rb(0.3, 0.05, 0.5, 0.02), glow('#ff3a3a', 1.2), 0, 0.51, -0.1, abd);
    faceOn(body, 0.9, 0.55, 0, 0.08, 0.565, (g2) => {
      g2.fillStyle = '#ff4d4d';
      for (const [x, y, r] of [[34, 60, 11], [94, 60, 11], [54, 36, 7], [74, 36, 7]]) {
        g2.beginPath();
        g2.arc(x, y, r, 0, TAU);
        g2.fill();
      }
    });
    for (const sx of [-1, 1]) mesh(new THREE.ConeGeometry(0.08, 0.35, 5), std('#e8e0f0'), sx * 0.2, -0.2, 0.6, body).rotation.x = Math.PI;
    for (const sx of [-1, 1]) {
      for (let i = 0; i < 4; i++) {
        const pv = new THREE.Group();
        pv.position.set(sx * 0.45, 0.8, 0.7 - i * 0.42);
        pv.rotation.y = sx * (0.35 - i * 0.22);
        mesh(rb(0.9, 0.11, 0.11, 0.04), hide, sx * 0.45, 0.1, 0, pv).rotation.z = sx * -0.45;
        mesh(rb(0.8, 0.1, 0.1, 0.04), hide, sx * 0.95, -0.25, 0, pv).rotation.z = sx * 0.9;
        g.add(pv);
        rig.legs.push(pv);
      }
    }
    rig.r = 0.95;
    rig.barY = 1.9;
    rig.baseY = 0.85;
    blob(1.1);
  } else if (type === 'golem') {
    const rock = std('#8c8f99', { roughness: 0.9 });
    const dark = std('#6c6f79', { roughness: 0.95 });
    const body = mesh(rb(1.9, 1.7, 1.3, 0.25), rock, 0, 2.0, 0, g);
    rig.body = body;
    for (const [x, y, z, w] of [[-0.5, 0.9, 0.2, 0.5], [0.45, 0.3, 0.68, 0.4], [0.3, -0.5, -0.7, 0.55]]) mesh(rb(w, w * 0.7, w, 0.1), dark, x, y, z, body);
    mesh(rb(0.8, 0.6, 0.15, 0.05), glow('#ffb347', 1.0), 0, 0.1, 0.66, body);
    const head = mesh(rb(1.0, 0.85, 0.9, 0.2), rock, 0, 1.3, 0.1, body);
    faceOn(head, 0.9, 0.9, 0, 0, 0.455, (g2) => {
      g2.fillStyle = '#ffb347';
      for (const x of [38, 90]) g2.fillRect(x - 12, 46, 24, 14);
      g2.fillStyle = '#1b1426';
      g2.fillRect(44, 92, 40, 7);
    });
    rig.armL = new THREE.Group();
    rig.armR = new THREE.Group();
    for (const [a, x] of [[rig.armL, -1.35], [rig.armR, 1.35]]) {
      a.position.set(x, 2.7, 0);
      mesh(rb(0.8, 1.7, 0.8, 0.2), rock, 0, -0.7, 0, a);
      mesh(rb(1.0, 0.8, 1.0, 0.2), dark, 0, -1.7, 0, a);
      g.add(a);
    }
    for (const sx of [-1, 1]) {
      const pv = new THREE.Group();
      pv.position.set(sx * 0.5, 1.2, 0);
      mesh(rb(0.8, 1.2, 0.8, 0.2), dark, 0, -0.55, 0, pv);
      g.add(pv);
      rig.legs.push(pv);
    }
    rig.r = 1.5;
    rig.barY = 4.5;
    rig.baseY = 2.0;
    blob(1.5);
  } else if (type === 'ghost') {
    const m = std('#cfe9ff', { transparent: true, opacity: 0.72, emissive: '#7fb8ff', emissiveIntensity: 0.55, roughness: 0.3 });
    const body = mesh(rb(1.1, 1.5, 0.9, 0.5), m, 0, 1.7, 0, g);
    rig.body = body;
    faceOn(body, 0.9, 0.9, 0, 0.25, 0.46, (g2) => {
      g2.fillStyle = '#1b1426';
      for (const x of [40, 88]) {
        g2.beginPath();
        g2.ellipse(x, 56, 11, 17, 0, 0, TAU);
        g2.fill();
      }
      g2.beginPath();
      g2.ellipse(64, 96, 10, 14, 0, 0, TAU);
      g2.fill();
    });
    for (let i = 0; i < 4; i++) mesh(new THREE.ConeGeometry(0.2, 0.7, 5), m, -0.45 + i * 0.3, -0.95, 0, body).rotation.x = Math.PI;
    for (const sx of [-1, 1]) mesh(rb(0.3, 0.8, 0.3, 0.14), m, sx * 0.72, -0.1, 0.1, body).rotation.z = sx * 0.5;
    rig.r = 0.9;
    rig.barY = 3.1;
    rig.baseY = 1.7;
    rig.hover = 0.7;
    blob(0.7);
  } else if (type === 'dragon') {
    const hide = std('#b3322e', { roughness: 0.45 });
    const belly = std('#e8b36a');
    const dark = std('#7a1f2e');
    const body = mesh(rb(2.6, 2.3, 4.4, 0.8), hide, 0, 3.4, 0, g);
    rig.body = body;
    mesh(rb(1.8, 1.4, 3.4, 0.5), belly, 0, -0.55, 0.15, body);
    for (let i = 0; i < 6; i++) mesh(new THREE.ConeGeometry(0.28, 0.8 - i * 0.05, 5), dark, 0, 1.35, 1.6 - i * 0.65, body);
    const neck = mesh(rb(1.0, 1.0, 1.8, 0.35), hide, 0, 0.85, 2.3, body);
    neck.rotation.x = -0.5;
    const head = mesh(rb(1.5, 1.2, 1.9, 0.45), hide, 0, 1.55, 3.1, body);
    head.rotation.x = 0.15;
    mesh(rb(1.2, 0.4, 1.4, 0.15), belly, 0, -0.5, 0.2, head);
    mesh(rb(0.8, 0.2, 0.9, 0.08), glow('#ff8a2a', 2), 0, -0.3, 0.55, head);
    faceOn(head, 1.4, 1.1, 0, 0.1, 0.96, (g2) => eyesAngry(g2, '#ffd23a'));
    for (const sx of [-1, 1]) {
      mesh(new THREE.ConeGeometry(0.22, 1.1, 6), std('#efe6cf'), sx * 0.55, 0.95, -0.4, head).rotation.x = -0.7;
      mesh(new THREE.ConeGeometry(0.1, 0.4, 5), std('#fff6e0'), sx * 0.4, -0.55, 0.9, head).rotation.x = Math.PI;
    }
    let tz = -2.4;
    let ty = 0.1;
    let ts = 1.5;
    for (let i = 0; i < 5; i++) {
      mesh(rb(ts, ts * 0.9, 1.5, 0.4), hide, 0, ty, tz, body);
      mesh(new THREE.ConeGeometry(0.18, 0.5, 5), dark, 0, ty + ts * 0.55, tz, body);
      tz -= 1.2;
      ty -= 0.15;
      ts *= 0.8;
    }
    rig.wings = [];
    for (const sx of [-1, 1]) {
      const w = new THREE.Group();
      w.position.set(sx * 1.2, 1.1, 0.4);
      mesh(rb(5.4, 0.12, 3.0, 0.05), dark, sx * 2.7, 0, -0.9, w);
      mesh(rb(5.4, 0.2, 0.2, 0.06), hide, sx * 2.7, 0.06, 0.55, w);
      for (const k of [1.4, 2.8, 4.2]) mesh(rb(0.12, 0.14, 2.8, 0.04), hide, sx * k, 0.05, -0.85, w);
      body.add(w);
      rig.wings.push([w, sx]);
    }
    for (const [x, z] of [[-1.0, 1.3], [1.0, 1.3], [-1.0, -1.3], [1.0, -1.3]]) {
      const pv = new THREE.Group();
      pv.position.set(x, 2.3, z);
      mesh(rb(0.8, 2.4, 0.9, 0.25), hide, 0, -1.1, 0, pv);
      mesh(rb(0.95, 0.35, 1.2, 0.1), dark, 0, -2.3, 0.15, pv);
      g.add(pv);
      rig.legs.push(pv);
    }
    rig.r = 3.8;
    rig.barY = 7.4;
    rig.baseY = 3.4;
    blob(3.4);
  }
  return rig;
}

// aplica cor (hue/sat/lum), tamanho e acessórios — é assim que poucas formas viram dezenas de monstros diferentes
export function buildCreature(id, def = {}) {
  const base = id === 'kingslime' ? 'kingslime' : (def.base ?? id);
  const look = def.look ?? {};
  const rig = buildBase(base);
  rig.id = id;
  const hsl = {};
  rig.g.traverse((o) => {
    if (!o.isMesh || !o.material?.isMeshStandardMaterial) return;
    const m = o.material.clone(); // material próprio: o brilho de dano não vaza para os outros
    if (look.hue || look.sat !== undefined || look.lum !== undefined) {
      for (const k of ['color', 'emissive']) {
        m[k].getHSL(hsl);
        const grey = hsl.s < 0.08 && !look.hue;
        const sat0 = look.hue && hsl.s < 0.25 && k === 'color' ? 0.4 : hsl.s; // ossos/pedra (quase cinza) ganham cor de verdade
        m[k].setHSL(grey ? hsl.h : (hsl.h + (look.hue ?? 0) / 360 + 1) % 1, Math.min(1, sat0 * (look.sat ?? 1)), Math.min(0.95, hsl.l * (k === 'color' ? (look.lum ?? 1) : 1)));
      }
    }
    o.material = m;
  });
  const gold = std('#ffd24a', { emissive: '#ffb300', emissiveIntensity: 0.6, metalness: 0.5 });
  const top = (rig.barY ?? 2) - 0.7;
  const w = (rig.r ?? 1) * 0.42;
  for (const acc of look.acc ?? []) {
    if (acc === 'horns') for (const sx of [-1, 1]) mesh(new THREE.ConeGeometry(0.16, 0.7, 6), std('#efe6cf'), sx * w, top + 0.2, 0.1, rig.g).rotation.z = -sx * 0.45;
    if (acc === 'crown') {
      for (let i = 0; i < 5; i++) {
        const a = (i / 5) * TAU;
        mesh(new THREE.ConeGeometry(0.11, 0.38, 5), gold, Math.cos(a) * w * 0.9, top + 0.45, Math.sin(a) * w * 0.9, rig.g);
      }
    }
    if (acc === 'spikes') for (let i = 0; i < 5; i++) mesh(new THREE.ConeGeometry(0.15, 0.55, 5), std('#cfc6b4'), 0, (rig.baseY ?? 1) + 0.6 + (i % 2) * 0.1, 0.5 - i * 0.28, rig.g).rotation.x = -0.3;
    if (acc === 'glow' && rig.body?.material) {
      rig.body.material.emissive.copy(rig.body.material.color);
      rig.body.material.emissiveIntensity = Math.max(rig.body.material.emissiveIntensity, 0.7);
    }
  }
  rig.g.scale.multiplyScalar(look.scale ?? 1);
  rig.gscale = rig.g.scale.x;
  return rig;
}

export function animateCreature(rig, e) {
  const { t, moving, atk } = e;
  if (rig.type === 'slime' || rig.type === 'kingslime') {
    const sq = Math.sin(t * 5);
    rig.body.scale.set(1 - sq * 0.07, 1 + sq * 0.09, 1 - sq * 0.07);
    rig.body.position.y = rig.baseY + Math.max(0, sq) * 0.12;
  } else if (rig.wings) {
    const f = Math.sin(t * (rig.type === 'dragon' ? 4 : 15));
    rig.body.position.y = rig.baseY + Math.sin(t * 3) * (rig.type === 'dragon' ? 0.08 : 0.15);
    for (const [w, sx] of rig.wings) w.rotation.z = sx * f * (rig.type === 'dragon' ? 0.45 : 0.8);
    rig.legs.forEach((l, i) => (l.rotation.x = moving ? Math.sin(t * 5 + (i % 2 ? Math.PI : 0)) * 0.5 : 0));
  } else if (rig.type === 'ghost') {
    rig.body.position.y = rig.baseY + Math.sin(t * 2.4) * 0.18;
    rig.body.rotation.z = Math.sin(t * 1.7) * 0.08;
  } else if (rig.type === 'spider') {
    rig.body.position.y = rig.baseY + (moving ? Math.abs(Math.sin(t * 12)) * 0.07 : 0);
    rig.legs.forEach((l, i) => (l.rotation.y = (l.userData.r0 ??= l.rotation.y) + (moving ? Math.sin(t * 14 + (i % 2) * Math.PI) * 0.32 : 0)));
  } else {
    rig.body.position.y = rig.baseY + (moving ? Math.abs(Math.sin(t * 6)) * 0.12 : Math.sin(t * 2) * 0.03);
    rig.legs.forEach((l, i) => (l.rotation.x = moving ? Math.sin(t * 9 + (i % 2 ? Math.PI : 0)) * 0.7 : 0));
    if (rig.armL) {
      rig.armL.rotation.x = moving ? Math.sin(t * 6) * 0.5 : 0;
      rig.armR.rotation.x = atk > 0 ? -2.2 + (1 - atk / 0.35) * 2.6 : moving ? -Math.sin(t * 6) * 0.5 : 0;
    }
  }
}

// ---------- NPCs fixos ----------
export function buildNpc(kind, items) {
  const presets = {
    mayor: { ap: { skin: 2, hair: 0, hairColor: 4, shirt: 6, pants: 6, face: 2 }, eq: { head: 'top_hat', back: 'cape_red', body: null }, name: 'Prefeito Ouro' },
    smith: { ap: { skin: 4, hair: 4, hairColor: 0, shirt: 9, pants: 1, face: 3 }, eq: { head: null, weapon: null }, name: 'Ferreiro Brasa' },
    farmer: { ap: { skin: 1, hair: 3, hairColor: 3, shirt: 2, pants: 2, face: 0 }, eq: { head: 'cap_red' }, name: 'Fazendeira Lia' },
    guard: { ap: { skin: 3, hair: 4, hairColor: 0, shirt: 7, pants: 3, face: 3 }, eq: { head: 'helm_iron', body: 'armor_iron', weapon: 'sword_iron' }, name: 'Guarda' },
    kid: { ap: { skin: 0, hair: 1, hairColor: 5, shirt: 1, pants: 7, face: 2 }, eq: { head: null }, name: 'Pipoca' },
  };
  const p = presets[kind];
  return { rig: buildAvatar(p.ap, p.eq, items, p.name, '#ffe08a'), name: p.name };
}
