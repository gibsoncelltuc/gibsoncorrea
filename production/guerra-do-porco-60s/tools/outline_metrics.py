#!/usr/bin/env python3
"""Métrica objetiva do contorno de tinta dos personagens: variação da espessura da linha ao redor das cabeças/mãos brancas.
Método: máscara de preenchimento claro (cabeças) → tinta escura a ≤ 22 px do preenchimento → esqueleto (skimage) → espessura local = 2 × distância ao fundo (scipy).
Reporta p10/p50/p90 normalizados pela mediana e a razão p90/p10 (≈1 = linha uniforme; o canal tem razão alta: fino de um lado, grosso do outro).
Uso: python3 tools/outline_metrics.py nome=pasta_ou_glob [nome2=...] [--n 40]"""
import sys, os, glob, json, numpy as np
from PIL import Image
from scipy import ndimage as ndi
from skimage.morphology import skeletonize
def frame_metric(path, W=540):
    im = Image.open(path).convert('RGB'); H = int(im.size[1] * W / im.size[0]); a = np.asarray(im.resize((W, H), Image.LANCZOS)).astype(np.float32) / 255
    L = a.mean(2); mx = a.max(2); mn = a.min(2); sat = (mx - mn) / (mx + 1e-6)
    fill = (L > 0.80) & (sat < 0.28)                                    # branco-lavanda da cabeça
    fill = ndi.binary_opening(fill, iterations=2); lab, n = ndi.label(fill)
    if n == 0: return None
    sizes = ndi.sum(fill, lab, range(1, n + 1)); big = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 1800])   # cabeças (grandes)
    if big.sum() == 0: return None
    near = ndi.binary_dilation(big, iterations=22)
    ink = (L < 0.20) & near & ~big; ink = ndi.binary_closing(ink, iterations=1)
    if ink.sum() < 200: return None
    sk = skeletonize(ink); dt = ndi.distance_transform_edt(ink); t = 2 * dt[sk]; t = t[t > 1.5]
    return t if len(t) > 80 else None
def collect(spec, n):
    files = sorted(glob.glob(spec) if not os.path.isdir(spec) else glob.glob(os.path.join(spec, '**', '*.png'), recursive=True))
    step = max(1, len(files) // n); allt = []
    for f in files[::step][:n * 3]:
        t = frame_metric(f)
        if t is not None: allt.append(t / np.median(t))
        if len(allt) >= n: break
    return allt
if __name__ == '__main__':
    n = int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else 40; out = {}
    for arg in [a for a in sys.argv[1:] if '=' in a]:
        nm, spec = arg.split('=', 1); ts = collect(spec, n)
        if not ts: print(nm, ': sem quadros válidos'); continue
        per = [np.percentile(t, 90) / max(np.percentile(t, 10), 1e-6) for t in ts]; allt = np.concatenate(ts)
        out[nm] = dict(quadros=len(ts), razao_p90_p10_mediana=round(float(np.median(per)), 2), cv=round(float(allt.std() / allt.mean()), 3), p10=round(float(np.percentile(allt, 10)), 2), p90=round(float(np.percentile(allt, 90)), 2))
        print(nm, out[nm])
    json.dump(out, open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'qa', 'outline-metrics.json'), 'w'), indent=1, ensure_ascii=False)
