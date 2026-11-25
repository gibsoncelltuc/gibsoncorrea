// Combate contra monstros NO SERVIDOR: monstros compartilhados, golpes e habilidades validados, vida dos jogadores,
// morte/renascimento e recompensas para todos que causaram dano. O cliente só mostra o que o servidor decide.
import { ENEMIES, SKILLS, RULES } from './catalog.js';
import { GameError } from './economy.js';
import { LOCATIONS, SPAWN, biomeAt, heightAt, SEA_LEVEL, WORLD_HALF, isSafe } from '../public/shared/world.js';

const fail = (code, msg) => {
  throw new GameError(code, msg);
};
// espécies por bioma (vem do bestiário); quanto mais longe da vila, mais forte a espécie sorteada
const BY_BIOME = {};
for (const [id, d] of Object.entries(ENEMIES)) if (!d.boss) for (const b of d.biomes) (BY_BIOME[b] ??= []).push([id, d.lv]);
const pickSpecies = (b, dist, rng) => {
  const list = BY_BIOME[b];
  if (!list?.length) return null;
  const want = 1 + dist / 22 + (rng() - 0.5) * 5;
  const w = list.map(([, lv]) => 0.12 + 1 / (1 + Math.abs(lv - want) ** 1.5));
  let r = rng() * w.reduce((a, c) => a + c, 0);
  for (let i = 0; i < list.length; i++) if ((r -= w[i]) <= 0) return list[i][0];
  return list[0][0];
};
const ELITE = 4;
const ENRAGED = 8;
const ROAR = 16;
const r2 = (n) => Math.round(n * 100) / 100;
const deepWater = (x, z) => heightAt(x, z) < SEA_LEVEL - 0.9;

export class Combat {
  constructor(eco, world, { now = Date.now, rng = Math.random, emit = () => {}, onReward = () => {}, perPlayer = 12 } = {}) {
    this.eco = eco;
    this.world = world;
    this.now = now;
    this.rng = rng;
    this.emit = emit;
    this.onReward = onReward;
    this.perPlayer = perPlayer;
    this.monsters = new Map();
    this.seq = 1;
    this.spawnT = 0;
    this.bossAt = {};
  }

  // ---------- estado de combate de cada jogador (guardado junto da posição) ----------
  maxHp(name) {
    return this.eco.stats(this.eco.player(name)).hp;
  }
  ps(name) {
    const p = this.world.pos.get(name);
    if (!p) return null;
    if (p.hp === undefined) Object.assign(p, { hp: this.maxHp(name), dead: false, deadUntil: 0, shieldUntil: 0, atkReady: 0, skillReady: {}, lastHurt: 0, sent: '' });
    return p;
  }
  eligible(p) {
    return p && !p.dead && !this.world.inMatch.has(p.name) && !isSafe(p.x, p.z);
  }
  emitNear(x, z, radius, msg, except = null) {
    for (const [n, p] of this.world.pos) if (n !== except && Math.hypot(p.x - x, p.z - z) <= radius) this.emit(n, msg);
  }

  // ---------- criação de monstros ----------
  create(type, x, z, tier = 1, elite = false) {
    const d = ENEMIES[type];
    const e = elite && !d.boss;
    const hp = Math.round(d.hp * tier * (e ? 2.6 : 1));
    const m = { id: 'M' + this.seq++, type, x, z, hx: x, hz: z, yaw: 0, hp, max: hp, atk: d.atk * (e ? 1.4 : 1), speed: d.speed * (e ? 1.1 : 1), r: d.r * (e ? 1.25 : 1), aggro: d.aggro, cd: 0, atkT: 0, moving: false, boss: !!d.boss, elite: e, enraged: false, roarT: 7 + this.rng() * 3, roarFx: 0, minionT: 8, target: null, contrib: new Map() };
    this.monsters.set(m.id, m);
    return m;
  }
  debugSpawn(name, type, dx = 2, dz = 2, elite = false) {
    const p = this.world.pos.get(name);
    return this.create(type, p.x + dx, p.z + dz, 1, elite);
  }
  #trySpawn(p) {
    for (let i = 0; i < 4; i++) {
      const a = this.rng() * Math.PI * 2;
      const d = 26 + this.rng() * 32;
      const x = p.x + Math.cos(a) * d;
      const z = p.z + Math.sin(a) * d;
      if (Math.abs(x) > WORLD_HALF - 10 || Math.abs(z) > WORLD_HALF - 10 || deepWater(x, z) || isSafe(x, z)) continue;
      const b = biomeAt(x, z);
      const type = pickSpecies(b, Math.hypot(x, z), this.rng);
      if (!type) continue;
      if ([...this.monsters.values()].some((m) => Math.hypot(m.x - x, m.z - z) < 6)) continue;
      this.create(type, x, z, 1, this.rng() < RULES.eliteChance);
      return;
    }
  }

  // ---------- dano em jogadores ----------
  hurtPlayer(name, raw) {
    const p = this.ps(name);
    if (!p || p.dead) return;
    const t = this.now();
    const st = this.eco.stats(this.eco.player(name));
    const dmg = Math.max(1, Math.round(raw - st.def * 0.5)) * (t < p.shieldUntil ? 0.5 : 1);
    p.hp -= dmg;
    p.lastHurt = t;
    this.emit(name, { t: 'hurt', dmg: Math.round(dmg) });
    if (p.hp <= 0) {
      p.hp = 0;
      p.dead = true;
      p.deadUntil = t + RULES.reviveMs;
      this.emit(name, { t: 'died' });
    }
  }

  // ---------- ações do jogador ----------
  playerAttack(name, yaw) {
    const p = this.ps(name);
    if (!p || p.dead) fail('morto', 'Você não pode atacar agora');
    if (this.world.inMatch.has(name)) fail('batalha', 'Em duelo só vale o ataque do duelo');
    const t = this.now();
    if (t < p.atkReady) fail('rapido', 'Golpe rápido demais');
    p.atkReady = t + RULES.attackCooldownMs - 60;
    const atk = this.eco.stats(this.eco.player(name)).atk;
    const dir = [Math.sin(yaw), Math.cos(yaw)];
    let hits = 0;
    for (const m of [...this.monsters.values()]) {
      const dx = m.x - p.x;
      const dz = m.z - p.z;
      const d = Math.hypot(dx, dz);
      if (d > 3.3 + m.r * 0.5 + 1.0) continue;
      if (d > 0.5 && (dx / d) * dir[0] + (dz / d) * dir[1] < 0.15) continue;
      const crit = this.rng() < 0.1;
      this.#damage(name, m, Math.round(atk * (0.9 + 0.2 * this.rng()) * (crit ? 1.6 : 1)), crit);
      if (!m.boss && this.monsters.has(m.id) && d > 0.1) {
        m.x += (dx / d) * 0.8;
        m.z += (dz / d) * 0.8;
      }
      hits++;
    }
    return hits;
  }
  playerSkill(name, id, yaw) {
    const p = this.ps(name);
    if (!p || p.dead) fail('morto', 'Você não pode usar habilidades agora');
    if (this.world.inMatch.has(name)) fail('batalha', 'Habilidades ficam desligadas em duelos');
    const pl = this.eco.player(name);
    const lv = pl.skills[id];
    const sk = SKILLS[id];
    if (!sk || !lv) fail('skill', 'Você não aprendeu essa habilidade');
    const t = this.now();
    if (t < (p.skillReady[id] ?? 0)) fail('rapido', 'Habilidade em recarga');
    p.skillReady[id] = t + sk.cd[lv - 1] * 1000 - 300;
    const st = this.eco.stats(pl);
    const dir = [Math.sin(yaw), Math.cos(yaw)];
    this.emitNear(p.x, p.z, 90, { t: 'fx', kind: id, by: name, x: p.x, z: p.z, yaw }, name);
    if (id === 'fireball') {
      let best = null;
      let bd = 24;
      for (const m of this.monsters.values()) {
        const dx = m.x - p.x;
        const dz = m.z - p.z;
        const along = dx * dir[0] + dz * dir[1];
        const side = Math.abs(dx * dir[1] - dz * dir[0]);
        if (along > 0 && along < bd && side < m.r + 0.9) (bd = along), (best = m);
      }
      if (best) this.#damage(name, best, Math.round(sk.dmg[lv - 1] + st.atk * 0.5), false);
    } else if (id === 'whirl') {
      for (const m of [...this.monsters.values()]) if (Math.hypot(m.x - p.x, m.z - p.z) < 5 + m.r * 0.5) this.#damage(name, m, Math.round(sk.dmg[lv - 1] + st.atk * 0.4), false);
    } else if (id === 'heal') p.hp = Math.min(this.maxHp(name), p.hp + sk.heal[lv - 1]);
    else if (id === 'shield') p.shieldUntil = t + sk.dur[lv - 1] * 1000;
  }
  #damage(name, m, dmg, crit) {
    m.hp -= dmg;
    m.contrib.set(name, (m.contrib.get(name) ?? 0) + dmg);
    this.emitNear(m.x, m.z, 90, { t: 'mhit', id: m.id, dmg, crit, by: name, x: r2(m.x), z: r2(m.z) });
    if (m.hp <= 0) this.#die(m);
  }
  #die(m) {
    this.monsters.delete(m.id);
    this.emitNear(m.x, m.z, 100, { t: 'mdie', id: m.id, type: m.type, boss: m.boss, elite: m.elite, x: r2(m.x), z: r2(m.z) });
    if (m.boss) this.bossAt[m.type] = this.now() + RULES.bossRespawnMs;
    for (const name of m.contrib.keys()) {
      const p = this.world.pos.get(name);
      if (!p || Math.hypot(p.x - m.x, p.z - m.z) > 90) continue; // quem já foi embora não leva
      try {
        const r = this.eco.claimKill(name, m.type, { skipGap: true, mult: m.elite ? 3 : 1 });
        this.onReward(name, r, m);
      } catch {
        /* jogador removido durante a recompensa */
      }
    }
  }

  // ---------- chefes: cada região tem o seu; o Dragão só acorda para quem chegou ao último capítulo ----------
  #bosses(t) {
    const alive = new Set([...this.monsters.values()].filter((m) => m.boss).map((m) => m.type));
    for (const [type, d] of Object.entries(ENEMIES)) {
      if (!d.boss || alive.has(type) || t < (this.bossAt[type] ?? 0)) continue;
      const L = LOCATIONS[d.at];
      let ok = false;
      for (const [n, p] of this.world.pos) {
        if (Math.hypot(p.x - L.x, p.z - L.z) > Math.max(120, L.r + 70)) continue;
        if (d.gate !== undefined) {
          const c = this.eco.player(n).career;
          if (!(c?.done || (c?.chapter ?? 0) >= d.gate)) continue;
        }
        ok = true;
        break;
      }
      if (ok) this.create(type, L.x + (type === 'dragon' ? 18 : 0), L.z - (type === 'dragon' ? -14 : 6), 1, false);
    }
  }

  // ---------- simulação ----------
  update(dt) {
    const t = this.now();
    // jogadores: renascimento, regeneração e limite de vida
    for (const [name] of this.world.pos) {
      const p = this.ps(name);
      const max = this.maxHp(name);
      if (p.dead) {
        if (t >= p.deadUntil) {
          p.dead = false;
          p.hp = max;
          this.world.teleport(name, SPAWN.x, SPAWN.z);
          this.emit(name, { t: 'revive' });
        }
        continue;
      }
      p.hp = Math.min(p.hp, max);
      if (t - p.lastHurt > 5000 && p.hp < max) p.hp = Math.min(max, p.hp + dt * (2 + max * 0.02));
    }
    // aparecimento de monstros perto dos jogadores
    this.spawnT -= dt;
    if (this.spawnT <= 0) {
      this.spawnT = 0.35;
      for (const [, p] of this.world.pos) {
        if (this.world.inMatch.has(p.name) || this.monsters.size >= 150) continue;
        let near = 0;
        for (const m of this.monsters.values()) if (Math.hypot(m.x - p.x, m.z - p.z) < 75) near++;
        if (near < this.perPlayer) this.#trySpawn(p);
      }
      this.#bosses(t);
    }
    // IA
    for (const m of [...this.monsters.values()]) {
      let best = null;
      let bd = m.aggro;
      let cur = m.target ? this.world.pos.get(m.target) : null;
      if (cur && (!this.eligible(this.ps(m.target)) || Math.hypot(cur.x - m.x, cur.z - m.z) > m.aggro * 1.4)) (cur = null), (m.target = null);
      if (!cur) {
        for (const [name, p] of this.world.pos) {
          if (!this.eligible(this.ps(name))) continue;
          const d = Math.hypot(p.x - m.x, p.z - m.z);
          if (d < bd) (bd = d), (best = name);
        }
        if (best) (m.target = best), (cur = this.world.pos.get(best));
      }
      const home = Math.hypot(m.x - m.hx, m.z - m.hz);
      let mx = 0;
      let mz = 0;
      let dist = Infinity;
      if (cur && home < (m.boss ? 70 : 60)) {
        const dx = cur.x - m.x;
        const dz = cur.z - m.z;
        dist = Math.hypot(dx, dz);
        m.yaw = Math.atan2(dx, dz);
        if (dist > 1.4 + m.r * 0.4) (mx = dx / dist), (mz = dz / dist);
      } else if (home > 4) {
        mx = (m.hx - m.x) / home;
        mz = (m.hz - m.z) / home;
        m.target = null;
        m.yaw = Math.atan2(mx, mz);
      } else m.target = null;
      m.moving = !!(mx || mz);
      if (m.moving) {
        const sp = m.speed * dt * (cur ? 1 : 0.6);
        const nx = m.x + mx * sp;
        const nz = m.z + mz * sp;
        if (!isSafe(nx, nz) && !deepWater(nx, nz)) (m.x = nx), (m.z = nz);
        else m.moving = false;
      }
      m.cd = Math.max(0, m.cd - dt);
      m.atkT = Math.max(0, m.atkT - dt);
      if (m.boss) this.#bossAbilities(m, dt);
      if (cur && m.cd <= 0 && dist < 1.7 + m.r * 0.6 && Math.abs((cur.y ?? 0) - heightAt(m.x, m.z)) < 3) {
        m.cd = m.boss ? 1.4 : 1.0;
        m.atkT = 0.35;
        this.hurtPlayer(m.target, m.atk);
      }
      // sem jogador por perto: some (o chefe volta ao máximo de vida quando for recriado)
      let anyone = false;
      for (const p of this.world.pos.values()) {
        if (Math.hypot(p.x - m.x, p.z - m.z) < (m.boss ? 220 : 130)) {
          anyone = true;
          break;
        }
      }
      if (!anyone) this.monsters.delete(m.id);
    }
  }

  #bossAbilities(m, dt) {
    const d = ENEMIES[m.type];
    if (d.phases && !m.enraged && m.hp < m.max / 2) {
      m.enraged = true;
      m.atk *= 1.35;
      m.speed *= 1.2;
      m.minionT = 0;
    }
    m.roarFx = Math.max(0, m.roarFx - dt);
    m.roarT -= dt;
    if (m.roarT <= 0 && m.target) {
      m.roarT = d.phases ? 7 : 9;
      m.roarFx = 0.7;
      for (const [n, p] of this.world.pos) if (this.eligible(this.ps(n)) && Math.hypot(p.x - m.x, p.z - m.z) < 10) this.hurtPlayer(n, m.atk * 0.5);
    }
    if (d.phases && m.enraged) {
      m.minionT -= dt;
      if (m.minionT <= 0) {
        m.minionT = 20;
        const minions = [...this.monsters.values()].filter((o) => o.type === 'imp').length;
        for (let i = minions; i < 4 && i < minions + 2; i++) {
          const a = this.rng() * Math.PI * 2;
          this.create('imp', m.x + Math.cos(a) * 6, m.z + Math.sin(a) * 6, 1, false);
        }
      }
    }
  }

  // ---------- o que cada jogador recebe ----------
  snapshotFor(name) {
    const p = this.world.pos.get(name);
    if (!p) return [];
    const out = [];
    for (const m of this.monsters.values()) if (Math.hypot(m.x - p.x, m.z - p.z) < 100) out.push([m.id, m.type, r2(m.x), r2(m.z), r2(m.yaw), Math.ceil(m.hp), m.max, (m.moving ? 1 : 0) | (m.atkT > 0 ? 2 : 0) | (m.elite ? ELITE : 0) | (m.enraged ? ENRAGED : 0) | (m.roarFx > 0 ? ROAR : 0)]);
    return out;
  }
  // vida só é enviada quando muda
  hpMessage(name) {
    const p = this.ps(name);
    if (!p) return null;
    const msg = { t: 'php', hp: Math.round(p.hp), max: this.maxHp(name), sh: Math.max(0, Math.round((p.shieldUntil - this.now()) / 100) / 10), dead: p.dead };
    const key = `${msg.hp}|${msg.max}|${msg.sh}|${msg.dead}`;
    if (key === p.sent) return null;
    p.sent = key;
    return msg;
  }
}
