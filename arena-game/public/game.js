// Jogabilidade do mundo aberto: movimento, pulo, combate, inimigos por região, jogadores online, NPCs, cristais e duelos.
// O cliente cuida do movimento e do combate contra criaturas; QUALQUER ganho (moedas/XP/carreira) é pedido ao servidor.
import * as THREE from 'three';
import { net, call, fire, on } from './net.js';
import { Fx, createComposer } from './visuals.js';
import { buildOpenWorld } from './world.js';
import { buildAvatar, animateAvatar, buildCreature, animateCreature, nameTag } from './avatar.js';
import { LOCATIONS, SPAWN, WORLD_HALF, heightAt } from './shared/world.js';

const rnd = (a, b) => a + Math.random() * (b - a);
const angLerp = (a, b, k) => a + Math.atan2(Math.sin(b - a), Math.cos(b - a)) * k;
const PLACES = ['colosseum', 'town', 'castle', 'ruins', 'forest', 'desert', 'snow', 'farm', 'beach'];

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
    this.pitch = 0.4;
    this.dist = 11;
    this.last = performance.now();
    this.elapsed = 0;
    this.mons = new Map(); // monstros compartilhados (o servidor decide tudo)
    this.projectiles = [];
    this.effects = [];
    this.coins = [];
    this.remotes = new Map();
    this.profiles = new Map();
    this.cd = {};
    this.atkCd = 0;
    this.swing = 0;
    this.shield = 0;
    this.dashT = 0;
    this.spin = 0;
    this.vy = 0;
    this.onGround = true;
    this.dead = false;
    this.battle = null;
    this.facing = new THREE.Vector3(0, 0, 1);
    this.vel = new THREE.Vector3();
    this.hudT = 0;
    this.sendT = 0;
    this.lastSent = new THREE.Vector3(1e9, 0, 0);
    this.dustT = 0;
    this.slow = 0;
    this.placeT = 0;
    this.place = '';
    this.crystalCd = 0;
    this.quality = localStorage.getItem('arena-q') ?? 'high';

    const r = (this.renderer = new THREE.WebGLRenderer({ canvas, antialias: true }));
    r.setPixelRatio(Math.min(devicePixelRatio, 2));
    r.shadowMap.enabled = true;
    r.shadowMap.type = THREE.PCFSoftShadowMap;
    r.toneMapping = THREE.ACESFilmicToneMapping;
    r.toneMappingExposure = 0.95;
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(55, 1, 0.1, 1600);
    this.fx = new Fx(this.scene, 1400);
    this.world = buildOpenWorld(this.scene, this.fx);
    this.world.spawnNpcs(net.catalog.items);
    this.player = new THREE.Group();
    this.player.position.set(SPAWN.x, heightAt(SPAWN.x, SPAWN.z), SPAWN.z);
    this.scene.add(this.player);
    this.hp = this.maxHp = 100;
    this.refreshCharacter();
    this.shieldMesh = new THREE.Mesh(new THREE.SphereGeometry(1.9, 24, 16), new THREE.MeshBasicMaterial({ color: '#7fd0ff', transparent: true, opacity: 0.22, blending: THREE.AdditiveBlending, depthWrite: false }));
    this.shieldMesh.visible = false;
    this.scene.add(this.shieldMesh);
    this.#bind(canvas);
    this.#net();
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
  get stats() {
    return net.state.stats;
  }
  eq(st = net.state) {
    const out = {};
    for (const slot of net.catalog.slots) out[slot] = st.inventory.find((i) => i.iid === st.equipped[slot])?.itemId ?? null;
    return out;
  }
  refreshCharacter() {
    const keep = this.player.position.clone();
    this.player.clear();
    const st = net.state;
    this.rig = buildAvatar(st.ap, this.eq(), net.catalog.items, `${st.name}`, st.career?.done ? '#ffd24a' : '#ffffff');
    this.player.add(this.rig.root);
    this.player.position.copy(keep);
    const ratio = this.maxHp ? this.hp / this.maxHp : 1;
    this.maxHp = st.stats.hp;
    this.hp = Math.max(1, Math.round(this.maxHp * ratio));
  }

  // ---------- rede: jogadores online, chat, duelos ----------
  #net() {
    on('profiles', (m) => m.list.forEach((p) => this.profiles.set(p.n, p)));
    on('profile', (p) => {
      this.profiles.set(p.n, p);
      const r = this.remotes.get(p.n);
      if (r) this.#removeRemote(p.n);
    });
    on('left', (m) => {
      this.profiles.delete(m.n);
      this.#removeRemote(m.n);
    });
    on('presence', (m) => this.#presence(m.p));
    on('tp', (m) => {
      this.player.position.set(m.x, this.world.groundY(m.x, m.z), m.z);
      this.vy = 0;
      this.lastSent.set(1e9, 0, 0);
    });
    on('chat', (m) => {
      this.hooks.chat?.(m);
      const rig = m.n === net.state.name ? this.rig : this.remotes.get(m.n)?.rig;
      if (rig) this.#bubble(rig, m.text);
    });
    on('battle', (m) => this.#battleEvent(m));
    on('mons', (m) => this.#mons(m.m));
    on('mhit', (m) => this.#monHit(m));
    on('mdie', (m) => this.#monDie(m));
    on('reward', (m) => this.#reward(m));
    on('hurt', (m) => {
      const p = this.player.position;
      this.floatText(p.clone().setY(p.y + 3.2), `-${m.dmg}`, '#ff6b6b');
      this.fx.burst(p.clone().setY(p.y + 1.4), { color: '#ff5a6a', count: 12, speed: 4, life: 0.4, size: 0.35 });
      beep(100, 0.1, 'sawtooth');
    });
    on('php', (m) => {
      this.hp = m.hp;
      this.maxHp = m.max;
      this.shield = m.sh;
    });
    on('died', () => {
      this.dead = true;
      this.hooks.dead?.(true);
      const p = this.player.position;
      this.fx.burst(p.clone().setY(p.y + 1.2), { color: '#ffffff', count: 40, speed: 5, life: 0.9, size: 0.5 });
    });
    on('revive', () => {
      this.player.position.set(SPAWN.x, heightAt(SPAWN.x, SPAWN.z), SPAWN.z);
      this.vy = 0;
      this.dead = false;
      this.hooks.dead?.(false);
    });
    on('fx', (m) => this.#remoteFx(m));
  }
  // ---------- monstros: só desenha o que o servidor manda ----------
  #monster(id, type) {
    const def = net.catalog.enemies[type];
    const boss = type === 'kingslime';
    const rig = buildCreature(type);
    const g = rig.g;
    const bar = new THREE.Group();
    const bg = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 0.18), new THREE.MeshBasicMaterial({ color: '#1b1426', depthTest: false }));
    const fg = new THREE.Mesh(new THREE.PlaneGeometry(1.44, 0.12).translate(0.72, 0, 0), new THREE.MeshBasicMaterial({ color: boss ? '#ff6a3a' : '#46e0a0', depthTest: false }));
    fg.position.set(-0.72, 0, 0.01);
    bg.renderOrder = 10;
    fg.renderOrder = 11;
    bar.add(bg, fg);
    bar.position.y = rig.barY;
    bar.scale.setScalar(boss ? 2.6 : 1);
    g.add(bar);
    this.scene.add(g);
    const m = rig.body?.material;
    return { id, type, g, rig, body: rig.body, bar, fg, r: rig.r, hp: def.hp, max: def.hp, tx: 0, tz: 0, tyaw: 0, flags: 0, flash: 0, dying: 0, t: Math.random() * 6, atkAnim: 0, boss, em: m?.emissive ? { c: m.emissive.clone(), i: m.emissiveIntensity } : null, init: false };
  }
  #mons(list) {
    const seen = new Set();
    for (const [id, type, x, z, yaw, hp, max, flags] of list) {
      seen.add(id);
      let e = this.mons.get(id);
      if (!e) {
        e = this.#monster(id, type);
        this.mons.set(id, e);
      }
      if (!e.init) {
        e.g.position.set(x, this.world.groundY(x, z), z);
        e.init = true;
      }
      Object.assign(e, { tx: x, tz: z, tyaw: yaw, hp, max });
      if (flags & 2 && !(e.flags & 2)) e.atkAnim = 0.35;
      e.flags = flags;
    }
    for (const [id, e] of this.mons) {
      if (seen.has(id) || e.dying) continue;
      this.scene.remove(e.g);
      this.mons.delete(id);
    }
  }
  #monHit(m) {
    const e = this.mons.get(m.id);
    const mine = m.by === net.state.name;
    const y = (e ? e.g.position.y : this.world.groundY(m.x, m.z)) + 2.6;
    this.floatText(new THREE.Vector3(m.x, y, m.z), String(m.dmg), m.crit ? '#ffb300' : mine ? '#ffffff' : '#bfe9ff');
    this.fx.burst(new THREE.Vector3(m.x, y - 1.3, m.z), { color: '#fff2a8', count: 9, speed: 5, life: 0.35, size: 0.32 });
    if (e) e.flash = 0.12;
    if (mine) this.slow = 0.05;
    beep(180, 0.05, 'sawtooth');
  }
  #monDie(m) {
    const e = this.mons.get(m.id);
    const y = this.world.groundY(m.x, m.z) + 1;
    this.fx.burst(new THREE.Vector3(m.x, y, m.z), { color: m.type === 'slime' ? '#74e590' : '#ff8a5a', count: m.boss ? 90 : 30, speed: m.boss ? 10 : 6.5, life: 0.8, size: 0.55 });
    if (e) e.dying = 0.4;
  }
  #reward(m) {
    const y = this.world.groundY(m.x, m.z) + 3;
    this.floatText(new THREE.Vector3(m.x, y, m.z), m.coins ? `+${m.coins} 🪙  +${m.xp} XP` : `+${m.xp} XP (teto de moedas da hora)`, '#ffd24a');
    for (let i = 0; i < Math.min(10, m.coins); i++) this.dropCoin(new THREE.Vector3(m.x, y - 2, m.z));
    if (m.levelUp) {
      this.hooks.toast?.('⬆ Você subiu de nível!');
      const p = this.player.position;
      this.fx.burst(p.clone().setY(p.y + 0.3), { color: '#ffe066', count: 70, speed: 6, life: 1.1, size: 0.55, gravity: -1.5 });
      this.ring(p, '#ffe066', 5);
    }
    beep(880, 0.1, 'triangle');
  }
  // habilidades de OUTROS jogadores (só o visual; o dano é do servidor)
  #remoteFx(m) {
    const y = this.world.groundY(m.x, m.z);
    const pos = new THREE.Vector3(m.x, y, m.z);
    if (m.kind === 'fireball') this.#fireballVisual(pos.clone().setY(y + 1.6), new THREE.Vector3(Math.sin(m.yaw), 0, Math.cos(m.yaw)));
    else if (m.kind === 'whirl') (this.ring(pos, '#e0a0ff', 4.6), this.fx.burst(pos.clone().setY(y + 1), { color: '#e6b3ff', count: 40, speed: 8, life: 0.5, size: 0.45, gravity: 0 }));
    else if (m.kind === 'heal') (this.ring(pos, '#74f0a7', 3), this.fx.burst(pos.clone().setY(y + 0.2), { color: '#7dffb2', count: 30, speed: 1.8, life: 1.2, size: 0.45, gravity: 2.4 }));
    else if (m.kind === 'dash') this.fx.burst(pos.clone().setY(y + 0.4), { color: '#bfe9ff', count: 22, speed: 3, life: 0.5, size: 0.5, gravity: 0 });
  }
  #fireballVisual(from, dir) {
    const g = new THREE.Group();
    g.add(new THREE.Mesh(new THREE.SphereGeometry(0.46, 14, 10), new THREE.MeshBasicMaterial({ color: '#ffb347' })));
    g.add(new THREE.Mesh(new THREE.SphereGeometry(0.7, 14, 10), new THREE.MeshBasicMaterial({ color: '#ff5a1a', transparent: true, opacity: 0.45, blending: THREE.AdditiveBlending, depthWrite: false })));
    g.position.copy(from).addScaledVector(dir, 1.2);
    this.scene.add(g);
    this.projectiles.push({ m: g, v: dir.clone().multiplyScalar(22), life: 1.1 });
  }
  #presence(list) {
    const seen = new Set();
    for (const [n, x, y, z, yaw, a, hp] of list) {
      if (n === net.state.name) continue;
      seen.add(n);
      let r = this.remotes.get(n);
      if (!r) {
        const pr = this.profiles.get(n);
        if (!pr) continue;
        const rig = buildAvatar(pr.ap, pr.eq, net.catalog.items, `${n} · Nv ${pr.lv}`, pr.done ? '#ffd24a' : '#bfe9ff');
        const g = new THREE.Group();
        g.add(rig.root);
        g.position.set(x, y, z);
        this.scene.add(g);
        r = { g, rig, tx: x, ty: y, tz: z, yaw, a: 0, moved: 0, swing: 0, prev: new THREE.Vector3(x, y, z) };
        this.remotes.set(n, r);
      }
      r.tx = x;
      r.ty = y;
      r.tz = z;
      r.ty = y;
      r.tyaw = yaw;
      if (a === 2 && r.a !== 2) r.swing = 0.3;
      r.a = a;
      r.hp = hp;
    }
    for (const n of [...this.remotes.keys()]) if (!seen.has(n)) this.#removeRemote(n);
  }
  #removeRemote(n) {
    const r = this.remotes.get(n);
    if (!r) return;
    this.scene.remove(r.g);
    this.remotes.delete(n);
  }
  #bubble(rig, text) {
    if (rig.bubble) rig.root.remove(rig.bubble);
    const c = document.createElement('canvas');
    c.width = 512;
    c.height = 128;
    const g = c.getContext('2d');
    g.font = 'bold 34px system-ui, sans-serif';
    const t = text.length > 34 ? text.slice(0, 33) + '…' : text;
    const w = Math.min(496, g.measureText(t).width + 40);
    g.fillStyle = 'rgba(255,255,255,0.95)';
    g.beginPath();
    g.roundRect(256 - w / 2, 14, w, 64, 22);
    g.fill();
    g.beginPath();
    g.moveTo(240, 78);
    g.lineTo(256, 100);
    g.lineTo(272, 78);
    g.fill();
    g.fillStyle = '#1b1426';
    g.textAlign = 'center';
    g.textBaseline = 'middle';
    g.fillText(t, 256, 48);
    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true, depthWrite: false }));
    s.scale.set(4.2, 1.05, 1);
    s.position.set(0, 4.3, 0);
    s.renderOrder = 30;
    rig.root.add(s);
    rig.bubble = s;
    setTimeout(() => {
      if (rig.bubble === s) (rig.root.remove(s), (rig.bubble = null));
    }, 5500);
  }
  #battleEvent(m) {
    if (m.phase === 'start') {
      this.battle = { opponent: m.opponent, hp: m.hp, maxHp: m.maxHp, until: performance.now() + m.seconds * 1000 };
      this.keys.clear();
      this.hooks.toast?.(`⚔ Duelo contra ${m.opponent}! Derrote-o antes do tempo acabar.`);
    } else if (m.phase === 'hit') {
      if (this.battle) this.battle.hp = m.hp;
      const who = m.target === net.state.name ? this.player : this.remotes.get(m.target)?.g;
      if (who) {
        this.floatText(who.position.clone().setY(who.position.y + 3), `-${m.dmg}`, m.target === net.state.name ? '#ff6b6b' : '#fff');
        this.fx.burst(who.position.clone().setY(who.position.y + 1.4), { color: '#ffe08a', count: 12, speed: 5, life: 0.4, size: 0.4 });
        if (m.target === net.state.name) beep(110, 0.1, 'sawtooth');
      }
    } else if (m.phase === 'end') {
      this.battle = null;
      this.hooks.toast?.(m.winner ? (m.winner === net.state.name ? `🏆 Você venceu o duelo! +${m.prize} moedas` : `Você perdeu o duelo para ${m.winner}`) : 'Duelo empatado: apostas devolvidas');
    }
    this.hooks.battle?.(this.battle, m);
  }

  // ---------- entrada ----------
  #bind(canvas) {
    const SK = { 1: 'dash', 2: 'fireball', 3: 'shield', 4: 'heal', 5: 'whirl' };
    addEventListener('keydown', (e) => {
      if (!this.enabled || e.target.matches?.('input,select,textarea')) return;
      const k = e.key.toLowerCase();
      this.keys.add(k);
      if (k === ' ') (e.preventDefault(), this.jump());
      if (k === 'f') this.attack();
      if (k === 'e') this.interact();
      if (k === 'tab') (e.preventDefault(), this.hooks.bigmap?.(true));
      if (SK[k]) this.useSkill(SK[k]);
      if (k === 'p') this.setQuality(this.quality === 'high' ? 'low' : 'high');
      try {
        audio ??= new AudioContext();
      } catch {
        /* sem áudio */
      }
    });
    addEventListener('keyup', (e) => {
      this.keys.delete(e.key.toLowerCase());
      if (e.key === 'Tab') this.hooks.bigmap?.(false);
    });
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
      this.pitch = Math.min(1.25, Math.max(0.05, this.pitch + (e.clientY - drag.y) * 0.004));
      drag = { x: e.clientX, y: e.clientY };
    });
    canvas.addEventListener('wheel', (e) => (this.dist = Math.min(26, Math.max(5, this.dist + e.deltaY * 0.012))), { passive: true });
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
  jump() {
    if (this.dead || !this.onGround || this.battleFrozen) return;
    this.vy = 11;
    this.onGround = false;
    beep(520, 0.06, 'triangle', 0.025);
  }

  // ---------- NPCs e carreira ----------
  nearestNpc(range = 5.5) {
    let best = null;
    let bd = range;
    for (const n of this.world.npcs) {
      const d = Math.hypot(n.x - this.player.position.x, n.z - this.player.position.z);
      if (d < bd) (bd = d), (best = n);
    }
    return best;
  }
  interact() {
    const n = this.nearestNpc();
    if (n && !this.dead) this.hooks.dialog?.(n);
  }
  questTarget() {
    const q = net.state.career?.quest;
    if (!q) return null;
    if (q.type === 'talk') return { x: LOCATIONS.mayor.x, z: LOCATIONS.mayor.z };
    if (q.type === 'collect') {
      const c = this.world.crystals.find((k) => !k.taken && net.state.career.quest.id === 3);
      if (c) return { x: c.x, z: c.z };
    }
    return q.loc ? { x: LOCATIONS[q.loc].x, z: LOCATIONS[q.loc].z } : null;
  }

  // ---------- inimigos (visão do servidor) ----------
  nearestEnemy(range = 7) {
    let best = null;
    let bd = range;
    for (const e of this.mons.values()) {
      if (e.dying) continue;
      const d = e.g.position.distanceTo(this.player.position);
      if (d < bd) (bd = d), (best = e);
    }
    return best;
  }
  dropCoin(pos) {
    const c = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 0.09, 16), new THREE.MeshStandardMaterial({ color: '#ffd24a', emissive: '#ffb300', emissiveIntensity: 1.0, metalness: 0.6, roughness: 0.3 }));
    c.rotation.x = Math.PI / 2;
    c.position.set(pos.x + rnd(-1, 1), pos.y + 0.9, pos.z + rnd(-1, 1));
    this.scene.add(c);
    this.coins.push({ m: c, t: 0, sp: rnd(0, 6) });
  }

  // ---------- ações ----------
  attack() {
    if (this.dead || this.atkCd > 0 || !this.enabled) return;
    this.atkCd = 0.45;
    this.swing = 0.3;
    const p = this.player.position;
    if (this.battle) {
      const r = this.remotes.get(this.battle.opponent);
      if (r) {
        this.facing.set(r.g.position.x - p.x, 0, r.g.position.z - p.z).normalize();
        if (Math.hypot(r.g.position.x - p.x, r.g.position.z - p.z) <= 5) call('battle_hit', { target: this.battle.opponent }).catch(() => {});
      }
      beep(200, 0.05, 'square');
      return;
    }
    const t = this.nearestEnemy(6);
    if (t) this.facing.copy(t.g.position).sub(p).setY(0).normalize();
    fire('attack', { yaw: +Math.atan2(this.facing.x, this.facing.z).toFixed(3) });
    this.fx.burst(p.clone().addScaledVector(this.facing, 1.8).setY(p.y + 1.5), { color: '#ffffff', count: 5, speed: 3, life: 0.25, size: 0.25, gravity: 0 });
    beep(t ? 260 : 140, 0.05, 'square');
  }
  useSkill(id) {
    if (this.dead || !this.enabled || this.battle) return;
    const lv = net.state.skills[id];
    const sk = net.catalog.skills[id];
    if (!lv) return this.hooks.toast?.(`Você ainda não aprendeu ${sk.name} (compre o pergaminho na Loja)`);
    if ((this.cd[id] ?? 0) > 0) return;
    this.cd[id] = sk.cd[lv - 1];
    const p = this.player.position;
    const t = this.nearestEnemy(14);
    if (id !== 'dash' && t) this.facing.copy(t.g.position).sub(p).setY(0).normalize();
    fire('skill', { id, yaw: +Math.atan2(this.facing.x, this.facing.z).toFixed(3) });
    // só o visual; dano, cura e escudo são decididos pelo servidor
    if (id === 'dash') {
      this.dashT = 0.22;
      this.vel.copy(this.facing).multiplyScalar(24);
      this.fx.burst(p.clone().setY(p.y + 0.4), { color: '#bfe9ff', count: 22, speed: 3, life: 0.5, size: 0.5, gravity: 0 });
    }
    if (id === 'fireball') {
      this.#fireballVisual(p.clone().setY(p.y + 1.6), this.facing.clone());
      beep(320, 0.15, 'sawtooth');
    }
    if (id === 'shield') this.shield = sk.dur[lv - 1];
    if (id === 'heal') {
      this.ring(p, '#74f0a7', 3);
      this.fx.burst(p.clone().setY(p.y + 0.2), { color: '#7dffb2', count: 40, speed: 1.8, life: 1.2, size: 0.45, gravity: 2.4 });
      beep(660, 0.2, 'sine');
    }
    if (id === 'whirl') {
      this.spin = 0.5;
      this.ring(p, '#e0a0ff', 4.6);
      this.fx.burst(p.clone().setY(p.y + 1), { color: '#e6b3ff', count: 40, speed: 8, life: 0.5, size: 0.45, gravity: 0 });
      beep(200, 0.25, 'sawtooth');
    }
  }
  ring(pos, color, size) {
    const m = new THREE.Mesh(new THREE.RingGeometry(0.6, 0.95, 40), new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.85, side: THREE.DoubleSide, blending: THREE.AdditiveBlending, depthWrite: false }));
    m.rotation.x = -Math.PI / 2;
    m.position.set(pos.x, pos.y + 0.15, pos.z);
    this.scene.add(m);
    this.effects.push({ m, t: 0, size });
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
    this.slowFrames = Math.max(0, (this.slowFrames ?? 0) + (dt > 1 / 22 ? 1 : -1));
    if (this.quality === 'high' && this.slowFrames > 150 && !this.autoDowngraded) {
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
    const W = this.world;
    for (const k of Object.keys(this.cd)) this.cd[k] = Math.max(0, this.cd[k] - dt);
    this.atkCd = Math.max(0, this.atkCd - dt);
    this.swing = Math.max(0, this.swing - dt);
    this.shield = Math.max(0, this.shield - dt);
    this.spin = Math.max(0, this.spin - dt);
    this.crystalCd -= dt;
    this.battleFrozen = false;

    // movimento
    let ix = 0;
    let iz = 0;
    if (this.enabled && !this.dead) {
      if (this.keys.has('w') || this.keys.has('arrowup')) iz -= 1;
      if (this.keys.has('s') || this.keys.has('arrowdown')) iz += 1;
      if (this.keys.has('a')) ix -= 1;
      if (this.keys.has('d')) ix += 1;
      if (this.keys.has('arrowleft')) this.yaw += dt * 1.8;
      if (this.keys.has('arrowright')) this.yaw -= dt * 1.8;
    }
    const moving = !!(ix || iz);
    let mx = 0;
    let mz = 0;
    if (this.dashT > 0) {
      this.dashT -= dt;
      mx = this.vel.x * dt;
      mz = this.vel.z * dt;
      this.fx.burst(p.clone().setY(p.y + 0.8), { color: '#bfe9ff', count: 2, speed: 0.6, life: 0.35, size: 0.5, gravity: 0 });
    } else if (moving) {
      const dir = new THREE.Vector3(ix, 0, iz).normalize().applyAxisAngle(new THREE.Vector3(0, 1, 0), this.yaw);
      const sp = (7.5 + (this.stats.speed ?? 0)) * (this.keys.has('shift') ? 1.6 : 1);
      mx = dir.x * sp * dt;
      mz = dir.z * sp * dt;
      this.facing.lerp(dir, Math.min(1, dt * 14)).normalize();
      this.dustT -= dt;
      if (this.dustT < 0 && this.onGround) {
        this.dustT = 0.13;
        this.fx.burst(p.clone().setY(p.y + 0.1), { color: '#d9c9a0', count: 2, speed: 0.8, life: 0.45, size: 0.4, gravity: 0.5, up: 0.5 });
      }
    }
    if (mx || mz) {
      const nx = p.x + mx;
      const nz = p.z + mz;
      if (!W.isDeepWater(nx, nz)) (p.x = nx), (p.z = nz);
      else if (!W.isDeepWater(nx, p.z)) p.x = nx;
      else if (!W.isDeepWater(p.x, nz)) p.z = nz;
      W.col.resolve(p, 0.55);
      p.x = Math.max(-WORLD_HALF + 3, Math.min(WORLD_HALF - 3, p.x));
      p.z = Math.max(-WORLD_HALF + 3, Math.min(WORLD_HALF - 3, p.z));
    }
    // vertical: gravidade, pulo e terreno
    const gy = W.groundY(p.x, p.z);
    this.vy -= 30 * dt;
    p.y += this.vy * dt;
    if (p.y <= gy + 0.02 || (this.onGround && p.y - gy < 1.0 && this.vy <= 0)) {
      p.y = gy;
      this.vy = 0;
      this.onGround = true;
    } else this.onGround = false;
    if (p.y < -30) (p.set(SPAWN.x, 0, SPAWN.z), (this.vy = 0));

    const a = this.swing > 0 ? 2 : !this.onGround ? 3 : moving ? 1 : 0;
    this.rig.root.rotation.y = Math.atan2(this.facing.x, this.facing.z) + (this.spin > 0 ? (1 - this.spin / 0.5) * Math.PI * 4 : 0);
    animateAvatar(this.rig, { moving, air: !this.onGround, swing: this.swing > 0 ? 1 - this.swing / 0.3 : 0, t, dt });
    if (this.rig.flame && this.rig.weapon && Math.random() < 0.6) {
      const tip = this.rig.weapon.localToWorld(new THREE.Vector3(0, 1.3, 0));
      this.fx.burst(tip, { color: '#ff7a2a', count: 1, speed: 0.6, life: 0.4, size: 0.35, gravity: 2.5, up: 0.4 });
    }
    this.shieldMesh.visible = this.shield > 0;
    if (this.shield > 0) {
      this.shieldMesh.position.copy(p).setY(p.y + 1.4);
      this.shieldMesh.scale.setScalar(1 + Math.sin(t * 8) * 0.03);
    }

    // presença online (10 vezes por segundo quando se mexe; 1 vez por segundo parado)
    this.sendT += dt;
    const moved = Math.hypot(p.x - this.lastSent.x, p.z - this.lastSent.z) > 0.05 || Math.abs(p.y - this.lastSent.y) > 0.05;
    if ((moved && this.sendT > 0.1) || this.sendT > 1) {
      this.sendT = 0;
      this.lastSent.copy(p);
      fire('move', { x: +p.x.toFixed(2), y: +p.y.toFixed(2), z: +p.z.toFixed(2), yaw: +Math.atan2(this.facing.x, this.facing.z).toFixed(2), a });
    }

    // outros jogadores
    for (const r of this.remotes.values()) {
      const k = 1 - Math.exp(-12 * dt);
      const before = r.g.position.clone();
      r.g.position.x += (r.tx - r.g.position.x) * k;
      r.g.position.y += (r.ty - r.g.position.y) * k;
      r.g.position.z += (r.tz - r.g.position.z) * k;
      r.rig.root.rotation.y = angLerp(r.rig.root.rotation.y, r.tyaw ?? 0, k);
      const spd = before.distanceTo(r.g.position) / Math.max(dt, 1e-3);
      r.swing = Math.max(0, r.swing - dt);
      animateAvatar(r.rig, { moving: spd > 0.8, air: r.g.position.y - W.groundY(r.g.position.x, r.g.position.z) > 0.5, swing: r.swing > 0 ? 1 - r.swing / 0.3 : 0, t, dt });
    }

    // NPCs: olham para o jogador quando perto
    for (const n of W.npcs) {
      const d = Math.hypot(n.x - p.x, n.z - p.z);
      if (d < 9) n.rig.root.rotation.y = angLerp(n.rig.root.rotation.y, Math.atan2(p.x - n.x, p.z - n.z), Math.min(1, dt * 6));
      animateAvatar(n.rig, { moving: false, air: false, swing: 0, t: t + n.x, dt });
    }

    // cristais da carreira
    const q = net.state.career?.quest;
    if (q?.type === 'collect' && this.crystalCd <= 0) {
      for (const c of W.crystals) {
        if (c.taken || Math.hypot(c.x - p.x, c.z - p.z) > 3.6) continue;
        this.crystalCd = 0.6;
        call('collect', { id: c.id })
          .then((r) => {
            if (!r.progressed) return;
            c.taken = true;
            c.mesh.visible = false;
            this.fx.burst(c.mesh.position, { color: '#7fe8ff', count: 40, speed: 6, life: 0.9, size: 0.5 });
            beep(1040, 0.15, 'triangle');
            this.hooks.toast?.('💎 Cristal coletado!');
          })
          .catch(() => {});
        break;
      }
    }

    // monstros do servidor: suaviza posição, anima, barra de vida
    for (const e of [...this.mons.values()]) {
      const ep = e.g.position;
      if (e.dying) {
        e.dying -= dt;
        e.g.scale.multiplyScalar(0.88);
        if (e.dying <= 0) (this.scene.remove(e.g), this.mons.delete(e.id));
        continue;
      }
      const k = 1 - Math.exp(-10 * dt);
      const px = ep.x;
      const pz = ep.z;
      ep.x += (e.tx - ep.x) * k;
      ep.z += (e.tz - ep.z) * k;
      ep.y = W.groundY(ep.x, ep.z);
      e.g.rotation.y = angLerp(e.g.rotation.y, e.tyaw, Math.min(1, dt * 10));
      const moving = Math.hypot(ep.x - px, ep.z - pz) / Math.max(dt, 1e-3) > 0.6;
      e.atkAnim = Math.max(0, e.atkAnim - dt);
      e.t += dt;
      animateCreature(e.rig, { t: e.t, moving, atk: e.atkAnim });
      e.flash = Math.max(0, e.flash - dt);
      const m = e.body?.material;
      if (m?.emissive && e.em) {
        if (e.flash > 0) (m.emissive.set('#ffffff'), (m.emissiveIntensity = 0.9));
        else (m.emissive.copy(e.em.c), (m.emissiveIntensity = e.em.i));
      }
      e.fg.scale.x = Math.max(0.001, e.hp / e.max);
      e.bar.quaternion.copy(this.camera.quaternion);
    }

    // projéteis, efeitos, moedas
    for (const pr of [...this.projectiles]) {
      pr.m.position.addScaledVector(pr.v, dt);
      pr.life -= dt;
      this.fx.burst(pr.m.position, { color: '#ff9a3a', count: 2, speed: 0.8, life: 0.3, size: 0.55, gravity: 0 });
      if (pr.life <= 0) {
        this.ring(pr.m.position, '#ff7a1a', 2.4);
        this.fx.burst(pr.m.position, { color: '#ff8a2a', count: 36, speed: 7, life: 0.55, size: 0.6 });
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
    const pickup = 2.8 + (this.stats.pickup ?? 0);
    for (const c of [...this.coins]) {
      c.t += dt;
      c.m.rotation.z += dt * 6;
      const d = c.m.position.distanceTo(p);
      if (d < pickup || c.t > 8) {
        c.m.position.lerp(p.clone().setY(p.y + 1.4), Math.min(1, dt * 12));
        if (d < 1 || c.t > 8) {
          this.fx.burst(c.m.position, { color: '#ffe066', count: 6, speed: 2.5, life: 0.4, size: 0.3 });
          this.scene.remove(c.m);
          this.coins.splice(this.coins.indexOf(c), 1);
        }
      } else c.m.position.y = this.world.groundY(c.m.position.x, c.m.position.z) + 0.9 + Math.sin(t * 4 + c.sp) * 0.12;
    }

    // mundo, partículas e câmera
    W.update(t, dt, p);
    this.fx.update(dt);
    const target = p.clone().setY(p.y + 1.9);
    const cp = new THREE.Vector3(target.x + Math.sin(this.yaw) * Math.cos(this.pitch) * this.dist, target.y + Math.sin(this.pitch) * this.dist, target.z + Math.cos(this.yaw) * Math.cos(this.pitch) * this.dist);
    cp.y = Math.max(cp.y, W.groundY(cp.x, cp.z) + 1.2);
    this.camera.position.lerp(cp, Math.min(1, dt * 14));
    this.camera.lookAt(target);

    // nome do lugar e dicas
    this.placeT -= dt;
    if (this.placeT <= 0) {
      this.placeT = 0.5;
      let place = 'Campos Abertos';
      for (const k of PLACES) {
        if (Math.hypot(p.x - LOCATIONS[k].x, p.z - LOCATIONS[k].z) < LOCATIONS[k].r) {
          place = LOCATIONS[k].name;
          break;
        }
      }
      if (place !== this.place) {
        this.place = place;
        this.hooks.place?.(place);
      }
    }
    const n = this.nearestNpc();
    this.hooks.prompt?.(n && !this.dead ? `[E] Falar com ${n.name}` : null);

    this.hudT += dt;
    if (this.hudT > 0.1) {
      this.hudT = 0;
      this.hooks.hud?.({ hp: this.hp, max: this.maxHp, shield: this.shield > 0, cd: this.cd, x: p.x, z: p.z, yaw: Math.atan2(this.facing.x, this.facing.z), tod: this.world.tod, battle: this.battle });
    }
  }
}
