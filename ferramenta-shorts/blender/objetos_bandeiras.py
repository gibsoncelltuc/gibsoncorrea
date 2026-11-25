# 25/11 Uisque: bandeiras de PAIS no mastro (o war/flagpole tem pano listrado generico). blender -b --python blender/objetos_bandeiras.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
VERM = '#d52b1e'; BR = '#f7f7f2'
def mastro():
    cil((0, 2.0, 0), .05, 4.0, '#6b6b70'); bola((0, 4.05, 0), .09, '#d4af37'); cil((0, .06, 0), .32, .12, '#55555a')
W, H, Y0, X0 = 1.9, 1.2, 3.85, .06   # pano: largura, altura, topo, comeco junto ao mastro
novo('bandeira_canada'); mastro()
caixa((X0 + W * .125, Y0 - H / 2, 0), (W * .25, H, .03), VERM); caixa((X0 + W * .5, Y0 - H / 2, 0), (W * .5, H, .03), BR); caixa((X0 + W * .875, Y0 - H / 2, 0), (W * .25, H, .03), VERM)
cx, cy, s = X0 + W * .5, Y0 - H / 2, .44   # folha de bordo (silhueta) no meio
folha = [(0, 1), (.12, .72), (.3, .8), (.24, .42), (.5, .58), (.44, .38), (.62, .34), (.38, .08), (.44, -.04), (.08, .02), (.06, -.45), (-.06, -.45), (-.08, .02), (-.44, -.04), (-.38, .08), (-.62, .34), (-.44, .38), (-.5, .58), (-.24, .42), (-.3, .8), (-.12, .72)]
prisma((cx, cy, 0), [(x * s, y * s) for x, y in folha], .05, VERM)
fim(0.005)
novo('bandeira_dinamarca'); mastro()
caixa((X0 + W / 2, Y0 - H / 2, 0), (W, H, .03), VERM)
caixa((X0 + W * 14 / 37, Y0 - H / 2, 0), (W * 4 / 37, H, .045), BR); a, b = W * 12 / 37, W * 16 / 37; caixa((X0 + a / 2, Y0 - H / 2, 0), (a, H * 4 / 28, .045), BR); caixa((X0 + (b + W) / 2, Y0 - H / 2, 0), (W - b, H * 4 / 28, .045), BR)
fim(0.005)
