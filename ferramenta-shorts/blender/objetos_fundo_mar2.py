# 26/11 Fundo do Mar (parte 2): peixe-vibora, peixe-bolha, isopode-gigante. blender -b --python blender/objetos_fundo_mar2.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
from objetos_fundo_mar_base import olho, dentes

# PEIXE-VIBORA: corpo longo escuro, dentes enormes que nao cabem na boca, pontinhos de luz na barriga
novo('peixe_vibora')
bola((0, 0, 0), .26, '#1d2a3a', esc=(4.2, .9, .6))
bola((.98, .02, 0), .22, '#23344a', esc=(1.2, .9, .8))
bola((1.12, -.12, 0), .14, '#141e2a', esc=(1.4, .5, .7))
for i in range(4): x = 1.0 + i * .07; cil((x, .2, .06 if i % 2 else -.06), .02, .42, '#e9f4ff', raio_topo=.002, rot=(math.pi, 0, 0), lados=6)   # presas de cima, enormes, por fora da boca
for i in range(3): x = 1.05 + i * .08; cil((x, -.22, 0), .018, .32, '#e9f4ff', raio_topo=.002, lados=6)
olho((1.0, .12, .18), .07, '#0e1622'); olho((1.0, .12, -.18), .07, '#0e1622')
luz(True)
for i in range(10): bola((.85 - i * .17, -.18, .14), .022, '#59c8ff', seg=6); bola((.85 - i * .17, -.18, -.14), .022, '#59c8ff', seg=6)
luz(False)
tubo([(.3, .22, 0), (.5, .55, 0), (.62, .7, 0)], .015, '#2c3a4c')
prisma((-1.08, 0, 0), [(0, .12), (-.3, .3), (-.22, 0), (-.3, -.28), (0, -.1)], .04, '#1d2a3a')
fim(.01)

# PEIXE-BOLHA: corpo gelatinoso rosado, nariz caido, boca triste
novo('peixe_bolha')
bola((0, 0, 0), .45, '#e9b3b0', esc=(1.15, .85, .95))
bola((.4, -.02, 0), .18, '#dc9b98', esc=(1, 1.3, .9))                     # nariz caido
bola((.38, -.25, 0), .1, '#b9706e', esc=(1.4, .35, 1.2))                  # boca triste
olho((.32, .14, .2), .045); olho((.32, .14, -.2), .045)
prisma((-.55, -.05, 0), [(0, .15), (-.25, .2), (-.2, 0), (-.25, -.2), (0, -.15)], .04, '#dfa7a4')
fim(.01)

# ISOPODE-GIGANTE: "tatuzinho" gigante, placas segmentadas cinza-lilas, antenas, perninhas
novo('isopode_gigante')
for i in range(8):
    x = .75 - i * .2; r = .3 - abs(i - 3.5) * .02
    bola((x, .12, 0), r, '#b8b2c4' if i % 2 else '#a59fb3', esc=(.42, .55, 1.25))
bola((.95, .08, 0), .2, '#9c96aa', esc=(.7, .6, 1.0))
olho((1.05, .14, .16), .04, '#20202a', False); olho((1.05, .14, -.16), .04, '#20202a', False)
tubo([(1.1, .1, .08), (1.45, .25, .3), (1.7, .2, .45)], .015, '#8f899c'); tubo([(1.1, .1, -.08), (1.45, .25, -.3), (1.7, .2, -.45)], .015, '#8f899c')
for i in range(7):
    x = .7 - i * .2
    for s in (1, -1): tubo([(x, -.05, .25 * s), (x + .05, -.2, .42 * s)], .018, '#8f899c')
prisma((-.95, .08, 0), [(0, .2), (-.25, .1), (-.25, -.1), (0, -.2)], .06, '#a59fb3')
fim(.01)
