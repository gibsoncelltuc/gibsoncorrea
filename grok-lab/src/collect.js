// Coleta DADOS REAIS (somente leitura) de memecoins da Solana e grava em data/real-<data>.json
// Uso: NODE_USE_ENV_PROXY=1 node src/collect.js --pools 60
//   GeckoTerminal: pools em alta + velas de 1 min (até 1000 por pool, ~16 h)
//   RugCheck: autoridades de mint/freeze, LP travada, carteira do dev, maiores holders
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { getJson } from './net.js';

const arg = (k, d) => {
  const i = process.argv.indexOf('--' + k);
  return i > 0 ? Number(process.argv[i + 1]) : d;
};
const maxPools = arg('pools', 60);
const pages = arg('pages', 5);
const GT = 'https://api.geckoterminal.com/api/v2/networks/solana';
const RC = 'https://api.rugcheck.xyz/v1/tokens';
const SKIP = new Set(['SOL', 'USDC', 'USDT', 'WSOL', 'JUP', 'JITOSOL', 'MSOL', 'BONK', 'WIF']);

const log = (...a) => console.log(new Date().toISOString().slice(11, 19), ...a);

async function discover() {
  const out = new Map();
  for (let p = 1; p <= pages; p++) {
    try {
      const j = await getJson(`${GT}/trending_pools?page=${p}`);
      for (const d of j.data) {
        const a = d.attributes;
        const mint = d.relationships.base_token.data.id.replace('solana_', '');
        const symbol = (a.name || '').split(' / ')[0].trim();
        const fdv = Number(a.fdv_usd);
        const created = Date.parse(a.pool_created_at);
        if (!fdv || fdv < 10_000 || fdv > 100_000_000 || SKIP.has(symbol.toUpperCase())) continue;
        if (Date.now() - created < 30 * 60_000) continue;
        if (!out.has(mint)) out.set(mint, { pool: a.address, mint, symbol, created, fdv, priceNow: Number(a.base_token_price_usd), liqNow: Number(a.reserve_in_usd) });
      }
      log(`trending página ${p}: ${out.size} pools elegíveis até agora`);
    } catch (e) {
      log('falha na descoberta, página', p, String(e.message ?? e));
    }
  }
  return [...out.values()].slice(0, maxPools);
}

function mapRug(r) {
  const known = new Set(Object.keys(r.knownAccounts ?? {}));
  const poolAccts = new Set();
  for (const m of r.markets ?? []) for (const k of ['pubkey', 'liquidityA', 'liquidityB', 'mintLP']) if (m[k]) poolAccts.add(m[k]);
  const holders = (r.topHolders ?? []).filter((h) => !known.has(h.owner) && !known.has(h.address) && !poolAccts.has(h.address) && !poolAccts.has(h.owner));
  const top10 = holders.slice(0, 10).reduce((s, h) => s + (h.pct ?? 0), 0);
  const lp = Math.max(0, ...(r.markets ?? []).map((m) => m.lp?.lockedPct ?? 0));
  const supply = r.token?.supply ?? r.markets?.[0]?.mintAAccount?.supply ?? 0;
  const devPct = supply ? ((r.creatorBalance ?? 0) / supply) * 100 : 0;
  return {
    mintRevoked: r.mintAuthority == null,
    freezeOff: r.freezeAuthority == null,
    lpLocked: lp,
    devPct,
    top10,
    ruggedNow: !!r.rugged, // atenção: informação do FUTURO em relação às velas antigas (viés de olhar adiante)
    scoreNorm: r.score_normalised ?? null,
  };
}

const pools = await discover();
log(`coletando velas e RugCheck de ${pools.length} pools (≈ ${Math.ceil((pools.length * 3.1) / 60)} min)`);
const data = [];
for (const [i, t] of pools.entries()) {
  try {
    const o = await getJson(`${GT}/pools/${t.pool}/ohlcv/minute?aggregate=1&limit=1000`);
    const list = o.data.attributes.ohlcv_list; // [ts, o, h, l, c, v] em ordem decrescente
    if (!list || list.length < 60) {
      log(`${i + 1}/${pools.length} ${t.symbol}: poucas velas (${list?.length ?? 0}), ignorado`);
      continue;
    }
    let rug = null;
    try {
      rug = mapRug(await getJson(`${RC}/${t.mint}/report`));
    } catch (e) {
      log(`  RugCheck falhou para ${t.symbol}: ${String(e.message ?? e)}`);
    }
    data.push({ ...t, candles: list.reverse(), rug });
    log(`${i + 1}/${pools.length} ${t.symbol}: ${list.length} velas, rug=${rug ? 'ok' : 'NÃO'}`);
  } catch (e) {
    log(`${i + 1}/${pools.length} ${t.symbol}: erro ${String(e.message ?? e)}`);
  }
}

const dir = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'data');
fs.mkdirSync(dir, { recursive: true });
const file = path.join(dir, `real-${new Date().toISOString().slice(0, 16).replace(/[:T]/g, '-')}.json`);
fs.writeFileSync(file, JSON.stringify({ collectedAt: new Date().toISOString(), source: 'GeckoTerminal + RugCheck', tokens: data }));
log(`gravado: ${file} (${data.length} tokens)`);
