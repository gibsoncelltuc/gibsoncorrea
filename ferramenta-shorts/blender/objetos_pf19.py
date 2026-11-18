# PF 19 Neuralink: o macaco Pager sentado, com o monitor do Pong, o joystick e o canudo da vitamina de banana. blender -b --python blender/objetos_pf19.py
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('monkey_pong')
B, F = '#7a5236', '#e8c49a'
torno((-.3, 0, 0), [(.28, 0), (.3, .04), (.12, .08), (.1, .42), (.3, .46), (.3, .5), (0, .5)], '#5a5e66', 16)   # banquinho
bola((-.3, .78, 0), .26, B, esc=(1, 1.15, .9))                          # corpo
bola((-.3, .74, .17), .16, F, esc=(1, 1.2, .5))                         # barriga
bola((-.3, 1.18, 0), .2, B)                                             # cabeca
bola((-.3, 1.15, .15), .14, F, esc=(1.2, 1, .6))                        # cara
for s in (-1, 1):
    bola((-.3 + s * .2, 1.2, 0), .07, F, esc=(.6, 1, 1))                 # orelhas
    bola((-.3 + s * .06, 1.22, .22), .035, '#ffffff', seg=10); bola((-.3 + s * .06, 1.22, .25), .02, '#1b1b1f', seg=8)   # olhos
bola((-.3, 1.11, .25), .05, '#c8a07a', esc=(1.3, .7, .6))               # focinho
caixa((-.3, 1.37, 0), (.16, .03, .12), '#c8ccd2', 1.0)                  # o implante (discreto, em cima da cabeca)
tubo([(-.5, .9, .05), (-.62, .7, .15), (-.55, .55, .3)], .05, B, passo=.35)         # braco esquerdo
tubo([(-.1, .9, .05), (.05, .8, .2), (.12, .78, .3)], .05, B, passo=.35)           # braco direito estendido
for s in (-1, 1): tubo([(-.3 + s * .12, .58, .1), (-.3 + s * .16, .52, .3), (-.3 + s * .18, .2, .35)], .055, B, passo=.35)   # pernas
tubo([(-.3, .6, -.2), (-.45, .4, -.4), (-.6, .55, -.55), (-.65, .8, -.5)], .03, B, passo=.4)   # rabo
caixa((.55, .25, 0), (.5, .5, .4), '#3a3e46', 1.0)                      # mesinha
caixa((.55, .62, 0), (.08, .25, .08), '#2a2a30', 1.0)                   # pe do monitor
caixa((.55, 1.0, 0), (.62, .46, .08), '#1b1b1f', 1.0)                   # monitor
caixa((.55, 1.0, .045), (.56, .4, .01), '#05070a', 1.0)                 # tela
for x in (.32, .78): caixa((.55 + (x - .55), 1.0 + (.06 if x < .5 else -.08), .055), (.025, .12, .01), '#f4f4f4', 1.0)   # raquetes do Pong
bola((.6, 1.05, .055), .022, '#f4f4f4', seg=8)                          # bolinha
for i in range(5): caixa((.55, .84 + i * .08, .052), (.008, .04, .01), '#8a8a8a', 1.0)  # rede pontilhada
tubo([(.3, .5, .2), (.15, .9, .25), (-.2, 1.1, .3)], .012, '#c8ccd2')   # canudo de metal da vitamina
caixa((.4, .52, .15), (.08, .06, .08), '#1b1b1f', 1.0); cil((.4, .6, .15), .015, .12, '#d8282f')   # joystick
fim(0.008)
