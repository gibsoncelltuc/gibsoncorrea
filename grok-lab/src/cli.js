// Uso: node src/cli.js --ticks 1440 --seed 1   (1 tick = 1 minuto simulado)
import { SimMarket } from './market/sim.js';
import { Engine } from './engine.js';

const arg = (k, d) => {
  const i = process.argv.indexOf('--' + k);
  return i > 0 ? Number(process.argv[i + 1]) : d;
};
const ticks = arg('ticks', 1440);
const seed = arg('seed', 1);

const eng = new Engine(new SimMarket(seed));
for (let i = 0; i < ticks; i++) eng.tick();
eng.closeAll();
const s = eng.summary();
console.log(`SIMULAÇÃO (dados sintéticos) · seed ${seed} · ${ticks} min (${(ticks / 60).toFixed(1)} h)`);
console.log(`capital final : $${s.equity.toFixed(2)} (início $${eng.cfg.startEquity})  PnL ${s.pnl >= 0 ? '+' : ''}${s.pnl.toFixed(2)} (${s.pnlPct.toFixed(1)}%)`);
console.log(`trades        : ${s.trades} (${s.wins}G · ${s.losses}P)  acerto ${s.winRate.toFixed(0)}%`);
console.log(`drawdown máx. : ${s.maxDD.toFixed(1)}%   taxas pagas: $${s.fees.toFixed(2)}`);
