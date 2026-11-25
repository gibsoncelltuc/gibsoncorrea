// Cliente HTTP somente-leitura para as APIs públicas, com intervalo mínimo por host e retentativas.
// Aqui no ambiente do Claude, rode com NODE_USE_ENV_PROXY=1 (o fetch do Node não usa o proxy por padrão).
const MIN_INTERVAL_MS = { 'api.geckoterminal.com': 2300, 'api.rugcheck.xyz': 800, 'api.dexscreener.com': 600 };
const lastCall = {};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export async function getJson(url, tries = 4) {
  const host = new URL(url).host;
  const gap = MIN_INTERVAL_MS[host] ?? 500;
  let lastErr;
  for (let attempt = 0; attempt < tries; attempt++) {
    const wait = (lastCall[host] ?? 0) + gap - Date.now();
    if (wait > 0) await sleep(wait);
    lastCall[host] = Date.now();
    try {
      const res = await fetch(url, {
        headers: { accept: 'application/json', 'user-agent': 'paper-trading-lab/0.1' },
        signal: AbortSignal.timeout(20_000),
      });
      if (res.status === 429) {
        await sleep(6000 * (attempt + 1));
        lastErr = new Error('429 ' + url);
        continue;
      }
      if (!res.ok) throw new Error(`HTTP ${res.status} ${url}`);
      return await res.json();
    } catch (e) {
      lastErr = e;
      await sleep(1500 * (attempt + 1));
    }
  }
  throw lastErr;
}
