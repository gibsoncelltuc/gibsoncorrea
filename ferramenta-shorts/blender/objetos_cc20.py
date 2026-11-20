# CC 20 Von Frisch: colmeia de observacao (moldura de madeira, favo sextavado e abelhas listradas). blender -b --python blender/objetos_cc20.py
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('beehive')
caixa((0, .06, 0), (1.1, .12, .4), '#6a4426', 1.0)                       # base
for x in (-.5, .5): caixa((x, .7, 0), (.08, 1.2, .14), '#8a5a2e', 1.0)   # montantes
caixa((0, 1.32, 0), (1.08, .08, .16), '#8a5a2e', 1.0)                     # travessa de cima
caixa((0, .7, -.03), (.92, 1.12, .04), '#c98a1a', 1.0)                    # fundo de cera
r = .062
for j in range(9):                                                        # favo: alveolos sextavados
    for i in range(7):
        x = -.4 + i * r * 1.8 + (r * .9 if j % 2 else 0); y = .22 + j * r * 1.56
        if abs(x) > .43: continue
        cil((x, y, .0), r * .95, .04, '#f2b632' if (i + j) % 5 else '#e8a020', rot=(m.pi / 2, 0, 0), lados=6)
def abelha(x, y, ang):
    ca, sa = m.cos(ang), m.sin(ang)
    for k, col in enumerate(('#1b1b1f', '#f2c21a', '#1b1b1f', '#f2c21a')):
        bola((x + ca * (k - 1.5) * .035, y + sa * (k - 1.5) * .035, .05), .033, col, seg=10)
    bola((x + ca * .085, y + sa * .085, .05), .028, '#1b1b1f', seg=10)                       # cabeca
    for s in (-1, 1): bola((x - sa * s * .045, y + ca * s * .045, .085), .035, '#dfefff', esc=(1.3, .6, .3), seg=10)   # asas
for (x, y, a) in ((-.2, .5, .5), (.15, .78, 2.0), (.0, 1.0, -.6), (.25, .4, 3.0), (-.28, .9, 1.2), (.05, .6, 1.57)): abelha(x, y, a)
torno((.75, 0, .1), [(.18, 0), (.2, .04), (.0, .045)], '#3a6fb0', 20)     # pratinho de agua com acucar
torno((.75, .04, .1), [(.15, 0), (0, .005)], '#e8f4ff', 20)
fim(0.006)
