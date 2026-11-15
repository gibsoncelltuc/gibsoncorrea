#!/usr/bin/env python3
"""storyboard/shots.json a partir de storyboard/edl.json (lista de edição ancorada nas PALAVRAS da narração) + script/word-timings.json.
'at' = 0 | segundos | [linha, prefixo_da_palavra, deslocamento_s, nth=0]. O fim de cada plano é o início do seguinte; o último termina no fim do áudio.
Regerar sempre que a voz mudar: os cortes acompanham as palavras sozinhos.   Uso: python3 tools/make_storyboard.py"""
import json, os, re, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = json.load(open(f'{R}/storyboard/edl.json', encoding='utf-8')); T = json.load(open(f'{R}/script/word-timings.json', encoding='utf-8'))
norm = lambda s: re.sub(r'[^\w]', '', s.lower())
def at(a):
    if isinstance(a, (int, float)): return float(a)
    line, pre, dt, nth = (list(a) + [0, 0])[:4]; ws = [w for w in T['words'] if w['line'] == line and norm(w['text']).startswith(norm(pre))]
    if len(ws) <= nth: sys.exit(f'âncora não encontrada: {a}')
    return ws[nth]['start'] + dt
st = [round(at(e['at']), 3) for e in E['edits']]; bad = [(E['edits'][i]['id'], st[i], st[i + 1]) for i in range(len(st) - 1) if st[i + 1] - st[i] < 0.5]
if bad: sys.exit(f'planos com menos de 0,5 s ou fora de ordem: {bad}')
shots = []
for i, e in enumerate(E['edits']):
    a = st[i]; b = st[i + 1] if i + 1 < len(st) else T['total']
    shots.append(dict(id=e['id'], scene=e['scene'], start=a, end=round(b, 3), dur=round(b - a, 3), lines=e['lines'], beat=e['beat'], purpose=e['purpose'], camera=e['camera'], action=e['action'], audio=e['audio']))
d = [s['dur'] for s in shots]
json.dump({'edl': 'storyboard/edl.json (âncoras em palavras)', 'dissolve': E.get('dissolve', 0.4), 'shot_count': len(shots), 'mean_shot_s': round(sum(d) / len(d), 2), 'shots': shots}, open(f'{R}/storyboard/shots.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(shots), 'planos; duração média', round(sum(d) / len(d), 2), 's; mín', min(d), 'máx', max(d))
for s in shots: print(f"  {s['id']:13s} {s['scene']:10s} {s['start']:6.2f}–{s['end']:6.2f} ({s['dur']:.2f}s)  {s['purpose']}")
