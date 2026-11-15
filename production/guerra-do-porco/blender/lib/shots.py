"""Cenas e coreografia do piloto 'A Guerra do Porco' (Blender). Cada shot: build() cria o mundo/atores; update(t) aplica poses/câmera determinísticas em t (s)."""
import bpy, math, numpy as np
from mathutils import Vector
from . import util, mats, texlib, renderlib, farm, nature, char, pig, props, ships, crowd, deck, anim, sets
from .anim import *
from .char import U
LOOKS = {
 'cutlar': dict(shirt='#ead9b4', pattern='plain', outfit='overalls', pants='#2f2a46', shoe='#5a3a2a', hat='straw', hatColor='#e8c068', hatBand='#3a6aa8', beard='#c9a06a', build=1.0, sleeve='#2f2a46'),
 'griffin': dict(shirt='#f3ead6', pattern='plain', outfit='waistcoat', trim='#8a6a3a', pants='#3a3350', shoe='#2a2030', hat='flatcap', hatColor='#8c7a58', sideburns='#c4682c', mustache='#c4682c', blush=True, build=1.18),
 'soldier': dict(shirt='#2f4f8a', pattern='uniform', shirt2='#9fb8e0', outfit='uniform', trim='#f0c250', pants='#6c8fc8', shoe='#1f1a2a', hat='kepi', hatColor='#2f4f8a', build=1.0, sleeve='#2f4f8a'),
 'baynes': dict(shirt='#24305c', pattern='plain', outfit='admiral', trim='#f0c250', pants='#2f2a46', shoe='#1a1624', hat='bicorn', sideburns='#e3dfea', mustache='#d8d4e0', build=1.15, sleeve='#24305c'),
 'aide': dict(shirt='#2a3a70', pattern='plain', outfit='uniform', trim='#f6f1e6', pants='#2f2a46', shoe='#1a1624', hat='peaked', hatColor='#24305c', blush=True, build=0.92, sleeve='#2a3a70'),
}
PIG0 = (1.1, -0.4); CUT = (-0.1, -2.5)
CAM_LOOP = dict(pos=(1.7, -6.4, 0.80), look=(0.55, -0.2, 0.95), fov=57)
def gz(x, y): return float(nature.height(x, y))
def apply_cam(cam, spec, focus=None, fstop=3.2, dof=True):
    cam.data.dof.use_dof = dof; renderlib.place_camera(cam, spec['pos'], spec['look'], fov=spec['fov'], roll=spec['roll'], focus=focus if focus is not None else math.dist(spec['pos'], spec['look']), fstop=fstop)
def aim_between(pos, pts, z=1.0):
    """direção de olhar que centraliza (em yaw) os pontos: mantém personagens dentro do quadro vertical 9:16"""
    ang = [math.atan2(p[0] - pos[0], p[1] - pos[1]) for p in pts]; yaw = (min(ang) + max(ang)) / 2; d = 8.0
    return (pos[0] + math.sin(yaw) * d, pos[1] + math.cos(yaw) * d, z)
def muzzle(rf): bpy.context.view_layer.update(); return rf.matrix_world @ Vector((0, 0, -0.9))
class Base:
    def __init__(self, R): self.R = R; self.cam = renderlib.camera(56, dof=True, fstop=3.2, focus=6.0)
    def frames(self, fps=30, pad=.2):
        a, b = SHOTS[self.id]; return range(int(round((a - (pad if self.id != 'S1' else 0)) * fps)), int(round((b + pad) * fps)))
# ------------------------------------------------------------------ S1 — gancho
class S1(Base):
    id = 'S1'
    def keys_(self): return {'cutlar': self.cut.head, 'pig': self.pig.head}
    def build(self):
        R = self.R; self.f = farm.build('golden', grass_n=R['grass']); self.fleet = ships.fleet(); self.cut = char.Char('cutlar', LOOKS['cutlar']); self.pig = pig.Pig(); self.rf = props.rifle(); self.cut.attach('R', self.rf, (0, 0, -.1))
        self.fl = props.Flash(); self.puffs = [props.Puff() for _ in range(5)]
        for o in self.fleet: self._ship_base = getattr(self, '_ship_base', {}); self._ship_base[o.name] = (tuple(o.location), tuple(o.scale))
        sets.S1()
    def update(self, t):
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
        end = SHOTS['S1'][1]
        pts = [CUT, PIG0]; p1 = (1.9, -6.3, .72)
        spec = cam_at(t, [dict(t=0, pos=CAM_LOOP['pos'], look=aim_between(CAM_LOOP['pos'], pts, .95), fov=CAM_LOOP['fov']), dict(t=1.5, pos=p1, look=aim_between(p1, pts, .9), fov=55), dict(t=2.3, pos=(1.5, -5.2, 1.8), look=(.4, 8.0, 1.9), fov=58), dict(t=end + .3, pos=(3.2, -3.6, 5.8), look=(-2.0, 60.0, 2.2), fov=64)])
        far = clamp((t - 2.0) / 1.5); apply_cam(self.cam, spec, focus=lerp(6.4, 70, far), fstop=lerp(2.1, 8.0, far))
# ------------------------------------------------------------------ S2 — setup
class S2(Base):
    id = 'S2'
    def keys_(self): return {'cutlar': self.cut.head, 'pig': self.pig.head}
    def build(self):
        R = self.R; self.f = farm.build('golden', grass_n=R['grass']); self.cut = char.Char('cutlar', LOOKS['cutlar']); self.pig = pig.Pig(); self.rf = props.rifle(); self.cut.attach('R', self.rf, (0, 0, -.1)); self.fl = props.Flash(); self.puffs = [props.Puff() for _ in range(5)]
        self.uk = props.Flag((12.0, 6.5, 0), 2.4, 1.5, texlib.flag_uk(), 6.5)
        sets.S2(); self.smk = sets.chimney()
    def update(self, t):
        t0 = BANG2 - 1.0; tn = word_start('L2', 'horta') + .1; base = idle(t, x=CUT[0], y=CUT[1], z=gz(*CUT), face=1); c = aim_fire(t, base, t0, BANG2)
        if tn - .1 < t < t0: c = dict(shock(t, c, tn), mouth='line')
        self.cut.pose(c); self.rf.rotation_euler = (0, math.pi * (1 - aim_up(t, t0, BANG2)), 0)
        trot = clamp((t - 3.9) / (6.0 - 3.9)); px = lerp(9.6, PIG0[0], ease_inout(trot)); py = lerp(1.4, PIG0[1], ease_inout(clamp((t - 5.3) / .9)))
        self.pig.pose(dict(x=px, y=py, z=gz(px, py), face=-1, t=t, mode='trot' if trot < 1 else 'eat')); m = muzzle(self.rf); self.fl.set(t, BANG2, m, .24)
        for i, p in enumerate(self.puffs): p.set(t, BANG2 + .05 + i * .07, (m.x + .25 + i * .15, m.y, m.z), 1.2, .07 + i * .02, .4 + i * .1, (.5, 0))
        self.uk.update(t); self.smk.update(t)
        s = SHOTS['S2']; spec = cam_at(t, [dict(t=s[0] - .2, pos=(11.4, -3.6, .8), look=(12.0, 6.5, 5.0), fov=62, roll=.05), dict(t=4.55, pos=(12.4, -6.4, 1.0), look=(8.2, -1.8, 1.4), fov=58, roll=-.03),
                                           dict(t=word_start('L2', 'horta') + .2, pos=(6.2, -7.4, .9), look=aim_between((6.2, -7.4), [CUT, PIG0], 1.0), fov=57), dict(t=s[1] + .3, pos=CAM_LOOP['pos'], look=aim_between(CAM_LOOP['pos'], [CUT, PIG0], .95), fov=CAM_LOOP['fov'], roll=.05)])
        apply_cam(self.cam, spec, focus=math.dist(spec['pos'], (px, py, 1.0)) if t > 4.5 else 9.0, fstop=2.4)
# ------------------------------------------------------------------ S3 — o zombador
class S3(Base):
    id = 'S3'
    def keys_(self): return {'cutlar': self.cut.head, 'griffin': self.gr.head, 'pig': self.pig.head}
    def build(self):
        R = self.R; self.f = farm.build('golden', grass_n=R['grass']); self.cut = char.Char('cutlar', LOOKS['cutlar']); self.gr = char.Char('griffin', LOOKS['griffin']); self.pig = pig.Pig()
        self.n100 = props.note('$100', .6); self.n10 = props.note('$10', .42); self.gr.attach('R', self.n100, (0.28, 0, -.1)); self.cut.attach('R', self.n10, (0.2, 0, -.1)); sets.S3(); self.smk = sets.chimney()
    def update(self, t):
        XC, XG, XP, Y = 4.7, 6.1, 5.4, -1.0; s = SHOTS['S3']; self.smk.update(t)
        tcem = word_start('L3', 'cem') - .35; tdez = word_start('L3', 'ofereceu') - .2; tlaugh = word_start('L3', 'dez') - .05
        g = smug(idle(t, x=XG, y=Y, z=gz(XG, Y), face=-1, off=.7)); gu = keys(t, [(tcem, 0), (tcem + .3, 1)], ease_inout)
        g.update(armR=(lerp(-.1, 1.75, gu), lerp(.12, .9, gu)), armL=(lerp(.1, 1.3, keys(t, [(s[0] + .3, 0), (s[0] + .6, 1)], ease_inout)), .1))
        if t > tlaugh: g = laugh(t, g, .8)
        c = idle(t, x=XC, y=Y, z=gz(XC, Y), face=1, off=.2); cu = keys(t, [(tdez, 0), (tdez + .3, 1)], ease_inout)
        c.update(eye='lid', lid=.35, angry=.7, brows=(-.2, -.2), mouth='teeth', armR=(lerp(-.1, 1.6, cu), lerp(.12, .8, cu)), sweat=(t - tdez) * 1.1 if t > tdez else 0)
        self.gr.pose(g); self.cut.pose(c); self.pig.pose(dict(x=XP, y=Y + .5, z=gz(XP, Y + .5), face=1, t=t, mode='dead', flip=1))
        for n, ch, look, p in ((self.n100, g, LOOKS['griffin'], self.gr), (self.n10, c, LOOKS['cutlar'], self.cut)):
            ang = ch['armR'][0] + ch['armR'][1] + ch['lean']; n.rotation_euler = (0, ang + (.1 if ch is g else -.12), 0); n.scale = (-1 if ch['face'] < 0 else 1, 1, 1)
        self.n100.hide_render = self.n100.hide_viewport = t < tcem; self.n10.hide_render = self.n10.hide_viewport = t < tdez
        spec = cam_at(t, [dict(t=s[0] - .2, pos=(5.4, -6.4, .6), look=(5.4, -1.0, 1.15), fov=54, roll=.12), dict(t=s[1] + .3, pos=(5.4, -5.2, .9), look=(5.4, -1.0, 1.25), fov=50, roll=.08)])
        apply_cam(self.cam, spec, focus=math.dist(spec['pos'], (5.35, Y, 1.0)), fstop=2.3)
# ------------------------------------------------------------------ S4 — escalada (soldados e navios)
class S4(Base):
    id = 'S4'
    def keys_(self): return {'lead': self.lead.head, 'sol0': self.sol[0]['ch'].head, 'sol20': self.sol[20]['ch'].head, 'fleet': self.fleet[2]}
    def build(self):
        R = self.R; self.f = farm.build('golden', grass_n=R['grass'] // 2, grass_areas=[((-42, -4, 16, 40), R['grass'])]); self.fleet = ships.fleet(); self.sol = crowd.block(10, 8); self.bearer = crowd.add_bearer(self.sol, 23); self.lead = char.Char('lead', LOOKS['soldier'])
        for o in self.f['trees']: o.visible_shadow = False   # abetos a oeste (|x|>38) projetavam sombra longa e escura (sol a 24°) sobre o campo desta cena
        for tp in [(-34, 38.5, 1.2, .2), (-27, 40.5, 1.1, -.3), (-41, 37.5, 1.0, .5)]: props.tent((tp[0], tp[1], gz(tp[0], tp[1])), tp[2], tp[3])
        self.us = props.Flag((-33, 42.0, gz(-33, 42)), 2.2, 1.4, texlib.flag_us(), 6.0); cn = props.cannon(); cn.location = (-22, 36, gz(-22, 36)); cn.rotation_euler = (0, 0, math.radians(75))
        self._ship_base = {o.name: (tuple(o.location), tuple(o.scale)) for o in self.fleet}; sets.S4()
    def update(self, t):
        s = SHOTS['S4']; bx = -24 + 2.45 * (t - s[0]); crowd.place_block(self.sol, bx, 27.2, t); self.us.update(t); self.bearer.update(t)
        ld = idle(t, x=bx + 0.3, y=25.2, z=gz(bx + 0.3, 25.2), face=1); ld.update(march(t)); ld.update(eye='lid', lid=.4, angry=.3, brows=(.1, .1), mouth='line', armR=(.3, .2)); self.lead.pose(ld)
        tn = word_start('L4', 'navios') - .5; u = smoother((t - tn) / 1.0); fu = smoother((t - (tn - .45)) / 1.0)
        for o in self.fleet: loc, sc = self._ship_base[o.name]; o.hide_render = o.hide_viewport = fu < .01; k = .15 + .85 * fu; o.scale = (sc[0] * k, sc[1] * k, sc[2] * k); o.location = (loc[0], loc[1] + 35 * (1 - fu), loc[2])
        a = dict(pos=(bx - 1.2, 21.0, .62), look=(bx + 1.4, 29.0, 1.25), fov=60); b = dict(pos=(bx - .2, 21.4, 3.6), look=(8.0, 78.0, 2.6), fov=58)
        spec = dict(pos=[lerp(a['pos'][i], b['pos'][i], u) for i in range(3)], look=[lerp(a['look'][i], b['look'][i], u) for i in range(3)], fov=lerp(a['fov'], b['fov'], u), roll=.02)
        apply_cam(self.cam, spec, focus=lerp(6.0, 70.0, u), fstop=lerp(2.8, 8.0, u))
# ------------------------------------------------------------------ S5 — o almirante recusa
class S5(Base):
    id = 'S5'
    def keys_(self): return {'baynes': self.b.head, 'aide': self.a.head}
    def build(self):
        self.d = deck.build('bright'); self.b = char.Char('baynes', LOOKS['baynes']); self.a = char.Char('aide', LOOKS['aide']); self.sg = props.spyglass(); self.a.attach('R', self.sg, (0, 0, -.12), (0, math.pi, 0)); sets.S5()
    def update(self, t):
        s = SHOTS['S5']; tr = word_start('L5', 'recusou') - .1; b = idle(t, x=0.75, y=0, z=0, face=-1); b.update(eye='lid', lid=.58, brows=(.15, .15), mouth='line', armL=(.2, .5))
        if t > tr: b = stop_hand(t, b, tr)
        a = idle(t, x=-.95, y=.3, z=0, face=1, off=1.0); a.update(eye='wide', brows=(.6, .6), mouth='shout', open=.6, armR=(lerp(-.1, 2.2, keys(t, [(s[0], 0), (s[0] + .4, 1)], ease_inout)), .1))
        if t > tr + .25: a = shock(t, dict(a, armR=(.3, .3), mouth='oh'), tr + .25)
        self.b.pose(b); self.a.pose(a); self.sg.hide_render = self.sg.hide_viewport = t > tr + .25
        spec = cam_at(t, [dict(t=s[0] - .2, pos=(.5, -5.6, .62), look=(-.1, 0, 1.45), fov=55, roll=-.1), dict(t=word_start('L5', 'recusou') + .2, pos=(.3, -5.0, .8), look=(-.1, 0, 1.5), fov=53, roll=-.07), dict(t=s[1] + .3, pos=(.2, -4.5, .95), look=(-.1, 0, 1.6), fov=51, roll=-.04)])
        apply_cam(self.cam, spec, focus=math.dist(spec['pos'], (0, 0, 1.4)), fstop=2.8)
# ------------------------------------------------------------------ S6 — túmulo (loop com o 1º quadro)
class S6(Base):
    id = 'S6'
    def keys_(self): return {'cutlar': self.cut.head, 'griffin': self.gr.head, 'grave': self.grave}
    def build(self):
        R = self.R; self.f = farm.build('dusk', grass_n=R['grass']); self.cut = char.Char('cutlar', LOOKS['cutlar']); self.gr = char.Char('griffin', LOOKS['griffin']); self.grave = props.grave(PIG0); sets.S6(); self.smk = sets.chimney()
        from . import props as P; self.hat1 = self._hat('#e8c068'); self.hat2 = self._hat('#8c7a58')
    def _hat(self, c):
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=.2, depth=.02); o = bpy.context.object; o.scale = (1, 1, 1); o.data.materials.append(char.mat('hatprop_' + c, char.hexc(c), emit=.28)); return o
    def update(self, t):
        s = SHOTS['S6']; self.smk.update(t); th = word_start('L5', 'só') - .15; k = keys(t, [(th, 0), (th + .3, 1)], ease_inout)
        for ch, (x, face, off), look in ((self.cut, (.55, 1, .3), LOOKS['cutlar']), (self.gr, (2.05, -1, .9), LOOKS['griffin'])):
            p = idle(t, x=x, y=-2.2, z=gz(x, -2.2), face=face, off=off); p.update(armR=(lerp(p['armR'][0], .95, k), lerp(p['armR'][1], 2.2, k)), tilt=p['tilt'] + .12 * k, mouth='frown', lid=.6, brows=(-.3, -.3), angry=-.5); ch.pose(p)
        for h, ch in ((self.hat1, self.cut), (self.hat2, self.gr)):
            h.hide_render = h.hide_viewport = t < th + .1; bpy.context.view_layer.update(); hd = ch.arm['R'][2]; h.location = hd.matrix_world @ Vector((0, 0, -.1 * U)); h.rotation_euler = (math.radians(90), 0, 0)
        pts6 = [(.55, -2.2), (2.05, -2.2), PIG0]
        spec = cam_at(t, [dict(t=s[0] - .2, pos=(1.9, -5.6, .65), look=aim_between((1.9, -5.6), pts6, .9), fov=54), dict(t=TOTAL - .3, pos=CAM_LOOP['pos'], look=aim_between(CAM_LOOP['pos'], pts6, .95), fov=CAM_LOOP['fov']), dict(t=999, pos=CAM_LOOP['pos'], look=aim_between(CAM_LOOP['pos'], pts6, .95), fov=CAM_LOOP['fov'])])
        apply_cam(self.cam, spec, focus=math.dist(spec['pos'], (.9, .2, .8)), fstop=2.3)
SHOT_CLASSES = {'S1': S1, 'S2': S2, 'S3': S3, 'S4': S4, 'S5': S5, 'S6': S6}
