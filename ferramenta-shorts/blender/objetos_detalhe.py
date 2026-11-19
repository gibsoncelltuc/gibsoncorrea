# OBJETOS COM DETALHE DE REFERENCIA REAL (19/11, ordem do Gibson: "todo objeto sem referencia: pesquisar na internet e modelar igual").
# Referencia baixada em /tmp/claude-0/ref/<nome>.png (pesquisa de imagem + print). blender -b --python blender/objetos_detalhe.py [nome ...]
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
import formas
H = m.pi / 2

def bitcoin():
    # moeda fisica de bitcoin (referencia: fotos de moeda dourada): borda serrilhada, anel com "texto", trilhas de circuito, B com dois tracos em relevo nas duas faces
    novo('bitcoin')
    R = .58; G, G2, G3 = '#e8b83a', '#c99628', '#f6d470'
    cil((0, .6, 0), R, .1, G2, lados=48, rot=(H, 0, 0))                                   # corpo
    for i in range(72): a = i / 72 * 2 * m.pi; caixa((R * m.cos(a), .6 + R * m.sin(a), 0), (.022, .03, .1), G3, rot=(0, 0, a))   # serrilha da borda
    for s in (-1, 1):
        z = s * .05
        torno((0, .6, z), [(R * .96, 0), (R * .96, .012 * s), (R * .84, .012 * s), (R * .84, 0)], G3, lados=48, tampa=False) if False else None
        cil((0, .6, z), R * .95, .012, G, lados=48, rot=(H, 0, 0)); cil((0, .6, z + s * .007), R * .82, .012, G2, lados=48, rot=(H, 0, 0))   # aro e campo rebaixado
        for i in range(40):                                                                  # "letras" em volta (tracinhos do texto)
            a = i / 40 * 2 * m.pi
            if i % 10 != 9: caixa((R * .885 * m.cos(a), .6 + R * .885 * m.sin(a), z + s * .012), (.012, .035, .008), G3, rot=(0, 0, a))
        for (x0, y0, x1, y1) in ((-.38, .2, -.2, .2), (-.2, .2, -.2, .32), (.2, -.25, .38, -.25), (.2, -.25, .2, -.36), (-.4, -.1, -.24, -.1), (.24, .12, .4, .12), (.3, .12, .3, .3), (-.3, -.1, -.3, -.3)):   # trilhas de circuito
            cx_, cy_ = (x0 + x1) / 2, (y0 + y1) / 2; L_ = max(abs(x1 - x0), abs(y1 - y0)) + .02
            caixa((cx_, .6 + cy_, z + s * .014), ((L_, .016, .006) if abs(x1 - x0) > abs(y1 - y0) else (.016, L_, .006)), G3)
            cil((x1, .6 + y1, z + s * .014), .022, .008, G3, lados=10, rot=(H, 0, 0))
        zz = z + s * .02; t = .016                                                           # o B (simbolo do bitcoin), inclinado como no logo
        q = .21
        caixa((-.06, .6, zz), (.075, .5, t), '#fff1b8', rot=(0, 0, -.24))                   # haste
        for yb, w in ((.12, .2), (-.12, .23)):                                                # duas barrigas do B
            bola((.05 + (.02 if yb < 0 else 0), .6 + yb, zz), .125 if yb > 0 else .14, '#fff1b8', esc=(1.05, .78, .12))
            bola((.05 + (.02 if yb < 0 else 0), .6 + yb, zz + s * .004), .06 if yb > 0 else .07, G2, esc=(1.2, .7, .12))
        for xb in (-.06, .04):                                                                # tracinhos em cima e embaixo
            caixa((xb + .07, .6 + .3, zz), (.04, .1, t), '#fff1b8', rot=(0, 0, -.24)); caixa((xb - .06, .6 - .3, zz), (.04, .1, t), '#fff1b8', rot=(0, 0, -.24))
    fim(.004)

def roadster():
    # Tesla Roadster vermelho (referencia: fotos de perfil/frente): esportivo baixo em cunha, conversivel, para-lamas arredondados, farois puxados para tras,
    # capo curto e liso, santantonio atras dos bancos, rodas grandes de liga. Mesmo tamanho e direcao do antigo (2,2 m ao longo de x, frente em -x).
    novo('roadster'); R, R2 = '#d21f2a', '#a8141e'
    bola((0, .45, 0), 1, R, esc=(1.12, .2, .47))                                   # corpo baixo e liso
    bola((-.62, .47, 0), 1, R, esc=(.52, .14, .44), rot=(0, 0, .1))               # capo descendo para o bico
    bola((.62, .52, 0), 1, R, esc=(.5, .2, .46))                                    # traseira alta
    for x in (-.7, .7):
        for z in (-.36, .36): bola((x, .5, z), .3, R, esc=(1.25, .75, .45))         # para-lamas
    bola((.1, .6, 0), 1, '#1b1b1f', esc=(.42, .08, .36))                            # cockpit aberto
    for z in (-.18, .18): bola((.18, .66, z), .14, '#2a2a30', esc=(.6, 1.3, .9))    # bancos
    caixa((.38, .74, 0), (.06, .22, .7), '#1b1b1f')                                 # santantonio
    caixa((-.22, .7, 0), (.04, .2, .82), '#9fd4ee', rot=(0, 0, .75))               # para-brisa inclinado
    caixa((-.22, .7, 0), (.06, .22, .86), '#1b1b1f', rot=(0, 0, .75)) if False else None
    for z in (-.3, .3): bola((-1.0, .5, z), .1, '#f2f0e0', esc=(1.6, .5, 1))         # farois puxados
    for z in (-.32, .32): bola((1.08, .55, z), .08, '#c8202a', esc=(.5, .6, 1.4))    # lanternas
    caixa((-1.1, .38, 0), (.05, .08, .5), '#1b1b1f')                                # grade baixa
    for x in (-.7, .7):
        for z in (-.47, .47):
            cil((x, .26, z), .26, .16, '#15151a', rot=(m.pi / 2, 0, 0), lados=24); cil((x, .26, z), .17, .18, '#c8ccd2', rot=(m.pi / 2, 0, 0), lados=20)
            for k in range(5): a = k / 5 * 2 * m.pi; caixa((x + .09 * m.cos(a), .26 + .09 * m.sin(a), z), (.15, .03, .19), '#8a8e96', rot=(0, 0, a))
    fim(.02)

def ball():
    # bola de futebol classica (Telstar): esfera branca com 12 pentagonos pretos lisos nos vertices de um icosaedro (sem espetos)
    import bmesh as _b
    from mathutils import Vector as V
    novo('ball'); r = .42; bola((0, r, 0), r, '#f4f1e8', seg=32)
    p = (1 + 5 ** .5) / 2; vs = [(0, 1, p), (0, -1, p), (0, 1, -p), (0, -1, -p), (1, p, 0), (-1, p, 0), (1, -p, 0), (-1, -p, 0), (p, 0, 1), (-p, 0, 1), (p, 0, -1), (-p, 0, -1)]
    bm = formas._S['bm']; k = formas._mat('#22252c')
    for v in vs:
        d = V(v).normalized(); t1 = d.orthogonal().normalized(); t2 = d.cross(t1); rr = r * .36
        def pt(f_, a_, h_):   # ponto na superficie (curvo), a f_ do raio do pentagono
            q = (d + (t1 * m.cos(a_) + t2 * m.sin(a_)) * (f_ * .36)).normalized() * (r * h_); return bm.verts.new((q.x, -q.z, q.y + r))
        cen = pt(0, 0, 1.03); mid = [pt(.5, i / 5 * 2 * m.pi, 1.03) for i in range(5)]; out = [pt(1, i / 5 * 2 * m.pi, 1.025) for i in range(5)]
        for i in range(5):
            j = (i + 1) % 5
            for fc in ((cen, mid[i], mid[j]), (mid[i], out[i], out[j], mid[j])): f = bm.faces.new(fc); f.material_index = k
    fim(0)

def fireplace():
    # lareira de casa do seculo XIX (referencia: lareiras de pedra/tijolo com consolo de madeira): moldura de pedra, boca escura em arco,
    # toras com fogo, consolo (prateleira) com castical e relogio, grelha na frente. Tamanho de boneco (~1,6 m de largura).
    novo('fireplace'); P, P2 = '#b8ab98', '#9a8e7c'
    caixa((0, .75, -.1), (1.7, 1.5, .5), P); caixa((0, 1.55, 0), (1.95, .12, .62), '#6a4426')
    caixa((0, .03, .25), (1.9, .06, .5), P2)                                            # soleira
    caixa((0, .45, .13), (.9, .8, .1), '#1e1814'); bola((0, .85, .13), .45, '#1e1814', esc=(1, .5, .2))   # boca em arco
    for i in range(8): a = i / 7 * m.pi; caixa((.56 * m.cos(a), .85 + .5 * m.sin(a) * .9, .17), (.14, .12, .06), P2, rot=(0, 0, a - m.pi / 2))   # pedras do arco
    for z, r_ in ((.22, .2), (.28, -.2)): cil((r_ * .2, .1, z), .07, .6, '#6a4426', rot=(0, 0, m.pi / 2 + r_))   # toras
    luz(True)   # fogo brilha na sala escura
    torno((0, .12, .24), [(.02, 0), (.17, .08), (.19, .24), (.1, .44), (.02, .6)], '#f08a2a', 12); torno((.04, .14, .3), [(.02, 0), (.1, .07), (.11, .19), (.04, .38), (.01, .47)], '#f2c230', 10)
    luz(False)
    cil((-.6, 1.72, 0), .05, .22, '#e8e2d0'); bola((-.6, 1.86, 0), .03, '#f2c230')      # vela
    caixa((.5, 1.74, 0), (.26, .3, .14), '#5a3a22'); cil((.5, 1.76, .075), .09, .02, '#f2efe6', rot=(m.pi / 2, 0, 0))   # relogio
    for x in (-.35, -.12, .12, .35): cil((x, .25, .4), .015, .4, '#2a2a2e')        # grelha
    caixa((0, .44, .4), (.8, .03, .03), '#2a2a2e')
    fim(.02)

E = dict(bitcoin=bitcoin, roadster=roadster, ball=ball, fireplace=fireplace)
alvo = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else list(E)
for k in alvo: E[k]()
