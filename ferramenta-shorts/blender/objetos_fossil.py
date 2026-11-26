# 26/11 Formato "Fossil" (pre-historia, EUA): crocodilo de agua salgada + rivais de cada era. blender -b --python blender/objetos_fossil.py
# Eixos: x = comprimento (FRENTE = +x), y = altura, z = largura. Medidas livres (o video escala pelo tamanho real em metros).
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *

def olho(x, y, z, r=.05, cor='#e8c23a'):
    bola((x, y, z), r, cor, seg=10); bola((x + r * .35, y, z + (r * .35 if z > 0 else -r * .35)), r * .55, '#111111', seg=8)
def dentes(x0, x1, y, z, n, tam, cor='#f2ecd8', para_baixo=True):
    for i in range(n):
        x = x0 + (x1 - x0) * i / max(1, n - 1)
        for s in (1, -1): cil((x, y, z * s), tam * .35, tam, cor, raio_topo=.002, rot=(math.pi if para_baixo else 0, 0, 0), lados=6)
def cauda(x0, y0, comp, r0, cor, n=10, onda=0.0, desce=0.0):
    for i in range(n):
        t = i / n; bola((x0 - comp * t, y0 - desce * t + onda * math.sin(t * 3), 0), r0 * (1 - t * .85), cor, seg=12, esc=(1.6, 1, 1))
def perna(x, z, alto, grossa, cor, dobra=.0):
    tubo([(x, alto, z), (x + dobra, alto * .5, z * 1.15), (x + .05, 0.03, z * 1.2)], grossa, cor, passo=.8); bola((x + .1, .03, z * 1.2), grossa * 1.3, cor, esc=(1.6, .5, 1.2))

def quadrupede_reptil(nome, cor, cor_b, comp=4.0, focinho=1.0, alto=.35, escamas=True, dorso=None):
    novo(nome)
    L = comp
    bola((0, alto + .18, 0), .42, cor, esc=(L * .32, .55, .85))                       # corpo baixo e comprido
    bola((0, alto + .06, 0), .38, cor_b, esc=(L * .3, .35, .8))                       # barriga clara
    cauda(-L * .3, alto + .16, L * .55, .3, cor, n=14)
    hx = L * .38; bola((hx, alto + .22, 0), .24, cor, esc=(1.2, .7, 1))                # cabeca
    bola((hx + .45 * focinho, alto + .16, 0), .16, cor, esc=(2.6 * focinho, .5, .8))   # focinho
    bola((hx + .42 * focinho, alto + .06, 0), .14, cor_b, esc=(2.5 * focinho, .35, .75))  # mandibula
    dentes(hx + .15, hx + .8 * focinho, alto + .11, .1, 7, .06)
    olho(hx + .08, alto + .36, .12); olho(hx + .08, alto + .36, -.12)
    for x in (L * .22, -L * .14):
        for z in (.36, -.36): perna(x, z, alto + .1, .09, cor, dobra=.06)
    if escamas:
        for i in range(18): t = i / 18; cil((L * .3 - t * L * .75, alto + .42 - t * .25, 0), .045, .09, dorso or cor, raio_topo=.01, lados=5)
    fim(.01)

def teropode(nome, cor, cor_b, cabeca=1.0, bracos=.35, crista=None, comp=5.0):
    novo(nome)
    L = comp; H = 1.55
    bola((0, H, 0), .5, cor, esc=(L * .2, .9, .75))                                   # tronco
    bola((0, H - .25, 0), .42, cor_b, esc=(L * .18, .6, .65))
    tubo([(L * .16, H + .15, 0), (L * .27, H + .45, 0), (L * .32, H + .55, 0)], .22, cor)   # pescoco
    hx = L * .36; hy = H + .55
    bola((hx, hy, 0), .3 * cabeca, cor, esc=(2.2, 1.1, .9))                           # cranio
    bola((hx + .15 * cabeca, hy - .22 * cabeca, 0), .22 * cabeca, cor_b, esc=(2.4, .5, .8))   # mandibula
    dentes(hx + .05, hx + .55 * cabeca, hy - .1 * cabeca, .14 * cabeca, 6, .08 * cabeca)
    olho(hx + .2 * cabeca, hy + .16 * cabeca, .2 * cabeca, r=.05 * cabeca, cor='#e05a1a'); olho(hx + .2 * cabeca, hy + .16 * cabeca, -.2 * cabeca, r=.05 * cabeca, cor='#e05a1a')
    if crista:
        for i in range(5): cil((hx - .1 + i * .08, hy + .3 * cabeca, 0), .05, .12 + .04 * (i % 2), crista, raio_topo=.01, lados=5)
    cauda(-L * .18, H + .05, L * .55, .38, cor, n=14, desce=-.2)
    for z in (.28, -.28):                                                              # pernas fortes
        tubo([(0, H - .2, z), (.25, .85, z * 1.1), (-.12, .35, z * 1.1), (.15, .05, z * 1.1)], .17, cor, passo=.7)
        bola((.3, .05, z * 1.1), .16, cor, esc=(2, .5, 1.1))
        tubo([(L * .17, H, z * .9), (L * .17 + bracos * .6, H - bracos, z * .9)], .06, cor)   # bracinhos
    fim(.01)

def peixe(nome, cor, cor_b, comp=4.0, alt=1.0, couraça=None, barbatana=None, dentao=False):
    novo(nome)
    hl = comp / 2 * .8; ea = alt * .5
    bola((0, 0, 0), .5, cor, esc=(hl / .5, alt, .7 * alt))                              # corpo fusiforme
    bola((0, -.12 * alt, 0), .5, cor_b, esc=(hl / .5 * .92, alt * .62, .62 * alt))
    if couraça: bola((hl * .62, .04, 0), .5, couraça, esc=(hl * .9, alt * 1.08, .78 * alt))   # placas osseas da cabeca
    bola((-hl * .95, 0, 0), .25, cor, esc=(1.6, .7 * alt, .6))                            # pedunculo
    prisma((-hl * 1.05, 0, 0), [(0, 0), (-.7 * alt, .9 * alt), (-.45 * alt, 0), (-.7 * alt, -.7 * alt)], .06, barbatana or cor)   # cauda
    prisma((-hl * .05, ea * .85, 0), [(.35, 0), (-.25, .75 * alt), (-.55, 0)], .06, barbatana or cor)   # nadadeira dorsal
    for s_ in (1, -1): prisma((hl * .35, -ea * .7, .28 * alt * s_), [(0, 0), (-.6, -.4), (-.3, 0)], .04, barbatana or cor)
    olho(hl * .82, ea * .3, .26 * alt, r=.07 * alt, cor='#d8d8d8'); olho(hl * .82, ea * .3, -.26 * alt, r=.07 * alt, cor='#d8d8d8')
    if dentao: dentes(hl * .72, hl * .98, -ea * .35, .2 * alt, 6, .1 * alt)
    fim(.01)

# ---------------- os animais ----------------
quadrupede_reptil('crocodilo', '#4c5a33', '#c9c08a', comp=4.2, dorso='#3a4527')                   # crocodilo de agua salgada (6 m)
quadrupede_reptil('deinosuchus', '#3f4230', '#b8ad86', comp=4.6, focinho=1.1, dorso='#2f3224')     # 10 m
quadrupede_reptil('purussaurus', '#5a4e36', '#cdbf96', comp=4.4, focinho=1.25, dorso='#463c29')    # 10 m, focinho largo
quadrupede_reptil('postosuchus', '#7a4a32', '#d9b68e', comp=3.4, focinho=.8, alto=.75, dorso='#5c3624')   # 4,5 m, pernas altas
quadrupede_reptil('megalania', '#6a6150', '#c8bea2', comp=3.8, focinho=.7, alto=.4, escamas=False)        # lagarto 5,5 m

novo('inostrancevia')   # gorgonopsideo 3,5 m: corpo de cao gigante, presas de sabre
bola((0, 1.0, 0), .5, '#8a6a4a', esc=(2.4, .9, .8)); bola((0, .85, 0), .4, '#c9a982', esc=(2.2, .6, .7))
bola((1.35, 1.15, 0), .32, '#8a6a4a', esc=(1.6, 1, .9)); bola((1.6, .98, 0), .2, '#c9a982', esc=(1.8, .5, .8))
for s in (1, -1): cil((1.62, .9, .09 * s), .045, .38, '#f2ecd8', raio_topo=.004, rot=(math.pi, 0, 0), lados=6)   # sabres
olho(1.45, 1.3, .2, cor='#e0a020'); olho(1.45, 1.3, -.2, cor='#e0a020')
cauda(-1.1, .95, 1.4, .22, '#8a6a4a', n=10)
for x in (.75, -.7):
    for z in (.32, -.32): perna(x, z, .9, .12, '#8a6a4a', dobra=.08)
fim(.01)

teropode('trex', '#5b4a33', '#cdb894', cabeca=1.35, bracos=.22, comp=5.2)
teropode('allosaurus', '#7a5a3a', '#d8c09a', cabeca=1.0, bracos=.45, crista='#b04020', comp=5.0)

peixe('dunkleosteus', '#4f5a62', '#c0c8cc', comp=3.6, alt=1.1, couraça='#3c4248', barbatana='#3f4a52')
peixe('megalodon', '#5f6e7a', '#e8eef2', comp=5.2, alt=1.0, barbatana='#55636e', dentao=True)

novo('anomalocaris')   # 1 m: corpo segmentado com abas, dois bracos espinhosos na frente
for i in range(11):
    x = .9 - i * .2; w = .35 * (1 - abs(i - 3) / 12); bola((x, 0, 0), .16, '#c06a4a', esc=(1, .45, 2.2 * w / .35))
    for s in (1, -1): prisma((x, 0, (.38 * w / .35 + .05) * s), [(0, 0), (-.18, .02), (-.2, .25 * s / abs(s))], .02, '#d88a62')
for s in (1, -1):
    tubo([(1.05, -.02, .12 * s), (1.35, -.1, .18 * s), (1.45, -.3, .14 * s), (1.3, -.42, .1 * s)], .04, '#e09a72', passo=.6)
olho(1.0, .12, .22, r=.07, cor='#222222'); olho(1.0, .12, -.22, r=.07, cor='#222222')
prisma((-1.25, 0, 0), [(0, 0), (-.4, .35), (-.3, 0), (-.4, -.35)], .03, '#c06a4a')
fim(.005)

novo('trilobita')   # 10 cm (aparece em cardume)
bola((0, 0, 0), .5, '#7b6a52', esc=(1.4, .3, 1)); bola((.55, .02, 0), .32, '#8a785e', esc=(.9, .35, 1.4))
for i in range(7): cil((.3 - i * .14, .14, 0), .38 - i * .03, .03, '#6a5a44', rot=(math.pi / 2, 0, 0), lados=16)
fim(.005)

novo('cameroceras')   # nautiloide de concha reta (ate ~6 m): cone comprido + tentaculos
cil((0, 0, 0), .45, 4.0, '#c8b08a', raio_topo=.06, rot=(0, 0, math.pi / 2), lados=20)
for i in range(12): cil((-1.6 + i * .3, 0, 0), .46 - i * .032, .04, '#9a7e5a', rot=(0, 0, math.pi / 2), lados=20)   # aneis da concha
for k in range(8):
    a = k * math.pi / 4; tubo([(2.0, .15 * math.sin(a), .15 * math.cos(a)), (2.5, .3 * math.sin(a), .3 * math.cos(a)), (2.9, .2 * math.sin(a) - .2, .35 * math.cos(a))], .05, '#b0705a', passo=.6)
olho(2.05, .25, .3, r=.08, cor='#222222'); olho(2.05, .25, -.3, r=.08, cor='#222222')
fim(.01)

novo('arthropleura')   # centopeia gigante 2,6 m
for i in range(26):
    x = 1.3 - i * .1; bola((x, .18, 0), .2, '#5a3a2a' if i % 2 else '#6e4a34', esc=(.6, .45, 1.6))
    for s in (1, -1): tubo([(x, .14, .25 * s), (x + .03, .08, .42 * s), (x + .05, 0, .5 * s)], .022, '#3e2a1e', passo=.6)
bola((1.42, .17, 0), .17, '#4a2e20', esc=(.9, .6, 1.2))
for s in (1, -1): tubo([(1.5, .2, .06 * s), (1.75, .32, .18 * s)], .02, '#3e2a1e')
fim(.005)

novo('meganeura')   # libelula gigante (70 cm de envergadura)
for i in range(9): bola((.25 - i * .09, 0, 0), .045, '#2a5a6a', esc=(1.2, 1, 1))
bola((.33, 0, 0), .07, '#2a4a5a'); olho(.36, .04, .05, r=.035, cor='#3aa0c8'); olho(.36, .04, -.05, r=.035, cor='#3aa0c8')
for x, s in ((.18, 1), (.18, -1), (.06, 1), (.06, -1)): bola((x, .02, .4 * s), .2, '#cfe6f0', esc=(.35, .05, 2))
fim(.003)

novo('titanoboa')   # cobra de 13 m, enrolada em S
pts = []
for i in range(60):
    t = i / 59; pts.append((2.2 - t * 4.6, .32, 1.1 * math.sin(t * 5.5)))
for i, p in enumerate(pts): bola(p, .32 * (1 - .55 * max(0, (i - 40) / 20)), '#4a5236' if i % 4 else '#2e3322', seg=12)
bola((2.5, .38, .0), .3, '#4a5236', esc=(1.6, .7, 1)); olho(2.65, .55, .17, r=.05); olho(2.65, .55, -.17, r=.05)
fim(.01)

# ---------------- plantas das eras (cenario) ----------------
novo('licopsida')   # "arvore" do Carbonifero (Lepidodendron): tronco escamado + tufo
cil((0, 2.5, 0), .28, 5.0, '#5a5a3a', raio_topo=.2, lados=10)
for i in range(4): tubo([(0, 4.9, 0), (.8 * math.cos(i * 1.6), 5.6, .8 * math.sin(i * 1.6))], .1, '#5a5a3a')
for i in range(4): bola((.9 * math.cos(i * 1.6), 5.75, .9 * math.sin(i * 1.6)), .45, '#3e6a2a', esc=(1, 1.4, 1))
fim(.01)
novo('samambaia')   # feto arborescente
cil((0, 1.2, 0), .12, 2.4, '#4a3a2a', lados=8)
for i in range(8):
    a = i * math.pi / 4; tubo([(0, 2.4, 0), (.7 * math.cos(a), 2.7, .7 * math.sin(a)), (1.3 * math.cos(a), 2.3, 1.3 * math.sin(a))], .07, '#4f7a2e', passo=.5)
fim(.01)
