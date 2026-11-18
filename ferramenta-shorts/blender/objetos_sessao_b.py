# Objetos da sessao B feitos com formas.py (formas redondas): blender -b --python blender/objetos_sessao_b.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
H = (0, 0, math.pi / 2)    # deita o cilindro ao longo do eixo x
novo('syringe')            # seringa antiga de vidro: corpo, liquido, aletas, embolo, ponta e agulha longa
cil((0, .3, 0), .17, 1.3, '#d4eaf0', rot=H); cil((0, .3, 0), .125, 1.1, '#6fb8d6', rot=H)
cil((-.68, .3, 0), .3, .05, '#8a8a8a', rot=H); cil((-1.0, .3, 0), .045, .7, '#9a9a9a', rot=H); cil((-1.38, .3, 0), .2, .07, '#7a7a7a', rot=H)
cil((.76, .3, 0), .1, .22, '#a8a8a8', raio_topo=.04, rot=H); cil((1.3, .3, 0), .028, .85, '#e2e2e2', rot=H)
fim()
novo('kite')               # pipa de losango (vermelha e amarela), varetas em cruz, linha e rabo com lacos
D = (0, 0, math.pi / 4)
caixa((0, 1.3, 0), (.95, .95, .03), '#d8282f', rot=D); caixa((0.0, 1.3, .02), (.45, .45, .03), '#f2d060', rot=D)
cil((0, 1.3, .045), .018, 1.3, '#7a5a3a'); cil((0, 1.3, .045), .018, 1.3, '#7a5a3a', rot=(0, 0, math.pi / 2))
tubo([(0, .78, 0), (.12, .55, 0), (-.1, .32, 0), (.1, .1, 0)], .018, '#f4f4f0')
for (x, y) in ((.12, .55), (-.1, .32), (.1, .1)): bola((x, y, 0), .07, '#d8282f', achata=.5)
fim()
novo('key')                # chave de metal: aro, haste e dentes
arco((0, .75, 0), .16, '#c9a040', esp=.035, de=0, ate=2 * math.pi, n=18)
cil((0, .38, 0), .03, .56, '#c9a040'); cil((.08, .12, 0), .05, .06, '#c9a040', rot=(0, 0, math.pi / 2)); cil((.08, .26, 0), .05, .06, '#c9a040', rot=(0, 0, math.pi / 2))
fim()
novo('lightning_rod')      # para-raios: haste alta de metal com ponta em bola e base
cil((0, 1.6, 0), .03, 3.2, '#8a8a90'); bola((0, 3.25, 0), .07, '#c9a040'); cil((0, .06, 0), .22, .12, '#5a5a62')
cil((0, 1.0, 0), .07, .08, '#5a5a62'); cil((0, 2.0, 0), .07, .08, '#5a5a62')
fim()
def passaro(nome, bico_raio, bico_comp, bico_cor, corpo='#7a6a4a', barriga='#cdbf9a'):   # tentilhao pousado: corpo, cabeca, bico (varia), cauda, patas e olhos
    novo(nome)
    bola((0, .42, 0), .30, corpo, achata=.95); bola((0, .38, .06), .25, barriga); bola((0, .74, .18), .20, corpo)
    cil((0, .72, .18 + .17 + bico_comp / 2), bico_raio, bico_comp, bico_cor, raio_topo=max(.012, bico_raio * .25), rot=(math.pi / 2, 0, 0))
    bola((.11, .78, .3), .035, '#1b1b1f'); bola((-.11, .78, .3), .035, '#1b1b1f')
    caixa((0, .38, -.36), (.16, .06, .34), '#5a4a30', rot=(0.4, 0, 0)); caixa((0, .42, -.3), (.22, .05, .2), '#6a5a3a', rot=(0.3, 0, 0))
    tubo([(.09, .16, .02), (.09, .02, .06)], .016, '#c98a4a'); tubo([(-.09, .16, .02), (-.09, .02, .06)], .016, '#c98a4a')
    fim()
passaro('finch', .06, .13, '#d9a040')
passaro('finch_thick', .13, .17, '#e0a040', corpo='#4a3f33', barriga='#9a8a6a')
passaro('finch_long', .035, .42, '#c98a30', corpo='#8a7a55', barriga='#e0d4aa')
def vagem(nome, pod, ervilha):   # vagem aberta com ervilhas redondas saltando para fora
    novo(nome)
    cil((0, .2, 0), .14, 1.2, pod, rot=H)
    for i in range(6): bola((-.5 + i * .2, .32, 0), .14, ervilha, seg=14)
    tubo([(.6, .2, 0), (.78, .3, 0)], .03, pod)
    fim()
vagem('pea_green', '#2f6a22', '#a6e85c')
vagem('pea_yellow', '#2f6a22', '#f0c828')
novo('globe')              # globo terrestre: esfera azul, continentes verdes, aro de metal e pe
bola((0, 1.0, 0), .62, '#2f6fd0', seg=24)
for (x, y, z, r) in ((.0, 1.45, .35, .24), (-.35, 1.0, .5, .26), (.38, .78, .47, .2), (.25, 1.18, .55, .16), (-.5, 1.3, .2, .16)): bola((x, y, z), r, '#4fa84a', achata=.45, seg=10)
arco((0, 1.0, 0), .7, '#8a8a90', esp=.03, de=0, ate=2 * math.pi, n=24)
cil((0, .18, 0), .26, .08, '#6a4a2a'); cil((0, .42, 0), .06, .5, '#6a4a2a')
fim()
novo('stick')              # vara fincada no chao (gnomon): haste de madeira com ponta redonda e pedras na base
cil((0, 1.1, 0), .045, 2.2, '#8a6a42'); bola((0, 2.22, 0), .07, '#6a4a2a')
for a in range(5): bola((.16 * math.cos(a * 1.25), .06, .16 * math.sin(a * 1.25)), .09, '#8a8a82', achata=.6, seg=8)
fim()
novo('well')               # poco de pedra com telhadinho de madeira, corda e balde
cil((0, .4, 0), .6, .8, '#a8a698'); cil((0, .83, 0), .6, .1, '#b8b6a8'); cil((0, .89, 0), .4, .03, '#15151a')
for x in (-.62, .62): cil((x, 1.45, 0), .045, 1.3, '#7a5a3a')
cil((0, 2.05, 0), .05, 1.4, '#7a5a3a', rot=H); cil((0, 2.2, 0), .05, 1.5, '#8a6a42', raio_topo=.02, rot=H)
tubo([(0, 1.9, 0), (0, 1.3, 0)], .018, '#d8c898'); cil((0, 1.15, 0), .12, .18, '#6a4a2a', raio_topo=.1)
fim()
novo('rocket')             # foguete de 3 corpos (central + 2 laterais), ponta, listra preta, pernas e bocais
for x in (-.5, 0, .5):
    h = 3.0 if x else 3.5
    cil((x, h / 2 + .2, 0), .22, h, '#f2f2ee'); cil((x, h + .35, 0), .22, .3, '#f2f2ee', raio_topo=.06)
    cil((x, .9, 0), .222, .18, '#1b1b1f'); cil((x, .15, 0), .2, .12, '#3a3a40', raio_topo=.15)
cil((0, 3.95, 0), .222, .25, '#1b1b1f')
for x in (-.5, .5): tubo([(x * 1.3, .2, 0), (x * 2.0, -.0, 0)], .03, '#2a2a30')
fim()
novo('roadster')           # roadster vermelho conversivel, visto de lado: carroceria, para-brisa, rodas, farol
caixa((0, .42, 0), (2.2, .34, .95), '#d8282f'); caixa((.2, .66, 0), (1.0, .22, .85), '#d8282f', afina=.8)
caixa((-.05, .86, 0), (.04, .3, .85), '#9fd4ee', rot=(0, 0, .5)); caixa((.35, .72, 0), (.5, .2, .7), '#1b1b1f')
for x in (-.7, .7):
    for z in (-.5, .5): cil((x, .26, z), .26, .18, '#15151a', rot=(math.pi / 2, 0, 0)); cil((x, .26, z), .13, .2, '#b8b8c0', rot=(math.pi / 2, 0, 0))
bola((-1.12, .45, .3), .07, '#f2e8a0'); bola((-1.12, .45, -.3), .07, '#f2e8a0')
fim()
novo('coin')               # moeda de ouro grande em pe: disco, aro e barra do simbolo, apoiada em suporte
cil((0, .9, 0), .7, .12, '#f2b822', rot=(math.pi / 2, 0, 0)); cil((0, .9, .02), .6, .12, '#e0a010', rot=(math.pi / 2, 0, 0))
cil((-.1, .9, .09), .07, .7, '#fff0a0'); caixa((.12, 1.08, .09), (.3, .09, .04), '#fff0a0'); caixa((.12, .72, .09), (.3, .09, .04), '#fff0a0')
caixa((.12, .9, .09), (.34, .09, .04), '#fff0a0'); cil((0, .16, 0), .35, .08, '#6a4a2a')
fim()
