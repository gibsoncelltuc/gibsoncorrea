#!/usr/bin/env python3
"""Ficha de ambientes + paleta MEDIDA (rubrica V2 "Identidade visual": style frame, character sheet, environment sheet, paleta).
 • design/environment-sheet.png — um quadro final por cena (S1–S6) e por insert, com rótulo do cenário e a paleta dominante abaixo de cada um;
 • design/palette.json / palette.png — k-means (k=10, espaço Lab) dos quadros do vídeo FINAL × dos prints de referência (só cores, nenhum quadro de terceiros é copiado),
   com distância ΔE76 entre as duas paletas (cada cor de uma ao vizinho mais próximo da outra) e os tons-assinatura (tinta ameixa, céu, grama, pele/rosto, uniforme).
Uso: python3 tools/make_design_sheets.py [renders/pilot_540.mp4] [pasta_referencia]"""
import glob, json, os, subprocess, sys, tempfile, textwrap
TMP = os.environ.get('WORK_TMP', os.path.join(tempfile.gettempdir(), 'toon-work'))
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); V = sys.argv[1] if len(sys.argv) > 1 else 'renders/pilot_540.mp4'; REF = sys.argv[2] if len(sys.argv) > 2 else os.environ.get('REF_DIR', '')
os.makedirs(f'{R}/design', exist_ok=True); K = 10
def font(sz):
    for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'):
        if os.path.exists(p): return ImageFont.truetype(p, sz)
    return ImageFont.load_default()
def to_lab(rgb): return cv2.cvtColor(np.asarray(rgb, np.uint8).reshape(-1, 1, 3), cv2.COLOR_RGB2LAB).reshape(-1, 3).astype(np.float32)
def kmeans(frames, k=K):
    px = np.concatenate([np.asarray(Image.open(f).convert('RGB').resize((54, 96), Image.BOX)).reshape(-1, 3) for f in frames]); lab = to_lab(px)
    _, lbl, cen = cv2.kmeans(lab, k, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 40, 0.5), 3, cv2.KMEANS_PP_CENTERS); share = np.bincount(lbl.ravel(), minlength=k) / len(lbl)
    rgb = cv2.cvtColor(np.clip(cen, 0, 255).astype(np.uint8).reshape(-1, 1, 3), cv2.COLOR_LAB2RGB).reshape(-1, 3); o = np.argsort(-share)
    return [dict(hex='#%02x%02x%02x' % tuple(int(v) for v in rgb[i]), share=round(float(share[i]), 3), lab=[round(float(v), 1) for v in cen[i]]) for i in o]
def dE(a, b): return float(np.linalg.norm(np.asarray(a['lab']) - np.asarray(b['lab'])))
# ---- quadros do vídeo final por cena (usa as amostras 25/50/75 % de qa/frame-samples se existirem) ----
smp = json.load(open(f'{R}/qa/frame-samples.json')) if os.path.exists(f'{R}/qa/frame-samples.json') else None
sb = json.load(open(f'{R}/storyboard/shots.json'))['shots']; vid = f'{R}/{V}'
raw = f'{R}/renders/_montage_raw.mp4'; nocap = f'{TMP}/dsheets/nocap.mp4'; os.makedirs(f'{TMP}/dsheets', exist_ok=True)
if os.path.exists(raw):   # mesma grade do vídeo final, SEM a camada de legendas: a paleta e as fichas não contam o texto branco
    subprocess.run([sys.executable, f'{R}/blender/grade.py', raw, '-', nocap], check=True, capture_output=True); vid = nocap
def grab(t, f): subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', vid, '-frames:v', '1', f], check=True); return f
os.makedirs(f'{TMP}/dsheets', exist_ok=True); tiles = []; allf = []
LABEL = {'S1': 'S1 — fazenda dourada: horta, cabana, celeiro, frota no horizonte', 'S2a': 'S2 — cerca, placa SAN JUAN 1859, bandeira britânica', 'I_eyes': 'insert — close do Cutlar (tiro)', 'S3a': 'S3 — acampamento: barris, caixas, notas',
         'I_notes': 'insert — notas US$ 100 × US$ 10', 'S4a': 'S4 — campo: tropa de 80 soldados, bandeira, navios', 'I_faces': 'insert — três rostos da tropa', 'S4b': 'S4 — tropa e frota ao fundo', 'S5a': 'S5 — convés da fragata',
         'I_baynes': 'insert — almirante recusa', 'S6': 'S6 — túmulo do porco (loop)'}
for s in sb:
    t = (s['start'] + s['end']) / 2; f = grab(t, f"{TMP}/dsheets/{s['id']}.png"); allf.append(f); tiles.append((s['id'], f, LABEL.get(s['id'], s['id'])))
pal_new = kmeans(allf)
# ---- referência (amostra regular de até 120 quadros) ----
ref_files = sorted(glob.glob(f'{REF}/*.png'))
pal_ref = kmeans(ref_files[::max(1, len(ref_files) // 120)][:120]) if ref_files else None
nearest = lambda c, P: min(dE(c, p) for p in P)
rep = {'video': V, 'k': K, 'paleta_piloto': pal_new, 'paleta_referencia': pal_ref}
if pal_ref:
    # distância ponderada pela área: quanto da imagem do piloto está a ≤ ΔE 15 de alguma cor da referência (e vice-versa)
    rep['cobertura_piloto_por_ref_dE15'] = round(sum(c['share'] for c in pal_new if nearest(c, pal_ref) <= 15), 3)
    rep['cobertura_ref_por_piloto_dE15'] = round(sum(c['share'] for c in pal_ref if nearest(c, pal_new) <= 15), 3)
    rep['dE_medio_ponderado_piloto→ref'] = round(sum(c['share'] * nearest(c, pal_ref) for c in pal_new), 1); rep['dE_medio_ponderado_ref→piloto'] = round(sum(c['share'] * nearest(c, pal_new) for c in pal_ref), 1)
# tons-assinatura (média Lab das regiões típicas do piloto): tinta = pixel mais escuro do quadro (L<22), cabeça = quase-branco azulado
sig = {}
for nm, (lo, hi) in {'tinta (L<22)': (0, 22), 'sombras (22–45)': (22, 45), 'tons médios (45–70)': (45, 70), 'luzes (70–100)': (70, 101)}.items():
    px = np.concatenate([np.asarray(Image.open(f).convert('RGB').resize((54, 96), Image.BOX)).reshape(-1, 3) for f in allf]); lab = to_lab(px); L = lab[:, 0] * 100 / 255; m = (L >= lo) & (L < hi)
    if m.any(): c = cv2.cvtColor(np.uint8([[np.mean(px[m], 0)]]), cv2.COLOR_RGB2LAB)[0, 0]; sig[nm] = dict(hex='#%02x%02x%02x' % tuple(int(v) for v in np.mean(px[m], 0)), share=round(float(m.mean()), 3))
rep['faixas_de_luminosidade'] = sig
json.dump(rep, open(f'{R}/design/palette.json', 'w'), ensure_ascii=False, indent=1)
# ---- PNGs ----
fb, fs = font(13), font(11); sw = 54
def strip(dr, x, y, w, pal, title):
    dr.text((x, y), title, fill=(240, 232, 250), font=fb); xx = x
    for c in pal:
        ww = max(6, int(w * c['share'])); dr.rectangle([xx, y + 18, xx + ww, y + 18 + 28], fill=c['hex']); xx += ww
    for i, c in enumerate(pal): dr.text((x + (i % 5) * (w // 5), y + 52 + (i // 5) * 14), f"{c['hex']} {c['share']*100:.0f}%", fill=(240, 232, 250), font=fs)
P = Image.new('RGB', (760, 200 if pal_ref else 110), (36, 26, 44)); d = ImageDraw.Draw(P); strip(d, 10, 6, 740, pal_new, 'Paleta do piloto (k-means Lab, quadros finais)')
if pal_ref: strip(d, 10, 96, 740, pal_ref, 'Paleta da referência (prints do canal; só cores)')
P.save(f'{R}/design/palette.png')
n = len(tiles); cols = 4; rows = (n + cols - 1) // cols; tw, th = 202, 360; E = Image.new('RGB', (cols * tw + 20, rows * (th + 46) + 40), (36, 26, 44)); d = ImageDraw.Draw(E); d.text((10, 8), 'Ficha de ambientes — quadros finais do piloto + paleta dominante de cada um', fill=(240, 232, 250), font=fb)
for i, (sid, f, lb) in enumerate(tiles):
    x, y = 10 + (i % cols) * tw, 30 + (i // cols) * (th + 46); E.paste(Image.open(f).convert('RGB').resize((tw - 6, th)), (x, y)); d.multiline_text((x, y + th + 3), '\n'.join(textwrap.wrap(lb, 33)[:2]), fill=(240, 232, 250), font=fs, spacing=2)
    pl = kmeans([f], 6); xx = x
    for c in pl: ww = max(3, int((tw - 6) * c['share'])); d.rectangle([xx, y + th + 30, xx + ww, y + th + 40], fill=c['hex']); xx += ww
E.save(f'{R}/design/environment-sheet.png')
print('ok: design/environment-sheet.png', E.size, '· design/palette.png/json'); print({k: v for k, v in rep.items() if k.startswith(('cobertura', 'dE'))})
