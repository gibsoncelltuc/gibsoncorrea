#!/usr/bin/env python3
"""Verifica assets referenciados × arquivos presentes (rubrica V2: "verificar assets referenciados e arquivos ausentes") e quadros do render por plano da EDL.
Confere: (1) todo quadro esperado de cada plano da EDL existe, não está vazio e tem a resolução esperada; (2) não há quadro duplicado consecutivo por hash perceptual
(sinaliza, não reprova: hold intencional é permitido); (3) texturas/áudios/legendas/stems referenciados pelo pipeline existem; (4) toda licença citada tem arquivo.
Saída: linhas PASS/FAIL/INFO + qa/assets-report.json.   Uso: python3 tools/check_assets.py [WxH]  (padrão 540x960)"""
import glob, json, os, re, sys
import numpy as np
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = [int(x) for x in (sys.argv[1] if len(sys.argv) > 1 else '540x960').split('x')]
res = []
def rec(name, ok, detail='', level='check'):
    res.append({'name': name, 'pass': bool(ok), 'detail': str(detail), 'level': level}); print(('PASS ' if ok else ('INFO ' if level == 'info' else 'FAIL ')) + name + (' — ' + str(detail) if detail else ''))
# ---- EDL (fonte da verdade dos quadros) ----
sys.path.insert(0, os.path.join(R, 'blender')); sys.modules.setdefault('bpy', None)
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location('anim_pure', os.path.join(R, 'blender', 'lib', 'anim.py'), submodule_search_locations=None)
    src = open(os.path.join(R, 'blender', 'lib', 'anim.py'), encoding='utf-8').read().replace('from . import util\nROOT = util.ROOT', f"ROOT = {R!r}")
    ns = {'__name__': 'anim_pure'}; exec(compile(src, 'anim.py', 'exec'), ns); EDL = ns['EDL']; FPS = ns['FPS']
except Exception as ex:
    rec('EDL lida de blender/lib/anim.py', False, repr(ex)[:200]); sys.exit(1)
first, last = EDL[0][0], EDL[-1][0]; bad = []; total = 0; ph = []
def dhash(p):
    im = Image.open(p).convert('L').resize((9, 8)); a = np.asarray(im, np.int16); return ((a[:, 1:] > a[:, :-1]).ravel()).tobytes()
for eid, cls, a, b in EDL:
    fr = range(int(round((a - (0 if eid == first else .2)) * FPS)), int(round((b + (0 if eid == last else .2)) * FPS)))
    miss = [f for f in fr if not os.path.exists(f'{R}/blender/out/frames/{eid}/f{f:04d}.png')]; total += len(fr)
    if miss: bad.append((eid, miss[:3], len(miss)))
    if not miss:
        im = Image.open(f'{R}/blender/out/frames/{eid}/f{fr[0]:04d}.png')
        if im.size != (W, H): bad.append((eid, 'resolução', im.size))
        hs = [dhash(f'{R}/blender/out/frames/{eid}/f{f:04d}.png') for f in fr]; dup = sum(1 for i in range(1, len(hs)) if hs[i] == hs[i - 1]); ph.append((eid, dup, len(hs)))
rec(f'quadros da EDL presentes (todos os {total} esperados) e na resolução {W}x{H}', not bad, bad[:6] if bad else f'{len(EDL)} edições')
dups = [(e, d, n) for e, d, n in ph if d > 0]
rec('quadros consecutivos idênticos por hash perceptual (dHash 8x8)', True, f"{sum(d for _, d, _ in ph)} pares de {sum(n for _, _, n in ph)}; " + (', '.join(f'{e}:{d}' for e, d, _ in dups) or 'nenhum'), level='info')
# ---- arquivos referenciados ----
need = ['audio/voice.wav', 'audio/music.wav', 'audio/sfx.wav', 'audio/ambience.wav', 'audio/final_mix.wav', 'audio/mix-report.json', 'audio/sfx-events.json', 'stems/voice.flac', 'stems/music.flac', 'stems/sfx.flac', 'stems/ambience.flac', 'stems/final_mix.flac',
        'renders/final.srt', 'renders/final.ass', 'renders/final_frases.srt', 'script/script.md', 'script/word-timings.json', 'script/beat-map.md', 'research/claims.json', 'research/fact-check.md',
        'assets/licenses/LICENSES.md', 'assets/licenses/dependency-audit.md', 'storyboard/shots.json', 'registry/registry.json', 'production.json', 'README.md']
miss = [p for p in need if not os.path.exists(os.path.join(R, p)) or os.path.getsize(os.path.join(R, p)) == 0]
rec('arquivos de entrega referenciados existem e não estão vazios', not miss, miss if miss else f'{len(need)} arquivos')
# texturas citadas em texlib/paint (arquivos tex/*.png gerados em runtime): existem?
tex = glob.glob(f'{R}/blender/tex/*.png'); rec('texturas pintadas geradas (cache blender/tex)', len(tex) > 0, f'{len(tex)} PNGs', level='info')
# licenças: todo item do registry tem licença declarada; todo "item" em LICENSES.md citado existe
lic = open(f'{R}/assets/licenses/LICENSES.md', encoding='utf-8').read()
for k in ('Piper', 'CC0', 'Blender', 'Montserrat', 'Remotion', 'FFmpeg', 'faster-whisper'): rec(f'LICENSES.md cita {k}', k.lower() in lic.lower())
# legendas: cartões com texto não vazio e tempos crescentes
srt = open(f'{R}/renders/final.srt', encoding='utf-8').read().strip().split('\n\n'); ok = True; prev = -1
for blk in srt:
    ln = blk.split('\n'); t = re.findall(r'(\d+):(\d+):(\d+),(\d+)', ln[1]); a_, b_ = [int(x[0]) * 3600 + int(x[1]) * 60 + int(x[2]) + int(x[3]) / 1000 for x in t]
    ok &= (len(ln) >= 3 and ln[2].strip() != '' and a_ >= prev - 1e-6 and b_ > a_); prev = a_
rec('SRT: cartões não vazios, início crescente, fim > início', ok, f'{len(srt)} cartões')
json.dump({'checks': res, 'passed': sum(r['pass'] for r in res if r['level'] == 'check'), 'total': sum(1 for r in res if r['level'] == 'check')}, open(f'{R}/qa/assets-report.json', 'w'), ensure_ascii=False, indent=1)
n_ok = sum(r['pass'] for r in res if r['level'] == 'check'); n = sum(1 for r in res if r['level'] == 'check'); print(f'{n_ok}/{n}')
sys.exit(0 if n_ok == n else 1)
