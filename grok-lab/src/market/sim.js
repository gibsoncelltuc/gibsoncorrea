// Mercado SINTÉTICO: passeio aleatório com regimes (pump / lateral / dump) e rugs.
// NÃO representa o mercado real. Serve para testar a lógica do motor e mostrar,
// com números, o que as mesmas regras fazem quando as entradas não têm vantagem.

export function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function gauss(rng) {
  let u = 0;
  let v = 0;
  while (u === 0) u = rng();
  while (v === 0) v = rng();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}

const SYL = ['ba', 'bo', 'bu', 'ca', 'co', 'da', 'do', 'fa', 'fo', 'ga', 'ha', 'jo', 'ka', 'ko', 'la', 'lo', 'ma', 'mo', 'na', 'no', 'pa', 'po', 'ra', 'ro', 'sa', 'so', 'ta', 'to', 'va', 'wo', 'za', 'zo', 'mi', 'ni', 'ri', 'ti'];

export class SimMarket {
  constructor(seed = 1) {
    this.rng = mulberry32(seed);
    this.tick = 0;
    this.tokens = [];
    this.nextId = 1;
    this.names = new Set();
    for (let i = 0; i < 30; i++) this.spawn(60 + Math.floor(this.rng() * 300));
  }

  newSymbol() {
    for (;;) {
      const n = 2 + Math.floor(this.rng() * 2);
      let s = '';
      for (let i = 0; i < n; i++) s += SYL[Math.floor(this.rng() * SYL.length)];
      s = s.toUpperCase();
      if (!this.names.has(s)) {
        this.names.add(s);
        return s;
      }
    }
  }

  spawn(ageMin) {
    const rng = this.rng;
    const mc0 = Math.exp(Math.log(30_000) + rng() * Math.log(100)); // 30K..3M
    const mintRevoked = rng() < 0.9;
    const freezeOff = rng() < 0.92;
    const lpLocked = rng() < 0.6 ? 85 + rng() * 15 : 30 + rng() * 55;
    const devPct = rng() < 0.7 ? rng() * 5 : 5 + rng() * 8;
    const top10 = 10 + rng() * 35;
    const risky = !mintRevoked || !freezeOff || lpLocked < 85 || devPct > 5 || top10 > 25;
    const rugP = risky ? 0.3 : 0.06; // os filtros reduzem, mas não eliminam, os rugs
    const tok = {
      id: this.nextId++,
      symbol: this.newSymbol(),
      born: this.tick - ageMin,
      mc: mc0,
      candles: [],
      regime: 0,
      regimeLeft: 0,
      rugged: false,
      rugAt: rng() < rugP ? this.tick + 30 + Math.floor(rng() * 900) : null,
      cloneOf: this.tokens.length && rng() < 0.08 ? this.tokens[Math.floor(rng() * this.tokens.length)].symbol : null,
      mintRevoked,
      freezeOff,
      lpLocked,
      devPct,
      top10,
      liqRatio: 0.06 + rng() * 0.14,
      baseVol: mc0 * (0.002 + rng() * 0.01),
    };
    const n = Math.min(ageMin, 120);
    for (let i = 0; i < n; i++) this.advance(tok, this.tick - (n - 1 - i), false);
    this.tokens.push(tok);
    return tok;
  }

  advance(tok, t, allowRug) {
    const rng = this.rng;
    if (tok.regimeLeft <= 0) {
      const x = rng();
      tok.regime = x < 0.15 ? 1 : x < 0.45 ? -1 : 0;
      tok.regimeLeft = 5 + Math.floor(rng() * 25);
    }
    tok.regimeLeft--;
    const mu = tok.regime === 1 ? 0.01 : tok.regime === -1 ? -0.012 : -0.0005;
    let r = mu + 0.035 * gauss(rng);
    if (allowRug && tok.rugAt !== null && t >= tok.rugAt) {
      r = Math.log(0.08);
      tok.rugAt = null;
      tok.rugged = true;
      tok.liqRatio = 0.005;
      tok.baseVol *= 0.1;
    }
    const o = tok.mc;
    const c = o * Math.exp(r);
    const h = Math.max(o, c) * (1 + Math.abs(gauss(rng)) * 0.012);
    const l = Math.min(o, c) * (1 - Math.abs(gauss(rng)) * 0.012);
    const v = tok.baseVol * (1 + 25 * Math.abs(r)) * Math.exp(0.4 * gauss(rng)) * (tok.regime === 1 ? 1.5 : 1);
    tok.mc = c;
    tok.candles.push({ t, o, h, l, c, v });
    if (tok.candles.length > 400) tok.candles.shift();
  }

  step() {
    this.tick++;
    for (const tok of this.tokens) this.advance(tok, this.tick, true);
    if (this.rng() < 0.15) this.spawn(30 + Math.floor(this.rng() * 120));
    if (this.tokens.length > 80) {
      this.tokens.sort((a, b) => a.born - b.born);
      this.tokens.splice(0, this.tokens.length - 80);
    }
  }

  liquidity(tok) {
    return tok.mc * tok.liqRatio;
  }
}
