"""Trilha + efeitos sonoros sintetizados (sem direitos autorais) para o formato countryballs.
uso: python3 audio_cb.py web/countryball/ww1.json out/cb_ww1/mix.wav   (le spec['sfx'] e spec['music'])"""
import json, sys, numpy as np, wave
SR = 44100
spec = json.load(open(sys.argv[1])); dur = spec['music']['dur']; bpm = spec['music']['bpm']; N = int((dur + 1) * SR)
rng = np.random.default_rng(7)
def tt(d): return np.arange(int(d * SR)) / SR
def env(n, a=.005, r=.2):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na); nr = max(1, min(n, int(r * SR))); e[-nr:] *= np.linspace(1, 0, nr); return e
def lp(x, k):   # passa-baixa simples
    y = np.cumsum(x); y = (y[k:] - y[:-k]) / k; return np.concatenate([y, np.zeros(k)])
def put(buf, x, t, g=1.0):
    i = int(t * SR)
    if i >= len(buf): return
    x = x[:len(buf) - i]; buf[i:i + len(x)] += x * g
def kick(): t = tt(.28); f = 130 * np.exp(-t * 18) + 42; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) * 1.1
def hat(o=False): d = .22 if o else .05; n = int(d * SR); x = rng.standard_normal(n); x = x - lp(x, 6); return x * np.exp(-tt(d) * (14 if o else 60)) * .35
def snare(): d = .22; t = tt(d); x = rng.standard_normal(len(t)) * np.exp(-t * 22) * .7 + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 28) * .5; return x
def note(f, d, kind='saw', g=1.0):
    t = tt(d); ph = (f * t) % 1
    w = {'saw': 2 * ph - 1, 'sq': np.sign(np.sin(2 * np.pi * f * t)), 'sin': np.sin(2 * np.pi * f * t), 'pl': (2 * ph - 1) * .6 + np.sin(2 * np.pi * f * 2 * t) * .3}[kind]
    if kind in ('saw', 'sq', 'pl'): w = w - lp(w, 3) * .5
    return w * env(len(t), .004, d * .8) * g
mid = lambda m: 440 * 2 ** ((m - 69) / 12)
music = np.zeros(N); beat = 60 / bpm; nb = int((dur + 1) / beat)
# progressao em La menor: Am F C G (2 compassos cada)... energia sobe por secoes
prog = [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [48, 52, 55]), (55, [55, 59, 62])]
for b in range(nb):
    t = b * beat; bar = b // 4; root, chord = prog[(bar // 2) % 4]; sec = t
    inten = 0.45 if sec < 7 else 0.8 if sec < 34 else 1.0
    if b % 4 in (0, 2) or (inten > .7 and b % 4 == 3 and bar % 2): put(music, kick(), t, .9)
    if b % 4 in (1, 3): put(music, snare(), t, .55 * inten)
    for h in range(2): put(music, hat(h == 1 and b % 2), t + h * beat / 2, .55 * inten)
    put(music, note(mid(root - 12), beat * .9, 'sq', .26 * inten), t)                           # baixo
    if b % 2 == 1: put(music, note(mid(root - 12 + 12), beat * .45, 'sq', .15 * inten), t + beat / 2)
    for k, m in enumerate([chord[0], chord[1], chord[2], chord[1]]):                                 # arpejo "pluck"
        put(music, note(mid(m + 12), beat / 2 * .9, 'pl', .22 * inten), t + k * beat / 2 * 0 + (k % 2) * beat / 2 + (k // 2) * 0)
    if sec > 7 and b % 8 in (0, 3, 6) : put(music, note(mid(chord[2] + 24), beat * .6, 'sin', .14), t)
music /= max(1e-6, np.abs(music).max()); music *= .55
# efeitos
sfx = np.zeros(N)
def mk(k):
    if k == 'shot': d = .35; t = tt(d); x = rng.standard_normal(len(t)); x = (x - lp(x, 4)) * np.exp(-t * 22); return x * .9 + np.sin(2 * np.pi * 95 * t) * np.exp(-t * 20) * .6
    if k == 'boom': d = 1.1; t = tt(d); x = lp(rng.standard_normal(len(t)), 40) * np.exp(-t * 4) * 6 + np.sin(2 * np.pi * (60 * np.exp(-t * 1.5) + 28) * t) * np.exp(-t * 3.2); return x * .9
    if k == 'pop': d = .18; t = tt(d); return np.sin(2 * np.pi * np.cumsum(900 * np.exp(-t * 16) + 200) / SR) * np.exp(-t * 20) * .9
    if k == 'ding': d = .8; t = tt(d); return (np.sin(2 * np.pi * 1320 * t) + .5 * np.sin(2 * np.pi * 1980 * t) + .3 * np.sin(2 * np.pi * 2640 * t)) * np.exp(-t * 5) * .45
    if k == 'bonk': d = .3; t = tt(d); return np.sin(2 * np.pi * np.cumsum(420 * np.exp(-t * 9) + 110) / SR) * np.exp(-t * 11) * 1.0
    if k == 'whoosh': d = .9; t = tt(d); x = rng.standard_normal(len(t)); x = lp(x, 14) * (np.sin(np.pi * t / d) ** 2) * 5; return x * .6
    if k == 'siren': d = 1.5; t = tt(d); f = 700 + 280 * np.sin(2 * np.pi * 1.6 * t); return np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * .22 * env(len(t), .05, .5)
    if k == 'horn': d = 1.1; t = tt(d); return (np.sin(2 * np.pi * 220 * t) + .6 * np.sin(2 * np.pi * 330 * t) + .4 * np.sin(2 * np.pi * 440 * t)) * env(len(t), .08, .5) * .35
    if k == 'puff': d = .6; t = tt(d); x = lp(rng.standard_normal(len(t)), 30) * np.exp(-t * 4) * 5; return x * .5
    return np.zeros(int(.1 * SR))
for e in spec.get('sfx', []): put(sfx, mk(e['k']), e['t'], 1.0)
mix = music * .8 + sfx * .85
mix = np.tanh(mix * 1.4) * .9
mix[int(dur * SR):] = 0; mix = mix[:int(dur * SR)]
w = wave.open(sys.argv[2], 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close(); print('ok', dur, 's')
