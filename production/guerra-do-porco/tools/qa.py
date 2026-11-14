#!/usr/bin/env python3
"""QA automático: formato, frames pretos/congelados, paleta, legendas, sincronia voz×timestamps, loudness."""
import json, os, re, subprocess, sys, colorsys, wave
import numpy as np
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
video = sys.argv[1]; tag = sys.argv[2] if len(sys.argv) > 2 else "qa"
exp = sys.argv[3] if len(sys.argv) > 3 else None   # "WxH@fps"
R = {"video": video, "checks": []}
def chk(name, ok, detail=""): R["checks"].append({"name": name, "pass": bool(ok), "detail": detail}); print(("PASS" if ok else "FAIL"), name, detail)
def run(c): return subprocess.run(c, capture_output=True, text=True)
D = json.load(open(f"{ROOT}/script/word-timings.json")); P = json.load(open(f"{ROOT}/production.json"))
pr = json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", video]).stdout)
vs = next(s for s in pr["streams"] if s["codec_type"] == "video"); au = next((s for s in pr["streams"] if s["codec_type"] == "audio"), None)
num, den = map(int, vs["r_frame_rate"].split("/")); fps = num / den; dur = float(pr["format"]["duration"])
if exp: ew, eh, ef = re.match(r"(\d+)x(\d+)@(\d+)", exp).groups(); chk("resolução/fps", (vs["width"], vs["height"], round(fps)) == (int(ew), int(eh), int(ef)), f"{vs['width']}x{vs['height']}@{fps:g}")
chk("duração ≈ manifesto", abs(dur - P["durationSeconds"]) < 0.25, f"{dur:.2f}s vs {P['durationSeconds']:.2f}s")
chk("proporção 9:16", abs(vs["width"] / vs["height"] - 9 / 16) < 0.01)
chk("faixa de áudio presente", au is not None, au["codec_name"] if au else "")
# pretos / congelados
bd = run(["ffmpeg", "-nostats", "-i", video, "-vf", "blackdetect=d=0.08:pix_th=0.12", "-an", "-f", "null", "-"]).stderr
blk = re.findall(r"black_start:([\d.]+)", bd); chk("sem frames pretos", len(blk) == 0, f"{len(blk)} trechos")
fz = run(["ffmpeg", "-nostats", "-i", video, "-vf", "freezedetect=n=-55dB:d=0.8", "-an", "-f", "null", "-"]).stderr
fzs = re.findall(r"freeze_start: ([\d.]+)", fz); chk("sem congelamento >0.8s", len(fzs) == 0, f"{len(fzs)} trechos {fzs[:4]}")
# paleta (frames 1/s, fora da faixa de legenda)
os.makedirs(f"/tmp/claude-0/qa_{tag}", exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", "fps=1,scale=180:320", f"/tmp/claude-0/qa_{tag}/f%03d.png"])
frames = sorted(f for f in os.listdir(f"/tmp/claude-0/qa_{tag}") if f.endswith(".png"))
blackpx, greenpx, warm, cool, shadow_bluepurple, shadow_total = [], [], [], [], 0, 0
for f in frames:
    a = np.asarray(Image.open(f"/tmp/claude-0/qa_{tag}/{f}").convert("RGB")).astype(np.float32) / 255
    a = np.concatenate([a[:int(320 * .64)], a[int(320 * .78):]])
    mx = a.max(2); mn = a.min(2); L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    blackpx.append(float((L < 0.05).mean()))
    d = mx - mn + 1e-6; r, g, b = a[..., 0], a[..., 1], a[..., 2]
    green = (g >= r) & (g >= b) & (d > 0.18) & (mx > 0.25); greenpx.append(float(green.mean()))
    warm.append(float(((r > b + 0.08) & (L > 0.25)).mean())); cool.append(float(((b > r + 0.05)).mean()))
    sh = L < 0.38; shadow_total += sh.sum(); shadow_bluepurple += (sh & (b >= r - 0.02) & (b > g)).sum()
R["palette"] = {"max_black_pixel_frac": round(max(blackpx), 4), "mean_green_dominant_frac": round(float(np.mean(greenpx)), 4), "max_green_frac": round(max(greenpx), 4),
                "mean_warm": round(float(np.mean(warm)), 3), "mean_cool": round(float(np.mean(cool)), 3), "shadows_blue_purple_frac": round(float(shadow_bluepurple / max(1, shadow_total)), 3)}
chk("sombras nunca pretas (L<0.05 < 6% dos pixels, exceto contorno)", max(blackpx) < 0.06, f"máx {max(blackpx):.3f}")
chk("verde nunca lidera (<12% dos pixels em qualquer frame)", max(greenpx) < 0.12, f"máx {max(greenpx):.3f} média {np.mean(greenpx):.3f}")
chk("paleta quente + fria presente", np.mean(warm) > 0.10 and np.mean(cool) > 0.10, f"quente {np.mean(warm):.2f} frio {np.mean(cool):.2f}")
chk("sombras predominantemente azul/roxo", shadow_bluepurple / max(1, shadow_total) > 0.55, f"{shadow_bluepurple / max(1, shadow_total):.2f}")
# legendas
srt = open(f"{ROOT}/renders/final.srt", encoding="utf-8").read(); blocks = [b for b in srt.strip().split("\n\n")]
tt = lambda s: (lambda h, m, x: int(h) * 3600 + int(m) * 60 + float(x.replace(",", ".")))(*s.split(":"))
prev = -1; ok = True; periods = 0
for b in blocks:
    ln = b.split("\n"); a, e = [tt(x.strip()) for x in ln[1].split("-->")]; txt = " ".join(ln[2:])
    ok &= (a >= prev - 1e-6 and e > a and e <= dur + 0.05); prev = a; periods += bool(re.search(r"[.!?]$", txt))
keep = P.get("captions", {}).get("keepPunctuation", False)
chk("SRT: tempos crescentes e dentro da duração", ok, f"{len(blocks)} cartões")
if keep: chk("legendas mantêm a pontuação do roteiro (observado no canal; config keepPunctuation)", periods >= 5, f"{periods} cartões com pontuação final")
else: chk("legendas sem ponto final", periods == 0, f"{periods} com pontuação final")
# sincronia: início de cada linha de voz × energia do áudio real
w = wave.open(f"{ROOT}/audio/voice.wav"); sr = w.getframerate(); v = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32768
hop = int(sr * 0.005); env = np.sqrt(np.convolve(v ** 2, np.ones(hop) / hop, "same"))
dev = []
for l in D["lines"]:
    fw = next(w for w in D["words"] if w["line"] == l["id"]); a = int(fw["start"] * sr); seg = env[max(0, a - int(.25 * sr)): a + int(.6 * sr)]; idx = np.argmax(seg > 0.01 * seg.max()); onset = (max(0, a - int(.25 * sr)) + idx) / sr; dev.append(onset - fw["start"])
R["sync_dev_s"] = [round(x, 3) for x in dev]
chk("sincronia voz×timestamps (desvio máx < 0.20s)", max(abs(x) for x in dev) < 0.20, f"máx {max(abs(x) for x in dev):.3f}s")
# loudness do áudio embutido
if au:
    lr = run(["ffmpeg", "-nostats", "-i", video, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr; s = lr[lr.rindex("Summary:"):]
    I = float(re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1)); TP = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", s).group(1))
    chk("loudness -14 LUFS (±0.7)", abs(I + 14) < 0.7, f"{I} LUFS"); chk("true peak ≤ -1.5 dBTP", TP <= -1.5, f"{TP} dBFS")
mr = json.load(open(f"{ROOT}/audio/mix-report.json")); chk("ducking ≈ 13 dB (11–15)", 11 <= abs(mr["ducking_db"]) <= 15, f"{mr['ducking_db']} dB"); chk("música ≈ 20 dB sob a voz (17–23)", 17 <= abs(mr["music_under_voice_db_vs_voice"]) <= 23, f"{mr['music_under_voice_db_vs_voice']} dB")
R["score_checks"] = f"{sum(c['pass'] for c in R['checks'])}/{len(R['checks'])}"
json.dump(R, open(f"{ROOT}/qa/{tag}.json", "w"), indent=1, default=float); print(R["score_checks"])
