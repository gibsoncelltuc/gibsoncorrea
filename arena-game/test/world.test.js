import test from 'node:test';
import assert from 'node:assert/strict';
import { Economy, GameError, emptyData } from '../server/economy.js';
import { World } from '../server/world.js';
import { RULES } from '../server/catalog.js';
import { LOCATIONS, ARENA_SPAWNS, CRYSTALS, SPAWN } from '../public/shared/world.js';
import { CHAPTERS } from '../public/shared/quests.js';

function setup() {
  let t = 5_000_000;
  const events = [];
  const eco = new Economy({ data: emptyData() }, { now: () => t, rng: () => 0.5 });
  const world = new World(eco, { now: () => t, emit: (n, m) => events.push([n, m]), touch: () => {}, rng: () => 0.5 });
  return { eco, world, events, adv: (ms) => (t += ms), clock: () => t };
}
const throwsCode = (fn, code) => assert.throws(fn, (e) => e instanceof GameError && e.code === code, `esperava erro ${code}`);
const at = (world, name, x, z) => {
  world.join(name);
  const p = world.position(name);
  Object.assign(p, { x, z });
};

test('carreira: capítulos em ordem, recompensa criada com contabilidade correta e final do jogo', () => {
  const { eco, adv } = setup();
  eco.register('Ana');
  assert.equal(eco.careerView(eco.player('Ana')).quest.id, 1);
  assert.equal(eco.careerEvent('Ana', 'kill', 'slime'), null, 'matar fora de ordem não avança');
  const r1 = eco.careerEvent('Ana', 'talk', 'mayor');
  assert.equal(r1.completed.id, 1);
  assert.equal(eco.careerView(eco.player('Ana')).quest.id, 2);
  assert.equal(eco.careerEvent('Ana', 'talk', 'outro'), null);
  for (const ch of CHAPTERS.slice(1)) {
    if (ch.type === 'kill') for (let i = 0; i < ch.goal; i++) eco.careerEvent('Ana', 'kill', ch.enemy);
    else if (ch.type === 'collect') for (const id of ch.ids) eco.careerEvent('Ana', 'collect', id);
    assert.ok(eco.audit().ok);
    adv(1);
  }
  const v = eco.careerView(eco.player('Ana'));
  assert.equal(v.done, true);
  assert.ok(eco.player('Ana').inventory.some((i) => i.itemId === 'crown_hero'), 'recompensa final');
  assert.equal(eco.careerEvent('Ana', 'kill', 'kingslime'), null, 'depois de zerar nada mais avança');
  assert.ok(eco.audit().ok);
});

test('carreira: cristal repetido não conta duas vezes', () => {
  const { eco } = setup();
  eco.register('Ana');
  eco.careerEvent('Ana', 'talk', 'mayor');
  for (let i = 0; i < 8; i++) eco.careerEvent('Ana', 'kill', 'slime');
  eco.careerEvent('Ana', 'collect', 'cr1');
  assert.equal(eco.careerEvent('Ana', 'collect', 'cr1'), null);
  assert.equal(eco.careerView(eco.player('Ana')).quest.count, 1);
  assert.equal(eco.careerEvent('Ana', 'collect', 'xx'), null);
});

test('aparência: só índices válidos são aceitos', () => {
  const { eco } = setup();
  const p = eco.register('Ana', { skin: 99, hair: 2, hairColor: -1, shirt: 3, pants: 'x', face: 1.5 });
  assert.deepEqual(p.ap, { skin: 1, hair: 2, hairColor: 1, shirt: 3, pants: 0, face: 0 });
});

test('presença: limite de velocidade, teleporte barrado e bordas do mundo', () => {
  const { world, adv } = setup();
  world.join('Ana');
  adv(100);
  assert.ok(world.move('Ana', { x: 1, y: 0, z: SPAWN.z, yaw: 0, a: 1 }).ok);
  adv(100);
  assert.equal(world.move('Ana', { x: 200, y: 0, z: SPAWN.z }).ok, false, 'teleporte');
  adv(1000);
  assert.ok(world.move('Ana', { x: 10, y: 0, z: SPAWN.z }).ok);
  adv(60_000);
  assert.equal(world.move('Ana', { x: 500, y: 0, z: 0 }).ok, false, 'fora do mundo');
  assert.equal(world.move('Ana', { x: NaN, y: 0, z: 0 }).ok, false);
});

test('chat: limite de frequência, tamanho e caracteres de controle', () => {
  const { world, adv } = setup();
  world.join('Ana');
  const m = world.chat('Ana', '  oi\u0007 mundo  ');
  assert.equal(m.text, 'oi mundo');
  throwsCode(() => world.chat('Ana', 'de novo'), 'rapido');
  adv(1000);
  assert.equal(world.chat('Ana', 'x'.repeat(500)).text.length, 120);
  adv(1000);
  throwsCode(() => world.chat('Ana', '   '), 'vazio');
});

test('validações da carreira usam a POSIÇÃO do servidor (bioma, NPC, cristal)', () => {
  const { world } = setup();
  at(world, 'Ana', 0, 20);
  assert.equal(world.canKill('Ana', 'slime'), true);
  assert.equal(world.canKill('Ana', 'scorpion'), false, 'escorpião só no deserto');
  assert.equal(world.canKill('Ana', 'dragao'), false);
  assert.equal(world.near('Ana', 'mayor'), false);
  Object.assign(world.position('Ana'), { x: LOCATIONS.mayor.x, z: LOCATIONS.mayor.z });
  assert.equal(world.near('Ana', 'mayor'), true);
  Object.assign(world.position('Ana'), { x: LOCATIONS.desert.x, z: LOCATIONS.desert.z });
  assert.equal(world.canKill('Ana', 'scorpion'), true);
  Object.assign(world.position('Ana'), { x: CRYSTALS[0].x, z: CRYSTALS[0].z });
  assert.equal(world.nearCrystal('Ana', 'cr1'), true);
  assert.equal(world.nearCrystal('Ana', 'cr2'), false);
});

function duel() {
  const s = setup();
  s.eco.register('Ana');
  s.eco.register('Beto');
  for (const n of ['Ana', 'Beto']) at(s.world, n, LOCATIONS.colosseum.x, LOCATIONS.colosseum.z);
  return s;
}

test('duelo: aposta em custódia, golpe validado, vencedor leva o prêmio e a auditoria fecha', () => {
  const { eco, world, adv, events } = duel();
  world.queueJoin('Ana');
  assert.equal(eco.player('Ana').coins, 100 - RULES.battleFee);
  assert.ok(eco.audit().ok);
  throwsCode(() => world.queueJoin('Ana'), 'fila');
  world.queueJoin('Beto');
  assert.ok(events.some(([, m]) => m.t === 'battle' && m.phase === 'start'));
  const pa = world.position('Ana');
  const pb = world.position('Beto');
  assert.deepEqual([pa.x, pa.z], [ARENA_SPAWNS[0].x, ARENA_SPAWNS[0].z]);
  Object.assign(pb, { x: pa.x + 30, z: pa.z });
  throwsCode(() => world.hit('Ana', 'Beto'), 'longe');
  Object.assign(pb, { x: pa.x + 2, z: pa.z });
  const dmg = world.hit('Ana', 'Beto');
  assert.ok(dmg >= 1);
  throwsCode(() => world.hit('Ana', 'Beto'), 'rapido');
  throwsCode(() => world.hit('Ana', 'Ana'), 'alvo');
  let n = 0;
  while (world.inMatch.has('Ana') && n++ < 200) {
    adv(RULES.battleCooldownMs + 1);
    world.hit('Ana', 'Beto');
    assert.ok(eco.audit().ok);
  }
  assert.ok(!world.inMatch.has('Ana') && !world.inMatch.has('Beto'));
  const prize = 20 - Math.floor(20 * RULES.battleRakePct);
  assert.equal(eco.player('Ana').coins, 100 - RULES.battleFee + prize);
  assert.equal(eco.player('Beto').coins, 100 - RULES.battleFee);
  assert.equal(eco.d.stats.escrowBattle, 0);
  assert.deepEqual(eco.d.battleLocks, {});
  assert.ok(eco.audit().ok, JSON.stringify(eco.audit()));
  assert.deepEqual([world.position('Ana').x, world.position('Ana').z], [SPAWN.x, SPAWN.z]);
});

test('duelo: fila cancelada devolve a aposta; abandono dá a vitória; tempo esgotado decide por vida', () => {
  const { eco, world, adv } = duel();
  world.queueJoin('Ana');
  assert.equal(world.cancelQueue('Ana'), true);
  assert.equal(eco.player('Ana').coins, 100);
  assert.equal(eco.d.stats.escrowBattle, 0);
  throwsCode(() => world.queueJoin('Ana') || world.hit('Ana', 'Beto'), 'batalha');
  world.cancelQueue('Ana');
  // abandono
  world.queueJoin('Ana');
  world.queueJoin('Beto');
  world.leave('Beto');
  assert.equal(eco.player('Ana').coins, 100 - 10 + 18);
  assert.ok(eco.audit().ok);
  // tempo esgotado: quem tem mais vida vence
  world.join('Beto');
  Object.assign(world.position('Beto'), { x: LOCATIONS.colosseum.x, z: LOCATIONS.colosseum.z });
  Object.assign(world.position('Ana'), { x: LOCATIONS.colosseum.x, z: LOCATIONS.colosseum.z });
  world.queueJoin('Ana');
  world.queueJoin('Beto');
  const pa = world.position('Ana');
  Object.assign(world.position('Beto'), { x: pa.x + 2, z: pa.z });
  world.hit('Ana', 'Beto');
  adv(RULES.battleSeconds * 1000 + 1);
  world.tick();
  assert.ok(!world.inMatch.has('Ana'));
  assert.ok(eco.audit().ok, JSON.stringify(eco.audit()));
  // empate: devolve as apostas
  const before = eco.player('Ana').coins + eco.player('Beto').coins;
  world.join('Ana');
  Object.assign(world.position('Ana'), { x: LOCATIONS.colosseum.x, z: LOCATIONS.colosseum.z });
  Object.assign(world.position('Beto'), { x: LOCATIONS.colosseum.x, z: LOCATIONS.colosseum.z });
  world.queueJoin('Ana');
  world.queueJoin('Beto');
  adv(RULES.battleSeconds * 1000 + 1);
  world.tick();
  assert.equal(eco.player('Ana').coins + eco.player('Beto').coins, before, 'empate não cria nem destrói moedas');
  assert.ok(eco.audit().ok);
});

test('duelo: só entra na fila perto do Coliseu e com moedas', () => {
  const { eco, world } = setup();
  eco.register('Ana');
  world.join('Ana');
  throwsCode(() => world.queueJoin('Ana'), 'longe');
  Object.assign(world.position('Ana'), { x: LOCATIONS.colosseum.x, z: LOCATIONS.colosseum.z });
  eco.player('Ana').coins = 5;
  eco.d.stats.minted = 5;
  throwsCode(() => world.queueJoin('Ana'), 'moedas');
});
