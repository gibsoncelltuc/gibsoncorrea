// Economia do jogo (lógica pura, sem rede). O servidor é a autoridade: o cliente só pede, o servidor valida.
// Moeda INTERNA do jogo. Contabilidade: minted (criada) = moedas dos jogadores + escrow de torneios + burned (destruída).
import crypto from 'node:crypto';
import { ITEMS, SKILLS, ENEMIES, RULES, SLOTS, MAX_SKILL_LEVEL, baseStats, levelFromXp, xpForLevel } from './catalog.js';
import { CHAPTERS, FINAL_TITLE } from '../public/shared/quests.js';
import { cleanAppearance } from '../public/shared/world.js';

export class GameError extends Error {
  constructor(code, msg) {
    super(msg);
    this.code = code;
  }
}
const fail = (code, msg) => {
  throw new GameError(code, msg);
};

function mulberry32(seed) {
  let a = seed >>> 0;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const hash = (s) => [...s].reduce((h, c) => (Math.imul(h, 31) + c.charCodeAt(0)) | 0, 7);
const int = (x, lo, hi, what) => {
  const n = Number(x);
  if (!Number.isInteger(n) || n < lo || n > hi) fail('valor', `${what} inválido (inteiro entre ${lo} e ${hi})`);
  return n;
};

export const emptyData = () => ({ seq: 1, players: {}, listings: [], trades: [], tournaments: [], stats: { minted: 0, burned: 0, escrowBattle: 0 } });

export class Economy {
  constructor(store, opts = {}) {
    this.store = store;
    this.d = store.data;
    this.d.stats.escrowBattle ??= 0;
    this.now = opts.now ?? Date.now;
    this.rng = opts.rng ?? Math.random;
  }

  #id(prefix) {
    return prefix + this.d.seq++;
  }
  #commit() {
    this.store.save?.();
  }
  #mint(n) {
    this.d.stats.minted += n;
  }
  #burn(n) {
    this.d.stats.burned += n;
  }

  // ---------- contas ----------
  register(rawName, appearance) {
    const name = String(rawName ?? '').trim();
    if (!/^[A-Za-z0-9_]{3,16}$/.test(name)) fail('nome', 'Nome: 3 a 16 letras, números ou _');
    if (this.d.players[name.toLowerCase()]) fail('existe', 'Esse nome já está em uso');
    const p = {
      name,
      token: crypto.randomBytes(16).toString('hex'),
      coins: RULES.startCoins,
      xp: 0,
      kills: 0,
      inventory: [],
      equipped: Object.fromEntries(SLOTS.map((s) => [s, null])),
      skills: {},
      ap: cleanAppearance(appearance),
      career: { chapter: 0, count: 0, got: [], done: false },
      earn: { hour: 0, amount: 0 },
      lastClaim: 0,
      createdAt: this.now(),
    };
    this.d.players[name.toLowerCase()] = p;
    this.#mint(RULES.startCoins);
    const iid = this.#giveItem(p, 'sword_wood');
    p.equipped.weapon = iid;
    this.#commit();
    return p;
  }
  login(token) {
    const p = Object.values(this.d.players).find((x) => x.token === token);
    if (!p) fail('login', 'Sessão inválida. Crie um personagem.');
    return p;
  }
  player(name) {
    const p = this.d.players[String(name ?? '').toLowerCase()];
    if (!p) fail('jogador', 'Jogador não encontrado');
    return p;
  }
  level(p) {
    return levelFromXp(p.xp);
  }
  stats(p) {
    const s = baseStats(this.level(p));
    for (const slot of SLOTS) {
      const it = p.inventory.find((i) => i.iid === p.equipped[slot]);
      if (it) for (const [k, v] of Object.entries(ITEMS[it.itemId].stats)) s[k] = (s[k] ?? 0) + v;
    }
    return s;
  }
  view(p) {
    const level = this.level(p);
    return {
      name: p.name,
      coins: p.coins,
      xp: p.xp,
      level,
      xpThis: xpForLevel(level),
      xpNext: xpForLevel(level + 1),
      kills: p.kills,
      inventory: p.inventory,
      equipped: p.equipped,
      skills: p.skills,
      stats: this.stats(p),
      ap: p.ap ?? cleanAppearance(),
      career: this.careerView(p),
    };
  }
  setAppearance(name, ap) {
    const p = this.player(name);
    p.ap = cleanAppearance(ap);
    this.#commit();
  }
  playersList() {
    return Object.values(this.d.players).map((p) => ({ name: p.name, level: this.level(p) }));
  }
  #giveItem(p, itemId) {
    const iid = this.#id('i');
    p.inventory.push({ iid, itemId });
    return iid;
  }
  #own(p, iid) {
    const it = p.inventory.find((i) => i.iid === iid);
    if (!it) fail('item', 'Você não possui esse item');
    return it;
  }
  #free(p, iid) {
    const it = this.#own(p, iid);
    if (Object.values(p.equipped).includes(iid)) fail('equipado', 'Desequipe o item primeiro');
    return it;
  }

  // ---------- loja, equipamentos, habilidades ----------
  buyItem(name, itemId) {
    const p = this.player(name);
    const item = ITEMS[itemId];
    if (!item) fail('item', 'Item inexistente');
    if (p.coins < item.price) fail('moedas', 'Moedas insuficientes');
    p.coins -= item.price;
    this.#burn(item.price);
    const iid = this.#giveItem(p, itemId);
    this.#commit();
    return iid;
  }
  equip(name, iid) {
    const p = this.player(name);
    const it = this.#own(p, iid);
    const slot = ITEMS[it.itemId].slot;
    if (!slot) fail('slot', 'Esse item não pode ser equipado');
    p.equipped[slot] = iid;
    this.#commit();
  }
  unequip(name, slot) {
    const p = this.player(name);
    if (!SLOTS.includes(slot)) fail('slot', 'Espaço inválido');
    p.equipped[slot] = null;
    this.#commit();
  }
  useScroll(name, iid) {
    const p = this.player(name);
    const it = this.#own(p, iid);
    const item = ITEMS[it.itemId];
    if (item.kind !== 'scroll') fail('item', 'Isso não é um pergaminho');
    if (p.skills[item.skill]) fail('ja', 'Você já conhece essa habilidade (venda ou troque o pergaminho)');
    p.skills[item.skill] = 1;
    p.inventory = p.inventory.filter((i) => i.iid !== iid);
    this.#commit();
    return item.skill;
  }
  upgradeSkill(name, skillId) {
    const p = this.player(name);
    const sk = SKILLS[skillId];
    const lv = p.skills[skillId];
    if (!sk || !lv) fail('skill', 'Você não conhece essa habilidade');
    if (lv >= MAX_SKILL_LEVEL) fail('max', 'Habilidade já está no nível máximo');
    const cost = sk.upgradeBase * lv;
    if (p.coins < cost) fail('moedas', `Moedas insuficientes (custa ${cost})`);
    p.coins -= cost;
    this.#burn(cost);
    p.skills[skillId] = lv + 1;
    this.#commit();
    return lv + 1;
  }

  // ---------- recompensa por inimigo derrotado (o servidor impõe teto e intervalo) ----------
  claimKill(name, type, opts = {}) {
    const out = this.#claimKill(name, type, opts);
    out.career = this.careerEvent(name, 'kill', type);
    return out;
  }
  #claimKill(name, type, opts = {}) {
    const p = this.player(name);
    const en = ENEMIES[type];
    if (!en) fail('inimigo', 'Inimigo inválido');
    const t = this.now();
    if (!opts.skipGap && t - p.lastClaim < RULES.minClaimGapMs) fail('rapido', 'Rápido demais');
    p.lastClaim = t;
    if (t - p.earn.hour > 3_600_000) p.earn = { hour: t, amount: 0 };
    const [lo, hi] = en.coins;
    let coins = lo + Math.floor(this.rng() * (hi - lo + 1));
    coins = Math.round(coins * (1 + (this.stats(p).luck ?? 0) / 100));
    coins = Math.max(0, Math.min(coins, RULES.maxCoinsPerHour - p.earn.amount));
    p.earn.amount += coins;
    p.coins += coins;
    this.#mint(coins);
    const before = this.level(p);
    p.xp += en.xp;
    p.kills++;
    this.#commit();
    return { coins, xp: en.xp, levelUp: this.level(p) > before };
  }

  // ---------- mercado entre jogadores (o item fica em custódia até vender ou cancelar) ----------
  listItem(name, iid, price) {
    const p = this.player(name);
    const pr = int(price, 1, RULES.maxPrice, 'Preço');
    const it = this.#free(p, iid);
    p.inventory = p.inventory.filter((i) => i.iid !== iid);
    const l = { id: this.#id('l'), seller: p.name, iid, itemId: it.itemId, price: pr, createdAt: this.now() };
    this.d.listings.push(l);
    this.#commit();
    return l;
  }
  cancelListing(name, lid) {
    const p = this.player(name);
    const l = this.d.listings.find((x) => x.id === lid);
    if (!l) fail('anuncio', 'Anúncio não existe mais');
    if (l.seller !== p.name) fail('dono', 'Só o vendedor pode cancelar');
    this.d.listings = this.d.listings.filter((x) => x !== l);
    p.inventory.push({ iid: l.iid, itemId: l.itemId });
    this.#commit();
  }
  buyListing(name, lid) {
    const p = this.player(name);
    const l = this.d.listings.find((x) => x.id === lid);
    if (!l) fail('anuncio', 'Anúncio não existe mais');
    if (l.seller === p.name) fail('proprio', 'Você não pode comprar o próprio anúncio');
    if (p.coins < l.price) fail('moedas', 'Moedas insuficientes');
    const seller = this.player(l.seller);
    const fee = Math.floor(l.price * RULES.marketFeePct);
    p.coins -= l.price;
    seller.coins += l.price - fee;
    this.#burn(fee);
    p.inventory.push({ iid: l.iid, itemId: l.itemId });
    this.d.listings = this.d.listings.filter((x) => x !== l);
    this.#commit();
    return { seller: seller.name, received: l.price - fee, fee };
  }
  market() {
    return this.d.listings.map((l) => ({ ...l }));
  }

  // ---------- troca direta entre dois jogadores ----------
  proposeTrade(from, to, offer) {
    const a = this.player(from);
    const b = this.player(to);
    if (a === b) fail('proprio', 'Escolha outro jogador');
    const giveItems = [...new Set(offer.giveItems ?? [])];
    const wantItems = [...new Set(offer.wantItems ?? [])];
    const giveCoins = int(offer.giveCoins ?? 0, 0, RULES.maxPrice, 'Moedas oferecidas');
    const wantCoins = int(offer.wantCoins ?? 0, 0, RULES.maxPrice, 'Moedas pedidas');
    if (!giveItems.length && !wantItems.length && !giveCoins && !wantCoins) fail('vazio', 'Troca vazia');
    this.#checkSide(a, giveItems, giveCoins);
    for (const iid of wantItems) this.#own(b, iid);
    if (this.d.trades.filter((t) => t.from === a.name && t.status === 'pending').length >= 5) fail('limite', 'Você já tem 5 trocas pendentes');
    const t = { id: this.#id('t'), from: a.name, to: b.name, give: { items: giveItems, coins: giveCoins }, want: { items: wantItems, coins: wantCoins }, status: 'pending', expires: this.now() + RULES.tradeTtlMs };
    this.d.trades.push(t);
    this.#commit();
    return t;
  }
  #checkSide(p, items, coins) {
    for (const iid of items) this.#free(p, iid);
    if (p.coins < coins) fail('moedas', `${p.name} não tem moedas suficientes`);
  }
  respondTrade(name, tid, accept) {
    const p = this.player(name);
    const t = this.d.trades.find((x) => x.id === tid);
    if (!t || t.status !== 'pending') fail('troca', 'Troca não está mais disponível');
    if (this.now() > t.expires) {
      t.status = 'expired';
      this.#commit();
      fail('expirou', 'A troca expirou');
    }
    if (t.to !== p.name) fail('dono', 'Essa troca não é para você');
    if (!accept) {
      t.status = 'declined';
      this.#commit();
      return t;
    }
    const a = this.player(t.from);
    this.#checkSide(a, t.give.items, t.give.coins);
    this.#checkSide(p, t.want.items, t.want.coins);
    const moveItems = (src, dst, ids) => {
      for (const iid of ids) {
        const it = src.inventory.find((i) => i.iid === iid);
        src.inventory = src.inventory.filter((i) => i.iid !== iid);
        dst.inventory.push(it);
      }
    };
    moveItems(a, p, t.give.items);
    moveItems(p, a, t.want.items);
    a.coins += t.want.coins - t.give.coins;
    p.coins += t.give.coins - t.want.coins;
    t.status = 'done';
    this.#commit();
    return t;
  }
  cancelTrade(name, tid) {
    const t = this.d.trades.find((x) => x.id === tid);
    if (!t || t.status !== 'pending') fail('troca', 'Troca não está mais disponível');
    if (t.from !== this.player(name).name) fail('dono', 'Só quem propôs pode cancelar');
    t.status = 'cancelled';
    this.#commit();
    return t;
  }
  tradesFor(name) {
    const p = this.player(name);
    return this.d.trades.filter((t) => t.status === 'pending' && this.now() <= t.expires && (t.from === p.name || t.to === p.name));
  }

  // ---------- torneios (mata-mata simulado no servidor) ----------
  createTournament(name, { entryFee, size }) {
    const p = this.player(name);
    const fee = int(entryFee, 0, 10_000, 'Inscrição');
    if (![4, 8].includes(Number(size))) fail('tamanho', 'Torneio de 4 ou 8 jogadores');
    if (p.coins < fee) fail('moedas', 'Moedas insuficientes');
    p.coins -= fee;
    const t = { id: this.#id('c'), host: p.name, entryFee: fee, size: Number(size), players: [p.name], pool: fee, bots: 0, status: 'open', createdAt: this.now(), rounds: [], winner: null, prize: 0 };
    this.d.tournaments.push(t);
    this.#commit();
    return t;
  }
  joinTournament(name, tid) {
    const p = this.player(name);
    const t = this.#openTournament(tid);
    if (t.players.includes(p.name)) fail('ja', 'Você já está inscrito');
    if (p.coins < t.entryFee) fail('moedas', 'Moedas insuficientes');
    p.coins -= t.entryFee;
    t.pool += t.entryFee;
    t.players.push(p.name);
    if (t.players.length === t.size) this.#runTournament(t);
    this.#commit();
    return t;
  }
  leaveTournament(name, tid) {
    const p = this.player(name);
    const t = this.#openTournament(tid);
    if (!t.players.includes(p.name)) fail('fora', 'Você não está inscrito');
    p.coins += t.entryFee;
    t.pool -= t.entryFee;
    t.players = t.players.filter((x) => x !== p.name);
    if (!t.players.length) this.d.tournaments = this.d.tournaments.filter((x) => x !== t);
    else if (t.host === p.name) t.host = t.players[0];
    this.#commit();
  }
  startTournament(name, tid) {
    const p = this.player(name);
    const t = this.#openTournament(tid);
    if (t.host !== p.name) fail('dono', 'Só o criador pode iniciar');
    while (t.players.length < t.size) {
      t.bots++;
      t.players.push(`Bot-${t.bots}`);
      t.pool += t.entryFee; // inscrição dos bots é subsidiada pela casa (moeda criada)
      this.#mint(t.entryFee);
    }
    this.#runTournament(t);
    this.#commit();
    return t;
  }
  #openTournament(tid) {
    const t = this.d.tournaments.find((x) => x.id === tid);
    if (!t) fail('torneio', 'Torneio não encontrado');
    if (t.status !== 'open') fail('fechado', 'Torneio já foi disputado');
    return t;
  }
  #fighter(name, avgLevel, rng) {
    const key = name.toLowerCase();
    if (this.d.players[key]) {
      const p = this.d.players[key];
      return { name: p.name, ...this.stats(p) };
    }
    const lv = Math.max(1, avgLevel + Math.floor(rng() * 3) - 1);
    const s = baseStats(lv);
    return { name, ...s, atk: s.atk + Math.floor(rng() * 6), def: Math.floor(rng() * 4), hp: s.hp + Math.floor(rng() * 20) };
  }
  #runTournament(t) {
    const rng = mulberry32(hash(t.id) ^ (t.createdAt & 0xffff));
    const humans = t.players.filter((n) => this.d.players[n.toLowerCase()]);
    const avg = Math.round(humans.reduce((s, n) => s + this.level(this.player(n)), 0) / Math.max(1, humans.length));
    let alive = t.players.map((n) => this.#fighter(n, avg, rng));
    for (let i = alive.length - 1; i > 0; i--) {
      const j = Math.floor(rng() * (i + 1));
      [alive[i], alive[j]] = [alive[j], alive[i]];
    }
    t.rounds = [];
    while (alive.length > 1) {
      const next = [];
      const round = [];
      for (let i = 0; i < alive.length; i += 2) {
        const r = simulateDuel(alive[i], alive[i + 1], rng);
        const w = r.winner === 'a' ? alive[i] : alive[i + 1];
        round.push({ a: alive[i].name, b: alive[i + 1].name, winner: w.name, turns: r.turns });
        next.push(w);
      }
      t.rounds.push(round);
      alive = next;
    }
    t.winner = alive[0].name;
    const rake = Math.floor(t.pool * RULES.tournamentRakePct);
    t.prize = t.pool - rake;
    this.#burn(rake);
    const wp = this.d.players[t.winner.toLowerCase()];
    if (wp) wp.coins += t.prize;
    else this.#burn(t.prize); // bot venceu: o prêmio volta para a casa
    t.status = 'done';
  }
  tournaments() {
    return this.d.tournaments.slice(-12).map((t) => ({ ...t }));
  }

  // ---------- modo carreira ----------
  careerView(p) {
    const c = (p.career ??= { chapter: 0, count: 0, got: [], done: false });
    const def = CHAPTERS[c.chapter];
    return { chapter: c.chapter, total: CHAPTERS.length, done: c.done, title: c.done ? FINAL_TITLE : null, quest: def ? { id: def.id, title: def.title, text: def.text, type: def.type, goal: def.goal, count: c.count, loc: def.loc ?? null, reward: def.reward } : null };
  }
  #grant(p, reward) {
    if (reward.coins) {
      p.coins += reward.coins;
      this.#mint(reward.coins);
    }
    if (reward.xp) p.xp += reward.xp;
    if (reward.item) this.#giveItem(p, reward.item);
  }
  // kind: 'kill' (key = tipo) | 'talk' (key = npc) | 'collect' (key = id do cristal) | 'reach' (key = local). Devolve null se nada mudou.
  careerEvent(name, kind, key) {
    const p = this.player(name);
    const c = (p.career ??= { chapter: 0, count: 0, got: [], done: false });
    const def = CHAPTERS[c.chapter];
    if (c.done || !def || def.type !== kind) return null;
    if (kind === 'kill' && def.enemy !== key) return null;
    if (kind === 'talk' && def.npc !== key) return null;
    if (kind === 'collect') {
      if (!def.ids?.includes(key) || c.got.includes(key)) return null;
      c.got.push(key);
    }
    if (kind === 'reach') return null;
    c.count++;
    let completed = null;
    if (c.count >= def.goal) {
      this.#grant(p, def.reward);
      completed = { id: def.id, title: def.title, reward: def.reward };
      c.chapter++;
      c.count = 0;
      c.got = [];
      if (c.chapter >= CHAPTERS.length) c.done = true;
    }
    this.#commit();
    return { progressed: true, completed, finished: c.done };
  }

  // ---------- custódia das apostas de batalha ----------
  battleLock(name, fee) {
    const p = this.player(name);
    if (p.coins < fee) fail('moedas', 'Moedas insuficientes para a aposta');
    p.coins -= fee;
    this.d.stats.escrowBattle += fee;
    this.#commit();
  }
  battleRefund(name, fee) {
    const p = this.player(name);
    p.coins += fee;
    this.d.stats.escrowBattle -= fee;
    this.#commit();
  }
  // vencedor leva o total menos a taxa (destruída); sem vencedor (empate), cada um recebe de volta
  battleSettle(winner, pot) {
    const rake = Math.floor(pot * RULES.battleRakePct);
    const prize = pot - rake;
    this.d.stats.escrowBattle -= pot;
    this.#burn(rake);
    this.player(winner).coins += prize;
    this.#commit();
    return { prize, rake };
  }

  // ---------- auditoria ----------
  audit() {
    const players = Object.values(this.d.players).reduce((s, p) => s + p.coins, 0);
    const escrow = this.d.tournaments.filter((t) => t.status === 'open').reduce((s, t) => s + t.pool, 0);
    const { minted, burned, escrowBattle } = this.d.stats;
    return { minted, burned, players, escrow, escrowBattle, ok: minted === players + escrow + escrowBattle + burned };
  }
}

export function simulateDuel(a, b, rng) {
  let ha = a.hp;
  let hb = b.hp;
  let aTurn = a.speed === b.speed ? rng() < 0.5 : a.speed > b.speed;
  let turns = 0;
  while (ha > 0 && hb > 0 && turns < 300) {
    const [atk, def] = aTurn ? [a, b] : [b, a];
    const dmg = Math.max(1, Math.round(atk.atk * (0.8 + 0.4 * rng()) - def.def * 0.5));
    if (aTurn) hb -= dmg;
    else ha -= dmg;
    aTurn = !aTurn;
    turns++;
  }
  return { winner: ha / a.hp >= hb / b.hp ? 'a' : 'b', turns };
}
