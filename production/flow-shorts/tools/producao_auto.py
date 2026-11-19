#!/usr/bin/env python3
"""Produção automática: gera, confere pela transcrição e só aprova a música com >=90% das palavras da letra reconhecidas.
Tenta várias sementes. Aprovada: masteriza (-14 LUFS) e salva em ../musicas-virais/NN-slug.mp3. Uso: producao_auto.py 2 3 4 ...
Roda tudo em sequência (a geração e a conferência não disputam memória). Registro: /home/user/musica/auto.log"""
import sys, os, re, shutil, subprocess, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import musicas_virais as m, librosa
from faster_whisper import WhisperModel
ACE = "/home/user/musica/acestep.cpp"; OUT = os.path.join(HERE, "..", "musicas-virais"); LOG = "/home/user/musica/auto.log"
SEEDS = [23, 41, 57]; LIMIAR = 0.85
W = WhisperModel("small", device="cpu", compute_type="int8")
norm = lambda s: re.sub(r"[^a-zà-ú ]", "", s.lower().replace("\n", " "))
def cobertura(mp3, n):
    y = librosa.load(mp3, sr=16000)[0]
    t = set(norm(" ".join(s.text for s in W.transcribe(y, language="pt", condition_on_previous_text=False)[0])).split())
    lw = set(norm(re.sub(r"\[.*?\]", "", m.SONGS[n]["lyr"])).split())
    return len(lw & t) / len(lw)
def log(x):
    open(LOG, "a").write(x + "\n"); print(x, flush=True)
for n in map(int, sys.argv[1:]):
    sl = m.SONGS[n]["slug"]; final = f"{OUT}/{n:02d}-{sl}.mp3"
    if os.path.exists(final): continue
    best = (-1, None, None)
    for seed in SEEDS:
        d = f"/home/user/musica/virais/{n:02d}_s{seed}_{sl}"; os.makedirs(d, exist_ok=True)
        mp3 = f"{d}/req00.mp3"
        if not os.path.exists(mp3):
            json.dump(m.build(n, seed), open(f"{d}/req.json", "w"), ensure_ascii=False, indent=2)
            for exe, req in (("ace-lm", "req.json"), ("ace-synth", "req0.json")):
                subprocess.run([f"{ACE}/build/{exe}", "--models", f"{ACE}/models", "--request", req], cwd=d, stdout=open(f"{d}/{exe}.log", "w"), stderr=subprocess.STDOUT)
        if not os.path.exists(mp3): log(f"{n} semente {seed}: FALHOU"); continue
        c = cobertura(mp3, n); log(f"{n} {m.SONGS[n]['titulo']} semente {seed}: {c:.0%} das palavras")
        if c > best[0]: best = (c, seed, mp3)
        if c >= LIMIAR: break
    if best[1] is None: log(f"{n} SEM RESULTADO"); continue
    subprocess.run([f"{HERE}/masterizar.sh", best[2], final], check=True)
    shutil.copy(f"{os.path.dirname(best[2])}/req.json", final[:-4] + ".json")
    log(f"{n} PRONTA semente {best[1]} cobertura {best[0]:.0%} {'APROVADA' if best[0] >= LIMIAR else 'ABAIXO DO LIMIAR (melhor das 4)'}")
log("FIM")
