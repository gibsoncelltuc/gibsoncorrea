# 26/11 Fundo do Mar (video 2): peixe-lanterna, peixe-caracol, batiscafo Trieste. blender -b --python blender/objetos_fundo_mar3.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
from objetos_fundo_mar_base import olho

# PEIXE-LANTERNA: pequeno, prateado, olhos grandes, fileiras de luz azul
novo('peixe_lanterna')
bola((0, 0, 0), .25, '#7e8fa6', esc=(2.4, 1, .6))
olho((.42, .06, .12), .09, '#0e1622'); olho((.42, .06, -.12), .09, '#0e1622')
luz(True)
for i in range(7): bola((.3 - i * .1, -.12, .13), .022, '#5fd0ff', seg=6); bola((.3 - i * .1, -.12, -.13), .022, '#5fd0ff', seg=6)
luz(False)
prisma((-.6, 0, 0), [(0, .1), (-.22, .24), (-.16, 0), (-.22, -.22), (0, -.1)], .03, '#6c7c92')
prisma((0, .24, 0), [(-.12, 0), (0, .12), (.12, 0)], .02, '#6c7c92')
fim(.01)

# PEIXE-CARACOL (hadal): corpo gelatinoso translucido rosado, cabeca larga, cauda afinando
novo('peixe_caracol')
bola((.2, 0, 0), .3, '#f1d4d6', esc=(1.2, .9, .9))
bola((-.3, -.02, 0), .22, '#ecc8cb', esc=(2, .7, .6))
bola((-.75, -.04, 0), .12, '#e7bfc3', esc=(2.4, .6, .4))
olho((.42, .1, .16), .035); olho((.42, .1, -.16), .035)
bola((.5, -.1, 0), .06, '#c98d93', esc=(1.4, .4, 1.2))
prisma((-.2, -.25, 0), [(.3, 0), (-.9, -.05), (-.9, .02)], .02, '#efcfd2')
fim(.01)

# BATISCAFO TRIESTE (1960): flutuador comprido cinza + esfera de aco embaixo com janelinha
novo('batiscafo_trieste')
bola((0, .45, 0), .5, '#c9ccd1', esc=(3.6, .9, .9))
caixa((0, .95, 0), (.8, .3, .35), '#b9bcc2')
cil((0, -.15, 0), .12, .3, '#7d828a')
bola((0, -.5, 0), .42, '#5f656e')
luz(True); bola((.0, -.5, .4), .09, '#ffe9a8', seg=10); luz(False)
for x in (-1.2, 1.2): caixa((x, .05, 0), (.08, .5, .08), '#8a8f97')
fim(.02)
