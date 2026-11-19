# PF 20 Teslaquila: garrafa de vidro em forma de raio, num suporte de metal. blender -b --python blender/objetos_pf20.py
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('tequila_bolt')
caixa((0, .03, 0), (.7, .06, .4), '#2a2a30', 1.0)                         # base de metal
for x in (-.18, .18): caixa((x, .3, 0), (.05, .5, .05), '#9a9ea6', 1.0, rot=(0, 0, .25 if x < 0 else -.25))   # bracos do suporte
caixa((0, .1, .205), (.16, .04, .01), '#d8282f', 1.0); caixa((0, .07, .205), (.04, .06, .01), '#d8282f', 1.0)  # "T" vermelho
V = '#e0a83a'                                                               # vidro com tequila dourada
prisma((0, 0, 0), [(.02, .12), (.2, .62), (.04, .62), (.16, 1.12), (-.12, 1.12), (-.2, .55), (-.04, .55), (-.12, .12)][::-1], .26, V)   # o raio (contorno)
cil((.02, 1.19, 0), .045, .14, '#e8e4da')                                   # gargalo
cil((.02, 1.29, 0), .055, .08, '#1b1b1f')                                   # tampa
fim(0.02)
