# 25/11 Curie: PECHBLENDA (uraninita), o minerio que Marie e Pierre moeram em toneladas: pedras PRETAS/marrom-escuras, brilho de piche,
# num monte grande no chao do galpao (refs.: amostras de pitchblende/uraninite em museus; galpao da rue Lhomond). blender -b --python blender/objetos_curie.py
import sys, os, math, random; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
random.seed(7)
novo('pechblenda')
for i in range(26):
    a = random.uniform(0, 2 * math.pi); r = random.uniform(0, .75) ** .8; h = max(0, .55 - r * .6)
    bola((r * math.cos(a), .12 + h * random.uniform(.6, 1.0), r * math.sin(a) * .8), random.uniform(.12, .22), random.choice(['#2a2622', '#3a302a', '#1f1d1c', '#4a3a2c']), seg=7, esc=(1.0, random.uniform(.7, 1.0), random.uniform(.8, 1.2)))
for i in range(5): bola((random.uniform(-.5, .5), .45 + random.uniform(0, .15), random.uniform(-.3, .3)), .05, '#6a6a5a', seg=6)   # reflexo de piche
fim(0)
