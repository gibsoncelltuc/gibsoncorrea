import test from 'node:test';
import assert from 'node:assert/strict';
import { Engine } from '../src/engine.js';
import { SimMarket } from '../src/market/sim.js';
import { CONFIG } from '../src/config.js';

function stub() {
  const tok = { id: 1, symbol: 'TEST', born: -999, candles: [{ t: 0, o: 100, h: 100, l: 100, c: 100, v: 1 }] };
  const m = { tick: 0, tokens: [tok], step() {}, liquidity: () => 1e9 };
  return { tok, m, eng: new Engine(m) };
}
const push = (tok, m, o, h, l, c) => {
  m.tick++;
  tok.candles.push({ t: m.tick, o, h, l, c, v: 1 });
};
const entryPx = 100 * (1 + CONFIG.slippagePct);

test('stop loss: executa no stop com derrapagem e taxa, e a conta fecha', () => {
  const { tok, m, eng } = stub();
  const pos = eng.enter(tok, 10);
  push(tok, m, 100, 101, 85, 86);
  eng.manage(pos);
  assert.equal(eng.positions.length, 0);
  const sl = entryPx * (1 - CONFIG.stopLossPct);
  const units = (10 * (1 - CONFIG.feePct)) / entryPx;
  const expected = units * sl * (1 - CONFIG.slippagePct) * (1 - CONFIG.feePct) - 10;
  assert.ok(Math.abs(eng.trades[0].pnl - expected) < 1e-9);
  assert.ok(eng.trades[0].pnl < 0);
  assert.ok(Math.abs(eng.cash - (CONFIG.startEquity - 10 + 10 + expected)) < 1e-9);
});

test('gap abaixo do stop: sai na abertura, pior que o stop', () => {
  const { tok, m, eng } = stub();
  const pos = eng.enter(tok, 10);
  push(tok, m, 70, 72, 60, 65);
  eng.manage(pos);
  const stopPnl = (10 * (1 - CONFIG.feePct)) / entryPx * entryPx * (1 - CONFIG.stopLossPct) * (1 - CONFIG.slippagePct) * (1 - CONFIG.feePct) - 10;
  assert.ok(eng.trades[0].pnl < stopPnl);
});

test('trailing: arma após +12% e sai quando recua 6% do pico', () => {
  const { tok, m, eng } = stub();
  const pos = eng.enter(tok, 10);
  push(tok, m, 101.5, 115, 110, 114);
  eng.manage(pos);
  assert.equal(eng.positions.length, 1);
  assert.equal(pos.trail, true);
  push(tok, m, 114, 114, 105, 106);
  eng.manage(pos);
  assert.equal(eng.positions.length, 0);
  assert.equal(eng.trades[0].reason, 'Trailing');
});

test('take profit em 3R', () => {
  const { tok, m, eng } = stub();
  const pos = eng.enter(tok, 10);
  push(tok, m, 101.5, 130, 101, 129);
  eng.manage(pos);
  assert.equal(eng.trades[0].reason, 'Take profit');
  assert.ok(eng.trades[0].pnl > 0);
});

test('determinístico: mesma semente, mesmo resultado', () => {
  const run = () => {
    const e = new Engine(new SimMarket(7));
    for (let i = 0; i < 600; i++) e.tick();
    e.closeAll();
    return e.summary();
  };
  assert.deepEqual(run(), run());
});

test('sem posições abertas: capital = inicial + soma dos PnL', () => {
  const e = new Engine(new SimMarket(3));
  for (let i = 0; i < 1000; i++) e.tick();
  e.closeAll();
  const sum = e.trades.reduce((a, t) => a + t.pnl, 0);
  assert.ok(Math.abs(e.equity() - (CONFIG.startEquity + sum)) < 1e-6);
  assert.ok(e.cash >= 0);
});

test('nunca arrisca mais caixa do que tem e respeita o máximo de posições', () => {
  const e = new Engine(new SimMarket(5));
  for (let i = 0; i < 1500; i++) {
    e.tick();
    assert.ok(e.cash >= -1e-9);
    assert.ok(e.positions.length <= CONFIG.maxPositions);
  }
});
