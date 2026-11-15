#!/usr/bin/env python3
"""ETAPA A do portão: verificação QUADRO A QUADRO. Cada PNG renderizado é lido e medido; o quadro só conta como CONCLUÍDO se passar. Reprovados vão para qa/frames-status.json
com o motivo, e `tools/repair_frames.py` refaz SÓ eles (nunca a sequência inteira). Medidas por quadro (miniatura 135×240): arquivo legível/tamanho, luminância média e contraste,
pretos esmagados, saturação, domínio do verde, nitidez (Laplaciano), presença de tinta (contorno), mudança em relação ao quadro anterior da MESMA edição (pop/flicker/congelado) e
desvio de brilho/saturação em relação à mediana da edição. Uso: python3 tools/frame_gate.py [pasta_frames=blender/out/frames] [--only edição,...]"""
import glob, json, os, re, sys
import numpy as np
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); root = next((a for a in sys.argv[1:] if not a.startswith('--')), f'{R}/blender/out/frames')
only = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else None
def feats(p):
    sz = os.path.getsize(p)
    try: im = Image.open(p).convert('RGB'); im.load()
    except Exception as ex: return dict(err=f'ilegível: {ex.__class__.__name__}', size=sz)
    a = np.asarray(im.resize((135, 240), Image.BOX), np.float32) / 255; mx = a.max(2); mn = a.min(2); L = a @ np.array([.2126, .7152, .0722], np.float32); sat = np.where(mx > 1e-4, (mx - mn) / np.maximum(mx, 1e-4), 0)
    g = L; lap = g[1:-1, 1:-1] * -4 + g[:-2, 1:-1] + g[2:, 1:-1] + g[1:-1, :-2] + g[1:-1, 2:]
    r, gg, b = a[..., 0], a[..., 1], a[..., 2]; green = ((gg > r * 1.08) & (gg > b * 1.15) & (sat > .3)).mean()
    ink = ((L < .16) & (sat < .6)).mean()
    return dict(size=sz, lum=float(L.mean()), std=float(L.std()), crushed=float((L < .03).mean()), sat=float(sat.mean()), green=float(green), sharp=float(lap.var()), ink=float(ink), thumb=L)
rows = []; status = {}; bad_total = 0; total = 0
EV = [e['t'] for e in json.load(open(f'{R}/audio/sfx-events.json')) if e['kind'] in ('gun', 'ding', 'thud', 'whoosh', 'rise', 'rustle')] if os.path.exists(f'{R}/audio/sfx-events.json') else []   # impactos INTENCIONAIS (tiro, corte): pops aqui são ação, não defeito
for d in sorted(glob.glob(f'{root}/*')):
    eid = os.path.basename(d)
    if only and eid not in only: continue
    files = sorted(glob.glob(f'{d}/f*.png')); F = [(f, feats(f)) for f in files]; ok = [x for _, x in F if 'err' not in x]
    if not ok: continue
    med = {k: float(np.median([x[k] for x in ok])) for k in ('lum', 'sat', 'sharp', 'size')}; prev = None
    th = [x.get('thumb') for _, x in F]; dser = [None] + [float(np.abs(th[i] - th[i - 1]).mean()) if th[i] is not None and th[i - 1] is not None else None for i in range(1, len(F))]
    inks = [x.get('ink') for _, x in F]
    def loc(arr, i, w=6):
        v = [a for a in arr[max(0, i - w):i + w + 1] if a is not None]; return float(np.median(v)) if v else 0.0
    for i_, (f, x) in enumerate(F):
        n = int(re.search(r'f(\d+)\.png', f).group(1)); why = []; total += 1
        if 'err' in x: why.append(x['err'])
        else:
            if x['size'] < 0.35 * med['size']: why.append(f"arquivo pequeno demais ({x['size'] // 1024} KB vs mediana {int(med['size']) // 1024} KB: quadro vazio/truncado)")
            if not .06 < x['lum'] < .93: why.append(f"brilho fora da faixa ({x['lum']:.2f})")
            if x['std'] < .035: why.append(f"sem contraste (desvio {x['std']:.3f})")
            if x['crushed'] > .06: why.append(f"pretos esmagados ({x['crushed']:.1%} dos pixels < 3 %)")
            if not .12 < x['sat'] < .85: why.append(f"saturação fora da faixa ({x['sat']:.2f})")
            if x['green'] > .30: why.append(f"verde domina ({x['green']:.0%})")
            if x['ink'] > .40: why.append(f"tinta demais ({x['ink']:.0%})")
            if x['sharp'] < .12 * med['sharp']: why.append("borrado (nitidez < 12 % da mediana da edição)")
            if abs(x['lum'] - med['lum']) > .22 * max(med['lum'], .2) + .06: why.append(f"flicker de brilho ({x['lum']:.2f} vs mediana {med['lum']:.2f})")
            if abs(x['sat'] - med['sat']) > .5 * med['sat']: why.append(f"flicker de cor (sat {x['sat']:.2f} vs {med['sat']:.2f})")
            if dser[i_] is not None and not any(abs(n / 30 - te) < .14 for te in EV) and dser[i_] > max(.12, 3.5 * loc(dser, i_)): why.append(f"pop isolado em relação ao quadro anterior (Δ={dser[i_]:.2f} vs vizinhos {loc(dser, i_):.2f})")
            if x['ink'] < .004 and loc(inks, i_) > .02: why.append(f"personagem some só neste quadro (tinta {x['ink']:.1%} vs vizinhos {loc(inks, i_):.1%})")
            if i_ > 0 and dser[i_] is not None and dser[i_] < .0005 and 'thumb' in x: why.append("quadro idêntico ao anterior (congelado/duplicado)")
            prev = x
        status[f'{eid}/f{n:04d}'] = dict(ok=not why, why=why)
        if why: bad_total += 1
json.dump(dict(total=total, reprovados=bad_total, status={k: v for k, v in status.items() if not v['ok']}, root=root), open(f'{R}/qa/frames-status.json', 'w'), ensure_ascii=False, indent=1)
bad = [(k, v['why']) for k, v in status.items() if not v['ok']]
for k, w in bad[:25]: print('FAIL', k, '—', '; '.join(w))
print(f'quadros concluídos: {total - bad_total}/{total} ({bad_total} reprovados)'); sys.exit(1 if bad_total else 0)
