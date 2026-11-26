# 23/11: cenario REAL da apresentacao do Tesla Roadster (SpaceX, McGregor/Texas, 15/out/2026, a noite): rampa curva gigante (o carro sobe ate ficar de cabeca
# para baixo, se solta e voa), torres de refletor, e galpao iluminado (interior 'galpao', serve para qualquer historia de fabrica/hangar/oficina).
# blender -b --python blender/objetos_mcgregor.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
# ---- RAMPA CURVA (meio loop): base em (0,0); o carro entra pela esquerda, sobe pela direita e chega no topo (0, 2R) de cabeca para baixo ----
R = 5.5; LARG = 3.4; N = 28
novo('rampa_curva')
for i in range(N):
    t0, t1 = math.pi * i / N, math.pi * (i + 1) / N; tm = (t0 + t1) / 2
    seg = 2 * R * math.sin((t1 - t0) / 2) + 0.06
    cx, cy = (R + 0.14) * math.sin(tm), R - (R + 0.14) * math.cos(tm)
    caixa((cx, cy, 0), (seg, 0.26, LARG), '#e9edf2', rot=(0, 0, -tm))
    for sd in (-1, 1):   # faixas de LED azul nas bordas
        luz(True); caixa(((R + 0.02) * math.sin(tm), R - (R + 0.02) * math.cos(tm), sd * (LARG / 2 - 0.1)), (seg, 0.08, 0.14), '#3a8cff', rot=(0, 0, -tm)); luz(False)
for x in (-9, -6, -3):   # pista de entrada no chao
    caixa((x + 1.5, 0.12, 0), (3.06, 0.24, LARG), '#e9edf2')
    for sd in (-1, 1): luz(True); caixa((x + 1.5, 0.27, sd * (LARG / 2 - 0.1)), (3.0, 0.07, 0.14), '#3a8cff'); luz(False)
for (px, ph) in ((R + 0.9, R * 1.6), (R * 0.75, 2 * R + 0.2)):   # pilares de aco (so' do lado de fora: o carro sai voando do topo para a esquerda)
    for sd in (-1, 1): cil((px, ph / 2, sd * (LARG / 2 + 0.4)), 0.22, ph, '#59606b')
fim(0.02)
# ---- TORRE DE REFLETOR ----
novo('torre_luz')
cil((0, 4.5, 0), 0.16, 9.0, '#4a4f58'); caixa((0, 0.15, 0), (1.2, 0.3, 1.2), '#4a4f58'); caixa((0, 9.2, 0), (2.8, 1.4, 0.3), '#2a2d33')
luz(True)
for ix in (-0.9, 0, 0.9):
    for iy in (8.85, 9.55): bola((ix, iy, 0.2), 0.3, '#fff6d8', achata=0.5, rot=(math.pi / 2, 0, 0))
luz(False)
fim(0.02)
# ---- GALPAO ILUMINADO (interior): mesmas medidas das salas (parede do fundo em z = -4.2, chao de x -15 a 15) ----
novo('room_galpao')
caixa((0, -0.05, 1.8), (30, 0.1, 12), '#8e9398')                             # piso de concreto
for x in range(-14, 15, 4): caixa((x, 0.01, 1.8), (0.08, 0.02, 12), '#7f8489')   # juntas do piso
for z in (-1.2, 4.6): caixa((0, 0.02, z), (30, 0.02, 0.22), '#f2c230')        # faixas amarelas de seguranca
caixa((0, 7, -4.3), (30, 14, 0.2), '#c9ced4')                                 # parede do fundo (chapa metalica)
for x in [i * 1.0 - 15 for i in range(31)]: caixa((x, 7, -4.15), (0.12, 14, 0.12), '#b1b7be')   # nervuras da chapa
caixa((0, 4.2, -4.05), (9.5, 8.4, 0.12), '#9aa3ad')                           # portao grande
for y in range(1, 8): caixa((0, y * 1.05, -3.97), (9.5, 0.06, 0.04), '#7e8791')
for x in (-15.2, 15.2): caixa((x, 7, 1.8), (0.2, 14, 12), '#bfc5cc')          # paredes laterais
for x in (-11, -6, 6, 11): caixa((x, 7, -4.0), (0.5, 14, 0.5), '#5d636b')      # colunas de aco
caixa((0, 12.6, -3.9), (30, 0.4, 0.6), '#5d636b')                             # viga
luz(True)
for x in (-11, -6, 0, 6, 11): caixa((x, 11.4, -3.6), (3.2, 0.35, 0.9), '#fffbe8')   # luminarias fortes (galpao iluminado)
for x in (-8.5, 8.5): caixa((x, 6.5, -4.02), (2.6, 0.5, 0.06), '#ffffff')      # letreiros/painel de luz na parede
luz(False)
for (x, z, c) in ((-12.5, -3.2, '#2f6db5'), (12.5, -3.0, '#d8282f')):           # tanques/containers ao fundo
    caixa((x, 1.3, z), (2.4, 2.6, 1.6), c)
cil((-9.2, 2.6, -3.4), 0.9, 5.2, '#eef1f4'); bola((-9.2, 5.3, -3.4), 0.9, '#eef1f4', achata=0.9)   # tanque branco (peca de foguete)
fim(0.0)
