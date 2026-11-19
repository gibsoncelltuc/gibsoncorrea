# MARCOS DOS LUGARES (2a leva, 19/11): o lugar exato da historia ao fundo. blender -b --python blender/objetos_marcos2.py [nome ...]
# Medidas em metros, de frente para +z. Ficam longe (~60-90 m) atras da cena; o mkvideo escolhe pelo titulo/mapa/comeco da narracao.
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
import formas
def escala(F):   # objetos do kit sao no tamanho do boneco (~1 a 1,5 m): amplia antes de exportar
    for v in formas._S['bm'].verts: v.co *= F
H = m.pi / 2
BR, CR, VD = '#f2efe6', '#e2dccb', '#6aa58e'

def colunas(x0, x1, z, y0, h, n, r=.45, col=BR):
    for i in range(n): cil((x0 + (x1 - x0) * i / max(1, n - 1), y0 + h / 2, z), r, h, col, lados=12)

def casa_branca():
    novo('marco_casabranca')
    caixa((0, 5, 0), (34, 10, 12), BR); caixa((0, 10.4, 0), (35, .8, 12.6), CR)
    for i in range(-7, 8):
        if abs(i) > 2: caixa((i * 2.2, 5.5, 6.05), (1.1, 2.2, .1), '#4a5a6a'); caixa((i * 2.2, 2, 6.05), (1.1, 2, .1), '#4a5a6a')
    torno((0, 0, 7.5), [(6.5, 0), (6.5, .6), (6.2, .6)], CR, lados=32)               # portico curvo (lado sul)
    for i in range(6): a = m.pi * (.15 + .7 * i / 5); cil((6 * m.cos(a), 5.2, 7.5 + 6 * m.sin(a) * .55), .45, 9.4, BR, lados=12)
    torno((0, 9.8, 7.5), [(6.6, 0), (6.6, .7), (0, .9)], CR, lados=32)
    for x in (-15, 15): caixa((x, 11.4, 0), (1, 1.4, 1), BR)
    cil((0, 13, 0), .12, 5, '#8a8a8a'); pano((0.1, 15.4, 0), 2.8, 1.6, ['#c8102e', '#f4f4f2', '#c8102e', '#f4f4f2', '#3c3b6e'])
    for x in range(-18, 19, 6): bola((x, 1.2, 12), 1.4, '#3f7a3a')
    fim(.02)

def capitolio():
    novo('marco_capitolio')
    caixa((0, 5, 0), (60, 10, 14), BR); caixa((0, 10.5, 0), (61, 1, 14.6), CR)
    colunas(-8, 8, 7.6, 0, 10, 8); cil((0, 11.5, 7.8), 9, 2.5, CR, raio_topo=.1, lados=3, rot=(H, 0, 0)) if False else caixa((0, 11.6, 7.5), (18, 1.6, 1.2), CR)
    torno((0, 11, 0), [(9, 0), (9, 5), (8.4, 5), (8.4, 6)], BR, lados=32)
    for i in range(24): a = i / 24 * 2 * m.pi; cil((9.2 * m.cos(a), 13.5, 9.2 * m.sin(a)), .35, 5, BR, lados=8)
    torno((0, 17, 0), [(8.4, 0), (8, 3), (6.5, 6.5), (4, 8.6), (1.5, 9.6), (0, 9.8)], BR, lados=36)
    cil((0, 27.8, 0), 1.2, 2.4, BR, lados=16); bola((0, 29.3, 0), 1.0, '#b8a888'); cil((0, 30.8, 0), .4, 2, '#7a6a5a')
    fim(.02)

LETRA = {   # letras em blocos (x0, y0, x1, y1) numa grade 4 x 6
 'H': [(0, 0, 1, 6), (3, 0, 4, 6), (1, 2.5, 3, 3.5)], 'O': [(0, 0, 1, 6), (3, 0, 4, 6), (1, 0, 3, 1), (1, 5, 3, 6)], 'L': [(0, 0, 1, 6), (1, 0, 4, 1)],
 'Y': [(1.5, 0, 2.5, 3.2), (0, 3, 1, 6), (3, 3, 4, 6), (0.6, 2.6, 3.4, 3.6)], 'W': [(0, 0, 1, 6), (3, 0, 4, 6), (1.5, 0, 2.5, 4), (0, 0, 4, 1)], 'D': [(0, 0, 1, 6), (1, 0, 3, 1), (1, 5, 3, 6), (3, .8, 4, 5.2)]}
def hollywood():
    novo('marco_hollywood')
    bola((0, -14, -10), 50, '#a89a6a', esc=(1.4, .55, .45)); bola((-40, -12, -20), 34, '#9a8c5e', esc=(1.3, .6, .5))
    for i, ch in enumerate('HOLLYWOOD'):
        x0 = (i - 4.5) * 6.2
        for (a0, b0, a1, b1) in LETRA[ch]: caixa((x0 + (a0 + a1) / 2 * 1.1, 12 + (b0 + b1) / 2 * 1.1, 10), ((a1 - a0) * 1.1, (b1 - b0) * 1.1, .4), '#f7f7f4')
        for k in (.6, 3.8): cil((x0 + k, 10.5, 9.4), .1, 4, '#7a7a7a', lados=6)
    fim(.02)

def golden_gate():
    novo('marco_goldengate')
    COR = '#c0362c'
    caixa((0, 9, 0), (140, 1.6, 4), COR)
    for x in (-38, 38):
        for z in (-1.8, 1.8): caixa((x, 22, z), (2.2, 44, 1.4), COR)
        for y in (14, 28, 40): caixa((x, y, 0), (2.4, 2, 5), COR)
    for z in (-1.8, 1.8):
        pts = [(-70, 30, z)] + [(x, 9.8 + 34 * ((abs(x) - 38) / 38) ** 2 if abs(x) <= 38 else 44 - (abs(x) - 38) * .45, z) for x in range(-38, 39, 4)] + [(70, 30, z)]
        pts = [(-70, 30, z), (-38, 44, z)] + [(x, 10 + 34 * (x / 38) ** 2, z) for x in range(-36, 37, 4)] + [(38, 44, z), (70, 30, z)]
        tubo(pts, .45, COR, passo=2.0)
        for x in range(-34, 35, 4): cil((x, 10 + 17 * (x / 38) ** 2, z), .08, 34 * (x / 38) ** 2 + .2, COR, lados=6)
    fim(.02)

def brandemburgo():
    novo('marco_brandemburgo')
    caixa((0, .6, 0), (30, 1.2, 10), CR)
    for x in (-12, -7.2, -2.4, 2.4, 7.2, 12):
        for z in (-3, 3): cil((x, 8.2, z), .85, 14, BR, lados=16)
    caixa((0, 16.2, 0), (30, 2, 10), BR); caixa((0, 18.6, 0), (18, 2.6, 8), CR)
    caixa((0, 20.4, 0), (5, 1, 3), '#5a7a6a')                                                  # quadriga (cavalos)
    for i in range(4): bola((-1.8 + i * 1.2, 21.6, .4), .5, '#5a7a6a', esc=(.6, 1, 1.6))
    bola((0, 22.8, -.6), .55, '#5a7a6a'); cil((0, 22, -.6), .4, 2, '#5a7a6a')
    fim(.02)

def pisa():
    novo('marco_pisa')
    for i in range(8):
        y = 2 + i * 6; r = 7.6 if i < 7 else 5.6
        cil((i * .55, y, 0), r, 6, BR if i % 2 else CR, lados=28, rot=(0, 0, -.07))
        for k in range(16): a = k / 16 * 2 * m.pi; cil((i * .55 + (r + .3) * m.cos(a), y, (r + .3) * m.sin(a)), .28, 5, '#efeadc', lados=8, rot=(0, 0, -.07))
    fim(.02)

def catedral_viena():
    novo('marco_viena')
    caixa((0, 12, 0), (24, 24, 50), '#cfc4a8');
    for i in range(10):                                                                              # telhado de azulejos em ziguezague
        cil((0, 30, -22 + i * 5), 12.6, 5.2, '#d9a441' if i % 2 else '#2f6a5a', raio_topo=.1, lados=3, rot=(H, 0, H))
    cil((0, 25, 27), 6, 50, '#bfb294', raio_topo=1.2, lados=8); cil((0, 54, 27), 1.4, 12, '#bfb294', raio_topo=.1, lados=8)
    for y in range(8, 46, 6): caixa((0, y, 31.2), (2, 3.4, .2), '#5a6aa0')
    fim(.02)

def atomium():
    novo('marco_atomium')
    P = [(0, 22, 0), (0, 40, 0), (0, 4, 0), (-12, 32, -6), (12, 32, 6), (-12, 12, 6), (12, 12, -6), (-12, 32, 6), (12, 12, 6)]
    for p_ in P: bola(p_, 3.6, '#c9ccd2')
    for p_ in P[1:]: tubo([P[0], p_], .9, '#b8bcc4', passo=1.5)
    cil((0, 1.5, 0), 1.6, 3, '#9a9ca4')
    fim(.02)

def alpes():
    novo('marco_alpes')
    for x, h, w in ((-40, 52, 34), (-6, 70, 40), (30, 58, 36), (62, 44, 30)):
        cil((x, h / 2, -30), w, h, '#8a96a8', raio_topo=1.5, lados=7); cil((x, h * .82, -30), w * .3, h * .36, '#f4f6fa', raio_topo=1.2, lados=7)
    for i, x in enumerate((-18, -6, 6, 18)):                                                       # chales suicos
        caixa((x, 2.2, 10), (7, 4.4, 6), '#e8dcc0'); caixa((x, 4.6, 13.05), (7, .2, .1), '#6a3a1f')
        cil((x, 6.2, 10), 5.8, 3.4, '#6a3a1f', raio_topo=.1, lados=4, rot=(H, 0, 0)) if False else caixa((x, 5.8, 10), (8.4, .6, 7.6), '#6a3a1f', afina=.25)
        for k in (-1.8, 1.8): caixa((x + k, 2.6, 13.06), (1.2, 1.2, .1), '#5a8aa8'); caixa((x + k, 1.8, 13.2), (1.4, .3, .4), '#d8282f')
    fim(.02)

def chichen_itza():
    novo('marco_chichenitza')
    for i in range(9): w = 28 - i * 2.6; caixa((0, i * 2.4 + 1.2, 0), (w, 2.4, w), '#cfc4a0' if i % 2 else '#bfb490')
    for a in (0, H, m.pi, -H): caixa((m.sin(a) * 8, 11, m.cos(a) * 8), (5 if a in (0, m.pi) else 22, 22, 22 if a in (0, m.pi) else 5), '#d8cca8', afina=.3) if False else None
    caixa((0, 11, 12.5), (5, .3, 7), '#9a8c6a', rot=(-.75, 0, 0))                                    # escadaria
    caixa((0, 24, 0), (8, 5, 8), '#d8cca8'); caixa((0, 23.2, 4.05), (2, 3, .1), '#3a3020')
    fim(.02)

def sao_basilio():
    novo('marco_saobasilio')
    caixa((0, 6, 0), (30, 12, 30), '#b8463a')
    for x, z, h, c1, c2 in ((0, 0, 30, '#c9a040', '#d8282f'), (-9, 9, 20, '#2f8a4a', '#f4f0e2'), (9, 9, 20, '#2a5aa8', '#e8c45a'), (-9, -9, 20, '#d8282f', '#2f8a4a'), (9, -9, 20, '#e8c45a', '#2a5aa8')):
        cil((x, 12 + h / 2 - 4, z), 3.4 if x else 4.4, h - 8, '#c45a4a', lados=12)
        bola((x, 12 + h - 2, z), 3.6 if x else 4.6, c1, esc=(1, 1.25, 1))
        for k in range(6): a = k / 6 * 2 * m.pi; bola((x + 3.3 * m.cos(a), 12 + h - 2, z + 3.3 * m.sin(a)), 1.2, c2, esc=(.5, 1.2, .5)) if x else None
        cil((x, 12 + h + 2.4, z), .5, 3, c1, raio_topo=.05, lados=8); cil((x, 12 + h + 4.2, z), .08, 1.6, '#e8c45a')
    fim(.02)

def opera_sydney():
    novo('marco_operasydney')
    caixa((0, 2, 0), (80, 4, 36), '#c9a080')
    for i, (x, s_) in enumerate(((-24, 1.0), (-12, 1.1), (0, 1.2), (14, .8), (24, .7))):
        bola((x, 4, 0), 14 * s_, '#f4f4f0', esc=(.42, 1.35, .55), rot=(0, 0, .55))
        bola((x + 4, 4, 10), 9 * s_, '#efeee8', esc=(.42, 1.3, .55), rot=(0, 0, .55))
    bola((0, -2, 20), 60, '#3a7ab0', esc=(1.5, .05, .5))
    fim(.02)

def mesquita():
    novo('marco_mesquita')
    caixa((0, 6, 0), (34, 12, 34), '#e8dcc0'); torno((0, 12, 0), [(12, 0), (12, 3), (11, 7), (8, 10.5), (4, 12.6), (0, 13.2)], '#3a7ab8', lados=32)
    cil((0, 26, 0), .6, 2.4, '#e8c45a', raio_topo=.05)
    for x in (-12, 12):
        for z in (-12, 12): bola((x, 12, z), 3.4, '#3a7ab8')
    for x in (-20, 20):
        cil((x, 16, 16), 1.3, 32, '#efe6cc', lados=12); caixa((x, 26, 16), (3.4, .5, 3.4), '#d8c8a0'); cil((x, 34, 16), 1.3, 4, '#3a7ab8', raio_topo=.05, lados=12)
    caixa((0, 6, 17.05), (9, 10, .2), '#3a7ab8')
    fim(.02)

def olinda():
    novo('marco_olinda')   # igreja colonial barroca branca no alto do morro (Pernambuco/Brasil colonia)
    bola((0, -14, 0), 40, '#5a9a4a', esc=(1.6, .5, 1))
    caixa((0, 10, 0), (18, 14, 26), BR); caixa((0, 17.6, 12.6), (18, 2, 1), '#5a7ab0')
    for x in (-11, 11):
        caixa((x, 13, 12), (6, 20, 6), BR); caixa((x, 23.6, 12), (6.4, 1, 6.4), '#5a7ab0'); cil((x, 26, 12), 2.6, 4, '#c9a040', raio_topo=.3, lados=8); cil((x, 29, 12), .1, 2, '#2a2a2a')
        caixa((x, 19, 15.05), (1.8, 2.6, .1), '#2a3a5a')
    cil((0, 22, 12.6), 6, 6, BR, raio_topo=.1, lados=3, rot=(H, 0, 0)) if False else caixa((0, 21, 12.6), (14, 4, .8), BR, afina=.35)
    caixa((0, 6, 13.05), (3.2, 6, .1), '#6a3a1f'); bola((0, 19, 13.1), 1.2, '#f4f0e2')
    for x in (-24, -16, 16, 24): caixa((x, 3, 8), (7, 6, 7), ['#e8c45a', '#5a9ad8', '#e07a8a', '#7ac87a'][int(x / 8) % 4])
    fim(.02)

E = dict(casabranca=casa_branca, capitolio=capitolio, hollywood=hollywood, goldengate=golden_gate, brandemburgo=brandemburgo, pisa=pisa, viena=catedral_viena,
         atomium=atomium, alpes=alpes, chichenitza=chichen_itza, saobasilio=sao_basilio, operasydney=opera_sydney, mesquita=mesquita, olinda=olinda)

# OBJETOS QUE AINDA ERAM CAIXOTE (19/11): chocolate, ovo, pipoca -> formas arredondadas (mesmo nome de arquivo)
def chocolate():
    novo('chocolate')
    caixa((0, .05, 0), (.5, .1, .26), '#5a3420')
    for i in range(4):
        for j in range(2): bola((-.18 + i * .12, .1, -.06 + j * .12), .05, '#6a3e26', esc=(1.05, .45, 1.05))
    caixa((.14, .06, 0), (.24, .125, .275), '#c8102e'); caixa((.14, .125, 0), (.24, .01, .2), '#e8c45a')
    escala(2.6)
    fim(.015)
def ovo():
    novo('egg')
    bola((0, .14, 0), .1, '#f6efe2', esc=(1, 1.38, 1), seg=24)
    escala(4.0)
    fim(.0)
def pipoca():
    novo('popcorn')
    torno((0, 0, 0), [(.09, 0), (.13, .26), (.135, .27)], '#f4f4f2', lados=24, tampa=False)
    for i in range(8): cil((.11 * m.cos(i * m.pi / 4), .135, .11 * m.sin(i * m.pi / 4)), .018, .27, '#d8282f', raio_topo=.024, lados=6, rot=(0, 0, 0))
    cil((0, .01, 0), .09, .02, '#f4f4f2')
    for i in range(18): a = i * 2.4; r = .1 * ((i % 5) / 5); bola((r * m.cos(a), .28 + .03 * (i % 3), r * m.sin(a)), .032, '#fff3c8' if i % 4 else '#f2d27a')
    escala(3.2)
    fim(.01)
E.update(chocolate=chocolate, egg=ovo, popcorn=pipoca)

# ===== 3a leva (19/11): lugar exato de cada roteiro =====
def farol_alexandria():
    novo('marco_alexandria')   # Farol de Alexandria (Egito antigo): base quadrada, meio octogonal, topo redondo com fogo
    caixa((0, 1, 0), (40, 2, 40), '#d8c8a0'); caixa((0, 16, 0), (18, 28, 18), '#e8dcc0', afina=.86); caixa((0, 30.6, 0), (16, 1.2, 16), '#d0c098')
    cil((0, 38, 0), 6.5, 14, '#e8dcc0', raio_topo=5.5, lados=8); cil((0, 45.6, 0), 6.2, 1.2, '#d0c098', lados=8)
    cil((0, 50, 0), 3.4, 8, '#e8dcc0', lados=16); torno((0, 54, 0), [(3.6, 0), (3.6, .6), (0, 2.6)], '#d0c098', lados=16)
    luz(); bola((0, 57.6, 0), 1.6, '#ffb03a', esc=(1, 1.4, 1)); luz(False); cil((0, 61, 0), .3, 3, '#c9a24a')
    bola((0, -1, 18), 34, '#3a7ab0', esc=(1.6, .05, .4)); fim(.02)
def notredame():
    novo('marco_notredame')    # Notre-Dame de Paris: fachada com 2 torres quadradas, rosacea, nave atras com agulha
    caixa((0, 14, 0), (34, 28, 10), '#d8cfb8')
    for x in (-11.5, 11.5): caixa((x, 34, 0), (11, 12, 10), '#d8cfb8'); caixa((x, 40.4, 0), (11.6, .8, 10.6), '#c8bea6')
    cil((0, 24, 5.1), 5, .4, '#5a6aa0', lados=24, rot=(m.pi / 2, 0, 0)); cil((0, 24, 5.2), 3.2, .4, '#c8302a', lados=16, rot=(m.pi / 2, 0, 0))
    for x in (-10, 0, 10): caixa((x, 5, 5.1), (6, 9, .3), '#4a3a2a', afina=.75)
    caixa((0, 13, 5.1), (30, 1.4, .4), '#c8bea6')
    caixa((0, 16, -26), (20, 22, 44), '#d0c6ae'); caixa((0, 30, -26), (21, 6, 44.6), '#5a6a72', afina=.08)
    cil((0, 44, -30), 1.2, 22, '#5a6a72', raio_topo=.05, lados=8); fim(.02)
def versalhes():
    novo('marco_versalhes')    # Palacio de Versalhes: fachada longa clara, telhado azul-ardosia, dourado no portao
    caixa((0, 9, 0), (90, 18, 14), '#e8dcc0'); caixa((0, 19.5, 0), (91, 3, 14.6), '#5a6a80', afina=.7)
    for x in (-38, 38): caixa((x, 9, 14), (14, 18, 16), '#e8dcc0'); caixa((x, 19.5, 14), (14.6, 3, 16.6), '#5a6a80', afina=.7)
    for i in range(-20, 21):
        caixa((i * 2.1, 8, 7.05), (1.1, 4, .1), '#5a6aa0')
    for i in range(-14, 15): cil((i * 2.4, 1.2, 30), .08, 2.4, '#c9a24a', lados=6)
    caixa((0, 2.6, 30), (70, .3, .2), '#c9a24a'); fim(.02)
def waterloo():
    novo('marco_waterloo')     # Monte do Leao de Waterloo: colina conica de grama com leao no topo
    cil((0, 20, 0), 40, 40, '#6aa04a', raio_topo=5, lados=28); cil((0, 41, 0), 3, 2, '#bdb5a2')
    bola((0, 43.4, 0), 1.6, '#4a4a52', esc=(1.8, 1, .9)); bola((1.9, 44.6, 0), 1.0, '#4a4a52'); bola((2.4, 44.8, 0), .9, '#3a3a42', esc=(.6, 1.2, 1.2))
    for x in (-1.2, 1.0): cil((x, 42.4, 0), .3, 1.2, '#4a4a52')
    fim(.02)
def onu():
    novo('marco_onu')          # Sede da ONU em Nova York: laje alta de vidro esverdeado + cupula baixa da Assembleia
    caixa((0, 77, 0), (22, 154, 6), '#7aa8a8'); caixa((0, 77, 3.05), (22.2, 154, .1), '#8ab8b8')
    for y in range(4, 154, 4): caixa((0, y, 3.12), (22, .25, .05), '#5a7a7a')
    caixa((30, 8, 6), (40, 16, 26), '#e8e4d8', afina=.85); torno((30, 16, 6), [(6, 0), (0, 3)], '#9aa2a8', lados=20)
    for i in range(8): cil((-26 + i * 4, 9, 22), .08, 18, '#9a9a9a', lados=6)
    fim(.02)
def zanzibar_palacio():
    novo('marco_zanzibar')     # Casa das Maravilhas (Zanzibar): palacio branco de varandas em volta e torre do relogio
    caixa((0, 12, 0), (40, 24, 30), '#f2efe6')
    for y in (8, 16, 24):
        caixa((0, y, 15.6), (42, .6, 3), '#e2ded2')
        for i in range(-10, 11): cil((i * 2, y - 4, 16.8), .35, 8, '#f2efe6', lados=8)
    caixa((0, 31, 0), (8, 14, 8), '#f2efe6'); cil((0, 33, 4.1), 2.4, .3, '#f4f4f2', rot=(m.pi / 2, 0, 0)); cil((0, 33, 4.2), .3, .4, '#2a2a30', rot=(m.pi / 2, 0, 0))
    caixa((0, 39, 0), (9, 2, 9), '#c8302a', afina=.2); fim(.02)
def ghirlandina():
    novo('marco_ghirlandina')  # Torre Ghirlandina (Modena, Italia): campanario romanico alto com agulha octogonal
    caixa((0, 22, 0), (10, 44, 10), '#e0d4bc')
    for y in range(6, 44, 7): caixa((0, y, 5.06), (2.4, 3, .1), '#4a3a2a', afina=.8)
    cil((0, 47, 0), 4.8, 6, '#d8ccb2', lados=8); cil((0, 58, 0), 4.4, 16, '#d0c4aa', raio_topo=.3, lados=8)
    caixa((-14, 10, -8), (20, 20, 30), '#d8ccb2'); caixa((-14, 21.5, -8), (21, 3, 31), '#a85a3a', afina=.2); fim(.02)
def ulua():
    novo('marco_ulua')         # Forte de San Juan de Ulua (Veracruz, Mexico): fortaleza de pedra no mar
    caixa((0, 6, 0), (60, 12, 40), '#9a9488')
    for x in (-30, 30):
        for z in (-20, 20): cil((x, 7, z), 6, 14, '#a8a294', lados=6)
    for i in range(-14, 15): caixa((i * 2, 12.8, 20.2), (1.1, 1.6, .5), '#9a9488')
    caixa((0, 16, 0), (14, 8, 10), '#b0aa9c'); cil((0, 23, 0), .2, 6, '#7a7a7a'); pano((.2, 26, 0), 3.6, 2.2, ['#2a8a4a', '#f4f4f2', '#c8302a'])
    bola((0, -1, 16), 50, '#3a7ab0', esc=(1.6, .04, .6)); fim(.02)
def trump_tower():
    novo('marco_trumptower')   # Trump Tower (Nova York): torre de vidro escuro em degraus, letreiro dourado
    for k, (w, h) in enumerate(((26, 40), (22, 40), (18, 40), (14, 40))):
        caixa((-k * 2, 20 + k * 40, -k * 2), (w, 40, w), '#2a2e36')
    for y in range(3, 160, 3): caixa((0, y, 13.05), (26, .3, .1), '#4a5262')
    caixa((0, 12, 13.2), (16, 2.2, .3), '#c9a24a'); fim(.02)

E.update(alexandria=farol_alexandria, notredame=notredame, versalhes=versalhes, waterloo=waterloo, onu=onu, zanzibar=zanzibar_palacio, ghirlandina=ghirlandina, ulua=ulua, trumptower=trump_tower)
alvo = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else list(E)
for k in alvo: E[k]()
