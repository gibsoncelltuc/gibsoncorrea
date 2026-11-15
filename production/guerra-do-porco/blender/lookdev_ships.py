import sys, os, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from lib import util, mats, texlib, renderlib, farm, ships
util.reset(); sc = renderlib.setup((360, 640), samples=int(os.environ.get('SAMPLES', 16)), bounces=3, view='Standard', look='None', exposure=0.3)
objs = farm.build('golden', grass_n=40000); f = ships.fleet()
cam = renderlib.camera(60, dof=False)
for k, (p, t, fv) in {'a': ((4.5, -7, 5.0), (-4, 70, 2.5), 62), 'b': ((-22, 38, 1.4), (-8, 80, 3.2), 58)}.items():
    renderlib.place_camera(cam, p, t, fov=fv); t1 = time.time(); renderlib.render_still(f'/tmp/claude-0/bl/ships_{k}.png'); print(k, round(time.time() - t1, 1), 's')
