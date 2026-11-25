# 25/11 PayPal: computador de mesa de 2002 (monitor CRT bege, teclado, mouse, gabinete). blender -b --python blender/objetos_computador.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
BEGE = '#d9d2bf'; BEGE2 = '#c4bca6'; TELA = '#3d6fb8'; PRETO = '#2a2a2e'
novo('computador_2002')
caixa((0, .26, -.05), (.46, .38, .40), BEGE)          # corpo do monitor CRT (fundo)
caixa((0, .28, .16), (.42, .34, .06), BEGE2)          # moldura frontal
caixa((0, .29, .195), (.34, .26, .01), TELA)          # tela azul acesa
caixa((0, .045, 0), (.22, .05, .22), BEGE2)           # pe do monitor
caixa((0, .015, .36), (.48, .03, .17), BEGE)          # teclado
for i in range(4): caixa((0, .033, .31 + i * .035), (.42, .008, .02), BEGE2)   # fileiras de teclas
caixa((.33, .015, .38), (.07, .025, .11), BEGE)       # mouse
caixa((-.42, .2, 0), (.18, .4, .42), BEGE)            # gabinete torre ao lado
caixa((-.42, .3, .212), (.13, .03, .005), PRETO)      # leitor de cd
bola((-.42, .12, .213), .015, '#3ad17a')              # luz de ligado
fim(0.005)
