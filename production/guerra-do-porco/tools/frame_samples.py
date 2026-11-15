#!/usr/bin/env python3
"""Amostras de quadros do vídeo FINAL em 0 %, 10 %, 25 %, 50 %, 75 %, 90 % e 100 % de cada cena (rubrica V2 "Verificações automatizáveis").
Para cada amostra mede: luminância média (não preta), nitidez (variância do Laplaciano), e distância ao quadro anterior (não congelado).
Saída: qa/frame-samples/<cena>_<pct>.png, qa/frame-samples/sheet.png (folha 7 colunas × cenas) e qa/frame-samples.json.
Uso: python3 tools/frame_samples.py [renders/pilot_540.mp4]"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); V = sys.argv[1] if len(sys.argv) > 1 else 'renders/pilot_540.mp4'
OUT = f'{R}/qa/frame-samples'; os.makedirs(OUT, exist_ok=True)
sb = json.load(open(f'{R}/storyboard/shots.json'))['shots']
# cenas = agrupa as edições pela cena de origem (S2a+I_eyes → S2 ...) mantendo a ordem
scenes = []
for s in sb:
    sc = s['scene'] if s['scene'] in ('S1', 'S2', 'S3', 'S4', 'S5', 'S6') else s['id'][:2]
    # inserts (I_*) pertencem à cena do plano em que estão (o anterior)
    if s['id'].startswith('I_') and scenes: scenes[-1][2] = s['end']; continue
    if scenes and scenes[-1][0] == sc: scenes[-1][2] = s['end']; continue
    scenes.append([sc, s['start'], s['end']])
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{R}/{V}']).decode().strip())
PCTS = [0, 10, 25, 50, 75, 90, 100]; rows = []; prev = None; fh = 4
def lap(g):
    k = g[1:-1, 1:-1] * -4 + g[:-2, 1:-1] + g[2:, 1:-1] + g[1:-1, :-2] + g[1:-1, 2:]; return float(k.var())
for sc, a, b in scenes:
    for p in PCTS:
        t = min(a + (b - a) * p / 100.0, dur - 1.5 / 30); t = max(t, 0.0); f = f'{OUT}/{sc}_{p:03d}.png'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', f'{R}/{V}', '-frames:v', '1', f], check=True)
        im = Image.open(f).convert('RGB'); a_ = np.asarray(im, np.float32) / 255; g = a_.mean(2); small = np.asarray(im.resize((54, 96)), np.float32)
        d = None if prev is None else float(np.abs(small - prev).mean()); prev = small
        rows.append({'cena': sc, 'pct': p, 't': round(t, 3), 'arquivo': os.path.relpath(f, R), 'lum_media': round(float(g.mean()), 3), 'nitidez_lap_var': round(lap(g), 5), 'dist_quadro_anterior': None if d is None else round(d, 2)})
ok_black = all(r['lum_media'] > 0.08 for r in rows); ok_sharp = all(r['nitidez_lap_var'] > 0.0002 for r in rows)
ok_frozen = all(r['dist_quadro_anterior'] is None or r['dist_quadro_anterior'] > 0.8 for r in rows)
# folha de contato
tw, th = 135, 240; font = ImageFont.load_default()
sheet = Image.new('RGB', (tw * len(PCTS) + 90, th * len(scenes) + 20), (30, 22, 38)); dr = ImageDraw.Draw(sheet)
for j, p in enumerate(PCTS): dr.text((90 + j * tw + 50, 4), f'{p} %', fill=(240, 232, 250), font=font)
for i, (sc, a, b) in enumerate(scenes):
    dr.text((8, 20 + i * th + th // 2), f'{sc}\n{a:.1f}–{b:.1f}s', fill=(240, 232, 250), font=font)
    for j, p in enumerate(PCTS): sheet.paste(Image.open(f'{OUT}/{sc}_{p:03d}.png').convert('RGB').resize((tw, th)), (90 + j * tw, 20 + i * th))
sheet.save(f'{OUT}/sheet.png')
rep = {'video': V, 'cenas': [{'cena': s, 'inicio': round(a, 3), 'fim': round(b, 3)} for s, a, b in scenes], 'percentuais': PCTS, 'amostras': rows, 'n': len(rows),
       'sem_preto': ok_black, 'nitidos': ok_sharp, 'sem_congelamento_entre_amostras': ok_frozen}
json.dump(rep, open(f'{R}/qa/frame-samples.json', 'w'), ensure_ascii=False, indent=1)
print(f"{len(rows)} amostras em {len(scenes)} cenas × {len(PCTS)} pontos · sem preto: {ok_black} · nítidas: {ok_sharp} · distintas do quadro anterior: {ok_frozen} → qa/frame-samples/sheet.png")
sys.exit(0 if (ok_black and ok_sharp and ok_frozen) else 1)
