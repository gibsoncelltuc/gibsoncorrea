# 25/11 (Gibson: "a banheira tem que ter cor propria, todo mundo tem que ver que e' uma banheira"): banheira classica de porcelana
# BRANCA brilhante, borda dourada, agua AZUL forte com espuma, pes dourados e torneira de metal. blender -b --python blender/objetos_banheira.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('bathtub')
luz(True); bola((0, .4, 0), .5, '#ffffff', esc=(1.9, .8, 1.0)); luz(False)                        # porcelana branca (brilha um pouco: nunca some no piso)
bola((0, .42, .0), .505, '#cfe6f7', esc=(1.88, .2, .99))                                           # faixa azul-clara no meio do corpo
bola((0, .76, 0), .46, '#1f8fe8', esc=(1.8, .14, .9))                                              # agua azul forte
for i in range(30): a = i * math.pi / 15; bola((.9 * math.cos(a), .78, .47 * math.sin(a)), .075, '#e8b830', seg=8)   # borda dourada
for x, z in ((-.35, .1), (.15, -.12), (.45, .15), (-.05, .18)): bola((x, .86, z), .1, '#ffffff', seg=8)   # espuma
for x in (-.6, .6):
    for z in (-.3, .3): bola((x, .1, z), .12, '#e8b830')                                            # pes dourados
tubo([(.8, .6, 0), (.8, 1.0, 0), (.6, 1.05, 0)], .045, '#9aa3b0'); fim(0)
