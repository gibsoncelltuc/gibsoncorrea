# OBJETOS COM DETALHE DE REFERENCIA REAL (19/11, ordem do Gibson: "todo objeto sem referencia: pesquisar na internet e modelar igual").
# Referencia baixada em /tmp/claude-0/ref/<nome>.png (pesquisa de imagem + print). blender -b --python blender/objetos_detalhe.py [nome ...]
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
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

E = dict(bitcoin=bitcoin)
alvo = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else list(E)
for k in alvo: E[k]()
