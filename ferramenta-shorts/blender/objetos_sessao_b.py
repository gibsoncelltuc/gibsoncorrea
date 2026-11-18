# Objetos da sessao B feitos com formas.py (formas redondas): blender -b --python blender/objetos_sessao_b.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
H = (0, 0, math.pi / 2)    # deita o cilindro ao longo do eixo x
novo('syringe')            # seringa antiga de vidro: corpo, liquido, aletas, embolo, ponta e agulha longa
cil((0, .3, 0), .17, 1.3, '#d4eaf0', rot=H); cil((0, .3, 0), .125, 1.1, '#6fb8d6', rot=H)
cil((-.68, .3, 0), .3, .05, '#8a8a8a', rot=H); cil((-1.0, .3, 0), .045, .7, '#9a9a9a', rot=H); cil((-1.38, .3, 0), .2, .07, '#7a7a7a', rot=H)
cil((.76, .3, 0), .1, .22, '#a8a8a8', raio_topo=.04, rot=H); cil((1.3, .3, 0), .028, .85, '#e2e2e2', rot=H)
fim()
