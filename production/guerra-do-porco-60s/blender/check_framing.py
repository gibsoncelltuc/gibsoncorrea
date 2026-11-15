"""Verificador de enquadramento: projeta objetos-chave na tela da câmera em vários instantes e acusa quem sai do quadro."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from bpy_extras.object_utils import world_to_camera_view
from lib import util, renderlib, shots, anim
sid = sys.argv[1]
from lib import anim as _a
t0, t1 = _a.EDIT[sid]; times = [round(t0 + k * .25, 2) for k in range(int((t1 - t0) / .25) + 1)]
util.reset(); sc = renderlib.setup((135, 240), samples=1); shot = shots.SHOT_CLASSES[sid]({'grass': 2000}); shot.build(); keys = shot.keys_()
for t in times:
    shot.update(t); bpy.context.view_layer.update(); row = []
    for name, o in keys.items():
        p = world_to_camera_view(sc, shot.cam, o.matrix_world.translation); ok = (0.03 < p.x < 0.97 and 0.03 < p.y < 0.97 and p.z > 0)
        row.append(f"{name}=({p.x:.2f},{p.y:.2f}){'' if ok else ' ✗FORA'}")
    bad = [r for r in row if 'FORA' in r and not r.startswith(('sol0', 'fleet', 'sol20'))]
    if bad: print(f'{sid} t={t:5.2f}  ' + '  '.join(row))
