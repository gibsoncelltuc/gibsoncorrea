# PF 17 Bukele: vulcao com usina geotermica (canos e vapor) e a moeda de bitcoin dourada. blender -b --python blender/objetos_pf17.py
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('volcano')
torno((0, 0, 0), [(4.2, 0), (3.6, .6), (2.6, 1.8), (1.6, 3.0), (1.1, 3.6), (.9, 3.4), (0, 3.2)], '#6a5a4a', 32)   # cone com cratera
torno((0, 0, 0), [(4.3, 0), (3.9, .35), (0, .36)], '#4a7a3a', 32)                                            # mato na base
for (x, y, z, r) in ((0, 3.9, 0, .7), (.4, 4.5, .2, .55), (-.3, 5.0, -.1, .5), (.2, 5.5, 0, .4)): bola((x, y, z), r, '#e8ecf0', seg=14)   # vapor
caixa((4.6, .7, 1.8), (1.6, 1.4, 1.2), '#d8d4ca', 1.0)                   # usina
cil((4.2, 1.9, 1.6), .25, 1.0, '#a8a49a', raio_topo=.32)                 # torre de resfriamento
bola((4.2, 2.7, 1.6), .35, '#e8ecf0', seg=12)
for k in range(3): tubo([(1.9 + k * .2, .4, 1.4 + k * .3), (3.0, .5, 1.6 + k * .2), (3.8, .5, 1.6 + k * .2)], .07, '#b8bcc2', passo=.5)   # canos de vapor
fim(0.02)
novo('bitcoin')
torno((0, 0, 0), [(.08, 0), (.12, .02), (0, .03)], '#6a4426', 16)
cil((0, .62, 0), .58, .12, '#e8a020', rot=(m.pi / 2, 0, 0), lados=40)                                     # moeda em pe
cil((0, .62, 0), .5, .14, '#f2b632', rot=(m.pi / 2, 0, 0), lados=40)
for z in (.075, -.075):                                                                                    # o B nas duas faces
    caixa((-.1, .62, z), (.07, .5, .02), '#fff1c2', 1.0)
    for yy in (.48, .76): caixa((-.1, yy, z), (.025, .1, .02), '#fff1c2', 1.0); caixa((.06, yy, z), (.025, .1, .02), '#fff1c2', 1.0)
    for (yc, rr) in ((.71, .1), (.53, .11)):
        for i in range(9):
            a = -m.pi / 2 + m.pi * i / 8; bola((-.06 + rr * m.cos(a) + .02, yc + rr * m.sin(a), z), .032, '#fff1c2', seg=8)
    for yy in (.81, .62, .43): caixa((-.03, yy, z), (.12, .05, .02), '#fff1c2', 1.0)
caixa((0, .03, 0), (.3, .06, .2), '#6a4426', 1.0)
fim(0.008)
novo('miners')                                                                                            # rack de computadores mineradores com luzinhas verdes
for x in (-.7, .7):
    caixa((x, 1.0, 0), (1.2, 2.0, .7), '#3a3e46', 1.0)
    for j in range(6):
        caixa((x, .25 + j * .3, .36), (1.08, .24, .02), '#1b1d22', 1.0)
        for i in range(4): bola((x - .4 + i * .08, .25 + j * .3, .38), .022, '#4aff6a' if (i + j) % 3 else '#ffcf3a', seg=8)
        cil((x + .3, .25 + j * .3, .375), .09, .02, '#5a5e66', rot=(m.pi / 2, 0, 0), lados=16)        # ventoinha
fim(0.01)
novo('coin')                                                                                              # moeda dourada generica (sem letra): "moeda/moedas"
torno((0, 0, 0), [(.08, 0), (.12, .02), (0, .03)], '#6a4426', 16)
cil((0, .62, 0), .58, .12, '#e8a020', rot=(m.pi / 2, 0, 0), lados=40)
cil((0, .62, 0), .5, .14, '#f2b632', rot=(m.pi / 2, 0, 0), lados=40)
for z in (.075, -.075): torno((0, .62, z), [(.3, 0), (.34, 0.001)], '#ffe08a', 32, tampa=False) if False else cil((0, .62, z), .3, .01, '#ffd25a', rot=(m.pi / 2, 0, 0), lados=32)
caixa((0, .03, 0), (.3, .06, .2), '#6a4426', 1.0)
fim(0.008)
