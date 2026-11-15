"""Renderiza quadros-chave: python stills.py <w> <h> <samples> S1:0.0,3.4 S2:4.7 ..."""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from lib import util, renderlib, shots, anim
W, H, S = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); out = os.environ.get('OUT', os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'out', 'stills'))
os.makedirs(out, exist_ok=True)
for spec in sys.argv[4:]:
    sid, ts = spec.split(':'); util.reset(); sc = renderlib.setup((W, H), samples=S, bounces=int(os.environ.get('BOUNCES', 3)), view='Standard', look='None', exposure=float(os.environ.get('EXPO', -0.45)))
    shot = shots.SHOT_CLASSES[sid]({'grass': int(os.environ.get('GRASS', 60000))}); shot.build()
    for t in [float(x) for x in ts.split(',')]:
        t0 = time.time(); shot.update(t); sc.render.filepath = f'{out}/st_{sid}_{t:.1f}.png'; bpy.ops.render.render(write_still=True); print(sid, t, round(time.time() - t0, 1), 's', flush=True)
