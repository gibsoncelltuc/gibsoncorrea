# Objetos novos da SESSAO A (24/11): fragata britanica classe Leander (anos 60-70) e barco pequeno da guarda costeira islandesa. blender -b --python blender/objetos_sessao_a2.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *

def casco(L, alt, larg, cor, cor_fundo, y0=0.0, bojo=1.0):
    bola((0, y0 + alt * 0.55, 0), 1.0, cor_fundo, esc=(L / 2, alt * 0.62, larg / 2 * bojo), seg=20)
    for i in range(9):
        t = (i - 4) / 4.0; w = larg * (1 - 0.55 * abs(t) ** 2.2); x = t * L * 0.44
        caixa((x, y0 + alt * 0.86, 0), (L * 0.12, alt * 0.5, w), cor)

# ---------------- FRAGATA LEANDER (Royal Navy, 1963-1990): casco cinza, canhao duplo de proa, mastro com radar grande, chamine, hangar de helicoptero ----------------
novo('navio_leander')
casco(5.0, 0.85, 0.8, '#8d959d', '#3b4249')
caixa((0, 1.0, 0), (4.5, 0.06, 0.7), '#a2aab2')                                         # convés
caixa((0.15, 1.35, 0), (1.9, 0.6, 0.58), '#8d959d', afina=0.85); caixa((0.35, 1.8, 0), (0.9, 0.34, 0.46), '#a2aab2', afina=0.85)   # superestrutura e ponte
for z in (-0.16, 0, 0.16): caixa((0.85, 1.82, z), (0.02, 0.1, 0.1), '#1c2a3a')          # janelas da ponte
mastro_x = -0.15
cil((mastro_x, 2.55, 0), 0.05, 1.5, '#6f7882')                                          # mastro alto
caixa((mastro_x, 3.15, 0), (0.9, 0.5, 0.05), '#6f7882'); caixa((mastro_x, 3.15, 0), (0.9, 0.04, 0.12), '#59616c')   # radar grande de varredura (Type 965)
caixa((0.45, 2.7, 0), (0.35, 0.2, 0.05), '#6f7882')                                       # antena menor
caixa((-0.75, 1.45, 0), (0.7, 0.75, 0.5), '#757e88', afina=0.7); caixa((-0.75, 1.88, 0), (0.62, 0.1, 0.46), '#262b31')   # chamine larga com topo preto
cil((1.7, 1.15, 0), 0.22, 0.22, '#7d8794'); caixa((1.7, 1.28, 0), (0.45, 0.2, 0.4), '#8d959d', afina=0.85)               # torre do canhao duplo de proa
cil((2.05, 1.3, 0.07), 0.03, 0.6, '#3b4249', rot=(0, math.pi / 2, 0)); cil((2.05, 1.3, -0.07), 0.03, 0.6, '#3b4249', rot=(0, math.pi / 2, 0))   # dois canos
caixa((-1.55, 1.3, 0), (0.7, 0.55, 0.5), '#8d959d', afina=0.9)                            # hangar do helicoptero
caixa((-2.05, 1.03, 0), (0.7, 0.04, 0.66), '#59616c'); cil((-2.0, 1.06, 0), 0.26, 0.01, '#e9edf2')   # heliponto da popa
caixa((0, 0.55, 0), (4.5, 0.07, 0.84), '#b02a2a')                                        # linha d'agua vermelha
caixa((0.6, 1.02, 0.3), (0.24, 0.05, 0.05), '#f4f4f4')                                    # numero do casco
fim(0.02)

# ---------------- BARCO DA GUARDA COSTEIRA ISLANDESA (patrulheiro pequeno): casco azul-marinho, casa do leme branca, mastro, canhao de proa, cortador de rede na popa ----------------
novo('barco_guarda')
casco(4.4, 0.7, 0.95, '#1f3a6a', '#14233f')
caixa((0, 0.85, 0), (3.9, 0.06, 0.85), '#a37a4b')                                        # convés de madeira
caixa((0.35, 1.2, 0), (1.3, 0.6, 0.62), '#f2f4f7', afina=0.9); caixa((0.55, 1.35, 0), (0.7, 0.28, 0.64), '#9fd0e6')   # casa do leme branca com janelas
caixa((0.35, 1.52, 0), (1.4, 0.05, 0.68), '#1f3a6a')                                      # teto
cil((0.35, 2.05, 0), 0.04, 0.9, '#6f7882'); caixa((0.35, 2.45, 0), (0.5, 0.05, 0.05), '#6f7882')   # mastro e antena
pano((0.35, 2.4, 0), 0.4, 0.26, ['#02529c', '#ffffff'], onda=0.05, nx=6)                  # bandeira azul da Islandia
cil((1.6, 1.0, 0), 0.14, 0.2, '#6f7882'); cil((1.9, 1.05, 0), 0.025, 0.55, '#3b4249', rot=(0, math.pi / 2, 0))   # canhao pequeno de proa
tubo([(-1.5, 0.9, 0), (-1.5, 1.75, 0)], 0.05, '#3b4249'); tubo([(-1.5, 1.75, 0), (-2.25, 1.55, 0)], 0.05, '#3b4249')   # braco da popa
caixa((-2.3, 1.4, 0), (0.25, 0.04, 0.05), '#d0d4d8'); caixa((-2.35, 1.3, 0.05), (0.18, 0.02, 0.2), '#e8c45a'); caixa((-2.35, 1.3, -0.05), (0.18, 0.02, 0.2), '#e8c45a')  # tesoura/gancho cortador de rede (lamina clara + garras amarelas)
caixa((0, 0.52, 0), (4.0, 0.06, 0.92), '#b02a2a')                                        # linha d'agua
fim(0.02)
