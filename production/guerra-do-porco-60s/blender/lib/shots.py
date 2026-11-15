"""Cenas e coreografia de 'A Guerra do Porco' — versão completa de 60 s (ESPECÍFICO DA HISTÓRIA).
Cada classe de cena: build() cria mundo/atores UMA vez; update(t) aplica poses e câmera como FUNÇÃO PURA do tempo absoluto t (s) → determinístico, e os INSERTS (subclasses)
reaproveitam a mesma coreografia com outra câmera (continuidade perfeita nos cortes). Os tempos vêm das PALAVRAS da narração (W = word_start) e da lista de edição
(storyboard/edl.json → shots.json → anim.EDIT). Cenas portadas do piloto aprovado: Hook, PigIn(+inserts), Notes, Army/Landing, Deck, Grave. Cenas novas: ver shots_new.py."""
import bpy, math, numpy as np
from mathutils import Vector
from . import util, mats, texlib, renderlib, farm, nature, char, pig, props, ships, crowd, deck, anim, sets
from .anim import *
from .char import U
W = word_start; E = EDIT
LOOKS = {
 'cutlar': dict(shirt='#ead9b4', pattern='plain', outfit='overalls', pants='#2f2a46', shoe='#5a3a2a', hat='straw', hatColor='#e8c068', hatBand='#3a6aa8', beard='#c9a06a', build=1.0, sleeve='#2f2a46'),
 'griffin': dict(shirt='#f3ead6', pattern='plain', outfit='waistcoat', trim='#8a6a3a', pants='#3a3350', shoe='#2a2030', hat='flatcap', hatColor='#8c7a58', sideburns='#c4682c', mustache='#c4682c', blush=True, build=1.18),
 'soldier': dict(shirt='#2f4f8a', pattern='uniform', shirt2='#9fb8e0', outfit='uniform', trim='#f0c250', pants='#6c8fc8', shoe='#1f1a2a', hat='kepi', hatColor='#2f4f8a', build=1.0, sleeve='#2f4f8a'),
 'captain': dict(shirt='#2a4478', pattern='uniform', shirt2='#9fb8e0', outfit='uniform', trim='#f0c250', pants='#6c8fc8', shoe='#1f1a2a', hat='kepi', hatColor='#2a4478', mustache='#3b2a22', beard='#3b2a22', build=1.08, sleeve='#2a4478'),
 'baynes': dict(shirt='#24305c', pattern='plain', outfit='admiral', trim='#f0c250', pants='#2f2a46', shoe='#1a1624', hat='bicorn', sideburns='#e3dfea', mustache='#d8d4e0', build=1.15, sleeve='#24305c'),
 'aide': dict(shirt='#2a3a70', pattern='plain', outfit='uniform', trim='#f6f1e6', pants='#2f2a46', shoe='#1a1624', hat='peaked', hatColor='#24305c', blush=True, build=0.92, sleeve='#2a3a70'),
 'marine': dict(shirt='#b9363a', pattern='uniform', shirt2='#d8776a', outfit='uniform', trim='#f6f1e6', pants='#2f2a46', shoe='#1a1624', hat='shako', hatColor='#1c1a2c', mustache='#7a4a2a', build=1.02, sleeve='#b9363a'),
 'official': dict(shirt='#3a3350', pattern='plain', outfit='waistcoat', trim='#6a5a86', pants='#2f2a46', shoe='#1a1624', hat='tophat', hatColor='#22202e', hatBand='#7a2a34', sideburns='#b8b0c4', glasses=True, build=1.04, sleeve='#3a3350'),
 'governor': dict(shirt='#2c2a48', pattern='plain', outfit='waistcoat', trim='#b08a3a', pants='#2f2a46', shoe='#1a1624', hat='tophat', hatColor='#1c1a2c', hatBand='#b08a3a', hatH=.86, sideburns='#e3dfea', mustache='#e3dfea', build=1.28, headScale=1.06, sleeve='#2c2a48'),
 'kaiser': dict(shirt='#1f3a6a', pattern='plain', outfit='admiral', trim='#f0c250', pants='#2f2a46', shoe='#1a1624', hat='pickelhaube', hatColor='#1c1a2c', sideburns='#d8d4e0', mustache='#d8d4e0', build=1.2, headScale=1.05, sleeve='#1f3a6a'),
}
PIG0 = (1.1, -0.4); CUT = (-0.1, -2.5)
CAM_LOOP = dict(pos=(1.7, -6.4, 0.80), look=(0.55, -0.2, 0.95), fov=57)
BANG1 = W('L1', 'matou') + 0.1; BANG2 = W('L3', 'atirou') + 0.05; STAMP = W('L11', 'americana') + 0.10
BANGS[:] = [BANG1, BANG2]                      # tremor de câmera em cam_at() (mesma lista de anim: alterada no lugar)
def gz(x, y): return float(nature.height(x, y))
def apply_cam(cam, spec, focus=None, fstop=3.2, dof=True):
    cam.data.dof.use_dof = dof; renderlib.place_camera(cam, spec['pos'], spec['look'], fov=spec['fov'], roll=spec.get('roll', 0), focus=focus if focus is not None else math.dist(spec['pos'], spec['look']), fstop=fstop)
def aim_between(pos, pts, z=1.0):
    """direção de olhar que centraliza (em yaw) os pontos: mantém personagens dentro do quadro vertical 9:16"""
    ang = [math.atan2(p[0] - pos[0], p[1] - pos[1]) for p in pts]; yaw = (min(ang) + max(ang)) / 2; d = 8.0
    return (pos[0] + math.sin(yaw) * d, pos[1] + math.cos(yaw) * d, z)
def muzzle(rf): bpy.context.view_layer.update(); return rf.matrix_world @ Vector((0, 0, -0.9))
def _head(ch): bpy.context.view_layer.update(); return ch.head.matrix_world.translation
def hide(o, h=True):
    o.hide_render = o.hide_viewport = h
    for c in o.children_recursive: c.hide_render = c.hide_viewport = h
def ramp(t, t0, d=.3, ease=ease_inout): return keys(t, [(t0, 0), (t0 + d, 1)], ease)
class Base:
    eid = None
    def __init__(self, R): self.R = R; self.cam = renderlib.camera(56, dof=True, fstop=3.2, focus=6.0)
    def focus_(self): return self.keys_() if hasattr(self, 'keys_') else {}        # objetos que DEVEM estar no quadro neste plano (check_framing / camera_report)
    def frames(self, fps=30, pad=.2):
        e = self.eid or self.id; a, b = EDIT[e]; first = e == EDL[0][0]; last = e == EDL[-1][0]
        return range(int(round((a - (0 if first else pad)) * fps)), int(round((b + (0 if last else pad)) * fps)))
    def span(self): return EDIT[self.eid]
# ------------------------------------------------------------------ GANCHO (portado: S1 do piloto)
class Hook(Base):
    id = 'Hook'
    def keys_(self): return {'cutlar': self.cut.head, 'pig': self.pig.head}
    def build(self):
        R = self.R; self.f = farm.build('golden', grass_n=R['grass']); self.fleet = ships.fleet(); self.cut = char.Char('cutlar', LOOKS['cutlar']); self.pig = pig.Pig(); self.rf = props.rifle(); self.cut.attach('R', self.rf, (0, 0, -.1))
        self.fl = props.Flash(); self.puffs = [props.Puff() for _ in range(5)]
        self._ship_base = {o.name: (tuple(o.location), tuple(o.scale)) for o in self.fleet}
        sets.S1(); self.birds = sets.Birds(7, 3)
    def update(self, t):
        self.birds.update(t); sets.drift_clouds(self.f, t)
        base = idle(t, x=CUT[0], y=CUT[1], z=gz(*CUT), face=1); up = aim_up(t, -.9, BANG1); c = aim_fire(t, base, -.9, BANG1)
        if t > BANG1 + .45: c.update(lid=.55, brows=(.2, -.3), mouth='smirk')
        self.cut.pose(c); self.rf.rotation_euler = (0, math.pi * (1 - up), 0)
        u = clamp((t - BANG1 - .04) / .5); dead = t > BANG1 + .04
        self.pig.pose(dict(x=PIG0[0], y=PIG0[1], z=gz(*PIG0), face=-1, t=t, mode='dead' if dead else 'eat', flip=ease_out(u), hop=2.1 * math.sin(min(1, u) * math.pi) if dead else 0))
        m = muzzle(self.rf); self.fl.set(t, BANG1, m, .22)
        for i, p in enumerate(self.puffs): p.set(t, BANG1 + .05 + i * .07, (m.x + .25 + i * .15, m.y, m.z), 1.2, .07 + i * .02, .4 + i * .1, (.5, 0))
        fu = smoother((t - 2.2) / 1.0)
        for o in self.fleet:
            loc, sc = self._ship_base[o.name]; o.hide_render = o.hide_viewport = fu < .01; k = .15 + .85 * fu; o.scale = (sc[0] * k, sc[1] * k, sc[2] * k); o.location = (loc[0], loc[1] + 35 * (1 - fu), loc[2])
        end = self.span()[1]; pts = [CUT, PIG0]; p1 = (1.9, -6.3, .72)
        spec = cam_at(t, [dict(t=0, pos=CAM_LOOP['pos'], look=aim_between(CAM_LOOP['pos'], pts, .95), fov=CAM_LOOP['fov']), dict(t=1.5, pos=p1, look=aim_between(p1, pts, .9), fov=55), dict(t=2.3, pos=(1.5, -5.2, 1.8), look=(.4, 8.0, 1.9), fov=58), dict(t=end + .3, pos=(3.2, -3.6, 5.8), look=(-2.0, 60.0, 2.2), fov=64)])
        far = clamp((t - 2.0) / 1.5); apply_cam(self.cam, spec, focus=lerp(6.4, 70, far), fstop=lerp(2.1, 8.0, far))
# ------------------------------------------------------------------ INCIDENTE (portado: S2 do piloto) + inserts
class PigIn(Base):
    """o porco trota pela brecha da cerca até a horta; Cutlar percebe, mira e atira (BANG2). Subclasses = outras câmeras sobre a MESMA ação."""
    id = 'PigIn'
    def cut_hook(self, c, t): return c
    def keys_(self): return {'cutlar': self.cut.head, 'pig': self.pig.head}
    def focus_(self): return {'pig': self.pig.head}
    def build(self):
        R = self.R; self.f = farm.build('golden', grass_n=R['grass']); self.cut = char.Char('cutlar', LOOKS['cutlar']); self.pig = pig.Pig(); self.rf = props.rifle(); self.cut.attach('R', self.rf, (0, 0, -.1)); self.fl = props.Flash(); self.puffs = [props.Puff() for _ in range(5)]
        self.uk = props.Flag((12.0, 6.5, 0), 2.4, 1.5, texlib.flag_uk(), 6.5)
        sets.S2(); self.smk = sets.chimney(); self.birds = sets.Birds(6, 5, (10, 140, 50))
    def pig_state(self, t):
        ta = E['E06_pigin'][0] - .1; tb = W('L3', 'invadiu') + .45; trot = clamp((t - ta) / (tb - ta))
        px = lerp(9.6, PIG0[0], ease_inout(trot)); py = lerp(1.4, PIG0[1], ease_inout(clamp((t - (tb - .8)) / .8))); return px, py, ('trot' if trot < 1 else 'eat')
    def act(self, t):
        self.birds.update(t); sets.drift_clouds(self.f, t)
        t0 = BANG2 - 1.0; tn = W('L3', 'horta') + .1; base = idle(t, x=CUT[0], y=CUT[1], z=gz(*CUT), face=1); c = aim_fire(t, base, t0, BANG2)
        if tn - .1 < t < t0: c = dict(shock(t, c, tn), mouth='line')
        c = self.cut_hook(c, t); self.cut.pose(c); self.rf.rotation_euler = (0, math.pi * (1 - aim_up(t, t0, BANG2)), 0)
        px, py, mode = self.pig_state(t); self.pig.pose(dict(x=px, y=py, z=gz(px, py), face=-1, t=t, mode=mode)); m = muzzle(self.rf); self.fl.set(t, BANG2, m, .24)
        for i, p in enumerate(self.puffs): p.set(t, BANG2 + .05 + i * .07, (m.x + .25 + i * .15, m.y, m.z), 1.2, .07 + i * .02, .4 + i * .1, (.5, 0))
        self.uk.update(t); self.smk.update(t); return px, py
    def camera(self, t, px, py):                                   # E06: acompanha o porco pela cerca (a bandeira britânica ao fundo no começo)
        a, b = E['E06_pigin']; spec = cam_at(t, [dict(t=a - .2, pos=(11.3, -5.4, .62), look=(0, 0, 0), fov=60, roll=.05), dict(t=b + .3, pos=(6.9, -7.0, .82), look=(0, 0, 0), fov=57, roll=-.02)])
        spec['look'] = (px - .9, py, .75); apply_cam(self.cam, spec, focus=math.dist(spec['pos'], (px, py, .6)), fstop=2.4)
    def update(self, t): px, py = self.act(t); self.camera(t, px, py)
class I_Garden(PigIn):
    """a horta: o porco devora os repolhos; Cutlar percebe ao fundo (choque)"""
    id = 'PigIn'
    def focus_(self): return {'cutlar': self.cut.head, 'pig': self.pig.head}
    def camera(self, t, px, py):
        a, b = E['E07_garden']; pa = (6.2, -7.4, .9); pb = (3.5, -6.7, .84)
        spec = cam_at(t, [dict(t=a - .2, pos=pa, look=aim_between(pa, [CUT, PIG0], 1.0), fov=57, roll=.02), dict(t=b + .3, pos=pb, look=aim_between(pb, [CUT, PIG0], .95), fov=53, roll=.05)])
        apply_cam(self.cam, spec, focus=math.dist(spec['pos'], (px, py, 1.0)), fstop=2.4)
def _deadpan(c, t):
    """rosto do Cutlar nos closes: olhar pesado e cansado ("de novo") que vai se estreitando até o tiro; clarão e reação depois"""
    d = t - BANG2; sq = clamp((t - (BANG2 - .75)) / .6); c = dict(c)
    c.update(eye='lid', lid=lerp(.70, .88, sq) if d < 0 else .9, brows=(lerp(-.12, -.55, sq), lerp(-.12, -.55, sq)), angry=lerp(.15, .5, sq), mouth='line' if d < .25 else 'smirk', open=0, squash=0,
             blink=1.0 if 0 <= d < .1 else 0.0, sweat=(t - (BANG2 - .5)) * 1.1 if -.5 < d < .8 else 0, look=(lerp(.75, .25, sq), 0))
    return c
class I_Again(PigIn):
    """'De novo.' — close frontal: Cutlar de olhar pesado; atrás dele o porco mastiga"""
    id = 'PigIn'
    def focus_(self): return {'cutlar': self.cut.head}
    def cut_hook(self, c, t): return _deadpan(c, t)
    def camera(self, t, px, py):
        hp = _head(self.cut); a, b = E['E08_again']; u = clamp((t - a + .2) / (b - a + .4)); dist = lerp(2.25, 2.0, u)
        spec = dict(pos=(hp.x - .2 + .1 * u, hp.y - dist, hp.z + .02), look=(hp.x + .26, hp.y, hp.z - .03), fov=lerp(47, 45, u), roll=.03)
        apply_cam(self.cam, spec, focus=dist, fstop=2.2)
class I_Eyes(PigIn):
    """close no rosto do Cutlar: os olhos se estreitam → TIRO (clarão acende o rosto, piscada, tremor) → reação"""
    id = 'PigIn'
    def focus_(self): return {'cutlar': self.cut.head}
    def cut_hook(self, c, t): return _deadpan(c, t)
    def camera(self, t, px, py):
        hp = _head(self.cut); u = clamp((t - (BANG2 - .75)) / .75); dist = lerp(1.75, 1.2, smoother(u)); d = t - BANG2
        e = math.exp(-d * 9) if 0 <= d < .7 else 0.0; pos = (hp.x + math.sin(d * 70) * .05 * e, hp.y - dist, hp.z + .04 + math.cos(d * 63) * .04 * e)
        spec = dict(pos=pos, look=(hp.x - .03, hp.y, hp.z + .0), fov=lerp(40, 34, u) - 3 * e, roll=.07 - .05 * u); apply_cam(self.cam, spec, focus=dist, fstop=1.8)
class I_PigDead(PigIn):
    """'…por causa de um porco.' — o porco morto na horta, olhos em X, uma mosca dando voltas"""
    id = 'PigIn'
    def focus_(self): return {'pig': self.pig.head}
    def build(self):
        PigIn.build(self); bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=.022); self.fly = bpy.context.object; self.fly.data.materials.append(mats.flat('fly_m', (.03, .03, .04, 1), rough=.5, haze=False)); self.fly.visible_shadow = False
    def update(self, t):
        self.birds.update(t); sets.drift_clouds(self.f, t); self.smk.update(t); self.uk.update(t); self.fl.set(-9, 0, (0, 0, 0)); [p.set(-9, 0, (0, 0, 0)) for p in self.puffs]
        self.cut.pose(idle(t, x=-30, y=-40, z=0)); x, y = PIG0; z = gz(x, y)
        self.pig.pose(dict(x=x, y=y, z=z, face=-1, t=t, mode='dead', flip=1))
        a, b = E['E25_pigdead']; k = t * 7.5; self.fly.location = (x - .1 + .34 * math.cos(k), y - .35 + .1 * math.sin(k * .7), z + 1.0 + .16 * math.sin(k * 1.3))
        u = clamp((t - a + .2) / (b - a + .4)); spec = dict(pos=(x + .75 - .3 * u, y - lerp(3.3, 2.75, smoother(u)), z + .34), look=(x - .05, y, z + .62), fov=lerp(44, 40, u), roll=.07 - .04 * u)
        apply_cam(self.cam, spec, focus=math.dist(spec['pos'], (x, y, z + .5)), fstop=2.2)
# ------------------------------------------------------------------ ZOMBADOR (portado: S3 do piloto) + insert
class Notes(Base):
    id = 'Notes'
    def keys_(self): return {'cutlar': self.cut.head, 'griffin': self.gr.head, 'pig': self.pig.head}
    def focus_(self): return {'cutlar': self.cut.head, 'griffin': self.gr.head}
    def build(self):
        R = self.R; self.f = farm.build('golden', grass_n=R['grass']); self.cut = char.Char('cutlar', LOOKS['cutlar']); self.gr = char.Char('griffin', LOOKS['griffin']); self.pig = pig.Pig()
        self.n100 = props.note('$100', .6); self.n10 = props.note('$10', .42); self.gr.attach('R', self.n100, (0.28, 0, -.1)); self.cut.attach('R', self.n10, (0.2, 0, -.1)); sets.S3(); self.smk = sets.chimney(); self.birds = sets.Birds(7, 7, (30, 150, 48))
    def act(self, t):
        self.birds.update(t); sets.drift_clouds(self.f, t)
        XC, XG, XP, Y = 4.7, 6.1, 5.4, -1.0; s0 = E['E10_notes'][0]; self.smk.update(t)
        tcem = W('L4', 'cem') - .35; tdez = W('L4', 'ofereceu') - .2; tlaugh = W('L4', 'dez') - .05
        g = smug(idle(t, x=XG, y=Y, z=gz(XG, Y), face=-1, off=.7)); gu = keys(t, [(tcem, 0), (tcem + .3, 1)], ease_inout)
        g.update(armR=(lerp(-.1, 1.75, gu), lerp(.12, .9, gu)), armL=(lerp(.1, 1.3, keys(t, [(s0 + .3, 0), (s0 + .6, 1)], ease_inout)), .1))
        if t > tlaugh: g = laugh(t, g, .8)
        c = idle(t, x=XC, y=Y, z=gz(XC, Y), face=1, off=.2); cu = keys(t, [(tdez, 0), (tdez + .3, 1)], ease_inout)
        c.update(eye='lid', lid=.35, angry=.7, brows=(-.2, -.2), mouth='teeth', armR=(lerp(-.1, 1.6, cu), lerp(.12, .8, cu)), sweat=(t - tdez) * 1.1 if t > tdez else 0)
        self.gr.pose(g); self.cut.pose(c); self.pig.pose(dict(x=XP, y=Y + .5, z=gz(XP, Y + .5), face=1, t=t, mode='dead', flip=1))
        for n, ch in ((self.n100, g), (self.n10, c)):
            ang = ch['armR'][0] + ch['armR'][1] + ch['lean']; n.rotation_euler = (0, ang + (.1 if ch is g else -.12), 0); n.scale = (-1 if ch['face'] < 0 else 1, 1, 1)
        self.n100.hide_render = self.n100.hide_viewport = t < tcem; self.n10.hide_render = self.n10.hide_viewport = t < tdez
    def update(self, t):
        self.act(t); a = E['E10_notes'][0]; b = E['E11_inotes'][1]
        spec = cam_at(t, [dict(t=a - .2, pos=(5.4, -6.4, .6), look=(5.4, -1.0, 1.15), fov=54, roll=.12), dict(t=b + .3, pos=(5.4, -5.2, .9), look=(5.4, -1.0, 1.25), fov=50, roll=.08)])
        apply_cam(self.cam, spec, focus=math.dist(spec['pos'], (5.35, -1.0, 1.0)), fstop=2.3)
class I_Notes(Notes):
    """close nas duas notas: $100 enorme × $10 pequena, com as mãos e a risada do Griffin"""
    id = 'Notes'
    def focus_(self): return {'n100': self.n100, 'n10': self.n10}
    def update(self, t):
        self.act(t); bpy.context.view_layer.update(); a = self.n100.matrix_world.translation; b = self.n10.matrix_world.translation
        mid = ((a.x + b.x) / 2, (a.y + b.y) / 2, (a.z + b.z) / 2 - .05); u = clamp((t - (E['E11_inotes'][0] - .2)) / 1.3)
        spec = dict(pos=(mid[0] - .1 + .12 * u, mid[1] - lerp(2.5, 2.0, smoother(u)), mid[2] + .1), look=mid, fov=lerp(40, 35, u), roll=.12 - .08 * u)
        apply_cam(self.cam, spec, focus=lerp(2.5, 2.0, smoother(u)), fstop=2.0)
# ------------------------------------------------------------------ ESCALADA (portado: S4 do piloto): tropa de personagens reais
class Army(Base):
    """tropa americana marchando no campo; frota britânica surge no horizonte (E19). Landing = mesma cena com a companhia de 64 homens recém-desembarcada."""
    id = 'Army'; COLS, ROWS = 12, 8; START = 'E17_army'; CAMP = True; BEARER = 23; SEED = 5
    def keys_(self): return {'lead': self.lead.head, 'sol0': self.sol[0]['ch'].head}
    def focus_(self): return {'lead': self.lead.head}
    def build(self):
        R = self.R; self.f = farm.build('golden', grass_n=R['grass'] // 2, grass_areas=[((-42, -4, 16, 40), R['grass'])]); self.fleet = ships.fleet(); self.sol = crowd.block(self.COLS, self.ROWS, seed=self.SEED); self.bearer = crowd.add_bearer(self.sol, self.BEARER)
        self.lead = char.Char('lead', LOOKS['captain'])
        for o in self.f['trees']: o.visible_shadow = False   # abetos a oeste projetavam sombra longa e escura (sol a 24°) sobre o campo desta cena
        self._ship_base = {o.name: (tuple(o.location), tuple(o.scale)) for o in self.fleet}; self.us = None; self.birds = sets.Birds(8, 9, (-40, 150, 50))
        if self.CAMP:
            for tp in [(-34, 38.5, 1.2, .2), (-27, 40.5, 1.1, -.3), (-41, 37.5, 1.0, .5), (-20.5, 41.5, 1.1, .1)]: props.tent((tp[0], tp[1], gz(tp[0], tp[1])), tp[2], tp[3])
            self.us = props.Flag((-33, 42.0, gz(-33, 42)), 2.2, 1.4, texlib.flag_us(), 6.0); sets.S4()
            self.cannons = []
            for i, x in enumerate((-22.5, -19.2, -15.9, -12.6, -9.3, -6.0)):
                cn = props.cannon(); cn.location = (x, 23.4 + .25 * (i % 2), gz(x, 23.4)); cn.rotation_euler = (0, 0, math.radians(78 + 5 * (i % 3))); self.cannons.append(cn)
        else: sets.S4_landing()
    def block_x(self, t): return -24 + 2.45 * (t - E[self.START][0])
    def fleet_u(self, t): return 0.0
    def act(self, t):
        self.birds.update(t); sets.drift_clouds(self.f, t); bx = self.block_x(t); crowd.place_block(self.sol, bx, 27.2, t, cols=self.COLS, rows=self.ROWS); self.bearer.update(t)
        if self.us: self.us.update(t)
        ld = idle(t, x=bx + self.COLS * .6 + .9, y=25.2, z=gz(bx + self.COLS * .6 + .9, 25.2), face=1); ld.update(march(t)); ld.update(eye='lid', lid=.4, angry=.3, brows=(.1, .1), mouth='line', armR=(.3, .2)); self.lead.pose(ld)
        fu = self.fleet_u(t)
        for o in self.fleet: loc, sc = self._ship_base[o.name]; o.hide_render = o.hide_viewport = fu < .01; k = .15 + .85 * fu; o.scale = (sc[0] * k, sc[1] * k, sc[2] * k); o.location = (loc[0], loc[1] + 35 * (1 - fu), loc[2])
        return bx
    def update(self, t):                                            # E17: grua subindo por trás da linha de canhões; a tropa enorme passa ao fundo
        bx = self.act(t); a, b = E['E17_army']; u = smoother(clamp((t - a + .2) / (b - a + .4))); cx = bx + 3.0
        spec = dict(pos=(cx - 1.6 + .8 * u, lerp(19.6, 18.6, u), lerp(.55, 2.7, u)), look=(cx + 1.0, 29.0, lerp(1.0, 1.5, u)), fov=lerp(58, 62, u), roll=.03 - .03 * u)
        apply_cam(self.cam, spec, focus=lerp(4.5, 9.5, u), fstop=3.2)
class I_Rows(Army):
    """'quatrocentos e sessenta e um soldados' — câmera baixa desliza rápido CONTRA a marcha: fileiras e fileiras de rostos diferentes"""
    id = 'Army'
    def focus_(self): return {}
    def update(self, t):
        bx = self.act(t); a, b = E['E18_rows']; u = clamp((t - a + .2) / (b - a + .4)); x = bx + lerp(8.2, -4.2, u)
        spec = dict(pos=(x, 24.9, .62), look=(x - 2.6, 31.0, 1.28), fov=60, roll=-.03); apply_cam(self.cam, spec, focus=4.2, fstop=3.0)
class Fleet5(Army):
    """'contra cinco navios' — a câmera sobe da tropa e encontra a frota em escalão na baía"""
    id = 'Army'
    def focus_(self): return {'fleet': self.fleet[2]}
    def fleet_u(self, t): return smoother((t - (E['E19_fleet5'][0] - .75)) / .8)
    def update(self, t):
        bx = self.act(t); a, b = E['E19_fleet5']; u = smoother(clamp((t - (a - .25)) / .95))
        pa = dict(pos=(bx - 1.2, 21.0, .62), look=(bx + 1.4, 29.0, 1.25), fov=60); pb = dict(pos=(bx - .2, 21.4, 3.6), look=(8.0, 78.0, 2.6), fov=58)
        spec = dict(pos=[lerp(pa['pos'][i], pb['pos'][i], u) for i in range(3)], look=[lerp(pa['look'][i], pb['look'][i], u) for i in range(3)], fov=lerp(pa['fov'], pb['fov'], u), roll=.02)
        apply_cam(self.cam, spec, focus=lerp(6.0, 70.0, u), fstop=lerp(2.8, 8.0, u))
class Landing(Army):
    """'Então chegou o exército americano' — a companhia de 64 homens (8×8) marcha com o capitão e o porta-bandeira; ainda sem acampamento"""
    id = 'Landing'; COLS, ROWS = 8, 8; START = 'E13_landing'; CAMP = False; BEARER = 7; SEED = 11
    def focus_(self): return {'lead': self.lead.head}
    def update(self, t):
        bx = self.act(t); a = E['E13_landing'][0]; b = E['E14_faces'][1]; u = clamp((t - a + .2) / (b - a + .4)); cx = bx + 3.4
        spec = dict(pos=(cx - 1.0 + .5 * u, 20.6, .6 + .1 * u), look=(cx + 1.3, 29.0, 1.25), fov=60, roll=.03); apply_cam(self.cam, spec, focus=6.0, fstop=2.8)
class I_Faces(Landing):
    """'sessenta e poucos soldados' — close em três rostos (todos diferentes) marchando; a câmera acompanha"""
    id = 'Landing'; FACES = (24, 33, 42)
    def focus_(self): return {f'sol{k}': self.sol[k]['ch'].head for k in self.FACES}
    def update(self, t):
        self.act(t); hs = [_head(self.sol[k]['ch']) for k in self.FACES]; c = ((hs[0].x + hs[2].x) / 2, (hs[0].y + hs[2].y) / 2, (hs[0].z + hs[1].z + hs[2].z) / 3)
        u = clamp((t - (E['E14_faces'][0] - .2)) / 1.9)
        spec = dict(pos=(c[0] - .3 - .25 * u, c[1] - lerp(3.0, 2.5, smoother(u)), c[2] - .05), look=(c[0] + .1, c[1], c[2]), fov=lerp(46, 40, u), roll=-.05 + .04 * u)
        apply_cam(self.cam, spec, focus=lerp(3.0, 2.5, smoother(u)), fstop=2.0)
# ------------------------------------------------------------------ VIRADA (portado: S5 do piloto): o almirante recusa
class Deck(Base):
    id = 'Deck'
    def keys_(self): return {'baynes': self.b.head, 'aide': self.a.head}
    def build(self):
        self.d = deck.build('bright'); self.b = char.Char('baynes', LOOKS['baynes']); self.a = char.Char('aide', LOOKS['aide']); self.sg = props.spyglass(); self.a.attach('R', self.sg, (0, 0, -.12), (0, math.pi, 0)); sets.S5()
    def act(self, t):
        s0 = E['E23_deck'][0]; tr = W('L8', 'recusou') - .1; b = idle(t, x=0.75, y=0, z=0, face=-1); b.update(eye='lid', lid=.58, brows=(.15, .15), mouth='line', armL=(.2, .5))
        if t > tr: b = stop_hand(t, b, tr)
        a = idle(t, x=-.95, y=.3, z=0, face=1, off=1.0); a.update(eye='wide', brows=(.6, .6), mouth='shout', open=.6, armR=(lerp(-.1, 2.2, keys(t, [(s0, 0), (s0 + .4, 1)], ease_inout)), .1))
        if t > tr + .25: a = shock(t, dict(a, armR=(.3, .3), mouth='oh'), tr + .25)
        self.b.pose(b); self.a.pose(a); self.sg.hide_render = self.sg.hide_viewport = t > tr + .25
        for o in self.sg.children: o.hide_render = o.hide_viewport = t > tr + .25
    def update(self, t):
        self.act(t); a = E['E23_deck'][0]; b = E['E24_baynes'][1]
        spec = cam_at(t, [dict(t=a - .2, pos=(.5, -4.9, .62), look=(-.1, 0, 1.45), fov=55, roll=-.1), dict(t=W('L8', 'recusou') + .2, pos=(.3, -4.5, .8), look=(-.1, 0, 1.5), fov=53, roll=-.07), dict(t=b + .3, pos=(.35, -4.4, .95), look=(.0, 0, 1.6), fov=51, roll=-.04)])
        apply_cam(self.cam, spec, focus=math.dist(spec['pos'], (0, 0, 1.4)), fstop=2.8)
class I_Baynes(Deck):
    """close no almirante: pálpebra pesada, a mão de "pare" no quadro"""
    id = 'Deck'
    def focus_(self): return {'baynes': self.b.head}
    def update(self, t):
        self.act(t); hp = _head(self.b); u = clamp((t - (E['E24_baynes'][0] - .2)) / 1.6)
        dist = lerp(2.2, 1.7, smoother(u)); spec = dict(pos=(hp.x + .12 - .08 * u, hp.y - dist, hp.z - .1), look=(hp.x - .02, hp.y, hp.z - .2), fov=lerp(42, 38, u), roll=-.08 + .05 * u)
        apply_cam(self.cam, spec, focus=dist, fstop=2.2)
# ------------------------------------------------------------------ PAYOFF + LOOP (portado: S6 do piloto): túmulo do porco
class Grave(Base):
    id = 'Grave'
    def keys_(self): return {'cutlar': self.cut.head, 'griffin': self.gr.head, 'grave': self.grave}
    def build(self):
        R = self.R; self.f = farm.build('dusk', grass_n=R['grass']); self.cut = char.Char('cutlar', LOOKS['cutlar']); self.gr = char.Char('griffin', LOOKS['griffin']); self.grave = props.grave(PIG0); sets.S6(); self.smk = sets.chimney(); self.birds = sets.Birds(5, 11, (-30, 150, 44))
        self.hat1 = self._hat('#e8c068'); self.hat2 = self._hat('#8c7a58')
    def _hat(self, c):
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=.2, depth=.02); o = bpy.context.object; o.scale = (1, 1, 1); o.data.materials.append(char.mat('hatprop_' + c, char.hexc(c), emit=.28)); return o
    def update(self, t):
        self.birds.update(t); sets.drift_clouds(self.f, t)
        a, b = E['E34_grave']; self.smk.update(t); th = W('L12', 'mortos') - .12; k = keys(t, [(th, 0), (th + .3, 1)], ease_inout)
        for ch, (x, face, off) in ((self.cut, (.55, 1, .3)), (self.gr, (2.05, -1, .9))):
            p = idle(t, x=x, y=-2.2, z=gz(x, -2.2), face=face, off=off); p.update(armR=(lerp(p['armR'][0], .95, k), lerp(p['armR'][1], 2.2, k)), tilt=p['tilt'] + .12 * k, mouth='frown', lid=.6, brows=(-.3, -.3), angry=-.5); ch.pose(p)
        for h, ch in ((self.hat1, self.cut), (self.hat2, self.gr)):
            h.hide_render = h.hide_viewport = t < th + .1; bpy.context.view_layer.update(); hd = ch.arm['R'][2]; h.location = hd.matrix_world @ Vector((0, 0, -.1 * U)); h.rotation_euler = (math.radians(90), 0, 0)
        pts6 = [(.55, -2.2), (2.05, -2.2), PIG0]
        spec = cam_at(t, [dict(t=a - .2, pos=(1.9, -5.6, .65), look=aim_between((1.9, -5.6), pts6, .9), fov=54), dict(t=TOTAL - .3, pos=CAM_LOOP['pos'], look=aim_between(CAM_LOOP['pos'], pts6, .95), fov=CAM_LOOP['fov']), dict(t=999, pos=CAM_LOOP['pos'], look=aim_between(CAM_LOOP['pos'], pts6, .95), fov=CAM_LOOP['fov'])])
        apply_cam(self.cam, spec, focus=math.dist(spec['pos'], (.9, .2, .8)), fstop=2.3)
# ------------------------------------------------------------------ registro: classe de cena (campo "scene" da EDL) → classe Python
CLASSES = {'Hook': Hook, 'PigIn': PigIn, 'I_Garden': I_Garden, 'I_Again': I_Again, 'I_Eyes': I_Eyes, 'I_PigDead': I_PigDead, 'Notes': Notes, 'I_Notes': I_Notes,
           'Army': Army, 'I_Rows': I_Rows, 'Fleet5': Fleet5, 'Landing': Landing, 'I_Faces': I_Faces, 'Deck': Deck, 'I_Baynes': I_Baynes, 'Grave': Grave}
try:
    from . import shots_new as _new; CLASSES.update(_new.CLASSES)      # cenas novas da versão de 60 s
except ImportError: pass
def _mk(cls, eid): return type(eid, (cls,), {'eid': eid})
SHOT_CLASSES = {eid: _mk(CLASSES[sc], eid) for eid, sc in EDIT_CLASS.items() if sc in CLASSES}
MISSING = sorted({sc for sc in EDIT_CLASS.values() if sc not in CLASSES})
