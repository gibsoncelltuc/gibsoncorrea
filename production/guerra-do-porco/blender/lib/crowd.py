"""Soldados em marcha (multidão de cabecinhas, como a arquibancada da referência): versão enxuta do personagem para dezenas de instâncias."""
import bpy, math, numpy as np
from . import util, mats
from .char import U, m_disc, m_box, m_stadium, m_capsule, mat, hexc, INK
class Soldier:
    def __init__(self, name, col=None, tone=1.0):
        self.name = name; self.col = col; self.root = util.empty(name, col=col); self.objs = []
        M_INK = mat('ink', INK, 'ink'); W = mat('head_w', hexc('#fbf8ff'), emit=.62); SH = mat('head_s', hexc('#d4d0ee'), emit=.45); blue = mat('s_blue', hexc('#2f4f8a'), emit=.28); belt = mat('s_belt', hexc('#f6f1e6'), emit=.3); leg = mat('s_leg', hexc('#6c8fc8'), emit=.25); gunm = mat('s_gun', (.05, .05, .08, 1), 'ink')
        a = self._a
        self.hipL = util.empty(name + '_hl', (-.2 * U, .05 * U, 1.38 * U), self.root, col); self.hipR = util.empty(name + '_hr', (.2 * U, -.01 * U, 1.38 * U), self.root, col)
        for h in (self.hipL, self.hipR): a(h, m_capsule(.085 * U, 1.1 * U), (1, 1, 1), (0, .04 * U + .004, 0), M_INK); a(h, m_capsule(.045 * U, 1.1 * U), (1, 1, 1), (0, -.002, 0), leg); a(h, m_disc(14), (.2 * U, 1, .115 * U), (.1 * U, -.003, -1.2 * U), M_INK)
        self.torso = util.empty(name + '_t', (0, 0, 1.38 * U), self.root, col)
        a(self.torso, m_stadium(1.0 * U, 1.5 * U), (1, 1, 1), (0, .004, .55 * U), M_INK); a(self.torso, m_stadium(.9 * U, 1.4 * U), (1, 1, 1), (0, 0, .55 * U), blue); a(self.torso, m_box(), (.15 * U, 1, 1.15 * U), (0, -.004, .55 * U), belt, rot=(0, .7, 0))
        for z in (.8, .5, .2): a(self.torso, m_disc(10), (.05 * U, 1, .05 * U), (0, -.006, z * U), mat('gold', hexc('#f0c250'), emit=.4))
        self.head = util.empty(name + '_h', (0, -.10 * U, 1.79 * U), self.torso, col); R = .56 * U
        a(self.head, m_disc(32), (R + .047 * U, 1, R + .047 * U), (0, .004, 0), M_INK); a(self.head, m_disc(32), (R, 1, R), (0, 0, 0), SH); a(self.head, m_disc(32), (R - .052 * U, 1, R - .052 * U), (.04 * U, -.003, .045 * U), W)
        for s in (-1, 1): a(self.head, m_box(), (.21 * U, 1, .05 * U), (s * .2 * U, -.012, .06 * U), M_INK)
        a(self.head, m_box(), (.16 * U, 1, .034 * U), (0, -.012, -.2 * U), M_INK)
        a(self.head, m_disc(24), (.5 * U, 1, .27 * U), (.02 * U, -.02, .47 * U), M_INK); a(self.head, m_disc(24), (.46 * U, 1, .235 * U), (.02 * U, -.024, .47 * U), blue); a(self.head, m_disc(18), (.34 * U, 1, .07 * U), (.36 * U, -.02, .36 * U), M_INK)
        a(self.torso, m_box(), (.07 * U, 1, 3.3 * U), (.55 * U, -.02, 1.5 * U), gunm, rot=(0, -.18, 0)) ; self.gun = self.objs[-1]
    def _a(self, parent, me, scale, loc, material, rot=(0, 0, 0)):
        o = bpy.data.objects.new(f'{self.name}_p', me); o.parent = parent; o.location = loc; o.scale = scale; o.rotation_euler = rot
        if len(me.materials) == 0: me.materials.append(None)
        o.material_slots[0].link = 'OBJECT'; o.material_slots[0].material = material; util.link(o, self.col); self.objs.append(o); return o
    def pose(self, x, y, t, off=0.0, z=0.0):
        ph = (t * 1.9 + off) * math.pi * 2; s, c = math.sin(ph), math.cos(ph)
        self.root.location = (x, y, z + abs(c) * .035); self.hipL.rotation_euler = (0, -(s * .62), 0); self.hipR.rotation_euler = (0, (s * .62), 0)
def block(cols=8, rows=5, col=None):
    out = []
    for c in range(cols):
        for r in range(rows): out.append(Soldier(f's{c}_{r}', col))
    return out
def place_block(soldiers, xc, y0, t, cols=8, rows=5, sx=1.25, sy=1.2):
    for c in range(cols):
        for r in range(rows):
            i = c * rows + r; x = xc + (c - (cols - 1) / 2) * sx + (r % 2) * .22; y = y0 + r * sy; z = float(__import__('lib.nature', fromlist=['height']).height(x, y)); soldiers[i].pose(x, y, t, ((i * 7) % 5) * .012, z)
