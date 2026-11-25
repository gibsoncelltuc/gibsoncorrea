// Painéis do jogo (HTML sobre o canvas 3D). Só usa textContent: nada vindo de outros jogadores vira HTML.
import { net, call, on } from './net.js';
import { CHAPTERS, FINAL_TITLE } from './shared/quests.js';
import { SKIN, HAIR_COLOR, SHIRT, PANTS, HAIR_STYLES, FACES } from './shared/world.js';

export const h = (tag, props = {}, ...kids) => {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(props)) {
    if (k === 'class') el.className = v;
    else if (k.startsWith('on')) el.addEventListener(k.slice(2), v);
    else if (k === 'disabled') el.disabled = !!v;
    else if (k === 'checked') el.checked = !!v;
    else if (k === 'value') el.value = v;
    else el.setAttribute(k, v);
  }
  for (const c of kids.flat()) if (c != null && c !== false) el.append(c.nodeType ? c : document.createTextNode(String(c)));
  return el;
};

export function toast(msg) {
  const t = h('div', { class: 'toast' }, msg);
  document.getElementById('toasts').append(t);
  setTimeout(() => t.remove(), 3700);
}
const act = (p, okMsg) =>
  p.then((r) => (okMsg && toast(okMsg), r)).catch((e) => (toast('⚠ ' + e.message), null));

const STAT = { atk: 'Ataque', def: 'Defesa', hp: 'Vida', speed: 'Velocidade', pickup: 'Coleta', luck: 'Sorte %' };
const statsText = (s) => Object.entries(s ?? {}).filter(([, v]) => v).map(([k, v]) => `${STAT[k] ?? k} ${v > 0 ? '+' : ''}${v}`).join(' · ') || '—';
const itemOf = (id) => net.catalog.items[id];
const rarityClass = (it) => 'item r-' + it.rarity;
const nameOf = (iidOrItemId, inv) => itemOf(inv ? inv.find((i) => i.iid === iidOrItemId)?.itemId : iidOrItemId)?.name ?? '?';

let tab = 'shop';
let panel;
let body;
let tabsEl;
const TABS = [
  ['shop', 'Loja (B)'],
  ['inv', 'Inventário (I)'],
  ['skills', 'Habilidades (K)'],
  ['market', 'Mercado (M)'],
  ['trade', 'Troca (T)'],
  ['tour', 'Torneios (O)'],
  ['career', 'Carreira (C)'],
  ['battle', 'Batalha (V)'],
  ['avatar', 'Avatar (U)'],
  ['help', 'Ajuda (H)'],
];
const KEYS = { b: 'shop', i: 'inv', k: 'skills', m: 'market', t: 'trade', o: 'tour', c: 'career', v: 'battle', u: 'avatar', h: 'help' };
let hooks = {};

export function initUI(h2 = {}) {
  hooks = h2;
  panel = document.getElementById('panel');
  body = document.getElementById('panelBody');
  tabsEl = document.getElementById('tabs');
  document.getElementById('panelClose').onclick = closePanel;
  tabsEl.replaceChildren(...TABS.map(([id, label]) => h('button', { class: 'tab', 'data-tab': id, onclick: () => openPanel(id) }, label)));
  addEventListener('keydown', (e) => {
    if (e.target.matches?.('input,select,textarea')) return;
    const k = e.key.toLowerCase();
    if (e.key === 'Escape') return void (isOpen() ? closePanel() : 0);
    if (KEYS[k] && !e.ctrlKey && !e.metaKey) {
      e.preventDefault();
      isOpen() && tab === KEYS[k] ? closePanel() : openPanel(KEYS[k]);
    }
  });
  on('state', () => isOpen() && ['shop', 'inv', 'skills', 'career', 'avatar'].includes(tab) && render());
  on('market', () => isOpen() && tab === 'market' && render());
  on('trades', () => isOpen() && tab === 'trade' && refreshPending());
  on('tournaments', () => isOpen() && tab === 'tour' && render());
}
export const isOpen = () => !panel.hidden;
export function openPanel(id) {
  tab = id;
  panel.hidden = false;
  hooks.onOpen?.();
  render();
}
export function closePanel() {
  panel.hidden = true;
  hooks.onClose?.();
}

function render() {
  tabsEl.querySelectorAll('.tab').forEach((b) => b.classList.toggle('on', b.dataset.tab === tab));
  body.replaceChildren(h('div', { class: 'mut' }, 'Carregando…'));
  const fn = { shop: tShop, inv: tInv, skills: tSkills, market: tMarket, trade: tTrade, tour: tTour, career: tCareer, battle: tBattle, avatar: tAvatar, help: tHelp }[tab];
  Promise.resolve(fn()).then((el) => el && body.replaceChildren(el)).catch((e) => body.replaceChildren(h('div', { class: 'bad' }, e.message)));
}

const header = () => h('div', { class: 'sub' }, h('span', { class: 'pill' }, '🪙 ', h('b', { class: 'gold' }, net.state.coins), ' moedas'), h('span', { class: 'pill' }, `Nv ${net.state.level}`));

// ---------------- Loja ----------------
let shopFilter = 'all';
function tShop() {
  const st = net.state;
  const filters = [['all', 'Tudo'], ['weapon', 'Armas'], ['head', 'Cabeça'], ['body', 'Corpo'], ['back', 'Costas'], ['tool', 'Ferramentas'], ['scroll', 'Pergaminhos']];
  const items = Object.entries(net.catalog.items).filter(([, it]) => !it.noShop).filter(([, it]) => shopFilter === 'all' || (shopFilter === 'scroll' ? it.kind === 'scroll' : it.slot === shopFilter));
  return h('div', {},
    header(),
    h('div', { class: 'sub' }, filters.map(([id, l]) => h('button', { class: 'b' + (shopFilter === id ? ' gold' : ''), onclick: () => ((shopFilter = id), render()) }, l))),
    h('div', { class: 'grid' }, items.sort((a, b) => a[1].price - b[1].price).map(([id, it]) =>
      h('div', { class: rarityClass(it) },
        h('h4', {}, it.name),
        h('small', {}, `${it.rarity} · ${it.kind === 'scroll' ? 'ensina habilidade' : net.catalog.slotNames[it.slot]}`),
        h('small', {}, it.kind === 'scroll' ? net.catalog.skills[it.skill].desc : statsText(it.stats)),
        h('div', { class: 'row' }, h('b', { class: 'gold' }, `🪙 ${it.price}`), h('button', { class: 'b gold', disabled: st.coins < it.price, onclick: () => act(call('buy', { itemId: id }), `Comprou ${it.name}`) }, 'Comprar'))))));
}

// ---------------- Inventário ----------------
function tInv() {
  const st = net.state;
  const worn = new Set(Object.values(st.equipped));
  return h('div', {},
    header(),
    h('h3', {}, 'Equipado'),
    h('div', { class: 'grid' }, net.catalog.slots.map((slot) => {
      const iid = st.equipped[slot];
      const it = iid && itemOf(st.inventory.find((i) => i.iid === iid)?.itemId);
      return h('div', { class: it ? rarityClass(it) : 'item' }, h('small', {}, net.catalog.slotNames[slot]), h('h4', {}, it ? it.name : '— vazio —'), it && h('small', {}, statsText(it.stats)), it && h('div', { class: 'row' }, h('button', { class: 'b', onclick: () => act(call('unequip', { slot })) }, 'Desequipar')));
    })),
    h('h3', {}, 'Atributos totais'), h('div', { class: 'pill' }, statsText(st.stats)),
    h('h3', {}, `Mochila (${st.inventory.length})`),
    h('div', { class: 'grid' }, st.inventory.map((inv) => {
      const it = itemOf(inv.itemId);
      return h('div', { class: rarityClass(it) },
        h('h4', {}, it.name), h('small', {}, it.kind === 'scroll' ? 'pergaminho' : statsText(it.stats)),
        h('div', { class: 'row' },
          it.slot && !worn.has(inv.iid) && h('button', { class: 'b', onclick: () => act(call('equip', { iid: inv.iid })) }, 'Equipar'),
          it.kind === 'scroll' && h('button', { class: 'b gold', onclick: () => act(call('scroll', { iid: inv.iid }), 'Habilidade aprendida!') }, 'Usar'),
          !worn.has(inv.iid) && h('button', { class: 'b', onclick: () => { const p = prompt(`Preço de venda de "${it.name}" (moedas)?`, String(Math.max(1, Math.round(it.price * 0.8)))); if (p) act(call('list', { iid: inv.iid, price: Number(p) }), 'Anunciado no mercado'); } }, 'Vender')));
    })));
}

// ---------------- Habilidades ----------------
function tSkills() {
  const st = net.state;
  return h('div', {}, header(), h('p', { class: 'mut' }, 'Aprenda habilidades usando pergaminhos (compre na Loja ou no Mercado). Depois evolua até o nível 3 com moedas. Use as teclas 1–5 na arena.'),
    h('div', { class: 'grid' }, Object.entries(net.catalog.skills).map(([id, sk]) => {
      const lv = st.skills[id] ?? 0;
      const cost = sk.upgradeBase * lv;
      return h('div', { class: 'item' },
        h('h4', {}, `[${sk.key}] ${sk.name}`), h('small', {}, sk.desc),
        h('small', {}, lv ? `Nível ${lv}/${net.catalog.maxSkill} · recarga ${sk.cd[lv - 1]}s` : 'Não aprendida'),
        h('div', { class: 'row' }, lv && lv < net.catalog.maxSkill ? h('button', { class: 'b gold', disabled: st.coins < cost, onclick: () => act(call('upgrade', { skill: id }), 'Habilidade evoluída!') }, `Evoluir 🪙 ${cost}`) : h('span', { class: 'pill' }, lv ? 'Nível máximo' : 'Compre o pergaminho')));
    })));
}

// ---------------- Mercado ----------------
async function tMarket() {
  const { listings } = await call('market');
  const me = net.state.name;
  return h('div', {}, header(), h('p', { class: 'mut' }, `Venda e compre de outros jogadores. Taxa de ${net.catalog.rules.marketFeePct * 100}% por venda (destruída, para evitar inflação).`),
    h('div', { class: 'list' }, listings.length ? listings.sort((a, b) => a.price - b.price).map((l) => {
      const it = itemOf(l.itemId);
      return h('div', {}, h('div', { class: 'grow' }, h('b', {}, it.name), ' ', h('span', { class: 'pill' }, it.rarity), h('div', { class: 'mut' }, it.kind === 'scroll' ? 'pergaminho' : statsText(it.stats)), h('small', { class: 'mut' }, `vendedor: ${l.seller}`)),
        h('b', { class: 'gold' }, `🪙 ${l.price}`),
        l.seller === me ? h('button', { class: 'b bad', onclick: () => act(call('cancel', { lid: l.id }), 'Anúncio cancelado').then(render) }, 'Cancelar') : h('button', { class: 'b gold', disabled: net.state.coins < l.price, onclick: () => act(call('buyListing', { lid: l.id }), `Comprou ${it.name}`).then(render) }, 'Comprar'));
    }) : h('div', { class: 'mut' }, 'Nenhum anúncio ainda. Venda algo pelo Inventário (I).')));
}

// ---------------- Troca ----------------
const trade = { to: '', mine: new Set(), theirs: new Set(), theirItems: [], giveCoins: 0, wantCoins: 0 };
let pendingEl;
async function refreshPending() {
  if (!pendingEl) return;
  const { trades } = await call('trades');
  const me = net.state.name;
  const desc = (t) => {
    const mine = t.from === me;
    const give = [...t.give.items.map((i) => nameOf(i, mine ? net.state.inventory : null) ?? 'item'), t.give.coins ? `🪙${t.give.coins}` : ''].filter(Boolean).join(', ') || 'nada';
    const want = [`${t.want.items.length} item(ns)`, t.want.coins ? `🪙${t.want.coins}` : ''].filter((x) => x && !x.startsWith('0 ')).join(', ') || 'nada';
    return mine ? `Você oferece [${give}] e pede [${want}] de ${t.to}` : `${t.from} oferece ${t.give.items.length} item(ns)${t.give.coins ? ` + 🪙${t.give.coins}` : ''} e pede [${want}]`;
  };
  pendingEl.replaceChildren(trades.length ? trades.map((t) => h('div', {}, h('div', { class: 'grow' }, desc(t)),
    t.to === me ? [h('button', { class: 'b gold', onclick: () => act(call('trade_respond', { tid: t.id, accept: true }), 'Troca concluída!').then(refreshPending) }, 'Aceitar'), h('button', { class: 'b', onclick: () => act(call('trade_respond', { tid: t.id, accept: false })).then(refreshPending) }, 'Recusar')]
      : h('button', { class: 'b bad', onclick: () => act(call('trade_cancel', { tid: t.id })).then(refreshPending) }, 'Cancelar'))) : h('div', { class: 'mut', style: 'padding:8px' }, 'Nenhuma troca pendente.'));
}
async function tTrade() {
  const { players } = await call('players');
  const st = net.state;
  const worn = new Set(Object.values(st.equipped));
  const mineItems = st.inventory.filter((i) => !worn.has(i.iid));
  pendingEl = h('div', { class: 'list' });
  const box = h('div', {}, header(),
    h('p', { class: 'mut' }, 'Troque itens e moedas diretamente com outro jogador. A troca só acontece se os dois lados ainda tiverem tudo no momento do "Aceitar".'),
    h('div', { class: 'sub' },
      h('select', { onchange: (e) => { trade.to = e.target.value; trade.theirs.clear(); trade.theirItems = []; if (trade.to) call('inspect', { name: trade.to }).then((r) => { trade.theirItems = r.items; draw(); }); else draw(); } },
        h('option', { value: '' }, 'Escolha o jogador…'), players.filter((p) => p.name !== st.name).map((p) => h('option', { value: p.name, ...(trade.to === p.name ? { selected: '' } : {}) }, `${p.name} (Nv ${p.level})${p.online ? ' ●' : ''}`)))),
    h('div', { id: 'tradeForm' }),
    h('h3', {}, 'Trocas pendentes'), pendingEl);
  const form = box.querySelector('#tradeForm');
  const check = (set, iid, label) => h('label', { style: 'display:flex;gap:6px;align-items:center;padding:3px 0' }, h('input', { type: 'checkbox', ...(set.has(iid) ? { checked: '' } : {}), onchange: (e) => (e.target.checked ? set.add(iid) : set.delete(iid)) }), label);
  const draw = () => {
    if (!trade.to) return form.replaceChildren();
    form.replaceChildren(h('div', { class: 'grid' },
      h('div', { class: 'item' }, h('h4', {}, 'Você oferece'), mineItems.length ? mineItems.map((i) => check(trade.mine, i.iid, itemOf(i.itemId).name)) : h('small', {}, 'Sem itens livres'), h('label', {}, 'Moedas: ', h('input', { type: 'number', min: 0, style: 'width:90px', value: trade.giveCoins, oninput: (e) => (trade.giveCoins = Number(e.target.value) || 0) }))),
      h('div', { class: 'item' }, h('h4', {}, `${trade.to} oferece`), trade.theirItems.length ? trade.theirItems.map((i) => check(trade.theirs, i.iid, itemOf(i.itemId).name)) : h('small', {}, 'Sem itens livres'), h('label', {}, 'Moedas: ', h('input', { type: 'number', min: 0, style: 'width:90px', value: trade.wantCoins, oninput: (e) => (trade.wantCoins = Number(e.target.value) || 0) })))),
      h('div', { class: 'sub', style: 'margin-top:10px' }, h('button', { class: 'b gold', onclick: () => act(call('trade_propose', { to: trade.to, giveItems: [...trade.mine], giveCoins: trade.giveCoins, wantItems: [...trade.theirs], wantCoins: trade.wantCoins }), 'Proposta enviada').then((r) => { if (r) { trade.mine.clear(); trade.theirs.clear(); trade.giveCoins = trade.wantCoins = 0; draw(); refreshPending(); } }) }, 'Enviar proposta')));
  };
  draw();
  setTimeout(refreshPending, 0);
  return box;
}

// ---------------- Torneios ----------------
let tfee = 20;
let tsize = 4;
async function tTour() {
  const { tournaments } = await call('tournaments');
  const me = net.state.name;
  const rule = net.catalog.rules;
  return h('div', {}, header(),
    h('p', { class: 'mut' }, `Mata-mata simulado pelo servidor com os atributos dos jogadores (equipamento importa!). ${rule.tournamentRakePct * 100}% do prêmio é destruído. Vagas vazias são preenchidas com bots (inscrição subsidiada pela casa).`),
    h('div', { class: 'sub' }, h('label', {}, 'Inscrição 🪙 ', h('input', { type: 'number', min: 0, max: 10000, value: tfee, style: 'width:90px', oninput: (e) => (tfee = Number(e.target.value) || 0) })),
      h('select', { onchange: (e) => (tsize = Number(e.target.value)) }, [4, 8].map((n) => h('option', { value: n, ...(tsize === n ? { selected: '' } : {}) }, `${n} jogadores`))),
      h('button', { class: 'b gold', onclick: () => act(call('t_create', { entryFee: tfee, size: tsize }), 'Torneio criado').then(render) }, 'Criar torneio')),
    h('div', { class: 'list' }, tournaments.length ? tournaments.slice().reverse().map((t) => h('div', { style: 'flex-wrap:wrap' },
      h('div', { class: 'grow' }, h('b', {}, `${t.id}`), ` · inscrição 🪙${t.entryFee} · ${t.players.length}/${t.size} · `, t.status === 'open' ? h('span', { class: 'ok' }, 'aberto') : h('span', { class: 'mut' }, `encerrado — vencedor ${t.winner} (+🪙${t.prize})`), h('div', { class: 'mut' }, 'Jogadores: ' + t.players.join(', '))),
      t.status === 'open' && !t.players.includes(me) && h('button', { class: 'b gold', onclick: () => act(call('t_join', { tid: t.id }), 'Inscrito!').then(render) }, 'Entrar'),
      t.status === 'open' && t.players.includes(me) && h('button', { class: 'b', onclick: () => act(call('t_leave', { tid: t.id })).then(render) }, 'Sair'),
      t.status === 'open' && t.host === me && h('button', { class: 'b gold', onclick: () => act(call('t_start', { tid: t.id })).then(render) }, 'Iniciar (completa com bots)'),
      t.status === 'done' && h('div', { class: 'mut', style: 'width:100%;font-size:12px' }, t.rounds.map((r, i) => h('div', {}, `Rodada ${i + 1}: `, r.map((m) => `${m.a} × ${m.b} → ${m.winner}`).join(' | ')))))) : h('div', { class: 'mut' }, 'Nenhum torneio ainda.')));
}

// ---------------- Ajuda ----------------
function tHelp() {
  return h('div', { class: 'help' },
    h('h3', {}, 'Controles'),
    h('p', {}, h('kbd', {}, 'W A S D'), ' mover · ', h('kbd', {}, 'Espaço'), ' pular · ', h('kbd', {}, 'Shift'), ' correr · clique ou ', h('kbd', {}, 'F'), ' atacar · ', h('kbd', {}, 'E'), ' falar com NPC · botão direito + arrastar ou setas: girar a câmera · roda do mouse: zoom · ', h('kbd', {}, 'Tab'), ' mapa grande · ', h('kbd', {}, 'Enter'), ' chat'),
    h('p', {}, 'Habilidades: ', h('kbd', {}, '1'), ' Investida · ', h('kbd', {}, '2'), ' Bola de Fogo · ', h('kbd', {}, '3'), ' Escudo · ', h('kbd', {}, '4'), ' Cura · ', h('kbd', {}, '5'), ' Redemoinho'),
    h('p', {}, 'Painéis: ', h('kbd', {}, 'B'), ' Loja · ', h('kbd', {}, 'I'), ' Inventário · ', h('kbd', {}, 'K'), ' Habilidades · ', h('kbd', {}, 'M'), ' Mercado · ', h('kbd', {}, 'T'), ' Troca · ', h('kbd', {}, 'O'), ' Torneios · ', h('kbd', {}, 'C'), ' Carreira · ', h('kbd', {}, 'V'), ' Batalha · ', h('kbd', {}, 'U'), ' Avatar · ', h('kbd', {}, 'P'), ' gráficos'),
    h('h3', {}, 'O mundo'),
    h('p', {}, 'Mundo aberto com 8 regiões ligadas por estradas: Vila Moeda (centro, segura), Floresta (norte), Deserto (leste), Montanhas Geladas (oeste), Fazenda (sudoeste), Praia (sul), Ruínas (noroeste) e o Castelo do Rei Gosma (nordeste). Quanto mais longe da vila, mais fortes os monstros e melhores as recompensas.'),
    h('h3', {}, 'Como funciona a economia'),
    h('p', {}, '🪙 A moeda é INTERNA do jogo e não tem valor em dinheiro. Você ganha derrotando monstros (há um teto por hora), cumprindo a carreira e vencendo duelos e torneios.'),
    h('p', {}, 'Gaste na Loja, evolua habilidades, venda e compre no Mercado, troque direto com jogadores. Parte das moedas é destruída em compras, taxas e prêmios, para a economia não inflacionar.'));
}

// ---------------- Carreira ----------------
function tCareer() {
  const c = net.state.career;
  return h('div', {}, header(),
    h('p', { class: 'mut' }, 'Modo carreira: cumpra os capítulos em ordem e derrote o Rei Gosma para zerar o jogo.'),
    c.done ? h('div', { class: 'item r-épico' }, h('h4', {}, `🏆 Você zerou o jogo! Título: ${FINAL_TITLE}`), h('small', {}, 'A Coroa do Herói está no seu inventário. Continue explorando, duelando e negociando!')) : null,
    h('div', { class: 'list' }, CHAPTERS.map((ch, i) => {
      const state = i < c.chapter || c.done ? 'feito' : i === c.chapter ? 'atual' : 'bloqueado';
      return h('div', { style: state === 'atual' ? 'background:#1a2036;border-radius:8px' : '' },
        h('div', { style: 'width:28px;font-size:18px' }, state === 'feito' ? '✅' : state === 'atual' ? '▶️' : '🔒'),
        h('div', { class: 'grow' }, h('b', {}, `${ch.id}. ${ch.title}`), h('div', { class: state === 'bloqueado' ? 'mut' : '' }, state === 'bloqueado' ? 'Complete o capítulo anterior.' : ch.text),
          state === 'atual' && c.quest ? h('div', { class: 'gold' }, `Progresso: ${c.quest.count}/${c.quest.goal}`) : null),
        h('div', { class: 'mut' }, `🪙 ${ch.reward.coins} · ${ch.reward.xp} XP${ch.reward.item ? ' · 👑 Coroa do Herói' : ''}`));
    })));
}

// ---------------- Batalha (duelo 1x1) ----------------
let queued = false;
function tBattle() {
  const r = net.catalog.rules;
  return h('div', {}, header(),
    h('p', { class: 'mut' }, `Duelo 1×1 no Coliseu (leste da vila). Cada jogador aposta 🪙 ${r.battleFee}; o vencedor leva o total menos ${r.battleRakePct * 100}% (destruído). Dura até ${r.battleSeconds}s: vence quem derrubar o outro ou tiver mais vida. Seu equipamento vale!`),
    h('p', { class: 'mut' }, 'O dano é calculado pelo servidor com os atributos reais dos dois jogadores e só conta se vocês estiverem perto. Vá até o Coliseu e entre na fila; quando outro jogador entrar, o duelo começa.'),
    h('div', { class: 'sub' },
      queued ? h('button', { class: 'b bad', onclick: () => act(call('battle_leave'), 'Você saiu da fila').then(() => ((queued = false), render())) }, 'Sair da fila') : h('button', { class: 'b gold', disabled: net.state.coins < r.battleFee, onclick: () => act(call('battle_join'), 'Na fila! Aguardando um adversário…').then((x) => { if (x) { queued = true; render(); } }) }, `Entrar na fila (🪙 ${r.battleFee})`),
      h('span', { class: 'pill' }, queued ? '⏳ Aguardando adversário' : 'Fora da fila')),
    h('p', { class: 'mut' }, 'Dica: abra duas abas com personagens diferentes para testar sozinho.'));
}
on('battle', (m) => {
  if (m.phase === 'start' || m.phase === 'end') queued = false;
});

// ---------------- Avatar ----------------
function tAvatar() {
  const ap = net.state.ap;
  const sw = (key, list, label, colors) => h('div', { style: 'margin:10px 0' }, h('b', {}, label),
    h('div', { class: 'sub', style: 'margin-top:6px' }, list.map((v, i) => h('button', { class: 'b' + (ap[key] === i ? ' gold' : ''), style: colors ? `background:${v};min-width:34px;height:34px;border:3px solid ${ap[key] === i ? '#ffd24a' : '#3a4470'}` : '', title: colors ? '' : v, onclick: () => act(call('appearance', { ap: { ...ap, [key]: i } })) }, colors ? '' : v))));
  return h('div', {}, header(), h('p', { class: 'mut' }, 'Personalize seu avatar. A mudança aparece na hora no seu personagem e para os outros jogadores.'),
    sw('skin', SKIN, 'Pele', true), sw('hair', HAIR_STYLES, 'Estilo de cabelo', false), sw('hairColor', HAIR_COLOR, 'Cor do cabelo', true), sw('shirt', SHIRT, 'Camisa', true), sw('pants', PANTS, 'Calça', true), sw('face', FACES, 'Rosto', false));
}
