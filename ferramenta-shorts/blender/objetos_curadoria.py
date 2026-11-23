# 23/11: objetos da PESQUISA VISUAL dos roteiros (curadoria). blender -b --python blender/objetos_curadoria.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
# canivete de bolso aberto (Guerra de Toledo 1835: o unico ferido levou uma canivetada) - escala de desenho (legivel na tela)
novo('canivete')
caixa((0, 0.12, 0), (0.62, 0.16, 0.12), '#7a4a26', afina=0.92)            # cabo de madeira
for x in (-0.28, 0.28): cil((x, 0.12, 0.065), 0.03, 0.02, '#c9a24a', rot=(math.pi / 2, 0, 0))   # rebites de latao
prisma((0.58, 0.16, 0), [(-0.27, -0.05), (0.2, -0.05), (0.3, 0.0), (0.2, 0.06), (-0.27, 0.06)], 0.035, '#d4d9de')   # lamina de aco
fim(0.01)
# teodolito/bussola de agrimensor em tripe (topografos de Ohio em Phillips Corners, 1835)
novo('teodolito')
for a in (0, 2.1, 4.2): tubo([(0, 1.15, 0), (0.42 * math.cos(a), 0.0, 0.42 * math.sin(a))], 0.035, '#8a6a3a')
cil((0, 1.2, 0), 0.16, 0.08, '#b8862e'); cil((0, 1.33, 0), 0.07, 0.18, '#b8862e')
cil((0, 1.45, 0), 0.06, 0.62, '#c9962e', rot=(0, 0, math.pi / 2)); bola((0.31, 1.45, 0), 0.07, '#2a2a30')
fim(0.01)
# mapa antigo aberto num cavalete (o erro no mapa que comecou a briga)
novo('mapa_antigo')
for x in (-0.55, 0.55): tubo([(x, 0.0, 0.25), (x * 0.8, 1.9, 0)], 0.04, '#6a4a2a')
tubo([(0, 0.0, -0.4), (0, 1.8, 0)], 0.04, '#6a4a2a')
caixa((0, 1.35, 0.05), (1.3, 0.95, 0.04), '#e8d6a8', rot=(-0.15, 0, 0))     # pergaminho
caixa((0.1, 1.38, 0.08), (0.9, 0.06, 0.01), '#3a5a8a', rot=(-0.15, 0, 0.3))  # lago/rio desenhado
caixa((-0.1, 1.3, 0.08), (0.05, 0.7, 0.01), '#8a2a2a', rot=(-0.15, 0, 0))    # linha da fronteira
fim(0.01)
# cesto de batatas da horta (Guerra do Porco, 1859: o porco comia as batatas do fazendeiro)
novo('batatas')
torno((0, 0, 0), [(0.36, 0.0), (0.42, 0.06), (0.5, 0.42), (0.52, 0.46)], '#9a6a3a', tampa=False); cil((0, 0.02, 0), 0.36, 0.04, '#8a5a2a')
for i, (x, z) in enumerate(((0, 0), (0.22, 0.1), (-0.2, 0.12), (0.1, -0.2), (-0.12, -0.18), (0.25, -0.12), (-0.26, -0.05))):
    bola((x, 0.42 + 0.06 * (i % 2), z), 0.13, '#c79a5a', esc=(1.25, 0.9, 1.0))
fim(0.01)
