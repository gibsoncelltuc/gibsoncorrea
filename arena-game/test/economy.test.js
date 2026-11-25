import test from 'node:test';
import assert from 'node:assert/strict';
import { Economy, GameError, emptyData } from '../server/economy.js';
import { RULES, SKILLS } from '../server/catalog.js';

function setup() {
  let t = 1_000_000;
  const eco = new Economy({ data: emptyData() }, { now: () => t, rng: () => 0.5 });
  return { eco, adv: (ms) => (t += ms), clock: () => t };
}
const throwsCode = (fn, code) => assert.throws(fn, (e) => e instanceof GameError && e.code === code, `esperava erro ${code}`);
const rich = (eco, name, coins) => {
  const p = eco.player(name);
  p.coins += coins;
  eco.d.stats.minted += coins; // dinheiro de teste entra na contabilidade
};

test('registro: nome válido, único, moedas iniciais e espada equipada', () => {
  const { eco } = setup();
  const p = eco.register('Ana_01');
  assert.equal(p.coins, RULES.startCoins);
  assert.ok(p.equipped.weapon);
  throwsCode(() => eco.register('ana_01'), 'existe');
  throwsCode(() => eco.register('a'), 'nome');
  throwsCode(() => eco.register('nome com espaço'), 'nome');
  assert.ok(eco.audit().ok);
});

test('loja: compra destrói moedas, bloqueia saldo insuficiente e a auditoria fecha', () => {
  const { eco } = setup();
  eco.register('Ana');
  eco.buyItem('Ana', 'hat_cloth');
  assert.equal(eco.player('Ana').coins, RULES.startCoins - 25);
  throwsCode(() => eco.buyItem('Ana', 'crown_gold'), 'moedas');
  throwsCode(() => eco.buyItem('Ana', 'nao_existe'), 'item');
  assert.ok(eco.audit().ok);
});

test('equipar muda os atributos; pergaminho ensina habilidade uma vez; evolução custa moedas', () => {
  const { eco } = setup();
  eco.register('Ana');
  rich(eco, 'Ana', 1000);
  const base = eco.stats(eco.player('Ana'));
  const iid = eco.buyItem('Ana', 'sword_iron');
  eco.equip('Ana', iid);
  assert.equal(eco.stats(eco.player('Ana')).atk, base.atk - 3 + 8);
  const sc = eco.buyItem('Ana', 'scroll_fireball');
  assert.equal(eco.useScroll('Ana', sc), 'fireball');
  assert.equal(eco.player('Ana').skills.fireball, 1);
  const sc2 = eco.buyItem('Ana', 'scroll_fireball');
  throwsCode(() => eco.useScroll('Ana', sc2), 'ja');
  const before = eco.player('Ana').coins;
  assert.equal(eco.upgradeSkill('Ana', 'fireball'), 2);
  assert.equal(eco.player('Ana').coins, before - SKILLS.fireball.upgradeBase);
  assert.equal(eco.upgradeSkill('Ana', 'fireball'), 3);
  throwsCode(() => eco.upgradeSkill('Ana', 'fireball'), 'max');
  throwsCode(() => eco.upgradeSkill('Ana', 'dash'), 'skill');
  assert.ok(eco.audit().ok);
});

test('recompensa por inimigo: intervalo mínimo, teto por hora e subida de nível', () => {
  const { eco, adv } = setup();
  eco.register('Ana');
  const r1 = eco.claimKill('Ana', 'slime');
  assert.ok(r1.coins >= 3 && r1.coins <= 8);
  throwsCode(() => eco.claimKill('Ana', 'slime'), 'rapido');
  let total = r1.coins;
  for (let i = 0; i < 400; i++) {
    adv(RULES.minClaimGapMs + 1);
    total += eco.claimKill('Ana', 'brute').coins;
  }
  assert.ok(total <= RULES.maxCoinsPerHour, `teto por hora violado: ${total}`);
  assert.ok(eco.level(eco.player('Ana')) > 1);
  adv(3_700_000);
  assert.ok(eco.claimKill('Ana', 'brute').coins > 0, 'o teto deve resetar depois de 1 hora');
  throwsCode(() => eco.claimKill('Ana', 'dragao'), 'inimigo');
  assert.ok(eco.audit().ok);
});

test('mercado: custódia, taxa queimada, cancelar devolve, não compra o próprio, não vende equipado', () => {
  const { eco } = setup();
  eco.register('Ana');
  eco.register('Beto');
  rich(eco, 'Ana', 500);
  rich(eco, 'Beto', 500);
  const iid = eco.buyItem('Ana', 'armor_iron');
  eco.equip('Ana', iid);
  throwsCode(() => eco.listItem('Ana', iid, 100), 'equipado');
  eco.unequip('Ana', 'body');
  const l = eco.listItem('Ana', iid, 200);
  assert.ok(!eco.player('Ana').inventory.some((i) => i.iid === iid), 'item em custódia sai do inventário');
  throwsCode(() => eco.buyListing('Ana', l.id), 'proprio');
  const aBefore = eco.player('Ana').coins;
  const bBefore = eco.player('Beto').coins;
  const res = eco.buyListing('Beto', l.id);
  assert.equal(res.fee, 10);
  assert.equal(eco.player('Ana').coins, aBefore + 190);
  assert.equal(eco.player('Beto').coins, bBefore - 200);
  assert.ok(eco.player('Beto').inventory.some((i) => i.iid === iid));
  throwsCode(() => eco.buyListing('Beto', l.id), 'anuncio'); // segunda compra do mesmo anúncio falha
  const iid2 = eco.buyItem('Beto', 'helm_iron');
  const l2 = eco.listItem('Beto', iid2, 50);
  eco.cancelListing('Beto', l2.id);
  assert.ok(eco.player('Beto').inventory.some((i) => i.iid === iid2));
  throwsCode(() => eco.listItem('Beto', iid2, 0), 'valor');
  throwsCode(() => eco.listItem('Beto', iid2, 1.5), 'valor');
  assert.ok(eco.audit().ok);
});

test('troca direta: itens e moedas trocam atomicamente; validações e expiração', () => {
  const { eco, adv } = setup();
  eco.register('Ana');
  eco.register('Beto');
  rich(eco, 'Ana', 500);
  rich(eco, 'Beto', 500);
  const a1 = eco.buyItem('Ana', 'scroll_dash');
  const b1 = eco.buyItem('Beto', 'lantern');
  const t = eco.proposeTrade('Ana', 'Beto', { giveItems: [a1], giveCoins: 10, wantItems: [b1] });
  throwsCode(() => eco.respondTrade('Ana', t.id, true), 'dono');
  const totalBefore = eco.player('Ana').coins + eco.player('Beto').coins;
  eco.respondTrade('Beto', t.id, true);
  assert.ok(eco.player('Beto').inventory.some((i) => i.iid === a1));
  assert.ok(eco.player('Ana').inventory.some((i) => i.iid === b1));
  assert.equal(eco.player('Ana').coins + eco.player('Beto').coins, totalBefore, 'troca não cria nem destrói moedas');
  // item vendido antes de aceitar: a troca falha
  const a2 = eco.buyItem('Ana', 'helm_iron');
  const t2 = eco.proposeTrade('Ana', 'Beto', { giveItems: [a2], wantCoins: 5 });
  eco.listItem('Ana', a2, 99);
  throwsCode(() => eco.respondTrade('Beto', t2.id, true), 'item');
  // expiração e recusa
  const a3 = eco.buyItem('Ana', 'tunic_green');
  const t3 = eco.proposeTrade('Ana', 'Beto', { giveItems: [a3], wantCoins: 1 });
  adv(RULES.tradeTtlMs + 1);
  throwsCode(() => eco.respondTrade('Beto', t3.id, true), 'expirou');
  const t4 = eco.proposeTrade('Ana', 'Beto', { giveCoins: 5 });
  assert.equal(eco.respondTrade('Beto', t4.id, false).status, 'declined');
  throwsCode(() => eco.proposeTrade('Ana', 'Ana', { giveCoins: 1 }), 'proprio');
  throwsCode(() => eco.proposeTrade('Ana', 'Beto', {}), 'vazio');
  throwsCode(() => eco.proposeTrade('Ana', 'Beto', { giveCoins: 99999 }), 'moedas');
  assert.ok(eco.audit().ok);
});

test('torneio: inscrição em custódia, bots subsidiados, prêmio e auditoria fecham', () => {
  const { eco } = setup();
  eco.register('Ana');
  eco.register('Beto');
  const t = eco.createTournament('Ana', { entryFee: 20, size: 4 });
  assert.equal(eco.player('Ana').coins, RULES.startCoins - 20);
  assert.ok(eco.audit().ok && eco.audit().escrow === 20);
  eco.joinTournament('Beto', t.id);
  throwsCode(() => eco.joinTournament('Beto', t.id), 'ja');
  eco.leaveTournament('Beto', t.id);
  assert.equal(eco.player('Beto').coins, RULES.startCoins);
  eco.joinTournament('Beto', t.id);
  throwsCode(() => eco.startTournament('Beto', t.id), 'dono');
  const done = eco.startTournament('Ana', t.id);
  assert.equal(done.status, 'done');
  assert.equal(done.players.length, 4);
  assert.equal(done.rounds.length, 2);
  assert.equal(done.pool, 80);
  assert.equal(done.prize, 72);
  assert.ok(done.winner);
  assert.ok(eco.audit().ok, JSON.stringify(eco.audit()));
  throwsCode(() => eco.joinTournament('Beto', t.id), 'fechado');
});

test('torneio é determinístico para o mesmo estado e o vencedor humano recebe o prêmio', () => {
  const run = () => {
    const { eco } = setup();
    eco.register('Ana');
    const t = eco.createTournament('Ana', { entryFee: 10, size: 4 });
    return { t: eco.startTournament('Ana', t.id), eco };
  };
  const r1 = run();
  const r2 = run();
  assert.equal(r1.t.winner, r2.t.winner);
  if (r1.t.winner === 'Ana') assert.equal(r1.eco.player('Ana').coins, RULES.startCoins - 10 + r1.t.prize);
});

test('auditoria continua fechando depois de uma sequência longa de operações misturadas', () => {
  const { eco, adv } = setup();
  const names = ['A1x', 'B2x', 'C3x', 'D4x'];
  names.forEach((n) => {
    eco.register(n);
    rich(eco, n, 5000); // saldo para as operações realmente acontecerem (sem isso o teste passa sem cobrir nada)
  });
  let seed = 1;
  const rnd = () => ((seed = (seed * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff);
  const ok = {};
  const hit = (k) => (ok[k] = (ok[k] ?? 0) + 1);
  for (let i = 0; i < 1500; i++) {
    const n = names[Math.floor(rnd() * 4)];
    const m = names[Math.floor(rnd() * 4)];
    adv(500);
    try {
      const r = rnd();
      if (r < 0.2) {
        eco.claimKill(n, rnd() < 0.5 ? 'slime' : 'brute');
        hit('kill');
      } else if (r < 0.35) {
        eco.buyItem(n, ['lantern', 'sword_iron', 'scroll_dash', 'hat_cloth', 'tunic_green'][Math.floor(rnd() * 5)]);
        hit('buy');
      } else if (r < 0.5) {
        const inv = eco.player(n).inventory.filter((x) => !Object.values(eco.player(n).equipped).includes(x.iid));
        const it = inv[Math.floor(rnd() * inv.length)];
        if (it) {
          eco.listItem(n, it.iid, 1 + Math.floor(rnd() * 80));
          hit('list');
        }
      } else if (r < 0.65) {
        const ls = eco.market();
        const l = ls[Math.floor(rnd() * ls.length)];
        if (l) {
          eco.buyListing(n, l.id);
          hit('buyListing');
        }
      } else if (r < 0.77) {
        const it = eco.player(n).inventory.find((x) => !Object.values(eco.player(n).equipped).includes(x.iid));
        if (it && n !== m) {
          eco.proposeTrade(n, m, { giveItems: [it.iid], wantCoins: Math.floor(rnd() * 20) });
          hit('propose');
        }
      } else if (r < 0.9) {
        const t = eco.tradesFor(m).find((x) => x.to === m);
        if (t) {
          const acc = rnd() < 0.7;
          const res = eco.respondTrade(m, t.id, acc);
          hit(res.status);
        }
      } else {
        const t = eco.createTournament(n, { entryFee: Math.floor(rnd() * 15), size: 4 });
        hit('torneio');
        if (rnd() < 0.7) eco.startTournament(n, t.id);
      }
    } catch (e) {
      if (!(e instanceof GameError)) throw e; // erros de regra são esperados; qualquer outro é bug
    }
    assert.ok(eco.audit().ok, `auditoria falhou na iteração ${i}: ${JSON.stringify(eco.audit())}`);
  }
  // garante que o teste exercitou de verdade cada parte da economia
  assert.ok(ok.kill > 50 && ok.buy > 50 && ok.list > 30 && ok.buyListing > 30, JSON.stringify(ok));
  assert.ok(ok.propose > 20 && ok.done > 5 && ok.declined > 2 && ok.torneio > 20, JSON.stringify(ok));
});
