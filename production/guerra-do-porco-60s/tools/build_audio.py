#!/usr/bin/env python3
"""Áudio do vídeo: SFX ancorados nas palavras (audio/events.json) + ambiência + base musical simples → audio/{music,sfx,ambience}.wav (mesmo contrato de tools/mix.py).
audio/events.json: [{"line": "L1", "word": "palavra", "dt": 0.1, "kind": "gun", "gain": 1.0}, {"t": 3.2, "kind": "whoosh", "gain": 0.4}]   — timbres: python3 tools/sfxlib.py --list
audio/music.json (opcional): {"bpm": 100, "root": 50, "chords": [[0,4,7],[5,9,12],[7,11,14],[0,4,7]], "ambience": {"sea": 0.1, "wind": 0.06}}
Tudo sintetizado (numpy, semente fixa): sem samples de terceiros. Para um desenho de som sofisticado, veja production/guerra-do-porco/tools/build_audio.py (música por seção, marcha, sino…)."""
import json, os, re, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(f"{ROOT}/script/word-timings.json")); TOTAL = D["total"]; N = int(TOTAL * SR)
def W(line, pre, nth=0):
    n = lambda s: re.sub(r"[^\w]", "", s.lower())
    return [w for w in D["words"] if w["line"] == line and n(w["text"]).startswith(n(pre))][nth]["start"]
ev_path = f"{ROOT}/audio/events.json"; events = json.load(open(ev_path)) if os.path.exists(ev_path) else []
mu_path = f"{ROOT}/audio/music.json"; M = json.load(open(mu_path)) if os.path.exists(mu_path) else {}
sfxb = np.zeros(N)
for e in events:
    t = e["t"] if "t" in e else W(e["line"], e["word"], e.get("nth", 0)) + e.get("dt", 0.0); add(sfxb, sfx(e["kind"]), t, e.get("gain", 1.0))
tt = np.arange(N) / SR; A = M.get("ambience", {"sea": 0.1, "wind": 0.06})
amb = lp(noise(N), 450) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.17 * tt)) * A.get("sea", 0.1) + bp(noise(N), 330, 200) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.08 * tt + 1)) * A.get("wind", 0.06)
bpm = M.get("bpm", 100); beat = 60 / bpm; root = M.get("root", 50); chords = M.get("chords", [[0, 4, 7], [5, 9, 12], [7, 11, 14], [0, 4, 7]]); music = np.zeros(N)
mnote = lambda m: 440.0 * 2 ** ((m - 69) / 12)
for b in range(int(TOTAL / beat) + 1):
    ch = chords[(b // 4) % len(chords)]; t0 = b * beat
    add(music, tone(mnote(root + ch[b % 3] + 12), .35, (1, .5, .28, .12), .3, .002) * .2, t0)
    if b % 4 == 0: add(music, tone(mnote(root + ch[0]), beat * 4, (1, .3, .1), 3, .35) * .06, t0)
music *= np.clip(tt / 0.6, 0, 1) * np.clip((TOTAL - tt) / 1.6, 0, 1); music = lp(music, 7500)
def save(name, x):
    x = np.clip(x / max(1e-9, np.abs(x).max()) * 0.8, -1, 1); a = (x * 32767).astype(np.int16)
    with wave.open(f"{ROOT}/audio/{name}.wav", "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(a.tobytes())
os.makedirs(f"{ROOT}/audio", exist_ok=True); save("music", music); save("sfx", sfxb); save("ambience", amb)
print("ok", len(events), "eventos; total", round(TOTAL, 2))
