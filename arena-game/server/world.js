// Mundo online: posições dos jogadores, chat e duelos (PvP). Lógica pura: não usa rede (o index.js liga os sockets).
// O servidor é a autoridade: valida velocidade, bioma dos inimigos, distância dos golpes e quem ganhou o duelo.
import { inWorld, biomeAt, ENEMY_BIOMES, ARENA_SPAWNS, ARENA_RADIUS, LOCATIONS, SPAWN, CRYSTALS, WORLD_HALF } from '../public/shared/world.js';
import { RULES, ITEMS } from './catalog.js';
import { GameError } from './economy.js';

const fail = (code, msg) => {
  throw new GameError(code, msg);
};
const r2 = (n) => Math.round(n * 100) / 100;

export class World {
  constructor(eco, { now = Date.now, emit = () => {}, touch = () => {}, rng = Math.random } = {}) {
    this.eco = eco;
    this.now = now;
    this.emit = emit; // (nome, mensagem) -> envia a um jogador
    this.touch = touch; // (nome) -> reenvia o estado do jogador (moedas mudaram)
    this.rng = rng;
    this.pos = new Map();
    this.queue = [];
    this.inMatch = new Map();
    this.chatLast = new Map();
    this.seq = 1;
    // se o servidor caiu no meio de um duelo, devolve as apostas que ficaram em custódia
    this.recoverEscrow();
  }

  recoverEscrow() {
    const stuck = this.eco.d.stats.escrowBattle;
    if (stuck > 0 && this.eco.d.battleLocks) {
      for (const [name, fee] of Object.entries(this.eco.d.battleLocks)) {
        try {
          this.eco.battleRefund(name, fee);
        } catch {
          /* jogador removido: o valor fica registrado como destruído abaixo */
        }
      }
      this.eco.d.battleLocks = {};
    }
  }
  #lock(name, fee) {
    this.eco.battleLock(name, fee);
    (this.eco.d.battleLocks ??= {})[name] = (this.eco.d.battleLocks[name] ?? 0) + fee;
  }
  #unlock(name, fee) {
    this.eco.battleRefund(name, fee);
    this.eco.d.battleLocks[name] -= fee;
    if (this.eco.d.battleLocks[name] <= 0) delete this.eco.d.battleLocks[name];
  }

  // ---------- presença ----------
  join(name) {
    this.pos.set(name, { name, x: SPAWN.x, y: 0, z: SPAWN.z, yaw: 0, a: 0, t: this.now() });
  }
  leave(name) {
    this.pos.delete(name);
    this.cancelQueue(name);
    const m = this.inMatch.get(name);
    if (m) this.endMatch(m, m.a === name ? m.b : m.a, 'abandono');
  }
  position(name) {
    return this.pos.get(name) ?? null;
  }
  teleport(name, x, z) {
    const p = this.pos.get(name);
    if (p) Object.assign(p, { x, y: 0, z, t: this.now() });
    this.emit(name, { t: 'tp', x, z });
  }
  move(name, d) {
    const cur = this.pos.get(name);
    if (!cur) return { ok: false };
    const x = Number(d.x);
    const y = Number(d.y);
    const z = Number(d.z);
    if (![x, y, z].every(Number.isFinite)) return { ok: false };
    const t = this.now();
    const dt = Math.min(2, Math.max(0.05, (t - cur.t) / 1000));
    const dist = Math.hypot(x - cur.x, z - cur.z);
    const m = this.inMatch.get(name);
    const arena = LOCATIONS.colosseum;
    const outOfArena = m && Math.hypot(x - arena.x, z - arena.z) > ARENA_RADIUS + 2;
    if (!inWorld(x, z) || dist > 30 * dt + 4 || outOfArena) return { ok: false, snap: { x: cur.x, z: cur.z } };
    Object.assign(cur, { x, y: Math.max(-5, Math.min(120, y)), z, yaw: Number(d.yaw) || 0, a: (d.a | 0) % 8, t });
    return { ok: true };
  }
  respawn(name) {
    if (this.inMatch.has(name)) fail('batalha', 'Você está em um duelo');
    this.teleport(name, SPAWN.x, SPAWN.z);
  }
  snapshot() {
    const out = [];
    for (const [n, p] of this.pos) {
      const m = this.inMatch.get(n);
      out.push([n, r2(p.x), r2(p.y), r2(p.z), r2(p.yaw), p.a, m ? Math.max(0, Math.round(m.hp[n])) : -1]);
    }
    return out;
  }

  // ---------- chat ----------
  chat(name, text) {
    const t = this.now();
    if (t - (this.chatLast.get(name) ?? 0) < 800) fail('rapido', 'Devagar com o chat');
    const clean = String(text ?? '').replace(/[\u0000-\u001f\u007f]/g, '').trim().slice(0, 120);
    if (!clean) fail('vazio', 'Mensagem vazia');
    this.chatLast.set(name, t);
    return { n: name, text: clean };
  }

  // ---------- validações usadas pela carreira e pelas recompensas ----------
  canKill(name, type) {
    const p = this.pos.get(name);
    const ok = ENEMY_BIOMES[type];
    if (!p || !ok) return false;
    for (const [dx, dz] of [[0, 0], [25, 0], [-25, 0], [0, 25], [0, -25]]) if (ok.includes(biomeAt(p.x + dx, p.z + dz))) return true;
    return false;
  }
  near(name, key, extra = 8) {
    const p = this.pos.get(name);
    const l = LOCATIONS[key];
    return !!p && !!l && Math.hypot(p.x - l.x, p.z - l.z) <= l.r + extra;
  }
  nearCrystal(name, id) {
    const p = this.pos.get(name);
    const c = CRYSTALS.find((k) => k.id === id);
    return !!p && !!c && Math.hypot(p.x - c.x, p.z - c.z) <= 9;
  }

  // ---------- duelos 1x1 ----------
  queued(name) {
    return this.queue.includes(name);
  }
  queueJoin(name) {
    if (this.inMatch.has(name)) fail('batalha', 'Você já está em um duelo');
    if (this.queue.includes(name)) fail('fila', 'Você já está na fila');
    if (!this.near(name, 'colosseum', 6)) fail('longe', 'Vá até o Coliseu para entrar na fila');
    this.#lock(name, RULES.battleFee);
    this.queue.push(name);
    this.#tryMatch();
  }
  cancelQueue(name) {
    const i = this.queue.indexOf(name);
    if (i < 0) return false;
    this.queue.splice(i, 1);
    this.#unlock(name, RULES.battleFee);
    return true;
  }
  #tryMatch() {
    while (this.queue.length >= 2) {
      const a = this.queue.shift();
      const b = this.queue.shift();
      const maxHp = { [a]: this.eco.stats(this.eco.player(a)).hp, [b]: this.eco.stats(this.eco.player(b)).hp };
      const m = { id: 'm' + this.seq++, a, b, hp: { ...maxHp }, maxHp, pot: RULES.battleFee * 2, start: this.now(), cd: {}, over: false };
      this.inMatch.set(a, m);
      this.inMatch.set(b, m);
      this.teleport(a, ARENA_SPAWNS[0].x, ARENA_SPAWNS[0].z);
      this.teleport(b, ARENA_SPAWNS[1].x, ARENA_SPAWNS[1].z);
      for (const [me, op] of [[a, b], [b, a]]) this.emit(me, { t: 'battle', phase: 'start', id: m.id, opponent: op, hp: m.hp, maxHp: m.maxHp, seconds: RULES.battleSeconds, pot: m.pot });
    }
  }
  hit(attacker, target) {
    const m = this.inMatch.get(attacker);
    if (!m || m.over) fail('batalha', 'Você não está em um duelo');
    const foe = m.a === attacker ? m.b : m.a;
    if (target !== foe) fail('alvo', 'Alvo inválido');
    const t = this.now();
    if (t - (m.cd[attacker] ?? 0) < RULES.battleCooldownMs) fail('rapido', 'Golpe rápido demais');
    const pa = this.pos.get(attacker);
    const pb = this.pos.get(foe);
    if (!pa || !pb) fail('pos', 'Posição desconhecida');
    if (Math.hypot(pa.x - pb.x, pa.z - pb.z) > 5.5) fail('longe', 'Fora de alcance');
    m.cd[attacker] = t;
    const sa = this.eco.stats(this.eco.player(attacker));
    const sb = this.eco.stats(this.eco.player(foe));
    const dmg = Math.max(1, Math.round(sa.atk * (0.85 + 0.3 * this.rng()) - sb.def * 0.5));
    m.hp[foe] = Math.max(0, m.hp[foe] - dmg);
    for (const n of [m.a, m.b]) this.emit(n, { t: 'battle', phase: 'hit', by: attacker, target: foe, dmg, hp: m.hp });
    if (m.hp[foe] <= 0) this.endMatch(m, attacker, 'ko');
    return dmg;
  }
  endMatch(m, winner, reason) {
    if (m.over) return;
    m.over = true;
    let result = { winner: winner ?? null, reason, prize: 0 };
    if (winner) {
      // a aposta do perdedor e a do vencedor estão na custódia; libera as duas contas de trava e paga o prêmio
      for (const n of [m.a, m.b]) this.eco.d.battleLocks[n] = (this.eco.d.battleLocks[n] ?? 0) - RULES.battleFee;
      for (const n of [m.a, m.b]) if (this.eco.d.battleLocks[n] <= 0) delete this.eco.d.battleLocks[n];
      const r = this.eco.battleSettle(winner, m.pot);
      result = { ...result, prize: r.prize };
    } else {
      this.#unlock(m.a, RULES.battleFee);
      this.#unlock(m.b, RULES.battleFee);
    }
    for (const n of [m.a, m.b]) {
      this.inMatch.delete(n);
      if (this.pos.has(n)) this.teleport(n, SPAWN.x, SPAWN.z);
      this.emit(n, { t: 'battle', phase: 'end', ...result });
      this.touch(n);
    }
  }
  // chamado a cada segundo: encerra duelos por tempo (vence quem tem mais vida; empate devolve as apostas)
  tick() {
    const t = this.now();
    for (const m of new Set(this.inMatch.values())) {
      if (m.over || t - m.start < RULES.battleSeconds * 1000) continue;
      const ra = m.hp[m.a] / m.maxHp[m.a];
      const rb = m.hp[m.b] / m.maxHp[m.b];
      this.endMatch(m, Math.abs(ra - rb) < 1e-9 ? null : ra > rb ? m.a : m.b, 'tempo');
    }
  }
}
export { WORLD_HALF, ITEMS };
