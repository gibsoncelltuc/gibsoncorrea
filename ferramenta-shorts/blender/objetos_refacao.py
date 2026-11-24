# 24/11: objetos que faltavam na conferencia frase a frase (Los Angeles: submarino japones; Toledo: minerio de cobre e ferro)
# blender -b --python blender/objetos_refacao.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('submarino_ww2')   # submarino japones classe I (1942): casco charuto, torre, canhao no convés, metade fora d'agua
bola((0, 0.0, 0), 1.0, '#3d4148', esc=(9.0, 1.0, 1.05))
caixa((0, 0.95, 0), (11.0, 0.12, 1.1), '#5a5f68')
caixa((1.2, 1.75, 0), (2.4, 1.6, 0.9), '#3d4148', afina=0.8)
caixa((1.2, 2.6, 0), (2.0, 0.12, 0.8), '#5a5f68')
cil((1.6, 3.2, 0), 0.06, 1.2, '#2a2d33'); cil((0.9, 3.0, 0), 0.05, 0.9, '#2a2d33')
cil((-2.6, 1.25, 0), 0.22, 0.4, '#2a2d33'); tubo([(-2.6, 1.4, 0), (-1.5, 1.55, 0)], 0.07, '#2a2d33')
caixa((1.2, 1.9, 0.46), (0.9, 0.5, 0.02), '#f4f4f2'); bola((1.2, 1.9, 0.48), 0.16, '#d8282f', esc=(1, 1, 0.2))
caixa((-8.6, 0.2, 0), (0.1, 1.2, 1.4), '#2a2d33')
fim(0.04)
novo('minerio')   # monte de minerio: pedras de cobre (alaranjado/verde) e ferro (cinza escuro)
import random; random.seed(3)
for i in range(16):
    a = random.uniform(0, 6.28); r = random.uniform(0, 0.55); y = 0.12 + random.uniform(0, 0.35) * (1 - r)
    col = ['#c46a2b', '#b5662f', '#3f8a6a', '#4a4d55', '#5b5e66', '#d98a3a'][i % 6]
    bola((r * math.cos(a), y, r * math.sin(a)), random.uniform(0.13, 0.22), col, esc=(1.2, 0.8, 1.0), seg=7)
fim(0.01)
