#!/usr/bin/env python3
"""QA extra do piloto: câmera sempre em movimento, sem cortes secos fora de dissolves/tiros, gancho 9–14 palavras, eco do loop."""
import json, os, re, subprocess, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
video = sys.argv[1]; tag = sys.argv[2] if len(sys.argv) > 2 else "extra"
D = json.load(open(f"{ROOT}/script/word-timings.json")); shots = json.load(open(f"{ROOT}/storyboard/shots.json"))["shots"]; story = json.load(open(f"{ROOT}/script/story.json"))
R = {"checks": []}
def chk(n, ok, d=""): R["checks"].append({"name": n, "pass": bool(ok), "detail": d}); print(("PASS" if ok else "FAIL"), n, d)
pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of", "json", video], capture_output=True, text=True).stdout)
num, den = map(int, pr["streams"][0]["r_frame_rate"].split("/")); fps = num / den
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-vf", "scale=72:128,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
F = np.frombuffer(raw, np.uint8).reshape(-1, 128, 72).astype(np.float32)
t_of = lambda i: i / fps
# 1) movimento de câmera por plano (diferença média entre quadros separados por 0.4 s)
lag = max(1, int(round(0.4 * fps))); mot = {}
for s in shots:
    a, b = int((s["start"] + 0.35) * fps), int((s["end"] - 0.25) * fps)
    if b - a <= lag: continue
    d = [np.abs(F[i + lag] - F[i]).mean() for i in range(a, b - lag)]; mot[s["id"]] = (float(np.mean(d)), float(np.min(d)))
R["motion"] = {k: [round(v[0], 2), round(v[1], 2)] for k, v in mot.items()}
chk("câmera sempre em movimento (média ≥ 1.2 em todos os planos)", all(v[0] >= 1.2 for v in mot.values()), str(R["motion"]))
# 2) cortes secos: salto entre quadros consecutivos fora de dissolve/tiro
bangs = []
n = lambda s: re.sub(r"[^\w]", "", s.lower())
for line, pre in (("L1", "matou"), ("L2", "atirou")): bangs.append(next(w["start"] for w in D["words"] if w["line"] == line and n(w["text"]).startswith(n(pre))) + 0.1)
bad = []; J = np.array([np.abs(F[i] - F[i - 1]).mean() for i in range(1, len(F))])
for i in range(len(J)):
    t = t_of(i + 1); loc = np.median(np.concatenate([J[max(0, i - 6):i], J[i + 1:i + 7]])) if len(J) > 8 else 0
    if J[i] > 20 and J[i] > 3 * max(loc, 1.0) and not any(-0.1 <= t - b <= 0.45 for b in bangs): bad.append((round(t, 2), round(float(J[i]), 1)))
R["jump_stats"] = {"mean": round(float(J.mean()), 2), "p90": round(float(np.percentile(J, 90)), 2), "max": round(float(J.max()), 2), "frac_gt14": round(float((J > 14).mean()), 3)}
chk("sem cortes secos (SPIKE isolado: salto > 20 e ≥ 3× a mediana local) fora de tiros — movimento rápido sustentado é permitido (prints: 16–22 % dos quadros com salto > 14)", len(bad) == 0, f"{len(bad)} spikes {bad[:6]} | saltos: {R['jump_stats']}")
# 3) gancho 9–14 palavras
hook = len(re.findall(r"\w+", story["lines"][0]["text"])); chk("gancho com 9–14 palavras", 9 <= hook <= 14, f"{hook} palavras")
# 4) eco do loop (primeiro × último quadro, histograma equalizado)
def eq(x): h, _ = np.histogram(x, 256, (0, 255)); c = h.cumsum() / h.sum(); return np.interp(x, np.arange(256), c * 255)
loop = float(np.abs(eq(F[0]) - eq(F[-1])).mean()); R["loop_mad"] = round(loop, 2)
rnd = float(np.abs(eq(F[0]) - eq(F[len(F) // 2])).mean()); R["loop_vs_mid"] = round(rnd, 2)
chk("último quadro ecoa o primeiro (mais parecido que um quadro do meio)", loop < rnd, f"loop {loop:.1f} vs meio {rnd:.1f}")
R["score_checks"] = f"{sum(c['pass'] for c in R['checks'])}/{len(R['checks'])}"
os.makedirs(f"{ROOT}/qa", exist_ok=True); json.dump(R, open(f"{ROOT}/qa/{tag}.json", "w"), indent=1); print(R["score_checks"])
