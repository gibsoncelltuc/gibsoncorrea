#!/usr/bin/env python3
# Comparativo lado a lado com o canal de referencia: python3 comparar.py <id> [<id2>...]
#  -> out/comparativo_<id>.jpg (em cima: quadros reais do canal; embaixo: nosso video) + tabela de medidas no terminal.
import sys, glob, subprocess, os, numpy as np
from PIL import Image
def metr(im):
    a = np.asarray(im.convert('RGB').resize((270, 480)), dtype=np.float32) / 255
    mx, mn = a.max(2), a.min(2); lum = a @ np.array([.299, .587, .114], dtype=np.float32)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    gx = np.abs(np.diff(lum, axis=1)).mean(); gy = np.abs(np.diff(lum, axis=0)).mean()
    b = lum[::, ::]; noise = np.abs(b[1:-1, 1:-1] - (b[:-2, 1:-1] + b[2:, 1:-1] + b[1:-1, :-2] + b[1:-1, 2:]) / 4); flat = noise[noise < 0.02].mean()
    return dict(lum=lum.mean(), contraste=lum.std(), sat=sat.mean(), escuros=(lum < 0.12).mean() * 100, claros=(lum > 0.9).mean() * 100, nitidez=(gx + gy) / 2, ruido=flat * 100)
ref = sorted(glob.glob('ref_privado/yt/v/*/oar2.jpg'))
R = [metr(Image.open(f)) for f in ref]
keys = list(R[0]); avg = lambda L, k: float(np.mean([x[k] for x in L])); sd = lambda L, k: float(np.std([x[k] for x in L]))
for vid in sys.argv[1:]:
    mp4 = [f for f in glob.glob(f'out/{vid}/*.mp4') if 'preview' not in f][0]
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mp4]))
    os.makedirs('tmp/cmp', exist_ok=True); ours = []
    for i in range(12):
        o = f'tmp/cmp/{vid}_{i}.jpg'; subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{dur * (i + 0.5) / 12:.2f}', '-i', mp4, '-frames:v', '1', '-q:v', '3', o]); ours.append(Image.open(o))
    O = [metr(i) for i in ours]
    print(f'\n== {vid}  ({len(ref)} quadros do canal x 12 quadros nossos)\n{"medida":10s} {"canal":>8s} {"faixa canal":>15s} {"nosso":>8s}  situacao')
    for k in keys:
        a, s, o = avg(R, k), sd(R, k), avg(O, k); ok = abs(o - a) <= max(1.5 * s, 0.1 * abs(a))
        print(f'{k:10s} {a:8.3f} {a - s:7.3f}-{a + s:7.3f} {o:8.3f}  {"igual" if ok else "DIFERENTE"}')
    W, H = 270, 480; S = Image.new('RGB', (W * 6, H * 4), '#111')
    pick = [ref[int(i * len(ref) / 12)] for i in range(12)]
    for i, f in enumerate(pick): S.paste(Image.open(f).convert('RGB').resize((W, H)), ((i % 6) * W, (i // 6) * H))
    for i, im in enumerate(ours): S.paste(im.convert('RGB').resize((W, H)), ((i % 6) * W, (2 + i // 6) * H))
    S.save(f'out/comparativo_{vid}.jpg', quality=88); print(f'out/comparativo_{vid}.jpg  (2 linhas de cima = canal, 2 de baixo = nosso)')
