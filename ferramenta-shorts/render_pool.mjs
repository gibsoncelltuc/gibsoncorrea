// RENDER EM PISCINA, RETOMAVEL, COM SEGMENTOS.   usage: node render_pool.mjs <id> <N> [workers]
//  - N navegadores (padrao = nº de nucleos) puxam quadros de UMA fila dinamica (quadros caros nao travam um shard so').
//  - Cada quadro: grava .part e renomeia (nunca fica JPEG truncado). Ao iniciar, valida os JPEG existentes e descarta os corrompidos.
//  - A cada SEG quadros completos: QA do trecho (preto/branco/faixa/glitch -> re-renderiza so' esses) e codifica o trecho em ckpt/<id>/seg_NNN.mp4
//    (ja' com legenda, qualidade final). Trecho pronto = nunca mais re-renderizado. O trecho e' o "ponto de retomada": no pior caso perde-se 1 trecho parcial.
//  - Trava de seguranca: SIGTERM/SIGINT, arquivo out/<id>/PAUSE ou DEADLINE (epoch s) => para de puxar quadros, termina os em curso, codifica trechos completos,
//    roda o checkpoint (ckpt.sh) e sai com codigo 75 ("pausado, relance para continuar").
import { launch } from './launch.mjs'; import http from 'http'; import fs from 'fs'; import path from 'path'; import os from 'os'; import { spawn, spawnSync } from 'child_process';
const [,, ID, NARG, WARG] = process.argv; const N = +NARG; const SEG = +(process.env.SEG || 150); const QUAL = +(process.env.QUAL || 0.99);   /* QUALIDADE MAXIMA (ordem do Gibson): quadro quase sem compressao */
const K = Math.max(1, +(WARG || process.env.WORKERS || os.cpus().length)); const DEADLINE = +(process.env.DEADLINE || 0) * 1000;
const FR = path.resolve(`out/${ID}/frames`), CK = path.resolve(`ckpt/${ID}`), PAUSE = path.resolve(`out/${ID}/PAUSE`), WEB = path.resolve(process.env.WEB || `../webs/${ID}`);
fs.mkdirSync(FR, { recursive: true }); fs.mkdirSync(CK, { recursive: true });
const log = (...a) => console.log(new Date().toTimeString().slice(0, 8), ...a);
const fname = (f) => path.join(FR, `f${String(f).padStart(4, '0')}.jpg`), sname = (k) => path.join(CK, `seg_${String(k).padStart(3, '0')}.mp4`);
const segRange = (k) => [k * SEG, Math.min(N, (k + 1) * SEG) - 1]; const NSEG = Math.ceil(N / SEG);
// ---- validacao de retomada ----
for (const f of fs.readdirSync(FR)) if (f.endsWith('.part')) fs.rmSync(path.join(FR, f));
for (const f of fs.readdirSync(CK)) if (f.endsWith('.part')) fs.rmSync(path.join(CK, f));
const okJpeg = (p) => { try { const st = fs.statSync(p); if (st.size < 20000) return false; const fd = fs.openSync(p, 'r'); const b = Buffer.alloc(2); fs.readSync(fd, b, 0, 2, st.size - 2); fs.closeSync(fd); return b[0] === 0xff && b[1] === 0xd9; } catch { return false; } };
const segOk = (k) => { const p = sname(k); if (!fs.existsSync(p)) return false; const r = spawnSync('ffprobe', ['-v', 'error', '-count_packets', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', p], { encoding: 'utf8' }); const [a, b] = segRange(k); return parseInt(r.stdout) === b - a + 1; };
const segDone = new Set(); for (let k = 0; k < NSEG; k++) if (segOk(k)) segDone.add(k); else fs.rmSync(sname(k), { force: true });
let bad = 0; const have = new Set(); for (const f of fs.readdirSync(FR)) { const m = /^f(\d+)\.jpg$/.exec(f); if (!m) continue; const n = +m[1]; if (segDone.has(Math.floor(n / SEG)) || !okJpeg(path.join(FR, f))) { if (!segDone.has(Math.floor(n / SEG))) { fs.rmSync(path.join(FR, f)); bad++; } continue; } have.add(n); }
log(`retomada: ${segDone.size}/${NSEG} trechos prontos, ${have.size} quadros validos soltos, ${bad} corrompidos descartados`);
// ---- fila ----
const queue = []; const remaining = {}; const attempts = {};
for (let k = 0; k < NSEG; k++) { if (segDone.has(k)) continue; const [a, b] = segRange(k); remaining[k] = 0; for (let f = a; f <= b; f++) if (!have.has(f)) { queue.push(f); remaining[k]++; } }
const segReady = []; for (const k in remaining) if (remaining[k] === 0) segReady.push(+k);
log(`${queue.length} quadros a renderizar, ${K} navegadores`);
let stopping = false, stopWhy = ''; const stop = (w) => { if (!stopping) { stopping = true; stopWhy = w; log('PAUSANDO:', w); } };
process.on('SIGTERM', () => stop('SIGTERM')); process.on('SIGINT', () => stop('SIGINT'));
const shouldStop = () => { if (stopping) return true; if (fs.existsSync(PAUSE)) { stop('arquivo PAUSE'); return true; } if (DEADLINE && Date.now() >= DEADLINE) { stop('prazo da sessao (DEADLINE)'); return true; } return false; };
// ---- servidor estatico ----
const srv = http.createServer((q, s) => { const p = path.join(WEB, decodeURIComponent(q.url.split('?')[0])); if (!fs.existsSync(p)) { s.writeHead(404); return s.end(); } s.writeHead(200, { 'Content-Type': p.endsWith('.js') ? 'text/javascript' : 'text/html' }); fs.createReadStream(p).pipe(s); }).listen(0);
await new Promise((r) => srv.on('listening', r)); const PORT = srv.address().port;
let done = 0, failed = 0; const t0 = Date.now(); let inflight = 0, doneSegs = 0;
const onFrameDone = (f) => { const k = Math.floor(f / SEG); if (--remaining[k] === 0) { segReady.push(k); drain(); } };
async function worker(id) {
  let b = null, pg = null;
  const open = async () => { b = await launch(); pg = await b.newPage({ viewport: { width: 1080, height: 1920 } }); pg.on('pageerror', (e) => log(`w${id} ERR`, e.message)); await pg.goto(`http://localhost:${PORT}/index.html${process.env.HASH || ''}`); await pg.waitForFunction(() => window.ready || window.err, null, { timeout: 240000 }); if (await pg.evaluate(() => window.err)) throw new Error('erro de pagina'); };
  const close = async () => { try { await Promise.race([b?.close(), new Promise((r) => setTimeout(r, 5000))]); } catch {} b = pg = null; };
  while (true) {
    if (shouldStop() || !queue.length) break;
    const f = queue.shift(); inflight++;
    try {
      if (!pg) await open();
      const d = await Promise.race([pg.evaluate(([f, q]) => { window.renderFrame(f); return window.getFrameDataURL(q); }, [f, QUAL]), new Promise((_, rej) => setTimeout(() => rej(new Error('timeout 180 s no quadro')), 180000))]);
      const tmp = fname(f) + '.part'; fs.writeFileSync(tmp, Buffer.from(d.slice(d.indexOf(',') + 1), 'base64')); if (!okJpeg(tmp)) throw new Error('JPEG invalido'); fs.renameSync(tmp, fname(f));
      done++; onFrameDone(f); if (done % 20 === 0) { const el = (Date.now() - t0) / 1000; log(`${done}/${done + queue.length + inflight - 1} quadros (${(el / done).toFixed(2)} s/quadro de parede; faltam ~${Math.round((queue.length + inflight) * el / done / 60)} min)`); }
    } catch (e) {
      log(`w${id} falha no quadro ${f}: ${e.message}`); attempts[f] = (attempts[f] || 0) + 1; if (attempts[f] <= 3) queue.unshift(f); else { failed++; log(`quadro ${f} DESISTIDO apos 3 tentativas`); onFrameDone(f); }
      await close();
    } finally { inflight--; }
  }
  await close();
}
// ---- codificador de trechos (1 por vez, baixa prioridade) ----
const sh = (cmd, args, opt = {}) => new Promise((res) => { const c = spawn(cmd, args, { stdio: ['ignore', 'pipe', 'pipe'], ...opt }); let o = ''; c.stdout.on('data', (d) => (o += d)); c.stderr.on('data', (d) => (o += d)); c.on('close', (code) => res({ code, out: o })); });
async function processSeg(k, round = 0) {
  const [a, b] = segRange(k); const n = b - a + 1;
  const q = await sh('python3', ['qa_frames.py', FR, path.join(WEB, 'story.js'), '--range', `${a}-${b}`, '--report', path.resolve(`out/${ID}/qa_seg${k}.json`)]);
  let flagged = []; try { flagged = JSON.parse(fs.readFileSync(`out/${ID}/qa_seg${k}.json`, 'utf8')).frames.filter((e) => e.reasons.some((r) => /band|black|white|glitch/.test(r))).map((e) => e.f); } catch {}
  if (flagged.length && round < 2) { log(`trecho ${k}: ${flagged.length} quadros reprovados no QA (${flagged.slice(0, 8).join(',')}) -> re-renderizando`); for (const f of flagged) { fs.rmSync(fname(f), { force: true }); queue.push(f); } remaining[k] = flagged.length; roundOf[k] = round + 1; return false; }
  const vf = `setpts=PTS+${a}/30/TB,subtitles=stories/${ID}/caps.ass:fontsdir=fonts,setpts=PTS-STARTPTS,format=yuv420p`;
  const r = await sh('nice', ['-n', '10', 'ffmpeg', '-v', 'error', '-y', '-framerate', '30', '-start_number', String(a), '-i', path.join(FR, 'f%04d.jpg'), '-frames:v', String(n), '-vf', vf, '-c:v', 'libx264', '-preset', process.env.X264_PRESET || 'medium', '-crf', process.env.CRF || '15', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-g', '30', '-keyint_min', '30', '-sc_threshold', '0', '-r', '30', '-threads', '2', '-an', '-f', 'mp4', sname(k) + '.part']);
  if (r.code !== 0) { log(`trecho ${k}: ffmpeg falhou: ${r.out.slice(-300)}`); fs.rmSync(sname(k) + '.part', { force: true }); return false; }
  fs.renameSync(sname(k) + '.part', sname(k)); doneSegs++; log(`trecho ${k} PRONTO (${a}-${b}, ${(fs.statSync(sname(k)).size / 1e6).toFixed(1)} MB) [${segDone.size + doneSegs}/${NSEG}]`);
  if (process.env.CKPT !== '0') sh('bash', ['ckpt.sh', ID, `trecho ${k}`]).then((x) => { if (x.code) log('ckpt:', x.out.trim().slice(-200)); });
  return true;
}
const roundOf = {}; let encRunning = false;
async function drain() { if (encRunning) return; encRunning = true; try { while (segReady.length) { const k = segReady.shift(); await processSeg(k, roundOf[k] || 0); } } finally { encRunning = false; } }
drain();
do {
  await Promise.all(Array.from({ length: K }, (_, i) => worker(i)));
  while (encRunning || segReady.length) { if (!encRunning) drain(); await new Promise((r) => setTimeout(r, 300)); }
} while (queue.length && !shouldStop());
srv.close();
const allDone = Array.from({ length: NSEG }).every((_, k) => fs.existsSync(sname(k)));
if (process.env.CKPT !== '0') await sh('bash', ['ckpt.sh', ID, 'fim da sessao de render']);
log(`fim: ${done} quadros nesta rodada (${((Date.now() - t0) / 60000).toFixed(1)} min), ${failed} desistidos, trechos ${Array.from({ length: NSEG }).filter((_, k) => fs.existsSync(sname(k))).length}/${NSEG}`);
if (allDone) process.exit(0); if (stopping) process.exit(75); process.exit(1);
