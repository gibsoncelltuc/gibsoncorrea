// Teste de integração ONLINE: sobe o servidor de verdade e conecta dois jogadores por WebSocket.
// Cobre: presença, chat, carreira (capítulos 1 e 2), anti-teleporte, bioma, duelo PvP até o fim e auditoria final das moedas.
import test, { before, after } from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { LOCATIONS, SPAWN } from '../public/shared/world.js';

const root = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const PORT = 8830 + Math.floor(Math.random() * 100);
const DATA = path.join(os.tmpdir(), `arena-online-${process.pid}.json`);
let server;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const step = (s) => process.env.TEST_STEPS && console.error('[passo]', s);

class Client {
  constructor(name) {
    this.name = name;
    this.seq = 1;
    this.pending = new Map();
    this.events = [];
    this.pos = { x: SPAWN.x, y: 0, z: SPAWN.z };
  }
  async connect() {
    this.ws = new WebSocket(`ws://127.0.0.1:${PORT}`);
    await new Promise((res, rej) => {
      this.ws.onopen = res;
      this.ws.onerror = () => rej(new Error('sem conexão'));
    });
    this.ws.onmessage = (ev) => {
      const m = JSON.parse(ev.data);
      if (m.id && this.pending.has(m.id)) {
        const p = this.pending.get(m.id);
        this.pending.delete(m.id);
        return m.ok ? p.res(m) : p.rej(Object.assign(new Error(m.error), { code: m.code }));
      }
      if (m.t === 'state') this.state = m.state;
      if (m.t === 'tp') this.pos = { x: m.x, y: 0, z: m.z };
      this.events.push(m);
    };
    const r = await this.call('register', { name: this.name });
    this.state = r.state;
    return r;
  }
  call(t, data = {}) {
    return new Promise((res, rej) => {
      const id = this.seq++;
      this.pending.set(id, { res, rej });
      this.ws.send(JSON.stringify({ id, t, ...data }));
      setTimeout(() => {
        if (this.pending.delete(id)) rej(new Error(`sem resposta do servidor para "${t}"`));
      }, 5000);
    });
  }
  fire(t, data = {}) {
    this.ws.send(JSON.stringify({ t, ...data }));
  }
  // anda em passos curtos (o servidor limita a velocidade)
  async walk(x, z) {
    while (Math.hypot(x - this.pos.x, z - this.pos.z) > 0.01) {
      const d = Math.hypot(x - this.pos.x, z - this.pos.z);
      const k = Math.min(1, 4 / d);
      this.pos = { x: this.pos.x + (x - this.pos.x) * k, y: 0, z: this.pos.z + (z - this.pos.z) * k };
      this.fire('move', { ...this.pos, yaw: 0, a: 1 });
      await sleep(45); // ~22 mensagens/s, abaixo do limite do servidor (30/s)
    }
    await sleep(60);
  }
  async until(pred, ms = 3000) {
    const t0 = Date.now();
    while (Date.now() - t0 < ms) {
      const e = this.events.find(pred);
      if (e) return e;
      await sleep(25);
    }
    throw new Error('evento não chegou');
  }
}

before(async () => {
  fs.rmSync(DATA, { force: true });
  server = spawn(process.execPath, ['server/index.js'], { cwd: root, env: { ...process.env, PORT: String(PORT), DATA_FILE: DATA, ARENA_TEST: '1' }, stdio: ['ignore', 'ignore', 'inherit'] });
  for (let i = 0; i < 80; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${PORT}/`);
      if (r.ok) return;
    } catch {
      /* ainda subindo */
    }
    await sleep(100);
  }
  throw new Error('servidor não subiu');
});
after(() => server?.kill('SIGTERM'));

test('online: presença, chat, anti-teleporte, carreira, bioma e duelo PvP com auditoria final', async () => {
  const a = new Client('Alice');
  const b = new Client('Bob');
  await a.connect();
  await b.connect();

  step('presença');
  // presença: cada um enxerga o outro com perfil
  await a.until((m) => m.t === 'presence' && m.p.some((p) => p[0] === 'Bob'));
  assert.ok(a.events.some((m) => m.t === 'profile' && m.n === 'Bob'), 'perfil do Bob chegou para a Alice');

  step('chat');
  // chat com limite de frequência
  await b.call('chat', { text: 'oi pessoal' });
  await a.until((m) => m.t === 'chat' && m.n === 'Bob' && m.text === 'oi pessoal');
  await assert.rejects(b.call('chat', { text: 'de novo' }), (e) => e.code === 'rapido');

  step('anti-teleporte');
  // anti-teleporte: salto enorme é recusado e o servidor devolve a posição
  a.fire('move', { x: 250, y: 0, z: 250, yaw: 0, a: 1 });
  const snap = await a.until((m) => m.t === 'tp');
  assert.ok(Math.hypot(snap.x - SPAWN.x, snap.z - SPAWN.z) < 6);
  a.pos = { x: snap.x, y: 0, z: snap.z };

  step('bioma');
  // o cliente NÃO consegue mais reivindicar mortes: só o servidor credita recompensas
  await assert.rejects(a.call('kill', { type: 'slime' }), (e) => e.code === 'comando');
  await assert.rejects(a.call('attack', { yaw: 0 }).then(() => a.call('attack', { yaw: 0 })), (e) => e.code === 'rapido', 'intervalo de golpe é do servidor');

  step('carreira cap.1');
  // carreira: falar com o prefeito exige estar perto dele
  await assert.rejects(a.call('talk', { npc: 'mayor' }), (e) => e.code === 'longe');
  await a.walk(10, 12);
  await a.walk(LOCATIONS.mayor.x, LOCATIONS.mayor.z + 2);
  const t1 = await a.call('talk', { npc: 'mayor' });
  assert.equal(t1.career.quest.id, 2, 'capítulo 1 concluído');
  await a.until((m) => m.t === 'state' && m.state.coins >= 140);
  step('cap.2 (8 gosmas)');
  await a.walk(0, 60); // campos ao redor da vila (bioma de gosma)
  const rewardsOf = (c, type) => c.events.filter((m) => m.t === 'reward' && (!type || m.type === type)).length;
  for (let i = 0; i < 8; i++) {
    await a.call('debug_spawn', { type: 'slime', dx: 0, dz: 1.2 });
    const before = rewardsOf(a);
    for (let k = 0; k < 14 && rewardsOf(a) === before; k++) {
      a.fire('attack', { yaw: 0 });
      await sleep(430);
    }
    assert.ok(rewardsOf(a) > before, `a gosma ${i + 1} deveria ter morrido e dado recompensa do servidor`);
  }
  await a.until((m) => m.t === 'state' && m.state.career.chapter === 2);
  assert.equal((await a.call('career')).career.quest.id, 3, 'capítulo 2 concluído por monstros reais do servidor');

  // cooperação: os dois acertam a MESMA gosma e os dois recebem recompensa
  step('co-op');
  await b.walk(0, 60);
  const [ra, rb] = [rewardsOf(a), rewardsOf(b)];
  for (let tries = 0; tries < 6 && !(rewardsOf(a) > ra && rewardsOf(b) > rb); tries++) {
    await a.call('debug_spawn', { type: 'slime', dx: 0, dz: 1.0 });
    for (let k = 0; k < 6 && !(rewardsOf(a) > ra && rewardsOf(b) > rb); k++) {
      (k % 2 ? b : a).fire('attack', { yaw: 0 });
      await sleep(430);
    }
  }
  assert.ok(rewardsOf(a) > ra && rewardsOf(b) > rb, 'os dois jogadores receberam a recompensa do mesmo monstro');

  step('duelo: caminhada');
  // duelo: os dois vão ao Coliseu e entram na fila
  const C = LOCATIONS.colosseum;
  await assert.rejects(b.call('battle_join'), (e) => e.code === 'longe');
  for (const c of [a, b]) {
    await c.walk(40, 30);
    await c.walk(C.x - 36, C.z - 4);
  }
  step('duelo: fila');
  const before = a.state.coins;
  await a.call('battle_join');
  await b.call('battle_join');
  await a.until((m) => m.t === 'battle' && m.phase === 'start');
  await b.until((m) => m.t === 'battle' && m.phase === 'start');
  await a.until((m) => m.t === 'state' && m.state.coins === before - 10);
  const tpA = await a.until((m) => m.t === 'tp' && Math.hypot(m.x - (C.x - 10), m.z - C.z) < 1);
  a.pos = { x: tpA.x, y: 0, z: tpA.z };
  const tpB = await b.until((m) => m.t === 'tp' && Math.hypot(m.x - (C.x + 10), m.z - C.z) < 1);
  b.pos = { x: tpB.x, y: 0, z: tpB.z };
  step('duelo: aproxima');
  await a.walk(C.x - 1, C.z); // aproxima dentro da arena
  await b.walk(C.x + 1, C.z);
  await assert.rejects(a.call('battle_hit', { target: 'Alice' }), (e) => e.code === 'alvo');
  step('duelo: golpes');
  let end = null;
  for (let i = 0; i < 80 && !end; i++) {
    try {
      await a.call('battle_hit', { target: 'Bob' });
    } catch (e) {
      assert.ok(['rapido', 'batalha'].includes(e.code), `erro inesperado ${e.code}`);
    }
    end = a.events.find((m) => m.t === 'battle' && m.phase === 'end');
    await sleep(470);
  }
  assert.ok(end, 'o duelo terminou');
  assert.equal(end.winner, 'Alice');
  assert.equal(end.prize, 18);
  await sleep(200);

  step('pós-duelo');
  // anti-trapaça: Bob já saiu do duelo e não pode ser atingido
  await assert.rejects(a.call('battle_hit', { target: 'Bob' }), (e) => e.code === 'batalha');
  a.ws.close();
  b.ws.close();
  await sleep(300);
  server.kill('SIGTERM');
  await sleep(600);

  // auditoria das moedas direto do arquivo salvo
  const d = JSON.parse(fs.readFileSync(DATA, 'utf8'));
  const players = Object.values(d.players).reduce((s, p) => s + p.coins, 0);
  const escrowT = d.tournaments.filter((t) => t.status === 'open').reduce((s, t) => s + t.pool, 0);
  assert.equal(d.stats.escrowBattle, 0);
  assert.equal(d.stats.minted, players + escrowT + d.stats.escrowBattle + d.stats.burned, `auditoria: ${JSON.stringify(d.stats)} jogadores=${players}`);
});
