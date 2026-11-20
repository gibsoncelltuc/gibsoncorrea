# CC 11 Rontgen: tubo de Crookes e chapa de raio X da mao. blender -b --python blender/objetos_cc11.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('crookes_tube')                                           # tubo de vidro em pera, eletrodos e suporte de madeira
caixa((0, .05, 0), (.7, .1, .4), '#8a5a34'); cil((-.25, .3, 0), .03, .5, '#3a3d47'); cil((.25, .3, 0), .03, .5, '#3a3d47')
torno((0, .45, 0), [(.03, 0), (.14, .08), (.24, .3), (.2, .52), (.08, .66), (.03, .74)], '#bfe3ef', 20)
cil((0, .43, 0), .05, .06, '#8d949c'); cil((0, 1.22, 0), .035, .12, '#8d949c'); bola((0, .8, 0), .09, '#e9f9ff')
tubo([(0, 1.28, 0), (.25, 1.35, 0), (.25, .55, 0)], .015, '#c0262d'); tubo([(0, .4, 0), (-.25, .52, 0)], .015, '#22252c')
fim(0.01)
novo('xray_plate')                                             # chapa de raio X num cavalete: placa escura com os ossos da mao em branco e a alianca dourada
caixa((0, 1.1, 0), (1.0, 1.3, .05), '#1d2a3a'); caixa((0, 1.1, -.01), (1.08, 1.38, .03), '#6a4426')
for x in (-.35, .35): cil((x, .45, -.15), .035, 1.0, '#7a4a26', rot=(.25, 0, 0))
B_ = '#e6eef5'
tubo([(-.06, .45, .04), (-.06, .85, .04)], .03, B_); tubo([(.06, .45, .04), (.06, .85, .04)], .028, B_)          # radio e ulna
bola((0, .9, .04), .13, B_, .4, esc=(1.35, 1, .3))                                                                  # carpo
for i, (bx, tx, fx) in enumerate(((-.09, -.13, -.2), (-.03, -.045, -.07), (.03, .045, .06), (.09, .13, .18))):
    tubo([(bx, .95, .04), (tx, 1.22, .04)], .022, B_)                                                               # metacarpo
    ln = (.36, .42, .39, .3)[i]; tubo([(tx, 1.25, .04), (tx + (fx - tx) * .5, 1.25 + ln * .55, .04), (fx, 1.25 + ln, .04)], .018, B_)   # dedo inteiro
    for t in (0, .55, 1): bola((tx + (fx - tx) * t * (.5 if t < 1 else 1) if t < 1 else fx, 1.25 + ln * t, .04), .026, B_, seg=10)    # juntas
tubo([(-.1, .92, .04), (-.27, 1.05, .04), (-.38, 1.2, .04), (-.44, 1.32, .04)], .02, B_)                          # polegar
torno((.03, 1.37, .04), [(.03, -.025), (.042, 0), (.042, .03), (.03, .035)], '#f2c230', 14)                       # alianca no dedo anelar
fim(0.008)
