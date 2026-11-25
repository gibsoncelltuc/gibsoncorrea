// Uso: node src/replay-cli.js [--file data/real-....json] [--resamples 10000] [--bootstrap 10000] [--len 200]
// Roda o MESMO motor sobre velas REAIS coletadas, e depois mede a variação com reamostragens.
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
const file = arg('file') ?? path.join(dir, fs.readdirSync(dir).filter((f) => f.startsWith('real-')).sort().pop());
const resamples = Number(arg('resamples', 10000));
const boots = Number(arg('bootstrap', 10000));
const len = Number(arg('len', 200));
const maxAgeH = Number(arg('maxAge', 72)); // idade máxima do token em horas (72 = regra do vídeo; use 100000 para tokens antigos)
const noRug = process.argv.includes('--noRug'); // desliga o filtro de segurança (só para estudar sinais e saídas)
const CFG = { ...CONFIG, scan: { ...CONFIG.scan, maxAgeMin: maxAgeH * 60 }, rug: { ...CONFIG.rug, disabled: noRug } };

const raw = JSON.parse(fs.readFileSync(file, 'utf8'));
const tokens = loadTokens(raw);

function run(toks, cfg = CFG) {
  const m = new ReplayMarket(toks);
  const e = new Engine(m, cfg);
  while (!m.done) e.tick();
  e.closeAll();
  return e;
}

function stats(e) {
  const s = e.summary();
  const w = e.trades.filter((t) => t.ret > 0);
  const l = e.trades.filter((t) => t.ret <= 0);
  const avg = (a) => (a.length ? (a.reduce((x, t) => x + t.ret, 0) / a.length) * 100 : 0);
  const gw = w.reduce((x, t) => x + t.pnl, 0);
  const gl = -l.reduce((x, t) => x + t.pnl, 0);
  return { ...s, avgWin: avg(w), avgLoss: avg(l), expectancy: avg(e.trades), pf: gl ? gw / gl : Infinity };
}
const fmt = (s) =>
  `capital final $${s.equity.toFixed(2)} (${s.pnlPct >= 0 ? '+' : ''}${s.pnlPct.toFixed(1)}%) · ${s.trades} trades · acerto ${s.winRate.toFixed(0)}% · ganho médio ${s.avgWin.toFixed(1)}% · perda média ${s.avgLoss.toFixed(1)}% · expectativa/trade ${s.expectancy.toFixed(2)}% · fator de lucro ${s.pf.toFixed(2)} · drawdown máx. ${s.maxDD.toFixed(0)}% · taxas $${s.fees.toFixed(2)}`;

const t0 = Math.min(...tokens.map((t) => t.all[0].t));
const t1 = Math.max(...tokens.map((t) => t.all[t.all.length - 1].t));
console.log(`DADOS REAIS · ${path.basename(file)} · coletado em ${raw.collectedAt}`);
console.log(`${tokens.length} tokens com dados do RugCheck · janela de ${((t1 - t0) / 60).toFixed(1)} h · velas de 1 min (GeckoTerminal) · idade máxima do token: ${maxAgeH} h · filtro de segurança: ${noRug ? 'DESLIGADO' : 'ligado'}\n`);

const base = run(tokens);
const bs = stats(base);
console.log('1) Regras do vídeo + custos realistas (taxa 0,5% + derrapagem 1,5% por lado):');
console.log('   ' + fmt(bs));
const free = run(tokens, { ...CFG, feePct: 0, slippagePct: 0 });
console.log('2) Mesmas regras SEM custos (só para ver quanto os custos comem):');
console.log('   ' + fmt(stats(free)));
const harsh = run(tokens, { ...CFG, slippagePct: 0.03 });
console.log('3) Derrapagem de 3% por lado (memecoin de pouca liquidez):');
console.log('   ' + fmt(stats(harsh)));
const reasons = {};
for (const t of base.trades) reasons[t.reason] = (reasons[t.reason] ?? 0) + 1;
console.log('   saídas do cenário 1:', JSON.stringify(reasons));

// ---- reamostragem 1: subconjuntos aleatórios de 70% dos tokens (sorte na escolha dos tokens) ----
console.log(`\n4) ${resamples} execuções, cada uma com 70% dos tokens sorteados:`);
const rng = mulberry32(12345);
const finals = [];
let totalTrades = 0;
for (let i = 0; i < resamples; i++) {
  const sub = tokens.filter(() => rng() < 0.7);
  if (sub.length < 5) continue;
  const e = run(sub);
  finals.push(e.equity());
  totalTrades += e.trades.length;
}
finals.sort((a, b) => a - b);
const q = (arr, p) => arr[Math.min(arr.length - 1, Math.floor(p * arr.length))];
const S = CONFIG.startEquity;
const pct = (arr, f) => ((arr.filter(f).length / arr.length) * 100).toFixed(0) + '%';
console.log(`   ${finals.length} execuções · ${totalTrades} trades simulados no total`);
console.log(`   capital final: p5 $${q(finals, 0.05).toFixed(0)} · mediana $${q(finals, 0.5).toFixed(0)} · p95 $${q(finals, 0.95).toFixed(0)} (início $${S})`);
console.log(`   acima do capital inicial: ${pct(finals, (x) => x > S)} · +100% ou mais: ${pct(finals, (x) => x >= 2 * S)} · -50% ou pior: ${pct(finals, (x) => x <= S / 2)}`);

// ---- reamostragem 2: bootstrap dos retornos por trade do cenário 1 ----
const rets = base.trades.map((t) => t.ret);
console.log(`\n5) ${boots} sequências de ${len} trades sorteados (com reposição) dos retornos reais do cenário 1, 18% do capital por trade:`);
if (rets.length < 10) {
  console.log('   trades insuficientes para reamostrar.');
} else {
  const r2 = mulberry32(777);
  const end = [];
  for (let b = 0; b < boots; b++) {
    let eq = S;
    for (let i = 0; i < len; i++) eq *= 1 + CONFIG.sizePctEquity * rets[Math.floor(r2() * rets.length)];
    end.push(eq);
  }
  end.sort((a, b) => a - b);
  const mean = rets.reduce((a, b) => a + b, 0) / rets.length;
  console.log(`   retorno médio por trade nos dados: ${(mean * 100).toFixed(2)}% (n=${rets.length})`);
  console.log(`   capital após ${len} trades: p5 $${q(end, 0.05).toFixed(0)} · mediana $${q(end, 0.5).toFixed(0)} · p95 $${q(end, 0.95).toFixed(0)}`);
  console.log(`   terminam acima do início: ${pct(end, (x) => x > S)} · -50% ou pior: ${pct(end, (x) => x <= S / 2)} · +100% ou mais: ${pct(end, (x) => x >= 2 * S)}`);
}
console.log('\nAVISOS: (a) os pools vieram da lista "em alta", logo há viés de sobrevivência; (b) o RugCheck é de HOJE, aplicado a velas antigas;');
console.log('(c) o filtro de liquidez fica desligado (não há liquidez histórica); (d) todas as saídas executam (rug real pode travar a venda).');
console.log('Por tudo isso, o resultado costuma ser OTIMISTA em relação ao que aconteceria ao vivo.');
