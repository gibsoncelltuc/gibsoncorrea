# Objetos da SESSAO A feitos com formas.py (redondos, chanfrados). blender -b --python blender/objetos_sessao_a.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
import math
def afilado(pts, r0, r1, col, n=10):                  # tubo que afina de r0 a r1 por uma lista de pontos
    seg = []
    for a, b in zip(pts, pts[1:]):
        for i in range(n): t = i / n; seg.append(tuple(a[k] + (b[k] - a[k]) * t for k in range(3)))
    seg.append(pts[-1])
    for i, p in enumerate(seg): bola(p, r0 + (r1 - r0) * i / (len(seg) - 1), col, seg=8)
novo('lobster')                                       # lagosta olhando para +x (herói do EP 11)
V, V2, V3, PR = '#d8402a', '#e0553a', '#b82b1b', '#111111'
bola((.2, .27, 0), .3, V, .85); bola((.0, .26, 0), .3, V2, .85); bola((.55, .23, 0), .2, V2, .85)          # carapaça e cabeça
for i in range(5): bola((-.32 - i * .2, .21 - i * .012, 0), .26 - i * .035, V if i % 2 else V2, .8)         # cauda em gomos
for s in (1, -1):
    bola((-1.42, .12, .13 * s), .13, V3, .35); bola((-1.28, .12, .0), .16, V2, .3)                          # leque da cauda
    afilado([(.7, .2, .22 * s), (.98, .2, .3 * s)], .06, .05, V3); bola((1.18, .2, .36 * s), .2, V2, .65); afilado([(1.3, .21, .3 * s), (1.5, .2, .24 * s)], .07, .02, V); afilado([(1.3, .19, .44 * s), (1.52, .2, .5 * s)], .07, .02, V)   # braço e pinça
    afilado([(.72, .38, .1 * s), (1.2, .55, .2 * s), (1.7, .5, .45 * s)], .025, .008, V3, 8); bola((.66, .38, .1 * s), .05, PR)                       # antena e olho
    for i in range(4): afilado([(i * .17 - .05, .22, .22 * s), (i * .17 - .05, .1, .38 * s), (i * .17 - .02, .03, .42 * s)], .04, .025, V3, 4)    # patas
fim(.02)
novo('ear_jar')                                       # orelha sobre almofada (herói do EP 12; nome mantido)
cil((0, .05, 0), .5, .1, '#6a4426'); cil((0, .17, 0), .44, .14, '#b02a2a'); cil((0, .26, 0), .4, .05, '#d9a630')
P, P2 = '#f2b3a0', '#e08a76'
bola((0, .82, 0), .34, P, .38, rot=(math.pi / 2, 0, 0)); bola((0, .5, 0), .17, P, .55, rot=(math.pi / 2, 0, 0)); bola((0, .62, .0), .26, P, .4, rot=(math.pi / 2, 0, 0))
arco((0, .84, .07), .3, P2, .05, de=-.4, ate=math.pi + .4); arco((0, .84, .1), .19, P2, .045, de=.1, ate=math.pi - .1)                       # borda e dobra interna
bola((.0, .52, .12), .06, P2); bola((-.05, .7, .1), .09, P2, .4, rot=(math.pi / 2, 0, 0))
fim(.015)
novo('golden_stool')                                  # banquinho dourado ashanti (herói do EP 13)
GD, GL = '#d9a630', '#f2d060'
bola((0, .08, 0), .5, GD, .3); cil((0, .3, 0), .13, .4, GL); cil((-.3, .27, 0), .09, .34, GD); cil((.3, .27, 0), .09, .34, GD); cil((0, .3, .2), .08, .4, GD); cil((0, .3, -.2), .08, .4, GD)
for z in (-.24, -.12, 0, .12, .24): arco((0, .98, z), .56, GL, .07, de=math.pi * 1.18, ate=math.pi * 1.82)                                   # assento curvo em arco
for x in (-.55, .55): bola((x, .64, 0), .13, GD, 1.3)
arco((0, .98, .0), .5, '#b0282f', .03, de=math.pi * 1.25, ate=math.pi * 1.75)
fim(.02)
