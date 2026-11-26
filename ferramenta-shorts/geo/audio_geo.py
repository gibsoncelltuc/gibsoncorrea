# trilha dos shorts de geografia: pulso grave + pad (estilo "epic documentary") + whoosh em cada troca de pais + voz por cima
import subprocess, numpy as np, wave
SR = 48000
def _wav(p, x):
    x = np.clip(x, -1, 1); w = wave.open(p, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.repeat(x[:, None], 2, 1) * 32767).astype(np.int16).tobytes()); w.close()
def montar(OUT, SEG, TOTAL):
    n = int(TOTAL * SR); t = np.arange(n) / SR; rng = np.random.default_rng(1)
    bpm = 100; beat = 60 / bpm
    acordes = [(55.0, 65.41, 82.41), (43.65, 55.0, 65.41), (49.0, 61.74, 73.42), (41.2, 55.0, 61.74)]   # Am F G E (graves)
    pad = np.zeros(n); bass = np.zeros(n)
    for i, ac in enumerate(acordes * 20):
        a = int(i * 4 * beat * SR); b = min(n, int((i + 1) * 4 * beat * SR))
        if a >= n: break
        tt = t[a:b] - t[a]; env = np.minimum(1, tt / .4) * np.minimum(1, (4 * beat - tt) / .4)
        for f in ac: pad[a:b] += env * (np.sin(2 * np.pi * f * 2 * tt) + .5 * np.sin(2 * np.pi * f * 4 * tt + .3)) / 3
        bass[a:b] += env * np.sin(2 * np.pi * ac[0] * tt)
    kick = np.zeros(n); k1 = np.arange(int(.25 * SR)) / SR; kk = np.sin(2 * np.pi * (50 + 90 * np.exp(-k1 * 30)) * k1) * np.exp(-k1 * 9)
    for i in range(int(TOTAL / beat)):
        a = int(i * beat * SR); kick[a:a + len(kk)] += kk[:n - a]
    musica = .10 * pad + .16 * bass * (.6 + .4 * np.sin(2 * np.pi * t / beat)) + .22 * kick
    whoosh = np.zeros(n); L = int(.7 * SR); wl = np.arange(L) / SR
    ruido = rng.standard_normal(L); env = np.sin(np.pi * wl / .7) ** 2
    import scipy.signal as sg
    for (a, b, d) in SEG[1:]:
        i0 = int(max(0, a - .1) * SR); seg = ruido * env
        bb, aa = sg.butter(2, [600, 3000], 'band', fs=SR); seg = sg.lfilter(bb, aa, seg) * .5
        whoosh[i0:i0 + L] += seg[:n - i0]
    fade = np.minimum(1, np.minimum(t / 1.0, (TOTAL - t) / 1.5))
    _wav(f'{OUT}/trilha.wav', (musica + whoosh) * fade * .8)
    inp = ['-i', f'{OUT}/trilha.wav']; flt = []
    for k, (a, b, d) in enumerate(SEG):
        inp += ['-i', f'{OUT}/voz/s{k:02d}.mp3']; flt.append(f'[{k + 1}]adelay={int(a * 1000)}|{int(a * 1000)}[v{k}]')
    flt.append(''.join(f'[v{k}]' for k in range(len(SEG))) + f'amix=inputs={len(SEG)}:normalize=0,volume=1.6[voz]')
    flt.append('[0]volume=0.55[m];[voz][m]amix=2:normalize=0,loudnorm=I=-14:TP=-1.5[out]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(flt), '-map', '[out]', '-ar', '48000', '-t', str(TOTAL), f'{OUT}/audio.wav'], check=True)
