# Objetos que nasceram de caixas nas sessoes e foram REFEITOS redondos (mesmo nome de arquivo). blender -b --python blender/objetos_refeitos.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('apple'); bola((0, .45, 0), .45, '#d8282f', .95); bola((.12, .52, .2), .2, '#e85a4a', .9); tubo([(0, .82, 0), (.05, 1.0, 0)], .035, '#6a4426'); bola((.2, .95, 0), .13, '#4fa84a', .35, rot=(0, .5, 0), esc=(1.6, 1, .8)); fim(0)
novo('bathtub')                                                # banheira oval de pes redondos, com agua
bola((0, .4, 0), .5, '#f4f1e8', esc=(1.9, .8, 1.0)); bola((0, .74, 0), .46, '#6fc4ee', esc=(1.8, .16, .9)); arco((0, .74, .0), .0, '#f4f1e8', .01)
for i in range(26): a = i * math.pi / 13; bola((.9 * math.cos(a), .76, .47 * math.sin(a)), .07, '#e6e2d6', seg=8)   # borda da banheira
for x, z in ((-.3, .1), (.2, -.12), (.45, .15)): bola((x, .84, z), .09, '#ffffff', seg=8)   # espuma
for x in (-.6, .6):
    for z in (-.3, .3): bola((x, .1, z), .11, '#d9a630')
tubo([(.8, .6, 0), (.8, .95, 0), (.62, 1.0, 0)], .04, '#b8bcc4'); fim(0)
novo('crown')                                                  # coroa: aro redondo, pontas em cone, pedras
torno((0, 0, 0), [(.42, 0), (.46, .04), (.46, .2), (.42, .24), (.36, .24), (.36, 0)], '#f2c230', 24)
for i in range(6): a = i * math.pi / 3; cil((.41 * math.cos(a), .36, .41 * math.sin(a)), .09, .26, '#f2c230', .0, lados=10); bola((.41 * math.cos(a), .5, .41 * math.sin(a)), .05, '#d8282f' if i % 2 else '#2f6fd0')
for i in range(6): a = i * math.pi / 3 + .52; bola((.46 * math.cos(a), .12, .46 * math.sin(a)), .045, '#fff6f0')
fim(0.01)
novo('feather'); tubo([(-1.2, .08, 0), (1.25, .08, 0)], .03, '#d9d2c0'); bola((.2, .08, 0), .5, '#fbf6e6', .12, esc=(2.1, 1, .5)); bola((.95, .08, 0), .2, '#f4efe2', .12, esc=(1.6, 1, .6)); fim(0)   # pena: haste + barbas lisas
novo('petri'); cil((0, .04, 0), .62, .08, '#c9dfe8'); cil((0, .09, 0), .56, .05, '#f0c9b8'); torno((0, 0, 0), [(.6, .0), (.64, .02), (.64, .2), (.6, .2)], '#dbeef5', 24, tampa=False)                                    # placa de Petri com colonias
for x, z, r, c in ((.0, .05, .2, '#5aa05a'), (.25, -.2, .1, '#f4efe2'), (-.3, -.15, .08, '#f4efe2'), (-.2, .3, .09, '#f4efe2'), (.32, .25, .07, '#f4efe2')): bola((x, .13, z), r, c, .35)
bola((.0, .15, .05), .12, '#7cc07c', .4); fim(0)
novo('pisa_tower')                                             # torre de Pisa: 7 andares redondos com arcadas, inclinada
T = .075
for i in range(7):
    y = .5 + i * .95; x = y * T * 1.0
    cil((x, y, 0), 1.0 if i == 0 else .92, .95, '#f1ece0', rot=(0, -T, 0), lados=20); cil((x + .47 * T, y + .47, 0), 1.08, .1, '#d9d2c0', rot=(0, -T, 0), lados=20)
    if 0 < i < 7:
        for k in range(10): a = k * math.pi / 5; bola((x + 1.0 * math.cos(a), y, 1.0 * math.sin(a)), .14, '#8a7f70', 2.2, seg=8)
y = 7.1; cil((y * T, y, 0), .7, .7, '#f1ece0', rot=(0, -T, 0), lados=16); cil((y * T + .03, y + .42, 0), .76, .08, '#d9d2c0', rot=(0, -T, 0), lados=16)
fim(0.02)
