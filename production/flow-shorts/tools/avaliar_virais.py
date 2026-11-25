#!/usr/bin/env python3
"""Avaliador: 'ouve' cada música e dá notas. Uso: avaliar_virais.py <n> [arquivo.mp3]
Mede: (1) letra por transcrição Whisper, (2) Audiobox Aesthetics da Meta (CE prazer, CU utilidade, PC complexidade, PQ qualidade de produção, 1-10),
(3) andamento, (4) volume LUFS e pico. Roda UMA música por vez (a geração usa a memória)."""
import sys, os, re, glob, difflib, subprocess, tempfile
sys.path.insert(0, os.path.dirname(__file__))
import musicas_virais as m, librosa, numpy as np, pyloudnorm as pln, soundfile as sf, torch, torchaudio
n = int(sys.argv[1]); D = os.path.join(os.path.dirname(__file__), "..", "musicas-virais")
f = sys.argv[2] if len(sys.argv) > 2 else glob.glob(f"{D}/{n:02d}-*.mp3")[0]
wav = tempfile.mktemp(suffix=".wav"); subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f, "-ar", "48000", wav], check=True)
y16 = librosa.load(f, sr=16000)[0]
from faster_whisper import WhisperModel
norm = lambda s: re.sub(r"[^a-zà-ú ]", "", s.lower().replace("\n", " "))
segs, _ = WhisperModel("small", device="cpu", compute_type="int8").transcribe(y16, language="pt", condition_on_previous_text=False)
t = norm(" ".join(s.text for s in segs)); lyr = norm(re.sub(r"\[.*?\]", "", m.SONGS[n]["lyr"]))
# cobertura: fração das palavras da letra (únicas) que apareceram na transcrição
lw = set(lyr.split()); cob = len(lw & set(t.split())) / len(lw)
y, sr = sf.read(wav, dtype="float32"); lufs = pln.Meter(sr).integrated_loudness(y); pico = 20 * np.log10(np.abs(y).max())
bpm = float(librosa.feature.tempo(y=y16, sr=16000)[0])
def _load(path, *a, **k):
    x, r = sf.read(path, dtype="float32", always_2d=True); return torch.from_numpy(x.T.copy()), r
class _I:
    def __init__(s, r): s.sample_rate = r
torchaudio.load = _load; torchaudio.info = lambda p: _I(sf.info(p).samplerate)
from audiobox_aesthetics.infer import initialize_predictor
a = initialize_predictor().forward([{"path": wav}])[0]
print(f"{n:02d} {m.SONGS[n]['titulo']} | palavras da letra reconhecidas {cob:.0%} | LUFS {lufs:.1f} pico {pico:.1f} dB | bpm {bpm:.0f} (pedido {m.SONGS[n]['bpm']}) | "
      f"prazer {a['CE']:.1f} utilidade {a['CU']:.1f} complexidade {a['PC']:.1f} produção {a['PQ']:.1f}")
os.remove(wav)
