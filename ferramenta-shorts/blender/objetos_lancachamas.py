# 25/11 Lanca-chamas: BOCA DE TUNEL da Boring Company (Hawthorne, 2018): portal redondo de concreto cinza, tubo escuro por dentro,
# trilho de luzes brancas no teto (ref.: fotos do tunel de teste de Hawthorne). blender -b --python blender/objetos_lancachamas.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('tunel_boring')
cil((0, 1.6, 0), 2.0, 0.8, '#a9adb2', rot=(math.pi / 2, 0, 0), lados=28)       # anel de concreto (portal)
cil((0, 1.6, 0.05), 1.65, 0.82, '#15161a', rot=(math.pi / 2, 0, 0), lados=28)  # boca escura
caixa((0, 0.12, 0), (5.2, 0.24, 1.6), '#8a8e93')                                # base/rampa
caixa((-2.6, 1.0, 0), (0.6, 2.0, 0.9), '#9a9ea3'); caixa((2.6, 1.0, 0), (0.6, 2.0, 0.9), '#9a9ea3')   # muros de arrimo
fim(0.02)
