# MARCOS DOS LUGARES (3a leva, 19/11): cidades dos roteiros que ainda nao tinham marco. Referencias: fotos (Texas Capitol, Catedral Metropolitana do Mexico,
# Renaissance Center de Detroit, Residenz de Wurzburg, Marienkirche de Rostock, casas de canal + Westerkerk de Amsterda, pedras rai de Yap).
# blender -b --python blender/objetos_marcos3.py [nome ...]. Metros, frente para +z, ficam ao fundo (60-110 m).
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
H = m.pi / 2

def janelas(x0, x1, y, z, n, w=1.2, h=2.2, col='#3a4a5a'):
    for i in range(n): caixa((x0 + (x1 - x0) * i / max(1, n - 1), y, z), (w, h, .3), col)

def texas():   # Capitolio do Texas (Austin): granito rosado, cupula alta com tambor de colunas e estatua, alas laterais
    novo('marco_texas'); G, G2 = '#d9a796', '#c99484'
    caixa((0, 6, 0), (64, 12, 16), G); caixa((0, 12.5, 0), (65, 1, 16.6), G2)
    for f in (-1, 1): janelas(-30, 30, 4 + f * 0 + 3.5 * (f + 1) / 2 * 1.4, 8.2, 16)
    caixa((0, 9, 8.6), (14, 18, 2), G); cil((0, 18.5, 9.4), .1, .1, G) if False else caixa((0, 19.5, 9.2), (15, 2.5, 1.2), G2)
    for x in (-5, -2.5, 0, 2.5, 5): cil((x, 9, 9.8), .5, 14, '#ead0c4', lados=12)
    torno((0, 13, 0), [(9, 0), (9, 6), (8.4, 6), (8.4, 7)], G, lados=32)
    for i in range(24): a = i / 24 * 2 * m.pi; cil((9.3 * m.cos(a), 16.5, 9.3 * m.sin(a)), .35, 6, '#ead0c4', lados=8)
    torno((0, 20, 0), [(8.4, 0), (8, 3.5), (6.2, 8), (3.4, 10.6), (1.2, 11.6), (0, 11.8)], G, lados=36)
    cil((0, 33, 0), 1.3, 2.6, G, lados=16); bola((0, 34.6, 0), .9, G2); cil((0, 36.3, 0), .3, 2.5, '#8a8a7a'); bola((0, 37.8, 0), .45, '#8a8a7a')
    fim(.02)
def mexico():   # Catedral Metropolitana (Zocalo, Cidade do Mexico): duas torres com campanario em sino, fachada barroca, cupula central
    novo('marco_mexico'); P, P2 = '#c9b8a0', '#a8987e'
    caixa((0, 10, 0), (34, 20, 22), P); caixa((0, 21, 8), (12, 6, 3), P2)
    for s in (-1, 1):
        x = s * 13; caixa((x, 16, 9), (8, 32, 8), P); caixa((x, 33, 9), (7, 4, 7), P2)
        torno((x, 35, 9), [(3.2, 0), (3.2, 3), (2.4, 4.2), (1.2, 5.4), (0, 5.8)], P, lados=16); bola((x, 41.5, 9), .5, '#d9b84a'); cil((x, 42.6, 9), .12, 1.8, '#5a5a5a')
        for y in (20, 27): caixa((x, y, 13.1), (2, 3.6, .3), '#3a3430')
    for y in (6, 13): caixa((0, y, 11.1), (3.2, 5, .3), '#4a3a2a')
    for x in (-4, 4): cil((x, 9, 11.4), .45, 16, P2, lados=10)
    torno((0, 20, -3), [(5, 0), (5, 3), (4.4, 5), (2.4, 7.4), (0, 8)], '#b8c4c8', lados=24); cil((0, 28.8, -3), .5, 2, P)
    fim(.02)
def detroit():   # Renaissance Center (1977): torre cilindrica central de vidro escuro com 4 torres menores em volta
    novo('marco_detroit'); V, V2 = '#4a5a6a', '#6a7a8a'
    cil((0, 36, 0), 7, 72, V, lados=32); cil((0, 72.5, 0), 6.6, 1.5, V2, lados=32); cil((0, 74, 0), 3, 2.5, '#c8302a', lados=16)
    for i in range(16): cil((0, 4 + i * 4.3, 0), 7.08, .25, V2, lados=32)
    for a in (.785, 2.356, 3.927, 5.498):
        x, z = 14 * m.cos(a), 14 * m.sin(a); cil((x, 23, z), 5, 46, V, lados=8)
        for i in range(10): cil((x, 3 + i * 4.3, z), 5.06, .25, V2, lados=8)
    caixa((0, 4, 0), (40, 8, 40), '#5a6068')
    fim(.02)
def wurzburg():   # Residenz de Wurzburg: palacio barroco longo, amarelo-areia, pavilhao central com frontao, telhado mansarda cinza
    novo('marco_wurzburg'); A, A2, T = '#e2c890', '#cfb478', '#6a6e78'
    caixa((0, 8, 0), (90, 16, 14), A); caixa((0, 17.5, 0), (90, 3, 13), T, afina=.8)
    for s in (-1, 1): caixa((s * 40, 9, 10), (14, 18, 8), A); caixa((s * 40, 19.5, 10), (14, 3, 7.5), T, afina=.8)
    caixa((0, 10, 8), (24, 20, 4), A2); prisma((0, 20, 10.1), [(-12, 0), (12, 0), (0, 5)], 1.0, A2); caixa((0, 22.5, 4), (22, 4, 9), T, afina=.75)
    for y in (4.5, 11): janelas(-42, 42, y, 7.2, 26, 1.4, 3.0, '#3a3a40')
    for x in (-8, -4, 0, 4, 8): cil((x, 9, 10.3), .5, 16, '#f2e6c8', lados=10)
    fim(.02)
def rostock():   # Marienkirche de Rostock: igreja gotica de tijolo vermelho, torre-fachada larga com telhado de bico, janelas altas em arco
    novo('marco_rostock'); B, B2, T = '#a8483a', '#8a3a2e', '#3f5f50'
    caixa((0, 12, -8), (18, 24, 34), B); prisma((0, 24, -8), [(-9.5, 0), (9.5, 0), (0, 10)], 34, T) if False else caixa((0, 29, -8), (18, 10, 34), T, afina=.15)
    caixa((0, 13, -6), (34, 20, 10), B); caixa((0, 26, -6), (34, 8, 10), T, afina=.2)
    caixa((0, 26, 12), (20, 52, 10), B)
    for x in (-6, 0, 6):
        for y in (14, 30): caixa((x, y, 17.1), (2.2, 9, .3), '#3a3036'); bola((x, y + 4.5, 17.1), 1.1, '#3a3036', esc=(1, 1, .14))
    torno((0, 52, 12), [(7, 0), (6, 2), (2.5, 9), (.8, 15), (0, 18)], T, lados=4); cil((0, 71, 12), .15, 3, '#d9b84a')
    for i in range(8): caixa((-9 + i * 2.6, 52.6, 17), (1.4, 1.4, .4), B2)
    fim(.02)
def amsterdam():   # casas de canal de Amsterda (estreitas, altas, frontao em degrau/sino, cores tijolo) + torre da Westerkerk (1631) + canal
    novo('marco_amsterdam'); cores = ('#7a3a2a', '#3a3030', '#9a5a3a', '#2a3a4a', '#6a4a3a', '#8a2a2a', '#4a3a2a', '#a86a4a')
    caixa((0, -.4, 6), (64, .8, 6), '#3a5a6a')
    x = -30
    for i, c in enumerate(cores * 1):
        w = 5.5 + (i % 3) * .8; h = 14 + (i % 4) * 2.2
        caixa((x + w / 2, h / 2, 0), (w, h, 8), c)
        if i % 2: prisma((x + w / 2, h, 4.1), [(-w / 2, 0), (-w / 2, 1.5), (-w / 4, 1.5), (-w / 4, 3), (w / 4, 3), (w / 4, 1.5), (w / 2, 1.5), (w / 2, 0)], .8, c)   # frontao em degraus
        else: prisma((x + w / 2, h, 4.1), [(-w / 2, 0), (-w / 4, 2), (-w / 5, 3.6), (w / 5, 3.6), (w / 4, 2), (w / 2, 0)], .8, c); bola((x + w / 2, h + 3.8, 4.1), .5, '#f2efe6')
        for fy in range(int(h // 3.4)):
            for k in (-1, 1): caixa((x + w / 2 + k * w * .22, 2.2 + fy * 3.4, 4.1), (1.2, 2.0, .3), '#f2efe6'); caixa((x + w / 2 + k * w * .22, 2.2 + fy * 3.4, 4.25), (.9, 1.6, .2), '#2a3440')
        x += w + .2
    cx = 26; caixa((cx, 14, -6), (8, 28, 8), '#7a3a2a'); caixa((cx, 30, -6), (6, 6, 6), '#c8c0b0'); caixa((cx, 35, -6), (4.4, 5, 4.4), '#3a6a8a')
    cil((cx, 39.5, -6), 2.4, 4, '#c8c0b0', lados=8); torno((cx, 41.5, -6), [(2, 0), (1.2, 2), (.4, 4), (0, 6)], '#3a6a8a', lados=8); bola((cx, 48, -6), .9, '#d9b84a')
    fim(.02)
def yap():   # pedras rai de Yap: discos de pedra calcaria com furo no meio, encostados de pe numa fileira, palmeiras e casa de teto alto
    novo('marco_yap'); P = '#cfc6b0'
    for i, (x, r, z) in enumerate(((-10, 3.2, 0), (-3, 2.2, 1), (3, 2.8, -.5), (9, 1.8, .5), (14, 2.4, -1))):
        torno((x, r, z), [(r, -.35), (r, .35), (r * .22, .35), (r * .22, -.35)], P, lados=28, tampa=False) if False else None
        cil((x, r, z), r, .7, P, rot=(H, 0, 0), lados=28); cil((x, r, z + .02), r * .2, .75, '#5a5244', rot=(H, 0, 0), lados=16)
    caixa((0, .15, 0), (34, .3, 4), '#9a9488')
    for x in (-18, 20):
        tubo([(x, 0, -6), (x + .8, 6, -6), (x + 1.5, 11, -6)], .35, '#8a7050')
        for k in range(6): a = k / 6 * 2 * m.pi; bola((x + 1.5 + 2.2 * m.cos(a), 11, -6 + 2.2 * m.sin(a)), 1.6, '#4a8a3a', esc=(1.6, .25, .6), rot=(0, -a, 0))
    caixa((0, 3, -12), (10, 6, 7), '#8a6a4a'); prisma((0, 6, -8.4), [(-6, 0), (6, 0), (0, 7)], 7.4, '#b8a070')
    fim(.02)

E = dict(texas=texas, mexico=mexico, detroit=detroit, wurzburg=wurzburg, rostock=rostock, amsterdam=amsterdam, yap=yap)
alvo = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else list(E)
for k in alvo: E[k]()
