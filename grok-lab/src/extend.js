// Estende o histórico de velas de 1 min de um arquivo coletado, buscando páginas mais antigas.
// Uso: NODE_USE_ENV_PROXY=1 node src/extend.js --candles 6000 [--file data/real-....json]
// Grava um arquivo novo: data/<nome>-x<candles>.json (o original fica intacto). Pode ser interrompido
// e reexecutado com --file apontando para o arquivo -x..., que ele continua de onde parou.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { getJson } from './net.js';

const arg = (k, d) => {
  const i = process.argv.indexOf('--' + k);
  return i > 0 ? process.argv[i + 1] : d;
};
const target = Number(arg('candles', 6000));
const dir = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'data');
const src = arg('file') ?? path.join(dir, fs.readdirSync(dir).filter((f) => /^real-[\d-]+\.json$/.test(f)).sort().pop());
const out = src.includes('-x') ? src : src.replace(/\.json$/, `-x${target}.json`);
const GT = 'https://api.geckoterminal.com/api/v2/networks/solana';
const log = (...a) => console.log(new Date().toISOString().slice(11, 19), ...a);

const raw = JSON.parse(fs.readFileSync(src, 'utf8'));
for (const [i, t] of raw.tokens.entries()) {
  if (t.extended) continue;
  try {
    let guard = 0;
    while (t.candles.length < target && guard++ < 10) {
      const oldest = t.candles[0][0];
      const j = await getJson(`${GT}/pools/${t.pool}/ohlcv/minute?aggregate=1&limit=1000&before_timestamp=${oldest}`);
      const older = (j.data.attributes.ohlcv_list ?? []).filter((c) => c[0] < oldest).reverse();
      if (!older.length) break; // chegou ao início da vida do pool
      t.candles = older.concat(t.candles);
    }
    t.extended = true;
    log(`${i + 1}/${raw.tokens.length} ${t.symbol}: ${t.candles.length} velas (${(t.candles.length / 60 / 24).toFixed(1)} dias)`);
  } catch (e) {
    log(`${i + 1}/${raw.tokens.length} ${t.symbol}: erro ${String(e.message ?? e)}`);
  }
  if (i % 5 === 4) fs.writeFileSync(out, JSON.stringify(raw)); // checkpoint
}
fs.writeFileSync(out, JSON.stringify(raw));
const n = raw.tokens.map((t) => t.candles.length).sort((a, b) => a - b);
log(`gravado: ${out} · velas por token: mín ${n[0]} · mediana ${n[Math.floor(n.length / 2)]} · máx ${n[n.length - 1]}`);
