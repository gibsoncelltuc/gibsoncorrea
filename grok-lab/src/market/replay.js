// Mercado de REPLAY: reproduz velas REAIS de 1 minuto (coletadas por src/collect.js) no mesmo
// formato do mercado sintético, para o Engine rodar sem nenhuma alteração.
// Preço em valor de mercado (MC): preço × (FDV / preço atual), igual ao gráfico do vídeo.

export function loadTokens(raw) {
  const symbolsSeen = new Map(); // símbolo -> token mais antigo (para detectar clones)
  const toks = [...raw.tokens].sort((a, b) => a.created - b.created);
  const out = [];
  let id = 1;
  for (const r of toks) {
    if (!r.rug) continue; // sem dados do RugCheck = não negocia (rejeitar por padrão)
    const mult = r.fdv / r.priceNow;
    const byMin = new Map(r.candles.map((c) => [Math.floor(c[0] / 60), c]));
    const t0 = Math.min(...byMin.keys());
    const t1 = Math.max(...byMin.keys());
    const all = [];
    let prev = null;
    for (let m = t0; m <= t1; m++) {
      const c = byMin.get(m);
      if (c) {
        prev = { t: m, o: c[1] * mult, h: c[2] * mult, l: c[3] * mult, c: c[4] * mult, v: c[5] };
        all.push(prev);
      } else if (prev) {
        all.push({ t: m, o: prev.c, h: prev.c, l: prev.c, c: prev.c, v: 0 }); // minuto sem negócios
        prev = all[all.length - 1];
      }
    }
    const older = symbolsSeen.get(r.symbol.toUpperCase());
    if (!older) symbolsSeen.set(r.symbol.toUpperCase(), r);
    out.push({
      id: id++,
      symbol: r.symbol,
      mint: r.mint,
      born: Math.floor(r.created / 60_000),
      all,
      cursor: 0,
      candles: [],
      cloneOf: older && older.mint !== r.mint ? older.symbol : null,
      mintRevoked: r.rug.mintRevoked,
      freezeOff: r.rug.freezeOff,
      lpLocked: r.rug.lpLocked,
      devPct: r.rug.devPct,
      top10: r.rug.top10,
    });
  }
  return out;
}

export class ReplayMarket {
  // tokens: saída de loadTokens (pode ser um subconjunto)
  // opts.from / opts.to: janela de tempo (em minutos absolutos). O histórico anterior a `from` é
  // pré-carregado para o scanner ter velas, mas só se negocia dentro da janela.
  constructor(tokens, opts = {}) {
    this.tokens = tokens.map((t) => ({ ...t, cursor: 0, candles: [] }));
    this.live = false;
    this.tMin = Math.min(...this.tokens.map((t) => t.all[0].t));
    this.tMax = Math.min(opts.to ?? Infinity, Math.max(...this.tokens.map((t) => t.all[t.all.length - 1].t)));
    this.tick = (opts.from ?? this.tMin) - 1;
    this.tokensAll = this.tokens;
    this.tokens = []; // só entram no mercado os tokens que já têm velas
    this.advanceCandles(); // pré-carrega o histórico até o tick inicial
  }

  advanceCandles() {
    for (const tok of this.tokensAll) {
      while (tok.cursor < tok.all.length && tok.all[tok.cursor].t <= this.tick) {
        tok.candles.push(tok.all[tok.cursor++]);
      }
      if (tok.candles.length && !tok._in) {
        tok._in = true;
        this.tokens.push(tok);
      }
    }
  }

  step() {
    this.tick++;
    this.advanceCandles();
  }

  get done() {
    return this.tick >= this.tMax;
  }

  liquidity() {
    return 1e12; // sem liquidez histórica disponível: o filtro de liquidez fica desligado no replay
  }
}
