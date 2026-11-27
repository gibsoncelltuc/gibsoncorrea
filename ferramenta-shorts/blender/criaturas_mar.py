# 26/11 Fundo do mar ORGANICO (pele lisa por esqueleto): substitui os bonecos de bolinhas dos videos longos.
# blender -b --python blender/criaturas_mar.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from criaturas_pele import limpar, corpo, peca, olhos, dentes, exportar

def peixe_fundo(nome, L, costas, barriga, cab=1.0, alt=1.0, boca=1.0, dentes_n=0, dente_t=.1, isca=False, luzes=False, cauda_fina=False, olho_r=.07, olho_cor='#cfcfcf'):
    limpar(); s = L / 4.0
    esp = [(-2.0 * s, 0, 0, (.04 if cauda_fina else .1) * s), (-1.4 * s, 0, 0, .2 * s * alt), (-.6 * s, 0, 0, .42 * s * alt), (.3 * s, .02 * s, 0, .5 * s * alt * cab), (1.0 * s, .04 * s, 0, .55 * s * alt * cab), (1.5 * s, 0, 0, .4 * s * alt * cab), (1.8 * s, -.05 * s, 0, .2 * s * alt)]
    ga = [esp, [(-2.0 * s, 0, 0, .05 * s), (-2.4 * s, .45 * s * alt, 0, .03 * s)], [(-2.0 * s, 0, 0, .05 * s), (-2.35 * s, -.4 * s * alt, 0, .03 * s)]]
    ga.append([(1.5 * s, -.1 * s, 0, .3 * s * alt * cab), (1.75 * s, -.32 * s * boca, 0, .22 * s * alt * boca), (1.25 * s, -.42 * s * boca, 0, .16 * s * alt * boca)])   # mandibula
    for z in (1, -1): ga.append([(.5 * s, -.2 * s * alt, z * .35 * s, .1 * s), (.1 * s, -.45 * s * alt, z * .7 * s, .025 * s)])
    corpo(ga, costas, barriga)
    olhos(1.4 * s, .25 * s * alt * cab, .35 * s * alt * cab, olho_r * s, olho_cor)
    if dentes_n: dentes(1.25 * s, 1.85 * s, -.12 * s, .22 * s * alt * boca, dentes_n, dente_t * s)
    if isca:
        cad = [(1.2 * s, .5 * s * alt * cab, 0, .025 * s), (1.6 * s, 1.0 * s, 0, .02 * s), (2.1 * s, .95 * s, 0, .018 * s)]
        corpo([cad], costas, costas, sub=1); o = peca('bola', (2.15 * s, .9 * s, 0), .09 * s, '#9ff6ff')
        o.active_material.node_tree.nodes['Principled BSDF'].inputs['Emission Color'].default_value = (.6, 1, 1, 1); o.active_material.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = 3
    if luzes:
        for i in range(10):
            o = peca('bola', ((-1.4 + i * .3) * s, -.25 * s * alt, .3 * s * alt), .035 * s, '#9ff6ff'); o.active_material.node_tree.nodes['Principled BSDF'].inputs['Emission Color'].default_value = (.6, 1, 1, 1); o.active_material.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = 3
    exportar(nome)

def cefalopode(nome, L, cor, cor_b, manto=1.0, bracos=8, comp_braco=1.0, orelhas=False, nadadeiras=False, olho_r=.12, olho_cor='#e8e0c0', dumbo=False):
    limpar(); s = L / 4.0
    # manto apontando para tras (-x), cabeca em x=0, bracos para frente (+x) e caindo
    esp = [(-2.0 * s * manto, .1 * s, 0, .15 * s), (-1.4 * s * manto, .05 * s, 0, .45 * s), (-.6 * s * manto, 0, 0, .6 * s), (0, 0, 0, .45 * s), (.35 * s, 0, 0, .3 * s)]
    ga = [esp]
    for k in range(bracos):
        a = k * 2 * math.pi / bracos; cy, cz = math.cos(a), math.sin(a)
        cad = [(.35 * s, 0, 0, .3 * s)]
        for j in range(1, 6):
            tt = j / 5; cad.append(((.35 + tt * 1.6 * comp_braco) * s, (cy * .35 * tt - .25 * tt * tt) * s, cz * .4 * tt * s, max(.03, .12 * (1 - tt * .85)) * s))
        ga.append(cad)
    if orelhas:
        for z in (1, -1): ga.append([(-.9 * s, .4 * s, 0, .4 * s), (-.95 * s, .75 * s, z * .55 * s, .22 * s), (-1.0 * s, .9 * s, z * .95 * s, .12 * s)])
    if nadadeiras:
        for z in (1, -1): ga.append([(-1.6 * s * manto, .08 * s, 0, .3 * s), (-1.7 * s * manto, .1 * s, z * .65 * s, .07 * s)])
    corpo(ga, cor, cor_b)
    olhos(.05 * s, .32 * s, .42 * s, olho_r * s, olho_cor)
    if dumbo:   # as 'orelhas' (nadadeiras) grandes e achatadas, de cada lado do manto
        for z in (1, -1): peca('bola', (-.55 * s, .45 * s, z * .75 * s), .5 * s, cor, esc=(.9, .25, .75))
    exportar(nome)

def isopode(nome, L, cor, cor_b):   # segmentos achatados e largos (armadura), patas e antenas
    limpar(); s = L / 4.0
    esp = [(-1.8 * s, .2 * s, 0, .12 * s), (0, .25 * s, 0, .15 * s), (1.9 * s, .25 * s, 0, .12 * s)]
    ga = [esp]
    for i in range(7):
        x = (-1.0 + i * .3) * s
        for z in (1, -1): ga.append([(x, .2 * s, 0, .15 * s), (x + .1 * s, .02 * s, z * .7 * s, .045 * s), (x + .15 * s, -.12 * s, z * .8 * s, .03 * s)])
    for z in (1, -1): ga.append([(1.9 * s, .25 * s, 0, .12 * s), (2.6 * s, .5 * s, z * .45 * s, .02 * s)])
    corpo(ga, cor, cor_b)
    for i in range(12):
        x = (-1.75 + i * .32) * s; w = .55 * s * (1 - abs(i - 5.5) / 13)
        peca('bola', (x, .3 * s, 0), w, cor if i % 2 else '#b6b0c4', esc=(.38, .42, 1.0))
    peca('bola', (1.95 * s, .28 * s, 0), .3 * s, cor, esc=(.8, .6, 1.1))
    olhos(2.05 * s, .38 * s, .22 * s, .07 * s, '#202020')
    exportar(nome)

def agua_viva(nome, cor):
    limpar(); s = 1.0; ga = [[(0, 1.6, 0, .05), (0, 1.35, 0, .55), (0, 1.05, 0, .7), (0, .85, 0, .55)]]
    for k in range(10):
        a = k * math.pi / 5; ga.append([(0, .85, 0, .55), (math.cos(a) * .45, .7, math.sin(a) * .45, .04), (math.cos(a) * .5, .0, math.sin(a) * .5, .02), (math.cos(a) * .45, -.8, math.sin(a) * .45, .012)])
    corpo(ga, cor, '#f4fbff'); exportar(nome)

# os bichos do v1 e v2
peixe_fundo('peixe_diabo', 2.2, '#1e1c22', '#3a3640', cab=1.6, alt=1.1, boca=1.6, dentes_n=7, dente_t=.18, isca=True, olho_r=.05)
peixe_fundo('peixe_vibora', 3.0, '#1a2836', '#3a5068', cab=.9, alt=.6, boca=1.3, dentes_n=4, dente_t=.32, luzes=True, cauda_fina=True, olho_r=.06)
peixe_fundo('peixe_barril', 2.6, '#5a6870', '#a8b8c0', cab=1.1, alt=.8, olho_r=.12, olho_cor='#5adf6a')
peixe_fundo('peixe_bolha', 2.4, '#e8b4b4', '#f4d4d0', cab=1.5, alt=1.2, boca=.7, olho_r=.06, olho_cor='#2a2a2a', cauda_fina=True)
peixe_fundo('tubarao_duende', 3.6, '#d89a9a', '#f0c8c4', cab=.9, alt=.65, boca=1.1, dentes_n=9, dente_t=.1, olho_r=.05)
peixe_fundo('tubarao_groenlandia', 4.4, '#4a5258', '#8a949a', cab=1.0, alt=.75, olho_r=.06, olho_cor='#aab4a0')
peixe_fundo('peixe_lanterna', 1.6, '#2a3a5a', '#8aa0c0', cab=1.2, alt=.8, luzes=True, olho_r=.14, olho_cor='#dfe8f0')
peixe_fundo('peixe_caracol', 2.0, '#f2d8d0', '#fbeae4', cab=1.3, alt=.9, boca=.6, cauda_fina=True, olho_r=.07, olho_cor='#2a2a2a')
cefalopode('lula_vampira', 2.8, '#5a1420', '#8a2a36', manto=.9, comp_braco=.8, nadadeiras=True, olho_r=.16, olho_cor='#7fd0ff')
cefalopode('lula_gigante', 4.8, '#b8483a', '#e8a090', manto=1.3, comp_braco=1.6, nadadeiras=True, olho_r=.14)
cefalopode('polvo_dumbo', 2.2, '#e8a07a', '#f4c8a8', manto=.6, comp_braco=.7, orelhas=False, olho_r=.1, olho_cor='#2a2a2a', dumbo=True)
isopode('isopode_gigante', 2.0, '#c8c4d4', '#e8e4f0')
agua_viva('agua_viva_imortal', '#d8eef8')
