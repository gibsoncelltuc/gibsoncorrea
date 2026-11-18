# Pia de banheiro de coluna (porcelana branca, torneira cromada) - PF 10 "a pia no Twitter". blender -b --python blender/objetos_pia.py
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('sink')
torno((0, 0, 0), [(.2, 0), (.22, .03), (.13, .1), (.1, .55), (.16, .62), (0, .64)], '#f4f2ee', 24)       # coluna
torno((0, .62, 0), [(.12, 0), (.3, .08), (.38, .16), (.4, .2), (.37, .21), (.3, .14), (0, .1)], '#f4f2ee', 32)   # bacia aberta
caixa((0, .81, -.3), (.6, .06, .14), '#f4f2ee', 1.0)                                                     # borda de tras
cil((0, .9, -.3), .03, .14, '#c8ccd2')                                                                   # torneira
tubo([(0, .97, -.3), (0, .99, -.2), (0, .94, -.14)], .022, '#c8ccd2', passo=.4)
for x in (-.13, .13): cil((x, .88, -.3), .03, .05, '#c8ccd2'); bola((x, .92, -.3), .03, '#d8282f' if x < 0 else '#1f4fa8', seg=10)
cil((0, .74, 0), .04, .01, '#9a9ea6')                                                                    # ralo
fim(0.006)
