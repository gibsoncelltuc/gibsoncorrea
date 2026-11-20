# CC 15 Post-it: bloco amarelo de notas e o hinario do coral com marcadores colados. blender -b --python blender/objetos_cc15.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('postit')
caixa((-.3, .015, 0), (.95, .03, .72), '#7a1f2a', 1.0)                # capa de baixo do hinario
caixa((-.3, .205, 0), (.95, .03, .72), '#7a1f2a', 1.0)                # capa de cima
caixa((-.3, .11, -.345), (.95, .22, .04), '#6a1822', 1.0)             # lombada
caixa((-.32, .11, .0), (.9, .16, .66), '#f4ecd6', 1.0)                # paginas (aparecem na frente)
caixa((-.35, .224, 0), (.26, .008, .08), '#d9a630', 1.0)              # cruz dourada
caixa((-.35, .224, 0), (.08, .009, .36), '#d9a630', 1.0)
for i, x in enumerate((-.62, -.3, .02)):                               # marcadores amarelos saindo das paginas
    caixa((x, .12 + .03 * i, .4), (.18, .01, .2), '#ffd21a', 1.0)
for i in range(10):                                                    # bloco de notas ao lado
    caixa((.75, .015 + i * .03, .15), (.5, .03, .5), '#ffd21a' if i % 2 else '#f5c400', 1.0)
caixa((.75, .33, .15), (.5, .012, .5), '#ffdc3a', 1.0, rot=(.3, 0, 0))  # nota de cima levantando
fim(0.006)
