# magnetron do radar (caixa de aco com aletas, flange dourada e antena). blender -b --python blender/objetos_b6.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('magnetron')
cil((0, .06, 0), .55, .12, '#4a4f57', lados=24)
cil((0, .55, 0), .32, .9, '#7d8590', lados=24)
for k in range(7):
    cil((0, .22 + k * .12, 0), .48, .05, '#aeb6c0', lados=24)
caixa((.5, .58, 0), (.5, .34, .34), '#5b6470')
cil((.82, .58, 0), .12, .18, '#c9a227', rot=(0, 0, math.pi / 2), lados=16)
cil((0, 1.25, 0), .14, .18, '#c9a227', lados=16)
cil((0, 1.62, 0), .035, .6, '#d9dde2', lados=10)
bola((0, 1.95, 0), .07, '#e84a3a')
fim(.02)
