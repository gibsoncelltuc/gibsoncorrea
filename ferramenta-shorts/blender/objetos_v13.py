# v13 (24/11): KIT MODERNO (historias de 1950 em diante) para a cena atual nao ganhar barril/caixote/lampiao, e pecas de EXPLICACAO (tanque de ar, bocal do propulsor).
# blender -b --python blender/objetos_v13.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
novo('cone_transito')
caixa((0, 0.03, 0), (0.42, 0.06, 0.42), '#1b1b1f'); cil((0, 0.4, 0), 0.16, 0.68, '#f26a1b', raio_topo=0.035); cil((0, 0.42, 0), 0.105, 0.12, '#f4f4f2', raio_topo=0.085)
fim(0.01)
novo('barreira_jersey')
caixa((0, 0.14, 0), (2.4, 0.28, 0.62), '#c9cdd3'); caixa((0, 0.6, 0), (2.4, 0.66, 0.34), '#d6d9dd', afina=0.6)
for x in (-0.7, 0.7): caixa((x, 0.62, 0.11), (0.5, 0.14, 0.02), '#d8282f')
fim(0.02)
novo('palete')
for z in (-0.4, 0, 0.4): caixa((0, 0.07, z), (1.2, 0.1, 0.1), '#b98b5a')
for x in (-0.5, -0.25, 0, 0.25, 0.5): caixa((x, 0.15, 0), (0.2, 0.04, 1.0), '#c99a66')
for (x, y) in ((-0.3, 0.42), (0.3, 0.42), (-0.3, 0.92), (0.3, 0.92)): caixa((x, y, 0), (0.56, 0.48, 0.9), '#d9c8a6')
fim(0.01)
novo('telao_led')
caixa((0, 0.2, 0), (7.4, 0.4, 1.2), '#2a2d33')
for x in (-3.2, 3.2): cil((x, 2.2, -0.3), 0.14, 4.0, '#4a4f58')
caixa((0, 4.4, 0), (7.0, 4.0, 0.3), '#16181d')
luz(True); caixa((0, 4.4, 0.16), (6.6, 3.6, 0.04), '#2f6fd0'); caixa((0, 4.4, 0.19), (3.4, 0.5, 0.02), '#e9f2ff'); luz(False)
fim(0.02)
novo('grade_evento')
for x in (-1.1, 1.1): cil((x, 0.55, 0), 0.03, 1.1, '#b9bec6'); caixa((x, 0.02, 0), (0.08, 0.04, 0.6), '#8a9099')
for y in (1.08, 0.2): tubo([(-1.1, y, 0), (1.1, y, 0)], 0.03, '#b9bec6')
for i in range(9): cil((-0.88 + i * 0.22, 0.64, 0), 0.015, 0.88, '#b9bec6')
fim(0.005)
novo('tripe_camera')
for a in (0, 2.094, 4.189): tubo([(0, 1.3, 0), (0.55 * math.cos(a), 0, 0.55 * math.sin(a))], 0.025, '#2a2d33')
caixa((0, 1.45, 0), (0.42, 0.26, 0.24), '#1b1b1f'); cil((0, 1.45, 0.22), 0.09, 0.2, '#3a3f48', rot=(math.pi / 2, 0, 0)); caixa((0, 1.63, -0.02), (0.1, 0.1, 0.14), '#3a3f48')
fim(0.008)
# ---- pecas de explicacao: tanque de gas comprimido e bocal de propulsor (jato frio) ----
novo('tanque_ar')
torno((0, 0, 0), [(0.02, 0), (0.2, 0.05), (0.3, 0.2), (0.3, 1.0), (0.2, 1.15), (0.07, 1.2), (0.07, 1.3)], '#2a2d33')
for y in (0.3, 0.9): cil((0, y, 0), 0.31, 0.06, '#c9cdd3')
cil((0, 1.34, 0), 0.1, 0.08, '#c9a227')
fim(0.01)
novo('bocal_propulsor')
torno((0, 0, 0), [(0.3, 0), (0.24, 0.18), (0.1, 0.42), (0.14, 0.5), (0.14, 0.7)], '#b9bec6'); cil((0, 0.72, 0), 0.18, 0.06, '#59606b')
fim(0.01)
# ---- canhao do seculo XX (antiaereo/de campanha): troca automatica do canhao antigo de rodas de madeira em historias de 1900 em diante ----
novo('canhao_moderno')
for a in (0.5, 2.6, 4.7): caixa((0.9 * math.cos(a), 0.08, 0.9 * math.sin(a)), (1.5, 0.12, 0.22), '#4b5a3c', rot=(0, 0, -a))
cil((0, 0.35, 0), 0.34, 0.5, '#55653f'); caixa((0, 0.85, 0), (0.7, 0.6, 0.9), '#4b5a3c')
cil((0, 1.25, 0.9), 0.075, 2.6, '#3c4631', rot=(math.pi / 2 - 0.7, 0, 0)); cil((0, 1.86, 1.62), 0.1, 0.3, '#2f3827', rot=(math.pi / 2 - 0.7, 0, 0))
caixa((0, 1.0, 0.42), (1.1, 0.8, 0.06), '#55653f', rot=(-0.25, 0, 0)); cil((0.5, 0.9, -0.2), 0.16, 0.06, '#2f3827', rot=(0, math.pi / 2, 0))
fim(0.012)
# ---- Cybercab (taxi-robo da Tesla, 2024+): cupe dourado de 2 lugares, rodas cobertas por calotas lisas; pesquisa do Roadster (fileira de veiculos parados) ----
novo('cybercab')
bola((0, 0.62, 0), 1.0, '#c9b07a', esc=(2.15, 0.5, 0.92), seg=20)                 # corpo baixo e liso, dourado fosco
bola((-0.15, 1.02, 0), 1.0, '#1c2530', esc=(1.25, 0.42, 0.8), seg=18)             # cabine/vidro escuro em gota
caixa((0, 0.3, 0), (3.9, 0.22, 1.7), '#8a7a52')                                   # saia
for x in (-1.3, 1.3):
    for sd in (-1, 1):
        cil((x, 0.36, sd * 0.86), 0.36, 0.22, '#1b1b1f', rot=(math.pi / 2, 0, 0)); cil((x, 0.36, sd * 0.98), 0.3, 0.04, '#d9c48f', rot=(math.pi / 2, 0, 0))   # pneu + calota lisa dourada
luz(True); caixa((2.1, 0.66, 0), (0.06, 0.05, 1.3), '#ffffff'); caixa((-2.12, 0.7, 0), (0.06, 0.05, 1.4), '#ff3b30'); luz(False)   # barra de luz dianteira e traseira
fim(0.02)
