# CC 16 Velcro: o carrapicho gigante (bola de espinhos com ganchinhos) e a fita de velcro. blender -b --python blender/objetos_cc16.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('burr')
torno((0, 0, 0), [(.3, 0), (.32, .05), (.2, .1), (.14, .3), (.2, .34), (0, .36)], '#6a4426', 20)   # pedestal
C = (0, .66, 0); r0 = .3
bola(C, r0, '#8a6a2a', seg=16)                                                                      # miolo do carrapicho
n = 60; ga = math.pi * (3 - math.sqrt(5))
for i in range(n):                                                                                 # espinhos distribuidos na esfera, cada um com gancho na ponta
    y = 1 - 2 * (i + .5) / n; rr = math.sqrt(1 - y * y); th = ga * i
    d = (rr * math.cos(th), y, rr * math.sin(th))
    if d[1] < -.75: continue
    p0 = tuple(C[k] + d[k] * r0 * .9 for k in range(3)); p1 = tuple(C[k] + d[k] * (r0 + .14) for k in range(3))
    up = (0, 1, 0) if abs(d[1]) < .9 else (1, 0, 0)
    side = (d[1] * up[2] - d[2] * up[1], d[2] * up[0] - d[0] * up[2], d[0] * up[1] - d[1] * up[0])
    p2 = tuple(p1[k] + side[k] * .05 - d[k] * .03 for k in range(3))
    tubo([p0, p1, p2], .024, '#b08a3a' if i % 2 else '#9a7a30')
caixa((.75, .03, .25), (.5, .04, .16), '#2a2a30', 1.0)                                               # fita de velcro (lado dos ganchos)
for i in range(9):
    for j in range(3): bola((.53 + i * .055, .06, .19 + j * .055), .018, '#4a4a55', seg=8)
caixa((.75, .03, -.05), (.5, .05, .16), '#3a3a44', 1.0)                                             # lado felpudo
fim(0.005)
