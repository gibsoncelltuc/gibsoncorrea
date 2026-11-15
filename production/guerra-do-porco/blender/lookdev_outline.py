"""Look-dev do contorno: dois personagens em plano médio-fechado (como o print de referência) para comparar com os quadros nativos. Uso: python3 lookdev_outline.py <saida.png> [samples]"""
import sys, os, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from lib import util, mats, texlib, renderlib, farm, char
out = sys.argv[1]; S = int(sys.argv[2]) if len(sys.argv) > 2 else 16
util.reset(); sc = renderlib.setup((540, 960), samples=S, bounces=3, view='Standard', look='None', exposure=-0.45)
objs = farm.build('golden', grass_n=15000, trees_n=3, quality='low', sea=False)
from lib.shots import LOOKS
a = char.Char('griffin', LOOKS['griffin']); b = char.Char('cutlar', LOOKS['cutlar'])
a.pose(dict(x=-0.72, y=-1.2, face=1, scale=1.0, lean=.02, tilt=.05, armL=(.12, .15), armR=(-.1, .1), lid=.55, mouth='smirk', brows=(.35, -.3), look=(.5, 0)))
b.pose(dict(x=0.62, y=-1.0, face=-1, scale=1.0, lean=-.02, tilt=-.04, armL=(.1, .1), armR=(.2, .2), lid=.45, mouth='line', brows=(.2, -.2), look=(-.6, 0)))
cam = renderlib.camera(60, dof=False)
renderlib.place_camera(cam, (0.0, -5.6, 1.15), (0.0, 0.5, 1.05), fov=46)
t1 = time.time(); renderlib.render_still(out); print('render', round(time.time() - t1, 1), 's')
