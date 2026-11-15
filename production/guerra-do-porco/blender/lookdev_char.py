import sys, os, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from lib import util, mats, texlib, renderlib, farm, char
util.reset(); sc = renderlib.setup((540, 960), samples=int(os.environ.get('SAMPLES', 28)), bounces=3, view=os.environ.get('VIEW', 'Standard'), look='None', exposure=float(os.environ.get('EXPO', 0.3)))
t0 = time.time(); objs = farm.build('golden', grass_n=70000); print('farm', round(time.time() - t0, 1), 's')
CUTLAR = dict(shirt='#ead9b4', pattern='plain', outfit='overalls', pants='#2f2a46', shoe='#5a3a2a', hat='straw', hatColor='#e8c068', hatBand='#3a6aa8', beard='#c9a06a', build=1.0, sleeve='#2f2a46')
GRIFFIN = dict(shirt='#f3ead6', pattern='plain', outfit='waistcoat', trim='#8a6a3a', pants='#3a3350', shoe='#2a2030', hat='flatcap', hatColor='#8c7a58', sideburns='#d4772e', mustache='#d4772e', blush=True, build=1.18)
SOLDIER = dict(shirt='#2f4f8a', pattern='uniform', shirt2='#9fb8e0', outfit='uniform', trim='#f0c250', pants='#6c8fc8', shoe='#1f1a2a', hat='kepi', hatColor='#2f4f8a', build=1.0, sleeve='#2f4f8a')
BAYNES = dict(shirt='#24305c', pattern='plain', outfit='admiral', trim='#f0c250', pants='#2f2a46', shoe='#1a1624', hat='bicorn', sideburns='#e3dfea', mustache='#d8d4e0', build=1.15, sleeve='#24305c')
t0 = time.time(); c = char.Char('cutlar', CUTLAR); g = char.Char('griffin', GRIFFIN); print('chars', round(time.time() - t0, 1), 's', len(c.objs) + len(g.objs), 'objs')
c.pose(dict(x=-0.5, y=-1.6, face=1, scale=1.0, lean=.03, tilt=.04, armL=(.12, .15), armR=(-.12, .12), lid=.42, mouth='line', brows=(.2, -.2), angry=.2, look=(.6, 0)))
g.pose(dict(x=0.9, y=-1.2, face=-1, scale=1.0, lean=-.02, tilt=-.05, armL=(.3, .3), armR=(1.3, .8), lid=.55, mouth='smirk', brows=(.35, -.4), eye='lid'))
cam = renderlib.camera(60, dof=True, fstop=2.2, focus=4.2)
renderlib.place_camera(cam, (0.2, -5.2, 0.55), (0.1, 0.5, 0.95), fov=58, focus=3.9)
t1 = time.time(); renderlib.render_still('/tmp/claude-0/bl/char_a.png'); print('render', round(time.time() - t1, 1), 's')
