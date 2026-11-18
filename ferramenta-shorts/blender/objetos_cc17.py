# CC 17 Goodyear: fogao de ferro com a borracha queimada em cima (a vulcanizacao). blender -b --python blender/objetos_cc17.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('stove')
for x in (-.4, .4):
    for z in (-.25, .25): torno((x, 0, z), [(.05, 0), (.07, .05), (.04, .2), (.06, .24), (0, .25)], '#2a2a2e', 12)   # pes torneados
caixa((0, .5, 0), (1.0, .52, .66), '#34343a', 1.0)                       # corpo de ferro
caixa((0, .78, 0), (1.08, .05, .74), '#2a2a2e', 1.0)                     # tampo
caixa((0, .42, .335), (.34, .24, .02), '#1f1f24', 1.0)                   # portinhola
bola((.13, .42, .35), .025, '#b08a3a', seg=10)                            # puxador de latao
caixa((0, .42, .345), (.28, .03, .01), '#ff7a1a', 1.0)                   # brasa na fresta
for x in (-.25, .25): torno((x, .805, 0), [(.16, 0), (.17, .01), (.0, .015)], '#4a4a52', 20)        # bocas
cil((.38, 1.05, -.22), .07, .5, '#2a2a2e')                                 # chamine
for (x, z, r) in ((-.25, .02, .14), (-.12, .08, .1), (-.33, .12, .09), (-.18, -.1, .1)): bola((x, .83, z), r, '#1c1814', esc=(1.4, .35, 1.2))   # a borracha queimada, achatada como couro
cil((.12, .805, .18), .09, .08, '#e2c62a', raio_topo=.01)   # montinho de enxofre
fim(0.01)
