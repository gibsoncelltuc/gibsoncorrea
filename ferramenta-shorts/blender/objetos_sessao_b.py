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
novo('sink')               # pia de banheiro: bacia branca oval com cuba azulada, torneira cromada em L e pedestal
bola((0, .95, 0), .62, '#f6f6f2', achata=.35, seg=24, esc=(1.25, 1, .85)); bola((0, 1.05, .02), .46, '#8fb8d8', achata=.22, seg=20, esc=(1.2, 1, .8))
cil((0, .52, -.05), .24, .9, '#ecece8', raio_topo=.3); cil((0, .06, -.05), .38, .1, '#ecece8')
tubo([(0, 1.1, -.4), (0, 1.5, -.4), (0, 1.55, -.22)], .045, '#c0c4cc'); bola((.0, 1.52, -.4), .07, '#c0c4cc')
cil((-.18, 1.2, -.38), .05, .12, '#d83030'); cil((.18, 1.2, -.38), .05, .12, '#3060d8')
fim()
novo('steel_ball')         # bola de aco polida: esfera cinza metalica com brilho e pedestal
bola((0, .6, 0), .5, '#6f7c8a', seg=24); bola((-.2, .85, .3), .17, '#f2f6fa', seg=10)
cil((0, .08, 0), .3, .1, '#4a4a52')
fim()
novo('cybertruck')         # Cybertruck: picape de aco em cunha (corpo baixo, cabine triangular, vidro escuro, rodas grandes)
caixa((0, .55, 0), (2.6, .45, 1.1), '#8f979f'); caixa((-.1, .95, 0), (1.7, .5, 1.0), '#a9b0b8', afina=.5)
for z in (-.43, .43): caixa((-.1, .98, z), (1.1, .26, .05), '#1c2a36', rot=(0, 0, 0))
caixa((-.7, .95, 0), (.04, .3, .8), '#1c2a36'); caixa((.55, .78, 0), (.9, .14, .95), '#8a9098')
for x in (-.85, .85):
    for z in (-.58, .58): cil((x, .3, z), .32, .22, '#15151a', rot=(math.pi / 2, 0, 0)); cil((x, .3, z), .16, .24, '#b8bcc4', rot=(math.pi / 2, 0, 0))
caixa((-1.31, .6, 0), (.05, .08, .9), '#e8f0ff')
fim()
novo('flamethrower')       # "lanca-chamas" de brinquedo: tanque vermelho, cano preto longo com bico, cabo e gatilho
cil((0, .75, 0), .3, 1.0, '#d83a2a', rot=H); bola((-.5, .75, 0), .3, '#d83a2a', seg=14); bola((.5, .75, 0), .3, '#d83a2a', seg=14)
cil((0, 1.1, 0), .05, 1.2, '#2a2a30', rot=H); cil((.95, .75, 0), .07, 1.2, '#2a2a30', rot=H)
cil((1.6, .75, 0), .09, .22, '#f2a020', raio_topo=.05, rot=H)
cil((.55, .35, 0), .05, .4, '#2a2a30'); bola((.3, .6, 0), .09, '#f2d020', seg=10)
fim()
novo('extinguisher')       # extintor de incendio vermelho: corpo, alca, mangueira preta e bocal
cil((0, .75, 0), .24, 1.3, '#d83030'); bola((0, 1.4, 0), .24, '#d83030', seg=14); cil((0, 1.62, 0), .07, .12, '#2a2a30')
tubo([(.0, 1.5, 0), (.3, 1.55, 0), (.34, 1.0, 0)], .03, '#2a2a30'); cil((.34, .9, 0), .06, .14, '#2a2a30')
cil((0, 1.0, 0), .245, .2, '#f2f2f2')
fim()
novo('tv')                 # televisao antiga: caixa de madeira, tela azulada arredondada, botoes, antena em V e pes
caixa((0, .85, 0), (1.5, 1.1, .9), '#6a4a2a'); caixa((-.12, .88, .46), (1.05, .8, .06), '#7fc4e6'); bola((-.12, .88, .47), .5, '#9fd8f2', achata=.06, esc=(1, .75, 1), seg=14)
for i in range(3): cil((.55, .55 + i * .22, .47), .05, .06, '#e8d8a8', rot=(math.pi / 2, 0, 0))
tubo([(0, 1.4, 0), (-.4, 1.95, 0)], .02, '#b8bcc4'); tubo([(0, 1.4, 0), (.4, 1.95, 0)], .02, '#b8bcc4')
for x in (-.55, .55): cil((x, .12, 0), .07, .24, '#3a2a1a')
fim()
novo('prison_mini')        # maquete de prisao num pedestal: muralha quadrada cinza, 4 torres de vigia, portao e predio central
cil((0, .08, 0), 1.1, .16, '#6a4a2a')
for (cx, cz, w, d) in ((0, .8, 1.7, .12), (0, -.8, 1.7, .12), (.8, 0, .12, 1.7), (-.8, 0, .12, 1.7)): caixa((cx, .42, cz), (w, .5, d), '#9a9a96')
for x in (-.8, .8):
    for z in (-.8, .8): cil((x, .72, z), .16, 1.0, '#8a8a86'); cil((x, 1.34, z), .2, .22, '#5a5a56'); cil((x, 1.6, z), .22, .3, '#4a4a52', raio_topo=.02)
caixa((0, .3, .83), (.4, .4, .14), '#3a2a1a')
caixa((0, .5, 0), (1.0, .6, .8), '#b8b4a8'); caixa((0, .9, 0), (1.1, .1, .9), '#6a4a3a')
fim()
novo('bunk')               # beliche de metal de cela: 4 postes, 2 estrados com colchao fino cinza e escadinha
for x in (-.9, .9):
    for z in (-.4, .4): cil((x, 1.0, z), .04, 2.0, '#5a5e66')
for y in (.45, 1.35):
    caixa((0, y, 0), (1.9, .06, .9), '#7a7e86'); caixa((0, y + .08, 0), (1.8, .1, .8), '#9a9a94')
cil((.95, .9, .5), .025, 1.0, '#5a5e66'); 
for i in range(4): cil((.95, .3 + i * .3, .5), .02, .3, '#5a5e66', rot=(math.pi / 2, 0, 0))
fim()
novo('un_wall')            # painel de fundo da Assembleia: parede verde com moldura dourada, faixas douradas e emblema redondo
caixa((0, 1.8, 0), (6.4, 3.6, .2), '#2f6a4a'); caixa((0, 3.55, .12), (6.4, .16, .1), '#d8b040'); caixa((0, .12, .12), (6.4, .24, .1), '#d8b040')
for x in (-3.15, 3.15): caixa((x, 1.8, .12), (.16, 3.6, .1), '#d8b040')
for x in (-2.2, -1.1, 1.1, 2.2): caixa((x, 1.8, .11), (.12, 3.0, .06), '#b89030')
cil((0, 2.0, .15), .85, .08, '#d8b040', rot=(math.pi / 2, 0, 0)); cil((0, 2.0, .2), .65, .08, '#2f6a4a', rot=(math.pi / 2, 0, 0)); bola((0, 2.0, .26), .3, '#d8b040', seg=14)
fim()
novo('un_flags')           # fileira de 7 bandeiras de cores diferentes em mastros
cores = [('#d8282f', '#f2f2f2'), ('#2f4fb8', '#f2f2f2'), ('#2f8a4a', '#f2d040'), ('#f2d040', '#d8282f'), ('#f2f2f2', '#2f4fb8'), ('#d8282f', '#2a2a30'), ('#2f4fb8', '#d8282f')]
for i, (a, b) in enumerate(cores):
    x = -2.7 + i * .9
    cil((x, 1.4, 0), .035, 2.8, '#8a8a90'); bola((x, 2.82, 0), .06, '#d8b040', seg=8)
    pano((x + .03, 2.7, 0), .7, .5, [a, b], onda=.1)
fim()
novo('podium')             # puilpito de madeira escura com tampo inclinado, microfone e emblema dourado
caixa((0, .55, 0), (.9, 1.1, .6), '#5a3a22', afina=.9); caixa((0, 1.12, 0), (1.0, .08, .7), '#6a4a2a', rot=(.2, 0, 0))
cil((0, 1.5, .05), .015, .5, '#2a2a30'); bola((0, 1.78, .1), .05, '#2a2a30', seg=8); cil((0, .65, .31), .14, .03, '#d8b040', rot=(math.pi / 2, 0, 0))
fim()
novo('iceberg_mini')       # maquete de iceberg: bloco de agua azul cortado, ponta de gelo branca fora e base grande submersa em tom claro
caixa((0, .12, 0), (1.9, .24, 1.3), '#2f6fd0'); caixa((0, .5, 0), (1.9, .5, 1.3), '#7ab8e8')
cil((0, .85, 0), .55, .45, '#cfe8f6', raio_topo=.15, lados=7); cil((.5, .78, .1), .3, .3, '#f2f8fc', raio_topo=.1, lados=6)
cil((0, 1.25, 0), .3, .5, '#ffffff', raio_topo=.02, lados=6)
cil((-.35, .35, .1), .5, .3, '#b8dcf2', raio_topo=.7, lados=8)
fim()
novo('titanic')            # transatlantico Titanic: casco preto com faixa branca e vermelha embaixo, superestrutura branca, 4 chamines amarelas com topo preto, mastros
bola((0, .78, 0), 1.0, '#15151a', esc=(3.6, .3, .6))                       # casco preto arredondado (proa e popa)
caixa((0, .62, 0), (6.0, .5, 1.12), '#15151a')                               # corpo central do casco
caixa((0, .39, 0), (6.1, .1, 1.16), '#a8261f')                               # faixa vermelha na linha dagua
caixa((0, .93, 0), (6.1, .08, 1.14), '#f4f1e8')                              # faixa branca do convés
caixa((0, 1.2, 0), (5.2, .5, .95), '#f4f1e8'); caixa((0, 1.5, 0), (4.4, .22, .8), '#ece6d6'); caixa((-.4, 1.72, 0), (2.6, .2, .6), '#f4f1e8')   # decks brancos empilhados
for i in range(14): caixa((-2.4 + i * .36, 1.2, .485), (.12, .12, .02), '#2a3a52'); caixa((-2.4 + i * .36, 1.2, -.485), (.12, .12, .02), '#2a3a52')   # janelinhas
for i, x in enumerate((-1.5, -.5, .5, 1.5)): cil((x, 2.1, 0), .24, .9, '#e8b830', raio_topo=.22, lados=14); cil((x, 2.58, 0), .245, .16, '#15151a', lados=14)   # 4 chamines amarelas, topo preto
cil((2.3, 2.0, 0), .03, 1.6, '#8a6a4a'); cil((-2.6, 1.9, 0), .03, 1.4, '#8a6a4a')   # mastros
caixa((2.6, 1.0, 0), (.7, .3, .6), '#e0d8c4')
fim()
