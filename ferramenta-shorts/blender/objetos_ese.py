# Serie "E Se": Lua com crateras num pedestal, iceberg (parte de cima pequena, de baixo enorme), relogio de bolso. blender -b --python blender/objetos_ese.py
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('moon')
torno((0, 0, 0), [(.3, 0), (.32, .05), (.12, .1), (.08, .4), (0, .42)], '#3a3a44', 16)
bola((0, 1.0, 0), .6, '#c8c6c0', seg=28)
for (a, b, r) in ((.3, .4, .12), (-.35, .2, .09), (.1, -.25, .15), (-.2, .45, .07), (.42, -.1, .08), (-.4, -.3, .1)):
    x, y = .6 * m.sin(a) * 1.0, .6 * m.sin(b); z = (max(.6 ** 2 - x * x - y * y, .01)) ** .5
    bola((x, 1.0 + y, z - .03), r, '#9a9890', esc=(1, 1, .35), seg=12)
fim(0.01)
novo('iceberg')
pts = [(1.4, 0), (1.6, .6), (1.2, 1.4), (.6, 1.9), (0, 2.0)]
torno((0, 0, 0), [(1.0, 0), (1.2, .3), (.9, .9), (.5, 1.3), (0, 1.4)], '#eef6ff', 9)            # ponta fora d'agua
torno((0, -.05, 0), [(0, -2.6), (1.8, -2.2), (2.4, -1.0), (1.6, 0), (0, .01)], '#9fd0ec', 9)      # parte submersa (azul, enorme)
torno((0, 0, 0), [(2.6, 0), (2.6, .02), (0, .03)], '#2f6fae', 32)                                 # linha d'agua
fim(0.02)
