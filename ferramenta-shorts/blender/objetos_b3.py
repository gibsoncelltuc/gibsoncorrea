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
# computador de mesa de 2002: monitor CRT bege, teclado e mouse
novo('computador_2002')
BEGE, ESC = '#d8d2bd', '#2b2e33'
caixa((0, .62, 0), (.8, .68, .62), BEGE)                                            # corpo do monitor de tubo
caixa((0, .62, -.34), (.5, .5, .4), BEGE, afina=.6)                                 # fundo afunilado do tubo
caixa((0, .66, .32), (.62, .5, .04), '#1f3a5c')                                     # tela azul
caixa((0, .66, .335), (.58, .46, .01), '#3a6aa8')                                   # brilho da tela
caixa((0, .24, .05), (.5, .1, .46), BEGE)                                           # pe do monitor
caixa((0, .06, .62), (.82, .06, .3), BEGE)                                          # teclado
for r in range(2):
    caixa((0, .095, .55 + r * .1), (.74, .02, .07), '#b9b3a0')                      # teclas
caixa((.62, .05, .62), (.12, .05, .18), BEGE)                                       # mouse
fim(.02)
