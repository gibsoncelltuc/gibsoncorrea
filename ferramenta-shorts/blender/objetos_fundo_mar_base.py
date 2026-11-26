# 26/11 Videos longos Fundo do Mar: 8 criaturas (olham para +x, perfil). blender -b --python blender/objetos_fundo_mar.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
P = '#101014'; B = '#f4f4f0'

def olho(c, r, iris='#1b1b22', brilho=True):
    bola(c, r, B, seg=12); bola((c[0] + r * .45, c[1], c[2] + r * .5), r * .55, iris, seg=10)
    if brilho: luz(True); bola((c[0] + r * .6, c[1] + r * .25, c[2] + r * .75), r * .18, '#ffffff', seg=6); luz(False)

def dentes(x0, x1, y, z0, z1, n, h, para_baixo=True, col='#e8f0ff'):
    for i in range(n):
        t = i / max(1, n - 1); x = x0 + (x1 - x0) * t; z = z0 + (z1 - z0) * t
        cil((x, y - h / 2 if para_baixo else y + h / 2, z), h * .22, h, col, raio_topo=0.002, rot=(math.pi if para_baixo else 0, 0, 0), lados=6)

