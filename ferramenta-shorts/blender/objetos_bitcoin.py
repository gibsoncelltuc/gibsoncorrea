# 25/11 (Gibson: "fala que El Salvador tem fazendas de mineracao de bitcoin"): ESTANTE DE MINERACAO (as fazendas de El Salvador sao galpoes/containers
# com fileiras de estantes cheias de mineradoras ASIC: caixas cinza com 2 ventoinhas e luzes verdes, cabos). blender -b --python blender/objetos_bitcoin.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('rack_mineracao')
W, H, D = 1.6, 2.1, .6
for x in (-W / 2, W / 2):
    for z in (-D / 2, D / 2): caixa((x, H / 2, z), (.05, H, .05), '#3a3f48')            # colunas de aco
for k in range(5): caixa((0, .12 + k * .48, 0), (W + .06, .04, D + .06), '#4a505a')       # prateleiras
for k in range(4):
    y = .36 + k * .48
    for i in range(3):
        x = -W / 2 + .3 + i * .5
        caixa((x, y, 0), (.42, .3, .5), '#9aa3ad')                                       # mineradora ASIC (caixa de aluminio)
        for dx in (-.09, .09): cil((x + dx, y, .26), .085, .02, '#2a2d33', rot=(1.5708, 0, 0), lados=16); cil((x + dx, y, .275), .025, .01, '#6a707a', rot=(1.5708, 0, 0), lados=8)   # 2 ventoinhas na frente
        luz(True); bola((x + .17, y + .1, .26), .018, '#3aff7a', seg=6); bola((x + .17, y + .05, .26), .014, '#ffb43a', seg=6); luz(False)   # luzes acesas
tubo([(-W / 2 + .1, 2.05, -D / 2), (W / 2 - .1, 2.05, -D / 2)], .02, '#d8282f')            # cabos no alto
tubo([(-W / 2 + .1, 2.0, -D / 2 + .05), (W / 2 - .1, 2.0, -D / 2 + .05)], .02, '#2a5fd0')
fim(0)
