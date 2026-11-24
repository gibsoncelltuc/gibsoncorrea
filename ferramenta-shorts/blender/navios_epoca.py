# v13 (24/11, Gibson: "tem que ver os barcos da epoca... modelar e pintar com as cores certas, nada de navio velho sem graca"):
# EMBARCACOES POR EPOCA, pintadas como nas referencias (quadros e fotos de museu naval). Todas com ~4,5 m de modelo, proa para +x; a ferramenta poe no tamanho real.
#   navio_galera     ate 1400     galera a remo: casco baixo, esporao, vela listrada, fileira de remos
#   navio_caravela   1400-1620    caravela/nau: casco bojudo de madeira clara, castelos de proa e popa, velas com cruz vermelha
#   navio_fragata    1620-1865    fragata/nau de linha: casco PRETO com faixa creme e portinholas (xadrez de Nelson), cobre na linha d'agua, 3 mastros de velas cheias
#   navio_encouracado 1905-1960   encouracado cinza: torres de canhao, chamines, mastro de combate, linha d'agua vermelha
# blender -b --python blender/navios_epoca.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *

def casco(L, alt, larg, cor, cor_fundo, y0=0.0, bojo=1.0):
    """casco arredondado: meio elipsoide alongado (fundo) + costado; proa afilada para +x"""
    bola((0, y0 + alt * 0.55, 0), 1.0, cor_fundo, esc=(L / 2, alt * 0.62, larg / 2 * bojo), seg=20)
    for i in range(9):   # costado em fatias que afinam para a proa e a popa (silhueta de navio, nao de caixote)
        t = (i - 4) / 4.0; w = larg * (1 - 0.55 * abs(t) ** 2.2); x = t * L * 0.44
        caixa((x, y0 + alt * 0.86, 0), (L * 0.12, alt * 0.5, w), cor)
def vela(x, y, larg, alt, cor='#efe6cc', bojo=0.16, z=0.0):
    caixa((x, y, z + 0.03), (larg, alt, 0.05), cor, afina=0.9); bola((x, y - alt * 0.04, z + 0.05), 1.0, cor, esc=(larg * 0.46, alt * 0.44, bojo * 0.8), seg=12)   # pano retangular + barriga do vento: vela enfunada, de frente para quem ve o navio de lado (como nos quadros de marinha)
def mastro(x, base, h, cor='#5a3d24', r=0.055):
    cil((x, base + h / 2, 0), r, h, cor, raio_topo=r * 0.6)
def verga(x, y, larg, cor='#3d2a18'):
    cil((x, y, 0.02), 0.03, larg, cor, rot=(0, math.pi / 2, 0))

# ---------------- FRAGATA / NAU DE LINHA (1620-1865) ----------------
novo('navio_fragata')
casco(4.6, 1.15, 1.25, '#17171b', '#8a4a32')                      # casco preto; fundo forrado de cobre
for i in range(9):                                                # faixa creme com portinholas pretas (xadrez de Nelson)
    t = (i - 4) / 4.0; w = 1.25 * (1 - 0.55 * abs(t) ** 2.2); x = t * 4.6 * 0.44
    caixa((x, 1.02, 0), (4.6 * 0.121, 0.2, w + 0.03), '#e6d9a8')
for i in range(10):
    x = -1.75 + i * 0.39; w = 1.25 * (1 - 0.55 * abs(x / 2.02) ** 2.2)
    for sd in (-1, 1): caixa((x, 1.02, sd * (w / 2 + 0.02)), (0.15, 0.13, 0.03), '#17171b')
caixa((0, 1.3, 0), (4.0, 0.07, 1.05), '#b9895a')                  # conves de madeira
caixa((-1.95, 1.5, 0), (0.75, 0.55, 1.0), '#17171b'); caixa((-2.3, 1.45, 0), (0.06, 0.4, 0.8), '#e8c45a')   # castelo de popa com galeria dourada
for z in (-0.25, 0, 0.25): caixa((-2.34, 1.5, z), (0.03, 0.2, 0.16), '#9fd0e6')                              # janelas da camara do capitao
tubo([(2.1, 1.25, 0), (3.25, 1.75, 0)], 0.045, '#5a3d24')         # gurupes
prisma((2.55, 0, 0), [(-0.45, 1.55), (0.65, 1.72), (-0.45, 3.3)], 0.03, '#efe6cc')   # bujarrona (vela triangular de proa)
for x, h in ((-1.25, 3.6), (0.15, 4.3), (1.45, 3.7)):
    mastro(x, 1.3, h)
    for k in range(3):                                            # tres velas redondas por mastro, menores para cima
        y = 1.3 + h * (0.24 + 0.27 * k); wv = 1.22 - 0.22 * k; av = h * 0.24
        verga(x, y + av / 2, wv + 0.15); vela(x, y, wv, av)
    cil((x, 1.3 + h * 0.52, 0), 0.16, 0.05, '#3d2a18')            # cesto da gavea
prisma((-1.9, 0, 0), [(-0.55, 1.9), (0.45, 1.9), (0.45, 3.4)], 0.03, '#efe6cc')      # vela latina da mezena
pano((0.15, 5.95, 0), 0.6, 0.34, ['#c8102e', '#c8102e'], onda=0.06, nx=6)            # flamula vermelha no tope
fim(0.02)

# ---------------- CARAVELA / NAU (1400-1620) ----------------
novo('navio_caravela')
casco(4.0, 1.2, 1.45, '#8a5a2e', '#5e3b1e', bojo=1.1)
for y in (0.85, 1.12): 
    for i in range(9):
        t = (i - 4) / 4.0; w = 1.45 * (1 - 0.55 * abs(t) ** 2.2); caixa((t * 4.0 * 0.44, y, 0), (4.0 * 0.121, 0.05, w + 0.04), '#4a2e16')   # cintas escuras do costado
caixa((0, 1.32, 0), (3.3, 0.07, 1.15), '#c49a66')
caixa((-1.6, 1.75, 0), (1.0, 0.85, 1.15), '#8a5a2e'); caixa((-1.6, 2.2, 0), (1.06, 0.07, 1.2), '#4a2e16')     # castelo de popa alto
caixa((1.55, 1.55, 0), (0.7, 0.45, 0.95), '#8a5a2e'); caixa((1.55, 1.8, 0), (0.76, 0.06, 1.0), '#4a2e16')     # castelo de proa
for z in (-0.3, 0.3): caixa((-2.12, 1.8, z), (0.03, 0.22, 0.2), '#e8c45a')
tubo([(1.9, 1.5, 0), (2.8, 1.95, 0)], 0.045, '#5e3b1e')
for x, h, wv in ((1.0, 3.1, 1.15), (-0.35, 3.7, 1.4)):
    mastro(x, 1.3, h); y = 1.3 + h * 0.56; av = h * 0.52
    verga(x, y + av / 2, wv + 0.15); vela(x, y, wv, av, bojo=0.22)
    caixa((x, y, 0.3), (0.12, av * 0.5, 0.02), '#c8102e'); caixa((x, y + av * 0.06, 0.3), (wv * 0.42, 0.12, 0.02), '#c8102e')   # cruz vermelha na vela
    cil((x, 1.3 + h * 0.9, 0), 0.15, 0.12, '#5e3b1e')
mastro(-1.6, 2.2, 2.2); prisma((-1.6, 0, 0), [(-0.75, 2.5), (0.6, 2.6), (0.5, 4.2)], 0.03, '#efe6cc')          # vela latina na popa
pano((-0.35, 5.3, 0), 0.5, 0.3, ['#ffffff', '#c8102e'], onda=0.06, nx=6)
fim(0.02)

# ---------------- GALERA A REMO (antiguidade ate 1400) ----------------
novo('navio_galera')
casco(4.8, 0.7, 0.95, '#9a6a3a', '#6a4424')
for i in range(9):
    t = (i - 4) / 4.0; w = 0.95 * (1 - 0.55 * abs(t) ** 2.2); caixa((t * 4.8 * 0.44, 0.9, 0), (4.8 * 0.121, 0.08, w + 0.04), '#b3262d')        # faixa vermelha no bordo
tubo([(2.0, 0.45, 0), (2.9, 0.3, 0)], 0.07, '#c9a227')                                                                                      # esporao de bronze
bola((2.05, 0.75, 0.3), 0.09, '#ffffff'); bola((2.08, 0.75, 0.33), 0.04, '#17171b'); bola((2.05, 0.75, -0.3), 0.09, '#ffffff'); bola((2.08, 0.75, -0.33), 0.04, '#17171b')   # olho pintado na proa
tubo([(-2.1, 0.8, 0), (-2.5, 1.5, 0), (-2.25, 2.1, 0), (-1.9, 2.2, 0)], 0.06, '#9a6a3a')                                                     # popa em voluta
for i in range(11):
    x = -1.55 + i * 0.31
    for sd in (-1, 1): cil((x - 0.09, 0.46, sd * 0.85), 0.02, 1.05, '#d9c8a6', rot=(sd * 0.87, 0, 0), lados=6)                               # remos
caixa((0, 0.95, 0), (3.6, 0.05, 0.6), '#c49a66')
mastro(0.2, 0.95, 2.9); verga(0.2, 3.52, 2.3)
for k, c_ in enumerate(('#efe6cc', '#b3262d', '#efe6cc', '#b3262d', '#efe6cc')): caixa((0.2 - 0.84 + k * 0.42, 2.55, 0.06), (0.425, 1.85, 0.06), c_)     # vela quadrada listrada
fim(0.02)

# ---------------- ENCOURACADO (1905-1960) ----------------
novo('navio_encouracado')
casco(4.8, 0.85, 0.95, '#7d8794', '#8a2f2a')                      # cinza naval; obras vivas vermelhas
caixa((0, 1.0, 0), (4.3, 0.08, 0.82), '#9aa3ad')
caixa((0.1, 1.3, 0), (1.9, 0.5, 0.62), '#8b95a1'); caixa((0.35, 1.75, 0), (0.9, 0.42, 0.5), '#9aa3ad'); caixa((0.45, 2.1, 0), (0.5, 0.3, 0.4), '#aab3bd')   # superestrutura e ponte
for z in (-0.16, 0, 0.16): caixa((0.71, 2.12, z), (0.02, 0.1, 0.1), '#1c2a3a')
for x in (-0.25, -0.75): cil((x, 1.95, 0), 0.17, 0.9, '#59616c', raio_topo=0.15); cil((x, 2.42, 0), 0.155, 0.08, '#1c1c20')    # chamines com topo preto
mastro(0.45, 2.2, 1.7, '#59616c', 0.04); cil((0.45, 3.3, 0), 0.16, 0.14, '#7d8794'); verga(0.45, 3.0, 0.9, '#59616c')
for x, sg in ((1.55, 1), (1.1, 1), (-1.5, -1)):                    # torres de canhao com dois tubos
    cil((x, 1.2 + (0.18 if x == 1.1 else 0), 0), 0.27, 0.3, '#6d7783')
    for z in (-0.09, 0.09): cil((x + sg * 0.55, 1.26 + (0.18 if x == 1.1 else 0), z), 0.035, 0.9, '#4b535d', rot=(0, math.pi / 2, 0))
tubo([(2.35, 1.05, 0), (2.35, 1.5, 0)], 0.02, '#59616c')
fim(0.02)

# ---------------- NAVIO A VAPOR DE GUERRA (1865-1905): casco preto, obras brancas, chamine amarela, mastros com velas de apoio ----------------
novo('navio_vapor_guerra')
casco(4.7, 0.95, 1.05, '#17171b', '#8a2f2a')
for i in range(9):
    t = (i - 4) / 4.0; w = 1.05 * (1 - 0.55 * abs(t) ** 2.2); caixa((t * 4.7 * 0.44, 1.05, 0), (4.7 * 0.121, 0.07, w + 0.03), '#f2efe6')       # friso branco
caixa((0, 1.12, 0), (4.1, 0.07, 0.9), '#b9895a')
caixa((0.2, 1.4, 0), (1.5, 0.5, 0.66), '#f2efe6'); caixa((0.55, 1.8, 0), (0.6, 0.32, 0.5), '#f2efe6')
for z in (-0.2, 0, 0.2): caixa((0.86, 1.82, z), (0.02, 0.12, 0.12), '#1c2a3a')
cil((-0.15, 2.05, 0), 0.2, 1.1, '#e0b84a', raio_topo=0.18); cil((-0.15, 2.62, 0), 0.19, 0.1, '#17171b')
for x, h in ((-1.5, 2.9), (1.55, 3.1)):
    mastro(x, 1.12, h); verga(x, 1.12 + h * 0.7, 1.1); vela(x, 1.12 + h * 0.5, 1.0, h * 0.36)
for x in (-0.9, 1.0):
    for sd in (-1, 1): cil((x, 1.22, sd * 0.36), 0.05, 0.5, '#4b535d', rot=(sd * math.pi / 2.6, 0, 0))   # canhoes de bordo
tubo([(2.15, 1.1, 0), (2.9, 1.4, 0)], 0.04, '#5a3d24')
pano((1.55, 4.5, 0), 0.5, 0.3, ['#c8102e', '#c8102e'], onda=0.06, nx=6)
fim(0.02)

# ---------------- DESTROIER / FRAGATA MODERNA (1960 em diante): cinza claro, casco anguloso, radar, canhao de proa, heliponto ----------------
novo('navio_destroier')
casco(4.9, 0.8, 0.85, '#9aa3ad', '#59616c')
caixa((0, 0.95, 0), (4.4, 0.07, 0.75), '#aab3bd')
caixa((0.35, 1.3, 0), (1.7, 0.6, 0.6), '#9aa3ad', afina=0.82); caixa((0.6, 1.8, 0), (0.8, 0.4, 0.48), '#aab3bd', afina=0.8)
for z in (-0.17, 0, 0.17): caixa((1.0, 1.82, z), (0.02, 0.1, 0.11), '#1c2a3a')
cil((0.55, 2.5, 0), 0.05, 1.0, '#7d8794'); caixa((0.55, 2.75, 0), (0.5, 0.26, 0.06), '#7d8794'); bola((0.2, 2.2, 0), 0.18, '#e9edf2')   # mastro, antena de radar e radome
caixa((-0.55, 1.35, 0), (0.6, 0.55, 0.5), '#8b95a1', afina=0.7)                                                                          # chamine baixa e inclinada
cil((1.75, 1.12, 0), 0.2, 0.22, '#8b95a1'); cil((2.1, 1.18, 0), 0.03, 0.7, '#4b535d', rot=(0, math.pi / 2, 0))                           # canhao de proa
caixa((-1.6, 1.0, 0), (1.3, 0.04, 0.7), '#59616c'); cil((-1.6, 1.03, 0), 0.28, 0.01, '#e9edf2')                                          # heliponto
fim(0.02)
