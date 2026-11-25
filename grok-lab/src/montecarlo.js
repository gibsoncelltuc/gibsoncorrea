// Uso: node src/montecarlo.js --runs 300 --ticks 1440
// Roda o MESMO motor em muitos mercados sintéticos diferentes e mostra a distribuição dos resultados.
import { SimMarket } from './market/sim.js';
import { Engine } from './engine.js';
import { CONFIG } from './config.js';

const arg = (k, d) => {
  const i = process.argv.indexOf('--' + k);
  return i > 0 ? Number(process.argv[i + 1]) : d;
};
const runs = arg('runs', 300);
const ticks = arg('ticks', 1440);

const finals = [];
const wr = [];
const dd = [];
let nTrades = 0;
for (let seed = 1; seed <= runs; seed++) {
  const eng = new Engine(new SimMarket(seed));
  for (let i = 0; i < ticks; i++) eng.tick();
  eng.closeAll();
  const s = eng.summary();
  finals.push(s.equity);
  dd.push(s.maxDD);
  if (s.trades) wr.push(s.winRate);
  nTrades += s.trades;
}
finals.sort((a, b) => a - b);
const q = (p) => finals[Math.min(finals.length - 1, Math.floor(p * finals.length))];
const start = CONFIG.startEquity;
const pct = (f) => ((finals.filter(f).length / finals.length) * 100).toFixed(0) + '%';
const avg = (a) => a.reduce((x, y) => x + y, 0) / (a.length || 1);

console.log(`MONTE CARLO em mercado SINTÉTICO · ${runs} execuções × ${(ticks / 60).toFixed(0)} h · capital inicial $${start}`);
console.log(`trades por execução (média): ${(nTrades / runs).toFixed(1)}   acerto médio: ${avg(wr).toFixed(0)}%   drawdown máx. médio: ${avg(dd).toFixed(0)}%`);
console.log(`capital final  p5 $${q(0.05).toFixed(0)} · p25 $${q(0.25).toFixed(0)} · mediana $${q(0.5).toFixed(0)} · p75 $${q(0.75).toFixed(0)} · p95 $${q(0.95).toFixed(0)} · máx $${finals[finals.length - 1].toFixed(0)}`);
console.log(`terminaram acima do capital inicial : ${pct((x) => x > start)}`);
console.log(`terminaram com +100% ou mais         : ${pct((x) => x >= start * 2)}`);
console.log(`terminaram com -50% ou pior          : ${pct((x) => x <= start * 0.5)}`);
