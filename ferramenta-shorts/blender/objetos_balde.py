# Balde de madeira medieval (heroi da Guerra do Balde, 1325): aduelas de madeira, 3 aros de ferro, alca de corda. blender -b --python blender/objetos_balde.py
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('balde_madeira')
W, W2, FE, CO = '#8a5a2e', '#6f4522', '#3a3d42', '#c9a96a'
cil((0, .22, 0), .24, .44, W, raio_topo=.29, lados=14)                       # corpo de madeira (boca mais larga)
cil((0, .01, 0), .245, .03, W2, lados=14)                                    # fundo
for y, r in ((.06, .245), (.22, .26), (.40, .285)):
    torno((0, y, 0), [(r + .012, -.018), (r + .018, 0), (r + .012, .018)], FE, 20, tampa=False)   # aros de ferro
for i in range(14):
    a = 2 * m.pi * i / 14; cil((.255 * m.cos(a), .22, .255 * m.sin(a)), .006, .42, W2, lados=5)   # frestas entre as aduelas
arco((0, .44, 0), .27, CO, esp=.018, de=0.05, ate=m.pi - 0.05)                # alca de corda
fim(0.004)
