# Objetos da sessao B (3): bisturi cirurgico. blender -b --python blender/objetos_b3.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
P = math.pi / 2
novo('bisturi')
cil((-.30, .06, 0), .035, .46, '#9aa0aa', raio_topo=.028, rot=(0, 0, P))        # cabo metalico
cil((-.05, .06, 0), .028, .08, '#c8ccd2', raio_topo=.02, rot=(0, 0, P))          # encaixe
caixa((.20, .06, 0), (.34, .03, .012), '#e8eaee', afina=.7)                      # lamina
caixa((.40, .06, 0), (.10, .018, .010), '#ffffff', afina=.3)                     # ponta afiada
caixa((.18, .075, 0), (.30, .005, .014), '#b9bec6')                              # fio de luz
fim(.01)
