#!/usr/bin/env python3
"""Piloto 'A Guerra do Porco': música original, SFX e ambiência sintetizados (numpy, seed fixo), alinhados às palavras reais."""
import json, os, re, numpy as np, wave
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *
from sfxlib import rng
D = json.load(open(f"{ROOT}/script/word-timings.json")); TOTAL = D["total"]; N = int(TOTAL * SR)
def W(line, pre, nth=0):
    n = lambda s: re.sub(r"[^\w]", "", s.lower())
    return [w for w in D["words"] if w["line"] == line and n(w["text"]).startswith(n(pre))][nth]["start"]
L = {l["id"]: l for l in D["lines"]}
BANG1 = W("L1", "matou") + 0.1; BANG2 = W("L2", "atirou") + 0.05
S = {"S2": L["L2"]["start"] - .3, "S3": L["L3"]["start"] - .3, "S4": L["L4"]["start"] - .3, "S5": L["L5"]["start"] - .3, "S6": W("L5", "ninguém") - .3}
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
# --- camadas extras (desenho de som): fazenda viva, cortes dos inserts, convés, chapéus ---
t_eyes = W("L2", "ele") - .25; t_notes = W("L3", "ofereceu") - .30; t_faces = W("L4", "depois") + .03; t_bay = W("L5", "recusou") - .22   # = cortes da EDL (blender/lib/anim.py::_edl)
for t, g in ((.22, .3), (.52, .3), (.8, .28)): E(t, "crunch", g)                                   # porco mastigando antes do tiro
E(.32, "grunt", .35)
for t in (0.18, 1.9, 2.75, 3.4, 4.15, 5.0, 6.05, 7.9, 8.6, 9.7): E(float(t), "tweet", float(.2 + .12 * rng.random()))   # pássaros no campo (S1–S3)
for t in (S["S6"] + .35, S["S6"] + 1.05, S["S6"] + 1.9): E(float(t), "tweet", .2)                  # S6: calmaria
for t in (t_eyes, t_notes, t_faces, t_bay): E(t - .05, "whoosh", .32); E(t, "thud", .4)             # corte para o insert
E(S["S5"] + .15, "creak", .3); E(S["S5"] + .95, "flap", .32); E(S["S5"] + 1.7, "creak", .26)        # convés da fragata
E(W("L5", "só") - .12, "rustle", .5)                                                                # chapéus tirados
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
