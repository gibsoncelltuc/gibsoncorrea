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
    novo('burr')                         # carrapicho (Velcro): bolinha verde-marrom com ganchinhos em volta, num talinho
    bola((0, .32, 0), .13, '#7a8a3a')
    for i in range(46):
        a = i * 2.4; yy = 1 - 2 * (i + .5) / 46; r = (1 - yy * yy) ** .5; d = (r * m.cos(a), yy, r * m.sin(a))
        p0 = (d[0] * .12, .32 + d[1] * .12, d[2] * .12); p1 = (d[0] * .2, .32 + d[1] * .2, d[2] * .2)
        tubo([p0, p1], .008, '#8a7a3a'); bola((p1[0] * 1.04, p1[1] + .006, p1[2] * 1.04), .012, '#c8b060')
    tubo([(0, .2, 0), (.02, .1, 0), (0, 0, 0)], .012, '#5a6a2a')
    escala(2.8)
    fim(.0)

E = dict(panela=panela, frasco=frasco, tubos=tubos, enxofre=enxofre, gosma=gosma, borracha=borracha, microscopio=microscopio, balanca=balanca, lupa=lupa, bancada=bancada, burr=burr)
alvo = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else list(E)
for k in alvo: E[k]()
