#!/usr/bin/env python3
"""Biblioteca de timbres 100 % sintetizados (numpy, semente fixa, sem samples de terceiros) — reutilizável em qualquer vídeo da linha de produção.
Uso:  from sfxlib import *   →  sfx("gun") devolve um array mono (44,1 kHz); add(buffer, som, t_s, ganho) mistura; python3 tools/sfxlib.py --list mostra os timbres."""
import numpy as np
SR = 44100
rng = np.random.default_rng(2026)
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
    if kind == "tweet":      # passarinho (os pássaros do cenário: sets.Birds)
        n = int(0.26 * SR); t = np.arange(n) / SR; f = 3100 + 900 * np.sin(2 * np.pi * (8 + 4 * rng.random()) * t) + 800 * t / .26
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * np.minimum(t / .24, 1)) ** 2 * 0.3
    if kind == "grunt":      # porco grunhindo/mastigando
        n = int(0.32 * SR); t = np.arange(n) / SR; f = 150 + 45 * np.sin(2 * np.pi * 13 * t) - 60 * t; ph = 2 * np.pi * np.cumsum(f) / SR
        return lp(np.sign(np.sin(ph)) * .35 + np.sin(ph) * .5 + noise(n) * .12, 1100) * env(n, .012, .13)
    if kind == "creak":      # madeira/cordame do convés
        n = int(0.75 * SR); t = np.arange(n) / SR; f = 210 + 70 * np.sin(2 * np.pi * 2.6 * t) + 35 * np.sin(2 * np.pi * 9.3 * t); ph = 2 * np.pi * np.cumsum(f) / SR
        return bp(np.sign(np.sin(ph)) * .4 + np.sin(ph) * .3, 600, 420) * np.sin(np.pi * t / .75) ** 1.5 * .8
    if kind == "flap":       # pano da vela
        n = int(0.5 * SR); t = np.arange(n) / SR; return lp(noise(n), 1500) * (env(n, .004, .05) + .7 * np.roll(env(n, .004, .05), int(.13 * SR)) + .45 * np.roll(env(n, .004, .05), int(.27 * SR))) * .6
    if kind == "thud":       # batida grave no corte para um insert
        n = int(0.26 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * (58 + 40 * np.exp(-t * 30)) * t) * np.exp(-t * 17) + lp(noise(n), 260) * np.exp(-t * 32) * .35
    raise KeyError(kind)


KINDS = ["gun", "squeal", "flop", "whoosh", "rise", "crunch", "hoof", "click", "rustle", "ding", "stomp", "rattle", "horn", "squeak", "plop", "bell", "gull", "tweet", "grunt", "creak", "flap", "thud"]
if __name__ == "__main__":
    import sys
    if "--list" in sys.argv: print("\n".join(KINDS))
