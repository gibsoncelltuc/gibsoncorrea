#!/usr/bin/env python3
"""Mixagem: ganhos por LUFS, ducking sidechain (~13 dB), loudnorm two-pass -14 LUFS / TP -1.5 dB, alimiter."""
import json, os, re, subprocess, sys
import numpy as np, wave
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); A = f"{ROOT}/audio"
def sh(cmd): return subprocess.run(cmd, capture_output=True, text=True)
def lufs(path):
    r = sh(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r); return float(m[-1])
LV = {n: lufs(f"{A}/{n}.wav") for n in ("voice", "music", "sfx", "ambience")}
print("LUFS stems:", LV)
# alvo relativo à voz: música-bed -8 LU (sem voz), ducking ~13 dB sob a voz ⇒ ≈ -21 dB sob a fala; sfx -7 LU; ambiência -24 LU
g = {"voice": 0.0, "music": (LV["voice"] - 8) - LV["music"], "sfx": (LV["voice"] - 7) - LV["sfx"], "ambience": (LV["voice"] - 24) - LV["ambience"]}
print("ganhos dB:", {k: round(v, 1) for k, v in g.items()})
fc = (
 f"[0:a]highpass=f=70,acompressor=threshold=0.1:ratio=2.5:attack=8:release=120,volume={g['voice']}dB,asplit=2[vo][vsc];"
 f"[1:a]volume={g['music']}dB[mu];[mu][vsc]sidechaincompress=threshold=0.015:ratio=9:attack=15:release=420:makeup=1[mud];"
 f"[2:a]volume={g['sfx']}dB[sf];[3:a]volume={g['ambience']}dB[am];"
 f"[vo][mud][sf][am]amix=inputs=4:normalize=0:duration=longest[mix]"
)
ins = []
for n in ("voice", "music", "sfx", "ambience"): ins += ["-i", f"{A}/{n}.wav"]
subprocess.run(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", fc, "-map", "[mix]", "-ar", "44100", f"{A}/premix.wav"], check=True)
# ducked music stem (para QA)
fc2 = f"[1:a]volume={g['music']}dB[mu];[0:a]volume={g['voice']}dB[vsc];[mu][vsc]sidechaincompress=threshold=0.015:ratio=9:attack=15:release=420:makeup=1[o]"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{A}/voice.wav", "-i", f"{A}/music.wav", "-filter_complex", fc2, "-map", "[o]", f"{A}/music_ducked.wav"], check=True)
# loudnorm two-pass
t = "I=-14:TP=-1.5:LRA=11"
r = sh(["ffmpeg", "-nostats", "-i", f"{A}/premix.wav", "-af", f"loudnorm={t}:print_format=json", "-f", "null", "-"]).stderr
j = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
ln = f"loudnorm={t}:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{A}/premix.wav", "-af", f"{ln},alimiter=limit=0.84:level=false,aformat=channel_layouts=stereo", "-ar", "44100", f"{A}/final_mix.wav"], check=True)
r = sh(["ffmpeg", "-nostats", "-i", f"{A}/final_mix.wav", "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
summ = r[r.rindex("Summary:"):]
I = float(re.search(r"I:\s+(-?[\d.]+) LUFS", summ).group(1)); TP = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ).group(1))
# música sob voz vs voz (RMS em janelas de palavras)
def rd(p):
    w = wave.open(p); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32768; return x, w.getframerate()
v, sr = rd(f"{A}/voice.wav"); m, _ = rd(f"{A}/music_ducked.wav")
T = json.load(open(f"{ROOT}/script/word-timings.json"))
vs, ms = [], []
for w in T["words"]:
    a, b = int(w["start"] * sr), int(w["end"] * sr); vs.append(v[a:b]); ms.append(m[a:min(b, len(m))])
vrms = np.sqrt(np.mean(np.concatenate(vs) ** 2)); mrms = np.sqrt(np.mean(np.concatenate(ms) ** 2))
res = {"integrated_lufs": I, "true_peak_dbfs": TP, "stem_lufs": LV, "gains_db": g,
       "music_under_voice_db_vs_voice": round(20 * np.log10(mrms / vrms), 1)}
# ducking real: música sem ducking vs com ducking nas janelas de voz
m0, _ = rd(f"{A}/music.wav"); m0 = m0 * 10 ** (g["music"] / 20)
m0r = np.sqrt(np.mean(np.concatenate([m0[int(w["start"] * sr):int(w["end"] * sr)] for w in T["words"]]) ** 2))
res["ducking_db"] = round(20 * np.log10(mrms / m0r), 1)
json.dump(res, open(f"{ROOT}/audio/mix-report.json", "w"), indent=1); print(res)
