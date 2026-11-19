# CIDADES POR REGIAO (ordem do Gibson 19/11: cada historia na cidade/epoca certa). blender -b --python blender/objetos_regioes.py
# Gera kit/rg_<regiao>_<n>.glb. A ferramenta troca os predios de fundo dos cenarios por estes conforme "regiao" do roteiro (ou o pais do "mapa").
# Escala igual aos predios da biblioteca (casa ~8 m de largura, 7-12 m de altura; frente para +z).
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
H = m.pi / 2

def janelas(x0, x1, y0, y1, nx, ny, z, col, w=.9, h=1.3, mold=None):
    for i in range(nx):
        for j in range(ny):
            x = x0 + (x1 - x0) * (i + .5) / nx; y = y0 + (y1 - y0) * (j + .5) / ny
            if mold: caixa((x, y, z - .02), (w + .3, h + .3, .1), mold)
            caixa((x, y, z), (w, h, .12), col)

def telhado2(cx, y0, w, d, h, col, beiral=.4):          # telhado de duas aguas com cumeeira ao longo da largura (x)
    a = m.atan2(h, d / 2); L = m.hypot(h, d / 2) + beiral
    for s in (-1, 1): caixa((cx, y0 + h / 2, s * d / 4), (w + beiral * 2, .3, L), col, rot=(s * a, 0, 0))

def frontao(cx, y0, w, h, d, col):                       # triangulo de frente (cumeeira para o fundo)
    prisma((cx, y0, 0), [(-w / 2, 0), (w / 2, 0), (0, h)], d, col)

# ---------------- EUROPA (Polonia, Alemanha, Hungria, Inglaterra antiga...) ----------------
novo('rg_europa_1')   # casa enxaimel
caixa((0, 3.5, 0), (8, 7, 6), '#f3e8cf')
for x in (-3.9, -1.3, 1.3, 3.9): caixa((x, 3.5, 3.03), (.3, 7, .1), '#5a3a24')
for y in (.2, 3.5, 6.85): caixa((0, y, 3.03), (8, .3, .1), '#5a3a24')
for s in (-1, 1): caixa((s * 2.6, 1.9, 3.04), (.25, 3.6, .08), '#5a3a24', rot=(0, s * .6, 0))
janelas(-3.2, 3.2, 3.8, 6.6, 3, 1, 3.08, '#3b5f8a', mold='#f3e8cf')
caixa((0, 1.2, 3.08), (1.3, 2.4, .12), '#6a4428')
telhado2(0, 7, 8, 6, 4.2, '#b5462f')
fim(.02)
novo('rg_europa_2')   # sobrado estreito colorido com frontao para a rua
caixa((0, 5, 0), (6, 10, 6.5), '#d9a441')
janelas(-2.2, 2.2, 1.2, 9.4, 3, 3, 3.3, '#2f4a6a', mold='#f6efe0')
frontao(0, 10, 6.3, 3.6, 6.6, '#b04a35')
caixa((0, 1.1, 3.3), (1.2, 2.2, .12), '#4a2f22')
fim(.02)
novo('rg_europa_3')   # igreja com torre e agulha
caixa((0, 5, -2), (7, 10, 12), '#e8e0cc'); telhado2(0, 10, 7, 12, 4, '#7a3a2a')
caixa((0, 9, 4.6), (3.6, 18, 3.6), '#ddd3bc'); cil((0, 21.5, 4.6), 2.4, 7, '#3e5a4a', raio_topo=0.05, lados=8)
caixa((0, 14, 6.45), (1.4, 1.4, .1), '#f1e3a0'); cil((0, 14, 6.5), .55, .1, '#2b2b30', rot=(H, 0, 0))
caixa((0, 1.6, 6.45), (1.6, 3.2, .1), '#5a3a24')
fim(.02)
# ---------------- FRANCA (Paris) ----------------
novo('rg_franca_1')   # predio haussmanniano
caixa((0, 7.5, 0), (12, 15, 7), '#efe4cc'); caixa((0, 16.6, 0), (12.2, 3.2, 7.2), '#5d6f85', afina=.82)
for y in (5.2, 9.6): caixa((0, y, 3.7), (12, .25, .6), '#2b2b30')
janelas(-5, 5, 1, 14.5, 5, 4, 3.53, '#40566e', w=1, h=1.8, mold='#f7efdc')
for x in (-3.5, 0, 3.5): caixa((x, 17.2, 3.1), (1.2, 1.4, .8), '#efe4cc')
for x in (-5.5, 5.5): caixa((x, 19.3, 0), (.9, 1.6, .9), '#b5462f')
fim(.02)
novo('rg_franca_2')   # cafe com toldo listrado
caixa((0, 2.6, 0), (8, 5.2, 6), '#efe4cc'); caixa((0, 1.4, 3.02), (6.6, 2.4, .1), '#3b4f66')
for i in range(8): caixa((-3.5 + i, 3.1, 3.7), (1, .2, 1.6), '#c8302a' if i % 2 else '#f4f0e8', rot=(.35, 0, 0))
for x in (-2.5, 0, 2.5): cil((x, .5, 5), .45, .08, '#f4f0e8'); cil((x, .25, 5), .06, .5, '#2b2b30')
caixa((0, 4.6, 3.06), (5, .8, .1), '#2b3a55')
fim(.02)
novo('rg_franca_3')   # predio de esquina com torreao
caixa((0, 6, 0), (9, 12, 7), '#e8dcc0'); cil((4.2, 7, 3), 1.8, 14, '#e8dcc0', lados=16); cil((4.2, 15.2, 3), 2.1, 2.4, '#5d6f85', raio_topo=.2, lados=16)
caixa((0, 13, 0), (9.2, 2.4, 7.2), '#5d6f85', afina=.8)
janelas(-4, 2, 1, 11.5, 3, 4, 3.53, '#40566e', w=1, h=1.8, mold='#f7efdc')
fim(.02)
# ---------------- HOLANDA ----------------
for k, (c, w, h) in enumerate((('#8a3b2a', 5, 11), ('#2f4a3a', 4.6, 12.5), ('#6a4a3a', 5.4, 10))):
    novo(f'rg_holanda_{k + 1}')
    caixa((0, h / 2, 0), (w, h, 7), c)
    st = [(-w / 2, 0), (w / 2, 0), (w / 2, 1), (w / 3, 1), (w / 3, 2), (w / 6, 2), (w / 6, 3), (-w / 6, 3), (-w / 6, 2), (-w / 3, 2), (-w / 3, 1), (-w / 2, 1)]
    prisma((0, h, 0), st, 7, c); caixa((0, h + 1.6, -1.5), (w - .2, .3, 4), '#3a3a44', rot=(.5, 0, 0))
    janelas(-w / 2 + .8, w / 2 - .8, 1, h - .5, 2, 4, 3.53, '#2b3a55', w=1, h=1.6, mold='#f4f0e8')
    caixa((0, h + 2.4, 3.53), (.4, .4, .2), '#f4f0e8')
    fim(.02)
# ---------------- EUA (seculo XX) ----------------
novo('rg_eua_1')      # predio de tijolo com escada de incendio e caixa d'agua
caixa((0, 7, 0), (10, 14, 8), '#a14b34'); caixa((0, 14.3, 0), (10.4, .6, 8.4), '#7a3a2a')
janelas(-4, 4, 1.5, 13.5, 4, 4, 4.03, '#3a4a5a', w=1.2, h=1.7, mold='#d9c7a8')
for y in (4.5, 8, 11.5): caixa((-2.5, y, 4.7), (3.4, .12, 1.2), '#2b2b30'); caixa((-2.5, y + .5, 5.3), (3.4, .1, .06), '#2b2b30')
caixa((-2.5, 8, 5.3), (.1, 8, .06), '#2b2b30', rot=(0, .3, 0))
for x in (2, 4): cil((x, 15.6, -2), .12, 2.4, '#5a3a24')
cil((3, 18, -2), 1.6, 2.6, '#7a5a3a'); cil((3, 19.8, -2), 1.8, 1.1, '#5a4a3a', raio_topo=.1)
fim(.02)
novo('rg_eua_2')      # casa de suburbio com varanda
caixa((0, 2.8, 0), (9, 5.6, 7), '#f1ede4'); telhado2(0, 5.6, 9, 7, 2.8, '#4a4f5a')
for i in range(10): caixa((0, .3 + i * .55, 3.52), (9, .06, .06), '#d4cfc4')
caixa((0, 2.8, 4.6), (9, .25, 2.2), '#4a4f5a'); [cil((x, 1.4, 5.5), .12, 2.8, '#f1ede4') for x in (-4, -1.5, 1.5, 4)]
caixa((0, .25, 4.6), (9, .5, 2.2), '#c9c2b4'); janelas(-3.4, 3.4, 1.4, 3.6, 2, 1, 3.56, '#3b5f8a', mold='#2f4a6a')
caixa((0, 1.3, 3.56), (1.2, 2.4, .1), '#b5462f')
fim(.02)
novo('rg_eua_3')      # lanchonete com letreiro
caixa((0, 2.4, 0), (10, 4.8, 7), '#e6e1d6'); caixa((0, 1.7, 3.52), (8.6, 2, .1), '#6ea0c8')
caixa((0, .3, 3.6), (10, .6, .2), '#d8282f'); caixa((0, 4.4, 3.6), (10, .5, .2), '#d8282f')
caixa((0, 6.4, 1), (6, 2, .4), '#d8282f'); luz(); caixa((0, 6.4, 1.25), (5.4, 1.4, .1), '#ffd84a'); luz(False)
for x in (-4.5, 4.5): cil((x, 5.4, 1), .15, 2, '#2b2b30')
fim(.02)
# ---------------- ORIENTE MEDIO / EGITO / NORTE DA AFRICA ----------------
novo('rg_oriente_1')  # casa de adobe de telhado plano
caixa((0, 3, 0), (8, 6, 7), '#d9b98a'); caixa((0, 6.25, 0), (8.2, .5, 7.2), '#c9a878')
for x in (-3.8, 3.8): caixa((x, 6.9, 0), (.4, .8, 7.2), '#c9a878')
janelas(-2.8, 2.8, 3.4, 5, 3, 1, 3.53, '#4a3a2a', w=.8, h=1)
caixa((0, 1.4, 3.53), (1.4, 2.8, .1), '#3a6a8a'); bola((0, 2.8, 3.55), .7, '#3a6a8a', esc=(1, .6, .1))
fim(.02)
novo('rg_oriente_2')  # mesquita com cupula e minarete
caixa((0, 3.5, 0), (10, 7, 9), '#efe2c8'); bola((0, 7, 0), 3.6, '#5aa0b8', esc=(1, 1.1, 1)); cil((0, 11.2, 0), .12, 1.6, '#e8c45a')
cil((5.6, 9, 3.4), .9, 18, '#efe2c8', lados=12); cil((5.6, 18.4, 3.4), 1.3, .5, '#d9c7a8', lados=12); cil((5.6, 19.8, 3.4), .8, 2.4, '#5aa0b8', raio_topo=.05, lados=12)
for x in (-3, 0, 3): caixa((x, 2.4, 4.53), (1.6, 3.6, .1), '#3a5a6a'); bola((x, 4.2, 4.55), .8, '#3a5a6a', esc=(1, 1.2, .1))
fim(.02)
novo('rg_oriente_3')  # casa de adobe em degraus
caixa((0, 2.5, 0), (9, 5, 7), '#d4b07c'); caixa((-1.5, 6.5, -1), (5, 3, 5), '#ddbd8c')
janelas(-3.5, 3.5, 2.6, 4.2, 4, 1, 3.53, '#4a3a2a', w=.7, h=.9); caixa((-1.5, 6.6, 1.53), (.8, 1, .1), '#4a3a2a')
for i in range(5): cil((4.4, 5.3, -3 + i * 1.5), .08, .6, '#8a6a4a', rot=(0, H, 0))
fim(.02)
# ---------------- COLONIAL (Brasil, Portugal, Mexico, America Latina 1600-1900) ----------------
novo('rg_colonial_1') # casario colonial branco com portas e janelas coloridas
caixa((0, 3, 0), (9, 6, 7), '#f6f1e6'); telhado2(0, 6, 9, 7, 2.4, '#b5532f')
for x in (-3, 0, 3): caixa((x, 1.5, 3.53), (1.3, 3, .1), '#2f6a9a'); caixa((x, 1.5, 3.5), (1.7, 3.4, .06), '#e8c45a')
janelas(-3, 3, 4, 5.4, 3, 1, 3.53, '#2f6a9a', w=1.1, h=1.2, mold='#e8c45a'); caixa((0, .15, 3.5), (9, .3, .1), '#e8c45a')
fim(.02)
novo('rg_colonial_2') # igreja barroca de duas torres
caixa((0, 5, -1), (8, 10, 12), '#f6f1e6'); prisma((0, 10, 5), [(-4, 0), (4, 0), (2.5, 1.6), (1, 2.8), (-1, 2.8), (-2.5, 1.6)], .6, '#f6f1e6')
for x in (-5, 5): caixa((x, 7, 4.2), (3, 14, 3), '#f6f1e6'); bola((x, 14.6, 4.2), 1.3, '#4a7aa0', esc=(1, 1.3, 1)); cil((x, 16.6, 4.2), .08, 1.2, '#e8c45a')
caixa((0, 2, 5.03), (2.4, 4, .1), '#6a4428'); bola((0, 4, 5.05), 1.2, '#6a4428', esc=(1, .8, .1)); cil((0, 7.5, 5.1), .8, .1, '#4a7aa0', rot=(H, 0, 0))
for x in (-5, 5): caixa((x, 10.5, 5.75), (1, 1.6, .1), '#2b2b30')
fim(.02)
novo('rg_colonial_3') # sobrado amarelo com sacadas
caixa((0, 4, 0), (9, 8, 7), '#e8c45a'); telhado2(0, 8, 9, 7, 2.2, '#b5532f')
for x in (-3, 0, 3): caixa((x, 1.5, 3.53), (1.3, 3, .1), '#3a7a5a'); caixa((x, 5.6, 3.53), (1.2, 2.2, .1), '#3a7a5a'); caixa((x, 4.6, 4), (1.8, .12, .9), '#2b2b30'); caixa((x, 5.1, 4.45), (1.8, .9, .06), '#2b2b30')
caixa((0, 7.9, 3.6), (9.2, .3, .3), '#f6f1e6')
fim(.02)
# ---------------- JAPAO / CHINA ----------------
novo('rg_japao_1')    # pagode
for i in range(5):
    w = 7 - i * 1.1; y = i * 3.2
    caixa((0, y + 1.4, 0), (w * .7, 2.8, w * .7), '#b8322a'); caixa((0, y + 3, 0), (w + 1.8, .5, w + 1.8), '#3a3a44', afina=.7)
    for s1 in (-1, 1):
        for s2 in (-1, 1): bola((s1 * (w + 1.6) / 2, y + 3.2, s2 * (w + 1.6) / 2), .25, '#3a3a44')
cil((0, 17.6, 0), .12, 3, '#e8c45a')
fim(.02)
novo('rg_japao_2')    # casa de madeira com telhado escuro
caixa((0, 2, 0), (9, 4, 6.5), '#c9a77a'); caixa((0, 4.6, 0), (10.6, 1.6, 8.2), '#3a3a44', afina=.55)
for x in (-3, -1, 1, 3): caixa((x, 2, 3.28), (1.8, 3.2, .1), '#f4ead6'); caixa((x - .9, 2, 3.3), (.1, 3.4, .1), '#5a3a24')
caixa((0, .3, 3.6), (9, .6, 1), '#8a6a4a')
fim(.02)
novo('rg_japao_3')    # portal torii
for x in (-3, 3): cil((x, 3.2, 0), .35, 6.4, '#c8302a')
caixa((0, 6.6, 0), (9, .6, .9), '#2b2b30'); caixa((0, 5.6, 0), (7.6, .45, .6), '#c8302a'); caixa((0, 6.2, 0), (1, 1, .4), '#c8302a')
fim(.02)
# ---------------- RUSSIA / LESTE EUROPEU ----------------
novo('rg_russia_1')   # igreja de cupulas em cebola
caixa((0, 4.5, 0), (9, 9, 9), '#f4efe6'); caixa((0, 9.6, 0), (5, 2.4, 5), '#f4efe6')
for (x, z, r, c) in ((0, 0, 2.2, '#e8b83a'), (-3.4, 3.4, 1.2, '#3a6ab8'), (3.4, 3.4, 1.2, '#3a6ab8'), (-3.4, -3.4, 1.2, '#2f8a5a'), (3.4, -3.4, 1.2, '#2f8a5a')):
    yb = 10.8 if x == 0 else 9
    if x: cil((x, yb - 1, z), r * .6, 2, '#f4efe6')
    torno((x, yb, z), [(r * .7, 0), (r, r * .5), (r * .9, r * 1.1), (r * .4, r * 1.6), (.05, r * 2.1)], c)
    cil((x, yb + r * 2.4, z), .06, r * .8, '#e8c45a')
caixa((0, 2, 4.53), (2, 4, .1), '#6a4428')
fim(.02)
novo('rg_russia_2')   # izba de troncos
for i in range(9): cil((0, .35 + i * .7, 0), .38, 8.4, '#8a5a34', rot=(0, 0, H), lados=10)
caixa((0, 3.2, 0), (8, 6.4, 6.4), '#7a4e2e')
frontao(0, 6.4, 8.2, 3.2, 6.6, '#7a4e2e'); telhado2(0, 6.4, 8.4, 6.6, 3.2, '#5a6a4a')
janelas(-2.5, 2.5, 3, 4.6, 2, 1, 3.25, '#3b5f8a', w=1, h=1.2, mold='#f4f0e8')
fim(.02)
# ---------------- AFRICA (aldeias) ----------------
novo('rg_africa_1')   # cabana redonda de barro com teto de palha
cil((0, 1.5, 0), 3, 3, '#b07a4a', lados=20); cil((0, 4.2, 0), 3.8, 3, '#c9a25a', raio_topo=.1, lados=20)
caixa((0, 1, 2.95), (1.1, 2, .1), '#4a3020')
fim(.02)
novo('rg_africa_2')   # celeiro alto sobre pedras
cil((0, 1.4, 0), 1.6, 2.8, '#a86a3e', lados=16); cil((0, 3.5, 0), 2, 1.8, '#c9a25a', raio_topo=.05, lados=16)
for a in range(4): bola((1.4 * m.cos(a * H), .2, 1.4 * m.sin(a * H)), .4, '#8a8a80')
fim(.02)
# ---------------- CLASSICO (Roma / Grecia antigas) ----------------
novo('rg_classico_1') # templo de colunas
for i in range(3): caixa((0, .3 + i * .6, 0), (12 - i, .6, 9 - i), '#e8e2d4')
for x in (-4.5, -2.7, -.9, .9, 2.7, 4.5): cil((x, 5.1, 3.4), .45, 6.6, '#f1ece0', lados=14)
caixa((0, 4.8, -1), (9, 6, 6), '#e2dccd'); caixa((0, 8.7, 0), (11, .8, 8), '#e8e2d4')
frontao(0, 9.1, 11, 2.2, 8, '#ece6d8')
fim(.02)
novo('rg_classico_2') # casa romana branca com telha terracota
caixa((0, 2.5, 0), (9, 5, 7), '#f1ece0'); telhado2(0, 5, 9, 7, 1.8, '#c0603a')
caixa((0, 1.3, 3.52), (1.4, 2.6, .1), '#7a4a2a'); janelas(-3, 3, 3, 4, 2, 1, 3.52, '#5a3a24', w=.8, h=.6)
caixa((0, .1, 3.6), (9, .2, .4), '#d4ccbb')
fim(.02)
