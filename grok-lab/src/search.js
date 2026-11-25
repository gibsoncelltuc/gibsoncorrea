// Busca aleatória de parâmetros COM validação fora da amostra (treino 60% / validação 20% / teste cego 20% do tempo).
// Uso: node src/search.js --file data/real-....json --configs 10000 [--noRug] [--maxAge 100000] [--seed 1]
// Pergunta que responde: "o que dá certo no treino continua dando certo depois?" (se não, era sorte, não vantagem).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { CONFIG } from './config.js';
import { Engine } from './engine.js';
import { loadTokens, ReplayMarket } from './market/replay.js';
import { mulberry32 } from './market/sim.js';

const arg = (k, d) => {
  const i = process.argv.indexOf('--' + k);
  return i > 0 ? process.argv[i + 1] : d;
};
const dir = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'data');
const file = arg('file') ?? path.join(dir, fs.readdirSync(dir).filter((f) => /-x\d+\.json$/.test(f)).sort().pop());
const N = Number(arg('configs', 2000));
const seed = Number(arg('seed', 1));
const maxAgeH = Number(arg('maxAge', 100000));
const noRug = process.argv.includes('--noRug');
const MIN_TRADES = Number(arg('minTrades', 40));

const raw = JSON.parse(fs.readFileSync(file, 'utf8'));
const tokens = loadTokens(raw);
// Divisão DENTRO de cada token (primeiros 60% das velas = treino, próximos 20% = validação, últimos 20% = teste cego).
// Cada fatia é re-basada no tempo para que as três partes tenham quantidade parecida de dados.
const T0 = 1_000_000;
function sliceTokens(a, b) {
  const out = [];
  for (const t of tokens) {
    const n = t.all.length;
    const part = t.all.slice(Math.floor(a * n), Math.floor(b * n));
    if (part.length < 60) continue;
    const shift = part[0].t - T0;
    out.push({ ...t, all: part.map((c) => ({ ...c, t: c.t - shift })), born: t.born - shift, cursor: 0, candles: [], _in: false });
  }
  return out;
}
const SLICES = { train: sliceTokens(0, 0.6), val: sliceTokens(0.6, 0.8), test: sliceTokens(0.8, 1) };
const span = Math.max(...Object.values(SLICES).flat().map((t) => t.all.length));

const base = { ...CONFIG, scan: { ...CONFIG.scan, maxAgeMin: maxAgeH * 60 }, rug: { ...CONFIG.rug, disabled: noRug } };

function evaluate(cfg, key) {
  const m = new ReplayMarket(SLICES[key]);
  const e = new Engine(m, cfg);
  while (!m.done) e.tick();
  e.closeAll();
  const r = e.trades.map((t) => t.ret);
  const n = r.length;
  const exp = n ? (r.reduce((a, b) => a + b, 0) / n) * 100 : 0;
  const gw = e.trades.filter((t) => t.pnl > 0).reduce((a, t) => a + t.pnl, 0);
  const gl = -e.trades.filter((t) => t.pnl <= 0).reduce((a, t) => a + t.pnl, 0);
  return { n, exp, pf: gl ? gw / gl : gw ? Infinity : 0, win: n ? (r.filter((x) => x > 0).length / n) * 100 : 0, eq: e.equity(), rets: r };
}

const rng = mulberry32(seed);
const pick = (a) => a[Math.floor(rng() * a.length)];
const space = {
  lookback: [5, 10, 15, 20, 30],
  volSpike: [1.5, 2, 2.5, 3, 4, 6],
  sl: [0.03, 0.05, 0.08, 0.12, 0.16],
  tpR: [1, 1.5, 2, 3, 5],
  arm: [0.06, 0.1, 0.15, 0.25],
  trail: [0.03, 0.05, 0.08, 0.12],
  min5m: [2000, 5000, 15000],
};
const mkCfg = (p) => ({ ...base, stopLossPct: p.sl, tpR: p.tpR, trailArmPct: p.arm, trailPct: p.trail, scan: { ...base.scan, breakoutLookback: p.lookback, volSpike: p.volSpike, min5mVol: p.min5m } });
const label = (p) => `lookback ${p.lookback} · pico de volume ${p.volSpike}x · stop ${p.sl * 100}% · alvo ${p.tpR}R · trailing arma ${p.arm * 100}% recua ${p.trail * 100}% · vol5m≥${p.min5m}`;

const spearman = (xs, ys) => {
  const rank = (a) => {
    const idx = a.map((v, i) => [v, i]).sort((p, q) => p[0] - q[0]);
    const r = new Array(a.length);
    idx.forEach(([, i], k) => (r[i] = k));
    return r;
  };
  const rx = rank(xs);
  const ry = rank(ys);
  const n = xs.length;
  const mx = rx.reduce((a, b) => a + b, 0) / n;
  const my = ry.reduce((a, b) => a + b, 0) / n;
  let c = 0, vx = 0, vy = 0;
  for (let i = 0; i < n; i++) (c += (rx[i] - mx) * (ry[i] - my)), (vx += (rx[i] - mx) ** 2), (vy += (ry[i] - my) ** 2);
  return c / Math.sqrt(vx * vy);
};
const q = (a, p) => a.slice().sort((x, y) => x - y)[Math.min(a.length - 1, Math.floor(p * a.length))];
const fmt = (r) => `${r.n} trades · acerto ${r.win.toFixed(0)}% · expectativa ${r.exp >= 0 ? '+' : ''}${r.exp.toFixed(2)}%/trade · fator de lucro ${r.pf.toFixed(2)}`;

console.log(`BUSCA COM VALIDAÇÃO · ${path.basename(file)} · ${tokens.length} tokens`);
const nc = (k) => SLICES[k].reduce((a, t) => a + t.all.length, 0);
console.log(`velas por período: treino ${nc('train')} · validação ${nc('val')} · teste cego ${nc('test')} · idade máx. ${maxAgeH} h · filtro de segurança ${noRug ? 'DESLIGADO' : 'ligado'}\n`);

const baseline = { lookback: 10, volSpike: 2.5, sl: 0.08, tpR: 3, arm: 0.12, trail: 0.06, min5m: 2000 };
console.log('REGRAS DO VÍDEO (referência):');
for (const k of ['train', 'val', 'test']) console.log(`  ${k.padEnd(5)}: ${fmt(evaluate(mkCfg(baseline), k))}`);

const rows = [];
const t0 = Date.now();
for (let i = 0; i < N; i++) {
  const p = { lookback: pick(space.lookback), volSpike: pick(space.volSpike), sl: pick(space.sl), tpR: pick(space.tpR), arm: pick(space.arm), trail: pick(space.trail), min5m: pick(space.min5m) };
  const cfg = mkCfg(p);
  rows.push({ p, tr: evaluate(cfg, 'train'), va: evaluate(cfg, 'val'), te: evaluate(cfg, 'test') });
  if ((i + 1) % 500 === 0) process.stderr.write(`  ${i + 1}/${N} configs (${((Date.now() - t0) / 1000).toFixed(0)} s)\n`);
}

const ok = rows.filter((r) => r.tr.n >= MIN_TRADES && r.va.n >= 10 && r.te.n >= 10);
console.log(`\n${N} configurações testadas; ${ok.length} com trades suficientes nos 3 períodos (treino ≥${MIN_TRADES}).`);
const pos = (f) => ((ok.filter((r) => f(r) > 0).length / ok.length) * 100).toFixed(0) + '%';
console.log(`expectativa POSITIVA: treino ${pos((r) => r.tr.exp)} · validação ${pos((r) => r.va.exp)} · teste cego ${pos((r) => r.te.exp)}`);
console.log(`expectativa mediana por trade: treino ${q(ok.map((r) => r.tr.exp), 0.5).toFixed(2)}% · validação ${q(ok.map((r) => r.va.exp), 0.5).toFixed(2)}% · teste ${q(ok.map((r) => r.te.exp), 0.5).toFixed(2)}%`);
console.log(`correlação treino×validação: ${spearman(ok.map((r) => r.tr.exp), ok.map((r) => r.va.exp)).toFixed(2)} · treino×teste: ${spearman(ok.map((r) => r.tr.exp), ok.map((r) => r.te.exp)).toFixed(2)}  (≈0 = o que "funcionou" no treino não se repete)`);

const top = ok.slice().sort((a, b) => b.tr.exp - a.tr.exp).slice(0, 20);
console.log('\nTOP 5 DO TREINO (o que a busca "achou") e o que aconteceu DEPOIS:');
for (const r of top.slice(0, 5)) console.log(`  ${label(r.p)}\n     treino ${fmt(r.tr)}\n     valid. ${fmt(r.va)}`);
const trainPos = top.filter((r) => r.tr.exp > 0);
console.log(`\ndos 20 melhores do treino, ${top.filter((r) => r.va.exp > 0).length} continuaram positivos na validação.`);

// seleção honesta: melhor da validação entre os 20 melhores do treino; só então olha o teste cego, UMA vez
const chosen = top.slice().sort((a, b) => b.va.exp - a.va.exp)[0];
console.log('\nCONFIGURAÇÃO ESCOLHIDA (melhor validação entre os 20 melhores do treino):');
console.log('  ' + label(chosen.p));
console.log(`  treino ${fmt(chosen.tr)}\n  valid. ${fmt(chosen.va)}\n  TESTE CEGO: ${fmt(chosen.te)}`);
const r = chosen.te.rets;
if (r.length >= 10) {
  const mean = r.reduce((a, b) => a + b, 0) / r.length;
  const sd = Math.sqrt(r.reduce((a, b) => a + (b - mean) ** 2, 0) / (r.length - 1));
  const se = sd / Math.sqrt(r.length);
  console.log(`  intervalo de 95% da expectativa no teste: ${((mean - 1.96 * se) * 100).toFixed(2)}% a ${((mean + 1.96 * se) * 100).toFixed(2)}% por trade (n=${r.length})`);
}
console.log(`\ntempo: ${((Date.now() - t0) / 1000).toFixed(0)} s`);
console.log('AVISOS: tokens antigos/"em alta" (viés de sobrevivência), RugCheck de hoje aplicado ao passado, sem liquidez histórica, vendas sempre executam.');
