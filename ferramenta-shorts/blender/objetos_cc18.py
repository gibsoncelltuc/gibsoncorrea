# (com -- balloon_air 2.5 gera o balao ja no ar)
# CC 18 Montgolfier: balao de ar quente azul e dourado com a cesta-gaiola dos bichos. blender -b --python blender/objetos_cc18.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
NOME, DY = (sys.argv[sys.argv.index('--') + 1], float(sys.argv[sys.argv.index('--') + 2])) if '--' in sys.argv else ('balloon', 0.0)
novo(NOME)
import math as m
def raio(t): return .16 + .5 * m.sin(min(t, .75) / .75 * m.pi / 2) if t < .75 else .66 * m.cos((t - .75) / .25 * m.pi / 2) ** .6
Y0, H = 0.7 + DY, 1.6; cores = ['#1f4fa8', '#1f4fa8', '#d9a630', '#1f4fa8', '#1f4fa8', '#1f4fa8', '#d9a630', '#1f4fa8', '#1f4fa8', '#1f4fa8']
for i in range(10):                                                                  # envelope em faixas (azul real com dourado)
    t0, t1 = i / 10, (i + 1) / 10
    pf = [(raio(t0 + (t1 - t0) * k / 3), H * (t0 + (t1 - t0) * k / 3) - H * t0) for k in range(4)]
    if i == 9: pf[-1] = (0, pf[-1][1])
    torno((0, Y0 + H * t0, 0), pf, cores[i], 28, tampa=(i == 9))
for k in range(8):                                                                   # flores-de-lis douradas (bolinhas) na faixa larga
    a = 2 * m.pi * k / 8; bola((.67 * m.cos(a), Y0 + H * .62, .67 * m.sin(a)), .05, '#d9a630', seg=10)
torno((0, DY, 0), [(.26, 0), (.28, .3), (.26, .32), (0, .32)], '#8a6a3a', 20)        # cesta de vime
for k in range(4):                                                                   # cordas da cesta ao balao
    a = 2 * m.pi * k / 4 + .4; tubo([(.26 * m.cos(a), DY + .32, .26 * m.sin(a)), (.17 * m.cos(a), Y0, .17 * m.sin(a))], .012, '#c9b48a')
fim(0.01)
