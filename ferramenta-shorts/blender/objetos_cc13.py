# CC 13 Semmelweis: bacia de porcelana com agua clorada e jarra, num suporte de madeira. blender -b --python blender/objetos_cc13.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('wash_basin')
torno((0, 0, 0), [(.30, 0), (.32, .04), (.16, .08), (.12, .55), (.20, .6), (.22, .66), (0, .66)], '#6a4426', 20)  # pedestal de madeira
torno((0, .66, 0), [(.16, 0), (.30, .06), (.46, .2), (.5, .24), (.47, .25), (.42, .2), (.25, .1), (.0, .08)], '#f2efe6', 28)          # bacia de porcelana
torno((0, .83, 0), [(.37, 0), (0, 0.005)], '#7fc4bc', 24)                                                         # agua clorada
torno((0, .895, 0), [(.47, 0), (.515, .005), (.515, .03), (.47, .035)], '#3a6fb0', 28, tampa=False)                                          # friso azul da borda
torno((.32, .9, -.05), [(.09, 0), (.13, .08), (.13, .22), (.07, .32), (.08, .38), (0, .38)], '#f2efe6', 20)     # jarra
tubo([(.43, 1.08, -.05), (.5, 1.2, -.05), (.47, 1.24, -.05)], .03, '#f2efe6', passo=.4)                                   # bico da jarra
tubo([(.28, 1.24, -.05), (.18, 1.22, -.05), (.15, 1.14, -.05), (.18, 1.06, -.05), (.25, 1.0, -.05)], .03, '#f2efe6', passo=.4)                            # alca da jarra
fim(0.01)
