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
def _tulipa(x, z, c1, c2, h=1.0, s=1.0):                      # haste fina, 2 folhas curvas, calice em gota com 3 petalas
    cil((x, .5 * h * s, z), .03 * s, h * s, '#3f8a3a')
    bola((x - .13 * s, .36 * h * s, z), .1 * s, '#4fa84a', 2.6, rot=(0, .35, 0), seg=10); bola((x + .13 * s, .3 * h * s, z), .09 * s, '#5fb85a', 2.4, rot=(0, -.35, 0), seg=10)   # folhas largas
    torno((x, h * s, z), [(.02 * s, 0), (.15 * s, .08 * s), (.19 * s, .22 * s), (.15 * s, .36 * s), (.07 * s, .44 * s)], c1, 14)
    for a in (0, 2.09, 4.19): bola((x + .1 * s * math.cos(a), (h + .4) * s, z + .1 * s * math.sin(a)), .08 * s, c2, 1.5)
def _vaso(): torno((0, 0, 0), [(.2, 0), (.26, .05), (.34, .5), (.38, .56), (.38, .6), (.3, .6)], '#c2703a'); cil((0, .58, 0), .3, .04, '#4a3222')
for nm, c1, c2 in (('tulip_red', '#e2332f', '#f0564a'), ('tulip_yellow', '#f2c230', '#ffe07a'), ('tulip_purple', '#8a3fb5', '#b06ad6'), ('tulip_striped', '#f4f0e6', '#d8282f')):
    novo(nm); _vaso(); _tulipa(0, 0, c1, c2, h=1.15, s=1.25); fim(0.015)
novo('tulip_bed'); caixa((0, .18, 0), (5.2, .36, 1.3), '#8a5a34'); caixa((0, .37, 0), (4.9, .06, 1.0), '#4a3222')
for i, (c1, c2) in enumerate([('#e2332f', '#f0564a'), ('#f2c230', '#ffe07a'), ('#8a3fb5', '#b06ad6'), ('#f4f0e6', '#d8282f'), ('#f08a2a', '#ffb060'), ('#e2332f', '#f0564a'), ('#f2c230', '#ffe07a'), ('#d84a8a', '#f08ab5')]): _tulipa(-2.1 + i * .6, (.22 if i % 2 else -.22), c1, c2, h=.8 + .12 * (i % 3), s=1.0)
fim(0.015)
novo('ball'); bola((0, .42, 0), .42, '#f4f1e8')                                                                          # bola de futebol: esfera lisa com gomos pretos
for a, b in ((0, 0), (1.26, .9), (2.51, -.9), (3.77, .9), (5.03, -.9), (0, 2.2), (2.1, 2.2), (4.2, 2.2), (0, -2.2), (3.1, -2.2), (1.5, 0), (4.6, 0)):
    cb = math.cos(b * .7); bola((.4 * math.cos(a) * cb, .42 + .4 * math.sin(b * .7), .4 * math.sin(a) * cb), .12, '#22252c', .5)
fim(0)
novo('campfire')                                                                                                        # fogueira: pedras redondas, lenha em tubo, chama em gota
for i in range(8): a = i * .785; bola((.55 * math.cos(a), .1, .55 * math.sin(a)), .15, '#8d8d86', .7)
tubo([(-.45, .14, -.1), (.45, .2, .1)], .07, '#6a4426'); tubo([(-.1, .16, -.45), (.1, .22, .45)], .07, '#7a4a26'); tubo([(-.35, .15, .3), (.3, .3, -.25)], .06, '#6a4426')
torno((0, .2, 0), [(.02, 0), (.26, .12), (.3, .32), (.18, .62), (.02, .9)], '#f08a2a', 12); torno((.05, .22, .04), [(.02, 0), (.15, .1), (.17, .26), (.08, .5), (.01, .66)], '#f2c230', 10); torno((-.14, .2, -.08), [(.02, 0), (.12, .08), (.12, .2), (.02, .42)], '#e2332f', 10)
fim(0)
novo('tent'); cil((0, 1.0, 0), 1.5, 2.0, '#e8dcc0', .05, lados=10); caixa((0, .6, 1.3), (.7, 1.2, .1), '#4a3a2a', .3); cil((0, 2.15, 0), .04, .4, '#6a4426'); caixa((.16, 2.25, 0), (.3, .16, .02), '#d8282f'); fim()   # tenda em cone
novo('chest'); caixa((0, .3, 0), (1.1, .6, .7), '#8a5a34'); bola((0, .6, 0), .36, '#a8703c', esc=(1.55, .8, 1.0))                                   # bau de tampa abaulada
for x in (-.4, .4): caixa((x, .3, 0), (.1, .62, .74), '#d9a630'); bola((x, .6, 0), .37, '#d9a630', esc=(.16, .8, 1.02))
bola((0, .55, .37), .08, '#f2d060'); fim()
novo('fire')                                                   # FOGO/incendio: labaredas grandes (sem pedras), para "queimaram", "pegou fogo", "em chamas"
for x, z, s, c in ((0, 0, 1.0, '#f08a2a'), (-.45, .1, .75, '#e2532f'), (.5, -.05, .8, '#f08a2a'), (.1, .25, .6, '#f2c230'), (-.15, -.2, .55, '#f2c230'), (.3, .3, .45, '#ffe07a')):
    torno((x, 0, z), [(.05 * s, 0), (.5 * s, .25 * s), (.55 * s, .7 * s), (.36 * s, 1.3 * s), (.14 * s, 1.9 * s), (.02 * s, 2.3 * s)], c, 12)
for i in range(7): a = i * .9; bola((.8 * math.cos(a), .12, .6 * math.sin(a)), .14, '#3a2a22', .6, seg=8)
fim(0)
