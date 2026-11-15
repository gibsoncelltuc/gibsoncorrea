#!/usr/bin/env python3
"""Compara o vídeo final com as gravações de referência do canal (frames extraídos) e com o piloto v2: métricas objetivas + folha lado a lado.
Uso: python3 tools/fidelity_report.py renders/pilot_540.mp4 <ref_frames_dir A_*.png/B_*.png>   (frames de referência NÃO são versionados)"""
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
video, refdir = sys.argv[1], sys.argv[2]
def metrics(fr):
    res = {k: [] for k in ('laplacian_var', 'edge_density', 'colorfulness', 'sat_mean', 'val_mean', 'contrast_local', 'vignette')}
    for a in fr:
        a = np.concatenate([a[:int(648 * .62)], a[int(648 * .78):]]); L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
        lap = (-4 * L[1:-1, 1:-1] + L[:-2, 1:-1] + L[2:, 1:-1] + L[1:-1, :-2] + L[1:-1, 2:]); res['laplacian_var'].append(lap.var() * 1e3)
        gx = np.abs(L[:, 1:] - L[:, :-1])[:-1]; gy = np.abs(L[1:] - L[:-1])[:, :-1]; res['edge_density'].append((np.hypot(gx, gy) > .06).mean())
        rg = a[..., 0] - a[..., 1]; yb = .5 * (a[..., 0] + a[..., 1]) - a[..., 2]; res['colorfulness'].append(np.sqrt(rg.std() ** 2 + yb.std() ** 2) + .3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2))
        mx = a.max(2); mn = a.min(2); res['sat_mean'].append(((mx - mn) / (mx + 1e-6)).mean()); res['val_mean'].append(mx.mean())
        H, W = L.shape; res['contrast_local'].append(L[:H // 12 * 12, :W // 12 * 12].reshape(H // 12, 12, W // 12, 12).std(axis=(1, 3)).mean())
        h, w = L.shape; res['vignette'].append(L[h // 3:2 * h // 3, w // 3:2 * w // 3].mean() / (np.concatenate([L[:h // 6].ravel(), L[-h // 6:].ravel()]).mean() + 1e-6))
    return {k: round(float(np.mean(v)), 4) for k, v in res.items()}
def vframe(t):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', video, '-frames:v', '1', '-vf', 'scale=360:648', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(648, 360, 3).astype(np.float32) / 255
ref = []
for pre in 'AB':
    for k in range(8):
        i = int(round((k + .3) * 59.94)) + 1; p = os.path.join(refdir, f'{pre}_{i:03d}.png')
        if os.path.exists(p): ref.append(np.asarray(Image.open(p).convert('RGB').resize((360, 648))).astype(np.float32) / 255)
mine = [vframe(k + .3) for k in range(20)]
mr, mm = metrics(ref), metrics(mine); base = json.load(open(os.path.join(ROOT, 'qa', 'fidelity-baseline-v2.json')))['pilot_v2_threejs']
rows = ["| métrica | referência (canal) | piloto v2 (Three.js, reprovado) | **piloto v3 (Blender)** | razão v3/ref |", "|---|---:|---:|---:|---:|"]
for k in mr: rows.append(f"| {k} | {mr[k]:.4f} | {base[k]:.4f} | **{mm[k]:.4f}** | {mm[k] / mr[k]:.2f} |")
os.makedirs(os.path.join(ROOT, 'qa', '_local'), exist_ok=True)
pairs = [(ref[0], mine[0]), (ref[5], mine[9]), (ref[12], mine[13]), (ref[2], mine[17])] if len(ref) > 12 else []
if pairs:
    W, H = 360, 648; sh = Image.new('RGB', (len(pairs) * (W + 6), 2 * (H + 24)), (24, 24, 24)); d = ImageDraw.Draw(sh)
    for k, (a, b) in enumerate(pairs):
        x = k * (W + 6); sh.paste(Image.fromarray((a * 255).astype(np.uint8)), (x, 20)); sh.paste(Image.fromarray((b * 255).astype(np.uint8)), (x, H + 44)); d.text((x + 4, 4), 'REFERÊNCIA', fill=(255, 255, 255)); d.text((x + 4, H + 28), 'PILOTO v3 (Blender)', fill=(255, 200, 120))
    sh.save(os.path.join(ROOT, 'qa', '_local', 'fidelity_comparison.png'))
open(os.path.join(ROOT, 'qa', 'fidelity-report.md'), 'w', encoding='utf-8').write("# Relatório de fidelidade visual — piloto × referência do canal\n\nMétodo: frames extraídos com FFmpeg das 2 gravações de referência (8,2 s cada, 60 fps; interface do app recortada) e do vídeo final; mesmas métricas objetivas aplicadas a ambos (faixa de legenda excluída). `scripts/fidelity_metrics.py` da skill documenta o método.\n\n" + "\n".join(rows) + "\n\n**Leitura:** detalhe fino/bordas/contraste local medem a riqueza de cenário e textura (o piloto v2 estava 40–60 % abaixo); saturação/brilho medem a mood da cor. Métricas objetivas **não substituem** a comparação visual lado a lado (`qa/_local/fidelity_comparison.png`, não versionada por conter frames do canal).\n")
print("\n".join(rows))
