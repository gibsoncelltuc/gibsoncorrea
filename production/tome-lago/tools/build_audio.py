#!/usr/bin/env python3
"""Música original, SFX sintetizados (numpy, seed fixo) e stems alinhados à timeline. Sem assets de terceiros."""
import json, os, numpy as np, wave, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 44100
D = json.load(open(f"{ROOT}/script/word-timings.json"))
TOTAL = D["total"]; N = int(TOTAL * SR)
rng = np.random.default_rng(1234)

def wstart(line, prefix, nth=0):
    import unicodedata
    norm = lambda s: s.lower().strip('.,!?:;—-')
    ws = [w for w in D["words"] if w["line"] == line and norm(w["text"]).startswith(norm(prefix))]
    return ws[nth]["start"]
def lstart(i): return next(l["start"] for l in D["lines"] if l["id"] == i)

# ------------------------------------------------ eventos (espelham as fórmulas de src/shots/Shots.tsx)
ev = []  # (t, kind, gain)
ws = lambda l, w: wstart(l, w) - 0.95 + 0.05
throws = [
    max(0.35, wstart("L1", "jogava") - 0.95 + 0.05), wstart("L2", "jogava") - 0.95 + 0.05,
    ws("L5", "mesa") - 0.2, ws("L5", "cama") - 0.2, ws("L6", "porta") - 0.2,
]
for t0 in throws:
    ev += [(t0 + 0.55, "creak", 0.5), (t0 + 0.95 - 0.12, "whoosh", 0.8), (t0 + 1.9, "splash", 1.0)]
shots = {}
for l in D["lines"]: shots.setdefault(l["shot"], l["start"] - 0.3)
for sid, st in shots.items():
    if sid != "S1": ev.append((st, "whoosh", 0.55))
coin0 = shots["S5"] + 0.3 + 0.7  # a + 0.7  (a = S5.start)
tBreak, tFix = wstart("L8", "quebra"), wstart("L8", "único")
t = coin0
while t < tBreak: ev.append((t + 0.26, "coin", 0.55)); t += 0.28
ev += [(tBreak, "crack", 1.0), (tBreak + 0.1, "boing", 0.7), (tFix + 0.5, "snap", 0.9), (tFix + 0.6, "ding", 0.6)]
tSink = wstart("L9", "afundou") - 0.5
ev += [(tSink, "gurgle", 0.9), (tSink + 0.2, "creak", 0.7)]
tWalk = wstart("L10", "caminhou")
ev += [(wstart("L10", "eram") - 0.2, "swell", 0.9)]
for k in range(int(7.0 * 3.4)): ev.append((tWalk + 0.3 + k / 3.4, "step", 0.28))
tZ = wstart("L11", "zeca")
for k in range(int(4.4 * 4.6)): ev.append((tZ - 1.2 + k / 4.6, "step", 0.22))
ev += [(tZ + 3.4, "plop", 0.4), (D["lines"][-1]["end"] + 0.2, "chime", 0.9)]
for t in (1.2, 2.6, 4.8, 8.1, 10.4): ev.append((t, "bird", 0.22))   # alvorada
for t in (12.9, 13.6, 14.2): ev.append((t, "bird", 0.14))
ev.append((lstart("L3") - 0.1, "thud", 0.5))

# ------------------------------------------------ sintetizadores
def env_ad(n, a=0.005, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / d)
def noise(n): return rng.standard_normal(n)
def lp(x, fc):  # one-pole LP vetorizado aproximado via FFT
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X *= 1 / (1 + (f / fc) ** 4); return np.fft.irfft(X, len(x))
def bp(x, f0, bw):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X *= np.exp(-0.5 * ((f - f0) / bw) ** 2); return np.fft.irfft(X, len(x))
def tone(f, dur, harm=(1, .5, .25, .12), decay=0.6, a=0.004):
    n = int(dur * SR); t = np.arange(n) / SR; y = np.zeros(n)
    for i, h in enumerate(harm): y += h * np.sin(2 * np.pi * f * (i + 1) * t + i) * np.exp(-t * (1.5 + i * 2.2) / decay)
    return y * np.minimum(t / a, 1)

def sfx(kind):
    if kind == "whoosh":
        n = int(0.5 * SR); x = bp(noise(n), 1400, 900); e = np.sin(np.linspace(0, np.pi, n)) ** 2; return x * e * 0.9
    if kind == "splash":
        n = int(1.1 * SR); x = lp(noise(n), 3800) * env_ad(n, 0.003, 0.22) + bp(noise(n), 700, 300) * env_ad(n, 0.01, 0.5) * 0.7
        t = np.arange(n) / SR; x += np.sin(2 * np.pi * (240 - 120 * np.minimum(t, .25) / .25) * t) * np.exp(-t * 9) * 0.6; return x
    if kind == "creak":
        n = int(0.4 * SR); t = np.arange(n) / SR; f = 180 + 60 * np.sin(2 * np.pi * 7 * t); return np.sin(2 * np.pi * np.cumsum(f) / SR) * lp(noise(n), 800) * 0.3 * np.sin(np.pi * t / 0.4)
    if kind == "coin":
        f = 1700 + rng.integers(-5, 5) * 60; return (tone(f, 0.5, (1, .6, .3), 0.25) + tone(f * 1.5, 0.5, (1,), 0.2) * .4) * 0.6
    if kind == "crack":
        n = int(0.5 * SR); t = np.arange(n) / SR; return (noise(n) * np.exp(-t * 25) + np.sin(2 * np.pi * 90 * t) * np.exp(-t * 12)) * 0.9
    if kind == "boing":
        n = int(0.6 * SR); t = np.arange(n) / SR; f = 300 + 400 * np.exp(-t * 6) * np.sin(2 * np.pi * 9 * t) * 0.3 + 260 * np.exp(-t * 3); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4) * 0.5
    if kind == "snap":
        n = int(0.25 * SR); t = np.arange(n) / SR; return (noise(n) * np.exp(-t * 60) * .6 + np.sin(2 * np.pi * 520 * t) * np.exp(-t * 18)) * 0.8
    if kind == "ding": return tone(1320, 1.2, (1, .5, .2), 1.0) * 0.7
    if kind == "gurgle":
        n = int(2.2 * SR); t = np.arange(n) / SR; x = bp(noise(n), 400, 250) * (0.6 + 0.4 * np.sin(2 * np.pi * 11 * t)); x += lp(noise(n), 900) * 0.4 * (0.5 + 0.5 * np.sin(2 * np.pi * 5 * t)); return x * np.sin(np.pi * np.minimum(t / 2.2, 1)) * 0.8
    if kind == "swell":
        n = int(1.8 * SR); t = np.arange(n) / SR; x = sum(np.sin(2 * np.pi * f * t) for f in (220, 277.2, 329.6, 440)) / 4; return x * (t / 1.8) ** 2 * np.exp(-((t - 1.8) / 1.2) ** 2 * 0) * 0.9
    if kind == "step":
        n = int(0.09 * SR); t = np.arange(n) / SR; return bp(noise(n), 900, 500) * np.exp(-t * 55) + np.sin(2 * np.pi * 120 * t) * np.exp(-t * 50) * 0.4
    if kind == "plop":
        n = int(0.3 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * (500 - 250 * t / .3) * t) * np.exp(-t * 14)
    if kind == "chime": return (tone(880, 2.4, (1, .4, .2), 1.6) + tone(1318.5, 2.4, (1, .3), 1.4) * .7 + tone(1760, 2.4, (1,), 1.2) * .4) * 0.5
    if kind == "bird":
        n = int(0.5 * SR); t = np.arange(n) / SR; f = 3000 + 900 * np.sin(2 * np.pi * (6 + rng.random() * 5) * t) + 400 * t; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * np.minimum(t / .22, 1)) ** 2 * (t < .22)
    if kind == "thud":
        n = int(0.3 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * 70 * t) * np.exp(-t * 14)
    raise KeyError(kind)

sfx_bus = np.zeros(N)
for t, kind, g in sorted(ev):
    s = sfx(kind) * g; i = int(t * SR)
    if i < 0 or i >= N: continue
    j = min(N, i + len(s)); sfx_bus[i:j] += s[: j - i]
# ambiente: lago (ruído filtrado + ondas lentas) e vento de inverno
t_ = np.arange(N) / SR
water = lp(noise(N), 500) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.11 * t_)) * 0.09
wind_w = np.clip((t_ - lstart("L5")) / 6, 0, 1) * 0.85 + 0.15
wind = bp(noise(N), 350, 220) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * t_ + 1)) * 0.07 * wind_w
amb_bus = water + wind

def add(buf, s, t):
    i = int(t * SR)
    if i < 0 or i >= len(buf): return
    j = min(len(buf), i + len(s)); buf[i:j] += s[: j - i]
# ------------------------------------------------ música (progressão Am–F–C–G, 92 bpm; intensidade por seção)
BPM = 92; beat = 60 / BPM
chords = [("A", [220.0, 261.63, 329.63]), ("F", [174.61, 261.63, 349.23]), ("C", [261.63, 329.63, 392.0]), ("G", [196.0, 246.94, 392.0])]
def inten(t):
    pts = [(0, .35), (12, .45), (23, .6), (34, .85), (35, .5), (46, .7), (52, 1.0), (63, .6), (TOTAL, .25)]
    return float(np.interp(t, [p[0] for p in pts], [p[1] for p in pts]))
music = np.zeros(N)
bar = 4 * beat
nbars = int(TOTAL / bar) + 2
for b in range(nbars):
    name, notes = chords[b % 4]; t0 = b * bar
    if t0 > TOTAL: break
    I = inten(t0)
    # pad
    for f in notes:
        s = tone(f / 2, bar * 1.15, (1, .3, .1), 3.0, 0.4) * 0.07 * I; add(music, s, t0)
    # baixo
    for k in (0, 2):
        s = tone(notes[0] / 2, beat * 1.6, (1, .4), 0.5) * 0.18 * (0.5 + I * .5); add(music, s, (t0 + k * beat))
    # arpejo pluck (colcheias)
    arp = [0, 1, 2, 1, 2, 1, 0, 1] if I < .7 else [0, 1, 2, 1, 2, 1, 2, 1]
    for k, ix in enumerate(arp):
        f = notes[ix] * (2 if ix else 1) * (1.5 if (I > .9 and k == 7) else 1)
        s = tone(f, 0.7, (1, .55, .3, .15), 0.35) * 0.11 * (0.45 + 0.55 * I); add(music, s, (t0 + k * beat / 2))
    # melodia (a partir do S4)
    if t0 >= 23:
        mel = {"A": 659.25, "F": 698.46, "C": 783.99, "G": 587.33}[name]
        for k, off in enumerate((0, 1.5, 2.5)):
            s = tone(mel * (1.12246 if k == 2 and name in "CG" else 1), 1.0, (1, .35, .12), 0.7) * 0.07 * I; add(music, s, (t0 + off * beat))
    # shaker leve no S4/S5
    if 23 <= t0 < 46:
        for k in range(8):
            s = bp(noise(int(0.06 * SR)), 6500, 2500) * np.exp(-np.arange(int(0.06 * SR)) / SR * 70) * 0.05; add(music, s, (t0 + k * beat / 2))
# fade in/out
music *= np.clip(t_ / 1.5, 0, 1) * np.clip((TOTAL - t_) / 2.5, 0, 1)
music = lp(music, 7000)

def save(name, x, stereo=False):
    x = np.clip(x, -1, 1); a = (x * 32767).astype(np.int16)
    with wave.open(f"{ROOT}/audio/{name}.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(a.tobytes())
peak = lambda x: x / max(1e-9, np.abs(x).max()) * 0.8
save("music", peak(music)); save("sfx", peak(sfx_bus)); save("ambience", peak(amb_bus))
json.dump([{"t": round(t, 3), "kind": k, "gain": g} for t, k, g in sorted(ev)], open(f"{ROOT}/audio/sfx-events.json", "w"), indent=1)
print("ok", len(ev), "eventos")
