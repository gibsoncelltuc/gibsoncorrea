# MARCOS DOS LUGARES + HOSPITAL + CARRO NOVO (ordem do Gibson 19/11). blender -b --python blender/objetos_marcos.py
# Os marcos ficam ao fundo do cenario quando a historia acontece naquele lugar (piramides no Egito, plataforma no Cabo Canaveral...).
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
H = m.pi / 2
def piramide(x, z, b, h, col='#e2c58e', col2='#c9a86e'):
    cil((x, h / 2, z), b * .707, h, col, raio_topo=.02, lados=4, rot=(0, m.pi / 4, 0))
    for i in range(1, 6): cil((x, h * i / 6 - .05, z), b * .707 * (1 - i / 6) + .05, .12, col2, lados=4, rot=(0, m.pi / 4, 0))

novo('marco_piramides')   # as 3 piramides de Gize + esfinge
piramide(-14, -6, 22, 15); piramide(6, 0, 21, 14.4); piramide(22, 6, 10, 6.6)
caixa((-2, 1.2, 14), (2.6, 2.4, 7), '#d8b880'); bola((-2, 3.2, 17.3), 1.5, '#d8b880', esc=(1, 1.15, 1)); caixa((-2, 3.6, 17), (3.6, 1.2, .8), '#5a6aa0')
fim(.02)

novo('marco_canaveral')   # plataforma de lancamento: torre, foguete branco, vala das chamas, esfera de agua
caixa((0, .6, 0), (16, 1.2, 12), '#9a9ea6'); caixa((0, .05, 6.6), (6, .4, 3), '#4a4f58')
for x in (-6.4, -4.6):
    for z in (-1.4, 1.4): cil((x, 13, z), .25, 26, '#c8302a', lados=6)
for y in range(2, 26, 3):
    caixa((-5.5, y, 0), (2.4, .2, 3.2), '#c8302a'); caixa((-5.5, y + 1.5, 0), (.15, 3, 3.4), '#c8302a', rot=(.7, 0, 0))
caixa((-3.4, 21, 0), (3.6, .5, .6), '#c8302a')
cil((0, 15.5, 0), 1.6, 26, '#f4f4f2', lados=24); cil((0, 30, 0), 1.6, 3.2, '#f4f4f2', raio_topo=.15, lados=24)
caixa((0, 22, 1.62), (.15, 6, .1), '#2b2b30'); cil((0, 2.6, 0), 1.7, 1.2, '#2b2b30', lados=24)
for a in range(4): caixa((1.6 * m.cos(a * H + .78), 3.4, 1.6 * m.sin(a * H + .78)), (.2, 2.6, 1.2), '#2b2b30', rot=(0, 0, a * H + .78))
bola((10, 4, -3), 2.6, '#f4f4f2'); [cil((10 + 1.6 * m.cos(a), 1.2, -3 + 1.6 * m.sin(a)), .15, 2.4, '#9a9ea6') for a in (0, 2.1, 4.2)]
fim(.02)

novo('marco_bigben')      # torre do relogio de Londres
caixa((0, 14, 0), (5, 28, 5), '#d9c08a')
for y in range(3, 26, 4): caixa((0, y, 2.53), (3.6, .25, .1), '#b89a64')
caixa((0, 29.5, 0), (5.6, 3, 5.6), '#d9c08a')
for s in ((0, 2.83), (0, -2.83)): cil((0, 29.5, s[1]), 1.9, .15, '#f4f0e2', rot=(H, 0, 0)); cil((0, 29.5, s[1] * 1.01), .25, .2, '#2b2b30', rot=(H, 0, 0))
caixa((0, 31.6, 0), (5, 1.2, 5), '#5a6a5a'); cil((0, 35.6, 0), 3.2, 7, '#3e5a4a', raio_topo=.1, lados=4, rot=(0, m.pi / 4, 0)); cil((0, 39.6, 0), .12, 1.6, '#e8c45a')
fim(.02)

novo('marco_eiffel')      # torre Eiffel
for sx in (-1, 1):
    for sz in (-1, 1): cil((sx * 3.6, 6, sz * 3.6), .9, 13, '#8a6a4a', raio_topo=.55, lados=6, rot=(sz * .3, 0, -sx * .3))
caixa((0, 12.2, 0), (9, 1, 9), '#8a6a4a'); arco((0, 6.5, 4.4), 3.4, '#8a6a4a', esp=.35, de=0, ate=m.pi)
cil((0, 21, 0), 2.6, 17, '#8a6a4a', raio_topo=1.1, lados=4, rot=(0, m.pi / 4, 0)); caixa((0, 29.6, 0), (3.4, .8, 3.4), '#8a6a4a')
cil((0, 37, 0), 1.1, 14, '#8a6a4a', raio_topo=.2, lados=4, rot=(0, m.pi / 4, 0)); cil((0, 45, 0), .12, 2.4, '#8a6a4a')
fim(.02)

novo('marco_liberdade')   # Estatua da Liberdade
caixa((0, 4, 0), (8, 8, 8), '#bdb5a2'); caixa((0, 10, 0), (5, 4, 5), '#c9c1ae')
cil((0, 16, 0), 1.6, 8, '#6aa58e', raio_topo=1.1); bola((0, 21, 0), 1.2, '#6aa58e')
for a in range(7): cil((1.2 * m.cos(a * .45 - .3), 22.2, 1.2 * m.sin(a * .45 - .3) * .3), .12, 1.4, '#6aa58e', rot=(0, (a - 3) * .25, 0))
cil((1.6, 22, 0), .35, 4.6, '#6aa58e', rot=(0, -.25, 0)); cil((2.2, 24.6, 0), .45, .8, '#6aa58e', raio_topo=.7); luz(); bola((2.2, 25.4, 0), .5, '#ffcf3a', esc=(1, 1.4, 1)); luz(False)
caixa((-1.4, 17.4, .6), (.9, 1.6, .5), '#6aa58e')
fim(.02)

novo('marco_coliseu')     # Coliseu de Roma
for k, (r, h, c) in enumerate(((16, 4, '#d8c49a'), (16, 4, '#ccb88e'), (16, 4, '#d8c49a'), (16, 3, '#c4b084'))):
    torno((0, k * 4, 0), [(r, 0), (r, h), (r - 3, h), (r - 3, 0)], c, lados=40)
    for i in range(40):
        a = i / 40 * 2 * m.pi
        if k < 3: bola((r * m.cos(a) * 1.002, k * 4 + 2.1, r * m.sin(a) * 1.002), .95, '#6a5a44', esc=(.7, 1.5, .25), rot=(0, 0, -a + H))
fim(.02)

novo('marco_cristo')      # Cristo Redentor no morro
bola((0, 0, 0), 14, '#4f8a3a', esc=(1, .9, .8)); caixa((0, 13.4, 0), (2.2, 2, 2.2), '#d4d0c4')
cil((0, 18, 0), 1.1, 8, '#ece8dc', raio_topo=.7); bola((0, 22.6, 0), .8, '#ece8dc'); caixa((0, 20.8, 0), (10, .9, .7), '#ece8dc')
fim(.02)

novo('hospital_ext')      # fachada de hospital com cruz vermelha
caixa((0, 6, 0), (16, 12, 8), '#f4f6f8'); caixa((0, 12.3, 0), (16.4, .6, 8.4), '#c8ccd2')
for i in range(5):
    for j in range(3): caixa((-6 + i * 3, 3.5 + j * 3, 4.03), (1.6, 1.6, .1), '#7ab0d8')
caixa((0, 1.6, 4.03), (4, 3.2, .1), '#9ad0e6'); caixa((0, 3.6, 4.6), (6, .3, 1.6), '#c8ccd2')
caixa((0, 13.8, 0), (1, 3, .6), '#d8282f'); caixa((0, 13.8, 0), (3, 1, .6), '#d8282f')
caixa((5.6, 3.6, 4.2), (1, 3, .4), '#d8282f'); caixa((5.6, 3.6, 4.2), (3, 1, .4), '#d8282f')
fim(.02)

novo('maca')              # maca/leito de hospital
caixa((0, .9, 0), (2.2, .25, 1), '#c8ccd2'); caixa((0, 1.12, 0), (2.1, .2, .95), '#f4f6f8'); bola((-.8, 1.3, 0), .3, '#f4f6f8', esc=(1, .5, 1.4))
for x in (-1, 1):
    for z in (-.42, .42): cil((x, .45, z), .04, .9, '#8a8e96'); bola((x, .06, z), .07, '#2b2b30')
caixa((0, 1.15, .52), (2, .06, .04), '#8a8e96'); cil((1.4, 1.2, -.3), .03, 2.4, '#8a8e96'); bola((1.4, 2.3, -.3), .14, '#bfe6f7', esc=(1, 1.4, .6))
fim(.02)

novo('carro_redondo')     # carro conversivel arredondado (motorista aparece; substitui o carro quadrado)
bola((0, .75, 0), 1.1, '#d8282f', esc=(2.2, .55, 1.0)); caixa((0, .62, 0), (4.2, .5, 1.9), '#d8282f')
bola((1.25, 1.02, 0), .55, '#d8282f', esc=(1.2, .45, 1.6)); caixa((-.35, 1.1, 0), (1.9, .25, 1.5), '#5a2a22')
caixa((.55, 1.45, 0), (.08, .55, 1.55), '#bfe6f7', rot=(0, 0, .35)); cil((.2, 1.3, .3), .22, .06, '#2b2b30', rot=(0, 0, 1.2))
for x in (-1.35, 1.35):
    for z in (-.95, .95): cil((x, .42, z), .42, .3, '#2b2b30', rot=(H, 0, 0)); cil((x, .42, z * 1.03), .2, .32, '#d4d4d8', rot=(H, 0, 0))
for z in (-.6, .6): bola((2.15, .75, z), .16, '#fff6c8'); bola((-2.15, .75, z), .12, '#ff5a4a')
caixa((2.2, .45, 0), (.15, .15, 1.8), '#d4d4d8'); caixa((-2.2, .45, 0), (.15, .15, 1.8), '#d4d4d8')
fim(.03)
