# 25/11 Roadster (Gibson: "o palco, a plataforma tem que melhorar"): palco de lancamento de carro, estilo evento Tesla. blender -b --python blender/objetos_palco.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
PRETO = '#1c1d22'; GRAFITE = '#2c2f37'; CIANO = '#4fe3ff'; BRANCO = '#f2f4f8'; TELA1 = '#1f3a8a'; TELA2 = '#3b82f6'; METAL = '#8a8f99'
novo('palco_evento')
caixa((0, .25, 0), (16, .5, 9), PRETO)                     # plataforma principal (16 x 9 m, 50 cm de altura)
caixa((0, .51, 0), (15.2, .02, 8.2), GRAFITE)              # tampo fosco
caixa((0, .5, 4.52), (16, .06, .06), CIANO)                 # fita de LED na borda da frente
caixa((-8.02, .5, 0), (.06, .06, 9), CIANO); caixa((8.02, .5, 0), (.06, .06, 9), CIANO)   # bordas laterais
caixa((0, .26, 5.6), (6, .5, 2.4), GRAFITE, afina=1.0)     # rampa/degrau da frente
caixa((0, .52, 6.82), (6, .04, .05), CIANO)
caixa((0, 4.2, -4.3), (15, 7.4, .3), PRETO)                 # moldura do telao
caixa((0, 4.2, -4.12), (14.2, 6.6, .05), TELA1)             # telao
for i in range(6): caixa((0, 1.4 + i * 1.12, -4.08), (14.0, .45, .02), TELA2 if i % 2 else '#2b5bd8')   # faixas de luz no telao
caixa((0, 7.75, -4.1), (15.4, .12, .12), CIANO)            # LED no alto do telao
for x in (-8.6, 8.6):                                      # torres de trelica com refletores
    for dx in (-.3, .3):
        for dz in (-.3, .3): cil((x + dx, 4.5, -4.3 + dz), .06, 9, METAL, lados=8)
    for y in range(1, 9): caixa((x, y, -4.3), (.66, .05, .66), METAL)
    for k in range(3): cil((x, 8.2 - k * .6, -3.7), .22, .3, BRANCO, rot=(1.57, 0, 0), lados=12)
fim(0.01)
