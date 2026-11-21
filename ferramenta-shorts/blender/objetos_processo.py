# OBJETOS DE PROCESSO (19/11, ordem do Gibson: "mostrar a borracha sendo criada, ele jogando o produto, virando pasta").
# Usados pela ENCENACAO DA NARRACAO no mkvideo (misturou -> panela; jogou/caiu -> gosma voando; virou/endureceu -> produto novo...).
# blender -b --python blender/objetos_processo.py [nome ...]
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
import formas
def escala(F):   # objetos do kit sao no tamanho do boneco (~1 a 1,5 m): amplia antes de exportar
    for v in formas._S['bm'].verts: v.co *= F

def panela():
    novo('panela')                       # panela/caldeirao com mistura borbulhando
    torno((0, 0, 0), [(.22, 0), (.27, .06), (.28, .3), (.3, .32)], '#4a4a52', lados=28)
    torno((0, .26, 0), [(.27, 0), (0, .01)], '#c9a24a', lados=28)
    for i in range(6): bola((.15 * m.cos(i * 1.1), .28, .15 * m.sin(i * 1.1)), .04 + .01 * (i % 2), '#e0c060')
    for s in (-1, 1): arco((s * .3, .27, 0), .05, '#2a2a30', esp=.015)
    escala(2.8)
    fim(.01)
def frasco():
    novo('frasco')                       # frasco quimico (erlenmeyer) com liquido verde
    torno((0, 0, 0), [(.12, 0), (.13, .02), (.05, .2), (.04, .3), (.045, .31)], '#d8eef4', lados=24)
    torno((0, .005, 0), [(.132, 0), (.135, .02), (.1, .09), (0, .1)], '#4ac87a', lados=24)
    cil((0, .32, 0), .04, .03, '#8a5a3a')
    escala(4.0)
    fim(.01)
def tubos():
    novo('tubos')                        # suporte com tubos de ensaio coloridos
    caixa((0, .03, 0), (.36, .06, .1), '#8a5a3a'); caixa((0, .14, 0), (.36, .02, .1), '#8a5a3a')
    for i, c in enumerate(('#d8282f', '#2a8ad8', '#e8c45a', '#4ac87a')):
        x = -.12 + i * .08; cil((x, .14, 0), .018, .24, '#e8f4f8', lados=12); cil((x, .07, 0), .016, .1, c, lados=12)
    escala(3.6)
    fim(.01)
def enxofre():
    novo('enxofre')                      # monte de po amarelo (enxofre, polvora, farinha: cor pela cena)
    bola((0, 0, 0), .2, '#f2d23a', esc=(1.2, .45, 1.1))
    for i in range(7): bola((.16 * m.cos(i), .02, .16 * m.sin(i)), .05, '#e8c42a')
    escala(3.5)
    fim(.01)
def gosma():
    novo('gosma')                        # gosma/massa mole (borracha crua, massa, cola)
    bola((0, .05, 0), .12, '#c8a050', esc=(1.3, .45, 1.1))
    for i in range(5): bola((.1 * m.cos(i * 1.3), .03, .1 * m.sin(i * 1.3)), .06, '#b89040', esc=(1, .6, 1))
    bola((.04, .1, .02), .04, '#e0c070')
    escala(4.5)
    fim(.01)
def borracha():
    novo('borracha')                     # borracha pronta: placa escura firme e elastica (dobrando) + bola
    for i in range(6): caixa((-.15 + i * .06, .03 + .02 * m.sin(i), 0), (.065, .03, .24), '#6a4630', rot=(0, 0, .3 * m.cos(i)))
    bola((.2, .07, .05), .07, '#8a5a3a')
    escala(3.6)
    fim(.02)
def microscopio():
    novo('microscopio')
    caixa((0, .02, 0), (.2, .04, .24), '#2a2a30'); tubo([(0, .04, -.08), (0, .2, -.08), (0, .28, -.02)], .025, '#2a2a30')
    cil((0, .22, .03), .04, .2, '#e8e8ec', rot=(.4, 0, 0)); cil((0, .1, .04), .07, .015, '#e8e8ec'); cil((0, .33, -.02), .025, .06, '#2a2a30', rot=(.4, 0, 0))
    escala(3.4)
    fim(.01)
def balanca():
    novo('balanca')                      # balanca de pratos
    cil((0, .02, 0), .1, .04, '#c9a24a'); cil((0, .2, 0), .015, .34, '#c9a24a'); caixa((0, .37, 0), (.5, .02, .02), '#c9a24a')
    for s in (-1, 1):
        tubo([(s * .24, .37, 0), (s * .24, .22, 0)], .006, '#8a7a4a'); torno((s * .24, .2, 0), [(.09, 0), (.1, .02)], '#c9a24a', lados=20)
    escala(2.8)
    fim(.01)
def lupa():
    novo('lupa')
    torno((0, 0, 0), [(.1, 0), (.1, .02), (.085, .02), (.085, 0)], '#c9a24a', lados=24); cil((0, .01, 0), .086, .008, '#cfe8f4', lados=24)
    cil((0, .01, -.17), .018, .16, '#6a3a1f', rot=(m.pi / 2, 0, 0))
    escala(4.5)
    fim(.01)
def bancada():
    novo('bancada')                      # mesa de laboratorio/oficina
    caixa((0, .9, 0), (1.8, .08, .7), '#8a5a3a')
    for x in (-.8, .8):
        for z in (-.28, .28): cil((x, .45, z), .04, .9, '#6a4426', lados=8)
    caixa((0, .3, 0), (1.6, .03, .6), '#7a4e30')
    escala(1.0)
    fim(.02)
def burr():
    novo('burr')                         # carrapicho de bardana (Velcro): miolo marrom, MUITOS espinhos finos cor de palha com a ponta em GANCHO (20/11: o verde com espinhos pretos parecia o coronavirus)
    C = (0, .34, 0); r0 = .12
    bola(C, r0, '#6b4a26', seg=14)
    n = 120; ga = m.pi * (3 - m.sqrt(5))
    for i in range(n):
        yy = 1 - 2 * (i + .5) / n; rr = (1 - yy * yy) ** .5; th = ga * i
        d = (rr * m.cos(th), yy, rr * m.sin(th))
        if d[1] < -.8: continue
        p0 = tuple(C[k] + d[k] * r0 * .85 for k in range(3)); p1 = tuple(C[k] + d[k] * (r0 + .085) for k in range(3))
        up = (0, 1, 0) if abs(d[1]) < .9 else (1, 0, 0)
        side = (d[1] * up[2] - d[2] * up[1], d[2] * up[0] - d[0] * up[2], d[0] * up[1] - d[1] * up[0])
        p2 = tuple(p1[k] + side[k] * .03 - d[k] * .018 for k in range(3))
        tubo([p0, p1, p2], .0065, '#c9a45a' if i % 3 else '#b88a3e')
    tubo([(0, .22, 0), (.02, .1, 0), (0, 0, 0)], .011, '#4f5a24')
    escala(3.2)
    fim(.0)

def turbina():
    novo('turbina')                      # turbina da usina geotermica (vulcao/vapor): torre branca, cabine, hub e 3 pas
    cil((0, .05, 0), .22, .1, '#7a7f86', lados=16)
    torno((0, 0, 0), [(.12, .1), (.09, 1.5), (.07, 1.6)], '#e6e8ec', 18)
    caixa((0, 1.62, 0.05), (.2, .16, .3), '#d4d7dc')
    bola((0, 1.62, .22), .1, '#c9ccd2', seg=12)
    for k in range(3):
        a = k * 2.0944 + .4
        tubo([(0, 1.62, .25), (.28 * m.sin(a), 1.62 + .28 * m.cos(a), .26), (.62 * m.sin(a), 1.62 + .62 * m.cos(a), .27)], .035, '#f2f3f5')
    escala(2.4)
    fim(.0)

def rato():
    novo('rato')                         # 21/11: rato cinza com orelhas e rabo rosa (Paris: 'os roedores viraram um prato chique')
    bola((0, .11, 0), .10, '#8d8d94', seg=12); bola((0, .11, .09), .085, '#8d8d94', seg=12); bola((0, .11, -.07), .08, '#85858c', seg=10)
    bola((0, .10, .17), .06, '#9a9aa2', seg=10); bola((0, .09, .225), .022, '#e58f9a', seg=8)
    for sx in (-1, 1):
        bola((sx * .045, .175, .14), .034, '#e8a0aa', seg=8); bola((sx * .03, .125, .21), .011, '#1a1a1a', seg=6)
        cil((sx * .05, .02, .05), .014, .04, '#e8a0aa', lados=6); cil((sx * .05, .02, -.06), .014, .04, '#e8a0aa', lados=6)
    tubo([(0, .09, -.13), (0, .04, -.25), (0, .07, -.38), (.04, .05, -.46)], .011, '#e0a0a8')
    escala(1.0)
    fim(.0)
def trave():
    novo('trave')                        # 21/11: gol de futebol (2 traves, travessao e rede) - Guerra do Futebol
    for sx in (-1, 1): cil((sx * 1.1, .6, 0), .045, 1.2, '#f6f6f2', lados=10); tubo([(sx * 1.1, 1.2, 0), (sx * 1.1, .6, -.55), (sx * 1.1, 0, -.7)], .02, '#dcdcdc')
    caixa((0, 1.2, 0), (2.28, .09, .09), '#f6f6f2'); tubo([(-1.1, 1.2, -.0), (-1.1, 1.0, -.55), (1.1, 1.0, -.55), (1.1, 1.2, 0)], .018, '#dcdcdc')
    for k in range(9): tubo([(-1.1 + k * .275, 1.0, -.55), (-1.1 + k * .275, 0, -.7)], .008, '#e6e6e6')
    for k in range(5): tubo([(-1.1, 1.0 - k * .2, -.55 - k * .03), (1.1, 1.0 - k * .2, -.55 - k * .03)], .008, '#e6e6e6')
    escala(1.4)
    fim(.0)

E = dict(panela=panela, frasco=frasco, tubos=tubos, enxofre=enxofre, gosma=gosma, borracha=borracha, microscopio=microscopio, balanca=balanca, lupa=lupa, bancada=bancada, burr=burr, turbina=turbina, rato=rato, trave=trave)
alvo = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else list(E)
for k in alvo: E[k]()
