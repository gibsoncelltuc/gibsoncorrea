#!/usr/bin/env python3
"""Confere cada música: transcreve com Whisper e compara com a letra. Uso: conferir_virais.py [n ...]"""
import sys, re, difflib, glob, os
sys.path.insert(0, os.path.dirname(__file__))
import musicas_virais as m
from faster_whisper import WhisperModel
import librosa
W = WhisperModel("small", device="cpu", compute_type="int8")
norm = lambda s: re.sub(r"[^a-zà-ú ]", "", s.lower().replace("\n", " "))
D = os.path.join(os.path.dirname(__file__), "..", "musicas-virais")
for n in [int(x) for x in sys.argv[1:]] or range(1, 11):
    f = glob.glob(f"{D}/{n:02d}-*.mp3")
    if not f: continue
    y16 = librosa.load(f[0], sr=16000)[0]
    segs, _ = W.transcribe(y16, language="pt", condition_on_previous_text=False)
    t = norm(" ".join(s.text for s in segs))
    lyr = norm(re.sub(r"\[.*?\]", "", m.SONGS[n]["lyr"]))
    r = difflib.SequenceMatcher(None, t, lyr).ratio()
    dur = len(y16)/16000
    bpm = librosa.feature.tempo(y=y16, sr=16000)[0]
    print(f"{n:02d} {m.SONGS[n]['titulo']}: dur={dur:.1f}s similaridade={r:.2f} bpm≈{float(bpm):.0f} | {t[:110]}")
