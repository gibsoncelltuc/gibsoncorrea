# Objetos da sessao B feitos com formas.py (formas redondas): blender -b --python blender/objetos_sessao_b.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
H = (0, 0, math.pi / 2)    # deita o cilindro ao longo do eixo x
novo('syringe')            # seringa antiga de vidro: corpo, liquido, aletas, embolo, ponta e agulha longa
cil((0, .3, 0), .17, 1.3, '#d4eaf0', rot=H); cil((0, .3, 0), .125, 1.1, '#6fb8d6', rot=H)
cil((-.68, .3, 0), .3, .05, '#8a8a8a', rot=H); cil((-1.0, .3, 0), .045, .7, '#9a9a9a', rot=H); cil((-1.38, .3, 0), .2, .07, '#7a7a7a', rot=H)
cil((.76, .3, 0), .1, .22, '#a8a8a8', raio_topo=.04, rot=H); cil((1.3, .3, 0), .028, .85, '#e2e2e2', rot=H)
fim()
novo('kite')               # pipa de losango (vermelha e amarela), varetas em cruz, linha e rabo com lacos
D = (0, 0, math.pi / 4)
caixa((0, 1.3, 0), (.95, .95, .03), '#d8282f', rot=D); caixa((0.0, 1.3, .02), (.45, .45, .03), '#f2d060', rot=D)
cil((0, 1.3, .045), .018, 1.3, '#7a5a3a'); cil((0, 1.3, .045), .018, 1.3, '#7a5a3a', rot=(0, 0, math.pi / 2))
tubo([(0, .78, 0), (.12, .55, 0), (-.1, .32, 0), (.1, .1, 0)], .018, '#f4f4f0')
for (x, y) in ((.12, .55), (-.1, .32), (.1, .1)): bola((x, y, 0), .07, '#d8282f', achata=.5)
fim()
novo('key')                # chave de metal: aro, haste e dentes
arco((0, .75, 0), .16, '#c9a040', esp=.035, de=0, ate=2 * math.pi, n=18)
cil((0, .38, 0), .03, .56, '#c9a040'); cil((.08, .12, 0), .05, .06, '#c9a040', rot=(0, 0, math.pi / 2)); cil((.08, .26, 0), .05, .06, '#c9a040', rot=(0, 0, math.pi / 2))
fim()
novo('lightning_rod')      # para-raios: haste alta de metal com ponta em bola e base
cil((0, 1.6, 0), .03, 3.2, '#8a8a90'); bola((0, 3.25, 0), .07, '#c9a040'); cil((0, .06, 0), .22, .12, '#5a5a62')
cil((0, 1.0, 0), .07, .08, '#5a5a62'); cil((0, 2.0, 0), .07, .08, '#5a5a62')
fim()
