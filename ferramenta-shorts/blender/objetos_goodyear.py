# 25/11 Goodyear (decadas depois: bolas): bola de COURO do seculo 19 (ref.: Sport Antiques, bola de couro marrom de gomos costurados).
# A bola moderna de gomos pretos e brancos (anos 1970) e' fora de epoca. blender -b --python blender/objetos_goodyear.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('bola_couro')
R = .41   # mesmo tamanho de desenho da kit/ball (o motor usa a bola grande para ler na tela)
bola((0, R, 0), R, '#8a4f24', seg=24)                                     # couro marrom
for k in range(6):                                                         # costuras dos gomos (meridianos)
    a = k * math.pi / 6; tubo([(R * 1.01 * math.sin(t) * math.cos(a), R + R * 1.01 * math.cos(t), R * 1.01 * math.sin(t) * math.sin(a)) for t in [i * math.pi / 12 for i in range(13)]], .014, '#5a3014')
tubo([(R * 1.01 * math.cos(t), R, R * 1.01 * math.sin(t)) for t in [i * math.pi / 12 for i in range(25)]], .014, '#5a3014')   # costura do meio
fim(0)
