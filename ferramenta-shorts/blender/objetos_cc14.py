# CC 14 Kekule: a cobra que morde o proprio rabo (anel do benzeno) num pedestal. blender -b --python blender/objetos_cc14.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('snake_ring')
torno((0, 0, 0), [(.3, 0), (.32, .05), (.2, .1), (.14, .3), (.2, .34), (0, .36)], '#6a4426', 20)   # pedestal
R, cy = .42, .8
pts = [(R * math.sin(a), cy + R * math.cos(a), 0) for a in [math.pi * 2 * i / 90 * .92 + .3 for i in range(91)]]
for i, p in enumerate(pts):                                                                         # corpo que afina ate o rabo
    bola(p, .045 + .055 * (i / 90), '#2d7a38' if i % 12 in (0, 1) else '#3f9a4a', seg=10)
hx, hy = R * math.sin(.3 + math.pi * 2 * .92 + .12), cy + R * math.cos(.3 + math.pi * 2 * .92 + .12)
bola((hx, hy, 0), .13, '#3f9a4a', esc=(1.3, 1, 1.1))                                                # cabeca
for z in (-1, 1): bola((hx + .02, hy + .08, z * .08), .035, '#f2e14a', seg=10)                     # olhos
for z in (-1, 1): bola((hx + .03, hy + .09, z * .1), .018, '#111111', seg=8)
fim(0.01)
