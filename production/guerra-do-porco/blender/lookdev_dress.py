"""Lineup de objetos de cena para look-dev (fora do jardim, y=-5). Uso: python3 lookdev_dress.py <saida.png> <grupo 1..5> [samples]"""
import sys, os, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from lib import util, mats, renderlib, farm, dress, nature
out = sys.argv[1]; g = int(sys.argv[2]); S = int(sys.argv[3]) if len(sys.argv) > 3 else 8
util.reset(); sc = renderlib.setup((1280, 720), samples=S, bounces=3, view='Standard', look='None', exposure=-0.45)
objs = farm.build('golden', grass_n=9000, trees_n=2, quality='low', sea=False)
Y = -6.0; cx = 0.0
if g == 1:
    dress.barrel(-4.2, Y, label='H.B.CO.\nFLOUR'); dress.barrel(-3.2, Y + .3, h=.9, r=.38, rz=.4, label='POWDER'); dress.crate(-1.8, Y, label='CABBAGES', fill='cabbage'); dress.crate(-.6, Y + .1, (.8, .6, .6), .3, label='U.S.\nARMY')
    dress.hay_bale(.8, Y, .2); dress.hay_bale(1.1, Y + .1, -.3, (1.0, .5, .5)); dress.haystack(3.6, Y + 1.2, 1.2, 1.9); cx = 0
elif g == 2:
    dress.wheelbarrow(-3.5, Y, .5, 'cabbage'); dress.bucket(-2.0, Y - .2); dress.stump(-1.0, Y); dress.firewood(1.0, Y + .2, .2); dress.tool('rake', (3.0, Y + .8), (3.2, Y + 1.0, 1.5)); dress.tool('hoe', (3.5, Y + .8), (3.6, Y + 1.0, 1.5)); dress.tool('fork', (4.0, Y + .8), (4.1, Y + 1.0, 1.7)); cx = 0
elif g == 3:
    dress.wagon(-3.5, Y + 1, .35); dress.well(.5, Y + 1.5); dress.sheep(2.6, Y, .5); dress.sheep(3.6, Y + .6, 2.9, 5, False); dress.chicken(4.8, Y - .3, .6); dress.chicken(5.2, Y, 2.0, False, 3); cx = 1
elif g == 4:
    dress.scarecrow(-3, Y); dress.clothesline(.5, Y, .0); dress.lantern(3.2, Y); dress.rock(4.2, Y, .45); dress.rock(4.9, Y + .3, .3, 4); dress.picket_fence([(-6, Y + 3), (-2, Y + 3)]); dress.campfire(-4.5, Y + 1); dress.rifle_stack(2.0, Y + 1.5); cx = 0
else:
    dress.barn(0, Y + 12, 0); dress.path_decals([(-8, Y), (-3, Y + .8), (2, Y + .5), (8, Y - .4)], 1.8); dress.ground_scatter('straw', (-6, 6, Y - 2, Y + 3), 8, 3); dress.ground_scatter('leaves', (0, 8, Y - 2, Y + 2), 5, 4)
    dress.cannonballs(3, Y + 2, 0); dress.rope_coil(4.5, Y + 2, 0); dress.ladder(-4, Y + 3, 0, 2.2, .2); cx = 0
cam = (cx, Y - 6.5, 1.5); look = (cx, Y + (9 if g == 5 else 0), 1.0 if g != 5 else 2.0)
c = renderlib.camera(46, dof=False); renderlib.place_camera(c, cam, look, fov=44)
t0 = time.time(); renderlib.render_still(out); print('render', round(time.time() - t0, 1), 's')
