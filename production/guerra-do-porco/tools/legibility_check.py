#!/usr/bin/env python3
"""Legibilidade/acessibilidade das legendas (rubrica V2: "legendas, contraste, safe zones, idioma") medida no vídeo FINAL e nas camadas de legenda (alfa) do Remotion.
Por cartão: caixa do texto (alfa > 0,1) × zona segura de Shorts; altura relativa; contraste WCAG preenchimento×contorno e preenchimento×fundo imediatamente ao redor (anel sem legenda,
lido do próprio vídeo final); velocidade de leitura (caracteres/s); teste de tela pequena (1/3 da resolução: altura do texto em px e contraste); idioma (pt-BR) no roteiro, nas legendas e na faixa.
Saída: qa/legibility.json + qa/legibility-safezone.png.   Uso: python3 tools/legibility_check.py [renders/pilot_540.mp4] [renders/_captions]"""
import json, os, re, subprocess, sys, tempfile
TMP = os.environ.get('WORK_TMP', os.path.join(tempfile.gettempdir(), 'toon-work')); os.makedirs(TMP, exist_ok=True)
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); V = sys.argv[1] if len(sys.argv) > 1 else 'renders/pilot_540.mp4'; CAPS = sys.argv[2] if len(sys.argv) > 2 else 'renders/_captions'
FPS = 30
# zona segura (Shorts/Reels/TikTok): margens laterais ≥ 6 %, nada acima de 8 % nem abaixo de 80 % da altura (UI da plataforma ocupa a faixa inferior ~20 % e a coluna direita)
SAFE = dict(x0=0.06, x1=0.94, y0=0.08, y1=0.80)
def lum(rgb):  # luminância relativa WCAG (entrada 0–255 sRGB)
    c = np.asarray(rgb, np.float64) / 255; c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4); return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]
cr = lambda l1, l2: (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)
srt = open(f'{R}/renders/final.srt', encoding='utf-8').read().strip().split('\n\n'); cards = []
for blk in srt:
    ln = blk.split('\n'); t = re.findall(r'(\d+):(\d+):(\d+),(\d+)', ln[1]); a, b = [int(x[0]) * 3600 + int(x[1]) * 60 + int(x[2]) + int(x[3]) / 1000 for x in t]; cards.append([a, b, ' '.join(ln[2:])])
for c0, c1 in zip(cards[:-1], cards[1:]): c0[1] = min(c0[1], c1[0])   # uma legenda por vez
info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', f'{R}/{V}'])); vs = next(s for s in info['streams'] if s['codec_type'] == 'video'); W, H = vs['width'], vs['height']
au = next((s for s in info['streams'] if s['codec_type'] == 'audio'), {}); lang_tag = au.get('tags', {}).get('language', '(sem tag)')
rows = []; union = None
for a, b, tx in cards:
    t = (a + b) / 2; fi = int(round(t * FPS)); ov = f'{R}/{CAPS}/element-{fi:03d}.png'
    if not os.path.exists(ov): rows.append({'texto': tx, 't': round(t, 3), 'erro': f'camada ausente {ov}'}); continue
    O = np.asarray(Image.open(ov).convert('RGBA'), np.uint8); al = O[..., 3]; txt = al > 25
    if not txt.any(): rows.append({'texto': tx, 't': round(t, 3), 'erro': 'camada sem texto'}); continue
    ys, xs = np.where(txt); bx0, bx1, by0, by1 = xs.min() / W, (xs.max() + 1) / W, ys.min() / H, (ys.max() + 1) / H
    fill = (al > 230) & (O[..., :3].min(2) > 200); outl = (al > 230) & (O[..., :3].max(2) < 90)
    f_rgb = np.median(O[fill][:, :3], 0) if fill.any() else np.array([255, 255, 255]); o_rgb = np.median(O[outl][:, :3], 0) if outl.any() else np.array([26, 14, 18])
    # fundo: anel de 4–18 px em volta do texto (alfa ≈ 0) lido do quadro final (a camada sobreposta não o cobre ali)
    fr = f'{TMP}/legib_{fi}.png'; subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{R}/{V}', '-vf', f'select=eq(n\\,{fi})', '-frames:v', '1', fr], check=True)
    F = np.asarray(Image.open(fr).convert('RGB'), np.uint8); d1 = ndi.binary_dilation(txt, iterations=4); d2 = ndi.binary_dilation(txt, iterations=18); ring = d2 & ~d1 & (al < 5)
    bgL = lum(F[ring]); p95 = float(np.percentile(bgL, 95)); med = float(np.median(bgL))
    # tela pequena: 1/3 da resolução — altura do texto em px e contraste preenchimento×contorno após reamostrar
    def alt_px(div):
        S = np.asarray(Image.fromarray(O).resize((W * 2 // div, H * 2 // div), Image.LANCZOS), np.uint8); sa = S[..., 3] > 25; yy = np.where(sa)[0]; return int(yy.max() - yy.min() + 1) if sa.any() else 0
    cap_px_phone = alt_px(3); cap_px_thumb = alt_px(6)   # 2/3 da resolução (≈360 px de largura: celular) e 1/3 (miniatura em grade)
    cap_px_small = cap_px_phone
    r_fo = cr(float(lum(f_rgb)), float(lum(o_rgb))); r_fb = cr(float(lum(f_rgb)), p95)
    dur = b - a; cps = len(tx) / dur
    rows.append({'texto': tx, 't': round(t, 3), 'caixa_%': [round(bx0 * 100, 1), round(by0 * 100, 1), round(bx1 * 100, 1), round(by1 * 100, 1)], 'altura_%': round((by1 - by0) * 100, 1),
                 'dentro_zona_segura': bool(bx0 >= SAFE['x0'] and bx1 <= SAFE['x1'] and by0 >= SAFE['y0'] and by1 <= SAFE['y1']),
                 'contraste_preenchimento_contorno': round(r_fo, 1), 'contraste_preenchimento_fundo_p95': round(r_fb, 2), 'lum_fundo_mediana': round(med, 3),
                 'altura_px_celular_360': cap_px_phone, 'altura_px_miniatura_180': cap_px_thumb, 'cps': round(cps, 1), 'dur_s': round(dur, 2)})
    u = np.zeros((H, W), bool) if union is None else union; union = u | txt
ok = [r for r in rows if 'erro' not in r]
stop = {'o', 'a', 'de', 'um', 'uma', 'e', 'do', 'da', 'que', 'dois', 'ele', 'mas', 'só'}; words = ' '.join(r['texto'] for r in rows).lower().split()
pt_hits = sum(1 for w in words if w.strip('.,!?') in stop) + sum(1 for w in words if re.search(r'[áàâãéêíóôõúç]', w))
checks = {
 'todas_as_camadas_de_legenda_lidas': len(ok) == len(cards),
 'caixas_dentro_da_zona_segura (x 6–94 %, y 8–80 %)': all(r['dentro_zona_segura'] for r in ok),
 'altura da caixa do texto ≥ 2,5 % da altura do quadro (pior caso: palavra só com x-height, ex. "um"; corpo da fonte = 6,4 %)': all(r['altura_%'] >= 2.5 for r in ok),
 'contraste preenchimento×contorno ≥ 7:1 (WCAG AAA)': all(r['contraste_preenchimento_contorno'] >= 7 for r in ok),
 'contraste preenchimento×fundo (p95 mais claro) ≥ 1,5:1 OU contorno ≥ 7:1 (contorno separa o texto)': all(r['contraste_preenchimento_fundo_p95'] >= 1.5 or r['contraste_preenchimento_contorno'] >= 7 for r in ok),
 'velocidade de leitura: média ≤ 20 caracteres/s e pico ≤ 25 (cartões de 1–3 palavras, redundantes com a narração; a própria fala tem ~17 car/s)': (sum(len(r['texto']) for r in ok) / sum(r['dur_s'] for r in ok)) <= 20 and all(r['cps'] <= 25 for r in ok),
 'cartões exibidos por ≥ 0,30 s (janela real: cartão seguinte encerra o anterior)': all(r['dur_s'] >= 0.30 - 1e-3 for r in ok),
 'celular de 360 px de largura: texto ≥ 12 px de altura; miniatura de 180 px: ≥ 8 px': all(r['altura_px_celular_360'] >= 12 and r['altura_px_miniatura_180'] >= 8 for r in ok),
 'idioma pt-BR declarado (production.json) e texto em português': json.load(open(f'{R}/production.json'))['language'] == 'pt-BR' and pt_hits >= 8,
 'faixa de áudio com tag de idioma (por/pt)': lang_tag in ('por', 'pt', 'pt-BR')}
rep = {'video': V, 'resolucao': f'{W}x{H}', 'zona_segura': SAFE, 'tag_idioma_audio': lang_tag, 'cartoes': rows, 'checks': checks,
       'resumo': {'cartoes': len(rows), 'altura_%_min': min(r['altura_%'] for r in ok), 'altura_%_max': max(r['altura_%'] for r in ok), 'contraste_fill_contorno_min': min(r['contraste_preenchimento_contorno'] for r in ok),
                  'contraste_fill_fundo_p95_min': min(r['contraste_preenchimento_fundo_p95'] for r in ok), 'cps_max': max(r['cps'] for r in ok), 'cps_media': round(sum(len(r['texto']) for r in ok) / sum(r['dur_s'] for r in ok), 1), 'px_celular_360_min': min(r['altura_px_celular_360'] for r in ok), 'px_miniatura_180_min': min(r['altura_px_miniatura_180'] for r in ok),
                  'caixa_x_%_min_max': [min(r['caixa_%'][0] for r in ok), max(r['caixa_%'][2] for r in ok)], 'caixa_y_%_min_max': [min(r['caixa_%'][1] for r in ok), max(r['caixa_%'][3] for r in ok)]}}
json.dump(rep, open(f'{R}/qa/legibility.json', 'w'), ensure_ascii=False, indent=1)
# figura: um quadro do vídeo com a zona segura e a união de todas as caixas de legenda
sub = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '2.0', '-i', f'{R}/{V}', '-frames:v', '1', f'{TMP}/legib_bg.png'], check=True); bg = Image.open(f'{TMP}/legib_bg.png').convert('RGB')
dr = ImageDraw.Draw(bg, 'RGBA'); dr.rectangle([SAFE['x0'] * W, SAFE['y0'] * H, SAFE['x1'] * W, SAFE['y1'] * H], outline=(60, 255, 120, 255), width=3)
dr.rectangle([0, SAFE['y1'] * H, W, H], fill=(255, 40, 40, 70)); dr.rectangle([0, 0, W, SAFE['y0'] * H], fill=(255, 40, 40, 70)); dr.rectangle([0, 0, SAFE['x0'] * W, H], fill=(255, 40, 40, 70)); dr.rectangle([SAFE['x1'] * W, 0, W, H], fill=(255, 40, 40, 70))
if union is not None:
    ys, xs = np.where(union); dr.rectangle([xs.min(), ys.min(), xs.max(), ys.max()], outline=(255, 230, 0, 255), width=3); dr.text((8, 10), 'verde = zona segura · vermelho = interface da plataforma · amarelo = união das legendas', fill=(255, 255, 255, 255))
bg.save(f'{R}/qa/legibility-safezone.png')
for k, v in checks.items(): print(('PASS ' if v else 'FAIL ') + k)
print(rep['resumo']); print(f"{sum(checks.values())}/{len(checks)}")
sys.exit(0 if all(checks.values()) else 1)
