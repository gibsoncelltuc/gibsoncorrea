# 26/11 Videos longos Espaco: Saturno, Encelado, Tita, sonda Cassini, Plutao, Caronte, New Horizons. blender -b --python blender/objetos_espaco.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *

def planeta_faixas(c, r, cores, lados=40):   # esfera feita de faixas de latitude (uma cor por faixa)
    n = len(cores)
    for k, col in enumerate(cores):
        a0 = -math.pi / 2 + math.pi * k / n; a1 = -math.pi / 2 + math.pi * (k + 1) / n
        perf = [(r * math.cos(a0 + (a1 - a0) * j / 4), r * math.sin(a0 + (a1 - a0) * j / 4)) for j in range(5)]
        torno(c, perf, col, lados=lados, tampa=False)

def anel(c, r0, r1, col, lados=72): torno(c, [(r0, 0), (r1, 0)], col, lados=lados, tampa=False); torno(c, [(r1, -0.001), (r0, -0.001)], col, lados=lados, tampa=False)

novo('saturno')
planeta_faixas((0, 0, 0), 1.0, ['#c9b07a', '#d8c08a', '#e3cf9a', '#d9b97e', '#e8d6a6', '#cfae74', '#e2cc98', '#d6bb84', '#c4a46c', '#b89c66'])
for r0, r1, col in [(1.25, 1.5, '#b9a684'), (1.52, 1.95, '#e0d2b0'), (1.99, 2.05, '#3a3428'), (2.07, 2.3, '#cbbd9c')]: anel((0, 0, 0), r0, r1, col)
hx = [(.34 * math.cos(i * math.pi / 3), .945, .34 * math.sin(i * math.pi / 3)) for i in range(7)]; tubo(hx, .022, '#6f8796', passo=.6)   # o hexagono no polo: contorno colado na esfera
fim(0)

novo('encelado')
planeta_faixas((0, 0, 0), 1.0, ['#e8f2f8', '#f4f8fb', '#ffffff', '#f2f7fa', '#e6eef4'], lados=32)
import random; random.seed(7)
for gx, gz in [(-.22, .1), (0, -.05), (.22, .12)]:   # jatos dos geiseres do polo sul: spray de graozinhos de gelo abrindo em leque
    for k in range(40):
        d = random.random() ** .7 * 1.3; sp = .04 + d * .22
        bola((gx * (1 + d) + random.uniform(-sp, sp), -.96 - d, gz * (1 + d) + random.uniform(-sp, sp)), .018 + .012 * random.random(), '#e6f3fa', seg=6)
fim(0)

novo('tita')
planeta_faixas((0, 0, 0), 1.0, ['#c47a2c', '#d78a34', '#e09a42', '#d58833', '#c27326'], lados=32)
torno((0, 0, 0), [(max(.01, 1.07 * math.cos(-math.pi / 2 + math.pi * j / 16)), 1.07 * math.sin(-math.pi / 2 + math.pi * j / 16)) for j in range(17)], '#e9a44c', lados=40, tampa=False)   # nevoa da atmosfera
fim(0)

novo('sonda_cassini')
cil((0, 0, 0), .35, 1.1, '#c9a24a', lados=16)                        # corpo dourado (manta termica)
cil((0, .7, 0), .9, .12, '#e7e9ee', raio_topo=.05, lados=28)         # antena parabolica
cil((0, .8, 0), .04, .3, '#bfc3ca')
tubo([(.35, 0, 0), (1.9, .1, 0)], .025, '#9aa0a8')                    # mastro do magnetometro
cil((-.45, -.2, 0), .12, .5, '#5b5f66', rot=(0, 0, math.pi / 2))     # gerador
fim(.01)

novo('plutao')
planeta_faixas((0, 0, 0), 1.0, ['#8a6a55', '#a88a72', '#c9ab8f', '#bda087', '#9c7c64', '#7d5f4c'], lados=40)
bola((.15, -.05, .93), .42, '#f3ead8', esc=(1.15, 1, .25))            # o coracao (Tombaugh Regio)
bola((-.25, .05, .9), .32, '#efe3cc', esc=(1, 1.1, .25))
bola((-.7, -.2, .55), .28, '#5a3e32', esc=(1, .7, .3))                 # Cthulhu (regiao escura)
fim(0)

novo('caronte')
planeta_faixas((0, 0, 0), 1.0, ['#7a2c22', '#8f8478', '#a39a90', '#9b9187', '#8a7f73'], lados=32)   # polo norte avermelhado
fim(0)

novo('new_horizons')
caixa((0, 0, 0), (.7, .45, .55), '#d9b45a')                            # corpo (manta dourada)
cil((0, .45, 0), .62, .1, '#eef0f4', raio_topo=.05, lados=28)          # antena grande
cil((-.6, 0, 0), .12, .6, '#4f535a', rot=(0, 0, math.pi / 2))           # gerador RTG
fim(.01)
