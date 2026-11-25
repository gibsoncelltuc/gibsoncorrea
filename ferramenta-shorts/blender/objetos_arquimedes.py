# 25/11 (Gibson: "a pesquisa tinha que trazer o print da banheira da epoca e ir para o Blender modelar"). Modelos feitos A PARTIR das referencias:
#  kit/bathtub     <- banheira grega de TERRACOTA (Museu de Nafplio, sec. II a.C.; banheira do Palacio de Nestor, Pilos): ponta arredondada,
#                     ponta reta com degrau/assento por dentro, barro laranja, faixa pintada com espirais (Pilos), agua azul.
#  kit/coroa_louros <- coroa de LOUROS de ouro (Antikensammlungen Munique, 400 a.C.; coroa de Aigai/Vergina): aro fino de galho, folhas
#                     douradas em duas fileiras, aberta na frente. Nada de coroa de pontas medieval.
# blender -b --python blender/objetos_arquimedes.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
TERRA, TERRA2, FAIXA, AGUA = '#d0784a', '#a85a34', '#6a2416', '#1f8fe8'
novo('bathtub')
L0, L1, R, H = -.45, .75, .36, .5          # trecho reto de L0 a L1, ponta redonda (encosto) centrada em L0, corpo ate a altura H
caixa(((L0 + L1) / 2, H / 2, 0), (L1 - L0, H, 2 * R), TERRA, afina=1.08)     # paredes abrindo para cima (como a de Nafplio)
cil((L0, H / 2, 0), R, H, TERRA, raio_topo=R * 1.08, lados=28)
def contorno(r, y, n=16, so_encosto=False):   # volta da borda: lado, ponta redonda, outro lado, ponta reta
    curva = [(L0 - r * math.sin(math.pi * i / n), y, -r * math.cos(math.pi * i / n)) for i in range(0, n + 1)]
    if so_encosto: return curva
    return [(L1, y, -r)] + curva + [(L1, y, r), (L1, y, -r)]
for y in (.53, .58): tubo(contorno(R * 1.08 - .03, y), .04, TERRA)                         # parede da borda
for k, y in enumerate((.63, .68, .73, .78)): tubo(contorno(R * 1.08 - .03, y, so_encosto=True), .04, TERRA)   # ENCOSTO alto na ponta redonda
tubo([(L1, .62, -R * 1.08 + .03), (L0, .62, -R * 1.08 + .03)], .042, TERRA2); tubo([(L1, .62, R * 1.08 - .03), (L0, .62, R * 1.08 - .03)], .042, TERRA2)   # labio dos lados
tubo(contorno(R * 1.08 - .03, .82, so_encosto=True), .045, TERRA2); tubo([(L1, .62, -R * 1.08 + .03), (L1, .62, R * 1.08 - .03)], .042, TERRA2)
caixa(((L0 + L1) / 2 + .02, .56, 0), (L1 - L0 - .08, .04, 2 * R - .06), AGUA); cil((L0, .56, 0), R - .02, .04, AGUA, lados=24)   # agua azul
caixa((L1 - .16, .6, 0), (.2, .1, 2 * R - .06), TERRA2)                     # degrau/assento na ponta reta
caixa(((L0 + L1) / 2, .3, 0), (L1 - L0, .09, 2 * R * 1.04 + .01), FAIXA); cil((L0, .3, 0), R * 1.04 + .005, .09, FAIXA, lados=28)   # faixa pintada
for i in range(7):
    for zz in (1, -1): bola((L0 + .12 + i * .16, .3, zz * (R * 1.04 + .01)), .028, '#f1e0c0', seg=8)   # espirais/pontos claros (Pilos)
for i in range(1, 7): a_ = math.pi * i / 7; bola((L0 - (R * 1.04 + .01) * math.sin(a_), .3, -(R * 1.04 + .01) * math.cos(a_)), .028, '#f1e0c0', seg=8)
caixa(((L0 + L1) / 2 - .1, .03, 0), (L1 - L0 + .1, .06, 2 * R - .12), TERRA2)   # base baixa
fim(0)
novo('coroa_louros')                       # medida real: aro ~0.2 m de diametro (o motor escala pelo tamanho real)
OURO, OURO2 = '#f6c21c', '#e0a414'
luz(True)   # ouro brilha (sem isto a coroa ficava quase preta na cena de explicacao)
r = .1; n = 30; ab = .3                    # abertura na frente (radianos de cada lado)
ang = [ab + (2 * math.pi - 2 * ab) * i / n for i in range(n + 1)]
tubo([(r * math.sin(a), .0, r * math.cos(a)) for a in ang], .007, OURO2)        # galho do aro
for k, a in enumerate(ang[:-1]):
    for lado in (-1, 0, 1):                # tres fileiras de folhas (fora, cima, dentro), inclinadas para cima, como nas coroas de Munique e Aigai
        rr = r + lado * .02; x, z = rr * math.sin(a), rr * math.cos(a)
        bola((x, .014 + .01 * (lado == 0) + .005 * (k % 2), z), .028, OURO if (k + lado) % 2 else OURO2, rot=(.6 * lado, .3 + .2 * (k % 2), a + math.pi / 2), esc=(1.0, .16, .4), seg=10)
for a in (ab, 2 * math.pi - ab): bola((r * math.sin(a), .0, r * math.cos(a)), .012, OURO2, seg=8)   # pontas do galho
luz(False)
fim(0)
novo('semente')                            # 25/11 Darwin: semente dura que o tentilhao de bico grosso quebra (duas metades rachadas)
bola((-.06, .07, 0), .08, '#8a5a2a', esc=(1.0, .9, 1.25), seg=14); bola((.07, .065, .02), .075, '#a8763a', esc=(1.0, .85, 1.2), rot=(0, .4, .3), seg=14)
bola((.0, .09, 0), .03, '#f1dca8', seg=8); fim(0)
