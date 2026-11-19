# ANIMAIS COM ANATOMIA E ARTICULACAO (19/11, ordem do Gibson: porco, urso, galinha e emu iguais ao animal real; referencia: fotos de perfil em /tmp/claude-0/ref/).
# blender -b --python blender/animais_rig.py [emu chicken bear pig]  -> web/assets/<nome>.glb (frente para +z)
# Aves saem em PECAS com o nome que o motor anima: body, neckp (pescoco, gira para bicar) > head, legL/legR (coxa, anda) > shinL/shinR (canela + pes).
# Urso e porco saem pelo bicho() de animais.py (corpo inteiro arredondado; o motor deita o bicho quando leva tiro e abaixa o focinho quando fuca).
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, bmesh, formas
from mathutils import Vector
from formas import caixa, cil, bola, torno
OUT = os.environ.get('ANIMAIS_OUT') or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'web', 'assets') + os.sep

def _seg(a, b, ra, rb, col, lados=14):   # tronco de cone entre dois pontos (x, y-altura, z-frente)
    A = Vector((a[0], -a[2], a[1])); B = Vector((b[0], -b[2], b[1])); d = B - A
    r = bmesh.ops.create_cone(formas._S['bm'], cap_ends=True, segments=lados, radius1=ra, radius2=rb, depth=d.length)
    q = Vector((0, 0, 1)).rotation_difference(d.normalized()); k = formas._mat(col); mid = (A + B) / 2
    for v in r['verts']: v.co = q @ v.co + mid
    for f in {f for v in r['verts'] for f in v.link_faces}: f.material_index = k
def membro(pts, raios, col):
    for i, (pt, rr) in enumerate(zip(pts, raios)):
        bola(pt, rr, col, seg=14)
        if i: _seg(pts[i - 1], pt, raios[i - 1], rr, col)

def peca(nome, fazer, piv, pai=None):
    """constroi uma peca em coordenadas do mundo (x, y-altura, z-frente) e poe a origem no pivo (onde gira)"""
    formas._S.update(bm=bmesh.new(), mats=[]); fazer()
    me = bpy.data.meshes.new(nome); bm = formas._S['bm']
    for v in bm.verts: v.co -= Vector((piv[0], -piv[2], piv[1]))
    bm.to_mesh(me); bm.free()
    for mt in formas._S['mats']: me.materials.append(mt)
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(nome, me); bpy.context.collection.objects.link(o)
    o.location = Vector((piv[0], -piv[2], piv[1]))
    if pai is not None: o.parent = pai; o.location = o.location - pai.matrix_world.translation if False else Vector((piv[0] - pai['piv'][0], -(piv[2] - pai['piv'][2]), piv[1] - pai['piv'][1]))
    o['piv'] = list(piv); bpy.context.view_layer.update(); return o
def exporta(nome):
    for o in bpy.context.scene.objects: o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=OUT + nome + '.glb', export_format='GLB', export_yup=True, export_apply=True, export_cameras=False, export_lights=False, export_extras=False)
    print('OK', nome, sum(len(o.data.polygons) for o in bpy.context.scene.objects if o.type == 'MESH'))

def ave(nome, P):
    """ave de perfil: P = dicionario de medidas/cores (emu: plumagem caida e pescoco azulado; galinha: corpo gordo, crista, barbela, cauda em leque para cima)"""
    bpy.ops.wm.read_factory_settings(use_empty=True); formas._S.update(name=nome, luz=False)
    yb, zb, Rb = P['corpo']   # centro do corpo e raios (largura, altura, comprimento)
    def corpo():
        bola((0, yb, zb), 1, P['pena'], esc=Rb)
        bola((0, yb + Rb[1] * .25, zb - Rb[2] * .55), 1, P['pena'], esc=(Rb[0] * .8, Rb[1] * .75, Rb[2] * .55))        # garupa
        bola((0, yb - Rb[1] * .2, zb + Rb[2] * .45), 1, P['peito'], esc=(Rb[0] * .78, Rb[1] * .72, Rb[2] * .5))        # peito
        import random; rr = random.Random(4)
        for i in range(P.get('tufos', 0)):   # plumagem desgrenhada caindo pelos lados e pela traseira (emu)
            a = rr.uniform(-1.1, 1.1); zz = zb + rr.uniform(-.9, .6) * Rb[2]; side = rr.choice((-1, 1))
            x = side * Rb[0] * (.55 + .4 * m.cos(a)); y = yb + Rb[1] * (.15 + .45 * m.sin(a)) - .05
            bola((x, y - Rb[1] * .25, zz), Rb[0] * .32, rr.choice(P['penas']), esc=(.55, 1.5, .8), rot=(.25, 0, side * .2))
        if P.get('cauda_leque'):   # galinha: cauda alta em leque
            for k in range(6): bola((0, yb + Rb[1] * (.6 + .12 * k), zb - Rb[2] * (.85 + .04 * k)), Rb[0] * .5, P['cauda'], esc=(.25, 1.3, .8), rot=(-.5 - .12 * k, 0, 0))
        for s in (-1, 1):   # asa dobrada na lateral
            bola((s * Rb[0] * .8, yb + Rb[1] * .08, zb - Rb[2] * .05), 1, P['asa'], esc=(Rb[0] * .3, Rb[1] * .6, Rb[2] * .7), rot=(.15, 0, 0))
    body = peca('body', corpo, (0, yb, zb))
    nx, ny, nz = P['pescoco']; hx, hy, hz = P['cabeca']   # base do pescoco (pivo) e centro da cabeca (relativo ao pivo)
    def pescoco():
        pts = [(0, ny, nz), (0, ny + hy * .35, nz + hz * .1), (0, ny + hy * .7, nz + hz * .45), (0, ny + hy - P['rc'] * .4, nz + hz * .85)]
        rs = [P['rn'] * 1.5, P['rn'] * 1.1, P['rn'], P['rn'] * .9]
        membro(pts[:2], rs[:2], P['pena']); membro(pts[1:], rs[1:], P['pele'])
    neck = peca('neckp', pescoco, (0, ny, nz), body)
    def cabeca():
        c = (0, ny + hy, nz + hz); rc = P['rc']
        bola(c, rc, P['pele'], esc=(.85, .9, 1.15)); bola((0, c[1] + rc * .35, c[2] - rc * .1), rc * .75, P['topo'], esc=(.85, .6, 1.0))
        bola((0, c[1] - rc * .25, c[2] + rc * 1.1), rc * .42, P['bico'], esc=(.75, .45, 1.9))            # bico
        for s in (-1, 1):
            bola((s * rc * .62, c[1] + rc * .2, c[2] + rc * .35), rc * .26, '#ffffff'); bola((s * rc * .72, c[1] + rc * .22, c[2] + rc * .45), rc * .15, P['olho'])
        if P.get('crista'):
            for k in range(4): bola((0, c[1] + rc * (.85 + .1 * (k % 2)), c[2] + rc * (.5 - .32 * k)), rc * .3, P['crista'], esc=(.4, 1.2, .8))
            bola((0, c[1] - rc * .95, c[2] + rc * .6), rc * .3, P['crista'], esc=(.45, 1.4, .8))           # barbela
    peca('head', cabeca, (0, ny + hy * .55, nz + hz * .5), neck)
    for s, L in ((1, 'L'), (-1, 'R')):
        px, py, pz = P['quadril']; kx, ky, kz = P['joelho']
        def coxa(s=s): membro([(s * px, py, pz), (s * (px + .02), py + ky, pz + kz)], [P['rl'] * 2.2, P['rl'] * 1.3], P['coxa'])
        leg = peca('leg' + L, coxa, (s * px, py, pz), body)
        def canela(s=s):
            j = (s * (px + .02), py + ky, pz + kz); t = (s * (px + .02), .07, pz + kz - .02)
            membro([j, t], [P['rl'] * 1.05, P['rl'] * .85], P['perna'])
            for a in (-.5, 0, .5):   # 3 dedos para a frente + 1 para tras (galinha)
                membro([t, (t[0] + m.sin(a) * P['dedo'], .03, t[2] + m.cos(a) * P['dedo'])], [P['rl'] * .7, P['rl'] * .45], P['perna'])
            if P.get('esporao'): membro([t, (t[0], .03, t[2] - P['dedo'] * .6)], [P['rl'] * .6, P['rl'] * .4], P['perna'])
        peca('shin' + L, canela, (s * (px + .02), py + ky, pz + kz), leg)
    exporta(nome)

# medidas na mesma escala dos modelos antigos (o motor multiplica: emu 0,62; galinha ~0,6)
EMU = dict(corpo=(1.55, -.05, (.5, .48, .8)), pescoco=(0, 1.75, .55), cabeca=(0, .78, .38), rn=.085, rc=.13, tufos=60,
           pena='#5e4a36', penas=('#5e4a36', '#4e3c2a', '#6e5842', '#3e3020'), peito='#6a5440', asa='#55422f', pele='#8a9aac', topo='#2e2a28', bico='#2e2a2a', olho='#8a4a1a',
           quadril=(.24, 1.25, -.12), joelho=(.02, -.62, .08), rl=.075, coxa='#6a5440', perna='#7a7062', dedo=.2)
CHICKEN = dict(corpo=(.62, 0, (.3, .3, .42)), pescoco=(0, .78, .3), cabeca=(0, .3, .1), rn=.09, rc=.12, cauda_leque=True, cauda='#6a2a14',
               pena='#b05a2a', penas=(), peito='#c06a32', asa='#9a4a20', pele='#b05a2a', topo='#b05a2a', bico='#f2b84a', olho='#2b2430', crista='#e0403c',
               quadril=(.12, .45, -.04), joelho=(.01, -.2, .02), rl=.035, coxa='#b05a2a', perna='#f2b84a', dedo=.11, esporao=True)

def urso():
    import animais
    def corcova(d):   # urso pardo: corcova de musculo no ombro, focinho longo, orelhas redondas pequenas, garras
        bola((0, d['yc'] + d['bh'] * .42, d['L'] * .22), d['bw'] * .42, d['cor'], esc=(1, .7, 1.2))
        for s in (-1, 1):
            for k in (-1, 0, 1): bola((s * d['bw'] * .3 + k * .05, .03, d['L'] * .3 + .07 * d['L'] + .12), .03, '#e8e0cc', esc=(.6, .5, 1.6))
        bola((0, d['hc'][1] + d['hr'] * .05, d['hc'][2] - d['hr'] * .6), d['hr'] * .95, d['cor'], esc=(1.15, 1, 1))   # bochechas/pescoco grosso
    animais.bicho('bear', 1.7, .62, .8, .8, .2, 1.1, .3, .26, .15, '#6e4628', '#8a5e38', '#3a2416', orelha='redondo', cauda='curto', extra=corcova)
def porco():
    import animais
    def focinho(d):   # porco: disco do focinho chato e rosado com narinas, orelhas triangulares caidas para frente, rabo enrolado, papada
        mc, hr = d['mc'], d['hr']
        bola((0, d['yc'] + d['bh'] * .02, -d['L'] * .02), 1, d['cor'], esc=(d['bw'] * .53, d['bh'] * .52, d['L'] * .56), seg=28)   # barril liso (sem emendas/listras no contorno)
        cil((0, mc[1], mc[2] + .1), hr * .42, .06, '#f08aa0', rot=(m.pi / 2, 0, 0), lados=20)
        for s in (-1, 1): bola((s * hr * .14, mc[1], mc[2] + .135), hr * .08, '#a8485e')
        for s in (-1, 1): bola((s * hr * .6, d['hc'][1] + hr * .75, d['hc'][2] + hr * .25), hr * .38, '#f2a2b4', esc=(.8, .2, 1.1), rot=(.9, 0, -s * .5))
        bola((0, d['hc'][1] - hr * .7, d['hc'][2] - hr * .05), hr * .7, d['cor'], esc=(1, .7, 1))
        tz = -d['L'] * .55; ty = d['yc'] + d['bh'] * .15
        pts = [(0, ty, tz)] + [(.05 * m.cos(a), ty + .05 * m.sin(a) + .02, tz - .04 - .01 * a) for a in [k * .9 for k in range(1, 9)]]
        animais.tubo(pts, .022, d['cor'])
    animais.bicho('pig', 1.15, .32, .62, .58, .08, 1.3, .25, .14, .13, '#f4a6b8', '#f8c0cc', '#c9808f', orelha=None, cauda=None, casco=True, nariz='#f08aa0', extra=focinho, reto=True, perna=.55)

import animais as _an; _an.formas.OUT = OUT
E = dict(emu=lambda: ave('emu', EMU), chicken=lambda: ave('chicken', CHICKEN), bear=urso, pig=porco)
alvo = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else list(E)
for k in alvo: E[k]()
