import sys, os, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from lib import util, mats, texlib, renderlib, farm
env = sys.argv[sys.argv.index('--') + 1] if '--' in sys.argv else 'golden'; res = int(sys.argv[sys.argv.index('--') + 2]) if '--' in sys.argv and len(sys.argv) > sys.argv.index('--') + 2 else 270
util.reset(); sc = renderlib.setup((res, int(res * 16 / 9)), samples=int(os.environ.get('SAMPLES', 14)), bounces=3, view=os.environ.get('VIEW','AgX'), look=os.environ.get('LOOK','AgX - Punchy'))
t0 = time.time(); objs = farm.build(env, grass_n=90000); print('build', round(time.time() - t0, 1), 's')
cam = renderlib.camera(60, dof=True, fstop=2.4, focus=6.0)
shots = {'a': ((0.9, -5.7, 0.62), (0.6, 2.0, 0.85), 56), 'b': ((2.0, -8.0, 1.7), (0.0, 10.0, 1.1), 62), 'c': ((9.0, -8.5, 1.3), (6.0, 3.0, 1.2), 58)}
for k, (p, t, f) in shots.items():
    renderlib.place_camera(cam, p, t, fov=f, focus=math.dist(p, (0.7, -0.4, 0.5)) if k == 'a' else 9.0)
    t1 = time.time(); renderlib.render_still(f'/tmp/claude-0/bl/farm_{env}_{k}.png'); print(k, 'render', round(time.time() - t1, 1), 's')
