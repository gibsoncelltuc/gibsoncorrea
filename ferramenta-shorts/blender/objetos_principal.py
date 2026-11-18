# Objetos da SESSAO PRINCIPAL feitos com formas.py (redondos, chanfrados). blender -b --python blender/objetos_principal.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('cake_table')                                           # mesa de confeitaria com bolos REDONDOS
caixa((0, .86, 0), (2.4, .12, 1.1), '#a8703c'); caixa((0, .95, 0), (2.2, .06, .95), '#f4efe2')
for x in (-1.05, 1.05):
    for z in (-.42, .42): cil((x, .4, z), .07, .8, '#7a4a26')
cil((0, 1.0, 0), .5, .05, '#d9d2c0'); cil((0, 1.18, 0), .42, .3, '#f6c9d4'); cil((0, 1.35, 0), .44, .06, '#fff6f0')        # prato, massa, glace
cil((0, 1.52, 0), .28, .26, '#f6c9d4'); cil((0, 1.67, 0), .3, .05, '#fff6f0'); bola((0, 1.78, 0), .09, '#d8282f')          # 2o andar + cereja
for i in range(8): a = i * .785; bola((.36 * math.cos(a), 1.41, .36 * math.sin(a)), .05, '#fff6f0')                       # confeitos
cil((-.8, 1.1, .05), .27, .24, '#7a4a26'); cil((-.8, 1.24, .05), .29, .05, '#f4e3b0'); bola((-.8, 1.32, .05), .07, '#d8282f')   # bolo de chocolate
for x, z in ((.78, .18), (1.0, -.2), (.62, -.24)): bola((x, 1.05, z), .13, '#e8b46a', .6)                                 # paes doces
fim()
novo('kettle')                                               # chaleira de cobre: corpo no torno, bico inclinado, alca em arco
torno((0, 0, 0), [(.42, 0), (.56, .12), (.6, .4), (.5, .7), (.3, .86), (.3, .9)], '#c9743a'); cil((0, .93, 0), .32, .06, '#e8b46a'); bola((0, 1.02, 0), .08, '#2a2d33')
tubo([(.5, .5, 0), (.78, .68, 0), (.95, .92, 0)], .075, '#e8b46a'); arco((0, .9, 0), .34, '#2a2d33', .045)
fim()
novo('barrel_r')                                             # barril de verdade (bojudo) para destaque
torno((0, 0, 0), [(.36, 0), (.46, .25), (.5, .55), (.46, .85), (.36, 1.1)], '#9a6a3a')
for h in (.2, .55, .9): cil((0, h, 0), .49 if h == .55 else .45, .06, '#3a3d47')
fim()
