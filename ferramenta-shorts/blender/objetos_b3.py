# Objetos da sessao B (3): bisturi cirurgico EM PE (legivel no quadro vertical). blender -b --python blender/objetos_b3.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('bisturi')
cil((0, .02, 0), .16, .04, '#6b5a4a', lados=14)                                     # base de apoio
cil((0, .45, 0), .06, .8, '#7b7f88', raio_topo=.05)                                 # cabo metalico grosso
cil((0, .88, 0), .075, .06, '#c8ccd2')                                              # anel do cabo
caixa((0, 1.18, 0), (.22, .6, .05), '#f2f4f7', afina=.55)                           # lamina larga
caixa((0, 1.56, 0), (.10, .2, .04), '#ffffff', afina=.15)                           # ponta afiada
caixa((.0, 1.2, .03), (.05, .55, .012), '#9aa0aa')                                  # fio de luz da lamina
fim(.012)
