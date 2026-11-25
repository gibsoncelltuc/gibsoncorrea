// Cliente de rede: WebSocket com chamadas "pergunta/resposta" e eventos empurrados pelo servidor.
export const net = { ws: null, state: null, catalog: null, seq: 1, pending: new Map(), listeners: {} };

export const on = (evt, fn) => ((net.listeners[evt] ??= []).push(fn), fn);
const emit = (evt, data) => (net.listeners[evt] ?? []).forEach((f) => f(data));

export function connect() {
  return new Promise((resolve, reject) => {
    const proto = location.protocol === 'https:' ? 'wss' : 'ws';
    const ws = new WebSocket(`${proto}://${location.host}`);
    net.ws = ws;
    ws.onopen = () => resolve();
    ws.onerror = () => reject(new Error('Não consegui conectar ao servidor'));
    ws.onclose = (e) => {
      for (const p of net.pending.values()) p.reject(new Error('Conexão perdida'));
      net.pending.clear();
      emit('closed', e);
    };
    ws.onmessage = (ev) => {
      const m = JSON.parse(ev.data);
      if (m.id && net.pending.has(m.id)) {
        const p = net.pending.get(m.id);
        net.pending.delete(m.id);
        if (m.ok) p.resolve(m);
        else p.reject(Object.assign(new Error(m.error ?? 'Erro'), { code: m.code }));
        return;
      }
      if (m.t === 'state') {
        net.state = m.state;
        emit('state', m.state);
      } else emit(m.t, m);
    };
  });
}

export function call(t, data = {}) {
  return new Promise((resolve, reject) => {
    const id = net.seq++;
    net.pending.set(id, { resolve, reject });
    net.ws.send(JSON.stringify({ id, t, ...data }));
  });
}

export async function enter(kind, payload) {
  const r = await call(kind, payload);
  net.state = r.state;
  net.catalog = r.catalog;
  return r;
}
