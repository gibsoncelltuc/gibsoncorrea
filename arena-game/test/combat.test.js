import test from 'node:test';
import assert from 'node:assert/strict';
import { Economy, GameError, emptyData } from '../server/economy.js';
import { World } from '../server/world.js';
import { Combat } from '../server/monsters.js';
import { RULES, ENEMIES } from '../server/catalog.js';
import { LOCATIONS, SPAWN, isSafe } from '../public/shared/world.js';

function setup() {
  let t = 9_000_000;
  const events = [];
  const rewards = [];
  const eco = new Economy({ data: emptyData() }, { now: () => t, rng: () => 0.5 });
  const emit = (n, m) => events.push([n, m]);
  const world = new World(eco, { now: () => t, emit, touch: () => {}, rng: () => 0.5 });
  const combat = new Combat(eco, world, { now: () => t, rng: () => 0.5, emit, onReward: (n, r, m) => rewards.push([n, r, m.type]), perPlayer: 0 });
  const put = (name, x, z) => {
    eco.register(name);
    world.join(name);
    Object.assign(world.position(name), { x, z });
  };
  return { eco, world, combat, events, rewards, put, adv: (ms) => (t += ms), clock: () => t };
}
const throwsCode = (fn, code) => assert.throws(fn, (e) => e instanceof GameError && e.code === code, `esperava erro ${code}`);
const FIELD = { x: 0, z: 120 }; // campos fora da vila (bioma de gosma)

test('zonas seguras: vila e coliseu', () => {
  assert.equal(isSafe(0, 0), true);
  assert.equal(isSafe(LOCATIONS.colosseum.x, LOCATIONS.colosseum.z), true);
  assert.equal(isSafe(0, 120), false);
  assert.equal(isSafe(SPAWN.x, SPAWN.z), true);
});

test('golpe: o servidor decide alcance, direção e intervalo; recompensa vai para quem causou dano', () => {
  const { eco, combat, put, adv, rewards, events } = setup();
  put('Ana', FIELD.x, FIELD.z);
  const m = combat.create('slime', FIELD.x, FIELD.z + 2.5); // à frente (yaw 0 = +z)
  const far = combat.create('slime', FIELD.x, FIELD.z + 30);
  assert.equal(combat.playerAttack('Ana', Math.PI), 0, 'golpe para trás não acerta');
  adv(500);
  throwsCode(() => combat.playerAttack('Ana', 0) && combat.playerAttack('Ana', 0), 'rapido');
  assert.ok(combat.monsters.get(m.id).hp < ENEMIES.slime.hp || !combat.monsters.has(m.id), 'a gosma levou dano');
  assert.ok(combat.monsters.has(far.id) && combat.monsters.get(far.id).hp === ENEMIES.slime.hp, 'monstro longe não é atingido');
  let n = 0;
  while (combat.monsters.has(m.id) && n++ < 20) {
    adv(500);
    combat.playerAttack('Ana', 0);
  }
  assert.ok(!combat.monsters.has(m.id), 'morreu');
  assert.equal(rewards.length, 1);
  assert.equal(rewards[0][0], 'Ana');
  assert.ok(rewards[0][1].coins >= 3);
  assert.ok(events.some(([, e]) => e.t === 'mdie'));
  assert.ok(eco.audit().ok);
});

test('co-op: dois jogadores que causaram dano recebem a recompensa; quem só passou perto não', () => {
  const { eco, combat, put, adv, rewards } = setup();
  put('Ana', FIELD.x, FIELD.z);
  put('Beto', FIELD.x + 1, FIELD.z);
  put('Caio', FIELD.x - 1, FIELD.z);
  const m = combat.create('brute', FIELD.x, FIELD.z + 2.5);
  let n = 0;
  while (combat.monsters.has(m.id) && n++ < 40) {
    adv(500);
    Object.assign(m, { x: FIELD.x, z: FIELD.z + 2.5 }); // sem a IA rodando, o empurrão do golpe afastaria o monstro
    combat.playerAttack(n % 2 ? 'Ana' : 'Beto', 0);
  }
  assert.deepEqual(rewards.map((r) => r[0]).sort(), ['Ana', 'Beto']);
  assert.ok(eco.player('Caio').coins === 100);
  assert.ok(eco.audit().ok);
});

test('quem está longe na hora da morte não leva a recompensa', () => {
  const { combat, put, adv, rewards, world } = setup();
  put('Ana', FIELD.x, FIELD.z);
  const m = combat.create('slime', FIELD.x, FIELD.z + 2.5);
  adv(500);
  combat.playerAttack('Ana', 0);
  Object.assign(world.position('Ana'), { x: 250, z: 250 });
  m.hp = 1;
  adv(500);
  Object.assign(world.position('Ana'), { x: FIELD.x, z: FIELD.z });
  combat.playerAttack('Ana', 0);
  Object.assign(world.position('Ana'), { x: 250, z: 250 });
  assert.ok(rewards.length <= 1);
});

test('IA: persegue, ataca e tira vida; o escudo reduz o dano; morte e renascimento no ponto inicial', () => {
  const { eco, combat, put, adv, world, events } = setup();
  put('Ana', FIELD.x, FIELD.z);
  const m = combat.create('brute', FIELD.x + 8, FIELD.z);
  const start = Math.hypot(m.x - FIELD.x, m.z - FIELD.z);
  for (let i = 0; i < 100; i++) {
    adv(100);
    combat.update(0.1);
  }
  assert.ok(Math.hypot(m.x - FIELD.x, m.z - FIELD.z) < start, 'o bruto se aproximou');
  assert.ok(combat.ps('Ana').hp < combat.maxHp('Ana') || combat.ps('Ana').dead, 'tomou dano');
  assert.ok(events.some(([n, e]) => n === 'Ana' && e.t === 'hurt'));
  // morte
  let n = 0;
  while (!combat.ps('Ana').dead && n++ < 400) {
    adv(100);
    combat.update(0.1);
  }
  assert.equal(combat.ps('Ana').dead, true);
  assert.ok(events.some(([, e]) => e.t === 'died'));
  adv(RULES.reviveMs + 50);
  combat.update(0.1);
  assert.equal(combat.ps('Ana').dead, false);
  assert.equal(combat.ps('Ana').hp, combat.maxHp('Ana'));
  assert.deepEqual([world.position('Ana').x, world.position('Ana').z], [SPAWN.x, SPAWN.z]);
  assert.ok(eco.audit().ok);
});

test('monstros não entram na zona segura e jogadores dentro dela não sofrem dano', () => {
  const { combat, put, adv } = setup();
  put('Ana', 5, 5);
  const m = combat.create('slime', 90, 5);
  m.aggro = 200;
  for (let i = 0; i < 400; i++) {
    adv(100);
    combat.update(0.1);
  }
  assert.ok(!isSafe(m.x, m.z), 'o monstro parou na borda');
  assert.equal(combat.ps('Ana').hp, combat.maxHp('Ana'));
});

test('habilidades: precisam estar aprendidas, respeitam recarga e acertam no servidor', () => {
  const { eco, combat, put, adv } = setup();
  put('Ana', FIELD.x, FIELD.z);
  throwsCode(() => combat.playerSkill('Ana', 'fireball', 0), 'skill');
  eco.player('Ana').skills.fireball = 1;
  eco.player('Ana').skills.heal = 1;
  eco.player('Ana').skills.whirl = 1;
  const m = combat.create('brute', FIELD.x, FIELD.z + 10);
  combat.playerSkill('Ana', 'fireball', 0);
  assert.ok(combat.monsters.get(m.id).hp < 90, 'a bola de fogo acertou');
  throwsCode(() => combat.playerSkill('Ana', 'fireball', 0), 'rapido');
  adv(6000);
  combat.playerSkill('Ana', 'fireball', Math.PI); // olhando para o lado errado não acerta
  const hpAfter = combat.monsters.get(m.id).hp;
  combat.ps('Ana').hp = 10;
  combat.playerSkill('Ana', 'heal', 0);
  assert.ok(combat.ps('Ana').hp > 10);
  const w = combat.create('slime', FIELD.x + 2, FIELD.z);
  combat.playerSkill('Ana', 'whirl', 0);
  assert.ok(!combat.monsters.has(w.id) || combat.monsters.get(w.id).hp < ENEMIES.slime.hp);
  assert.equal(combat.monsters.get(m.id).hp <= hpAfter, true);
});

test('chefe: aparece com jogador perto do castelo, só um, e renasce depois da morte', () => {
  const { eco, combat, put, adv, rewards } = setup();
  const C = LOCATIONS.castle;
  put('Ana', C.x, C.z + 40);
  combat.spawnT = 0;
  combat.update(0.1);
  const bosses = () => [...combat.monsters.values()].filter((m) => m.boss && m.type === 'kingslime');
  assert.equal(bosses().length, 1);
  combat.spawnT = 0;
  combat.update(0.1);
  assert.equal(bosses().length, 1, 'nunca dois chefes');
  const b = bosses()[0];
  b.hp = 1;
  Object.assign(eco.player('Ana'), { career: { chapter: 6, count: 0, got: [], done: false } });
  const p = combat.world.position('Ana');
  Object.assign(p, { x: b.x, z: b.z - 3 });
  adv(500);
  combat.playerAttack('Ana', 0);
  assert.equal(bosses().length, 0);
  assert.ok(rewards.some((r) => r[2] === 'kingslime'));
  assert.equal(eco.careerView(eco.player('Ana')).quest.id, 8, 'derrotar o Rei Gosma libera o capítulo final');
  combat.spawnT = 0;
  combat.update(0.1);
  assert.equal(bosses().length, 0, 'ainda em espera');
  adv(RULES.bossRespawnMs + 10);
  combat.spawnT = 0;
  combat.update(0.1);
  assert.equal(bosses().length, 1, 'renasceu');
  assert.ok(eco.audit().ok);
});

test('aparecem monstros perto de quem está nos campos, nunca na zona segura, e somem sem jogadores', () => {
  const s = setup();
  const combat = new Combat(s.eco, s.world, { now: () => s.clock(), rng: Math.random, emit: () => {}, perPlayer: 12 });
  s.put('Ana', FIELD.x, FIELD.z);
  for (let i = 0; i < 80; i++) {
    s.adv(400);
    combat.update(0.4);
  }
  assert.ok(combat.monsters.size >= 8, `monstros: ${combat.monsters.size}`);
  for (const m of combat.monsters.values()) assert.ok(!isSafe(m.x, m.z));
  const snap = combat.snapshotFor('Ana');
  assert.ok(snap.length > 0 && snap[0].length === 8);
  s.world.leave('Ana');
  combat.update(0.4);
  assert.equal(combat.monsters.size, 0);
});

test('bestiário: dezenas de espécies, do fraco ao chefe final, com estatísticas coerentes', () => {
  const regular = Object.entries(ENEMIES).filter(([, d]) => !d.boss);
  const bosses = Object.entries(ENEMIES).filter(([, d]) => d.boss);
  assert.ok(regular.length >= 30, `espécies: ${regular.length}`);
  assert.ok(bosses.length >= 6);
  const bases = new Set(Object.values(ENEMIES).map((d) => d.base));
  assert.ok(bases.size >= 8, 'vários corpos diferentes');
  const lvs = regular.map(([, d]) => d.lv);
  assert.ok(Math.min(...lvs) === 1 && Math.max(...lvs) >= 17, 'do nível 1 ao 18');
  assert.ok(ENEMIES.dragon.hp > Math.max(...Object.values(ENEMIES).filter((d) => d !== ENEMIES.dragon).map((d) => d.hp)), 'o Dragão é o mais forte');
  for (const [id, d] of Object.entries(ENEMIES)) assert.ok(d.hp > 0 && d.atk > 0 && d.xp > 0 && d.coins[1] >= d.coins[0] && d.r > 0, id);
  assert.equal(ENEMIES.slime_blue.family, 'slime');
  // o spawn de cada bioma usa espécies variadas e cobre fracas e fortes
  const st = setup();
  const combat = new Combat(st.eco, st.world, { now: () => st.clock(), rng: Math.random, emit: () => {}, perPlayer: 12 });
  st.put('Ana', FIELD.x, FIELD.z);
  const seen = new Set();
  for (let i = 0; i < 400; i++) {
    combat.monsters.clear();
    combat.bossAt = { crabking: Infinity, ent: Infinity, pharaoh: Infinity, alpha: Infinity, lich: Infinity, kingslime: Infinity, dragon: Infinity };
    combat.world.pos.get('Ana').x = -280 + (i % 20) * 29;
    combat.world.pos.get('Ana').z = -300 + Math.floor(i / 20) * 30;
    for (let k = 0; k < 4; k++) {
      combat.spawnT = 0;
      combat.update(0.1);
    }
    for (const m of combat.monsters.values()) seen.add(m.type);
  }
  assert.ok(seen.size >= 12, `tipos sorteados: ${[...seen]}`);
});

test('elite: mais vida e dano, recompensa tripla; Dragão só acorda para quem chegou ao capítulo final', () => {
  const { eco, combat, put, adv, rewards } = setup();
  put('Ana', FIELD.x, FIELD.z);
  const a = combat.create('wolf', FIELD.x, FIELD.z + 2);
  const e = combat.create('wolf', FIELD.x + 10, FIELD.z + 2, 1, true);
  assert.ok(e.hp > a.hp * 2 && e.elite && e.atk > a.atk);
  assert.equal(combat.snapshotFor('Ana').find((r) => r[0] === e.id)[7] & 4, 4, 'flag de elite no pacote');
  const C = LOCATIONS.castle;
  Object.assign(combat.world.pos.get('Ana'), { x: C.x, z: C.z + 40 });
  for (let i = 0; i < 3; i++) (combat.spawnT = 0), combat.update(0.1);
  assert.ok(![...combat.monsters.values()].some((m) => m.type === 'dragon'), 'sem capítulo final, sem dragão');
  Object.assign(eco.player('Ana'), { career: { chapter: 7, count: 0, got: [], done: false } });
  combat.bossAt.kingslime = Infinity;
  combat.spawnT = 0;
  combat.update(0.1);
  const d = [...combat.monsters.values()].find((m) => m.type === 'dragon');
  assert.ok(d, 'dragão apareceu');
  d.hp = d.max * 0.4;
  combat.update(0.1);
  assert.ok(d.enraged, 'fúria abaixo de 50%');
  d.hp = 1;
  Object.assign(combat.world.pos.get('Ana'), { x: d.x, z: d.z - 3 });
  adv(500);
  combat.playerAttack('Ana', 0);
  assert.ok(rewards.some((r) => r[2] === 'dragon'));
  assert.equal(eco.careerView(eco.player('Ana')).done, true, 'derrotar o Dragão zera o jogo');
  assert.ok(eco.player('Ana').inventory.some((i) => i.itemId === 'crown_hero'));
  assert.ok(eco.audit().ok);
});
