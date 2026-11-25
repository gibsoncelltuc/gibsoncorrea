// Jogabilidade (movimento, combate, habilidades) sobre o visual de visuals.js.
// O cliente cuida do combate; QUALQUER ganho de moedas/XP é pedido ao servidor.
import * as THREE from 'three';
import { net, call } from './net.js';
import { ARENA, buildWorld, buildHero, animateHero, buildEnemy, Fx, createComposer, toon, mk } from './visuals.js';

const rnd = (a, b) => a + Math.random() * (b - a);
const clampArena = (p, r = ARENA) => {
  const d = Math.hypot(p.x, p.z);
  if (d > r) {
    p.x *= r / d;
    p.z *= r / d;
  }
};

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
    this.pitch = 0.42;
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
    this.dustT = 0;
    this.slow = 0;
    this.quality = localStorage.getItem('arena-q') ?? 'high';

    const r = (this.renderer = new THREE.WebGLRenderer({ canvas, antialias: true }));
    r.setPixelRatio(Math.min(devicePixelRatio, 2));
    r.shadowMap.enabled = true;
    r.shadowMap.type = THREE.PCFSoftShadowMap;
    r.toneMapping = THREE.ACESFilmicToneMapping;
    r.toneMappingExposure = 0.95;
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(52, 1, 0.1, 700);
    this.world = buildWorld(this.scene);
    this.fx = new Fx(this.scene);
    this.player = new THREE.Group();
    this.scene.add(this.player);
    this.hp = this.maxHp = 100;
    this.refreshCharacter();
    this.shieldMesh = new THREE.Mesh(new THREE.SphereGeometry(1.5, 24, 16), new THREE.MeshBasicMaterial({ color: '#7fd0ff', transparent: true, opacity: 0.22, blending: THREE.AdditiveBlending, depthWrite: false }));
    this.shieldMesh.visible = false;
    this.scene.add(this.shieldMesh);
    this.#bind(canvas);
    this.resize();
    addEventListener('resize', () => this.resize());
    createComposer(r, this.scene, this.camera).then((c) => ((this.composer = c), this.resize())).catch(() => (this.quality = 'low'));
    window.__game = this; // gancho para testes automatizados
    this.loop();
  }

  setQuality(q, say = true) {
    this.quality = q;
    localStorage.setItem('arena-q', q);
    if (say) this.hooks.toast?.(q === 'high' ? 'Gráficos: alto (brilho e suavização)' : 'Gráficos: modo desempenho');
  }

  // ---------- personagem ----------
  refreshCharacter() {
    const keep = this.player.position.clone();
    this.player.clear();
    const st = net.state;
    const eq = {};
    for (const slot of net.catalog.slots) eq[slot] = st.inventory.find((i) => i.iid === st.equipped[slot])?.itemId ?? null;
    this.rig = buildHero(eq, net.catalog.items, st.name);
    this.player.add(this.rig.root);
    this.player.position.copy(keep);
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
      if (k === 'p') this.setQuality(this.quality === 'high' ? 'low' : 'high');
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
      this.pitch = Math.min(1.2, Math.max(0.08, this.pitch + (e.clientY - drag.y) * 0.004));
      drag = { x: e.clientX, y: e.clientY };
    });
    canvas.addEventListener('wheel', (e) => (this.dist = Math.min(20, Math.max(5, this.dist + e.deltaY * 0.01))), { passive: true });
  }
  setEnabled(v) {
    this.enabled = v;
    if (!v) this.keys.clear();
  }
  resize() {
    const w = innerWidth;
    const h = innerHeight;
    this.renderer.setSize(w, h, false);
    this.composer?.setSize(w, h);
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
    const rig = buildEnemy(type);
    const g = rig.g;
    const bar = new THREE.Group();
    const bg = new THREE.Mesh(new THREE.PlaneGeometry(1.3, 0.16), new THREE.MeshBasicMaterial({ color: '#1b1426', depthTest: false }));
    const fg = new THREE.Mesh(new THREE.PlaneGeometry(1.24, 0.1).translate(0.62, 0, 0), new THREE.MeshBasicMaterial({ color: '#46e0a0', depthTest: false }));
    fg.position.set(-0.62, 0, 0.01);
    bg.renderOrder = 10;
    fg.renderOrder = 11;
    bar.add(bg, fg);
    bar.position.y = rig.barY;
    g.add(bar);
    g.position.set(x, 0, z);
    this.scene.add(g);
    const hp = Math.round(def.hp * (1 + 0.1 * (lv - 1)));
    const mat = rig.body.material;
    const e = { type, g, rig, body: rig.body, bar, fg, hp, max: hp, atk: def.atk * (1 + 0.05 * (lv - 1)), speed: def.speed, hitCd: 0, flash: 0, dying: 0, phase: Math.random() * 6, r: rig.r, em: mat.emissive.clone(), emI: mat.emissiveIntensity, atkAnim: 0 };
    this.enemies.push(e);
    return e;
  }
  #spawnLogic() {
    const lv = net.state.level;
    const target = 6 + Math.min(6, lv);
    while (this.enemies.filter((e) => !e.dying).length < target) {
      const a = Math.random() * Math.PI * 2;
      const d = rnd(14, ARENA - 3);
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
    this.floatText(e.g.position.clone().setY(2.2), String(Math.round(dmg)), color);
    this.fx.burst(e.g.position.clone().setY(1.1), { color: '#fff2a8', count: 9, speed: 5, life: 0.35, size: 0.32 });
    this.slow = 0.05; // pequena pausa de impacto
    beep(180, 0.05, 'sawtooth');
    if (e.hp <= 0) {
      e.dying = 0.4;
      this.fx.burst(e.g.position.clone().setY(0.9), { color: e.type === 'slime' ? '#74e590' : '#ff8a5a', count: 30, speed: 6.5, life: 0.75, size: 0.5 });
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
        this.floatText(k.pos.clone().setY(2.6), r.coins ? `+${r.coins} 🪙  +${r.xp} XP` : `+${r.xp} XP (teto de moedas da hora)`, '#ffd24a');
        for (let i = 0; i < Math.min(10, r.coins); i++) this.dropCoin(k.pos);
        if (r.levelUp) {
          this.hooks.toast?.('⬆ Você subiu de nível!');
          this.fx.burst(this.player.position.clone().setY(0.3), { color: '#ffe066', count: 70, speed: 6, life: 1.1, size: 0.55, gravity: -1.5 });
          this.ring(this.player.position, '#ffe066', 5);
        }
        beep(880, 0.1, 'triangle');
      } catch (err) {
        if (err.code !== 'rapido') this.hooks.toast?.('⚠ ' + err.message);
      }
      await new Promise((r) => setTimeout(r, 380));
    }
    this.killBusy = false;
  }
  dropCoin(pos) {
    const c = mk(new THREE.CylinderGeometry(0.25, 0.25, 0.07, 16), toon('#ffd24a', { emissive: '#ffb300', emissiveIntensity: 0.9 }), { outline: 0.02 });
    c.rotation.x = Math.PI / 2;
    c.position.set(pos.x + rnd(-0.9, 0.9), 0.7, pos.z + rnd(-0.9, 0.9));
    this.scene.add(c);
    this.coins.push({ m: c, t: 0, sp: rnd(0, 6) });
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
        e.g.position.addScaledVector(to, 0.8);
        hit = true;
      }
    }
    const at = this.player.position.clone().addScaledVector(this.facing, 1.6).setY(1.2);
    this.fx.burst(at, { color: '#ffffff', count: 5, speed: 3, life: 0.25, size: 0.25, gravity: 0 });
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
    if (id === 'dash') {
      this.dashT = 0.22;
      this.vel.copy(this.facing).multiplyScalar(22);
      this.fx.burst(p.clone().setY(0.4), { color: '#bfe9ff', count: 22, speed: 3, life: 0.5, size: 0.5, gravity: 0 });
    }
    if (id === 'fireball') {
      const g = new THREE.Group();
      g.add(new THREE.Mesh(new THREE.SphereGeometry(0.42, 14, 10), new THREE.MeshBasicMaterial({ color: '#ffb347' })));
      g.add(new THREE.Mesh(new THREE.SphereGeometry(0.62, 14, 10), new THREE.MeshBasicMaterial({ color: '#ff5a1a', transparent: true, opacity: 0.45, blending: THREE.AdditiveBlending, depthWrite: false })));
      g.position.copy(p).setY(1.4).addScaledVector(this.facing, 1);
      this.scene.add(g);
      this.projectiles.push({ m: g, v: this.facing.clone().multiplyScalar(20), life: 1.4, dmg: sk.dmg[lv - 1] + this.stats.atk * 0.5 });
      beep(320, 0.15, 'sawtooth');
    }
    if (id === 'shield') this.shield = sk.dur[lv - 1];
    if (id === 'heal') {
      this.hp = Math.min(this.maxHp, this.hp + sk.heal[lv - 1]);
      this.floatText(p.clone().setY(2.8), `+${sk.heal[lv - 1]} ♥`, '#74f0a7');
      this.ring(p, '#74f0a7', 3);
      this.fx.burst(p.clone().setY(0.2), { color: '#7dffb2', count: 40, speed: 1.8, life: 1.2, size: 0.45, gravity: 2.4 });
      beep(660, 0.2, 'sine');
    }
    if (id === 'whirl') {
      this.spin = 0.5;
      this.ring(p, '#e0a0ff', 4.4);
      this.fx.burst(p.clone().setY(1), { color: '#e6b3ff', count: 40, speed: 8, life: 0.5, size: 0.45, gravity: 0 });
      for (const e of this.enemies) if (!e.dying && e.g.position.distanceTo(p) < 4.6) this.hitEnemy(e, sk.dmg[lv - 1] + this.stats.atk * 0.4, '#e0a0ff');
      beep(200, 0.25, 'sawtooth');
    }
  }
  ring(pos, color, size) {
    const m = new THREE.Mesh(new THREE.RingGeometry(0.6, 0.95, 40), new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.85, side: THREE.DoubleSide, blending: THREE.AdditiveBlending, depthWrite: false }));
    m.rotation.x = -Math.PI / 2;
    m.position.set(pos.x, 0.12, pos.z);
    this.scene.add(m);
    this.effects.push({ m, t: 0, size });
  }
  hurt(n) {
    if (this.dead || this.dashT > 0) return;
    n = Math.max(1, Math.round(n - this.stats.def * 0.5)) * (this.shield > 0 ? 0.5 : 1);
    this.hp -= n;
    this.floatText(this.player.position.clone().setY(2.7), `-${Math.round(n)}`, '#ff6b6b');
    this.fx.burst(this.player.position.clone().setY(1.2), { color: '#ff5a6a', count: 12, speed: 4, life: 0.4, size: 0.35 });
    beep(100, 0.1, 'sawtooth');
    if (this.hp <= 0) {
      this.dead = true;
      this.hooks.dead?.(true);
      this.fx.burst(this.player.position.clone().setY(1), { color: '#ffffff', count: 40, speed: 5, life: 0.9, size: 0.5 });
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
    let dt = Math.min((now - this.last) / 1000, 0.05);
    this.last = now;
    // desempenho: se o quadro demorar muito por vários quadros, cai para o modo leve sozinho
    this.slowFrames = (this.slowFrames ?? 0) + (dt > 1 / 22 ? 1 : -1);
    this.slowFrames = Math.max(0, this.slowFrames);
    if (this.quality === 'high' && this.slowFrames > 120 && !this.autoDowngraded) {
      this.autoDowngraded = true;
      this.setQuality('low', false);
      this.hooks.toast?.('Computador lento: usei o modo desempenho (tecla P alterna)');
    }
    if (this.slow > 0) {
      this.slow -= dt;
      dt *= 0.25;
    }
    this.elapsed += dt;
    this.update(dt);
    if (this.composer && this.quality === 'high') this.composer.render(dt);
    else this.renderer.render(this.scene, this.camera);
  };

  update(dt) {
    const t = this.elapsed;
    const p = this.player.position;
    for (const k of Object.keys(this.cd)) this.cd[k] = Math.max(0, this.cd[k] - dt);
    this.atkCd = Math.max(0, this.atkCd - dt);
    this.swing = Math.max(0, this.swing - dt);
    this.shield = Math.max(0, this.shield - dt);
    this.spin = Math.max(0, this.spin - dt);

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
    const moving = !!(ix || iz);
    if (this.dashT > 0) {
      this.dashT -= dt;
      p.addScaledVector(this.vel, dt);
      this.fx.burst(p.clone().setY(0.6), { color: '#bfe9ff', count: 2, speed: 0.6, life: 0.35, size: 0.5, gravity: 0 });
    } else if (moving) {
      const dir = new THREE.Vector3(ix, 0, iz).normalize();
      dir.applyAxisAngle(new THREE.Vector3(0, 1, 0), this.yaw);
      const sp = (6 + (this.stats.speed ?? 0)) * (this.keys.has('shift') ? 1.5 : 1);
      p.addScaledVector(dir, sp * dt);
      this.facing.lerp(dir, Math.min(1, dt * 14)).normalize();
      this.dustT -= dt;
      if (this.dustT < 0) {
        this.dustT = 0.13;
        this.fx.burst(p.clone().setY(0.1), { color: '#d9c9a0', count: 2, speed: 0.8, life: 0.45, size: 0.4, gravity: 0.5, up: 0.5 });
      }
    }
    clampArena(p);
    this.rig.root.rotation.y = Math.atan2(this.facing.x, this.facing.z) + (this.spin > 0 ? (1 - this.spin / 0.5) * Math.PI * 4 : 0);
    animateHero(this.rig, { moving, swing: this.swing > 0 ? 1 - this.swing / 0.3 : 0, t, dt });
    if (this.rig.flame && this.rig.weapon && Math.random() < 0.6) {
      const tip = this.rig.weapon.localToWorld(new THREE.Vector3(0, 1.15, 0));
      this.fx.burst(tip, { color: '#ff7a2a', count: 1, speed: 0.6, life: 0.4, size: 0.35, gravity: 2.5, up: 0.4 });
    }
    this.shieldMesh.visible = this.shield > 0;
    if (this.shield > 0) {
      this.shieldMesh.position.copy(p).setY(1.2);
      this.shieldMesh.scale.setScalar(1 + Math.sin(t * 8) * 0.03);
    }

    this.#spawnLogic();
    for (const e of [...this.enemies]) {
      if (e.dying) {
        e.dying -= dt;
        e.g.scale.multiplyScalar(0.88);
        if (e.dying <= 0) {
          this.scene.remove(e.g);
          this.enemies.splice(this.enemies.indexOf(e), 1);
        }
        continue;
      }
      const to = p.clone().sub(e.g.position).setY(0);
      const d = to.length();
      if (!this.dead && d > 1.3 + e.r * 0.3) e.g.position.addScaledVector(to.normalize(), e.speed * dt);
      e.hitCd = Math.max(0, e.hitCd - dt);
      e.atkAnim = Math.max(0, e.atkAnim - dt);
      if (!this.dead && d < 1.5 + e.r * 0.5 && e.hitCd <= 0) {
        e.hitCd = 1.0;
        e.atkAnim = 0.35;
        this.hurt(e.atk);
      }
      for (const o of this.enemies) {
        if (o === e || o.dying) continue;
        const dd = e.g.position.distanceTo(o.g.position);
        if (dd < 1.4 && dd > 0.001) e.g.position.addScaledVector(e.g.position.clone().sub(o.g.position).setY(0).normalize(), dt * 2);
      }
      clampArena(e.g.position, ARENA - 0.8);
      e.phase += dt * (e.type === 'slime' ? 5 : 3.2);
      if (e.type === 'slime') {
        const sq = Math.sin(e.phase);
        e.body.scale.set(1 - sq * 0.07, 0.82 + sq * 0.1, 1 - sq * 0.07);
        e.body.position.y = 0.6 + Math.max(0, sq) * 0.12;
      } else {
        e.body.position.y = 1.15 + Math.abs(Math.sin(e.phase)) * 0.12;
        e.rig.armL.rotation.x = Math.sin(e.phase) * 0.4;
        e.rig.armR.rotation.x = e.atkAnim > 0 ? -2.2 + (1 - e.atkAnim / 0.35) * 2.6 : -Math.sin(e.phase) * 0.4;
      }
      e.g.rotation.y = Math.atan2(to.x, to.z);
      e.flash = Math.max(0, e.flash - dt);
      const m = e.body.material;
      if (e.flash > 0) (m.emissive.set('#ffffff'), (m.emissiveIntensity = 0.9));
      else (m.emissive.copy(e.em), (m.emissiveIntensity = e.emI));
      e.fg.scale.x = Math.max(0.001, e.hp / e.max);
      e.bar.quaternion.copy(this.camera.quaternion);
    }

    for (const pr of [...this.projectiles]) {
      pr.m.position.addScaledVector(pr.v, dt);
      pr.life -= dt;
      this.fx.burst(pr.m.position, { color: '#ff9a3a', count: 2, speed: 0.8, life: 0.3, size: 0.55, gravity: 0 });
      const hit = this.enemies.find((e) => !e.dying && e.g.position.distanceTo(pr.m.position.clone().setY(0)) < e.r + 0.5);
      if (hit || pr.life <= 0) {
        if (hit) {
          this.hitEnemy(hit, pr.dmg, '#ff9a3a');
          this.ring(pr.m.position, '#ff7a1a', 2.4);
          this.fx.burst(pr.m.position, { color: '#ff8a2a', count: 36, speed: 7, life: 0.55, size: 0.6 });
        }
        this.scene.remove(pr.m);
        this.projectiles.splice(this.projectiles.indexOf(pr), 1);
      }
    }
    for (const f of [...this.effects]) {
      f.t += dt * 2.5;
      f.m.scale.setScalar(1 + f.t * f.size);
      f.m.material.opacity = Math.max(0, 0.85 - f.t);
      if (f.t > 0.85) (this.scene.remove(f.m), this.effects.splice(this.effects.indexOf(f), 1));
    }
    const pickup = 2.5 + (this.stats.pickup ?? 0);
    for (const c of [...this.coins]) {
      c.t += dt;
      c.m.rotation.z += dt * 6;
      const d = c.m.position.distanceTo(p);
      if (d < pickup || c.t > 8) {
        c.m.position.lerp(p.clone().setY(1.2), Math.min(1, dt * 12));
        if (d < 0.9 || c.t > 8) {
          this.fx.burst(c.m.position, { color: '#ffe066', count: 6, speed: 2.5, life: 0.4, size: 0.3 });
          this.scene.remove(c.m);
          this.coins.splice(this.coins.indexOf(c), 1);
        }
      } else c.m.position.y = 0.7 + Math.sin(t * 4 + c.sp) * 0.12;
    }

    this.world.update(t, dt);
    this.fx.update(dt);

    const target = p.clone().setY(1.7);
    this.camera.position.set(target.x + Math.sin(this.yaw) * Math.cos(this.pitch) * this.dist, target.y + Math.sin(this.pitch) * this.dist, target.z + Math.cos(this.yaw) * Math.cos(this.pitch) * this.dist);
    this.camera.lookAt(target);

    this.hudT += dt;
    if (this.hudT > 0.1) {
      this.hudT = 0;
      this.hooks.hud?.({ hp: this.hp, max: this.maxHp, shield: this.shield > 0, cd: this.cd });
    }
  }
}
