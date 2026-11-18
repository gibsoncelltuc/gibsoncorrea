# PF 16 Starship: torre de lancamento com os bracos ("pauzinhos") e o propulsor. Gera 3: tower_catch (foguete preso nos bracos), tower (torre vazia), booster_air (foguete descendo com fogo). blender -b --python blender/objetos_pf16.py
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
def torre(braco_y):
    caixa((0, .15, 0), (3.2, .3, 3.2), '#8a8a90', 1.0)                         # base de concreto
    for (x, z) in ((-.6, -.6), (.6, -.6), (.6, .6), (-.6, .6)): caixa((x - 1.6, 4.3, z), (.16, 8.2, .16), '#3a3a40', 1.0)   # 4 colunas da torre
    for i in range(16):                                                            # trelica em X
        y = .5 + i * .5
        for z in (-.6, .6): caixa((-1.6, y, z), (1.2, .06, .06), '#4a4a52', 1.0, rot=(0, 0, .4 if i % 2 else -.4))
        for x in (-2.2, -1.0): caixa((x, y, 0), (.06, .06, 1.2), '#4a4a52', 1.0, rot=(.4 if i % 2 else -.4, 0, 0))
    caixa((-1.6, 8.5, 0), (1.4, .3, 1.4), '#2a2a30', 1.0)                         # topo
    caixa((-1.0, braco_y, 0), (.5, .7, .9), '#5a5a62', 1.0)                         # carrinho dos bracos
    for z in (-.55, .55): caixa((.3, braco_y, z), (2.6, .32, .22), '#d8d8de', 1.0)    # os dois "pauzinhos"
def foguete(y0, fogo):
    cil((.3, y0 + 3.0, 0), .45, 6.0, '#c8ccd2', lados=24)                         # propulsor de aco inox
    torno((.3, y0 + 6.0, 0), [(.45, 0), (.43, .15), (0, .18)], '#b8bcc2', 24)
    for k in range(4): a = k * m.pi / 2 + .4; caixa((.3 + .55 * m.cos(a), y0 + 5.6, .55 * m.sin(a)), (.22, .3, .22), '#5a5a62', 1.0)   # aletas de grade
    for k in range(3): cil((.3, y0 + 1.0 + k * 1.6, 0), .46, .06, '#9a9ea6', lados=24)                                            # aneis de solda
    if fogo:
        torno((.3, y0 - 1.6, 0), [(0, 0), (.25, .6), (.4, 1.4), (.35, 1.6)], '#ff8a1a', 20)   # chama
        torno((.3, y0 - .9, 0), [(0, 0), (.2, .5), (.28, .9)], '#ffe14a', 20)
novo('tower_catch'); torre(6.4); foguete(3.3, False); fim(0.02)
novo('tower'); torre(6.4); fim(0.02)
novo('booster_air'); foguete(6.0, True); fim(0.02)
