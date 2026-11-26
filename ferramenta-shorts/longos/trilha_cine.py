# trilha "cinematica" para os longos: cordas graves (serras desafinadas filtradas), pulso, tambor grave na entrada de cada bloco,
# riser antes da nota de tier e impacto quando ela aparece. uso: from trilha_cine import gerar; gerar(caminho_wav, total_s, blocos)
import numpy as np, wave
SR = 44100
def _lp(x, a):   # passa-baixa de 1 polo (a pequeno = mais escuro)
    y = np.empty_like(x); acc = 0.0
    for i in range(0, len(x), 4096):
        seg = x[i:i + 4096]; out = np.empty_like(seg)
        for j, v in enumerate(seg): acc += a * (v - acc); out[j] = acc
        y[i:i + 4096] = out
    return y
def _lpf(x, fc):   # passa-baixa rapido via FFT
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X *= 1 / (1 + (f / fc) ** 4); return np.fft.irfft(X, len(x))
def gerar(path, total, blocos):
    n = int(total * SR); t = np.arange(n) / SR; rng = np.random.default_rng(5)
    prog = [(55.0, 65.41, 82.41), (43.65, 55.0, 65.41), (49.0, 58.27, 73.42), (41.2, 49.0, 61.74)]   # Am F Gm Em (graves)
    cordas = np.zeros(n); dur_ac = 8.0
    for i in range(int(total / dur_ac) + 1):
        a = int(i * dur_ac * SR); b = min(n, int((i + 1) * dur_ac * SR) + SR)
        if a >= n: break
        tt = np.arange(b - a) / SR; env = np.minimum(1, tt / 2.5) * np.minimum(1, (b - a) / SR - tt) ** .5
        for f in prog[i % 4]:
            for det in (-.4, 0, .45):
                ff = f * 2 + det; cordas[a:b] += env * (2 * ((tt * ff) % 1) - 1) * .06
    cordas = _lpf(cordas, 900) * (1 + .15 * np.sin(2 * np.pi * t / 6))
    pulso = np.zeros(n); beat = 60 / 72
    k1 = np.arange(int(.5 * SR)) / SR; bumbo = np.sin(2 * np.pi * (38 + 70 * np.exp(-k1 * 18)) * k1) * np.exp(-k1 * 6)
    for i in range(int(total / beat)):
        a = int(i * beat * SR)
        if i % 2 == 0: pulso[a:a + len(bumbo)] += bumbo[:n - a] * .5
    tambor = np.zeros(n); rizer = np.zeros(n); imp = np.zeros(n)
    k2 = np.arange(int(1.6 * SR)) / SR; taiko = (np.sin(2 * np.pi * (60 + 40 * np.exp(-k2 * 10)) * k2) + .4 * rng.standard_normal(len(k2)) * np.exp(-k2 * 30)) * np.exp(-k2 * 3.5)
    for b in blocos:
        a = int(b['a'] * SR); tambor[a:a + len(taiko)] += taiko[:n - a] * .9
        if b.get('tier'):
            ti = b['b'] - 4.6; ia = int((ti - 2.2) * SR); L = int(2.2 * SR)
            if ia > 0:
                rr = np.arange(L) / L; ruido = rng.standard_normal(L) * rr ** 2 * .35; sw = np.sin(2 * np.pi * np.cumsum(200 + 1400 * rr ** 2) / SR) * rr ** 2 * .15
                rizer[ia:ia + L] += (_lpf(ruido, 4000) + sw)[:n - ia]
            ib = int(ti * SR); imp[ib:ib + len(taiko)] += (taiko * 1.4 + bumbo[:len(taiko)].sum() * 0 if False else taiko * 1.4)[:n - ib]
    mix = cordas * .9 + pulso * .55 + tambor * .5 + rizer + imp * .6
    fade = np.minimum(1, np.minimum(t / 2, (total - t) / 3)); mix *= fade
    mix = mix / (np.abs(mix).max() + 1e-9) * .7
    w = wave.open(path, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.repeat(mix[:, None], 2, 1) * 32767).astype(np.int16).tobytes()); w.close()
