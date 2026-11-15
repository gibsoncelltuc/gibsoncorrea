"""Cenas NOVAS da versão de 60 s (abertura): Isle, I_Flags, Treaty, Claim. Mesma convenção de shots.py (build/update como função pura de t; câmera própria)."""
import bpy, math, os
from PIL import Image, ImageDraw, ImageFont
from . import util, mats, texlib, renderlib, farm, nature, char, pig, props, sets
from .anim import *
from .shots import Base, LOOKS, gz, apply_cam, aim_between, E, W, ramp, hide
from .char import U
def map_tex(path, q=False):
    """mapa pintado do Tratado de 1846: mar, continente e ilha, linha de fronteira tracejada que se bifurca em duas ao redor da ilha; q=True acrescenta o '?' vermelho"""
    w, h = 768, 480; im = Image.new('RGB', (w, h), (232, 214, 170)); d = ImageDraw.Draw(im)
    d.rectangle([14, 14, w - 14, h - 14], outline=(70, 46, 30), width=8); d.rectangle([40, 40, w - 40, h - 40], fill=(120, 170, 215), outline=(70, 46, 30), width=5)
    d.polygon([(40, 40), (330, 40), (300, 150), (340, 260), (290, 440), (40, 440)], fill=(150, 190, 110), outline=(70, 46, 30)); d.polygon([(560, 40), (728, 40), (728, 200), (650, 170), (600, 110)], fill=(150, 190, 110), outline=(70, 46, 30))
    d.ellipse([430, 250, 560, 330], fill=(206, 178, 110), outline=(70, 46, 30), width=5)
    for x in range(40, 728, 28): d.line([x, 205, x + 16, 205], fill=(150, 30, 40), width=7)
    d.line([360, 210, 390, 250, 395, 300], fill=(150, 30, 40), width=7); d.line([470, 210, 500, 240, 490, 262], fill=(150, 30, 40), width=7)
    if q:
        f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 150); d.text((452, 238), '?', fill=(200, 30, 40), font=f, stroke_width=8, stroke_fill=(40, 20, 20))
    im.save(path); return path
def quad(name, path, w, h):
    me = bpy.data.meshes.new(name); me.from_pydata([(-w / 2, 0, -h / 2), (w / 2, 0, -h / 2), (w / 2, 0, h / 2), (-w / 2, 0, h / 2)], [], [(0, 1, 2, 3)]); uv = me.uv_layers.new(name='UVMap')
    for i, p in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]): uv.data[i].uv = p
    me.materials.append(mats.cutout_img(name + '_m', path, emit=.35)); o = bpy.data.objects.new(name, me); return util.link(o)
class Isle(Base):
    """grua descendo sobre a cerca que divide a ilha: americano (Cutlar) de um lado, britânico (Griffin) do outro, ovelhas e a bandeira britânica"""
    id = 'Isle'
    def keys_(self): return {'cutlar': self.cut.head, 'griffin': self.gr.head}
    def focus_(self): return self.keys_()
    def build(self):
        R = self.R; self.f = farm.build('golden', grass_n=R['grass']); self.cut = char.Char('cutlar', LOOKS['cutlar']); self.gr = char.Char('griffin', LOOKS['griffin']); sets.S2(); self.smk = sets.chimney(); self.birds = sets.Birds(6, 5, (10, 140, 50))
        self.uk = props.Flag((12.0, 6.5, 0), 2.4, 1.5, texlib.flag_uk(), 6.5); self.us = props.Flag((-8.5, -1.2, gz(-8.5, -1.2)), 1.4, .9, texlib.flag_us(), 3.6)
    def act(self, t):
        self.birds.update(t); sets.drift_clouds(self.f, t); self.smk.update(t); self.uk.update(t); self.us.update(t)
        c = idle(t, x=-2.6, y=-2.2, z=gz(-2.6, -2.2), face=1, off=.2); c.update(eye='lid', lid=.5, mouth='line', brows=(.1, -.1)); self.cut.pose(c)
        g = idle(t, x=2.9, y=-2.2, z=gz(2.9, -2.2), face=-1, off=.8); g.update(mouth='smirk', brows=(.3, -.3), lid=.55); self.gr.pose(g)
    def update(self, t):
        self.act(t); a, b = E['E02_isle']; u = smoother(clamp((t - a + .2) / (b - a + .4))); pa = (.2, -8.2, 3.6); pb = (.5, -6.4, 1.0)
        spec = dict(pos=[lerp(pa[i], pb[i], u) for i in range(3)], look=(.1, -2.0, lerp(.6, 1.2, u)), fov=lerp(60, 55, u), roll=.04 - .03 * u); apply_cam(self.cam, spec, focus=math.dist(spec['pos'], (.1, -2.2, 1)), fstop=2.6)
class I_Flags(Isle):
    """contra-plongée nas duas bandeiras (EUA × Reino Unido), leve giro"""
    id = 'Isle'
    def focus_(self): return {}
    def build(self):
        Isle.build(self); self.uk.pole.location = (0, 0, 0)
        self.uk2 = props.Flag((2.2, 1.2, gz(2.2, 1.2)), 1.7, 1.1, texlib.flag_uk(), 4.2, flip=False); self.us2 = props.Flag((-1.0, 1.2, gz(-1.0, 1.2)), 1.7, 1.1, texlib.flag_us(), 4.2, flip=True)
    def update(self, t):
        self.act(t); self.uk2.update(t); self.us2.update(t); a, b = E['E03_flags']; u = clamp((t - a + .2) / (b - a + .4))
        spec = dict(pos=(.6 + .5 * u, -3.6, .35), look=(.6, 1.2, 3.3 + .3 * u), fov=lerp(58, 52, u), roll=.12 - .2 * u); apply_cam(self.cam, spec, focus=5.0, fstop=3.2)
class Treaty(Base):
    """close de cima no mapa do tratado (um barril ao fundo): a fronteira se divide e aparece o '?' sobre a ilha"""
    id = 'Treaty'
    def build(self):
        R = self.R; self.f = farm.build('golden', grass_n=R['grass'] // 2); sets.S3(); self.birds = sets.Birds(4, 5, (10, 140, 50))
        tdir = util.TEX; os.makedirs(tdir, exist_ok=True); self.map1 = quad('map', map_tex(os.path.join(tdir, 'map_treaty.png')), 1.6, 1.0); self.map2 = quad('map_q', map_tex(os.path.join(tdir, 'map_treaty_q.png'), True), 1.6, 1.0)
    def update(self, t):
        a, b = E['E04_treaty']; pop = keys(t, [(a, 0), (a + .35, 1)], ease_out_back); show_q = t > W('L2', 'confuso') - .05
        for o, v in ((self.map1, not show_q), (self.map2, show_q)): o.location = (5.4, -3.0, 1.0); o.scale = (.2 + .8 * pop,) * 3; o.rotation_euler = (math.radians(-6), 0, math.radians(2) + .02 * math.sin(t * 2)); hide(o, not v)
        self.birds.update(t); u = clamp((t - a + .2) / (b - a + .4)); spec = dict(pos=(5.2 - .3 * u, -6.4 + 1.1 * u, 1.35), look=(5.4, -3.0, 1.0), fov=lerp(50, 42, u), roll=-.06 + .1 * u); apply_cam(self.cam, spec, focus=math.dist(spec['pos'], (5.4, -3.0, 1.0)), fstop=2.2)
class Claim(Base):
    """cada lado jura que a ilha é sua: americano e britânico nariz com nariz, batendo o pé no chão"""
    id = 'Claim'
    def keys_(self): return {'cutlar': self.cut.head, 'griffin': self.gr.head}
    def focus_(self): return self.keys_()
    def build(self):
        R = self.R; self.f = farm.build('golden', grass_n=R['grass']); self.cut = char.Char('cutlar', LOOKS['cutlar']); self.gr = char.Char('griffin', LOOKS['griffin']); sets.S3(); self.smk = sets.chimney(); self.birds = sets.Birds(5, 7, (30, 150, 48))
    def update(self, t):
        self.birds.update(t); sets.drift_clouds(self.f, t); self.smk.update(t); a, b = E['E05_claim']; k = (t * 3.2) % 1; stomp = abs(math.sin(t * 9)) * .06; sw = ramp(t, W('L2', 'cada') - .1, .25)
        XC, XG, Y = 4.9, 6.0, -1.0
        c = idle(t, x=XC, y=Y, z=gz(XC, Y), face=1, off=.2); c.update(eye='lid', lid=.4, angry=.8, brows=(-.3, -.3), mouth='shout', open=.5, armR=(lerp(-.1, 1.0, sw), .3), bob=stomp, tilt=.1); self.cut.pose(c)
        g = idle(t, x=XG, y=Y, z=gz(XG, Y), face=-1, off=.8); g.update(eye='lid', lid=.4, angry=.8, brows=(-.3, -.3), mouth='shout', open=.5, armR=(lerp(-.1, 1.0, sw), .3), bob=stomp * .9, tilt=-.1); self.gr.pose(g)
        u = clamp((t - a + .2) / (b - a + .4)); spec = dict(pos=(5.45, -5.6 + .7 * u, .55), look=(5.45, -1.0, 1.3), fov=lerp(54, 46, u), roll=.14 - .06 * u); apply_cam(self.cam, spec, focus=math.dist(spec['pos'], (5.45, Y, 1.0)), fstop=2.2)
CLASSES = {'Isle': Isle, 'I_Flags': I_Flags, 'Treaty': Treaty, 'Claim': Claim}
