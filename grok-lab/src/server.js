// Uso: node src/server.js --seed 7 --tick 400 --warm 180   -> http://127.0.0.1:8787
// Painel local (somente 127.0.0.1). Envia um snapshot por tick via Server-Sent Events.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { SimMarket } from './market/sim.js';
import { Engine } from './engine.js';

const arg = (k, d) => {
  const i = process.argv.indexOf('--' + k);
  return i > 0 ? Number(process.argv[i + 1]) : d;
};
const seed = arg('seed', 7);
const tickMs = arg('tick', 400); // ms reais por minuto simulado
const warm = arg('warm', 180); // minutos simulados antes de abrir o painel
const port = arg('port', 8787);

const root = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'public');
const FILES = {
  '/': ['index.html', 'text/html; charset=utf-8'],
  '/app.js': ['app.js', 'text/javascript; charset=utf-8'],
  '/styles.css': ['styles.css', 'text/css; charset=utf-8'],
};

const eng = new Engine(new SimMarket(seed));
for (let i = 0; i < warm; i++) eng.tick();

const clients = new Set();
const send = (res) => res.write(`data: ${JSON.stringify(eng.snapshot())}\n\n`);

setInterval(() => {
  eng.tick();
  for (const res of clients) send(res);
}, tickMs);

http
  .createServer((req, res) => {
    const url = (req.url ?? '/').split('?')[0];
    if (url === '/events') {
      res.writeHead(200, { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', Connection: 'keep-alive' });
      clients.add(res);
      send(res);
      req.on('close', () => clients.delete(res));
      return;
    }
    const f = FILES[url];
    if (!f) {
      res.writeHead(404).end('not found');
      return;
    }
    res.writeHead(200, { 'Content-Type': f[1] });
    fs.createReadStream(path.join(root, f[0])).pipe(res);
  })
  .listen(port, '127.0.0.1', () => console.log(`Painel (SIMULAÇÃO) em http://127.0.0.1:${port}  · seed ${seed} · ${tickMs} ms/min`));
