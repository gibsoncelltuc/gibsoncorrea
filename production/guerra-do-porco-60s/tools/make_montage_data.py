#!/usr/bin/env python3
"""Gera montage/data.json (planos, quadros disponíveis, legendas) para a composição Remotion `Montage` e prepara montage/public (links para quadros e áudio).
Uso: python3 tools/make_montage_data.py [--every N]   (N=2: só quadros da passada 1; padrão 1: todos os quadros existentes)"""
import sys, os, re, json, glob
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(R, 'blender'))
from lib import anim
every = int(sys.argv[sys.argv.index('--every') + 1]) if '--every' in sys.argv else 1
frames_root = os.path.join(R, 'blender', 'out', 'frames'); fps = anim.FPS
import PIL.Image as I
shots = []; first = None
for sid, (a, b) in anim.EDIT.items():
    files = sorted(glob.glob(os.path.join(frames_root, sid, 'f*.png')))
    if not files: continue
    first = first or files[0]
    nums = [int(re.search(r'f(\d+)\.png', f).group(1)) for f in files]
    if every > 1: nums = [n for n in nums if (n - nums[0]) % every == 0]
    shots.append(dict(id=sid, start=a, end=b, n0=nums[0], n1=nums[-1], frames=nums))
W, H = I.open(first).size
def tt(s): h, m, x = s.replace(',', '.').split(':'); return int(h) * 3600 + int(m) * 60 + float(x)
caps = []
for blk in open(os.path.join(R, 'renders', 'final.srt'), encoding='utf-8').read().strip().split('\n\n'):
    ln = blk.split('\n'); st, en = ln[1].split(' --> '); caps.append(dict(start=tt(st), end=tt(en), text=' '.join(ln[2:])))
# uma legenda por vez (como no canal): o cartão seguinte entra 0,1 s antes da palavra, então o anterior é encerrado quando o próximo começa
caps.sort(key=lambda c: c['start'])
for a_, b_ in zip(caps[:-1], caps[1:]): a_['end'] = min(a_['end'], b_['start'])
data = dict(fps=fps, width=W, height=H, duration=anim.TOTAL, dissolve=anim.DIS, shots=shots, captions=caps)
json.dump(data, open(os.path.join(R, 'montage', 'data.json'), 'w'), ensure_ascii=False)
pub = os.path.join(R, 'montage', 'public')                      # o bundler do Remotion não segue symlinks → hardlinks (mesmo disco, sem copiar bytes)
def hl(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst): os.remove(dst)
    os.link(src, dst)
for s_ in shots:
    for n in s_['frames']: hl(os.path.join(frames_root, s_['id'], f'f{n:04d}.png'), os.path.join(pub, 'frames', s_['id'], f'f{n:04d}.png'))
hl(os.path.join(R, 'audio', 'final_mix.wav'), os.path.join(pub, 'final_mix.wav'))
print('ok', W, 'x', H, 'planos:', [(s['id'], len(s['frames'])) for s in shots], 'legendas:', len(caps))
