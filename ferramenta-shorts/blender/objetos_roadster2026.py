# Tesla Roadster 2026 (revelado em 15/out/2026): branco, cunha angulosa estilo Lotus Esprit / SR-71, cabine de vidro escuro, rodas grandes,
# propulsores de ar na traseira. Gera roadster26 (no chao) e roadster26_air (no ar, com jatos). blender -b --python blender/objetos_roadster2026.py
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
from formas import _S
W = '#f2f2f0'
def carro(dy, jatos):
    perfil = [(-2.15, .35), (-2.2, .62), (-1.2, .78), (-.55, 1.12), (.55, 1.18), (1.55, .82), (2.2, .52), (2.15, .3), (1.6, .25), (-1.6, .25)]   # silhueta lateral em cunha
    for z0, esp in ((0, 1.9),):
        prisma((0, dy, 0), perfil, esp, W)
    for v in _S['bm'].verts:                      # gira a silhueta: o comprimento fica de lado (x) e a largura em profundidade
        pass
    prisma((.1, dy + .03, 0), [(-.55, 1.13), (.55, 1.19), (1.4, .84), (-1.15, .8)], 1.94, '#1b2230')            # cabine de vidro escuro
    caixa((-2.18, dy + .5, 0), (.06, .06, 1.6), '#bfe6ff', 1.0)                                             # farol em barra (frente)
    caixa((2.18, dy + .45, 0), (.06, .06, 1.6), '#ff3a3a', 1.0)                                             # lanterna em barra (tras)
    for x in (-1.35, 1.35):
        for z in (-.92, .92):
            cil((x, dy + .38, z), .38, .26, '#1b1b1f', rot=(m.pi / 2, 0, 0), lados=24)                     # pneus
            cil((x, dy + .38, z + (.13 if z > 0 else -.13)), .24, .02, '#8a8e96', rot=(m.pi / 2, 0, 0), lados=12)   # roda
    for z in (-.97, .97): prisma((-.1, dy + .02, z), [(-1.0, .45), (.7, .55), (1.0, .38), (-.8, .33)], .04, '#2a2e36')   # entrada de ar lateral
    for z in (-.5, 0, .5): cil((2.2, dy + .55, z), .08, .12, '#3a3e46', rot=(0, 0, m.pi / 2))                # bocais dos propulsores
    if jatos:
        for (x, z) in ((-1.4, -.6), (1.4, -.6), (-1.4, .6), (1.4, .6)): torno((x, dy - 1.1, z), [(0, 0), (.16, .5), (.26, 1.1)], '#eef4ff', 14)
        for (x, z) in ((-1.6, 0), (1.6, 0), (0, .8)): bola((x, dy - 1.2, z), .35, '#f4f6fa', seg=10)
        for z in (-.5, 0, .5): torno((2.5, dy + .55, z), [(.0, 0), (.12, .4), (.2, .8)], '#eef4ff', 12)       # jato para tras
novo('roadster26'); carro(0, False); fim(0.02)
novo('roadster26_air'); carro(2.4, True); fim(0.02)
