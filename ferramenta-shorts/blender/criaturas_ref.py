# 26/11 Criaturas REMODELADAS A PARTIR DE FOTOS DE REFERENCIA (referencias/_criaturas/*.jpg, Wikimedia Commons).
# Cada funcao cita o que foi visto na foto. blender -b --python blender/criaturas_ref.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from criaturas_pele import limpar, corpo, peca, olhos, dentes, exportar
import bpy
def aleta(pos, tam, cor, vertical=True, rot=(0, 0, 0)):   # nadadeira fina: bola achatada
    return peca('bola', pos, 1.0, cor, esc=(tam[0], tam[1], .04) if vertical else (tam[0], .04, tam[1]), rot=rot)
def transl(o, alfa=.35):   # material translucido (cupula do peixe-barril)
    m = o.active_material; b = m.node_tree.nodes['Principled BSDF']; b.inputs['Alpha'].default_value = alfa; m.blend_method = 'BLEND'

def dunkleosteus():   # foto: cabeca encouracada branco-acinzentada, placas, laminas osseas na boca, corpo de tubarao, cauda com lobo de cima maior
    limpar(); s = 1.0
    esp = [(-2.1, .05, 0, .06), (-1.6, .02, 0, .2), (-.8, 0, 0, .42), (0, 0, 0, .55), (.8, .02, 0, .62), (1.4, 0, 0, .58), (1.85, -.05, 0, .4)]
    corpo([esp, [(-2.1, .05, 0, .06), (-2.6, .7, 0, .05)], [(-2.1, .05, 0, .06), (-2.45, -.35, 0, .04)], [(-.3, .45, 0, .2), (-.75, 1.0, 0, .04)]] +
          [[(.9, -.35, z * .4, .12), (.4, -.75, z * .9, .04)] for z in (1, -1)], '#5a6268', '#c8ccc4')
    peca('bola', (1.25, .08, 0), .64, '#7a8278', esc=(1.15, .98, .98))                       # elmo osseo (uma peca, mais claro, como no museu)
    peca('bola', (1.55, .3, 0), .4, '#8a9286', esc=(1.0, .55, 1.15))                           # placa do cranio
    peca('bola', (1.25, -.02, 0), .66, '#52584e', esc=(.06, .9, .99))                          # junta entre cabeca e tronco
    for z in (1, -1): peca('cone', (1.9, -.15, z * .16), .09, '#ece4cc', rot=(math.pi, 0, 0), prof=.35); peca('cone', (1.85, -.45, z * .16), .08, '#ece4cc', prof=.3)   # laminas osseas
    olhos(1.5, .25, .48, .09, '#d0c8a0'); exportar('dunkleosteus')

def lula_gigante():   # foto: manto longo e afilado com nadadeiras em losango na ponta, 8 bracos + 2 tentaculos muito longos com clava, olho enorme
    limpar()
    esp = [(-2.6, 0, 0, .08), (-2.2, 0, 0, .32), (-1.2, 0, 0, .52), (-.2, 0, 0, .55), (.3, 0, 0, .45), (.6, 0, 0, .36)]
    ga = [esp]
    for k in range(8):
        a = k * math.pi / 4; ga.append([(.6, 0, 0, .3)] + [(.6 + j * .45, (math.cos(a) * .3 * (j / 5)) - .06 * j * j / 5, math.sin(a) * .3 * (j / 5), max(.025, .11 * (1 - j / 6))) for j in range(1, 6)])
    for z in (1, -1): ga.append([(.6, 0, 0, .3)] + [(.6 + j * .6, -.05 * j, z * (.12 + .04 * j), .03) for j in range(1, 8)] + [(5.1, -.4, z * .45, .09)])   # tentaculos com clava
    corpo(ga, '#a8402e', '#e8b098')
    peca('bola', (-2.3, 0, 0), .55, '#a8402e', esc=(.75, .06, 1.3), rot=(0, 0, 0))   # nadadeira em losango
    olhos(.35, .15, .38, .17, '#dcd2b0'); exportar('lula_gigante')

def tubarao_groenlandia():   # foto: corpo grosso cinza-marrom com pintas, focinho curto e arredondado, nadadeiras pequenas, olho pequeno
    limpar()
    esp = [(-2.3, .05, 0, .08), (-1.7, .02, 0, .3), (-.8, 0, 0, .55), (.2, 0, 0, .65), (1.1, 0, 0, .58), (1.7, -.02, 0, .42), (2.05, -.06, 0, .22)]
    ga = [esp, [(-2.3, .05, 0, .08), (-2.75, .55, 0, .05)], [(-2.3, .05, 0, .08), (-2.6, -.3, 0, .05)], [(-.2, .55, 0, .14), (-.45, .85, 0, .04)], [(-1.2, .4, 0, .1), (-1.4, .62, 0, .03)]]
    ga += [[(1.0, -.4, z * .4, .14), (.6, -.75, z * .8, .04)] for z in (1, -1)]
    corpo(ga, '#4e4a44', '#8c8880', mancha='#2e2a26'); olhos(1.65, .12, .36, .05, '#9ab0a0'); exportar('tubarao_groenlandia')

def peixe_vibora():   # foto: corpo MUITO longo e fino, cabeca grande, presas enormes para fora, raio dorsal longo, fotoforos na barriga
    limpar()
    esp = [(-2.5, 0, 0, .03), (-2.0, 0, 0, .1), (-.8, 0, 0, .2), (.6, 0, 0, .24), (1.3, .02, 0, .34), (1.75, .02, 0, .32), (2.05, 0, 0, .2)]
    ga = [esp, [(-2.5, 0, 0, .03), (-2.8, .25, 0, .02)], [(-2.5, 0, 0, .03), (-2.8, -.25, 0, .02)], [(1.6, -.12, 0, .2), (2.05, -.25, 0, .12), (1.6, -.36, 0, .08)]]
    ga.append([(.9, .22, 0, .05), (.4, 1.2, 0, .015), (-.3, 1.5, 0, .012)])   # raio dorsal longo
    corpo(ga, '#1e2a3a', '#4a5a72')
    for z in (1, -1):
        for x, h, y0 in ((2.0, .7, -.05), (1.82, .55, -.1), (1.95, .5, .15)): peca('cone', (x, y0, z * .14), .05, '#f4f8ff', prof=h, rot=(.2 * z if y0 < 0 else math.pi - .2 * z, 0, 0))   # presas enormes
    for i in range(14):
        o = peca('bola', (-1.9 + i * .26, -.17, .14), .025, '#9ff6ff'); b = o.active_material.node_tree.nodes['Principled BSDF']; b.inputs['Emission Color'].default_value = (.6, 1, 1, 1); b.inputs['Emission Strength'].default_value = 3
    olhos(1.7, .14, .26, .08, '#dfe8f0'); exportar('peixe_vibora')

def peixe_barril():   # foto: cabeca com CUPULA TRANSPARENTE, olhos tubulares verdes dentro, corpo marrom, nadadeiras grandes
    limpar()
    esp = [(-1.8, 0, 0, .06), (-1.3, 0, 0, .3), (-.3, 0, 0, .48), (.6, .02, 0, .45), (1.1, -.05, 0, .32), (1.35, -.12, 0, .14)]
    ga = [esp, [(-1.8, 0, 0, .06), (-2.2, .4, 0, .03)], [(-1.8, 0, 0, .06), (-2.2, -.4, 0, .03)]]
    corpo(ga, '#6a4a30', '#b89868')
    for x in (-.5, .2): aleta((x, .5, 0), (.35, .45), '#c8a880'); aleta((x, -.45, 0), (.3, .35), '#c8a880')
    for z in (1, -1): aleta((.6, -.15, z * .45), (.35, .25), '#c8a880', vertical=False)
    transl(peca('bola', (.85, .38, 0), .42, '#cfe8f0', esc=(1.1, .8, .8)), .3)   # cupula
    for z in (1, -1): peca('bola', (.85, .38, z * .12), .1, '#3adf6a', esc=(1, 1.6, 1))   # olhos tubulares verdes
    exportar('peixe_barril')

def tubarao_duende():   # foto: rosa acinzentado, focinho LONGO e achatado como lamina, mandibula saltada com dentes de prego, cauda longa
    limpar()
    esp = [(-2.6, .1, 0, .05), (-1.8, .04, 0, .22), (-.6, 0, 0, .42), (.6, 0, 0, .45), (1.3, -.02, 0, .32), (1.7, 0, 0, .14), (2.6, .05, 0, .06)]
    ga = [esp, [(-2.6, .1, 0, .05), (-2.95, .3, 0, .03)], [(-.1, .4, 0, .14), (-.4, .75, 0, .04)], [(1.35, -.3, 0, .18), (1.75, -.55, 0, .12), (1.3, -.62, 0, .08)]]
    ga += [[(.9, -.3, z * .35, .12), (.5, -.65, z * .75, .04)] for z in (1, -1)]
    corpo(ga, '#c49090', '#e8c4c0'); dentes(1.4, 1.72, -.42, .1, 7, .09, baixo=False); dentes(1.4, 1.72, -.22, .12, 7, .08); olhos(1.45, .12, .3, .05, '#e8e8e8'); exportar('tubarao_duende')

def lula_vampira():   # foto: vermelho-escuro, CAPA de membrana ligando os 8 bracos, olhos grandes azuis, duas 'orelhas' no manto
    limpar()
    esp = [(-1.3, 0, 0, .12), (-.9, 0, 0, .42), (-.3, 0, 0, .52), (.15, 0, 0, .42)]
    ga = [esp]
    for k in range(8):
        a = k * math.pi / 4; ga.append([(.15, 0, 0, .35), (.6, math.cos(a) * .45, math.sin(a) * .45, .1), (1.0, math.cos(a) * .7, math.sin(a) * .7, .06), (1.15, math.cos(a) * .6, math.sin(a) * .6, .03)])
    corpo(ga, '#4a0e18', '#7a2632')
    o = peca('cone', (.75, 0, 0), .72, '#3a0a12', rot=(0, -math.pi / 2, 0), prof=.9)   # capa: cone aberto de membrana, ponta no corpo
    o.active_material.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = .8; o.active_material.blend_method = 'BLEND'
    for z in (1, -1): aleta((-.85, .2, z * .5), (.3, .22), '#5a1420', vertical=False)   # orelhas
    olhos(.05, .25, .38, .14, '#5ab8ff'); exportar('lula_vampira')

def isopode_gigante():   # foto: oval achatado, ~12 placas largas sobrepostas cor lilas-claro, antenas longas, patas por baixo
    limpar()
    corpo([[(-1.7, .2, 0, .12), (0, .25, 0, .14), (1.8, .22, 0, .12)]] + [[((-1.0 + i * .3), .18, 0, .13), ((-.9 + i * .3), .02, z * .75, .04), ((-.85 + i * .3), -.12, z * .9, .025)] for i in range(7) for z in (1, -1)], '#b8b0c8', '#d8d0e4')
    for i in range(12):
        x = -1.7 + i * .3; w = .95 * (1 - abs(i - 5.5) / 11); peca('bola', (x, .32, 0), 1.0, '#cfc6dc' if i % 2 else '#bdb3cc', esc=(.2, .22, w))
    peca('bola', (1.9, .28, 0), 1.0, '#c4bad4', esc=(.3, .2, .55))
    for z in (1, -1): corpo([[(1.95, .3, z * .2, .03), (2.6, .5, z * .5, .015), (3.0, .3, z * .75, .01)]], '#a89cc0', '#a89cc0', sub=1)
    olhos(1.95, .38, .38, .07, '#202020'); exportar('isopode_gigante')

def polvo_dumbo():   # foto: forma de SINO, bracos ligados por membrana (saia), 'orelhas' em cima, cor branco-rosado/laranja
    limpar()
    esp = [(0, 1.2, 0, .25), (0, .85, 0, .6), (0, .4, 0, .66), (0, -.05, 0, .62)]
    ga = [esp]
    for k in range(8):
        a = k * math.pi / 4; ga.append([(0, 0, 0, .35), (math.cos(a) * .55, -.3, math.sin(a) * .55, .1), (math.cos(a) * .85, -.5, math.sin(a) * .85, .05)])
    corpo(ga, '#e89a78', '#f4c8b0')
    peca('bola', (0, -.12, 0), .9, '#f0a888', esc=(1.0, .2, 1.0))   # saia de membrana entre os bracos (disco achatado ligado ao corpo)
    for z in (1, -1): peca('bola', (0, .9, z * .62), 1.0, '#e89a78', esc=(.3, .08, .35), rot=(.5 * z, 0, 0))   # orelhas inclinadas
    olhos(.42, .55, .3, .1, '#1a1a1a'); exportar('polvo_dumbo')

def peixe_bolha():   # foto (no fundo do mar): corpo de peixe gelatinoso rosado, cabeca grande e larga, afina para a cauda
    limpar()
    esp = [(-1.6, 0, 0, .06), (-1.1, 0, 0, .2), (-.3, 0, 0, .45), (.5, .05, 0, .7), (1.05, 0, 0, .55)]
    corpo([esp, [(-1.6, 0, 0, .06), (-1.95, .25, 0, .03)], [(-1.6, 0, 0, .06), (-1.95, -.25, 0, .03)]] + [[(.3, -.3, z * .5, .14), (0, -.6, z * .95, .04)] for z in (1, -1)], '#d8a0a0', '#f0cccc')
    olhos(.85, .3, .5, .06, '#202020'); exportar('peixe_bolha')

def anomalocaris():   # foto: corpo segmentado com abas laterais, 2 apendices frontais espinhosos curvados para baixo, olhos em pedunculo, cauda em leque
    limpar()
    corpo([[(-1.4, 0, 0, .08), (-.4, 0, 0, .22), (.6, 0, 0, .26), (1.2, 0, 0, .2)]] + [[(1.2, 0, z * .1, .08), (1.6, -.05, z * .15, .06), (1.85, -.3, z * .12, .045), (1.7, -.55, z * .08, .03)] for z in (1, -1)] +
          [[(1.05, .12, z * .1, .05), (1.1, .3, z * .35, .04)] for z in (1, -1)], '#9a4a30', '#d88a62')
    for i in range(11):
        x = 1.0 - i * .22; w = .7 * (1 - abs(i - 3) / 12)
        for z in (1, -1): peca('bola', (x, 0, z * (w * .7)), 1.0, '#b85a3c' if i % 2 else '#c86a48', esc=(.14, .03, w * .6))
    for k in range(3): peca('bola', (-1.5, .0, (k - 1) * .25), 1.0, '#c86a48', esc=(.3, .03, .1), rot=(0, (k - 1) * .5, 0))
    for z in (1, -1): peca('bola', (1.1, .33, z * .36), .09, '#1a1a1a')
    exportar('anomalocaris')

def arthropleura():   # foto: corpo largo e achatado com placas laterais pontudas, ~30 segmentos, muitas patas, cabeca pequena com antenas
    limpar()
    corpo([[(-1.4, .12, 0, .1), (0, .14, 0, .12), (1.4, .14, 0, .1)]] + [[((-1.3 + i * .2), .1, 0, .1), ((-1.3 + i * .2), .02, z * .42, .025), ((-1.28 + i * .2), -.08, z * .5, .018)] for i in range(14) for z in (1, -1)], '#6a3a22', '#9a5a38')
    for i in range(28):
        x = -1.35 + i * .1; peca('bola', (x, .2, 0), 1.0, '#7a4428' if i % 2 else '#8a5030', esc=(.06, .08, .42))
        for z in (1, -1): peca('cone', (x, .18, z * .45), .04, '#6a3a22', prof=.12, rot=(math.pi / 2 * z, 0, 0))
    corpo([[(1.45, .15, z * .05, .02), (1.75, .3, z * .2, .012)] for z in (1, -1)], '#4a2816', '#4a2816', sub=1)
    peca('bola', (1.45, .15, 0), .12, '#5a3018', esc=(1.2, .7, 1.4)); exportar('arthropleura')

for f in [dunkleosteus, lula_gigante, tubarao_groenlandia, peixe_vibora, peixe_barril, tubarao_duende, lula_vampira, isopode_gigante, polvo_dumbo, peixe_bolha, anomalocaris, arthropleura]:
    f()
