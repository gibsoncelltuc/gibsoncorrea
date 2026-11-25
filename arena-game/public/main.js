import { connect, enter, net, on } from './net.js';
import { Game } from './game.js';
import { initUI, toast, closePanel } from './ui.js';

const $ = (id) => document.getElementById(id);
let game = null;

function updateHud(s) {
  $('hName').textContent = s.name;
  $('hLevel').textContent = `Nv ${s.level}`;
  $('hCoins').textContent = s.coins;
  const span = s.xpNext - s.xpThis;
  $('xpFill').style.width = `${Math.min(100, ((s.xp - s.xpThis) / span) * 100)}%`;
  $('xpText').textContent = `XP ${s.xp - s.xpThis}/${span}`;
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
  for (const [id, sk] of Object.entries(net.catalog.skills)) $('slot-' + id)?.classList.toggle('locked', !net.state.skills[id]);
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
  game = new Game($('view'), {
    toast,
    dead: (v) => ($('dead').hidden = !v),
    hud: ({ hp, max, shield, cd }) => {
      $('hpFill').style.width = `${(hp / max) * 100}%`;
      $('hpText').textContent = `${Math.ceil(hp)} / ${max}${shield ? ' 🛡' : ''}`;
      for (const [id, sk] of Object.entries(net.catalog.skills)) {
        const lv = net.state.skills[id];
        const total = lv ? sk.cd[lv - 1] : 1;
        const el = document.querySelector(`#slot-${id} .cd`);
        if (el) el.style.height = `${Math.min(100, ((cd[id] ?? 0) / total) * 100)}%`;
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
  toast('Bem-vindo! Pressione H para ver os controles.');
}

$('enterBtn').onclick = async () => {
  $('loginMsg').textContent = '';
  try {
    await start('register', { name: $('nameInput').value });
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
