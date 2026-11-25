# 25/11 (Gibson: "fogo ja era para existir"): FOGO com LUZ PROPRIA. O antigo (cones laranja foscos) a noite parecia arvore de outono.
# Labaredas em linguas curvas, nucleo branco-amarelo, borda laranja-vermelha, tudo emissivo (brilha no escuro), brasas na base.
# blender -b --python blender/objetos_clima.py  -> web/assets/library/kit/fire.glb
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('fire')
luz(True)
def lingua(x, z, h, r, cor, fase):   # labareda em GOTA: bolas que afinam subindo e balancam para o lado (forma de chama, nao de cone)
    n = 13
    for i in range(n):
        t = i / (n - 1); rr = r * (1 - t) ** 0.8 + 0.02; dx = math.sin(t * 2.6 + fase) * 0.18 * t * h
        bola((x + dx, .05 + t * h, z), rr, cor, seg=12, esc=(1.0, 1.25, 1.0))
for x, z, h, r, fase in ((0, -.15, 2.0, .48, 0.0), (-.45, -.05, 1.5, .38, 1.2), (.48, -.1, 1.6, .4, 2.1), (-.2, -.35, 1.2, .3, .7), (.25, -.35, 1.25, .3, 2.9)):
    lingua(x, z, h, r, '#e8401e', fase)                  # vermelho atras
for x, z, h, r, fase in ((0, .05, 1.7, .4, .4), (-.38, .1, 1.25, .32, 1.6), (.4, .08, 1.35, .33, 2.5)):
    lingua(x, z, h, r, '#ff8c1a', fase)                  # laranja no meio
for x, z, h, r, fase in ((0, .3, 1.25, .3, .9), (-.28, .32, .85, .22, 2.2), (.3, .3, .95, .23, 3.1)):
    lingua(x, z, h, r, '#ffd84a', fase)                  # amarelo na frente
for x, z, h, r, fase in ((0, .46, .75, .17, 1.4), (-.18, .46, .5, .12, 2.6), (.2, .46, .55, .12, .3)):
    lingua(x, z, h, r, '#fffbe0', fase)                  # nucleo branco
for i in range(6): a = i * 1.05; bola((.42 * math.cos(a), .14, .32 * math.sin(a)), .1, '#fff3b0', seg=8)   # nucleo branco na base
luz(False)
for i in range(9): a = i * .7; bola((.85 * math.cos(a), .1, .62 * math.sin(a)), .14, '#2e2018', .6, seg=8)   # lenha/brasa escura em volta
luz(True)
for i in range(9): a = i * .7 + .3; bola((.78 * math.cos(a), .2, .56 * math.sin(a)), .05, '#ff5a1e', seg=6)   # brasas acesas
luz(False)
fim(0)
