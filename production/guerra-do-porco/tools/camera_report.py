#!/usr/bin/env python3
"""Câmera e montagem (rubrica V2: shot list, curva de câmera, ritmo e composição) a partir do teste de movimento (qa/motion-report.json: posição/FOV da câmera e projeção dos sujeitos por quadro)
+ storyboard/shots.json. Produz qa/camera-curve.png (posição, FOV, velocidade, ritmo dos planos), qa/camera-report.json e uma tabela Markdown (qa/camera-report.md).
Uso: python3 tools/camera_report.py"""
import json, os, sys
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); M = json.load(open(f'{R}/qa/motion-report.json')); SB = json.load(open(f'{R}/storyboard/shots.json'))
cams = M['camera']; shots = {s['id']: s for s in SB['shots']}; order = [s['id'] for s in SB['shots'] if s['id'] in cams]
FPS = 30; OUT_OK = {'sol0', 'sol20', 'fleet'}   # sujeitos que saem do quadro de propósito (soldados de fundo/frota: pan intencional)
rows = []; fig, ax = plt.subplots(4, 1, figsize=(12, 10), sharex=True); cols = plt.cm.tab20(np.linspace(0, 1, 20))
T = []; POS = []; FOV = []
for i, eid in enumerate(order):
    c = cams[eid]; sh = shots[eid]; a, b = sh['start'], sh['end']
    t = np.array(c['t']); p = np.array(c['pos']); f = np.array(c['fov']); m = (t >= a - 1e-6) & (t <= b + 1e-6)   # só o trecho que aparece (sem o preenchimento do dissolve)
    t, p, f = t[m], p[m], f[m]; v = np.linalg.norm(np.diff(p, axis=0), axis=1) * FPS if len(t) > 1 else np.array([0.0])
    # composição: sujeitos-chave dentro do quadro e deslocamento horizontal do principal
    ins = []; xs = []
    for k, rec in enumerate(c['sujeitos_no_quadro']):
        if not m[k]: continue
        ok = all(0.03 < xy[0] < 0.97 and 0.03 < xy[1] < 0.97 for n, xy in rec.items() if n not in OUT_OK and not n.startswith('sol'))
        ins.append(ok); main = [xy for n, xy in rec.items() if n in ('cutlar', 'griffin', 'baynes', 'aide', 'pig')]
        if main: xs.append(np.mean([q[0] for q in main]))
    rows.append({'edicao': eid, 'cena': sh['scene'], 'inicio': a, 'fim': b, 'dur_s': round(b - a, 2), 'camera': sh['camera'], 'velocidade_media_m_s': round(float(v.mean()), 2), 'velocidade_p95_m_s': round(float(np.percentile(v, 95)), 2),
                 'fov_inicio': round(float(f[0]), 1), 'fov_fim': round(float(f[-1]), 1), 'fov_min_max': [round(float(f.min()), 1), round(float(f.max()), 1)], 'deslocamento_total_m': round(float(np.linalg.norm(p[-1] - p[0])), 2),
                 'quadros_com_sujeitos_no_enquadramento_%': round(100 * float(np.mean(ins)) if ins else 100.0, 1), 'x_medio_do_sujeito_principal': round(float(np.mean(xs)), 2) if xs else None,
                 'sujeito_dentro_do_terço_central (0,2–0,8)': bool(xs) and all(0.2 <= x <= 0.8 for x in xs)})
    T.append(t); POS.append(p); FOV.append(f)
    for j, lab in enumerate('xyz'): ax[j].plot(t, p[:, j], color=cols[(2 * i) % 20], lw=1.6)
    ax[3].plot(t, f, color=cols[(2 * i) % 20], lw=1.6)
    for a_ in ax: a_.axvline(a, color='#888', lw=.6, ls=':')
    ax[0].text((a + b) / 2, ax[0].get_ylim()[1] if False else p[:, 0].max() + .1, eid, ha='center', fontsize=7)
for j, lab in enumerate(('câmera X (m)', 'câmera Y (m)', 'câmera Z (m)', 'FOV vertical (°)')): ax[j].set_ylabel(lab); ax[j].grid(alpha=.25)
ax[3].set_xlabel('tempo (s) — linhas pontilhadas = cortes/dissolves'); fig.suptitle('Curva de câmera por plano — A Guerra do Porco (piloto)'); fig.tight_layout(); fig.savefig(f'{R}/qa/camera-curve.png', dpi=110); plt.close(fig)
# ritmo: duração dos planos
d = np.array([r['dur_s'] for r in rows]); fig, ax2 = plt.subplots(figsize=(10, 2.8)); ax2.barh(range(len(rows)), d, color=[cols[(2 * i) % 20] for i in range(len(rows))]); ax2.set_yticks(range(len(rows))); ax2.set_yticklabels([r['edicao'] for r in rows], fontsize=8)
ax2.axvspan(2.0, 2.7, color='#2a9d8f', alpha=.18, label='faixa observada nos prints (≈ 2–2,7 s/plano)'); ax2.set_xlabel('duração do plano (s)'); ax2.legend(fontsize=8); ax2.invert_yaxis(); fig.tight_layout(); fig.savefig(f'{R}/qa/shot-pacing.png', dpi=110); plt.close(fig)
tot = SB['shots'][-1]['end']; rep = {'planos': rows, 'resumo': {'n_planos': len(rows), 'cortes_por_10s': round((len(rows) - 1) * 10 / tot, 2), 'duracao_media_s': round(float(d.mean()), 2), 'duracao_min_s': round(float(d.min()), 2), 'duracao_max_s': round(float(d.max()), 2),
        'camera_parada_(vel_media<0,05)': [r['edicao'] for r in rows if r['velocidade_media_m_s'] < 0.05], 'enquadramento_min_%': min(r['quadros_com_sujeitos_no_enquadramento_%'] for r in rows)}}
json.dump(rep, open(f'{R}/qa/camera-report.json', 'w'), ensure_ascii=False, indent=1)
md = ['# Câmera e montagem — A Guerra do Porco (piloto)', '', f"{len(rows)} planos · duração média {rep['resumo']['duracao_media_s']} s (mín {rep['resumo']['duracao_min_s']}, máx {rep['resumo']['duracao_max_s']}) · {rep['resumo']['cortes_por_10s']} cortes por 10 s",
      '', '| plano | cena | t (s) | dur | movimento de câmera (projeto) | vel. média (m/s) | FOV ini→fim | sujeitos no quadro | x médio (0–1) |', '|---|---|---|---:|---|---:|---|---:|---:|']
for r in rows: md.append(f"| {r['edicao']} | {r['cena']} | {r['inicio']:.2f}–{r['fim']:.2f} | {r['dur_s']} | {r['camera']} | {r['velocidade_media_m_s']} | {r['fov_inicio']}→{r['fov_fim']} | {r['quadros_com_sujeitos_no_enquadramento_%']} % | {r['x_medio_do_sujeito_principal']} |")
md += ['', '![curva de câmera](camera-curve.png)', '', '![ritmo dos planos](shot-pacing.png)']
open(f'{R}/qa/camera-report.md', 'w', encoding='utf-8').write('\n'.join(md) + '\n'); print(json.dumps(rep['resumo'], ensure_ascii=False))
