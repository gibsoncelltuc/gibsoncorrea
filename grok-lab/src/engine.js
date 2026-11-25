// Motor de trading em modo SIMULADO. Pipeline (como no vídeo):
// Scanner -> Rug Check -> Sizer -> Executor -> Stop Guard / Take Profit -> Logger -> Equity.
// Nenhuma ordem real é enviada: tudo é simulado com custos (taxa + derrapagem).
import { CONFIG } from './config.js';

export function clock(minutes) {
  const hh = String(Math.floor(minutes / 60)).padStart(2, '0');
  const mm = String(minutes % 60).padStart(2, '0');
  return `${hh}:${mm}:00`;
}

const money = (x) => (x >= 0 ? '+' : '-') + '$' + Math.abs(x).toFixed(2);
const compact = (v) => (v >= 1e6 ? '$' + (v / 1e6).toFixed(2) + 'M' : v >= 1e3 ? '$' + (v / 1e3).toFixed(1) + 'K' : '$' + v.toFixed(0));

export class Engine {
  constructor(market, cfg = CONFIG) {
    this.m = market;
    this.cfg = cfg;
    this.t0 = market.tick;
    this.cash = cfg.startEquity;
    this.positions = [];
    this.trades = [];
    this.events = [];
    this.line = 0;
    this.fees = 0;
    this.cool = new Map();
    this.curve = [{ t: 0, e: cfg.startEquity }];
    this.peak = cfg.startEquity;
    this.maxDD = 0;
    this.lastCandidate = null;
    this.ag = {
      grok: 'aguardando',
      scanner: '—',
      rug: '—',
      sizer: '—',
      exec: 'flat',
      stop: `SL -${cfg.stopLossPct * 100}% · 0 armed`,
      tp: '—',
      logger: 'line #0',
    };
  }

  now() {
    return this.m.tick - this.t0;
  }

  lastClose(tok) {
    return tok.candles[tok.candles.length - 1].c;
  }

  equity() {
    let e = this.cash;
    for (const p of this.positions) e += p.units * this.lastClose(p.tok);
    return e;
  }

  log(type, sym, usd, pnl, note) {
    this.line++;
    this.ag.logger = `line #${this.line}`;
    this.events.push({ n: this.line, t: clock(this.now()), type, sym, usd, pnl, note });
    if (this.events.length > 300) this.events.shift();
  }

  // ---- Scanner: rompimento da máxima + pico de volume, sobre velas FECHADAS ----
  scan(T) {
    const s = this.cfg.scan;
    const out = [];
    for (const tok of this.m.tokens) {
      const cs = tok.candles;
      const n = cs.length;
      if (n < Math.max(24, s.breakoutLookback + 23)) continue;
      if ((this.cool.get(tok.id) ?? -1) > T) continue;
      if (this.positions.some((p) => p.tok === tok)) continue;
      const age = T - tok.born;
      if (age < s.minAgeMin || age > s.maxAgeMin) continue;
      const last = cs[n - 2];
      if (last.c < s.minMc || last.c > s.maxMc) continue;
      let hh = 0;
      for (let i = n - 2 - s.breakoutLookback; i < n - 2; i++) hh = Math.max(hh, cs[i].h);
      if (last.c <= hh) continue;
      let av = 0;
      let active = 0;
      for (let i = n - 22; i < n - 2; i++) {
        av += cs[i].v;
        if (cs[i].v > 0) active++;
      }
      av /= 20;
      if (active < 10) continue; // exige negociação contínua: velas vazias (preenchimento de buracos) geram falsos rompimentos
      if (last.v < s.volSpike * av) continue;
      let v5 = 0;
      for (let i = n - 6; i < n - 1; i++) v5 += cs[i].v;
      out.push({ tok, vol5: v5 });
    }
    return out;
  }

  // ---- Rug Check ----
  rugCheck(tok) {
    const r = this.cfg.rug;
    if (r.disabled) return { pass: true, reason: 'filtro desligado' };
    if (tok.cloneOf) return { pass: false, reason: `clone of $${tok.cloneOf}` };
    if (!tok.mintRevoked) return { pass: false, reason: 'mint authority on' };
    if (!tok.freezeOff) return { pass: false, reason: 'freeze authority on' };
    if (tok.lpLocked < r.minLpLockedPct) return { pass: false, reason: `LP locked ${tok.lpLocked.toFixed(0)}%` };
    if (tok.devPct > r.maxDevPct) return { pass: false, reason: `dev wallet ${tok.devPct.toFixed(1)}%` };
    if (tok.top10 > r.maxTop10Pct) return { pass: false, reason: `top10 ${tok.top10.toFixed(0)}%` };
    const liq = this.m.liquidity(tok);
    if (liq < this.cfg.scan.minLiq) return { pass: false, reason: `liq ${compact(liq)}` };
    return { pass: true, reason: 'ok' };
  }

  // ---- Sizer ----
  size() {
    return Math.min(this.cash, this.equity() * this.cfg.sizePctEquity);
  }

  // ---- Executor ----
  enter(tok, size) {
    const c = tok.candles[tok.candles.length - 1];
    const px = c.o * (1 + this.cfg.slippagePct);
    const fee = size * this.cfg.feePct;
    const units = (size - fee) / px;
    this.cash -= size;
    this.fees += fee;
    const pos = {
      tok,
      sym: tok.symbol,
      entry: px,
      units,
      size,
      sl: px * (1 - this.cfg.stopLossPct),
      tp: px * (1 + this.cfg.tpR * this.cfg.stopLossPct),
      peak: px,
      trail: false,
      entryT: c.t,
    };
    this.positions.push(pos);
    this.ag.exec = `LONG $${tok.symbol}`;
    this.ag.grok = `long $${tok.symbol}`;
    this.log('Buy', tok.symbol, size, null, `entry ${compact(px)}`);
    return pos;
  }

  exit(pos, level, reason, note) {
    const px = level * (1 - this.cfg.slippagePct);
    const gross = pos.units * px;
    const fee = gross * this.cfg.feePct;
    const proceeds = gross - fee;
    this.fees += fee;
    this.cash += proceeds;
    const pnl = proceeds - pos.size;
    this.trades.push({ sym: pos.sym, pnl, ret: pnl / pos.size, reason });
    this.positions = this.positions.filter((p) => p !== pos);
    this.cool.set(pos.tok.id, this.m.tick + this.cfg.cooldownMin);
    const isStop = reason === 'Stop loss';
    this.log(isStop ? 'Stop loss' : 'Sell', pos.sym, pos.size, pnl, note ?? reason);
    this.ag.exec = `closed $${pos.sym}`;
    this.ag.grok = isStop ? `stopped $${pos.sym} ${money(pnl)}` : `closed $${pos.sym} ${money(pnl)}`;
    if (isStop) this.ag.stop = `STOP $${pos.sym} ${money(pnl)}`;
    else this.ag.tp = `TP $${pos.sym} ${money(pnl)}`;
  }

  // ---- Stop Guard / Take Profit: ordem intra-vela conservadora (mínima antes da máxima) ----
  manage(pos) {
    const c = pos.tok.candles[pos.tok.candles.length - 1];
    const trailLevel = pos.trail ? pos.peak * (1 - this.cfg.trailPct) : 0;
    const stopLevel = Math.max(pos.sl, trailLevel);
    const isTrail = pos.trail && trailLevel > pos.sl;
    if (c.o <= stopLevel) return this.exit(pos, c.o, isTrail ? 'Trailing' : 'Stop loss', isTrail ? 'trailing (gap)' : 'stop (gap)');
    if (c.l <= stopLevel) return this.exit(pos, stopLevel, isTrail ? 'Trailing' : 'Stop loss', isTrail ? 'trailing' : 'stop -8%');
    pos.peak = Math.max(pos.peak, c.h);
    if (!pos.trail && pos.peak >= pos.entry * (1 + this.cfg.trailArmPct)) pos.trail = true;
    if (c.h >= pos.tp) return this.exit(pos, pos.tp, 'Take profit', 'take-profit');
  }

  tick() {
    this.m.step();
    const T = this.m.tick;
    // 1) entradas: sinal nas velas fechadas, execução na abertura da vela atual
    const cands = this.scan(T);
    for (const { tok, vol5 } of cands) {
      this.lastCandidate = tok;
      this.ag.scanner = `$${tok.symbol} · vol ${compact(vol5)}`;
      if (this.positions.length >= this.cfg.maxPositions) break;
      const rug = this.rugCheck(tok);
      if (!rug.pass) {
        this.ag.rug = `REJECT $${tok.symbol}`;
        this.log('Rejected', tok.symbol, null, null, rug.reason);
        this.cool.set(tok.id, T + 30);
        continue;
      }
      this.ag.rug = `PASS $${tok.symbol}`;
      const size = this.size();
      if (size < this.cfg.minTradeUsd) continue;
      this.ag.sizer = `$${size.toFixed(2)} · ${Math.round(this.cfg.sizePctEquity * 100)}% eq`;
      this.enter(tok, size);
    }
    // 2) gestão das posições abertas
    for (const pos of [...this.positions]) this.manage(pos);
    this.ag.stop = this.ag.stop.startsWith('STOP') && this.positions.length === 0 ? this.ag.stop : `SL -${this.cfg.stopLossPct * 100}% · ${this.positions.length} armed`;
    // 3) equity
    const e = this.equity();
    this.peak = Math.max(this.peak, e);
    this.maxDD = Math.max(this.maxDD, (this.peak - e) / this.peak);
    this.curve.push({ t: this.now(), e });
  }

  closeAll() {
    for (const pos of [...this.positions]) this.exit(pos, this.lastClose(pos.tok), 'Fim', 'fim da simulação');
  }

  summary() {
    const wins = this.trades.filter((t) => t.pnl > 0).length;
    const n = this.trades.length;
    const eq = this.equity();
    return {
      equity: eq,
      pnl: eq - this.cfg.startEquity,
      pnlPct: ((eq - this.cfg.startEquity) / this.cfg.startEquity) * 100,
      trades: n,
      wins,
      losses: n - wins,
      winRate: n ? (wins / n) * 100 : 0,
      maxDD: this.maxDD * 100,
      fees: this.fees,
    };
  }

  snapshot() {
    const s = this.summary();
    const focusTok = this.positions.length ? this.positions[this.positions.length - 1].tok : (this.lastCandidate ?? this.m.tokens[0]);
    const pos = this.positions.find((p) => p.tok === focusTok) ?? null;
    const cs = focusTok.candles.slice(-60).map((c) => [c.t, c.o, c.h, c.l, c.c, c.v]);
    const step = Math.max(1, Math.ceil(this.curve.length / 300));
    return {
      mode: 'SIMULAÇÃO',
      clock: clock(this.now()),
      ...s,
      agents: this.ag,
      focus: {
        symbol: focusTok.symbol,
        candles: cs,
        position: pos && {
          entry: pos.entry,
          size: pos.size,
          sl: pos.sl,
          tp: pos.tp,
          entryT: pos.entryT,
          trail: pos.trail,
          upl: pos.units * this.lastClose(pos.tok) - pos.size,
          uplPct: (this.lastClose(pos.tok) / pos.entry - 1) * 100,
        },
      },
      open: this.positions.length,
      curve: this.curve.filter((_, i) => i % step === 0 || i === this.curve.length - 1).map((p) => p.e),
      events: this.events.slice(-14).reverse(),
    };
  }
}
