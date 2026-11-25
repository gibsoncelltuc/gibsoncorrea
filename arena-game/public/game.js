// Cena 3D e jogabilidade. O cliente cuida de movimento/combate; QUALQUER ganho de moedas/XP é pedido ao servidor.
import * as THREE from './vendor/three.module.js';
import { net, call } from './net.js';

const ARENA = 34;
const rnd = (a, b) => a + Math.random() * (b - a);
const clampArena = (p, r = ARENA) => {
  const d = Math.hypot(p.x, p.z);
  if (d > r) {
    p.x *= r / d;
    p.z *= r / d;
  }
};
const M = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: 0.7, ...o });

let audio;
function beep(freq = 440, dur = 0.08, type = 'square', vol = 0.04) {
  try {
    audio ??= new AudioContext();
    const o = audio.createOscillator();
    const g = audio.createGain();
    o.type = type;
    o.frequency.value = freq;
    g.gain.value = vol;
    o.connect(g).connect(audio.destination);
    o.start();
    g.gain.exponentialRampToValueAtTime(0.0001, audio.currentTime + dur);
    o.stop(audio.currentTime + dur);
  } catch {
    /* áudio é opcional */
  }
}

export class Game {
  constructor(canvas, hooks = {}) {
    this.hooks = hooks;
    this.enabled = true;
    this.keys = new Set();
    this.yaw = 0.6;
    this.pitch = 0.5;
    this.dist = 10;
    this.last = performance.now();
    this.elapsed = 0;
    this.enemies = [];
    this.projectiles = [];
    this.effects = [];
    this.coins = [];
    this.cd = {};
    this.atkCd = 0;
    this.swing = 0;
    this.shield = 0;
    this.dashT = 0;
    this.spin = 0;
    this.dead = false;
    this.killQueue = [];
    this.killBusy = false;
    this.vel = new THREE.Vector3();
    this.facing = new THREE.Vector3(0, 0, 1);
    this.hudT = 0;

    const r = (this.renderer = new THREE.WebGLRenderer({ canvas, antialias: true }));
    r.setPixelRatio(Math.min(devicePixelRatio, 2));
    r.shadowMap.enabled = true;
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color('#9ec9ff');
    this.scene.fog = new THREE.Fog('#9ec9ff', 45, 120);
    this.camera = new THREE.PerspectiveCamera(60, 1, 0.1, 300);
    this.#world();
    this.player = new THREE.Group();
    this.scene.add(this.player);
    this.hp = this.maxHp = 100;
    this.refreshCharacter();
    this.#bind(canvas);
    this.resize();
    addEventListener('resize', () => this.resize());
    window.__game = this; // gancho para testes automatizados
    this.loop();
  }

  // ---------- mundo ----------
  #world() {
    const s = this.scene;
    s.add(new THREE.HemisphereLight('#dff0ff', '#5a7a4a', 1.0));
    const sun = new THREE.DirectionalLight('#fff4da', 1.6);
    sun.position.set(30, 50, 20);
    sun.castShadow = true;
    sun.shadow.mapSize.set(2048, 2048);
    Object.assign(sun.shadow.camera, { left: -48, right: 48, top: 48, bottom: -48, near: 1, far: 140 });
    s.add(sun);
    const c = document.createElement('canvas');
    c.width = c.height = 256;
    const g = c.getContext('2d');
    g.fillStyle = '#4d8a4a';
    g.fillRect(0, 0, 256, 256);
    for (let i = 0; i < 2600; i++) {
      g.fillStyle = `hsl(${95 + Math.random() * 30},${40 + Math.random() * 20}%,${28 + Math.random() * 14}%)`;
      g.fillRect(Math.random() * 256, Math.random() * 256, 2, 3);
    }
    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(30, 30);
    tex.colorSpace = THREE.SRGBColorSpace;
    const ground = new THREE.Mesh(new THREE.CircleGeometry(150, 48), new THREE.MeshStandardMaterial({ map: tex, roughness: 1 }));
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    s.add(ground);
    const sand = new THREE.Mesh(new THREE.CircleGeometry(ARENA + 1, 64), M('#d9c48c', { roughness: 1 }));
    sand.rotation.x = -Math.PI / 2;
    sand.position.y = 0.02;
    sand.receiveShadow = true;
    s.add(sand);
    const plat = new THREE.Mesh(new THREE.CylinderGeometry(5, 5.4, 0.3, 32), M('#8d93a3', { metalness: 0.2 }));
    plat.position.y = 0.15;
    plat.receiveShadow = true;
    s.add(plat);
    const emblem = new THREE.Mesh(new THREE.TorusGeometry(2.2, 0.18, 8, 40), M('#ffd24a', { metalness: 0.9, roughness: 0.25, emissive: '#6b4a00' }));
    emblem.rotation.x = Math.PI / 2;
    emblem.position.y = 0.35;
    s.add(emblem);
    for (let i = 0; i < 28; i++) {
      const a = (i / 28) * Math.PI * 2;
      const p = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 1.1, 5 + (i % 3), 8), M('#9aa0ad'));
      p.position.set(Math.cos(a) * (ARENA + 2), 2.6, Math.sin(a) * (ARENA + 2));
      p.castShadow = p.receiveShadow = true;
      s.add(p);
      const cap = new THREE.Mesh(new THREE.SphereGeometry(0.8, 10, 8), M('#ffd24a', { metalness: 0.8, roughness: 0.3, emissive: '#5a4000' }));
      cap.position.set(p.position.x, 5.6 + (i % 3), p.position.z);
      s.add(cap);
    }
    for (let i = 0; i < 46; i++) {
      const a = Math.random() * Math.PI * 2;
      const d = rnd(ARENA + 8, 90);
      const t = new THREE.Group();
      const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.55, 2.2, 6), M('#6b4a2b'));
      trunk.position.y = 1.1;
      trunk.castShadow = true;
      t.add(trunk);
      for (let k = 0; k < 3; k++) {
        const cone = new THREE.Mesh(new THREE.ConeGeometry(2.1 - k * 0.5, 2.6, 8), M(['#2f7a3d', '#378a45', '#3f9a50'][k]));
        cone.position.y = 3 + k * 1.5;
        cone.castShadow = true;
        t.add(cone);
      }
      t.position.set(Math.cos(a) * d, 0, Math.sin(a) * d);
      t.scale.setScalar(rnd(0.8, 1.5));
      s.add(t);
    }
  }

  // ---------- personagem (muda conforme o equipamento) ----------
  refreshCharacter() {
    const keepPos = this.player.position.clone();
    this.player.clear();
    const items = net.catalog.items;
    const st = net.state;
    const eq = (slot) => st.inventory.find((i) => i.iid === st.equipped[slot])?.itemId;
    const body = eq('body');
    const head = eq('head');
    const weapon = eq('weapon');
    const tool = eq('tool');
    const g = this.player;
    const part = (geo, mat, x, y, z, parent = g) => {
      const m = new THREE.Mesh(geo, mat);
      m.position.set(x, y, z);
      m.castShadow = true;
      parent.add(m);
      return m;
    };
    const bodyColor = body ? items[body].color : '#4a7bd0';
    part(new THREE.CapsuleGeometry(0.36, 0.62, 4, 10), M(bodyColor, { metalness: body && items[body].rarity !== 'comum' ? 0.55 : 0.05 }), 0, 1.15, 0);
    part(new THREE.SphereGeometry(0.3, 16, 12), M('#f1c9a5'), 0, 1.88, 0);
    for (const x of [-0.11, 0.11]) part(new THREE.SphereGeometry(0.045, 8, 6), M('#111'), x, 1.92, 0.27);
    const limb = (x, y, w, h, color) => {
      const pv = new THREE.Group();
      pv.position.set(x, y, 0);
      g.add(pv);
      part(new THREE.BoxGeometry(w, h, w), M(color), 0, -h / 2, 0, pv);
      return pv;
    };
    this.legL = limb(-0.16, 0.62, 0.22, 0.62, '#2e3550');
    this.legR = limb(0.16, 0.62, 0.22, 0.62, '#2e3550');
    this.armL = limb(-0.5, 1.5, 0.17, 0.6, bodyColor);
    this.armR = limb(0.5, 1.5, 0.17, 0.6, bodyColor);
    if (!head) part(new THREE.SphereGeometry(0.31, 12, 8, 0, Math.PI * 2, 0, Math.PI / 2), M('#4a2f1c'), 0, 1.9, -0.02);
    if (head === 'hat_cloth') {
      part(new THREE.CylinderGeometry(0.42, 0.42, 0.05, 16), M(items[head].color), 0, 2.1, 0);
      part(new THREE.ConeGeometry(0.28, 0.55, 14), M(items[head].color), 0, 2.4, 0);
    } else if (head === 'helm_iron') {
      part(new THREE.SphereGeometry(0.35, 14, 10, 0, Math.PI * 2, 0, Math.PI / 2), M(items[head].color, { metalness: 0.9, roughness: 0.3 }), 0, 1.9, 0);
    } else if (head === 'crown_gold') {
      const gold = M(items[head].color, { metalness: 1, roughness: 0.2, emissive: '#5a4000' });
      part(new THREE.CylinderGeometry(0.3, 0.3, 0.14, 12, 1, true), gold, 0, 2.12, 0);
      for (let i = 0; i < 6; i++) {
        const a = (i / 6) * Math.PI * 2;
        part(new THREE.ConeGeometry(0.06, 0.2, 6), gold, Math.cos(a) * 0.28, 2.28, Math.sin(a) * 0.28);
      }
    }
    if (weapon) {
      const w = new THREE.Group();
      const col = items[weapon].color;
      const metal = M(col, { metalness: 0.85, roughness: 0.25, emissive: weapon === 'sword_flame' ? '#a02000' : weapon === 'axe_titan' ? '#3a1d9a' : '#000' });
      if (weapon === 'axe_titan') {
        part(new THREE.CylinderGeometry(0.05, 0.05, 1.3, 8), M('#5a3a1e'), 0, 0.55, 0, w);
        part(new THREE.BoxGeometry(0.55, 0.38, 0.08), metal, 0.22, 1.1, 0, w);
        part(new THREE.BoxGeometry(0.55, 0.38, 0.08), metal, -0.22, 1.1, 0, w);
      } else {
        part(new THREE.CylinderGeometry(0.04, 0.04, 0.25, 8), M('#5a3a1e'), 0, 0.05, 0, w);
        part(new THREE.BoxGeometry(0.34, 0.06, 0.08), metal, 0, 0.2, 0, w);
        part(new THREE.BoxGeometry(0.08, weapon === 'sword_wood' ? 0.85 : 1.05, 0.03), weapon === 'sword_wood' ? M(col) : metal, 0, 0.7, 0, w);
      }
      w.position.set(0, -0.58, 0.05);
      w.rotation.x = 1.25;
      this.armR.add(w);
    }
    this.charm = null;
    if (tool) {
      const col = items[tool].color;
      const glow = M(col, { emissive: col, emissiveIntensity: 0.8 });
      if (tool === 'lantern') {
        const t = new THREE.Group();
        part(new THREE.BoxGeometry(0.22, 0.3, 0.22), M('#3b3b46'), 0, 0, 0, t);
        part(new THREE.SphereGeometry(0.12, 10, 8), glow, 0, 0, 0, t);
        t.position.set(0, -0.62, 0.1);
        this.armL.add(t);
      } else if (tool === 'magnet') {
        const t = part(new THREE.TorusGeometry(0.16, 0.055, 8, 14, Math.PI), M(col, { metalness: 0.6, roughness: 0.3 }), 0, -0.6, 0.1, this.armL);
        t.rotation.z = Math.PI;
      } else {
        this.charm = part(new THREE.OctahedronGeometry(0.2), glow, -0.75, 2.2, 0);
      }
    }
    this.player.position.copy(keepPos);
    const ratio = this.maxHp ? this.hp / this.maxHp : 1;
    this.maxHp = st.stats.hp;
    this.hp = Math.max(1, Math.round(this.maxHp * ratio));
  }

  // ---------- entrada ----------
  #bind(canvas) {
    const SK = { 1: 'dash', 2: 'fireball', 3: 'shield', 4: 'heal', 5: 'whirl' };
    addEventListener('keydown', (e) => {
      if (!this.enabled || e.target.matches?.('input,select,textarea')) return;
      const k = e.key.toLowerCase();
      this.keys.add(k);
      if (k === ' ') (e.preventDefault(), this.attack());
      if (SK[k]) this.useSkill(SK[k]);
      try {
        audio ??= new AudioContext(); // navegadores só liberam áudio depois de uma tecla/clique
      } catch {
        /* sem áudio */
      }
    });
    addEventListener('keyup', (e) => this.keys.delete(e.key.toLowerCase()));
    let drag = null;
    canvas.addEventListener('contextmenu', (e) => e.preventDefault());
    canvas.addEventListener('pointerdown', (e) => {
      if (!this.enabled) return;
      if (e.button === 2) drag = { x: e.clientX, y: e.clientY };
      else this.attack();
    });
    addEventListener('pointerup', () => (drag = null));
    addEventListener('pointermove', (e) => {
      if (!drag) return;
      this.yaw -= (e.clientX - drag.x) * 0.006;
      this.pitch = Math.min(1.2, Math.max(0.1, this.pitch + (e.clientY - drag.y) * 0.004));
      drag = { x: e.clientX, y: e.clientY };
    });
    canvas.addEventListener('wheel', (e) => (this.dist = Math.min(18, Math.max(5, this.dist + e.deltaY * 0.01))), { passive: true });
  }
  setEnabled(v) {
    this.enabled = v;
    if (!v) this.keys.clear();
  }
  resize() {
    const w = innerWidth;
    const h = innerHeight;
    this.renderer.setSize(w, h, false);
    this.camera.aspect = w / h;
    this.camera.updateProjectionMatrix();
  }
  get stats() {
    return net.state.stats;
  }

  // ---------- inimigos ----------
  spawnEnemy(type, x, z) {
    const def = net.catalog.enemies[type];
    const lv = net.state.level;
    const g = new THREE.Group();
    let body;
    if (type === 'slime') {
      body = new THREE.Mesh(new THREE.SphereGeometry(0.7, 16, 12), M('#5be37d', { transparent: true, opacity: 0.9, roughness: 0.2 }));
      body.position.y = 0.55;
      body.scale.set(1, 0.85, 1);
      for (const ex of [-0.22, 0.22]) {
        const eye = new THREE.Mesh(new THREE.SphereGeometry(0.1, 8, 6), M('#fff'));
        eye.position.set(ex, 0.7, 0.55);
        g.add(eye);
        const pu = new THREE.Mesh(new THREE.SphereGeometry(0.05, 6, 5), M('#111'));
        pu.position.set(ex, 0.7, 0.64);
        g.add(pu);
      }
    } else {
      body = new THREE.Mesh(new THREE.IcosahedronGeometry(1.0, 1), M('#b3382c', { flatShading: true }));
      body.position.y = 1.1;
      for (const hx of [-0.55, 0.55]) {
        const horn = new THREE.Mesh(new THREE.ConeGeometry(0.2, 0.7, 6), M('#e8e0c8'));
        horn.position.set(hx, 2.0, 0);
        horn.rotation.z = hx > 0 ? -0.4 : 0.4;
        g.add(horn);
        const eye = new THREE.Mesh(new THREE.SphereGeometry(0.12, 8, 6), M('#ffe066', { emissive: '#ffcc00' }));
        eye.position.set(hx * 0.5, 1.3, 0.9);
        g.add(eye);
      }
    }
    body.castShadow = true;
    g.add(body);
    const bar = new THREE.Group();
    const bg = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 0.14), new THREE.MeshBasicMaterial({ color: '#111', depthTest: false }));
    const fg = new THREE.Mesh(new THREE.PlaneGeometry(1.16, 0.1).translate(0.58, 0, 0), new THREE.MeshBasicMaterial({ color: '#46e0a0', depthTest: false }));
    fg.position.set(-0.58, 0, 0.01);
    bg.renderOrder = 10;
    fg.renderOrder = 11;
    bar.add(bg, fg);
    bar.position.y = type === 'slime' ? 1.7 : 2.9;
    g.add(bar);
    g.position.set(x, 0, z);
    this.scene.add(g);
    const hp = Math.round(def.hp * (1 + 0.1 * (lv - 1)));
    const e = { type, g, body, bar, fg, hp, max: hp, atk: def.atk * (1 + 0.05 * (lv - 1)), speed: def.speed, hitCd: 0, flash: 0, dying: 0, phase: Math.random() * 6, r: type === 'slime' ? 0.8 : 1.2 };
    this.enemies.push(e);
    return e;
  }
  #spawnLogic() {
    const lv = net.state.level;
    const target = 6 + Math.min(6, lv);
    while (this.enemies.filter((e) => !e.dying).length < target) {
      const a = Math.random() * Math.PI * 2;
      const d = rnd(14, ARENA - 2);
      const p = this.player.position;
      const pos = new THREE.Vector3(Math.cos(a) * d, 0, Math.sin(a) * d);
      if (pos.distanceTo(p) < 10) continue;
      this.spawnEnemy(Math.random() < Math.min(0.35, 0.05 * (lv - 1)) ? 'brute' : 'slime', pos.x, pos.z);
    }
  }
  nearestEnemy(range = 7) {
    let best = null;
    let bd = range;
    for (const e of this.enemies) {
      if (e.dying) continue;
      const d = e.g.position.distanceTo(this.player.position);
      if (d < bd) (bd = d), (best = e);
    }
    return best;
  }
  hitEnemy(e, dmg, color = '#fff') {
    if (e.dying) return;
    e.hp -= dmg;
    e.flash = 0.12;
    this.floatText(e.g.position.clone().setY(2), String(Math.round(dmg)), color);
    beep(180, 0.05, 'sawtooth');
    if (e.hp <= 0) {
      e.dying = 0.35;
      this.killQueue.push({ type: e.type, pos: e.g.position.clone() });
      this.#drain();
    }
  }
  // as recompensas são pedidas ao servidor, uma por vez, respeitando o intervalo mínimo dele
  async #drain() {
    if (this.killBusy) return;
    this.killBusy = true;
    while (this.killQueue.length) {
      const k = this.killQueue.shift();
      try {
        const r = await call('kill', { type: k.type });
        this.floatText(k.pos.clone().setY(2.4), r.coins ? `+${r.coins} 🪙  +${r.xp} XP` : `+${r.xp} XP (teto de moedas da hora)`, '#ffd24a');
        for (let i = 0; i < Math.min(10, r.coins); i++) this.dropCoin(k.pos);
        if (r.levelUp) this.hooks.toast?.('⬆ Você subiu de nível!');
        beep(880, 0.1, 'triangle');
      } catch (err) {
        if (err.code !== 'rapido') this.hooks.toast?.('⚠ ' + err.message);
      }
      await new Promise((r) => setTimeout(r, 380));
    }
    this.killBusy = false;
  }
  dropCoin(pos) {
    const c = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 0.06, 14), M('#ffd24a', { metalness: 0.9, roughness: 0.25, emissive: '#7a5600' }));
    c.rotation.x = Math.PI / 2;
    c.position.set(pos.x + rnd(-0.8, 0.8), 0.6, pos.z + rnd(-0.8, 0.8));
    this.scene.add(c);
    this.coins.push({ m: c, t: 0 });
  }

  // ---------- ações do jogador ----------
  attack() {
    if (this.dead || this.atkCd > 0 || !this.enabled) return;
    this.atkCd = 0.45;
    this.swing = 0.3;
    const t = this.nearestEnemy(6);
    if (t) this.facing.copy(t.g.position).sub(this.player.position).setY(0).normalize();
    const dmgBase = this.stats.atk;
    let hit = false;
    for (const e of this.enemies) {
      if (e.dying) continue;
      const to = e.g.position.clone().sub(this.player.position).setY(0);
      const d = to.length();
      if (d < 2.9 + e.r * 0.5 && to.normalize().dot(this.facing) > 0.15) {
        const crit = Math.random() < 0.1;
        this.hitEnemy(e, dmgBase * rnd(0.9, 1.1) * (crit ? 1.6 : 1), crit ? '#ffb300' : '#fff');
        e.g.position.addScaledVector(to, 0.7);
        hit = true;
      }
    }
    beep(hit ? 260 : 140, 0.05, 'square');
  }
  useSkill(id) {
    if (this.dead || !this.enabled) return;
    const lv = net.state.skills[id];
    const sk = net.catalog.skills[id];
    if (!lv) return this.hooks.toast?.(`Você ainda não aprendeu ${sk.name} (compre o pergaminho na Loja)`);
    if ((this.cd[id] ?? 0) > 0) return;
    this.cd[id] = sk.cd[lv - 1];
    const p = this.player.position;
    const t = this.nearestEnemy(14);
    if (id !== 'dash' && t) this.facing.copy(t.g.position).sub(p).setY(0).normalize();
    if (id === 'dash') (this.dashT = 0.22), (this.vel.copy(this.facing).multiplyScalar(22));
    if (id === 'fireball') {
      const m = new THREE.Mesh(new THREE.SphereGeometry(0.4, 12, 10), new THREE.MeshBasicMaterial({ color: '#ff7a1a' }));
      m.position.copy(p).setY(1.4).addScaledVector(this.facing, 1);
      this.scene.add(m);
      this.projectiles.push({ m, v: this.facing.clone().multiplyScalar(20), life: 1.4, dmg: sk.dmg[lv - 1] + this.stats.atk * 0.5 });
      beep(320, 0.15, 'sawtooth');
    }
    if (id === 'shield') this.shield = sk.dur[lv - 1];
    if (id === 'heal') {
      this.hp = Math.min(this.maxHp, this.hp + sk.heal[lv - 1]);
      this.floatText(p.clone().setY(2.6), `+${sk.heal[lv - 1]} ♥`, '#74f0a7');
      this.ring(p, '#74f0a7', 3);
      beep(660, 0.2, 'sine');
    }
    if (id === 'whirl') {
      this.spin = 0.5;
      this.ring(p, '#e0a0ff', 4.4);
      for (const e of this.enemies) if (!e.dying && e.g.position.distanceTo(p) < 4.6) this.hitEnemy(e, sk.dmg[lv - 1] + this.stats.atk * 0.4, '#e0a0ff');
      beep(200, 0.25, 'sawtooth');
    }
  }
  ring(pos, color, size) {
    const m = new THREE.Mesh(new THREE.RingGeometry(0.6, 0.9, 32), new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.8, side: THREE.DoubleSide }));
    m.rotation.x = -Math.PI / 2;
    m.position.set(pos.x, 0.1, pos.z);
    this.scene.add(m);
    this.effects.push({ m, t: 0, size });
  }
  hurt(n) {
    if (this.dead || this.dashT > 0) return;
    n = Math.max(1, Math.round(n - this.stats.def * 0.5)) * (this.shield > 0 ? 0.5 : 1);
    this.hp -= n;
    this.floatText(this.player.position.clone().setY(2.5), `-${Math.round(n)}`, '#ff6b6b');
    beep(100, 0.1, 'sawtooth');
    if (this.hp <= 0) {
      this.dead = true;
      this.hooks.dead?.(true);
      setTimeout(() => {
        this.hp = this.maxHp;
        this.player.position.set(0, 0, 0);
        this.dead = false;
        this.hooks.dead?.(false);
      }, 2500);
    }
  }
  floatText(world, text, color) {
    const v = world.clone().project(this.camera);
    if (v.z > 1) return;
    const el = document.createElement('div');
    el.className = 'float';
    el.textContent = text;
    el.style.color = color;
    el.style.left = `${((v.x + 1) / 2) * innerWidth}px`;
    el.style.top = `${((1 - v.y) / 2) * innerHeight}px`;
    document.body.append(el);
    setTimeout(() => el.remove(), 1000);
  }

  // ---------- laço principal ----------
  loop = () => {
    requestAnimationFrame(this.loop);
    const now = performance.now();
    const dt = Math.min((now - this.last) / 1000, 0.05);
    this.last = now;
    this.elapsed += dt;
    this.update(dt);
    this.renderer.render(this.scene, this.camera);
  };

  update(dt) {
    const t = this.elapsed;
    const p = this.player.position;
    for (const k of Object.keys(this.cd)) this.cd[k] = Math.max(0, this.cd[k] - dt);
    this.atkCd = Math.max(0, this.atkCd - dt);
    this.swing = Math.max(0, this.swing - dt);
    this.shield = Math.max(0, this.shield - dt);
    this.spin = Math.max(0, this.spin - dt);

    // movimento relativo à câmera
    let ix = 0;
    let iz = 0;
    if (this.enabled && !this.dead) {
      if (this.keys.has('w') || this.keys.has('arrowup')) iz -= 1;
      if (this.keys.has('s') || this.keys.has('arrowdown')) iz += 1;
      if (this.keys.has('a') || this.keys.has('arrowleft')) ix -= 1;
      if (this.keys.has('d') || this.keys.has('arrowright')) ix += 1;
      if (this.keys.has('q')) this.yaw += dt * 1.8;
      if (this.keys.has('e')) this.yaw -= dt * 1.8;
    }
    const moving = ix || iz;
    if (this.dashT > 0) {
      this.dashT -= dt;
      p.addScaledVector(this.vel, dt);
    } else if (moving) {
      const dir = new THREE.Vector3(ix, 0, iz).normalize();
      dir.applyAxisAngle(new THREE.Vector3(0, 1, 0), this.yaw);
      const sp = (6 + (this.stats.speed ?? 0)) * (this.keys.has('shift') ? 1.5 : 1);
      p.addScaledVector(dir, sp * dt);
      this.facing.lerp(dir, Math.min(1, dt * 14)).normalize();
    }
    clampArena(p);
    this.player.rotation.y = Math.atan2(this.facing.x, this.facing.z);
    const w = moving ? Math.sin(t * 11) * 0.8 : 0;
    this.legL.rotation.x = w;
    this.legR.rotation.x = -w;
    this.armL.rotation.x = -w * 0.7;
    this.armR.rotation.x = this.swing > 0 ? -2.2 + (1 - this.swing / 0.3) * 2.6 : w * 0.7;
    if (this.spin > 0) this.player.rotation.y += (1 - this.spin / 0.5) * Math.PI * 4;
    if (this.charm) (this.charm.rotation.y += dt * 2), (this.charm.position.y = 2.2 + Math.sin(t * 3) * 0.08);
    this.player.position.y = moving ? Math.abs(Math.sin(t * 11)) * 0.06 : 0;

    // inimigos
    this.#spawnLogic();
    for (const e of [...this.enemies]) {
      if (e.dying) {
        e.dying -= dt;
        e.g.scale.multiplyScalar(0.9);
        if (e.dying <= 0) {
          this.scene.remove(e.g);
          this.enemies.splice(this.enemies.indexOf(e), 1);
        }
        continue;
      }
      const to = p.clone().sub(e.g.position).setY(0);
      const d = to.length();
      if (!this.dead && d > 1.3) e.g.position.addScaledVector(to.normalize(), e.speed * dt);
      e.hitCd = Math.max(0, e.hitCd - dt);
      if (!this.dead && d < 1.5 + e.r * 0.4 && e.hitCd <= 0) (e.hitCd = 1.0), this.hurt(e.atk);
      for (const o of this.enemies) {
        if (o === e || o.dying) continue;
        const dd = e.g.position.distanceTo(o.g.position);
        if (dd < 1.2 && dd > 0.001) e.g.position.addScaledVector(e.g.position.clone().sub(o.g.position).setY(0).normalize(), dt * 2);
      }
      clampArena(e.g.position, ARENA - 0.5);
      e.phase += dt * 5;
      e.body.scale.y = (e.type === 'slime' ? 0.85 : 1) * (1 + Math.sin(e.phase) * 0.08);
      e.g.rotation.y = Math.atan2(to.x, to.z);
      e.flash = Math.max(0, e.flash - dt);
      e.body.material.emissive?.set(e.flash > 0 ? '#ffffff' : '#000000');
      e.fg.scale.x = Math.max(0.001, e.hp / e.max);
      e.bar.quaternion.copy(this.camera.quaternion);
    }

    // projéteis, efeitos, moedas
    for (const pr of [...this.projectiles]) {
      pr.m.position.addScaledVector(pr.v, dt);
      pr.life -= dt;
      const hit = this.enemies.find((e) => !e.dying && e.g.position.distanceTo(pr.m.position.clone().setY(0)) < e.r + 0.5);
      if (hit || pr.life <= 0) {
        if (hit) (this.hitEnemy(hit, pr.dmg, '#ff9a3a'), this.ring(pr.m.position, '#ff7a1a', 2.2));
        this.scene.remove(pr.m);
        this.projectiles.splice(this.projectiles.indexOf(pr), 1);
      }
    }
    for (const f of [...this.effects]) {
      f.t += dt * 2.5;
      f.m.scale.setScalar(1 + f.t * f.size);
      f.m.material.opacity = Math.max(0, 0.8 - f.t);
      if (f.t > 0.85) (this.scene.remove(f.m), this.effects.splice(this.effects.indexOf(f), 1));
    }
    const pickup = 2.5 + (this.stats.pickup ?? 0);
    for (const c of [...this.coins]) {
      c.t += dt;
      c.m.rotation.z += dt * 6;
      const d = c.m.position.distanceTo(p);
      if (d < pickup || c.t > 8) {
        c.m.position.lerp(p.clone().setY(1.2), Math.min(1, dt * 12));
        if (d < 0.8 || c.t > 8) (this.scene.remove(c.m), this.coins.splice(this.coins.indexOf(c), 1));
      }
    }

    // câmera
    const target = p.clone().setY(1.6);
    this.camera.position.set(target.x + Math.sin(this.yaw) * Math.cos(this.pitch) * this.dist, target.y + Math.sin(this.pitch) * this.dist, target.z + Math.cos(this.yaw) * Math.cos(this.pitch) * this.dist);
    this.camera.lookAt(target);

    this.hudT += dt;
    if (this.hudT > 0.1) {
      this.hudT = 0;
      this.hooks.hud?.({ hp: this.hp, max: this.maxHp, shield: this.shield > 0, cd: this.cd });
    }
  }
}
