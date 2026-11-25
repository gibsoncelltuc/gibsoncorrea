# Vagens de ervilha EM PE (sessao B): cabem no enquadramento vertical do short. blender -b --python blender/objetos_b4.py
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
def _vagem(nome, casca, ervilha):
    novo(nome)
    cil((0, .02, 0), .22, .04, '#6b4a2b', lados=14)                                   # torrao de terra na base
    tubo([(0, .04, 0), (.0, .22, 0)], .03, '#5f8a3a')                                  # caule
    bola((0, .72, 0), .5, casca, achata=.5, seg=24, esc=(.62, 1.0, .5))               # casca em pe, pontas afinadas
    bola((0, 1.26, 0), .1, casca, esc=(.6, 2.0, .6))                                    # ponta de cima
    for i in range(6):
        for zz in (-.14, .14): bola((0, .38 + i * .152, zz), .12, ervilha, seg=14)           # ervilhas empilhadas na casca
    caixa((.0, .72, .0), (.03, 1.05, .56), casca)                                      # costura
    fim(.015)
_vagem('vagem_verde', '#5fae3f', '#9bdc4a')
_vagem('vagem_amarela', '#e0c030', '#ffd400')
