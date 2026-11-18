# Cachorro sentado (objeto heroi da Guerra do Cao Fugitivo): caramelo com orelhas caidas, coleira vermelha e plaquinha. blender -b --python blender/objetos_cachorro.py
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('dog_sit')
C, B, E = '#c98a4a', '#f2e2c8', '#3a2418'
bola((0, .32, -.05), .26, C, esc=(1, .9, 1.25))                       # quadril sentado
bola((0, .58, .08), .2, C, esc=(1, 1.3, 1))                           # peito
bola((0, .6, .2), .12, B, esc=(1, 1.4, .5))                           # peito claro
bola((0, .9, .14), .2, C)                                            # cabeca
bola((0, .85, .32), .1, B, esc=(1, .8, 1.2))                          # focinho
bola((0, .88, .43), .045, E, seg=10)                                    # nariz
for s in (-1, 1):
    bola((s * .18, .86, .1), .08, '#8a5a2a', esc=(.5, 1.6, .9))       # orelhas caidas
    bola((s * .07, .96, .3), .032, '#ffffff', seg=10); bola((s * .07, .96, .328), .02, E, seg=8)   # olhos
    tubo([(s * .09, .5, .15), (s * .09, .25, .2), (s * .09, .05, .24)], .06, C, passo=.35)          # patas da frente
    bola((s * .09, .04, .28), .055, B, esc=(1, .6, 1.3))              # pes
    bola((s * .2, .12, .0), .1, C, esc=(1, .6, 1.6))                   # patas de tras dobradas
tubo([(0, .2, -.32), (.12, .25, -.45), (.2, .4, -.5)], .035, C, passo=.35)   # rabo
torno((0, .72, .1), [(.15, 0), (.16, .03), (.15, .06)], '#d8282f', 20, tampa=False)   # coleira
cil((0, .66, .25), .035, .015, '#e8c45a', rot=(m.pi / 2, 0, 0))       # plaquinha
fim(0.005)
