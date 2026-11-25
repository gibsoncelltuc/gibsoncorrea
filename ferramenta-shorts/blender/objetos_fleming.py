# 25/11 Fleming: PLACA DE PETRI COM MOFO (Penicillium notatum, 1928): placa de vidro rasa, agar amarelado, colonia de mofo
# verde-azulada felpuda num lado, ANEL LIMPO em volta (bacterias sumiram) e colonias brancas de estafilococo longe dele
# (ref.: foto da placa original de Fleming, Museu de Ciencias de Londres). blender -b --python blender/objetos_fleming.py
import sys, os, math, random; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
random.seed(11)
novo('petri_mofo')
torno((0, 0, 0), [(.6, .0), (.64, .02), (.64, .16), (.6, .16)], '#dbeef5', 28, tampa=False)      # vidro
cil((0, .03, 0), .62, .06, '#c9dfe8'); cil((0, .07, 0), .58, .04, '#f2dca0')          # fundo + agar
mx, mz = -.2, .1
for i in range(22):                                                                  # mofo felpudo verde-azulado
    a = random.uniform(0, 2 * math.pi); r = random.uniform(0, .21)
    bola((mx + r * math.cos(a), .1, mz + r * math.sin(a)), random.uniform(.06, .1), random.choice(['#3f8f5a', '#5aa86a', '#2f7a6a', '#7cc07c']), .3, seg=8, esc=(1, .55, 1))
bola((mx, .13, mz), .07, '#e8f0d0', .3, seg=8, esc=(1, .5, 1))                       # borda clara do mofo
for i in range(110):                                                                 # colonias de bacteria FORA do anel limpo
    a = random.uniform(0, 2 * math.pi); r = random.uniform(0, .52); x, z = r * math.cos(a), r * math.sin(a)
    if math.hypot(x - mx, z - mz) < .36: continue
    bola((x, .09, z), random.uniform(.025, .045), '#fbf6e6', .4, seg=6, esc=(1, .5, 1))
fim(0)
