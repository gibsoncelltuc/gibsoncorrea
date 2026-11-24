# 24/11: submarino moderno (classe Ohio/Virginia, sem bandeira japonesa) para o Martelo da Meia-Noite
# blender -b --python blender/objetos_martelo.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('submarino_moderno')   # casco preto comprido, torre (vela) com lemes de mergulho, leme em cruz na popa, metade fora d'agua
bola((0, 0.0, 0), 1.0, '#1f2226', esc=(10.0, 1.0, 1.0))
caixa((2.6, 1.55, 0), (2.2, 1.7, 0.7), '#1f2226', afina=0.85)
caixa((2.6, 1.9, 0), (3.2, 0.08, 0.12), '#2a2e33')
caixa((-9.3, 0.0, 0), (0.6, 1.6, 0.08), '#2a2e33'); caixa((-9.3, 0.0, 0), (0.6, 0.08, 1.6), '#2a2e33')
cil((2.9, 2.6, 0), 0.05, 0.8, '#2a2e33')
fim(0.04)
