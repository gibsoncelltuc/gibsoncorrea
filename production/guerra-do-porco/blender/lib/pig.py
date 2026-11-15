"""Porco 2D cut-out em 3D (porta de src/characters/Pig.tsx): corpo, cabeça com focinho/orelha/olho (pálpebra ou X), 4 pernas, rabo em espiral."""
import bpy, math
from . import util, mats
from .char import U, m_disc, m_box, m_tri, m_arc, m_capsule, mat, hexc, INK
class Pig:
    def __init__(self, name='pig', col=None):
        self.name = name; self.col = col; self.objs = []
        PINK, PINK2, PINK3 = hexc('#f7a2b6'), hexc('#e98aa2'), hexc('#ffd0da'); M_INK = mat('ink', INK, 'ink'); M_P = mat('pig_p', PINK, emit=.4); M_P2 = mat('pig_p2', PINK2, emit=.4); M_P3 = mat('pig_p3', PINK3, emit=.4)
        self.root = util.empty(name, col=col); self.pivot = util.empty(name + '_pivot', (0, 0, .88 * U), self.root, col); self.shape = util.empty(name + '_shape', (0, 0, -.88 * U), self.pivot, col)
        a = self._add
        # pernas (articuladas no quadril)
        self.legs = []
        for i, (x, d) in enumerate([(-.62, -1), (-.34, 1), (.42, 1), (.70, -1)]):
            dy = .02 if i % 2 == 0 else -.03; g = util.empty(f'{name}_leg{i}', (x * U, dy * U, .68 * U), self.shape, col)
            a(g, m_capsule(.15 * U, .38 * U), (1, 1, 1), (0, (.15 - .118) * U + .004, 0), M_INK); a(g, m_capsule(.118 * U, .38 * U), (1, 1, 1), (0, -.002, 0), M_P2)
            a(g, m_disc(14), (.13 * U, 1, .08 * U), (.03 * U, -.004, -.66 * U), M_INK); self.legs.append((g, d))
        # tronco
        a(self.shape, m_disc(40), (1.14 * U, 1, .74 * U), (0, .004, .88 * U), M_INK); a(self.shape, m_disc(40), (1.07 * U, 1, .67 * U), (0, 0, .88 * U), M_P)
        a(self.shape, m_disc(32), (.82 * U, 1, .34 * U), (-.05 * U, -.004, .66 * U), M_P3); a(self.shape, m_disc(20), (.3 * U, 1, .2 * U), (-.4 * U, -.006, 1.12 * U), mat('pig_spot', hexc('#7d4f66'), emit=.3))
        # rabo
        self.tail = util.empty(name + '_tail', (-1.05 * U, .03 * U, 1.05 * U), self.shape, col); a(self.tail, m_arc(.5, math.pi * 1.6), (.14 * U, 1, .14 * U), (0, .003, 0), M_INK); a(self.tail, m_arc(.25, math.pi * 1.6), (.14 * U, 1, .14 * U), (0, 0, 0), M_P2)
        # cabeça
        self.head = util.empty(name + '_head', (.98 * U, -.06 * U, .98 * U), self.shape, col); H = self.head
        a(H, m_disc(36), (.52 * U, 1, .50 * U), (0, .004, 0), M_INK); a(H, m_disc(36), (.47 * U, 1, .45 * U), (0, 0, 0), M_P)
        self.ear = util.empty(name + '_ear', (-.12 * U, -.004, .48 * U), H, col); a(self.ear, m_tri(), (.55 * U, 1, .5 * U), (0, .003, .1 * U), M_INK); a(self.ear, m_tri(), (.44 * U, 1, .4 * U), (0, 0, .09 * U), M_P2)
        a(H, m_disc(22), (.25 * U, 1, .2 * U), (.46 * U, -.008, -.12 * U), M_INK); a(H, m_disc(22), (.215 * U, 1, .165 * U), (.46 * U, -.010, -.12 * U), M_P3)
        for dx in (.43, .54): a(H, m_disc(10), (.034 * U, 1, .055 * U), (dx * U, -.012, -.10 * U), M_INK)
        a(H, m_disc(12), (.07 * U, 1, .05 * U), (0, -.008, -.12 * U), mat('pig_blush', hexc('#f26a8a'), emit=.4))
        eg = util.empty(name + '_eye', (.14 * U, -.012, .12 * U), H, col); self.pupil = a(eg, m_disc(12), (.05 * U, 1, .058 * U), (0, 0, 0), M_INK); self.lid = a(eg, m_box(), (.16 * U, 1, .04 * U), (0, -.002, .055 * U), M_INK)
        self.x1 = a(eg, m_box(), (.2 * U, 1, .045 * U), (0, -.002, 0), M_INK, rot=(0, .8, 0)); self.x2 = a(eg, m_box(), (.2 * U, 1, .045 * U), (0, -.002, 0), M_INK, rot=(0, -.8, 0)); self.eg = eg
        self.tongue = a(H, m_disc(12), (.07 * U, 1, .13 * U), (.36 * U, -.014, -.34 * U), mat('tongue', hexc('#e0646a'), emit=.4))
    def _add(self, parent, me, scale, loc, material, rot=(0, 0, 0)):
        o = bpy.data.objects.new(f'{self.name}_p', me); o.parent = parent; o.location = loc; o.scale = scale; o.rotation_euler = rot
        if len(me.materials) == 0: me.materials.append(None)
        o.material_slots[0].link = 'OBJECT'; o.material_slots[0].material = material; util.link(o, self.col); self.objs.append(o); return o
    def pose(self, p):
        t = p.get('t', 0); mode = p.get('mode', 'eat'); sc = p.get('scale', 1.25) * 0.8
        self.root.location = (p.get('x', 0), p.get('y', 0), p.get('z', 0) + p.get('hop', 0) * U); self.root.scale = (p.get('face', -1) * sc, 1, sc)
        self.pivot.rotation_euler = (0, -p.get('flip', 0) * math.pi, 0)
        eat, trot, dead = mode == 'eat', mode == 'trot', mode == 'dead'
        chew = math.sin(t * 13) * .05 if eat else 0; head_rot = (-.62 + chew) if eat else (math.sin(t * 7) * .04 if trot else 0)
        self.head.rotation_euler = (0, -head_rot, 0); swing = math.sin(t * 11) if trot else 0
        for g, d in self.legs: g.rotation_euler = (0, -(d * swing * .5 + (.1 * d if dead else 0)), 0)
        self.tail.rotation_euler = (0, -(0 if dead else math.sin(t * (9 if eat else 5)) * .25), 0); self.ear.rotation_euler = (0, -(.6 if dead else math.sin(t * 6) * .07), 0)
        showx = dead or p.get('shock', 0) > 0
        for o, v in ((self.pupil, not showx), (self.lid, not showx), (self.x1, showx), (self.x2, showx), (self.tongue, dead)): o.hide_render = o.hide_viewport = not v
        self.lid.location.z = (.055 - (.03 if eat else 0)) * U
