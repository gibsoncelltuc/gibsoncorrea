# CC 12 Tycho Brahe: nariz de metal (protese de latao) numa almofada sobre pedestal. blender -b --python blender/objetos_cc12.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('brass_nose')
torno((0, 0, 0), [(.28, 0), (.3, .05), (.18, .1), (.14, .5), (.22, .56), (.24, .62), (0, .62)], '#6a4426', 20)   # pedestal
bola((0, .7, 0), .3, '#b0282f', .3, esc=(1.2, 1, 1))                                                             # almofada
caixa((0, 1.05, .03), (.2, .34, .18), '#d9a630', .6, rot=(-.2, 0, 0))                                           # ponte do nariz
bola((0, .89, .13), .13, '#e8b84a', .9, esc=(1.1, 1, 1.05))                                                          # ponta
for x in (-1, 1): bola((x * .13, .85, .07), .09, '#d9a630', .8, esc=(1, 1, 1.2))                                    # abas
for x in (-1, 1): bola((x * .06, .8, .17), .04, '#4a3010', .7, seg=10)                                             # narinas
fim(0.01)
