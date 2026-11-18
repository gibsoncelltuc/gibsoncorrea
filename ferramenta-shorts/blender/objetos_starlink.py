# Starlink: satelite chato com um painel solar comprido (kit/starlink_sat) e a antena de casa "Dishy" retangular no pe (kit/starlink_dish). blender -b --python blender/objetos_starlink.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('starlink_sat')
caixa((0, .5, 0), (1.1, .7, .14), '#d9dce2')                   # corpo chato (bandeja prateada), de frente
caixa((0, .5, .08), (1.0, .6, .02), '#8d939d')                  # tampa escura
for i in range(6):                                              # painel solar comprido, em gomos azul-escuro
    caixa((.82 + i * .42, .5, 0), (.4, .62, .04), '#1f3f8a')
    caixa((.82 + i * .42, .5, .03), (.36, .56, .01), '#2f5fc4')
caixa((.62, .5, 0), (.16, .08, .08), '#c9ccd2')                 # braco do painel
bola((-.42, .72, .1), .06, '#ffcf3a')                           # luz dourada
fim(0.01)
novo('starlink_dish')
caixa((0, 0.05, 0), (.5, .1, .4), '#e8e8ea')                    # base
cil((0, .45, 0), .05, .8, '#d8d8dc')                            # mastro
caixa((0, 1.0, .05), (1.0, .08, .62), '#f2f2f4', rot=(-0.55, 0, 0))   # prato retangular branco inclinado
caixa((0, 1.0, .02), (.9, .02, .52), '#d0d4da', rot=(-0.55, 0, 0))
fim(0.02)
novo('starlink_train'); luz()                                  # o "trem" de luzes no ceu: fila diagonal de pontos brilhantes, alta (7 a 11 m)
for i in range(16):
    bola((-6 + i * .8, 7 + i * .26, 0), .16, '#fff6c8', seg=10)
    bola((-6 + i * .8, 7 + i * .26, -.05), .28, '#ffe680', seg=10, esc=(1, 1, .2))
fim(0.0)
