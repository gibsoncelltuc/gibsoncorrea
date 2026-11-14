#!/usr/bin/env python3
"""Piloto 'A Guerra do Porco': música original, SFX e ambiência sintetizados (numpy, seed fixo), alinhados às palavras reais."""
import json, os, re, numpy as np, wave
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 44100
D = json.load(open(f"{ROOT}/script/word-timings.json")); TOTAL = D["total"]; N = int(TOTAL * SR)
rng = np.random.default_rng(2026)
def W(line, pre, nth=0):
    n = lambda s: re.sub(r"[^\w]", "", s.lower())
    return [w for w in D["words"] if w["line"] == line and n(w["text"]).startswith(n(pre))][nth]["start"]
L = {l["id"]: l for l in D["lines"]}
BANG1 = W("L1", "matou") + 0.1; BANG2 = W("L2", "atirou") + 0.05
S = {"S2": L["L2"]["start"] - .3, "S3": L["L3"]["start"] - .3, "S4": L["L4"]["start"] - .3, "S5": L["L5"]["start"] - .3, "S6": W("L5", "ninguém") - .3}
def env(n, a=0.004, d=0.2): t = np.arange(n) / SR; return np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / d)
def noise(n): return rng.standard_normal(n)
def spec(x, f):
    X = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / SR); return np.fft.irfft(X * f(fr), len(x))
def lp(x, fc): return spec(x, lambda f: 1 / (1 + (f / fc) ** 4))
def hp(x, fc): return spec(x, lambda f: 1 - 1 / (1 + (f / fc) ** 4))
def bp(x, f0, bw): return spec(x, lambda f: np.exp(-0.5 * ((f - f0) / bw) ** 2))
def tone(f, dur, harm=(1, .5, .25, .12), dec=.6, a=.004, vib=0.0):
    n = int(dur * SR); t = np.arange(n) / SR; ph = 2 * np.pi * f * t + (vib * np.sin(2 * np.pi * 5.5 * t) if vib else 0); y = np.zeros(n)
    for i, h in enumerate(harm): y += h * np.sin(ph * (i + 1) + i) * np.exp(-t * (1.2 + i * 1.8) / dec)
    return y * np.minimum(t / a, 1)
def add(buf, s, t, g=1.0):
    i = int(t * SR)
    if i < 0 or i >= len(buf): return
    j = min(len(buf), i + len(s)); buf[i:j] += s[: j - i] * g

def sfx(kind):
    if kind == "gun":
        n = int(1.6 * SR); t = np.arange(n) / SR
        x = noise(n) * np.exp(-t * 18) + hp(noise(n), 800) * np.exp(-t * 55) * 1.2 + np.sin(2 * np.pi * (95 - 40 * np.minimum(t, .3) / .3) * t) * np.exp(-t * 9) * 1.1
        return x + lp(noise(n), 600) * np.exp(-t * 3.2) * 0.35
    if kind == "squeal":
        n = int(0.62 * SR); t = np.arange(n) / SR; f = 900 + 700 * np.sin(np.pi * np.minimum(t / .5, 1)) - 250 * t; f += 45 * np.sin(2 * np.pi * 32 * t)
        ph = 2 * np.pi * np.cumsum(f) / SR; y = np.sign(np.sin(ph)) * 0.35 + np.sin(ph) * 0.6 + np.sin(2 * ph) * 0.25
        return lp(y, 4200) * np.minimum(t / .02, 1) * np.exp(-np.maximum(t - .3, 0) * 6)
    if kind == "flop": n = int(0.35 * SR); t = np.arange(n) / SR; return lp(noise(n), 400) * np.exp(-t * 18) + np.sin(2 * np.pi * 70 * t) * np.exp(-t * 16)
    if kind == "whoosh": n = int(0.7 * SR); t = np.arange(n) / SR; return bp(noise(n), 1800, 1100) * np.sin(np.pi * t / 0.7) ** 2
    if kind == "rise": n = int(1.4 * SR); t = np.arange(n) / SR; f = 120 * np.exp(t * 1.3); y = np.sin(2 * np.pi * np.cumsum(f) / SR) * (t / 1.4) ** 2; return y * 0.8 + bp(noise(n), 2500, 1500) * (t / 1.4) ** 3 * 0.3
    if kind == "crunch": n = int(0.12 * SR); t = np.arange(n) / SR; return bp(noise(n), 2600, 1400) * env(n, .001, .03) + lp(noise(n), 500) * env(n, .001, .05) * .6
    if kind == "hoof": n = int(0.08 * SR); t = np.arange(n) / SR; return lp(noise(n), 900) * env(n, .001, .02) + np.sin(2 * np.pi * 180 * t) * np.exp(-t * 50) * .5
    if kind == "click": n = int(0.2 * SR); t = np.arange(n) / SR; return hp(noise(n), 2500) * (env(n, .0005, .004) + .7 * np.roll(env(n, .0005, .004), int(.09 * SR))) * 0.7
    if kind == "rustle": n = int(0.4 * SR); t = np.arange(n) / SR; return hp(noise(n), 3000) * env(n, .01, .09) * (0.6 + 0.4 * np.sin(2 * np.pi * 38 * t))
    if kind == "ding": return tone(1760, 1.0, (1, .4, .15), .5) * 0.6
    if kind == "stomp": n = int(0.16 * SR); t = np.arange(n) / SR; return lp(noise(n), 700) * env(n, .001, .03) + np.sin(2 * np.pi * 85 * t) * np.exp(-t * 28)
    if kind == "rattle": n = int(0.1 * SR); return hp(noise(n), 4000) * env(n, .001, .02) * .5
    if kind == "horn": return (tone(147, 1.5, (1, .7, .5, .3, .2), 1.6, .12) + tone(110, 1.5, (1, .6, .4, .2), 1.6, .12)) * 0.5
    if kind == "squeak": n = int(0.22 * SR); t = np.arange(n) / SR; f = 1400 + 900 * t / .22; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
    if kind == "plop": n = int(0.25 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * (700 - 400 * t / .25) * t) * np.exp(-t * 15) * .6
    if kind == "bell": return (tone(196, 3.2, (1, .5, .3), 2.4, .003) + tone(196 * 2.01, 3.2, (1, .35), 2.0, .003) * .6 + tone(196 * 3.03, 3.2, (1,), 1.4, .003) * .35) * 0.8
    if kind == "gull":
        n = int(0.7 * SR); t = np.arange(n) / SR; f = 1800 + 700 * np.sin(2 * np.pi * 4 * t) * np.exp(-t * 2) - 600 * t; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * np.minimum(t / .6, 1)) ** 2 * 0.5
    raise KeyError(kind)

ev = []
def E(t, k, g=1.0): ev.append((t, k, g))
E(BANG1, "gun", 1.0); E(BANG1 + .04, "squeal", .85); E(BANG1 + .6, "flop", .8)
E(2.2, "rise", .8); E(2.3, "whoosh", .6); E(W("L1", "guerra") - 0.1, "horn", .7)
for t in np.arange(4.0, 5.9, 0.17): E(float(t), "hoof", .35)
for t in np.arange(W("L2", "horta") + .1, BANG2 - .5, 0.19): E(float(t), "crunch", .38)
E(BANG2 - .85, "click", .7); E(BANG2, "gun", 1.0)
for k in ("S3", "S4", "S5", "S6"): E(S[k] - .15, "whoosh", .45)
E(W("L3", "cem") - .35, "rustle", .6); E(W("L3", "cem") - .1, "ding", .5); E(W("L3", "ofereceu") - .2, "rustle", .45)
for k in range(int((S["S5"] - 0.1 - S["S4"]) * 3.8)):
    t = S["S4"] + .15 + k / 3.8; E(t, "stomp", .5 + .4 * min(1, k / 10)); E(t + .02, "rattle", .35)
E(W("L4", "navios") - .2, "horn", .9)
E(W("L5", "recusou") + .2, "squeak", .6); E(W("L5", "recusou") + .75, "plop", .5)
E(W("L5", "ninguém") - .05, "bell", .7); E(W("L5", "só") + .05, "bell", .55)
for t in (S["S5"] + .3, S["S5"] + 1.3): E(t, "gull", .35)
sfxb = np.zeros(N)
for t, k, g in sorted(ev): add(sfxb, sfx(k), t, g)
tt = np.arange(N) / SR
sea = lp(noise(N), 450) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.17 * tt)) * 0.12
wind = bp(noise(N), 330, 200) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.08 * tt + 1)) * 0.07
cric = np.zeros(N)
for t in np.arange(S["S6"], TOTAL, 0.22):
    for j in range(3): add(cric, tone(4300, 0.03, (1,), .02, .002) * 0.18, float(t) + j * 0.045)
amb = sea + wind + cric

# ---- música: D menor → D maior. 112 bpm.
BPM = 112; beat = 60 / BPM; music = np.zeros(N)
def mnote(m): return 440.0 * 2 ** ((m - 69) / 12)
def pluck(f, dur=0.5, g=.2): return tone(f, dur, (1, .5, .28, .12), .3, .002) * g
def fife(f, dur, g=.14): return tone(f, dur, (1, .08, .3, .05, .12), 1.2, .02, vib=1.2) * g
def pad(f, dur, g=.05): return tone(f, dur, (1, .3, .1), 3, .35) * g
def snare(g=.1): n = int(0.09 * SR); return (bp(noise(n), 3200, 1800) * env(n, .001, .03)) * g
def tim(f=74, g=.35): n = int(0.4 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * (f + 25 * np.exp(-t * 14)) * t) * np.exp(-t * 7) * g
Dm = [50, 53, 57]; Gm = [55, 58, 62]; A7 = [57, 61, 64]; Dmaj = [50, 54, 57]
def chord_at(t): return Dm if t < 5.2 else (Gm if t < 8 else (Dm if t < 11.4 else (A7 if t < 15.8 else (Dm if t < 17.8 else Dmaj))))
nb = int(TOTAL / beat) + 2
for b in range(nb):
    t0 = b * beat; ch = chord_at(t0)
    if t0 >= TOTAL: break
    root = mnote(ch[0] - 12)
    if t0 < 3.7:      # S1: tensão
        if b % 2 == 0: add(music, pluck(root * 2, .6, .22), t0)
        add(music, pad(mnote(ch[0]), beat * 2.2, .06), t0)
    elif t0 < 11.4:   # S2–S3: pizzicato "caminhando" cômico
        add(music, pluck(root, .35, .26), t0); add(music, pluck(mnote(ch[(b % 3)] + 12), .22, .16), t0 + beat / 2)
        if b % 2 == 1: add(music, pluck(mnote(ch[2] + 12), .18, .14), t0 + beat * .75)
    elif t0 < 15.8:   # S4: marcha
        add(music, tim(74), t0, .6 if b % 2 == 0 else .35)
        for k in range(4): add(music, snare(.12 + .02 * k), t0 + k * beat / 4)
        mel = [74, 77, 81, 77, 74, 77, 79, 81]; add(music, fife(mnote(mel[b % 8] + 0), beat * .9, .14 + .02 * (t0 - 11.4)), t0)
        add(music, pad(mnote(ch[0] - 12), beat, .05), t0)
    elif t0 < 17.8:   # S5: suspense (cai a quase silêncio em 'recusou')
        g = 1.0 if t0 < W("L5", "recusou") else .3
        add(music, pad(mnote(ch[0]), beat * 2.4, .07 * g), t0)
        if b % 2 == 0: add(music, pluck(mnote(ch[2] + 12), .6, .14 * g), t0)
    else:             # S6: resolução em ré maior (harpa lenta)
        for k, m in enumerate([62, 66, 69, 74]): add(music, pluck(mnote(m), 1.2, .16), t0 + k * beat / 2)
        add(music, pad(mnote(50), beat * 2.4, .08), t0)
music *= np.clip(tt / 0.6, 0, 1) * np.clip((TOTAL - tt) / 1.6, 0, 1); music = lp(music, 7500)
def save(name, x):
    x = np.clip(x / max(1e-9, np.abs(x).max()) * 0.8, -1, 1); a = (x * 32767).astype(np.int16)
    with wave.open(f"{ROOT}/audio/{name}.wav", "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(a.tobytes())
save("music", music); save("sfx", sfxb); save("ambience", amb)
json.dump([{"t": round(t, 3), "kind": k, "gain": g} for t, k, g in sorted(ev)], open(f"{ROOT}/audio/sfx-events.json", "w"), indent=1)
print("ok", len(ev), "eventos; total", round(TOTAL, 2))
