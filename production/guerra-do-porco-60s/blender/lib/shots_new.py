"""Cenas NOVAS da versão de 60 s (abertura): Isle, I_Flags, Treaty, Claim. Mesma convenção de shots.py (build/update como função pura de t; câmera própria)."""
import bpy, math, os
from PIL import Image, ImageDraw, ImageFont
from . import util, mats, texlib, renderlib, farm, nature, char, pig, props, sets
from .anim import *
from .shots import Base, LOOKS, gz, apply_cam, aim_between, E, W, ramp, hide, _head, STAMP
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
# =================================================================== CENAS DA ESCALADA, VIRADA, RESOLUÇÃO E PAYOFF
from . import ships, crowd, deck, dress as D
from .shots import Landing, Army
def _chars(self, names): 
    for n in names: setattr(self, 'c_' + n, char.Char(n, LOOKS[n]))
def _field(self, grass=None): self.f = farm.build('golden', grass_n=grass or self.R['grass']); self.birds = sets.Birds(5, 7, (30, 150, 48))
class Ships3(Base):
    """'os britânicos respondem com três navios' — rente à água, a câmera sobe e revela os cascos em linha"""
    id = 'Ships3'
    def focus_(self): return {}
    def build(self): _field(self); self.fleet = ships.fleet(); sets.S1()
    def update(self, t):
        self.birds.update(t); sets.drift_clouds(self.f, t); a, b = E['E15_ships3']; u = smoother(clamp((t - a + .2) / (b - a + .4)))
        for i, o in enumerate(self.fleet): o.hide_render = o.hide_viewport = i >= 3 + (1 if t > a + .8 else 0) * 0
        spec = dict(pos=(-6 + 3 * u, 14, lerp(.5, 2.6, u)), look=(-8 + 4 * u, 70, lerp(2.0, 4.5, u)), fov=lerp(58, 62, u), roll=.04 - .06 * u); apply_cam(self.cam, spec, focus=60, fstop=6)
class I_Ports(Ships3):
    id = 'Ships3'
    def update(self, t):
        self.birds.update(t); sets.drift_clouds(self.f, t); a, b = E['E16_ports']; u = clamp((t - a + .2) / (b - a + .4)); sh = self.fleet[1]; p = sh.location
        for i, o in enumerate(self.fleet): o.hide_render = o.hide_viewport = i >= 3
        spec = dict(pos=(p.x + 7.5 - 3 * u, p.y - 9.5, 2.0), look=(p.x + 1 - 5 * u, p.y, 2.2), fov=50, roll=-.08 + .05 * u); apply_cam(self.cam, spec, focus=12, fstop=3.5)
class Marines(Base):
    """'com mais de dois mil homens' — convés lotado de fuzileiros de casaca vermelha; a câmera recua revelando a massa"""
    id = 'Marines'
    def build(self):
        self.d = deck.build('bright'); self.sol = crowd.block(9, 5, seed=21, nation='uk', prefix='m', rifles=True); sets.S5()
    def update(self, t):
        a, b = E['E20_marines']; u = clamp((t - a + .2) / (b - a + .4)); crowd.place_block(self.sol, 0, -2.2, t, cols=9, rows=5, sx=.95, sy=.85, face=1, mode='idle', gz=0.0)
        spec = dict(pos=(.2 + 1.2 * u, -8.6 + -3.0 * u, .8 + .9 * u), look=(0, 1.0, 1.3), fov=lerp(56, 60, u), roll=.05 - .07 * u); apply_cam(self.cam, spec, focus=9, fstop=3.2)
class Governor(Base):
    id = 'Governor'
    def keys_(self): return {'governor': self.g.head}
    def focus_(self): return self.keys_()
    def build(self): self.d = deck.build('bright'); self.g = char.Char('governor', LOOKS['governor']); self.a = char.Char('aide', LOOKS['aide']); sets.S5()
    def act(self, t):
        a, b = E['E21_governor']; pt = ramp(t, a + .15, .3, ease_out_back); g = idle(t, x=.7, y=0, z=0, face=-1); g.update(eye='lid', lid=.45, angry=.9, brows=(-.4, -.4), mouth='shout', open=.7, armR=(lerp(-.1, 2.0, pt), lerp(.1, -.1, pt)), bob=abs(math.sin(t * 8)) * .04 if t > a else 0); self.g.pose(g)
        ad = idle(t, x=-1.0, y=.3, z=0, face=1, off=1.0); tg = E['E22_gulp'][0]; ad.update(eye='wide' if t > tg else 'lid', brows=(.6, .6), mouth='oh' if t > tg else 'line', sweat=(t - tg) * 1.3 if t > tg else 0, squash=.06 * math.sin(clamp((t - tg) / .4) * math.pi)); self.a.pose(ad)
    def update(self, t):
        self.act(t); a, b = E['E21_governor']; u = clamp((t - a + .2) / (b - a + .4)); spec = dict(pos=(.6 - .3 * u, -5.2 + 1.1 * u, .45), look=(.1, 0, 1.55), fov=lerp(56, 48, u), roll=-.1 + .05 * u); apply_cam(self.cam, spec, focus=4.2, fstop=2.6)
class I_Gulp(Governor):
    id = 'Governor'
    def focus_(self): return {'aide': self.a.head}
    def update(self, t):
        self.act(t); hp = _head(self.a); a, b = E['E22_gulp']; u = clamp((t - a + .2) / (b - a + .4)); dist = lerp(2.3, 1.8, smoother(u)); spec = dict(pos=(hp.x + .15, hp.y - dist, hp.z - .05), look=(hp.x, hp.y, hp.z - .1), fov=lerp(44, 38, u), roll=.06 - .04 * u); apply_cam(self.cam, spec, focus=dist, fstop=2.2)
class Arrest(Base):
    """britânicos (cartola e fuzileiro de casaca vermelha) ameaçam prender o Cutlar; algemas balançam"""
    id = 'Arrest'
    def keys_(self): return {'cutlar': self.cut.head, 'official': self.o1.head}
    def focus_(self): return self.keys_()
    def build(self):
        _field(self); self.cut = char.Char('cutlar', LOOKS['cutlar']); self.o1 = char.Char('official', LOOKS['official']); self.o2 = char.Char('marine', LOOKS['marine']); sets.S3()
        bpy.ops.mesh.primitive_torus_add(major_radius=.09, minor_radius=.016); self.cuff = bpy.context.object; self.cuff.data.materials.append(mats.flat('cuff', (.1, .1, .12, 1), metallic=.8, haze=False)); self.o1.attach('R', self.cuff, (.12, 0, -.05)) if False else None
    def update(self, t):
        self.birds.update(t); sets.drift_clouds(self.f, t); a, b = E['E12_arrest']; pt = ramp(t, a + .1, .3, ease_out_back); Y = -1.0
        c = idle(t, x=4.6, y=Y, z=gz(4.6, Y), face=1, off=.2); c.update(eye='wide', brows=(.9, .9), mouth='oh', sweat=(t - a) * 1.2, armR=(.9, 1.4), armL=(.9, 1.4)); self.cut.pose(c)
        o = idle(t, x=6.3, y=Y + .2, z=gz(6.3, Y), face=-1, off=.5); o.update(angry=.7, brows=(-.3, -.3), mouth='shout', open=.5, armR=(lerp(-.1, 1.8, pt), .1)); self.o1.pose(o)
        m = idle(t, x=7.5, y=Y - .1, z=gz(7.5, Y), face=-1, off=.9); m.update(angry=.6, brows=(-.2, -.2), mouth='line', armR=(lerp(-.1, 1.5, pt), .2)); self.o2.pose(m)
        u = clamp((t - a + .2) / (b - a + .4)); spec = dict(pos=(6.0 - .4 * u, -5.6 + .8 * u, .4), look=(6.0, -1.0, 1.5), fov=lerp(56, 50, u), roll=-.1 + .06 * u); apply_cam(self.cam, spec, focus=4.6, fstop=2.4)
class Standoff(Base):
    """azul e vermelho frente a frente baixam os fuzis (perfil)"""
    id = 'Standoff'
    def keys_(self): return {'us': self.us.head, 'uk': self.uk.head}
    def focus_(self): return self.keys_()
    def build(self):
        _field(self); self.us = char.Char('us', LOOKS['soldier']); self.uk = char.Char('uk', LOOKS['marine']); self.r1 = props.rifle(); self.r2 = props.rifle(); self.us.attach('R', self.r1, (0, 0, -.1), (0, math.pi + 1.1, 0)); self.uk.attach('R', self.r2, (0, 0, -.1), (0, math.pi + 1.1, 0)); sets.S3()
    def update(self, t):
        self.birds.update(t); sets.drift_clouds(self.f, t); a, b = E['E26_standoff']; lo = ramp(t, a + .5, .5); Y = -1.0
        for ch, x, f, r in ((self.us, 4.7, 1, self.r1), (self.uk, 6.0, -1, self.r2)):
            p = idle(t, x=x, y=Y, z=gz(x, Y), face=f, off=.3 * f); p.update(eye='lid', lid=.45, brows=(lerp(-.3, .2, lo), lerp(-.3, .2, lo)), angry=lerp(.7, 0, lo), mouth='line', armR=(lerp(1.5, .4, lo), .3)); ch.pose(p)
        u = clamp((t - a + .2) / (b - a + .4)); spec = dict(pos=(5.35, -5.2 + .8 * u, .6), look=(5.35, -1.0, 1.3), fov=lerp(52, 46, u), roll=.05); apply_cam(self.cam, spec, focus=4.2, fstop=2.3)
class I_Plant(Standoff):
    id = 'Standoff'
    def build(self):
        Standoff.build(self); self.fl1 = props.Flag((4.1, -.2, gz(4.1, -.2)), .9, .6, texlib.flag_us(), 2.2); self.fl2 = props.Flag((6.6, -.2, gz(6.6, -.2)), .9, .6, texlib.flag_uk(), 2.2, flip=True)
        for o in (self.r1, self.r2): hide(o)
    def update(self, t):
        self.birds.update(t); sets.drift_clouds(self.f, t); self.fl1.update(t); self.fl2.update(t); a, b = E['E28_plant']; nod = math.sin(clamp((t - (a + .9)) / .5) * math.pi) * .25; Y = -1.0
        for ch, x, f in ((self.us, 4.7, 1), (self.uk, 6.0, -1)): p = idle(t, x=x, y=Y, z=gz(x, Y), face=f, off=.3 * f); p.update(mouth='smile', tilt=nod * f, armR=(.9, 1.2)); ch.pose(p)
        u = clamp((t - a + .2) / (b - a + .4)); spec = dict(pos=(5.35 + .4 * u, -4.6, .55), look=(5.35, -.6, 1.2), fov=lerp(54, 48, u), roll=-.06 + .05 * u); apply_cam(self.cam, spec, focus=4.0, fstop=2.4)
class Camps(Base):
    """grua descendo sobre a cerca: um acampamento de cada lado, cada um com sua bandeira"""
    id = 'Camps'
    def build(self):
        _field(self); sets.S3()
        for i, x in enumerate((-1.6, -.2, -2.4)): props.tent((x, -1.0 + i * 2.0, gz(x, -1.0)), .8, .2 * i)
        for i, x in enumerate((6.2, 7.6, 5.4)): props.tent((x, -1.0 + i * 2.0, gz(x, -1.0)), .8, -.2 * i)
        self.us = props.Flag((-1.2, 3.6, gz(-1.2, 3.6)), 1.2, .8, texlib.flag_us(), 4.0); self.uk = props.Flag((6.4, 3.6, gz(6.4, 3.6)), 1.2, .8, texlib.flag_uk(), 4.0)
    def update(self, t):
        self.birds.update(t); sets.drift_clouds(self.f, t); self.us.update(t); self.uk.update(t); a, b = E['E27_camps']; u = smoother(clamp((t - a + .2) / (b - a + .4)))
        spec = dict(pos=(2.6, lerp(-12, -8, u), lerp(8, 3.0, u)), look=(2.6, 2.0, lerp(0, .9, u)), fov=lerp(56, 58, u), roll=.03); apply_cam(self.cam, spec, focus=18, fstop=4)
class Visit(Base):
    """fuzileiros vermelhos atravessam a porteira com um barril; os azuis acenam"""
    id = 'Visit'
    def build(self):
        _field(self); self.red = crowd.block(3, 2, seed=31, nation='uk', prefix='r', rifles=False); self.blue = crowd.block(3, 2, seed=32, prefix='b', rifles=False); sets.S3(); self.barrel = None
    def update(self, t):
        self.birds.update(t); sets.drift_clouds(self.f, t); a, b = E['E29_visit']; u = (t - a) / (b - a)
        crowd.place_block(self.red, 1.2 + 4 * u, -2.2, t, cols=3, rows=2, sx=1.0, sy=.9, face=1, mode='march'); crowd.place_block(self.blue, 6.0, -.4, t, cols=3, rows=2, sx=1.0, sy=.9, face=-1, mode='idle')
        for it in self.blue: it['over'] = (lambda t_, d: dict(armL=(1.9 + .3 * math.sin(t_ * 9), .2)))
        spec = dict(pos=(-1.0 + 6 * u, -6.0, .75), look=(1.5 + 6 * u, -1.0, 1.1), fov=56, roll=-.03); apply_cam(self.cam, spec, focus=5.5, fstop=2.6)
class Party(Base):
    """noite: azuis e vermelhos em volta da fogueira, canecas no ar"""
    id = 'Party'
    def build(self):
        self.f = farm.build('dusk', grass_n=self.R['grass']); self.birds = sets.Birds(2, 3, (30, 150, 48)); D.campfire(5.4, -1.0); D.lantern(3.6, -2.4); D.lantern(7.4, 0.6); D.barrel(8.2, -2.2, label='RUM', seed=9); sets.S3()
        self.cs = [char.Char(f'p{i}', LOOKS['marine' if i % 2 else 'soldier']) for i in range(6)]
    def update(self, t):
        self.birds.update(t); sets.drift_clouds(self.f, t); a, b = E['E30_party']
        for i, ch in enumerate(self.cs):
            ang = i / 6 * 2 * math.pi + .3; x = 5.4 + 1.6 * math.cos(ang); y = -1.0 + 1.1 * math.sin(ang) - 1.0; p = idle(t, x=x, y=y, z=gz(x, y), face=-1 if math.cos(ang) > 0 else 1, off=i * .4)
            p.update(eye='arc', mouth='laugh', open=.5 + .5 * abs(math.sin(t * 6 + i)), brows=(.6, .6), armR=(1.7 + .3 * math.sin(t * 5 + i), .5), bob=abs(math.sin(t * 6 + i)) * .06); ch.pose(p)
        u = clamp((t - a + .2) / (b - a + .4)); th = lerp(-.5, .5, u); spec = dict(pos=(5.4 + 4.6 * math.sin(th), -1.0 - 4.6 * math.cos(th) - 1.0, .8), look=(5.4, -2.0, 1.1), fov=56, roll=.04); apply_cam(self.cam, spec, focus=4.6, fstop=2.4)
class Kaiser(Base):
    """gabinete do imperador: mesa com o mapa, janela; ele de costas gira para o perfil"""
    id = 'Kaiser'
    def keys_(self): return {'kaiser': self.k.head}
    def focus_(self): return self.keys_()
    def build(self):
        w = renderlib.world_gradient([(0, (.5, .38, .3, 1)), (1, (.3, .22, .2, 1))]); renderlib.sun(40, 200, (1, .85, .7), 3.0, 8)
        tex = mats.image('k_floor', texlib.wood_planks(base='#8a5a38', dark='#3a2418'), rough=.7, scale=(1 / 2.0, 1 / 2.0), coord='Object', box=True, haze=False)
        for nm, V in (('floor', [(-8, -9, 0), (8, -9, 0), (8, 6, 0), (-8, 6, 0)]), ('wall', [(-8, 2.6, 0), (8, 2.6, 0), (8, 2.6, 5), (-8, 2.6, 5)])):
            me = bpy.data.meshes.new(nm); me.from_pydata(V, [], [(0, 1, 2, 3)]); me.materials.append(tex if nm == 'floor' else mats.flat('kwall', (.55, .24, .26, 1), haze=False)); util.link(bpy.data.objects.new(nm, me))
        D.crate(0, 1.2, (3.0, 1.4, .8), 0, seed=3); self.k = char.Char('kaiser', LOOKS['kaiser']); self.map = quad('kmap', map_tex(os.path.join(util.TEX, 'map_k.png'), True), 1.5, .95); sets.S5() if False else None
        D.lantern(-3.0, 2.0, 2.2); D.lantern(3.0, 2.0, 2.2)
    def update(self, t):
        a, b = E['E31_kaiser']; k = idle(t, x=0, y=2.0, z=0, face=1); k.update(eye='lid', lid=.5, brows=(.2, .2), mouth='line', tilt=.05); self.k.pose(k); self.map.location = (0, 1.0, .85); self.map.rotation_euler = (math.radians(-50), 0, 0); self.map.scale = (1.0,) * 3
        u = clamp((t - a + .2) / (b - a + .4)); spec = dict(pos=(lerp(-1.6, -.5, u), -1.4, 1.5), look=(0, 1.8, 1.3), fov=52, roll=.04); apply_cam(self.cam, spec, focus=6.5, fstop=3.0)
class I_Kaiser(Kaiser):
    id = 'Kaiser'
    def update(self, t):
        a, b = E['E32_ikaiser']; k = idle(t, x=0, y=2.0, z=0, face=1); k.update(eye='lid', lid=.55, brows=(.2, .2), mouth='line'); self.k.pose(k); self.map.hide_render = True; hp = _head(self.k); u = clamp((t - a + .2) / (b - a + .4))
        spec = dict(pos=(hp.x + .1, hp.y - lerp(2.3, 1.7, smoother(u)), hp.z + .02), look=(hp.x, hp.y, hp.z), fov=40, roll=.05 - .05 * u); apply_cam(self.cam, spec, focus=2.0, fstop=2.0)
class I_Stamp(Kaiser):
    id = 'Kaiser'
    def build(self):
        Kaiser.build(self); bpy.ops.mesh.primitive_cube_add(size=1); self.stamp = bpy.context.object; self.stamp.scale = (.26, .26, .22); self.stamp.data.materials.append(mats.flat('stampm', (.5, .12, .14, 1), haze=False)); self.usf = props.Flag((0, 1.25, .9), .5, .32, texlib.flag_us(), .5)
    def update(self, t):
        a, b = E['E33_stamp']; self.k.pose(idle(t, x=40, y=40, z=0)); self.map.hide_render = False; self.map.location = (0, 1.0, .85); self.map.rotation_euler = (math.radians(-90), 0, 0)
        tt = ramp(t, STAMP, .12, ease_in) if 'ease_in' in globals() else ramp(t, STAMP, .12); hh = lerp(1.5, .88, ease_out(clamp((t - (STAMP - .35)) / .35))); self.stamp.location = (.25, .82, hh); self.usf.update(t); hide(self.usf.o, t < STAMP)
        spec = dict(pos=(0, .8 - 0, 3.2), look=(0, 1.0, .85), fov=44 - 4 * clamp((t - STAMP) / .4), roll=.04); apply_cam(self.cam, spec, focus=2.4, fstop=2.4)
CLASSES.update({'Ships3': Ships3, 'I_Ports': I_Ports, 'Marines': Marines, 'Governor': Governor, 'I_Gulp': I_Gulp, 'Arrest': Arrest, 'Standoff': Standoff, 'I_Plant': I_Plant, 'Camps': Camps, 'Visit': Visit, 'Party': Party, 'Kaiser': Kaiser, 'I_Kaiser': I_Kaiser, 'I_Stamp': I_Stamp})
