import { connect, enter, net, on, call } from './net.js';
import { Game } from './game.js';
import { initUI, toast, isOpen, closePanel } from './ui.js';
import { Minimap } from './minimap.js';
import { LOCATIONS, SKIN, HAIR_COLOR, SHIRT, PANTS, HAIR_STYLES, FACES } from './shared/world.js';

const $ = (id) => document.getElementById(id);
const rn = (n) => Math.floor(Math.random() * n);
let game = null;
let mm = null;
let mmBig = null;
let bigOn = false;

function updateHud(s) {
  $('hName').textContent = s.name;
  $('hLevel').textContent = `Nv ${s.level}`;
  $('hCoins').textContent = s.coins;
  const span = s.xpNext - s.xpThis;
  $('xpFill').style.width = `${Math.min(100, ((s.xp - s.xpThis) / span) * 100)}%`;
  $('xpText').textContent = `XP ${s.xp - s.xpThis}/${span}`;
  const q = s.career?.quest;
  $('questBox').hidden = !q && !s.career?.done;
  if (q) {
    $('qTitle').textContent = `${q.id}/${s.career.total} · ${q.title}`;
    $('qText').textContent = q.text;
    $('qFill').style.width = `${(q.count / q.goal) * 100}%`;
    $('qCount').textContent = `${q.count}/${q.goal}`;
  } else if (s.career?.done) {
    $('qTitle').textContent = '🏆 Herói da Vila Moeda';
    $('qText').textContent = 'Você zerou a carreira! Duele, negocie e explore.';
    $('qFill').style.width = '100%';
    $('qCount').textContent = '';
    $('qHint').textContent = '';
  }
}

function buildSkillbar() {
  $('skillbar').replaceChildren(
    ...Object.entries(net.catalog.skills).map(([id, sk]) => {
      const el = document.createElement('div');
      el.className = 'slot';
      el.id = 'slot-' + id;
      const k = document.createElement('b');
      k.textContent = sk.key;
      const n = document.createElement('span');
      n.textContent = sk.name;
      const cd = document.createElement('div');
      cd.className = 'cd';
      el.append(k, n, cd);
      return el;
    }),
  );
}
function refreshSkillbar() {
  for (const id of Object.keys(net.catalog.skills)) $('slot-' + id)?.classList.toggle('locked', !net.state.skills[id]);
}

const DIALOG = {
  smith: ['Eu forjo ferro há 30 anos. Armaduras de ferro e a Lâmina Flamejante deixam qualquer um mais forte!', 'Quer sobreviver ao Castelo? Equipe armadura e aprenda a Cura. Os pergaminhos estão na loja (B).'],
  farmer: ['As Gosmas estão comendo minhas plantações! Se puder, derrote algumas.', 'No inverno os lobos descem das montanhas geladas. Cuidado, eles são rápidos!'],
  guard1: ['O Coliseu fica logo ali. Duelos valem moedas, mas só os corajosos vencem!', 'Aperte V para ver as regras do duelo.'],
  guard2: ['Atrás do Coliseu a estrada segue até o deserto. Leve água... ou melhor, poções de cura.', 'O Rei Gosma no castelo é muito forte. Treine antes!'],
  kid: ['Dizem que há cristais brilhantes na floresta!', 'Eu queria ter uma Capa Vermelha. Sou o maior fã de heróis!'],
};
let dialogOpen = false;
function closeDialog() {
  if (!dialogOpen) return;
  dialogOpen = false;
  $('dialog').hidden = true;
  game.setEnabled(true);
}
async function openDialog(npc) {
  let text;
  if (npc.id === 'mayor') {
    try {
      const r = await call('talk', { npc: 'mayor' });
      const c = r.career;
      if (r.progressed && c.chapter === 1) text = 'Bem-vindo, aventureiro! A Vila Moeda precisa de você. Os campos estão cheios de Gosmas: derrote 8 delas e volte à sua jornada. Cuidado, o mundo é grande e perigoso!';
      else if (c.done) text = 'Você é o Herói da Vila Moeda! O Rei Gosma foi derrotado graças a você. Obrigado, campeão!';
      else text = `Sua missão atual: ${c.quest.title}. ${c.quest.text}`;
    } catch (e) {
      text = e.message;
    }
  } else text = DIALOG[npc.id][Math.floor(Math.random() * DIALOG[npc.id].length)];
  $('dName').textContent = npc.name;
  $('dText').textContent = text;
  $('dialog').hidden = false;
  dialogOpen = true;
  game.setEnabled(false);
}

function addChat(m) {
  const row = document.createElement('div');
  if (m.n.startsWith('★')) row.className = 'sys';
  const b = document.createElement('b');
  b.textContent = m.n + ': ';
  row.append(b, document.createTextNode(m.text));
  const log = $('chatLog');
  log.append(row);
  while (log.children.length > 8) log.firstChild.remove();
  setTimeout(() => row.remove(), 25000);
}

function hint(q, g) {
  const t = g.questTarget();
  if (!t || !q) return '';
  const d = Math.round(Math.hypot(t.x - g.player.position.x, t.z - g.player.position.z));
  return `🎯 Destino a ${d} m (marcado no mapa)`;
}

async function start(kind, payload) {
  if (!net.ws || net.ws.readyState > 1) await connect();
  const r = await enter(kind, payload);
  localStorage.setItem('arena-token', r.token);
  $('login').hidden = true;
  $('hud').hidden = false;
  buildSkillbar();
  refreshSkillbar();
  updateHud(net.state);
  let mmReady = false;
  game = new Game($('view'), {
    toast,
    chat: addChat,
    dead: (v) => ($('dead').hidden = !v),
    dialog: openDialog,
    prompt: (t) => {
      $('prompt').hidden = !t || dialogOpen;
      if (t) $('prompt').textContent = t;
    },
    place: (name) => {
      const b = $('placeBanner');
      b.textContent = name;
      b.classList.remove('show');
      void b.offsetWidth;
      b.classList.add('show');
    },
    bigmap: (v) => {
      bigOn = v;
      $('bigmap').hidden = !v;
    },
    battle: (b, ev) => {
      $('battleHud').hidden = !b;
      if (b) {
        $('bMe').textContent = net.state.name;
        $('bOp').textContent = b.opponent;
      }
      void ev;
    },
    hud: ({ hp, max, shield, cd, x, z, yaw, tod, battle }) => {
      if (!mmReady) {
        mm = new Minimap($('minimap'));
        mmBig = new Minimap($('bigmap'), mm.terrain);
        mmBig.setBig(true);
        mmReady = true;
      }
      $('hpFill').style.width = `${(hp / max) * 100}%`;
      $('hpText').textContent = `${Math.ceil(hp)} / ${max}${shield ? ' 🛡' : ''}`;
      for (const [id, sk] of Object.entries(net.catalog.skills)) {
        const lv = net.state.skills[id];
        const total = lv ? sk.cd[lv - 1] : 1;
        const el = document.querySelector(`#slot-${id} .cd`);
        if (el) el.style.height = `${Math.min(100, ((cd[id] ?? 0) / total) * 100)}%`;
      }
      const others = [...game.remotes.values()].map((r) => ({ x: r.g.position.x, z: r.g.position.z }));
      const me = { x, z, yaw };
      mm.draw(me, others, game.questTarget(), game.world.npcs);
      if (bigOn) mmBig.draw(me, others, game.questTarget(), game.world.npcs);
      const hour = (tod * 24 + 6) % 24;
      $('clock').textContent = `🕒 ${String(Math.floor(hour)).padStart(2, '0')}:${String(Math.floor((hour % 1) * 60)).padStart(2, '0')}`;
      $('qHint').textContent = hint(net.state.career?.quest, game);
      if (battle) {
        const op = battle.opponent;
        const f = (n) => Math.max(0, battle.hp[n]) / battle.maxHp[n];
        $('bMeFill').style.width = `${f(net.state.name) * 100}%`;
        $('bOpFill').style.width = `${f(op) * 100}%`;
        $('bMeText').textContent = Math.ceil(battle.hp[net.state.name]);
        $('bOpText').textContent = Math.ceil(battle.hp[op]);
        $('bTimer').textContent = `⚔ ${Math.max(0, Math.ceil((battle.until - performance.now()) / 1000))}`;
      }
    },
  });
  on('state', (s) => {
    updateHud(s);
    refreshSkillbar();
    game.refreshCharacter();
  });
  on('toast', (m) => toast(m.msg));
  on('closed', () => toast('Conexão perdida. Recarregue a página.'));
  initUI({ onOpen: () => game.setEnabled(false), onClose: () => game.setEnabled(true) });
  game.world.npcs.length || null;

  // chat
  const input = $('chatInput');
  input.addEventListener('focus', () => game.setEnabled(false));
  input.addEventListener('blur', () => !isOpen() && !dialogOpen && game.setEnabled(true));
  input.addEventListener('keydown', (e) => {
    e.stopPropagation();
    if (e.key === 'Enter') {
      const text = input.value.trim();
      input.value = '';
      input.blur();
      if (text) call('chat', { text }).catch((err) => toast('⚠ ' + err.message));
    } else if (e.key === 'Escape') input.blur();
  });
  addEventListener('keydown', (e) => {
    if (e.target.matches?.('input,select,textarea')) return;
    if (e.key === 'Enter' && !isOpen() && !dialogOpen) (e.preventDefault(), input.focus());
    if ((e.key === 'e' || e.key === 'E' || e.key === 'Escape') && dialogOpen) (e.preventDefault(), closeDialog());
  });
  toast('Bem-vindo ao mundo aberto! Fale com o Prefeito (E) para começar a carreira. H = ajuda.');
}

$('enterBtn').onclick = async () => {
  $('loginMsg').textContent = '';
  const ap = { skin: rn(SKIN.length), hair: rn(HAIR_STYLES.length), hairColor: rn(HAIR_COLOR.length), shirt: rn(SHIRT.length), pants: rn(PANTS.length), face: rn(FACES.length) };
  try {
    await start('register', { name: $('nameInput').value, ap });
  } catch (e) {
    $('loginMsg').textContent = e.message;
  }
};
$('nameInput').addEventListener('keydown', (e) => e.key === 'Enter' && $('enterBtn').click());

const saved = localStorage.getItem('arena-token');
if (saved) {
  start('login', { token: saved }).catch(() => {
    localStorage.removeItem('arena-token');
    $('login').hidden = false;
  });
}
void closePanel;
void LOCATIONS;
