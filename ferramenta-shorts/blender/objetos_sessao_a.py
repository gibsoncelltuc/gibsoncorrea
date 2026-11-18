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
novo('scroll')                                        # pergaminho do tratado de paz (herói do EP 14): rolo deitado sobre suporte, laço e selo
cil((0, .08, 0), .55, .16, '#7a4a26'); cil((0, .17, 0), .5, .04, '#a8703c')
cil((0, .45, 0), .2, 1.1, '#f1e6c8', rot=(0, 0, math.pi / 2)); cil((0, .45, 0), .16, 1.14, '#e0cfa2', rot=(0, 0, math.pi / 2))
for x in (-.56, .56): cil((x, .45, 0), .21, .06, '#d6c08a', rot=(0, 0, math.pi / 2))
cil((0, .45, 0), .215, .12, '#b0282f', rot=(0, 0, math.pi / 2)); bola((0, .45, .22), .09, '#d8282f', .6); tubo([(0, .4, .24), (-.1, .22, .3), (-.2, .18, .34)], .02, '#b0282f'); tubo([(0, .4, .24), (.1, .22, .3), (.22, .17, .32)], .02, '#b0282f')
fim(.02)
novo('cod')                                           # bacalhau (herói do EP 15): corpo liso de esferas sobrepostas, cauda achatada, nadadeiras, barbilhão; olha para +x
C1, C2, C3 = '#8a9a6a', '#d8d2a4', '#6f7f52'
FL = (math.pi / 2, 0, 0)
x = .75
while x > -.85:
    r = max(.07, .3 * math.sqrt(max(0, 1 - (x / .95) ** 2)))
    bola((x, .42 + .02 * (x < 0), 0), r, C1); bola((x, .42 - .09 * r / .3, .0), r * .8, C2, .85)
    x -= .06
bola((.72, .44, 0), .17, C1); bola((.82, .4, 0), .1, C1)
for s in (1, -1): bola((.74, .5, .1 * s), .055, '#f4f4ec'); bola((.76, .5, .125 * s), .028, '#111111')
bola((-1.02, .42, 0), .22, C3, .3, rot=FL); bola((-1.1, .6, 0), .15, C3, .3, rot=FL); bola((-1.1, .24, 0), .15, C3, .3, rot=FL)   # cauda em leque
bola((.0, .74, 0), .2, C3, .3, rot=FL); bola((-.4, .68, 0), .14, C3, .3, rot=FL); bola((-.15, .13, 0), .13, C3, .3, rot=FL)      # dorsais e ventral
for s in (1, -1): bola((.3, .33, .24 * s), .11, C3, .3, rot=FL)
tubo([(.86, .34, 0), (.9, .22, 0)], .022, C2)
fim(.02)
novo('melon')                                         # melancia cortada ao meio (herói do EP 16): casca listrada, miolo vermelho, sementes
FL = (math.pi / 2, 0, 0)
bola((0, .48, -.3), .5, '#2f7a3a', .95)
for sx in (-1, 1):
    for dy in (-.22, 0, .22): bola((sx * .47, .48 + dy, -.3), .11, '#1f5a2a', .6)
cil((0, .48, .3), .47, .06, '#f4f0c0', rot=FL); cil((0, .48, .33), .4, .06, '#e8403a', rot=FL)
for x, y in ((-.18, .6), (.1, .68), (.22, .5), (-.05, .42), (-.24, .38), (.16, .3), (-.1, .24), (.0, .54)): bola((x, y, .37), .035, '#1b1b1f', .6)
fim(.02)
novo('whisky')                                        # garrafa de uísque (herói do EP 17): corpo no torno, gargalo, rolha dourada, rótulo
torno((0, 0, 0), [(.01, 0), (.2, .01), (.23, .06), (.23, .62), (.2, .72), (.09, .86), (.075, .98), (.08, 1.12), (.075, 1.14)], '#8a4a1a')
cil((0, .35, 0), .25, .3, '#f1e6c8'); cil((0, .35, 0), .255, .05, '#b0282f'); bola((0, .38, .26), .06, '#d9a630', .4, rot=(math.pi / 2, 0, 0))
cil((0, 1.18, 0), .095, .1, '#d9a630'); cil((0, 1.1, 0), .088, .03, '#b0282f')
fim(.015)
novo('dog')                                           # cachorro caramelo em pé (herói do EP 18): corpo de esferas, cabeça com focinho, orelhas caídas, pernas, rabo; olha para +x
D1, D2, D3 = '#c98a4a', '#e8c48a', '#7a4a26'
FL2 = (math.pi / 2, 0, 0)
bola((-.1, .62, 0), .3, D1, .85); bola((.18, .64, 0), .28, D1, .9); bola((-.38, .6, 0), .22, D1, .9)       # tronco
bola((.5, .92, 0), .24, D1); bola((.74, .84, 0), .13, D2, .8); bola((.86, .85, 0), .05, '#1b1b1f')           # cabeça, focinho, nariz
for s in (1, -1):
    bola((.58, .98, .13 * s), .05, '#f4f4ec'); bola((.6, .98, .16 * s), .025, '#111111')                    # olhos
    bola((.42, .96, .22 * s), .11, D3, .35, rot=FL2)                                                         # orelhas
    for x in (.32, -.34): cil((x, .22, .15 * s), .07, .44, D1); bola((x + .03, .03, .15 * s), .08, D2, .6)   # pernas e patas
tubo([(-.55, .75, 0), (-.78, .95, 0), (-.9, 1.12, 0)], .045, D1)                                           # rabo
bola((.1, .5, 0), .2, D2, .8)                                                                                # barriga
fim(.02)
