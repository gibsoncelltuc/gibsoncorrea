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
# seringa em pe (cilindro de vidro + extrator + agulha), legivel no quadro vertical
novo('seringa_pe')
cil((0, .06, 0), .13, .04, '#6b5a4a', lados=14)                                     # base
cil((0, .62, 0), .11, .95, '#cfe8f2', lados=18)                                     # corpo de vidro
cil((0, .62, 0), .075, .85, '#8fc4de', lados=18)                                    # liquido
cil((0, 1.15, 0), .16, .04, '#e8eaee', lados=18)                                    # aletas de apoio
cil((0, 1.35, 0), .03, .4, '#b9bec6', lados=10)                                     # haste do embolo
cil((0, 1.58, 0), .11, .05, '#e8eaee', lados=14)                                    # botao do embolo
cil((0, .0, 0), .01, .01, '#9aa0aa', lados=6)
fim(.012)
