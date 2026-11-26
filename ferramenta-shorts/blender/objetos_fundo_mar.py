# 26/11 Videos longos Fundo do Mar: 8 criaturas (olham para +x, perfil). blender -b --python blender/objetos_fundo_mar.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
P = '#101014'; B = '#f4f4f0'

def olho(c, r, iris='#1b1b22', brilho=True):
    bola(c, r, B, seg=12); bola((c[0] + r * .45, c[1], c[2] + r * .5), r * .55, iris, seg=10)
    if brilho: luz(True); bola((c[0] + r * .6, c[1] + r * .25, c[2] + r * .75), r * .18, '#ffffff', seg=6); luz(False)

def dentes(x0, x1, y, z0, z1, n, h, para_baixo=True, col='#e8f0ff'):
    for i in range(n):
        t = i / max(1, n - 1); x = x0 + (x1 - x0) * t; z = z0 + (z1 - z0) * t
        cil((x, y - h / 2 if para_baixo else y + h / 2, z), h * .22, h, col, raio_topo=0.002, rot=(math.pi if para_baixo else 0, 0, 0), lados=6)

# 1 PEIXE-DIABO (anglerfish): corpo redondo escuro, boca enorme com dentes de vidro, vara com lanterna azul
novo('peixe_diabo')
bola((0, 0, 0), .5, '#2a2430', esc=(1.15, .95, .85))
bola((.42, -.12, 0), .34, '#1a1520', esc=(1, .7, .9))                      # mandibula
bola((.5, -.05, 0), .22, '#3a0d14', esc=(.6, .55, .8))                     # boca aberta (vermelho escuro)
dentes(.32, .7, .12, -.18, .18, 9, .16, True); dentes(.34, .72, -.24, -.16, .16, 8, .13, False)
olho((.18, .24, .3), .06); olho((.18, .24, -.3), .06)
tubo([(.05, .45, 0), (.25, .78, 0), (.55, .86, 0), (.72, .7, 0)], .022, '#3a3440')
luz(True); bola((.74, .64, 0), .08, '#7fe9ff', seg=14); luz(False)           # lanterna viva
prisma((-.6, 0, 0), [(0, .32), (-.38, .52), (-.28, 0), (-.38, -.5), (0, -.3)], .05, '#2a2430')   # cauda
prisma((-.1, .42, 0), [(-.2, 0), (0, .2), (.18, 0)], .04, '#2a2430')
fim(.01)

# 2 PEIXE-BARRIL (barreleye): corpo prateado, cupula transparente com dois olhos verdes dentro
novo('peixe_barril')
bola((0, 0, 0), .32, '#8a929c', esc=(1.9, .8, .55))
bola((.38, .2, 0), .26, '#cfe8f2', esc=(1.1, 1, .8))                       # cupula (vidro claro)
luz(True); bola((.36, .2, .08), .07, '#6cff7a', seg=12); bola((.36, .2, -.08), .07, '#6cff7a', seg=12); luz(False)
bola((.62, .04, .1), .025, P, seg=6); bola((.62, .04, -.1), .025, P, seg=6)   # narinas (parecem olhos)
prisma((-.72, 0, 0), [(0, .18), (-.3, .32), (-.22, 0), (-.3, -.3), (0, -.16)], .04, '#6f7781')
prisma((0, -.22, .2), [(-.2, 0), (0, -.22), (.2, 0)], .02, '#9aa2ad'); prisma((0, -.22, -.2), [(-.2, 0), (0, -.22), (.2, 0)], .02, '#9aa2ad')
fim(.01)

# 3 TUBARAO-DUENDE (goblin shark): rosa, focinho em lamina, mandibula projetada
novo('tubarao_duende')
bola((0, 0, 0), .4, '#e7a6a8', esc=(3.2, .75, .7))
bola((1.25, .12, 0), .18, '#efb6b6', esc=(2.4, .35, .5))                   # focinho chato
bola((.98, -.2, 0), .2, '#c98184', esc=(1.2, .5, .7))                      # mandibula para fora
dentes(.85, 1.12, -.1, -.1, .1, 7, .1, False, '#fff6f0'); dentes(.86, 1.12, -.3, -.1, .1, 6, .1, True, '#fff6f0')
olho((.95, .12, .2), .04)
prisma((0, .34, 0), [(-.3, 0), (0, .36), (.28, 0)], .04, '#d99597')
prisma((-1.3, 0, 0), [(0, .1), (-.6, .55), (-.4, 0), (-.25, -.25), (0, -.1)], .05, '#d99597')
prisma((.3, -.24, .24), [(-.25, 0), (-.05, -.3), (.2, 0)], .02, '#d99597'); prisma((.3, -.24, -.24), [(-.25, 0), (-.05, -.3), (.2, 0)], .02, '#d99597')
fim(.01)

# 4 LULA-VAMPIRA: corpo vermelho escuro, capa entre os bracos, olhos azuis, nadadeiras
novo('lula_vampira')
bola((0, .35, 0), .32, '#7a1426', esc=(.85, 1.25, .85))
bola((-.05, .78, 0), .14, '#8c1a2e', esc=(1.4, .6, .4)); bola((.0, .74, .32), .1, '#8c1a2e', esc=(.6, .4, 1.5)); bola((.0, .74, -.32), .1, '#8c1a2e', esc=(.6, .4, 1.5))
luz(True); bola((.2, .32, .16), .07, '#59c8ff', seg=12); bola((.2, .32, -.16), .07, '#59c8ff', seg=12); luz(False)
torno((0, -.02, 0), [(.3, .05), (.55, -.25), (.62, -.45), (.05, -.5)], '#5a0d1c', lados=16, tampa=True)   # capa (guarda-chuva)
for i in range(8): a = i * math.pi / 4; tubo([(.15 * math.cos(a), 0, .15 * math.sin(a)), (.55 * math.cos(a), -.5, .55 * math.sin(a))], .035, '#4a0a17')
fim(.01)

# 5 LULA-GIGANTE: manto longo, 8 bracos + 2 tentaculos longos, olho enorme
novo('lula_gigante')
bola((0, 0, 0), .45, '#c8483c', esc=(3.4, .9, .9))
prisma((-1.55, 0, 0), [(0, .35), (-.4, 0), (0, -.35)], .04, '#b13d33')
olho((1.05, .1, .34), .17, '#101018'); olho((1.05, .1, -.34), .17, '#101018')
for i in range(8):
    a = i * math.pi / 4; dy, dz = .25 * math.cos(a), .25 * math.sin(a)
    tubo([(1.35, dy, dz), (2.1, dy * 1.6 - .1, dz * 1.6), (2.7, dy * 1.2 - .25, dz * 1.3)], .06, '#b84236')
tubo([(1.35, -.05, .1), (2.4, -.35, .3), (3.6, -.5, .2), (3.9, -.42, .1)], .035, '#a8382e'); tubo([(1.35, -.05, -.1), (2.4, -.35, -.3), (3.6, -.5, -.2), (3.9, -.42, -.1)], .035, '#a8382e')
fim(.01)

# 6 POLVO-DUMBO: corpo de sino claro, duas "orelhas" (nadadeiras), bracos curtos com membrana
novo('polvo_dumbo')
bola((0, .2, 0), .32, '#f3b58a', esc=(1, 1.1, 1))
bola((.06, .5, .3), .16, '#efa77a', esc=(.5, .9, 1.4)); bola((.06, .5, -.3), .16, '#efa77a', esc=(.5, .9, 1.4))   # orelhas
olho((.26, .26, .14), .06); olho((.26, .26, -.14), .06)
torno((0, -.05, 0), [(.3, .05), (.46, -.18), (.42, -.28), (.05, -.24)], '#e89c70', lados=16)
fim(.01)

# 7 TUBARAO-DA-GROENLANDIA: cinza escuro, robusto, olho pequeno claro, nadadeiras pequenas
novo('tubarao_groenlandia')
bola((0, 0, 0), .5, '#4b5158', esc=(3.6, .85, .85))
bola((1.5, -.02, 0), .32, '#555b63', esc=(1.1, .7, .9))
olho((1.62, .12, .22), .04, '#cfe3ea', False)
prisma((.1, .4, 0), [(-.25, 0), (0, .22), (.22, 0)], .04, '#43484f'); prisma((-.6, .36, 0), [(-.18, 0), (0, .16), (.16, 0)], .04, '#43484f')
prisma((-1.75, 0, 0), [(0, .15), (-.55, .5), (-.4, 0), (-.5, -.35), (0, -.12)], .05, '#43484f')
prisma((.7, -.34, .3), [(-.3, 0), (-.1, -.3), (.2, 0)], .02, '#43484f'); prisma((.7, -.34, -.3), [(-.3, 0), (-.1, -.3), (.2, 0)], .02, '#43484f')
fim(.01)

# 8 AGUA-VIVA IMORTAL: sino transparente com miolo vermelho e tentaculos finos
novo('agua_viva_imortal')
luz(True)
torno((0, 0, 0), [(.02, .5), (.25, .45), (.4, .25), (.42, .05), (.35, 0)], '#bfe9ff', lados=20, tampa=False)
bola((0, .22, 0), .14, '#ff5a6e', esc=(1, .8, 1))
for i in range(16): a = i * math.pi / 8; tubo([(.36 * math.cos(a), 0, .36 * math.sin(a)), (.4 * math.cos(a), -.45, .4 * math.sin(a)), (.33 * math.cos(a), -.8, .33 * math.sin(a))], .012, '#e6f6ff', passo=1.5)
luz(False)
fim(.005)
