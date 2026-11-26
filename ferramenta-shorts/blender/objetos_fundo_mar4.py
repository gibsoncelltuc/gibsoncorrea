# 26/11 Fundo do Mar (video 2): recife, Titanic no fundo, fonte hidrotermal, copo de isopor espremido. blender -b --python blender/objetos_fundo_mar4.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *

novo('recife_coral')   # zona da luz: coral colorido e peixinhos
caixa((0, -.15, 0), (3.2, .3, 1.6), '#d8c49a')
for i, (x, z, h, col) in enumerate([(-1.1, .2, .9, '#ff7a59'), (-.5, -.3, 1.2, '#ffb547'), (.2, .1, .8, '#e85a9c'), (.8, -.2, 1.1, '#7fd36b'), (1.2, .3, .7, '#ffa0b4')]):
    tubo([(x, 0, z), (x + .1, h * .5, z), (x - .05, h, z + .05)], .09, col); tubo([(x, h * .4, z), (x + .3, h * .75, z - .1)], .06, col)
for i in range(6): bola((-1.2 + i * .45, .9 + .2 * math.sin(i), .4 - (i % 2) * .6), .09, ['#ffd23a', '#3ac8ff', '#ff6b3a'][i % 3], esc=(1.8, 1, .6))
fim(.01)

novo('titanic_fundo')   # o casco da proa no fundo, enferrujado, com "pingentes" de ferrugem
caixa((0, .45, 0), (3.4, .9, .9), '#3b2a22', afina=.9)
prisma((1.7, .45, 0), [(0, -.45), (.55, .5), (0, .5)], .9, '#3b2a22')
caixa((0, .95, 0), (3.0, .1, .85), '#5a4436')
for i in range(5): cil((-1.2 + i * .55, 1.12, 0), .05, .3, '#4a382d')
for i in range(14): cil((-1.6 + i * .25, .1 + (i % 3) * .2, .46), .035, .25 + (i % 4) * .08, '#a5582a', raio_topo=.005, rot=(math.pi, 0, 0), lados=6)   # rusticles
caixa((0, -.05, 0), (4.0, .1, 1.6), '#2a2a2e')
fim(.02)

novo('fonte_hidrotermal')   # chamine preta soltando "fumaca" escura, vermes de tubo vermelhos em volta
torno((0, 0, 0), [(.6, 0), (.45, .5), (.35, 1.1), (.25, 1.7), (.3, 1.85)], '#2a2624', lados=18)
for i in range(5): bola((0, 2.0 + i * .28, 0), .22 + i * .08, '#1a1a1e', seg=10)
for i in range(16):
    a = i * 2 * math.pi / 16; r = .75 + (i % 3) * .12
    cil((r * math.cos(a), .35, r * math.sin(a)), .05, .7, '#f0ece4', lados=8); luz(False); bola((r * math.cos(a), .75, r * math.sin(a)), .09, '#d8282f', seg=8)
caixa((0, -.05, 0), (3.2, .1, 3.2), '#3a3430')
fim(.01)

novo('copo_isopor')   # o copo normal e o copo espremido pela pressao, lado a lado
torno((-.6, 0, 0), [(.28, 0), (.4, .9), (.42, .95)], '#f6f4ee', lados=24, tampa=False); torno((-.6, 0, 0), [(.01, 0), (.28, 0)], '#f6f4ee', lados=24, tampa=False)
torno((.6, 0, 0), [(.09, 0), (.13, .3), (.14, .32)], '#ece6d6', lados=24, tampa=False); torno((.6, 0, 0), [(.01, 0), (.09, 0)], '#ece6d6', lados=24, tampa=False)
fim(.005)
