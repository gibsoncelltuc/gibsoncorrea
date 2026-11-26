# PF 18 Trump: The Game: mesa com o tabuleiro, a caixa em pe, dados e montinhos de dinheiro de mentira. blender -b --python blender/objetos_pf18.py
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('boardgame')
caixa((0, .72, 0), (1.5, .06, 1.0), '#7a4a26', 1.0)                                    # tampo da mesa
for (x, z) in ((-.65, -.4), (.65, -.4), (.65, .4), (-.65, .4)): torno((x, 0, z), [(.05, 0), (.06, .1), (.04, .4), (.05, .69), (0, .7)], '#6a4426', 12)   # pes torneados
caixa((0, .77, .05), (.8, .03, .8), '#1f5a3a', 1.0)                                    # tabuleiro
for i in range(9):                                                                      # casas coloridas na borda
    for (x, z) in ((-.36 + i * .09, -.31), (-.36 + i * .09, .41), (-.36, -.31 + i * .09 * 0.8), (.36, -.31 + i * .09 * 0.8)):
        caixa((x, .79, z), (.075, .01, .075), ['#d8282f', '#f2c21a', '#f4f1e8', '#1f4fa8'][i % 4], 1.0)
caixa((0, .795, .05), (.36, .01, .2), '#d9a630', 1.0)                                   # logotipo dourado no meio
caixa((0, .95, -.42), (.6, .34, .05), '#1b1b1f', 1.0, rot=(-.25, 0, 0))                 # caixa do jogo em pe
caixa((0, 1.0, -.39), (.44, .07, .01), '#d9a630', 1.0, rot=(-.25, 0, 0))                 # titulo dourado na caixa
for (x, z, r) in ((.25, .1, .3), (.33, .0, -.5)):
    caixa((x, .82, z), (.07, .07, .07), '#f4f1e8', 1.0, rot=(0, r, 0))                  # dados
for k in range(3):                                                                      # montinhos de notas de "milhoes"
    for j in range(6): caixa((-.55 + k * .12, .79 + j * .012, .35), (.1, .01, .06), '#7ab86a' if j % 2 else '#8ac87a', 1.0, rot=(0, .1 * k, 0))
fim(0.006)
