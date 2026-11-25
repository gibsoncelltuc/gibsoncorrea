// Servidor do jogo: arquivos estáticos + WebSocket. A economia é validada aqui (cliente nunca é confiável).
// Uso: node server/index.js            (http://127.0.0.1:8800, só na sua máquina)
//      HOST=0.0.0.0 node server/index.js   (para amigos na mesma rede entrarem)
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { WebSocketServer } from 'ws';
import { Economy, GameError, emptyData } from './economy.js';
import { World } from './world.js';
import { ITEMS, SKILLS, ENEMIES, RULES, SLOTS, SLOT_NAMES, MAX_SKILL_LEVEL } from './catalog.js';

const here = path.dirname(fileURLToPath(import.meta.url));
const PUBLIC = path.join(here, '..', 'public');
const DATA_FILE = process.env.DATA_FILE ?? path.join(here, '..', 'data', 'game.json');
const PORT = Number(process.env.PORT ?? 8800);
const HOST = process.env.HOST ?? '127.0.0.1';

class Store {
  constructor(file) {
    this.file = file;
    this.data = emptyData();
    try {
      this.data = { ...emptyData(), ...JSON.parse(fs.readFileSync(file, 'utf8')) };
    } catch {
      /* primeiro uso: começa vazio */
    }
    this.timer = null;
  }
  save() {
    clearTimeout(this.timer);
    this.timer = setTimeout(() => this.flush(), 300);
  }
  flush() {
    fs.mkdirSync(path.dirname(this.file), { recursive: true });
    const tmp = this.file + '.tmp';
    fs.writeFileSync(tmp, JSON.stringify(this.data));
    fs.renameSync(tmp, this.file);
  }
}

const store = new Store(DATA_FILE);
const eco = new Economy(store);
let world;
const catalog = { items: ITEMS, skills: SKILLS, enemies: ENEMIES, rules: RULES, slots: SLOTS, slotNames: SLOT_NAMES, maxSkill: MAX_SKILL_LEVEL };

const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.json': 'application/json', '.png': 'image/png', '.svg': 'image/svg+xml' };
const server = http.createServer((req, res) => {
  const url = decodeURIComponent((req.url ?? '/').split('?')[0]);
  const rel = url === '/' ? 'index.html' : url.replace(/^\/+/, '');
  const file = path.normalize(path.join(PUBLIC, rel));
  if (!file.startsWith(PUBLIC + path.sep)) return void res.writeHead(403).end('proibido');
  fs.readFile(file, (err, buf) => {
    if (err) return void res.writeHead(404).end('não encontrado');
    res.writeHead(200, { 'Content-Type': MIME[path.extname(file)] ?? 'application/octet-stream', 'Cache-Control': 'no-cache' });
    res.end(buf);
  });
});

const wss = new WebSocketServer({ server, maxPayload: 16 * 1024 });
const online = new Map(); // nome -> ws

const send = (ws, obj) => ws.readyState === 1 && ws.send(JSON.stringify(obj));
const profileOf = (name) => {
  const p = eco.player(name);
  const eq = {};
  for (const slot of SLOTS) eq[slot] = p.inventory.find((i) => i.iid === p.equipped[slot])?.itemId ?? null;
  return { t: 'profile', n: p.name, ap: p.ap, eq, lv: eco.level(p), done: !!p.career?.done };
};
const broadcast = (obj) => online.forEach((ws) => send(ws, obj));
const pushState = (name) => {
  const ws = online.get(name);
  if (ws) send(ws, { t: 'state', state: eco.view(eco.player(name)) });
  if (ws) broadcast(profileOf(name));
};
world = new World(eco, { emit: (name, msg) => online.get(name) && send(online.get(name), msg), touch: pushState });
const toast = (name, msg) => {
  const ws = online.get(name);
  if (ws) send(ws, { t: 'toast', msg });
};

// cada comando devolve { data, touch: [nomes], bcast: [tipos] }
function notifyCareer(me, r) {
  if (!r?.completed) return;
  toast(me, `📜 Capítulo concluído: ${r.completed.title} (+${r.completed.reward.coins} moedas)`);
  if (r.finished) broadcast({ t: 'chat', n: '★ Sistema', text: `${me} ZEROU O JOGO e virou Herói da Vila Moeda!` });
}
const handlers = {
  buy: (me, m) => ({ data: { iid: eco.buyItem(me, m.itemId) } }),
  equip: (me, m) => void eco.equip(me, m.iid),
  unequip: (me, m) => void eco.unequip(me, m.slot),
  scroll: (me, m) => ({ data: { skill: eco.useScroll(me, m.iid) } }),
  upgrade: (me, m) => ({ data: { level: eco.upgradeSkill(me, m.skill) } }),
  kill: (me, m) => {
    if (!world.canKill(me, m.type)) throw new GameError('bioma', 'Esse inimigo não está aqui (posição inválida)');
    const r = eco.claimKill(me, m.type);
    notifyCareer(me, r.career);
    return { data: r };
  },
  career: (me) => ({ data: { career: eco.careerView(eco.player(me)) } }),
  talk: (me, m) => {
    if (!world.near(me, String(m.npc), 8)) throw new GameError('longe', 'Chegue mais perto');
    const r = eco.careerEvent(me, 'talk', String(m.npc));
    notifyCareer(me, r);
    return { data: { career: eco.careerView(eco.player(me)), progressed: !!r } };
  },
  collect: (me, m) => {
    if (!world.nearCrystal(me, String(m.id))) throw new GameError('longe', 'Chegue mais perto do cristal');
    const r = eco.careerEvent(me, 'collect', String(m.id));
    notifyCareer(me, r);
    return { data: { career: eco.careerView(eco.player(me)), progressed: !!r } };
  },
  appearance: (me, m) => void eco.setAppearance(me, m.ap),
  chat: (me, m) => {
    const c = world.chat(me, m.text);
    broadcast({ t: 'chat', ...c });
  },
  respawn: (me) => void world.respawn(me),
  battle_join: (me) => void world.queueJoin(me),
  battle_leave: (me) => void (world.cancelQueue(me), pushState(me)),
  battle_hit: (me, m) => ({ data: { dmg: world.hit(me, String(m.target)) } }),

  market: () => ({ data: { listings: eco.market() } }),
  list: (me, m) => ({ data: { listing: eco.listItem(me, m.iid, m.price) }, bcast: ['market'] }),
  cancel: (me, m) => (eco.cancelListing(me, m.lid), { bcast: ['market'] }),
  buyListing: (me, m) => {
    const r = eco.buyListing(me, m.lid);
    toast(r.seller, `${me} comprou seu item! +${r.received} moedas (taxa ${r.fee})`);
    return { data: r, touch: [r.seller], bcast: ['market'] };
  },

  players: () => ({ data: { players: eco.playersList().map((p) => ({ ...p, online: online.has(p.name) })) } }),
  inspect: (me, m) => {
    const p = eco.player(m.name);
    const worn = new Set(Object.values(p.equipped));
    return { data: { name: p.name, level: eco.level(p), items: p.inventory.filter((i) => !worn.has(i.iid)) } };
  },
  trades: (me) => ({ data: { trades: eco.tradesFor(me) } }),
  trade_propose: (me, m) => {
    const t = eco.proposeTrade(me, m.to, { giveItems: m.giveItems, giveCoins: m.giveCoins, wantItems: m.wantItems, wantCoins: m.wantCoins });
    toast(t.to, `${me} enviou uma proposta de troca`);
    return { data: { trade: t }, bcast: ['trades'] };
  },
  trade_respond: (me, m) => {
    const t = eco.respondTrade(me, m.tid, !!m.accept);
    toast(t.from, `${me} ${t.status === 'done' ? 'aceitou' : 'recusou'} sua troca`);
    return { data: { trade: t }, touch: [t.from], bcast: ['trades'] };
  },
  trade_cancel: (me, m) => ((eco.cancelTrade(me, m.tid), { bcast: ['trades'] })),

  tournaments: () => ({ data: { tournaments: eco.tournaments() } }),
  t_create: (me, m) => ({ data: { tournament: eco.createTournament(me, m) }, bcast: ['tournaments'] }),
  t_join: (me, m) => {
    const t = eco.joinTournament(me, m.tid);
    return { data: { tournament: t }, touch: t.players, bcast: ['tournaments'] };
  },
  t_leave: (me, m) => (eco.leaveTournament(me, m.tid), { bcast: ['tournaments'] }),
  t_start: (me, m) => {
    const t = eco.startTournament(me, m.tid);
    t.players.forEach((n) => toast(n, `Torneio ${t.id} terminou: vencedor ${t.winner}`));
    return { data: { tournament: t }, touch: t.players, bcast: ['tournaments'] };
  },
};

wss.on('connection', (ws) => {
  let me = null;
  let budget = 30; // mensagens por segundo
  const refill = setInterval(() => (budget = 30), 1000);
  ws.on('close', () => {
    clearInterval(refill);
    if (me && online.get(me) === ws) {
      online.delete(me);
      world.leave(me);
      broadcast({ t: 'left', n: me });
    }
  });
  ws.on('message', (raw) => {
    let m;
    try {
      m = JSON.parse(raw.toString());
    } catch {
      return;
    }
    if (--budget < 0) {
      // excesso de mensagens: quem espera resposta recebe um aviso; posições em excesso são simplesmente ignoradas
      if (m?.id) send(ws, { id: m.id, ok: false, code: 'rapido', error: 'Devagar: mensagens demais por segundo' });
      return;
    }
    const reply = (obj) => send(ws, { id: m.id, ...obj });
    try {
      if (m.t === 'register' || m.t === 'login') {
        const p = m.t === 'register' ? eco.register(m.name, m.ap) : eco.login(m.token);
        me = p.name;
        online.get(me)?.close(4000, 'outra aba entrou');
        online.set(me, ws);
        world.join(me);
        reply({ ok: true, token: p.token, state: eco.view(p), catalog });
        send(ws, { t: 'profiles', list: [...online.keys()].map(profileOf) });
        broadcast(profileOf(me));
        return;
      }
      if (!me) throw new GameError('login', 'Entre primeiro');
      if (m.t === 'move') {
        const r = world.move(me, m);
        if (r.snap) send(ws, { t: 'tp', x: r.snap.x, z: r.snap.z });
        return;
      }
      const h = handlers[m.t];
      if (!h) throw new GameError('comando', 'Comando desconhecido');
      const out = h(me, m) ?? {};
      reply({ ok: true, ...(out.data ?? {}) });
      new Set([me, ...(out.touch ?? [])]).forEach(pushState);
      (out.bcast ?? []).forEach((t) => broadcast({ t }));
    } catch (e) {
      if (e instanceof GameError) return reply({ ok: false, code: e.code, error: e.message });
      console.error(e);
      reply({ ok: false, code: 'erro', error: 'Erro interno' });
    }
  });
});

setInterval(() => online.size && broadcast({ t: 'presence', p: world.snapshot() }), 100);
setInterval(() => world.tick(), 1000);

process.on('SIGINT', () => (store.flush(), process.exit(0)));
process.on('SIGTERM', () => (store.flush(), process.exit(0)));
server.listen(PORT, HOST, () => console.log(`Arena em http://${HOST}:${PORT}  (dados: ${DATA_FILE})`));
