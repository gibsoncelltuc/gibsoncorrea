'use strict';
const $ = (id) => document.getElementById(id);
const usd = (x) => '$' + x.toFixed(2);
const sgn = (x) => (x >= 0 ? '+' : '-') + '$' + Math.abs(x).toFixed(2);
const mc = (v) => (v >= 1e6 ? '$' + (v / 1e6).toFixed(2) + 'M' : v >= 1e3 ? '$' + (v / 1e3).toFixed(1) + 'K' : '$' + v.toFixed(0));
const AGENTS = [
  ['Maestro', 'grok', '#8b9099'], ['Scanner', 'scanner', '#f5c542'], ['Rug Check', 'rug', '#ff5d5d'], ['Sizer', 'sizer', '#8b7bff'],
  ['Executor', 'exec', '#2dd4a7'], ['Stop Guard', 'stop', '#ff9f43'], ['Take Profit', 'tp', '#4c8dff'], ['Logger', 'logger', '#e8eaed'],
];

function drawChart(canvas, f) {
  const dpr = window.devicePixelRatio || 1;
  const w = canvas.clientWidth, h = canvas.clientHeight;
  canvas.width = w * dpr; canvas.height = h * dpr;
  const g = canvas.getContext('2d'); g.scale(dpr, dpr); g.clearRect(0, 0, w, h);
  const cs = f.candles; if (!cs.length) return;
  const padR = 74, padB = 20, volH = 38, top = 8;
  const ph = h - padB - volH - top, pw = w - padR, pos = f.position;
  let lo = Math.min(...cs.map((c) => c[3])), hi = Math.max(...cs.map((c) => c[2]));
  if (pos) { lo = Math.min(lo, pos.sl); hi = Math.max(hi, pos.tp); }
  const pad = (hi - lo) * 0.06; lo -= pad; hi += pad;
  const y = (p) => top + (1 - (p - lo) / (hi - lo)) * ph;
  const cw = pw / cs.length, bw = Math.max(2, cw * 0.62);
  const vmax = Math.max(...cs.map((c) => c[5]));
  g.font = '11px ui-monospace, Menlo, monospace'; g.textBaseline = 'middle';
  // grade e eixo de preço
  g.strokeStyle = '#161920'; g.fillStyle = '#5d6471'; g.lineWidth = 1;
  const tagYs = [y(cs[cs.length - 1][4])]; if (pos) tagYs.push(y(pos.tp), y(pos.sl));
  for (let i = 0; i <= 4; i++) { const p = lo + ((hi - lo) * i) / 4, yy = y(p); g.beginPath(); g.moveTo(0, yy); g.lineTo(pw, yy); g.stroke(); if (tagYs.every((t) => Math.abs(t - yy) > 14)) { g.textAlign = 'left'; g.fillText(mc(p), pw + 8, yy); } }
  // caixas de TP / SL a partir da vela de entrada
  if (pos) {
    let i0 = cs.findIndex((c) => c[0] >= pos.entryT); if (i0 < 0) i0 = 0;
    const x0 = i0 * cw + cw / 2;
    g.fillStyle = 'rgba(45,212,167,.13)'; g.fillRect(x0, y(pos.tp), pw - x0, y(pos.entry) - y(pos.tp));
    g.fillStyle = 'rgba(255,93,93,.20)'; g.fillRect(x0, y(pos.entry), pw - x0, y(pos.sl) - y(pos.entry));
    g.setLineDash([4, 4]); g.strokeStyle = '#4a505c'; g.beginPath(); g.moveTo(0, y(pos.entry)); g.lineTo(pw, y(pos.entry)); g.stroke(); g.setLineDash([]);
    g.strokeStyle = '#2dd4a7'; g.beginPath(); g.moveTo(x0, y(pos.tp)); g.lineTo(pw, y(pos.tp)); g.stroke();
    g.strokeStyle = '#ff6b6b'; g.beginPath(); g.moveTo(x0, y(pos.sl)); g.lineTo(pw, y(pos.sl)); g.stroke();
    const tag = (txt, yy, bg, fg) => { g.fillStyle = bg; g.fillRect(pw + 2, yy - 9, padR - 4, 18); g.fillStyle = fg; g.textAlign = 'left'; g.fillText(txt, pw + 6, yy); };
    tag('TP ' + mc(pos.tp), y(pos.tp), '#0f3a30', '#2dd4a7');
    tag('SL ' + mc(pos.sl), y(pos.sl), '#431a1a', '#ff8a8a');
  }
  // velas + volume
  cs.forEach((c, i) => {
    const x = i * cw + cw / 2, up = c[4] >= c[1], col = up ? '#2dd4a7' : '#ff6b6b';
    g.strokeStyle = col; g.fillStyle = col;
    g.beginPath(); g.moveTo(x, y(c[2])); g.lineTo(x, y(c[3])); g.stroke();
    const yo = y(c[1]), yc = y(c[4]); g.fillRect(x - bw / 2, Math.min(yo, yc), bw, Math.max(1.5, Math.abs(yo - yc)));
    g.globalAlpha = 0.35; const vh = (c[5] / vmax) * volH; g.fillRect(x - bw / 2, h - padB - vh, bw, vh); g.globalAlpha = 1;
  });
  // marcador "Buy"
  if (pos) {
    let i0 = cs.findIndex((c) => c[0] >= pos.entryT);
    if (i0 >= 0) {
      const x = i0 * cw + cw / 2, yy = y(cs[i0][3]) + 8;
      g.fillStyle = '#2dd4a7'; g.beginPath(); g.moveTo(x, yy); g.lineTo(x - 5, yy + 7); g.lineTo(x + 5, yy + 7); g.fill();
      g.fillStyle = '#0f3a30'; g.fillRect(x - 17, yy + 7, 34, 16); g.fillStyle = '#2dd4a7'; g.textAlign = 'center'; g.fillText('Buy', x, yy + 15);
    }
  }
  // preço atual
  const last = cs[cs.length - 1], yl = y(last[4]), up = last[4] >= last[1];
  g.fillStyle = up ? '#2dd4a7' : '#ff6b6b'; g.fillRect(pw + 2, yl - 9, padR - 4, 18); g.fillStyle = '#06130f'; g.textAlign = 'left'; g.fillText(mc(last[4]), pw + 6, yl);
  // eixo do tempo
  g.fillStyle = '#5d6471'; g.textAlign = 'center';
  [0, 0.25, 0.5, 0.75, 1].forEach((k) => { const i = Math.min(cs.length - 1, Math.round(k * (cs.length - 1))); const m = cs[i][0]; g.fillText(String(Math.floor(m / 60)).padStart(2, '0') + ':' + String(m % 60).padStart(2, '0'), Math.min(pw - 16, Math.max(16, i * cw + cw / 2)), h - 6); });
}

function drawEquity(canvas, curve) {
  const dpr = window.devicePixelRatio || 1, w = canvas.clientWidth, h = canvas.clientHeight;
  canvas.width = w * dpr; canvas.height = h * dpr;
  const g = canvas.getContext('2d'); g.scale(dpr, dpr); g.clearRect(0, 0, w, h);
  if (curve.length < 2) return;
  const lo = Math.min(...curve), hi = Math.max(...curve), pad = (hi - lo || 1) * 0.15;
  const x = (i) => (i / (curve.length - 1)) * (w - 70), y = (v) => 8 + (1 - (v - (lo - pad)) / (hi - lo + 2 * pad)) * (h - 16);
  const grad = g.createLinearGradient(0, 0, 0, h); grad.addColorStop(0, 'rgba(45,212,167,.28)'); grad.addColorStop(1, 'rgba(45,212,167,0)');
  g.beginPath(); curve.forEach((v, i) => (i ? g.lineTo(x(i), y(v)) : g.moveTo(x(i), y(v)))); g.strokeStyle = '#2dd4a7'; g.lineWidth = 1.6; g.stroke();
  g.lineTo(x(curve.length - 1), h); g.lineTo(0, h); g.closePath(); g.fillStyle = grad; g.fill();
  g.fillStyle = '#e8eaed'; g.font = '12px ui-monospace, Menlo, monospace'; g.textBaseline = 'middle'; g.fillText(usd(curve[curve.length - 1]), w - 64, y(curve[curve.length - 1]));
}

function render(s) {
  $('clock').textContent = 'Simulado · ' + s.clock;
  $('equity').textContent = usd(s.equity);
  const p = $('pnl'); p.textContent = sgn(s.pnl); p.className = s.pnl >= 0 ? 'up' : 'down';
  $('pnlpct').textContent = (s.pnlPct >= 0 ? '+' : '') + s.pnlPct.toFixed(1) + '%';
  $('trades').textContent = s.trades; $('wl').textContent = s.wins + 'G · ' + s.losses + 'P';
  $('wr').textContent = s.trades ? s.winRate.toFixed(0) + '%' : '—'; $('fees').textContent = 'taxas ' + usd(s.fees);
  $('dd').textContent = s.maxDD.toFixed(1) + '%'; $('open').textContent = s.open + ' posição(ões) aberta(s)';
  $('agentList').replaceChildren(...AGENTS.map(([name, key, color]) => {
    const li = document.createElement('li'), ic = document.createElement('span'), box = document.createElement('div'), nm = document.createElement('div'), st = document.createElement('div');
    ic.className = 'ico'; ic.style.background = color; nm.className = 'nm'; nm.textContent = name; st.className = 'st'; st.textContent = s.agents[key];
    if (/^(PASS|LONG|TP)/.test(s.agents[key])) st.classList.add('ok'); if (/^(REJECT|STOP|stopped)/.test(s.agents[key])) st.classList.add('bad');
    box.append(nm, st); li.append(ic, box); return li;
  }));
  const f = s.focus, last = f.candles[f.candles.length - 1];
  $('sym').textContent = '$' + f.symbol; $('px').textContent = mc(last[4]);
  $('ohlc').textContent = `O ${mc(last[1])} H ${mc(last[2])} L ${mc(last[3])} C ${mc(last[4])}`;
  const pos = f.position;
  $('posrow').replaceChildren();
  if (pos) {
    const a = document.createElement('span'); a.textContent = `Long  size ${usd(pos.size)}  entry ${mc(pos.entry)}${pos.trail ? '  · trailing armado' : ''}`;
    const b = document.createElement('span'); b.className = 'pl ' + (pos.upl >= 0 ? 'up' : 'down'); b.textContent = `${sgn(pos.upl)}  ${(pos.uplPct >= 0 ? '+' : '') + pos.uplPct.toFixed(1)}%`;
    $('posrow').append(a, b);
  } else { $('posrow').textContent = 'Flat · sem posição neste token'; }
  drawChart($('chart'), f); drawEquity($('eq'), s.curve); $('eqlast').textContent = usd(s.equity);
  $('evcount').textContent = s.events.length ? 'linha #' + s.events[0].n : '';
  $('events').replaceChildren(...s.events.map((e) => {
    const tr = document.createElement('tr'); const cls = e.type === 'Stop loss' ? 's-Stop' : 's-' + e.type;
    const cells = [e.t, e.type, '$' + e.sym, e.pnl !== null ? sgn(e.pnl) : e.usd !== null ? usd(e.usd) : '', e.note || ''];
    cells.forEach((t, i) => { const td = document.createElement('td'); td.textContent = t; if (i === 1) td.className = cls; if (i === 3) td.className = 'r ' + (e.pnl !== null ? (e.pnl >= 0 ? 'up' : 'down') : ''); tr.append(td); });
    return tr;
  }));
}

const es = new EventSource('/events');
es.onmessage = (m) => render(JSON.parse(m.data));
