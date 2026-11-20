# VEGETACAO DA REGIAO (19/11, ordem do Gibson: "arvores, flores e chao da epoca e do lugar"). blender -b --python blender/vegetacao.py [nome ...]
# Mesmo tamanho das arvores da biblioteca (arvore ~6 m, arbusto ~2,5 m, canteiro ~3 m). O mkvideo troca nature/tree_oak, nature/bush e nature/flowerbed por estas conforme a regiao.
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
TR = '#6a4a30'

def copa(c, r, cores, n=7, achata=.8, seed=1):
    import random; rr = random.Random(seed)
    bola(c, r, cores[0], esc=(1, achata, 1))
    for i in range(n):
        a = i / n * 2 * m.pi + rr.random() * .4
        bola((c[0] + r * .7 * m.cos(a), c[1] + r * (rr.random() - .3) * .5, c[2] + r * .7 * m.sin(a)), r * (.45 + rr.random() * .2), cores[i % len(cores)], esc=(1, achata, 1))

def oliveira():
    novo('veg_oliveira'); tubo([(0, 0, 0), (.3, 1.2, .1), (-.2, 2.2, 0), (.1, 3.0, 0)], .32, '#7a6a58')
    tubo([(-.2, 2.2, 0), (-1.2, 3.0, .2)], .18, '#7a6a58'); tubo([(.3, 1.2, .1), (1.3, 2.6, -.1)], .16, '#7a6a58')
    copa((0, 3.6, 0), 1.9, ['#8a9a6a', '#7a8a5a', '#9aaa7a'], 9, .55, 3); fim(.02)
def cipreste():
    novo('veg_cipreste'); cil((0, .5, 0), .2, 1, TR)
    bola((0, 3.6, 0), 1.1, '#3a5a32', esc=(1, 3.2, 1)); bola((.1, 4.6, .1), .8, '#2f4f2a', esc=(1, 2.4, 1)); fim(.02)
def cerejeira():
    novo('veg_cerejeira'); tubo([(0, 0, 0), (.2, 1.5, 0), (-.3, 2.6, .1)], .3, '#5a3a2a'); tubo([(.2, 1.5, 0), (1.4, 2.8, 0)], .18, '#5a3a2a'); tubo([(-.3, 2.6, .1), (-1.4, 3.2, 0)], .15, '#5a3a2a')
    copa((0, 3.6, 0), 2.1, ['#f6b8cc', '#f2a2bc', '#fbd0dc'], 10, .6, 5)
    for i in range(10): bola((-2 + i * .45, .05, 1.2 * m.sin(i)), .14, '#f6b8cc', esc=(1, .2, 1))
    fim(.02)
def bambu():
    novo('veg_bambu')
    for i in range(9):
        x, z = .5 * m.cos(i * 2.3) * (i % 3), .5 * m.sin(i * 2.3) * (i % 3); h = 4.5 + (i % 4) * .6
        cil((x, h / 2, z), .09, h, '#7aa04a', lados=8)
        for k in range(1, 6): cil((x, k * h / 6, z), .11, .06, '#5a8032', lados=8)
        for k in range(3): bola((x + .4 * m.cos(k * 2 + i), h - k * .5, z + .4 * m.sin(k * 2 + i)), .45, '#6a9a3a', esc=(1.6, .3, .6), rot=(0, k + i, 0))
    fim(.02)
def acacia():
    novo('veg_acacia'); tubo([(0, 0, 0), (.3, 2.0, 0), (1.2, 3.6, 0)], .26, TR); tubo([(.3, 2.0, 0), (-1.0, 3.5, .2)], .2, TR)
    bola((0, 4.0, 0), 3.0, '#7a8a3a', esc=(1, .22, 1)); bola((.6, 4.2, .3), 2.2, '#8a9a4a', esc=(1, .2, 1)); fim(.02)
def baoba():
    novo('veg_baoba'); torno((0, 0, 0), [(1.6, 0), (1.4, 1.5), (1.15, 3.5), (1.1, 4.6)], '#9a8270', lados=20)
    for i in range(7): a = i / 7 * 2 * m.pi; tubo([(0, 4.5, 0), (1.6 * m.cos(a), 5.4, 1.6 * m.sin(a)), (2.2 * m.cos(a), 5.6 + .3 * (i % 2), 2.2 * m.sin(a))], .18, '#9a8270'); bola((2.2 * m.cos(a), 5.8, 2.2 * m.sin(a)), .55, '#6a8a3a', esc=(1, .5, 1))
    fim(.02)
def bananeira():
    novo('veg_bananeira'); cil((0, 1.4, 0), .22, 2.8, '#8aa05a', raio_topo=.16, lados=10)
    for i in range(7):
        a = i / 7 * 2 * m.pi; bola((1.3 * m.cos(a), 3.0 - .2 * (i % 2), 1.3 * m.sin(a)), 1.3, '#5aa03a', esc=(1.4, .12, .45), rot=(0, -a, .5))
    bola((.3, 2.5, .2), .3, '#e8c44a', esc=(.6, 1.2, .6)); fim(.02)
def cacto():
    novo('veg_cacto'); cil((0, 1.4, 0), .38, 2.8, '#4a8a4a', lados=12); bola((0, 2.8, 0), .38, '#4a8a4a')
    tubo([(.38, 1.2, 0), (.9, 1.3, 0), (.9, 2.1, 0)], .24, '#4a8a4a'); tubo([(-.38, 1.6, 0), (-.8, 1.7, 0), (-.8, 2.3, 0)], .22, '#4a8a4a')
    bola((0, 3.15, 0), .14, '#f08aa0'); fim(.02)
def lavanda():
    novo('veg_lavanda')
    for i in range(3):
        for j in range(5):
            x, z = -1.2 + j * .6, -.5 + i * .5; bola((x, .25, z), .3, '#6a8a5a', esc=(1, .7, 1))
            for k in range(5): cil((x + .12 * m.cos(k * 1.3), .55, z + .12 * m.sin(k * 1.3)), .04, .35, '#8a6ac8', lados=5)
    fim(.02)
def hibisco():
    novo('veg_hibisco'); copa((0, 1.0, 0), 1.0, ['#3f8a3a', '#4a9a44'], 6, .8, 7)
    for i in range(22):
        yy = 1 - 2 * (i + .5) / 22; r = (1 - yy * yy) ** .5; a = i * 2.4
        if yy > -.4: bola((1.02 * r * m.cos(a), 1.0 + .8 * yy, 1.02 * r * m.sin(a)), .26, ['#e8283a', '#f06a2a', '#f2c42a'][i % 3], esc=(1, .55, 1)); bola((1.08 * r * m.cos(a), 1.0 + .82 * yy, 1.08 * r * m.sin(a)), .07, '#fff2a8')
    fim(.02)
def girassol():
    novo('veg_girassol')
    for i in range(5):
        x = -1.2 + i * .6; h = 1.6 + (i % 2) * .4
        cil((x, h / 2, 0), .05, h, '#4a8a3a', lados=6); bola((x + .25, h * .5, 0), .2, '#4a8a3a', esc=(1.5, .3, .8))
        cil((x, h, .08), .32, .08, '#f2c42a', lados=14, rot=(m.pi / 2, 0, 0)); cil((x, h, .12), .16, .06, '#5a3a1a', lados=12, rot=(m.pi / 2, 0, 0))
    fim(.02)

E = dict(oliveira=oliveira, cipreste=cipreste, cerejeira=cerejeira, bambu=bambu, acacia=acacia, baoba=baoba, bananeira=bananeira, cacto=cacto, lavanda=lavanda, hibisco=hibisco, girassol=girassol)
alvo = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else list(E)
for k in alvo: E[k]()
