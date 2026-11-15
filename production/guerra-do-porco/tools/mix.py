#!/usr/bin/env python3
"""Mixagem: ganhos por LUFS, ducking sidechain (~13 dB), loudnorm two-pass -14 LUFS / TP -1.5 dB, alimiter."""
import json, os, re, subprocess, sys
import numpy as np, wave
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); A = f"{ROOT}/audio"
def sh(cmd): return subprocess.run(cmd, capture_output=True, text=True)
def lufs(path):
    r = sh(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r); return float(m[-1])
DUCK_DB = float(os.environ.get("DUCK_DB", 13.5))
def ducked_music(g_music_db):
    """música com ducking por envelope: -DUCK_DB dB nas janelas de fala (palavras ±), ataque 60 ms / soltura 350 ms — determinístico e independente do nível da voz"""
    from scipy.signal import fftconvolve
    w = wave.open(f"{A}/music.wav"); sr = w.getframerate(); ch = w.getnchannels(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64).reshape(-1, ch) / 32768
    T = json.load(open(f"{ROOT}/script/word-timings.json")); m = np.zeros(len(x))
    for wd in T["words"]: m[max(0, int((wd["start"] - .12) * sr)):int((wd["end"] + .30) * sr)] = 1.0
    up = np.exp(-np.arange(int(.06 * sr)) / (.06 * sr / 3)); up /= up.sum(); dn = np.exp(-np.arange(int(.35 * sr)) / (.35 * sr / 3)); dn /= dn.sum()
    a = fftconvolve(m, up)[:len(m)]; r = fftconvolve(m, dn)[:len(m)]; env = np.maximum(a, r)                      # sobe rápido, solta devagar
    gain = 10 ** (-DUCK_DB * env / 20) * 10 ** (g_music_db / 20); y = x * gain[:, None]
    out = f"{A}/music_ducked_env.wav"; wo = wave.open(out, "wb"); wo.setnchannels(ch); wo.setsampwidth(2); wo.setframerate(sr); wo.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()); wo.close(); return out
LV = {n: lufs(f"{A}/{n}.wav") for n in ("voice", "music", "sfx", "ambience")}
print("LUFS stems:", LV)
# alvo relativo à voz: música-bed -8 LU (sem voz), ducking ~13 dB sob a voz ⇒ ≈ -21 dB sob a fala; sfx -7 LU; ambiência -24 LU
g = {"voice": 0.0, "music": (LV["voice"] - 8) - LV["music"], "sfx": (LV["voice"] - 7) - LV["sfx"], "ambience": (LV["voice"] - 24) - LV["ambience"]}
print("ganhos dB:", {k: round(v, 1) for k, v in g.items()})
fc = (
 f"[0:a]highpass=f=70,acompressor=threshold=0.1:ratio=2.5:attack=8:release=120,volume={g['voice']}dB[vo];"
 f"[1:a]anull[mud];"
 f"[2:a]volume={g['sfx']}dB[sf];[3:a]volume={g['ambience']}dB[am];"
 f"[vo][mud][sf][am]amix=inputs=4:normalize=0:duration=longest[mix]"
)
ins = []
MD = ducked_music(g["music"])
for n in ("voice", "music", "sfx", "ambience"): ins += ["-i", MD if n == "music" else f"{A}/{n}.wav"]
subprocess.run(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", fc, "-map", "[mix]", "-ar", "44100", f"{A}/premix.wav"], check=True)
# ducked music stem (para QA)
import shutil; shutil.copy(MD, f"{A}/music_ducked.wav")
# loudnorm two-pass
t = "I=-14:TP=-1.5:LRA=11"
r = sh(["ffmpeg", "-nostats", "-i", f"{A}/premix.wav", "-af", f"loudnorm={t}:print_format=json", "-f", "null", "-"]).stderr
j = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
ln = f"loudnorm={t}:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{A}/premix.wav", "-af", f"{ln},alimiter=limit=0.84:level=false,aformat=channel_layouts=stereo", "-ar", "44100", f"{A}/final_mix.wav"], check=True)
def meas(p):
    r = sh(["ffmpeg", "-nostats", "-i", p, "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr; summ = r[r.rindex("Summary:"):]
    return float(re.search(r"I:\s+(-?[\d.]+) LUFS", summ).group(1)), float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ).group(1))
I, TP = meas(f"{A}/final_mix.wav")
for _ in range(2):                                   # correção fina: leva a −14,0 LUFS usando a folga de pico (limite −1,5 dBTP)
    if abs(I + 14) < .15: break
    adj = min(-14 - I, (-1.6 - TP) if -14 - I > 0 else 99)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{A}/final_mix.wav", "-af", f"volume={adj}dB,alimiter=limit=0.84:level=false", "-ar", "44100", f"{A}/final_mix_adj.wav"], check=True); os.replace(f"{A}/final_mix_adj.wav", f"{A}/final_mix.wav"); I, TP = meas(f"{A}/final_mix.wav")
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
m0, _ = rd(f"{A}/music.wav"); m0 = m0 * 10 ** (g["music"] / 20); m0 = m0[:, 0] if m0.ndim > 1 else m0
m0r = np.sqrt(np.mean(np.concatenate([m0[int(w["start"] * sr):int(w["end"] * sr)] for w in T["words"]]) ** 2))
res["ducking_db"] = round(20 * np.log10(mrms / m0r), 1)
json.dump(res, open(f"{ROOT}/audio/mix-report.json", "w"), indent=1); print(res)
