# bisturi EM PE (legivel no quadro vertical). blender -b --python blender/objetos_b5.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('bisturi')
cil((0, .02, 0), .22, .05, '#6b5a4a', lados=14)
cil((0, .5, 0), .11, .9, '#5c6f8a', raio_topo=.09)
cil((0, .98, 0), .13, .08, '#c9a227')
caixa((0, 1.35, 0), (.5, .7, .09), '#e9eef4', afina=.5)
caixa((0, 1.8, 0), (.22, .25, .07), '#ffffff', afina=.1)
caixa((0, 1.38, .06), (.12, .6, .02), '#a9b4c2')
fim(.02)
