# CC 19 Marie Curie: caixa de chumbo aberta com o caderno e o frasquinho de radio brilhando. blender -b --python blender/objetos_cc19.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('curie_box')
caixa((0, .16, 0), (.9, .32, .62), '#6a6e76', 1.0)                       # caixa de chumbo
caixa((0, .33, 0), (.82, .02, .54), '#4a4e56', 1.0)                       # fundo interno escuro
caixa((0, .6, -.4), (.9, .04, .62), '#7a7e86', 1.0, rot=(1.25, 0, 0))    # tampa aberta
caixa((-.15, .37, .02), (.46, .1, .36), '#5a3a22', 1.0, rot=(0, .12, 0)) # caderno de capa marrom
caixa((-.15, .425, .02), (.42, .012, .32), '#efe6c8', 1.0, rot=(0, .12, 0))  # paginas
for i in range(5): caixa((-.15, .434, -.08 + i * .05), (.3, .003, .012), '#3a3a6a', 1.0, rot=(0, .12, 0))  # linhas escritas
torno((.3, .34, .05), [(.06, 0), (.065, .02), (.06, .2), (.03, .24), (.035, .3), (0, .3)], '#7dffa0', 16)   # frasco de vidro
torno((.3, .35, .05), [(.05, 0), (.05, .12), (0, .12)], '#5cff7a', 16)    # radio brilhando (verde)
cil((.3, .65, .05), .04, .05, '#7a5a3a')                                   # rolha
caixa((0, .2, .315), (.4, .14, .01), '#e8d23a', 1.0)                       # etiqueta de perigo
for a in range(3):
    import math as m; ang = m.pi / 2 + a * 2 * m.pi / 3
    bola((.0 + .045 * m.cos(ang), .2 + .045 * m.sin(ang), .325), .03, '#1b1b1f', seg=8)   # simbolo radioativo
fim(0.006)
