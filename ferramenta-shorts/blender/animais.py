# ANIMAIS COM ANATOMIA (ordem do Gibson 19/11: "estrutura fisiologica melhor, igual ao animal real").
# blender -b --python blender/animais.py [especie ...]  -> web/assets/<especie>.glb (de frente para +z, 1 unidade = 1 m)
# Peito fundo e cintura fina, pescoco, cabeca com focinho, olhos, orelhas da especie, pernas com cotovelo/joelho e jarrete
# (pata traseira dobrada para tras), patas/cascos, cauda da especie. Estilo arredondado do canal (sem caixote).
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import formas, bmesh
from formas import *
formas.OUT = os.environ.get('ANIMAIS_OUT') or (os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'web', 'assets') + os.sep)

def _seg(a, b, ra, rb, col, lados=16):   # tronco de cone liso ligando dois pontos (x, y-altura, z-frente)
    from mathutils import Vector
    A = Vector((a[0], -a[2], a[1])); B = Vector((b[0], -b[2], b[1])); d = B - A
    r = bmesh.ops.create_cone(formas._S['bm'], cap_ends=True, segments=lados, radius1=ra, radius2=rb, depth=d.length)
    q = Vector((0, 0, 1)).rotation_difference(d.normalized()); k = formas._mat(col); mid = (A + B) / 2
    for v in r['verts']: v.co = q @ v.co + mid
    for f in {f for v in r['verts'] for f in v.link_faces}: f.material_index = k
def membro(pts, raios, col):   # perna/tromba: cones lisos + bola em cada articulacao (sem aneis)
    for i, (pt, rr) in enumerate(zip(pts, raios)):
        bola(pt, rr, col, seg=16)
        if i: _seg(pts[i - 1], pt, raios[i - 1], rr, col)

def tubo(pts, r, col, passo=1):   # versao lisa (substitui a de formas): afina ate 70% na ponta
    membro(pts, [r * (1 - .3 * i / max(1, len(pts) - 1)) for i in range(len(pts))], col)

def bicho(nome, L, H, bw, bh, nl, na, hr, ml, mr, cor, barriga, pata, orelha='tri', cauda='fino', olho='#2b2430', extra=None, casco=False, nariz='#2b2430', reto=False):
    """L corpo (m), H altura da perna, bw/bh largura/altura do tronco, nl/na pescoco (comprimento, angulo p/ frente rad), hr raio da cabeca, ml/mr focinho"""
    novo(nome)
    yc = H + bh * .45
    bola((0, yc, L * .22), 1, cor, esc=(bw * .55, bh * .55, L * .3))            # peito (fundo)
    bola((0, yc + bh * .03, -L * .25), 1, cor, esc=(bw * .5, bh * .48, L * .28))  # quadril/garupa
    bola((0, yc - bh * .02, 0), 1, cor, esc=(bw * .46, bh * .42, L * .36))      # meio (cintura mais fina)
    bola((0, yc - bh * .28, L * .18), 1, barriga, esc=(bw * .38, bh * .22, L * .22))   # peito/barriga clara
    # pescoco e cabeca
    nb = (0, yc + bh * .2, L * .4); nc = (0, nb[1] + m.cos(na) * nl / 2, nb[2] + m.sin(na) * nl / 2)
    cil(nc, bw * .26, nl, cor, raio_topo=bw * .2, rot=(na, 0, 0), lados=16)
    hc = (0, nb[1] + m.cos(na) * nl + hr * .2, nb[2] + m.sin(na) * nl + hr * .3)
    bola(hc, hr, cor, esc=(1, .95, 1.05))
    mc = (0, hc[1] - hr * .3, hc[2] + hr * .55 + ml / 2)
    bola(mc, mr, barriga if nome not in ('wolf', 'fox', 'lion') else barriga, esc=(1, .85, ml / mr / 1.4 + .4))
    bola((0, mc[1] + mr * .35, mc[2] + ml / 2 + mr * .1), mr * .38, nariz)               # nariz
    for s in (-1, 1):
        bola((s * hr * .5, hc[1] + hr * .25, hc[2] + hr * .72), hr * .22, '#ffffff')
        bola((s * hr * .52, hc[1] + hr * .27, hc[2] + hr * .86), hr * .12, olho)
        ox, oy, oz = s * hr * .55, hc[1] + hr * .75, hc[2] - hr * .1
        if orelha == 'tri': cil((ox, oy + hr * .25, oz), hr * .32, hr * .7, cor, raio_topo=.02, rot=(0, 0, -s * .25), lados=3)
        elif orelha == 'caido': bola((s * hr * .85, hc[1] + hr * .1, hc[2] - hr * .05), hr * .3, pata, esc=(.45, 1.5, .9), rot=(0, 0, s * .3))
        elif orelha == 'longo': bola((s * hr * .3, oy + hr * .9, oz - hr * .2), hr * .3, cor, esc=(.5, 2.6, .8), rot=(-.2, 0, -s * .12))
        elif orelha == 'lateral': bola((s * hr * 1.0, hc[1] + hr * .45, hc[2] - hr * .1), hr * .28, cor, esc=(1.6, .6, .7), rot=(0, 0, -s * .3))
        elif orelha == 'redondo': bola((s * hr * .7, oy, oz), hr * .3, cor, esc=(1, 1, .5))
    # pernas continuas (cadeia de bolas com raio afinando): ombro-cotovelo-pulso-pata / quadril-joelho-jarrete-pata
    r0 = bw * .21
    for s in (-1, 1):
        x = s * bw * .3; zf = L * .3; zr = -L * .3
        if reto: membro([(x, yc - bh * .1, zf), (x, H * .5, zf), (x, .06, zf)], [r0 * 1.2, r0 * 1.0, r0 * 1.05], cor)
        else: membro([(x, yc - bh * .1, zf), (x, H * .62, zf - .03 * L), (x, H * .14, zf + .01 * L), (x, .06, zf + .05 * L)], [r0 * 1.25, r0 * .85, r0 * .62, r0 * .7], cor)
        if reto: membro([(x, yc, zr), (x, H * .5, zr), (x, .06, zr)], [r0 * 1.3, r0 * 1.0, r0 * 1.05], cor)   # elefante: perna-coluna
        else: membro([(x, yc, zr), (x, H * .7, zr + .1 * L), (x, H * .32, zr - .1 * L), (x, .06, zr - .05 * L)], [r0 * 1.6, r0 * 1.0, r0 * .6, r0 * .7], cor)
        for zz in (zf + .07 * L, zr + .0 * L):
            if reto: cil((x, .05, zz if zz > 0 else zr), r0 * 1.15, .1, pata, raio_topo=r0 * 1.05, lados=16)
            elif casco: cil((x, .06, zz), r0 * .75, .12, pata, raio_topo=r0 * .6, lados=12)
            else: bola((x, .06, zz + .03), r0 * .85, pata, esc=(1, .55, 1.4))
    # cauda
    tz = -L * .52; ty = yc + bh * .2
    if cauda == 'fino': tubo([(0, ty, tz), (0, ty + .1, tz - .25), (0, ty + .25, tz - .45)], bw * .06, cor)
    elif cauda == 'grosso': tubo([(0, ty, tz), (0, ty - .05, tz - .25), (0, ty - .2, tz - .5)], bw * .11, cor); bola((0, ty - .25, tz - .55), bw * .12, barriga)
    elif cauda == 'raposa': tubo([(0, ty, tz), (0, ty - .1, tz - .3), (0, ty - .15, tz - .6)], bw * .16, cor); bola((0, ty - .16, tz - .68), bw * .16, '#f6f1e8')
    elif cauda == 'tufo': tubo([(0, ty, tz), (0, ty - .3, tz - .15), (0, ty - .7, tz - .2)], bw * .05, cor); bola((0, ty - .78, tz - .2), bw * .12, pata, esc=(1, 1.6, 1))
    elif cauda == 'curto': bola((0, ty + .02, tz - .05), bw * .14, barriga)
    elif cauda == 'pompom': bola((0, ty, tz - .02), bw * .25, '#ffffff')
    elif cauda == 'gato': tubo([(0, ty, tz), (0, ty + .25, tz - .2), (0, ty + .55, tz - .25), (0, ty + .7, tz - .1)], bw * .07, cor)
    if extra: extra(dict(L=L, H=H, bw=bw, bh=bh, yc=yc, hc=hc, hr=hr, mc=mc, cor=cor, pata=pata, barriga=barriga))
    fim(.01)

def juba(d):
    for i in range(14):
        a = i / 14 * 2 * m.pi
        bola((d['hr'] * 1.05 * m.cos(a), d['hc'][1] + d['hr'] * 1.0 * m.sin(a) - .05, d['hc'][2] - d['hr'] * .35), d['hr'] * .42, '#8a4f1c')
def chifres_cabra(d):
    for s in (-1, 1): tubo([(s * d['hr'] * .3, d['hc'][1] + d['hr'] * .8, d['hc'][2]), (s * d['hr'] * .45, d['hc'][1] + d['hr'] * 1.3, d['hc'][2] - d['hr'] * .4), (s * d['hr'] * .55, d['hc'][1] + d['hr'] * 1.2, d['hc'][2] - d['hr'] * .9)], .04, '#cfc4ac', passo=.3)
    bola((0, d['mc'][1] - d['hr'] * .35, d['mc'][2] - .02), d['hr'] * .2, '#e8e0cc', esc=(.6, 1.4, .6))
def chifres_vaca(d):
    for s in (-1, 1): tubo([(s * d['hr'] * .5, d['hc'][1] + d['hr'] * .75, d['hc'][2] - .05), (s * d['hr'] * 1.0, d['hc'][1] + d['hr'] * .95, d['hc'][2]), (s * d['hr'] * 1.15, d['hc'][1] + d['hr'] * 1.3, d['hc'][2] + .05)], .05, '#efe6d0', passo=.3)
    for (x, y, z, r) in ((.18, .1, .1, .22), (-.2, .05, -.35, .26), (.05, .18, -.15, .18)): bola((x * d['bw'] * 2, d['yc'] + y, z * d['L']), r, '#2b2430', esc=(.25, .9, 1.1), rot=(0, 0, 0)) if False else None
    for (x, z, r) in ((1, .15, .2), (-1, -.25, .24), (1, -.3, .18)): bola((x * d['bw'] * .47, d['yc'] + .05, z * d['L']), r, '#2b2430', esc=(.25, 1, 1.2))
def galhada(d):
    for s in (-1, 1):
        b = (s * d['hr'] * .35, d['hc'][1] + d['hr'] * .8, d['hc'][2] - d['hr'] * .2)
        tubo([b, (s * d['hr'] * .7, b[1] + .45, b[2] - .1), (s * d['hr'] * .9, b[1] + .9, b[2] - .25)], .035, '#8a6a4a', passo=.3)
        tubo([(s * d['hr'] * .7, b[1] + .45, b[2] - .1), (s * d['hr'] * .55, b[1] + .75, b[2] + .15)], .03, '#8a6a4a', passo=.3)
        tubo([(s * d['hr'] * .85, b[1] + .75, b[2] - .2), (s * d['hr'] * 1.15, b[1] + 1.0, b[2] - .05)], .03, '#8a6a4a', passo=.3)
def la(d):
    for i in range(22):
        a = i * 2.4; z = (i / 22 - .5) * d['L'] * .9
        bola((m.cos(a) * d['bw'] * .32, d['yc'] + m.sin(a) * d['bh'] * .3 + .05, z), d['bh'] * .28, '#f6f2ea')
def tromba(d):
    hc, hr = d['hc'], d['hr']
    tubo([(0, hc[1] - hr * .2, hc[2] + hr * .8), (0, hc[1] - hr * .9, hc[2] + hr * 1.2), (0, hc[1] - hr * 1.7, hc[2] + hr * 1.25), (0, hc[1] - hr * 2.1, hc[2] + hr * 1.5)], hr * .2, d['cor'], passo=.3)
    for s in (-1, 1):
        bola((s * hr * 1.05, hc[1], hc[2] - hr * .1), hr * .8, d['cor'], esc=(.18, 1.1, .9), rot=(0, s * .3, 0))
        tubo([(s * hr * .4, hc[1] - hr * .5, hc[2] + hr * .7), (s * hr * .5, hc[1] - hr * .9, hc[2] + hr * 1.3)], hr * .1, '#f4efe2', passo=.3)
def bigode(d):
    for s in (-1, 1):
        for k in (-1, 0, 1): tubo([(s * d['mr'] * .6 if 'mr' in d else s * .05, d['mc'][1] + k * .015, d['mc'][2] + .05), (s * .22, d['mc'][1] + k * .04, d['mc'][2] + .02)], .006, '#2b2430', passo=.3)

E = {
 'dog':      lambda: bicho('dog', .95, .5, .38, .42, .3, .7, .2, .16, .1, '#d49a5c', '#f4e2c4', '#5a3a24', orelha='caido', cauda='fino'),
 'wolf':     lambda: bicho('wolf', 1.15, .62, .4, .44, .34, .8, .22, .22, .1, '#8a8f98', '#e2e5ea', '#3a3d45', orelha='tri', cauda='grosso'),
 'fox':      lambda: bicho('fox', .8, .38, .3, .3, .24, .8, .17, .17, .07, '#e0782a', '#fbeede', '#2b2430', orelha='tri', cauda='raposa'),
 'cat':      lambda: bicho('cat', .62, .3, .26, .26, .16, .6, .16, .07, .08, '#ec9a44', '#fbe3c0', '#fbe3c0', orelha='tri', cauda='gato', olho='#3a8a4a', nariz='#f08aa0', extra=bigode),
 'lion':     lambda: bicho('lion', 1.5, .75, .55, .6, .35, .75, .3, .22, .16, '#d9a24a', '#f2d49a', '#8a5a2a', orelha='redondo', cauda='tufo', extra=juba),
 'cow':      lambda: bicho('cow', 1.9, .85, .8, .85, .35, 1.2, .32, .26, .22, '#fbf7f0', '#f4b6c0', '#3a3238', orelha='lateral', cauda='tufo', casco=True, nariz='#e8909e', extra=chifres_vaca),
 'deer':     lambda: bicho('deer', 1.3, .95, .45, .5, .55, .45, .22, .22, .1, '#b07a48', '#efe0c8', '#2b2430', orelha='lateral', cauda='curto', casco=True, extra=galhada),
 'donkey':   lambda: bicho('donkey', 1.4, .85, .5, .6, .5, .55, .26, .3, .15, '#9a958f', '#e1dad0', '#3a3330', orelha='longo', cauda='tufo', casco=True),
 'goat':     lambda: bicho('goat', 1.0, .62, .4, .45, .3, .55, .2, .2, .1, '#efe3cf', '#f7efe0', '#4a3a30', orelha='lateral', cauda='curto', casco=True, extra=chifres_cabra),
 'sheep':    lambda: bicho('sheep', 1.05, .5, .55, .55, .22, .8, .2, .16, .11, '#f6f2ea', '#f6f2ea', '#2b2430', orelha='lateral', cauda='curto', casco=True, nariz='#3d343b', extra=la),
 'rabbit':   lambda: bicho('rabbit', .45, .14, .28, .3, .08, .4, .15, .06, .07, '#e8e2da', '#ffffff', '#d4ccc0', orelha='longo', cauda='pompom', nariz='#f08aa0'),
 'elephant': lambda: bicho('elephant', 2.6, 1.4, 1.5, 1.6, .2, .9, .7, .1, .3, '#9aa0a8', '#b6bbc2', '#70757c', orelha=None, cauda='fino', casco=True, nariz='#70757c', extra=tromba, reto=True),
}
alvo = [a for a in sys.argv[sys.argv.index('--') + 1:]] if '--' in sys.argv else list(E)
for k in alvo: E[k]()
