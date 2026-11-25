# 25/11 Newton: LUA no ceu (esfera cinza com crateras, SEM pedestal: o kit/moon tem base de abajur). blender -b --python blender/objetos_newton.py
import sys, os, math, random; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
random.seed(3)
novo('lua_ceu'); bola((0, 1.0, 0), 1.0, '#d9d9d2', seg=28)
for i in range(14):
    a = random.uniform(0, 2 * math.pi); e = random.uniform(-1.0, 1.0); r = random.uniform(.08, .2)
    x, y, z = math.cos(a) * math.sqrt(1 - e * e), e, math.sin(a) * math.sqrt(1 - e * e)
    bola((x * .97, 1.0 + y * .97, z * .97), r, '#a9a9a2', .35, seg=10)
luz(True); bola((0, 1.0, 0), .02, '#ffffff', seg=6); luz(False)
fim(0)
