# PF 15 WrestleMania 23: ringue de luta (lona baixa, postes e cordas) e a maquina de raspar cabelo. blender -b --python blender/objetos_pf15.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('ring')
caixa((0, .04, 0), (6.4, .08, 6.4), '#e8e4da', 1.0)                      # lona (baixa, para os lutadores ficarem dentro)
caixa((0, .02, 0), (6.8, .04, 6.8), '#1f3f8a', 1.0)                      # saia azul
P = [(-3, -3), (3, -3), (3, 3), (-3, 3)]
for (x, z) in P:
    cil((x, .7, z), .09, 1.4, '#b8b8c0')                                 # poste
    for h in (.6, .95, 1.3): bola((x, h, z), .13, '#d8282f', esc=(1, .9, 1), seg=12)   # protetor do canto
for h, col in ((.6, '#d8282f'), (.95, '#f4f1e8'), (1.3, '#1f4fa8')):    # 3 cordas: vermelha, branca, azul
    for z in (-3, 3): cil((0, h, z), .035, 6.0, col, rot=(0, 0, math.pi / 2), lados=10)   # cordas lisas (cilindro deitado)
    for x in (-3, 3): cil((x, h, 0), .035, 6.0, col, rot=(math.pi / 2, 0, 0), lados=10)
fim(0.01)
novo('clipper')
caixa((0, .5, 0), (.34, .9, .24), '#2a2a30', 1.0)                         # corpo
bola((0, .95, 0), .17, '#2a2a30', esc=(1, .5, .7))                        # cabeca arredondada
caixa((0, 1.0, 0), (.38, .08, .26), '#c8ccd2', 1.0)                       # lamina
for i in range(7): caixa((-.15 + i * .05, 1.07, 0), (.02, .06, .24), '#e8ecf0', 1.0)   # dentes
caixa((0, .55, .125), (.08, .16, .02), '#d8282f', 1.0)                    # botao
tubo([(0, .05, 0), (.2, -.05, .1), (.5, -.02, .3)], .03, '#1b1b1f')       # fio
for (x, z) in ((-.5, .2), (-.6, -.1), (-.35, .35), (.4, -.3)): bola((x, .02, z), .07, '#5a3a22', esc=(1.4, .3, .8), seg=8)   # tufos de cabelo no chao
fim(0.008)
