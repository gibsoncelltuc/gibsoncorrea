#!/usr/bin/env python3
"""Pontua versões de música de um episódio: acerto da letra (Whisper) e encaixe nos blocos de 10 s.
Uso: escolher_musica.py <num_ep> musica1.mp3 [musica2.mp3 ...]   (precisa de faster-whisper e librosa)"""
import sys, os, re, difflib, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerar_pacote as g
import librosa
from faster_whisper import WhisperModel

def norm(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.findall(r"[a-z]+", s)

ep = next(e for e in g.EPISODES if e["num"] == int(sys.argv[1]))
intended = " ".join(f"{s['l1']} {s['l2']}" for s in ep["shots"])
m = WhisperModel("small", device="cpu", compute_type="int8")
rows = []
for f in sys.argv[2:]:
    y, _ = librosa.load(f, sr=16000)
    segs, _ = m.transcribe(y, language="pt", word_timestamps=True, condition_on_previous_text=False)
    words = [(w.word, w.start, w.end) for s in segs for w in s.words]
    heard = " ".join(w[0] for w in words)
    sim = difflib.SequenceMatcher(None, norm(intended), norm(heard)).ratio()
    # início do 1º verso de cada bloco: primeira palavra do verso procurada perto do múltiplo de 10 s
    devs = []
    for i, s in enumerate(ep["shots"]):
        first = norm(s["l1"])[0]
        cands = [w[1] for w in words if norm(w[0]) and norm(w[0])[0][:4] == first[:4] and abs(w[1] - 10 * i) < 5]
        devs.append(min((abs(c - 10 * i) for c in cands), default=5.0))
    dev = sum(devs) / len(devs)
    rows.append((sim - 0.05 * dev, f, sim, dev, devs, len(y) / 16000))
for sc, f, sim, dev, devs, d in sorted(rows, reverse=True):
    print(f"{sc:.2f}  {os.path.basename(os.path.dirname(f))}/{os.path.basename(f)}  letra={sim:.2f}  desvio médio do bloco={dev:.1f}s  por bloco={[round(x,1) for x in devs]}  dur={d:.1f}s")
