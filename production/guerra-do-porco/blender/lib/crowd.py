"""Multidão de personagens REAIS: cada soldado é um `Char` completo (mesmo rig, rosto, contorno irregular e atuação dos protagonistas), com variação individual
(altura, cabeça, olhos, boca, costeletas/bigode/barba, bochechas, tom do uniforme, fase da marcha, olhar). Regra do projeto (pedido do usuário): multidões/tropas/festas
nunca usam bonecos genéricos, instâncias simplificadas ou aleatórios — são personagens do mesmo estilo, renderizados de fato."""
import math, numpy as np
from . import util, anim, props, texlib
from .char import Char, U
NAVY = ['#2f4f8a', '#2a4a80', '#355896', '#2c4478', '#3a5a9a', '#34508c']
PANTS = ['#6c8fc8', '#7a9ad0', '#6286c0']
HAIR = ['#c4682c', '#7a4a2a', '#3b2a22', '#d8c8a0', '#a8843c', '#e3dfea', '#8a5a34']
MOUTHS = ['line', 'line', 'line', 'line', 'smirk', 'frown', 'teeth']
def soldier_look(rng, rank='private'):
    navy = str(rng.choice(NAVY)); L = dict(shirt=navy, pattern='uniform', shirt2='#9fb8e0', outfit='uniform', trim='#f0c250', pants=str(rng.choice(PANTS)), shoe='#1f1a2a', hat='kepi', hatColor=navy,
                                           build=float(rng.uniform(.9, 1.1)), headScale=float(rng.uniform(.94, 1.08)), sleeve=navy)
    if rng.random() < .38: L['sideburns'] = str(rng.choice(HAIR))
    if rng.random() < .36: L['mustache'] = str(rng.choice(HAIR))
    if rng.random() < .10: L['beard'] = str(rng.choice(HAIR))
    if rng.random() < .26: L['blush'] = True
    if rank == 'sergeant': L.update(hat='peaked', hatColor='#24305c', trim='#f6f1e6')
    return L
def block(cols=10, rows=8, col=None, seed=5):
    """tropa cols×rows de Chars completos; devolve lista de dicts (personagem + traços individuais)"""
    rng = np.random.default_rng(seed); out = []
    for c in range(cols):
        for r in range(rows):
            rank = 'sergeant' if rng.random() < .07 else 'private'
            ch = Char(f's{c}_{r}', soldier_look(rng, rank), col); rf = props.rifle(col); ch.attach('R', rf, (0, 0, -.1), (0, math.pi + 1.1, 0))   # fuzil vertical no ombro
            out.append(dict(ch=ch, rf=rf, c=c, r=r, off=float(rng.uniform(0, 1)), jit=(float(rng.uniform(-.28, .28)), float(rng.uniform(-.22, .22))),
                            lid=float(rng.uniform(.34, .62)), mouth=str(rng.choice(MOUTHS)), brows=(float(rng.uniform(-.2, .35)), float(rng.uniform(-.2, .35))), angry=float(rng.uniform(0, .25)),
                            tilt=float(rng.uniform(-.05, .05)), lx=float(rng.uniform(-.6, .6)), amp=float(rng.uniform(.88, 1.1))))
    return out
def place_block(items, xc, y0, t, cols=10, rows=8, sx=1.2, sy=1.12):
    from . import nature
    for it in items:
        x = xc + (it['c'] - (cols - 1) / 2) * sx + (it['r'] % 2) * .32 + it['jit'][0]; y = y0 + it['r'] * sy + it['jit'][1]; z = float(nature.height(x, y))
        d = anim.P(x=x, y=y, z=z, face=1, lid=it['lid'], mouth=it['mouth'], brows=it['brows'], angry=it['angry'], tilt=it['tilt'], blink=anim.blink_at(t, it['off'] * 3.0), look=(it['lx'] * (.6 + .4 * math.sin(t * .8 + it['off'] * 6)), 0))
        m = anim.march(t, it['off']); m['legL'] = tuple(v * it['amp'] for v in m['legL']); m['legR'] = tuple(v * it['amp'] for v in m['legR']); d.update(m); it['ch'].pose(d)

def add_bearer(items, idx=18, tex=None):
    """transforma o soldado `idx` em porta-bandeira (bandeira dos EUA ondulando, mastro preso à mão)"""
    it = items[idx]; it['rf'].hide_render = it['rf'].hide_viewport = True
    for o in it['rf'].children: o.hide_render = o.hide_viewport = True
    fl = props.Flag((0, 0, -.9), 1.5, .95, tex or texlib.flag_us(), 4.2); fl.attach(it['ch'].arm['R'][2], (0, 0, -.1 * U), (0, 1.1, 0)); it['flag'] = fl; return fl
