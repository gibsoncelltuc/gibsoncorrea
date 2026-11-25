#!/usr/bin/env python3
"""Alinha a letra ao áudio: tempo de cada palavra cantada. Uso: alinhar_musica.py N  -> grava ../musicas-virais/tempos/NN.json
Transcreve com Whisper (palavra a palavra), casa com a letra (difflib) e interpola o que a transcrição errou."""
import sys, os, re, json, glob, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import musicas_virais as m, librosa
from faster_whisper import WhisperModel
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "musicas-virais")
norm = lambda w: re.sub(r"[^a-zà-ú]", "", w.lower())

def lyric_words(n):
    out = []; li = 0
    for sec in re.split(r"\n\n", m.SONGS[n]["lyr"]):
        lines = sec.strip().split("\n"); tag = re.match(r"\[(.*?)\]", lines[0]).group(1)
        for line in lines[1:]:
            for w in re.split(r"[\s\-]+", line):
                if norm(w): out.append(dict(w=w.strip(",.!?;:"), n=norm(w), line=li, sec=tag))
            li += 1
    return out

def alinhar(n):
    f = glob.glob(f"{D}/{n:02d}-*.mp3")[0]; y = librosa.load(f, sr=16000)[0]; dur = len(y) / 16000
    segs, _ = WhisperModel("small", device="cpu", compute_type="int8").transcribe(y, language="pt", word_timestamps=True, condition_on_previous_text=False)
    W = [(norm(w.word), w.start, w.end) for s in segs for w in s.words if norm(w.word)]
    L = lyric_words(n)
    mb = difflib.SequenceMatcher(None, [x["n"] for x in L], [w[0] for w in W], autojunk=False).get_matching_blocks()
    for a, b, size in mb:
        for k in range(size): L[a + k]["t0"], L[a + k]["t1"] = W[b + k][1], W[b + k][2]; L[a + k]["ok"] = True
    ok = [i for i, x in enumerate(L) if x.get("ok")]
    # interpola o que não casou entre âncoras
    anc = [(-1, 0.0, 0.0)] + [(i, L[i]["t0"], L[i]["t1"]) for i in ok] + [(len(L), dur, dur)]
    for (i0, _, e0), (i1, s1, _) in zip(anc, anc[1:]):
        gap = list(range(i0 + 1, i1))
        if not gap: continue
        step = (s1 - e0) / len(gap)
        for k, i in enumerate(gap): L[i]["t0"] = e0 + k * step; L[i]["t1"] = e0 + (k + 1) * step; L[i]["ok"] = False
    cov = len(ok) / len(L)
    return dict(song=n, titulo=m.SONGS[n]["titulo"], dur=dur, bpm_pedido=m.SONGS[n]["bpm"], cobertura=cov,
                palavras=[dict(w=x["w"], t0=round(x["t0"], 2), t1=round(x["t1"], 2), line=x["line"], sec=x["sec"], medido=x["ok"]) for x in L])

if __name__ == "__main__":
    os.makedirs(f"{D}/tempos", exist_ok=True)
    for n in map(int, sys.argv[1:]):
        r = alinhar(n); json.dump(r, open(f"{D}/tempos/{n:02d}.json", "w"), ensure_ascii=False, indent=1)
        print(n, r["titulo"], f"dur {r['dur']:.1f}s, {r['cobertura']:.0%} das palavras com tempo medido")
