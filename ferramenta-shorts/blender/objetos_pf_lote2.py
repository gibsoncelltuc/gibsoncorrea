# Poder e Fama lote 2: B-2, bomba antibunker, montanha-bunker, urna, Casa Branca, Falcon 9 pousando, Roadster no ar, mega-prisao, celular. blender -b --python blender/objetos_pf_lote2.py
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
from formas import _S
def ergue(dy):
    for v in _S['bm'].verts: v.co.z += dy
novo('b2_air')                                     # bombardeiro B-2 (asa voadora) ja no ceu
prisma((0, 0, 0), [(0, .9), (2.6, -.4), (2.2, -.6), (1.5, -.35), (.9, -.6), (0, -.35), (-.9, -.6), (-1.5, -.35), (-2.2, -.6), (-2.6, -.4)], .12, '#3a3e46')
caixa((0, .03, .25), (.5, .14, .5), '#2a2e36', 1.0)
for v in _S['bm'].verts: y, z = v.co.y, v.co.z; v.co.y, v.co.z = z, y          # deita a asa (planta vira horizontal)
ergue(7.0); fim(0.01)
novo('bunker_bomb')                                # bomba GBU-57 (close: deitada num suporte)
cil((0, .55, 0), .32, 3.2, '#6a7258', rot=(0, 0, m.pi / 2), lados=24)
torno((1.6, .55, 0), [(.32, 0), (.2, .5), (0, .62)], '#6a7258', 24) if False else bola((1.6, .55, 0), .32, '#6a7258', esc=(1.8, 1, 1))
for z in (-.3, .3):
    for a in (0, m.pi / 2): caixa((-1.55, .55, 0), (.05, .9, .05), '#4a5040', 1.0, rot=(a, 0, 0))
caixa((0, .55, .33), (.5, .12, .01), '#e8c23a', 1.0)
for x in (-.9, .9): caixa((x, .15, 0), (.25, .3, .7), '#3a3a40', 1.0)
fim(0.01)
novo('mountain_bunker')                            # montanha com os 2 respiros do bunker de Fordow
torno((0, 0, 0), [(5.5, 0), (4.5, 1.0), (3.0, 2.6), (1.6, 3.6), (.4, 4.0), (0, 4.05)], '#8a7a5a', 28)
for x in (-.8, .8): cil((x, 3.5, 1.0), .25, .6, '#3a3a40')
caixa((0, .6, 4.9), (2.0, 1.2, .4), '#6a6a72', 1.0)                                  # portao do tunel
caixa((0, .6, 5.05), (1.4, .9, .1), '#2a2a30', 1.0)
fim(0.02)
novo('ballot_box')                                 # urna de votacao com cedulas
caixa((0, .5, 0), (.7, .5, .5), '#f4f2ee', 1.0)
caixa((0, .78, 0), (.74, .06, .54), '#1f3f8a', 1.0)
caixa((0, .82, 0), (.3, .02, .04), '#1b1b1f', 1.0)
caixa((0, .5, .26), (.4, .2, .01), '#1f3f8a', 1.0); caixa((0, .5, .265), (.2, .08, .01), '#f4f2ee', 1.0)
caixa((.05, .95, 0), (.18, .22, .01), '#ffffff', 1.0, rot=(0, 0, .15))              # cedula entrando
torno((0, 0, 0), [(.5, 0), (.5, .25), (0, .26)], '#6a4426', 4)
fim(0.006)
novo('white_house')                                # Casa Branca (fachada com colunas)
caixa((0, 1.6, 0), (9.0, 3.2, 3.0), '#f4f2ee', 1.0)
caixa((0, 3.3, 0), (9.2, .3, 3.2), '#e8e4da', 1.0)
for i in range(6): cil((-1.75 + i * .7, 1.6, 1.9), .16, 3.2, '#ffffff')              # colunas do portico
prisma((0, 3.5, 2.0), [(-2.2, 0), (2.2, 0), (0, .9)], .3, '#f4f2ee')                 # frontao
for x in (-3.8, -2.8, 2.8, 3.8):
    for y in (1.0, 2.4): caixa((x, y, 1.51), (.5, .8, .02), '#3a4a6a', 1.0)
caixa((0, .9, 1.51), (.8, 1.4, .02), '#6a4426', 1.0)
cil((0, 4.4, 0), .04, 1.6, '#c8ccd2'); prisma((.42, 4.95, 0), [(-.38, .2), (.38, .2), (.38, -.2), (-.38, -.2)], .02, '#d8282f')   # mastro e bandeira
fim(0.02)
novo('falcon9_land')                               # Falcon 9 descendo de re, chama para baixo, pernas abertas, e a plataforma
cil((0, 4.5, 0), .4, 7.0, '#f4f2ee', lados=24)
for k in range(3): cil((0, 2.0 + k * 2.2, 0), .41, .08, '#2a2a30', lados=24)
for k in range(4):
    a = k * m.pi / 2 + .4; tubo([(.38 * m.cos(a), 1.4, .38 * m.sin(a)), (1.0 * m.cos(a), .6, 1.0 * m.sin(a))], .07, '#2a2a30', passo=.5)
    caixa((.45 * m.cos(a), 7.8, .45 * m.sin(a)), (.25, .3, .25), '#5a5a62', 1.0)
torno((0, -.3, 0), [(0, 0), (.3, .8), (.42, 1.6)], '#ff8a1a', 20); torno((0, .2, 0), [(0, 0), (.22, .6), (.3, 1.1)], '#ffe14a', 20)
ergue(2.2)
torno((0, 0, 0), [(2.4, 0), (2.4, .2), (0, .21)], '#6a6a72', 32)                     # plataforma de pouso
for r in (1.6, 1.0): torno((0, .21, 0), [(r, 0), (r + .1, 0.001)], '#f4f2ee', 32, tampa=False) if False else cil((0, .21, 0), r, .01, '#f4f2ee' if r == 1.6 else '#6a6a72', lados=32)
caixa((0, .23, 0), (1.2, .01, .25), '#f4f2ee', 1.0); caixa((0, .23, 0), (.25, .01, 1.2), '#f4f2ee', 1.0)   # o X
fim(0.01)
novo('prison')                                     # mega-prisao: muralha, guarita e pavilhoes
caixa((0, 1.5, 0), (12, 3.0, .5), '#9a9ea6', 1.0)
for x in (-6, 6): caixa((x, 2.6, 0), (1.0, 5.2, 1.0), '#7a7e86', 1.0); caixa((x, 5.4, 0), (1.4, .4, 1.4), '#5a5e66', 1.0)
for x in (-3, 0, 3): caixa((x, 2.2, -3), (2.4, 4.4, 4.0), '#b8bcc4', 1.0)
for i in range(24): cil((-5.8 + i * .5, 3.15, 0), .03, .3, '#4a4e56')               # arame no alto do muro
fim(0.02)
novo('phone')                                      # celular (selfie)
caixa((0, .75, 0), (.4, .8, .06), '#1b1b1f', 1.0); caixa((0, .75, .032), (.36, .72, .01), '#3a7ad8', 1.0)
cil((.12, 1.08, -.035), .04, .02, '#5a5e66', rot=(m.pi / 2, 0, 0))
torno((0, 0, 0), [(.15, 0), (.17, .03), (.04, .06), (.03, .35), (0, .36)], '#3a3a40', 16)
fim(0.004)
