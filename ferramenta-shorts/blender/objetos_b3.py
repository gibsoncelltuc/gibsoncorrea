# Objetos da sessao B (3): bisturi e seringa EM PE (legiveis no quadro vertical). blender -b --python blender/objetos_b3.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('bisturi')
cil((0, .02, 0), .22, .05, '#6b5a4a', lados=14)                                     # base de apoio
cil((0, .5, 0), .11, .9, '#5c6f8a', raio_topo=.09)                                  # cabo azul-aco grosso
cil((0, .98, 0), .13, .08, '#c9a227')                                               # anel dourado
caixa((0, 1.35, 0), (.5, .7, .09), '#e9eef4', afina=.5)                             # lamina larga e clara
caixa((0, 1.8, 0), (.22, .25, .07), '#ffffff', afina=.1)                            # ponta afiada
caixa((0, 1.38, .06), (.12, .6, .02), '#a9b4c2')                                    # fio de luz da lamina
fim(.02)
novo('seringa_pe')
cil((0, .06, 0), .13, .04, '#6b5a4a', lados=14)                                     # base
cil((0, .62, 0), .11, .95, '#cfe8f2', lados=18)                                     # corpo de vidro
cil((0, .62, 0), .075, .85, '#8fc4de', lados=18)                                    # liquido
cil((0, 1.15, 0), .16, .04, '#e8eaee', lados=18)                                    # aletas
cil((0, 1.35, 0), .03, .4, '#b9bec6', lados=10)                                     # haste
cil((0, 1.58, 0), .11, .05, '#e8eaee', lados=14)                                    # botao
fim(.012)
