#!/usr/bin/env python3
"""REPARO CIRÚRGICO: lê qa/frames-status.json, apaga SÓ os quadros reprovados e manda o Blender refazer apenas eles (render_shot.py é retomável: pula os que existem). Depois roda o portão
de novo; repete até passar ou até N tentativas (padrão 3). Uso: python3 tools/repair_frames.py [W=540 H=960 S=12 GRASS=50000] [--max 3]"""
import json, os, re, subprocess, sys, collections
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); kv = dict(a.split('=') for a in sys.argv[1:] if '=' in a); W, H, S, G = kv.get('W', '540'), kv.get('H', '960'), kv.get('S', '12'), kv.get('GRASS', '50000')
mx = int(sys.argv[sys.argv.index('--max') + 1]) if '--max' in sys.argv else 3; root = f'{R}/blender/out/frames'
for attempt in range(1, mx + 1):
    rc = subprocess.run([sys.executable, f'{R}/tools/frame_gate.py', root], capture_output=True, text=True); st = json.load(open(f'{R}/qa/frames-status.json'))['status']
    print(f'tentativa {attempt}: {len(st)} quadros reprovados'); 
    if not st: print('portão A: todos os quadros concluídos'); sys.exit(0)
    by = collections.defaultdict(list)
    for k in st: eid, f = k.split('/'); by[eid].append(f); os.remove(f'{root}/{k}.png')
    for eid, fs in by.items():
        nums = sorted(int(re.search(r'f(\d+)', f).group(1)) for f in fs); print(f'  refazendo {eid}: quadros {nums[0]}…{nums[-1]} ({len(nums)})')
        subprocess.run(['python3', 'render_shot.py', eid, W, H, S, f'out/frames/{eid}', '1', G], cwd=f'{R}/blender', capture_output=True, text=True, env={**os.environ, 'OFFSET': '0'})
sys.exit(1)
