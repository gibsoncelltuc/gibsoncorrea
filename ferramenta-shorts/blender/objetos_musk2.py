# Cybertruck real (perfil em triangulo, aco inox, barra de luz) e o "Not-a-Flamethrower" da Boring Company (corpo de fuzil preto + botijao). blender -b --python blender/objetos_musk2.py
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
INOX = '#c4c8ce'
novo('cybertruck')
prisma((0, 0, 0), [(-2.7, .45), (-2.75, .95), (-.35, 1.85), (2.8, .95), (2.8, .45), (2.2, .35), (-2.2, .35)], 2.0, INOX)   # o triangulo
prisma((0, .02, 0), [(-1.35, 1.32), (-.35, 1.76), (.8, 1.42), (-.9, 1.12)], 2.04, '#1b1d22')                                   # vidros
caixa((-2.76, .9, 0), (.05, .05, 1.9), '#f4fbff', 1.0)                                                                           # barra de luz na frente
caixa((2.81, .9, 0), (.05, .06, 1.9), '#ff3a3a', 1.0)                                                                            # barra de luz atras
for x in (-1.75, 1.8):
    for z in (-.95, .95):
        cil((x, .45, z), .45, .32, '#1b1b1f', rot=(m.pi / 2, 0, 0), lados=24)
        cil((x, .45, z + (.17 if z > 0 else -.17)), .3, .02, '#5a5e66', rot=(m.pi / 2, 0, 0), lados=8)
for z in (-1.02, 1.02): prisma((0, 0, z), [(-2.4, .38), (-2.2, .62), (2.3, .62), (2.5, .38)], .03, '#2a2c30')                   # saia escura
fim(0.01)
novo('flamethrower')                                   # Not-a-Flamethrower num suporte
caixa((0, .62, 0), (1.3, .14, .1), '#1b1b1f', 1.0)    # corpo
caixa((-.78, .58, 0), (.4, .2, .08), '#1b1b1f', 1.0, rot=(0, 0, -.1))   # coronha
cil((.85, .64, 0), .035, .5, '#3a3a40', rot=(0, 0, m.pi / 2))            # cano
cil((1.12, .64, 0), .05, .06, '#ff8a1a', rot=(0, 0, m.pi / 2))           # bico
caixa((.05, .48, 0), (.08, .2, .06), '#1b1b1f', 1.0, rot=(0, 0, .3))     # punho
caixa((.45, .74, 0), (.35, .05, .05), '#3a3a40', 1.0)                    # trilho de cima
cil((.3, .42, 0), .09, .42, '#e8e2d0', rot=(0, 0, m.pi / 2))             # botijao de propano embaixo
bola((.51, .42, 0), .09, '#e8e2d0', seg=10); bola((.09, .42, 0), .09, '#e8e2d0', seg=10)
torno((0, 0, 0), [(.3, 0), (.32, .04), (.05, .08), (.04, .3), (0, .32)], '#5a3a22', 16)
fim(0.006)
novo('searchlight')                                    # holofote antiaereo de 1942 (tambor claro, lente acesa)
torno((0, 0, 0), [(.6, 0), (.62, .08), (0, .1)], '#4a5236', 20)
for s in (-1, 1): caixa((s * .48, .6, 0), (.08, 1.0, .2), '#5a6440', 1.0)
cil((0, 1.05, 0), .45, .9, '#7a8458', rot=(m.pi / 2 - .5, 0, 0), lados=24)
cil((0, 1.05 + .35, .35), .42, .03, '#fff6c8', rot=(m.pi / 2 - .5, 0, 0), lados=24)
fim(0.01)
