# Objetos da sessao B (modelados a partir dos prints da pesquisa): smartphone, roadster2008, radarange, uraniborg, microscopio_antigo. blender -b --python blender/objetos_b2.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
P = math.pi / 2
# 1) smartphone: retangulo fino com bordas arredondadas, tela grande com icones, camera e linha de inicio (escala da mao: 0.4 x 0.8 m)
novo('smartphone')
caixa((0, .42, 0), (.40, .82, .05), '#202228')                                  # corpo (moldura escura)
caixa((0, .42, .028), (.355, .76, .012), '#0c0e14')                              # vidro preto
caixa((0, .42, .036), (.335, .70, .006), '#2f6fc9')                              # tela azul
for r in range(5):
    for c in range(3):
        caixa((-.095 + c * .095, .62 - r * .11, .041), (.06, .06, .006), ['#f2b822', '#e8453c', '#4cc16a', '#f4f4f4', '#9b59d6'][(r * 3 + c) % 5])   # icones de apps
caixa((0, .10, .041), (.30, .075, .006), '#e8eef7')                              # dock inferior
cil((0, .76, .036), .012, .01, '#050608', rot=(P, 0, 0)); caixa((0, .795, .036), (.09, .012, .006), '#050608')   # camera frontal e alto-falante
caixa((0, .055, .042), (.12, .008, .006), '#f4f4f4')                             # barra de inicio
cil((.185, .55, 0), .01, .12, '#8a8d94', rot=(P, 0, 0)); cil((-.205, .6, 0), .008, .1, '#8a8d94', rot=(0, 0, 0))   # botoes laterais
cil((-.12, .78, -.034), .035, .01, '#15171c', rot=(P, 0, 0)); cil((-.12, .78, -.04), .022, .01, '#3a4a6a', rot=(P, 0, 0))  # lente traseira
fim(.012)
# 2) roadster2008: esportivo baixo vermelho, 2 lugares, conversivel (base Lotus Elise). Comprimento no eixo x ~3.9 m
novo('roadster2008')
RED, DK, CH = '#c9232b', '#16171b', '#c8ccd2'
bola((0, .52, 0), 1.0, RED, achata=.45, seg=26, esc=(1.55, .6, .98))                     # carroceria baixa e larga
bola((1.25, .46, 0), .7, RED, achata=.5, seg=20, esc=(.95, .45, 1.0))                     # capo comprido na frente
bola((-1.15, .56, 0), .7, RED, achata=.5, seg=20, esc=(.95, .55, 1.0))                    # traseira alta e curta
caixa((-.15, .5, 0), (1.5, .22, 1.2), '#2a2b30')                                            # cockpit aberto
caixa((-.2, .72, 0), (.5, .38, .55), '#202226'); caixa((-.2, .72, .5), (.5, .38, .35), '#202226')   # bancos
caixa((.32, .85, 0), (.05, .32, 1.15), '#7fb4d4', rot=(0, 0, -.45))                         # para-brisa baixo inclinado
cil((.5, .82, .35), .17, .03, DK, rot=(0, 0, -.9)); tubo([(.55, .7, .35), (.9, .55, .35)], .03, DK)   # volante
for sx in (-1.15, 1.15):
    for sz in (-.88, .88):
        cil((sx, .3, sz), .3, .24, '#111114', rot=(P, 0, 0)); cil((sx, .3, sz + (.02 if sz > 0 else -.02)), .2, .26, CH, rot=(P, 0, 0)); cil((sx, .3, sz), .07, .27, DK, rot=(P, 0, 0))   # pneu, aro, miolo
for sz in (-.5, .5): bola((1.75, .5, sz), .13, '#f4f1d8', esc=(1.3, .8, 1.5)); bola((-1.72, .62, sz), .1, '#e8222a', esc=(.6, .7, 1.6))   # farois e lanternas
caixa((1.82, .35, 0), (.1, .14, .9), DK)                                                    # entrada de ar frontal
caixa((-1.0, .82, 0), (.9, .12, 1.0), RED); caixa((-1.65, .72, 0), (.1, .06, .9), DK)       # tampa do motor e aerofolio fino
fim(.03)
# 3) radarange: forno de microondas Raytheon Radarange (1947): armario alto de metal, porta com janela e grade, mostradores no topo
novo('radarange')
ST, WH = '#cfd3d8', '#e9ebee'
caixa((0, .85, 0), (.95, 1.7, .8), ST)                                                      # gabinete do tamanho de uma geladeira
caixa((0, .03, .02), (1.0, .08, .86), '#4a4d52')                                           # rodape
caixa((0, 1.0, .41), (.82, .9, .04), WH)                                                    # porta
caixa((0, 1.1, .445), (.5, .38, .02), '#15181c')                                            # janela escura
for i in range(6): caixa((0, .95 + i * .05, .46), (.46, .012, .01), '#5a5e66')              # grade de ventilacao
caixa((.36, 1.0, .46), (.05, .5, .05), '#2a2c30')                                           # puxador vertical
caixa((0, 1.58, .41), (.82, .2, .04), '#2b2e34')                                            # painel de controle
for x in (-.28, -.09, .1, .29): cil((x, 1.58, .45), .05, .04, '#e8e4d6', rot=(P, 0, 0)); caixa((x, 1.58, .475), (.012, .05, .006), '#222222')   # mostradores
cil((-.34, 1.69, .41), .028, .02, '#e8453c', rot=(P, 0, 0)); bola((.34, 1.69, .41), .03, '#4cc16a')   # lampadas piloto
caixa((0, 1.74, 0), (.9, .06, .75), '#9a9ea6')                                              # tampa superior (ventilacao)
fim(.02)
# 4) uraniborg: castelo-observatorio de Tycho Brahe (1576): predio de tijolo simetrico, cupula central e torres de canto
novo('uraniborg')
BR, RF, DM = '#b5543a', '#5a6f78', '#7d8b91'
caixa((0, .9, 0), (3.6, 1.8, 3.6), BR)                                                      # corpo central de tijolo
caixa((0, 1.85, 0), (3.7, .1, 3.7), '#e4d9bf')                                              # friso de pedra
cil((0, 2.3, 0), 1.35, .9, BR, lados=24)                                                    # tambor central
cil((0, 3.1, 0), 1.45, .8, RF, raio_topo=.15, lados=24)                                     # cupula/telhado central pontudo
for sx in (-2.3, 2.3):                                                                      # torres redondas laterais
    cil((sx, 1.25, 0), .85, 2.5, BR, lados=18); cil((sx, 3.1, 0), .95, 1.2, RF, raio_topo=.05, lados=18)
for sz in (-2.2, 2.2):                                                                      # cupulas dos observatorios (norte e sul)
    cil((0, .85, sz), .7, 1.7, BR, lados=16); bola((0, 1.75, sz), .78, DM, achata=.55, seg=16)
for sx in (-1.7, 1.7):
    for sz in (-1.7, 1.7): cil((sx, 1.9, sz), .3, .5, '#e4d9bf', lados=10); cil((sx, 2.35, sz), .33, .45, RF, raio_topo=.03, lados=10)   # torrinhas de canto
for s in (-1, 1):
    for x in (-1.1, 0, 1.1):
        caixa((x, 1.0, s * 1.81), (.4, .6, .04), '#2c3e50'); caixa((s * 1.81, 1.0, x), (.04, .6, .4), '#2c3e50')   # janelas
caixa((0, .45, 1.82), (.7, .9, .06), '#5a3a22')                                             # portao
caixa((0, -.02, 0), (5.6, .06, 5.6), '#6f9a4a')                                             # gramado do patio
fim(.03)
# 5) microscopio_antigo: latao, tubo inclinado, base em ferradura, espelho embaixo (microscopio composto do inicio do seculo XX)
novo('microscopio_antigo')
BRA, BR2 = '#c9a23a', '#a07c24'
for a in (-.55, .55): cil((a * .35, .04, .12 * (1 if abs(a) < 1 else 0)), .09, .08, '#2b2b30', lados=10)    # pes
caixa((0, .05, 0), (.55, .07, .44), '#25262b', afina=.9)                                  # base em ferradura (corpo)
cil((0, .3, -.12), .045, .5, BRA, lados=14)                                                 # coluna
cil((0, .45, -.22), .05, .75, BR2, lados=12, rot=(.1, 0, 0))                                # braco traseiro
tubo([(0, .78, -.24), (0, .95, -.1), (0, .95, .15)], .05, BR2)                                            # ombro do braco
cil((0, .95, .18), .065, .75, BRA, lados=14, rot=(.5, 0, 0))                               # tubo inclinado
cil((0, 1.3, .36), .05, .16, '#222222', lados=12, rot=(.5, 0, 0)); cil((0, .6, .0), .045, .1, '#d8d8d8', lados=12, rot=(.5, 0, 0))   # ocular e objetiva
cil((0, .68, .04), .06, .05, BR2, lados=14)                                                 # revolver
caixa((0, .44, .05), (.34, .03, .26), '#2b2b30')                                            # platina
caixa((.13, .46, .08), (.02, .03, .1), '#d8d8d8'); caixa((-.13, .46, .08), (.02, .03, .1), '#d8d8d8')   # presilhas
cil((0, .22, .06), .09, .015, '#e8f2f8', rot=(-.4, 0, 0), lados=14); tubo([(0, .2, -.1), (0, .18, .0)], .015, BR2)   # espelho
cil((.1, .55, -.14), .03, .05, BR2, rot=(0, 0, P), lados=10)                                # parafuso de foco
fim(.012)
