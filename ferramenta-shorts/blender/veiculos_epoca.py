# VEICULOS DA EPOCA (19/11, ordem do Gibson; referencias: fotos de tanques WWI/WWII, biplanos, navios a vapor). blender -b --python blender/veiculos_epoca.py [nome ...]
# Mesma escala dos veiculos da biblioteca (tanque ~7 m, aviao ~6 m de asa, navio ~19 m). Frente para +z. O mkvideo troca o veiculo generico pelo da epoca da historia.
import sys, os, math as m; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
H = m.pi / 2
import formas
def escala(F):   # avioes: mesma envergadura do aviao da biblioteca (~6,5 m)
    for v in formas._S['bm'].verts: v.co *= F
def perfil(c, pts, esp, col, rot=(0, 0, 0)):   # silhueta 2D com espessura, girada (prisma com rot)
    bm = formas._S['bm']; fr = [bm.verts.new((x, -esp / 2, y)) for x, y in pts]; bk = [bm.verts.new((x, esp / 2, y)) for x, y in pts]; n = len(pts)
    bm.faces.new(fr); bm.faces.new(list(reversed(bk)))
    for i in range(n): bm.faces.new((fr[i], bk[i], bk[(i + 1) % n], fr[(i + 1) % n]))
    formas._put(fr + bk, col, c, rot)
def casco(L, W, D, col, proa=.28, popa=.08, y0=0.0, quilha=.35):   # casco de navio de verdade: proa pontuda, popa arredondada, fundo estreito (secoes ao longo de z)
    bm = formas._S['bm']; k = formas._mat(col); N = 16; secs = []
    for i in range(N + 1):
        t = i / N; z = -L / 2 + L * t
        if t > 1 - proa: w = W / 2 * (1 - ((t - (1 - proa)) / proa) ** 1.6) + .02
        elif t < popa: w = W / 2 * (.75 + .25 * (t / popa))
        else: w = W / 2
        sh = (1 + .25 * max(0, t - (1 - proa)) / proa)   # proa sobe um pouco
        pts = [(-w, y0 + D * sh), (-w * .92, y0 + D * .45), (-w * .55, y0 + .05), (0, y0 - quilha * (1 if t < 1 - proa / 2 else .4)), (w * .55, y0 + .05), (w * .92, y0 + D * .45), (w, y0 + D * sh)]
        secs.append([bm.verts.new((x, -z, y)) for x, y in pts])
    for a, b in zip(secs, secs[1:]):
        for j in range(len(a) - 1): f = bm.faces.new((a[j], a[j + 1], b[j + 1], b[j])); f.material_index = k
    for s_, rev in ((secs[0], True), (secs[-1], False)):
        f = bm.faces.new(list(reversed(s_)) if rev else s_); f.material_index = k
    top = bm.faces.new([s_[-1] for s_ in secs] + [s_[0] for s_ in reversed(secs)]); top.material_index = k

def rodas_esteira(L, x, r, n, cor='#2a2a2e'):
    for i in range(n): cil((x, r, -L / 2 + r + i * (L - 2 * r) / max(1, n - 1)), r, .35, cor, lados=14, rot=(0, 0, H))
def tanque_ww1():
    novo('tanque_ww1')   # Mark I/IV britanico (1916-18): LOSANGO alto com a esteira dando a volta no casco, canhoes nos sponsons laterais, sem torre, rodas-guia atras
    Q = [(-3.7, .9), (-3.2, 2.5), (2.2, 2.5), (3.9, 1.0), (3.2, 0.0), (-2.6, 0.0)]          # silhueta lateral (z, y): frente alta e inclinada
    for s in (-1, 1):
        perfil((s * 1.45, 0, 0), [(z, y) for z, y in Q], .7, '#3a3a30', rot=(0, -H, 0))                                   # esteira (anel externo)
        perfil((s * 1.82, 0, 0), [(z * .86, .35 + (y - .0) * .78) for z, y in Q], .06, '#6e6c4c', rot=(0, -H, 0))         # chapa lateral por dentro da esteira
        for i in range(9): z = -2.8 + i * .75; caixa((s * 1.45, .04 if abs(z) < 2.6 else .3, z), (.74, .1, .3), '#2a2a24')   # sapatas
        for i in range(7): bola((s * 1.86, 1.95, -2.6 + i * .85), .07, '#4a4a3a')                                          # rebites
        caixa((s * 2.05, 1.35, .3), (.6, 1.1, 1.8), '#7a7a58', afina=.8); cil((s * 2.5, 1.45, .7), .09, 1.6, '#3a3a3a', rot=(H, 0, 0))   # sponson + canhao
    caixa((0, 1.45, -.2), (2.2, 1.9, 5.0), '#76744f'); caixa((0, 2.6, .9), (1.2, .55, 1.2), '#6a6a4a')                     # casco e cabine do motorista
    for s in (-1, 1): caixa((s * .3, 2.6, 1.52), (.35, .14, .04), '#1a1a1a')
    for s in (-1, 1): cil((s * .6, .55, -4.3), .45, .2, '#4a3a2a', rot=(0, 0, H)); tubo([(s * .6, .9, -2.6), (s * .6, .6, -4.3)], .06, '#3a3a3a')   # rodas-guia de cauda
    fim(.03)
def tanque_ww2():
    novo('tanque_ww2')   # tanque WWII: casco baixo, torre redonda, canhao, esteiras com rodas
    for s in (-1, 1): caixa((s * 1.5, .7, 0), (.8, 1.0, 6.6), '#3a3a30'); rodas_esteira(5.6, s * 1.93, .4, 6, '#4a5230'); [cil((s * 2.0, .4, -2.4 + i * .96), .14, .38, '#2a2a2e', lados=10, rot=(0, 0, H)) for i in range(6)]
    caixa((0, 1.35, 0), (2.6, .9, 6.0), '#5a6338', afina=.92); caixa((0, 1.85, -1.8), (2.4, .4, 2.4), '#566034')
    torno((0, 1.8, .3), [(1.15, 0), (1.1, .55), (.8, .85), (0, .9)], '#5f6a3c', lados=20)
    cil((0, 2.25, 2.8), .13, 3.6, '#4a5230', rot=(H, 0, 0)); cil((0, 2.25, 4.6), .18, .3, '#4a5230', rot=(H, 0, 0))
    cil((.4, 2.75, .1), .32, .2, '#4a5230'); bola((-.5, 2.75, -.3), .12, '#3a3a2a')
    fim(.04)
def tanque_moderno():
    novo('tanque_moderno')   # tanque moderno: casco largo e baixo, torre angulosa, canhao longo, saias laterais
    for s in (-1, 1): caixa((s * 1.6, .55, 0), (.75, .8, 7.0), '#2a2a2e'); rodas_esteira(6.4, s * 1.6, .38, 7); caixa((s * 1.75, .95, 0), (.12, .55, 6.8), '#7a7a5a')
    caixa((0, 1.15, 0), (3.2, .7, 6.8), '#7a7a5a', afina=.9)
    caixa((0, 1.75, -.4), (2.6, .7, 3.2), '#86865f', afina=.75); caixa((0, 1.75, 1.6), (1.6, .5, 1.0), '#86865f', afina=.6)
    cil((0, 1.85, 4.2), .12, 5.0, '#5a5a44', rot=(H, 0, 0)); caixa((.7, 2.25, -.8), (.5, .3, .6), '#5a5a44')
    fim(.04)
def biplano():
    novo('biplano')   # biplano (ate ~1935): duas asas com montantes, helice de madeira, cockpit aberto, rodas fixas
    cil((0, 1.6, 0), .55, 5.4, '#c8302a', raio_topo=.25, rot=(H, 0, 0), lados=16); bola((0, 1.6, 2.7), .5, '#2a2a2e')
    for y in (1.15, 2.55): caixa((0, y, .6), (8.4, .12, 1.4), '#e8dcc0')
    for x in (-3.2, -1.2, 1.2, 3.2): cil((x, 1.85, .6), .05, 1.4, '#6a4a2a')
    caixa((0, 1.6, -2.7), (2.6, .1, .9), '#e8dcc0'); caixa((0, 2.2, -2.8), (.1, 1.1, .9), '#c8302a')
    for k in (0, 1): caixa((0, 1.6, 2.95), (.18, 1.9, .08), '#6a4a2a', rot=(0, 0, k * H))
    for s in (-1, 1): tubo([(s * .4, 1.2, 1.2), (s * .7, .35, 1.4)], .05, '#3a3a3a'); cil((s * .75, .35, 1.4), .32, .16, '#2a2a2e', rot=(0, 0, H))
    torno((0, 2.1, .2), [(.42, 0), (.4, .25)], '#3a2a1a', lados=14, tampa=False)
    escala(.72)
    fim(.03)
def aviao_ww2():
    novo('aviao_ww2')   # caca da 2a Guerra: asa baixa, fuselagem lisa, cabine de vidro, helice, trem de pouso
    cil((0, 1.4, 0), .6, 6.0, '#6a7a5a', raio_topo=.2, rot=(H, 0, 0), lados=18); bola((0, 1.4, 3.0), .55, '#4a4a4a', esc=(1, 1, .8))
    caixa((0, 1.1, .6), (9.0, .2, 1.8), '#6a7a5a', afina=.7); caixa((0, 1.5, -2.8), (3.0, .15, 1.0), '#6a7a5a'); caixa((0, 2.1, -2.9), (.15, 1.2, 1.1), '#6a7a5a')
    bola((0, 1.95, .4), .45, '#a8d0e8', esc=(1, .7, 1.8))
    for k in (0, 1, 2): caixa((0, 1.4, 3.3), (.16, 2.2, .08), '#2a2a2e', rot=(0, 0, k * m.pi / 3))
    for s in (-1, 1): bola((s * 2.6, .95, .8), .3, '#d8d8d8'); tubo([(s * 1.4, 1.0, 1.0), (s * 1.5, .3, 1.2)], .07, '#3a3a3a'); cil((s * 1.5, .3, 1.2), .3, .18, '#2a2a2e', rot=(0, 0, H))
    escala(.72)
    fim(.03)
def jato():
    novo('jato')   # aviao a jato (1950+): asa em flecha, nariz pontudo, cauda alta, turbinas
    cil((0, 1.5, 0), .55, 8.0, '#d8dce2', raio_topo=.35, rot=(H, 0, 0), lados=18); cil((0, 1.5, 4.6), .55, 1.4, '#d8dce2', raio_topo=.05, rot=(H, 0, 0), lados=18)
    for s in (-1, 1):
        prisma((0, 1.3, 0), [(s * .4, 1.5), (s * 4.6, -1.0), (s * 4.6, -1.8), (s * .4, -1.0)], .18, '#c8ccd2') if False else caixa((s * 2.4, 1.3, -.2), (4.4, .18, 1.6), '#c8ccd2', rot=(0, s * .45, 0))
        cil((s * 2.0, .95, .3), .35, 1.8, '#9aa0a8', rot=(H, 0, 0))
    caixa((0, 2.6, -3.4), (.15, 2.0, 1.4), '#2a5aa8', rot=(-.3, 0, 0)); caixa((0, 1.6, -3.6), (3.0, .14, 1.0), '#c8ccd2')
    for i in range(8): bola((.56, 1.75, 2.6 - i * .6), .1, '#2a3a5a')
    escala(.72)
    fim(.03)
def navio_vapor():
    novo('navio_vapor')   # navio a vapor (1860-1950): casco preto com proa pontuda, faixa vermelha na linha d'agua, conves de madeira, superestrutura branca, 2 chamines com faixa, mastros e botes
    casco(18.0, 4.6, 3.2, '#22232a', y0=.3); casco(17.6, 4.5, .55, '#a82a2a', y0=.0, quilha=.3)
    caixa((0, 3.6, -.3), (4.0, .12, 15.0), '#b89a6a')
    caixa((0, 4.5, -1.0), (3.4, 1.7, 7.0), '#f2efe6'); caixa((0, 5.75, .4), (2.8, .8, 3.0), '#f2efe6'); caixa((0, 6.25, 1.5), (3.4, .2, 1.0), '#f2efe6')
    for i in range(9): bola((1.72, 4.6, -4.0 + i * .75), .13, '#2a3a5a'); bola((-1.72, 4.6, -4.0 + i * .75), .13, '#2a3a5a')
    for z in (-2.0, 1.0): cil((0, 7.6, z), .6, 4.4, '#2a2a2e', raio_topo=.56, lados=16, rot=(-.12, 0, 0)); cil((0, 8.6, z - .1), .62, .6, '#c8302a', lados=16, rot=(-.12, 0, 0))
    for z in (-6.8, 5.8): cil((0, 7.5, z), .12, 8.0, '#6a4a2a'); cil((0, 9.0, z), .06, 2.6, '#6a4a2a', rot=(0, 0, H))
    for s in (-1, 1): bola((s * 1.9, 5.5, -3.5), .5, '#f2efe6', esc=(.6, .5, 2.6))
    fim(.03)
def navio_moderno():
    novo('navio_moderno')   # navio de guerra moderno: casco cinza com proa afilada, superestrutura angulosa (stealth), mastro de radar, canhao na proa, heliponto na popa, numero no casco
    casco(19.0, 4.4, 3.4, '#7a8088', y0=.2, proa=.34); casco(18.6, 4.3, .4, '#3a3e44', y0=-.05, quilha=.25)
    caixa((0, 3.65, -.4), (4.0, .1, 15.6), '#5e646c')
    caixa((0, 5.1, -.8), (3.4, 2.8, 5.4), '#8a9098', afina=.78); caixa((0, 7.1, -.4), (2.2, 1.4, 2.8), '#8a9098', afina=.65); caixa((0, 6.6, 1.95), (2.4, .7, .05), '#2a3a4a')
    torno((0, 7.8, -.4), [(.5, 0), (.25, 2.4), (.08, 3.0)], '#6a7078', lados=4); caixa((0, 10.5, -.4), (1.8, .5, .15), '#4a4e54'); bola((0, 9.3, -.4), .35, '#e8e8ec')
    torno((0, 3.7, 5.6), [(.95, 0), (.9, .4), (.5, .8), (0, .82)], '#7a8088', lados=16); cil((0, 4.15, 7.2), .1, 2.6, '#5a5a5a', rot=(H, 0, 0))
    caixa((0, 3.72, -6.4), (3.6, .06, 4.4), '#4e525a'); cil((0, 3.77, -6.4), 1.2, .02, '#f2f2f2', lados=24); cil((0, 3.78, -6.4), 1.0, .02, '#4e525a', lados=24)
    for s in (-1, 1): caixa((s * 2.08, 2.6, 6.0), (.04, .8, 1.2), '#f2f2f2')
    fim(.03)
def caminhao_antigo():
    novo('caminhao_antigo')   # caminhao militar antigo (ate ~1945): capo comprido, para-lamas redondos, carroceria de madeira com lona
    caixa((0, 1.4, 2.0), (1.6, 1.0, 1.8), '#5a6338'); caixa((0, 1.9, .7), (2.0, 1.4, 1.4), '#5a6338'); caixa((0, 2.2, 1.45), (1.8, .7, .05), '#a8d0e8')
    caixa((0, 1.3, -1.8), (2.3, .8, 4.0), '#7a5a3a'); caixa((0, 2.2, -1.8), (2.3, 1.6, 4.0), '#7a7a52', afina=.92)
    for z in (-3.0, -1.2, 2.2):
        for s in (-1, 1): cil((s * 1.05, .5, z), .5, .35, '#2a2a2e', lados=16, rot=(0, 0, H)); bola((s * 1.05, .9, z), .55, '#4a5230', esc=(.5, .5, 1.1)) if z == 2.2 else None
    for s in (-1, 1): bola((s * .55, 1.5, 2.95), .15, '#f4f0c8')
    fim(.04)

E = dict(tanque_ww1=tanque_ww1, tanque_ww2=tanque_ww2, tanque_moderno=tanque_moderno, biplano=biplano, aviao_ww2=aviao_ww2, jato=jato, navio_vapor=navio_vapor, navio_moderno=navio_moderno, caminhao_antigo=caminhao_antigo)
alvo = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else list(E)
for k in alvo: E[k]()
