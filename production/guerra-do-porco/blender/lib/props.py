"""Props 3D: mosquete, notas, luneta, canhão, túmulo, fumaça/clarão de tiro, cruz, bandeira com vento."""
import bpy, math, numpy as np
from . import util, mats, texlib, char
from .char import U, hexc
from .util import mesh_np
def rifle(col=None):
    """cano ao longo de −Z local (coronha em +Z); chega a −0.9 m (boca) e +0.7 m (coronha)"""
    o = util.empty('rifle', col=col)
    bar = bpy.data.meshes.new('rb'); V, F = _boxv((0.0, 0.0, -0.1), (.04, .04, 1.6)); bar.from_pydata(V, [], F)
    b = bpy.data.objects.new('rifle_barrel', bar); b.parent = o; util.link(b, col); bar.materials.append(mats.flat('steel', (.14, .14, .17, 1), rough=.35, spec=.8, metallic=.8, haze=False))
    st = bpy.data.meshes.new('rs'); V, F = _boxv((0.0, 0.0, .45), (.09, .06, .62)); st.from_pydata(V, [], F); s = bpy.data.objects.new('rifle_stock', st); s.parent = o; util.link(s, col); st.materials.append(mats.flat('stock', (.42, .22, .10, 1), rough=.55, spec=.3, haze=False))
    for z in (-.55, -.15, .15):
        bm = bpy.data.meshes.new('rbd'); V, F = _boxv((0, 0, z), (.06, .06, .05)); bm.from_pydata(V, [], F); bo = bpy.data.objects.new('rifle_band', bm); bo.parent = o; util.link(bo, col); bm.materials.append(mats.flat('brass', (.9, .65, .2, 1), rough=.3, spec=.8, metallic=.9, haze=False))
    for ob in o.children:
        bv = ob.modifiers.new('bv', 'BEVEL'); bv.width = .004; bv.segments = 2
    return o
def _boxv(c, s):
    sx, sy, sz = s[0] / 2, s[1] / 2, s[2] / 2; V = [(c[0] + x, c[1] + y, c[2] + z) for z in (-sz, sz) for y in (-sy, sy) for x in (-sx, sx)]
    F = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]; return V, F
def note(label, w=.62, col=None):
    tex = texlib.note(label); me = bpy.data.meshes.new('note'); h = w * .5; V = [(-w / 2, 0, -h / 2), (w / 2, 0, -h / 2), (w / 2, 0, h / 2), (-w / 2, 0, h / 2)]; me.from_pydata(V, [], [(0, 1, 2, 3)]); uv = me.uv_layers.new(name='UVMap')
    for i, (u, v) in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]): uv.data[i].uv = (u, v)
    me.materials.append(mats.cutout_img('note_' + label, tex, emit=.35)); o = bpy.data.objects.new('note', me); return util.link(o, col)
def spyglass(col=None):
    o = util.empty('spyglass', col=col); brass = mats.flat('brass2', hexc('#e8b83c'), rough=.3, spec=.8, metallic=.9, haze=False)
    for i, (r, L) in enumerate([(.035, .32), (.048, .28), (.062, .2)]):
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, location=(0, 0, -.2 - i * .26)); c = bpy.context.object; c.rotation_euler = (0, 0, 0); c.data.materials.append(brass); c.parent = o; util.link(c, col) if c.name not in [x.name for x in (col or bpy.context.scene.collection).objects] else None
    return o
def cannon(col=None, scale=1.0):
    o = util.empty('cannon', col=col); iron = mats.flat('iron', (.07, .07, .09, 1), rough=.4, spec=.7, metallic=.9, haze=True); wood = mats.image('cannon_wood', texlib.logs(), rough=.85, spec=.1, bump=.5, coord='Object', scale=(1, 1), box=True, haze=True)
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=.30, radius2=.20, depth=2.3, location=(.7, 0, .78)); b = bpy.context.object; b.rotation_euler = (0, math.radians(90 - 5), 0); b.data.materials.append(iron); b.parent = o
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=.27, depth=.1, location=(1.88, 0, .84)); r = bpy.context.object; r.rotation_euler = (0, math.radians(85), 0); r.data.materials.append(iron); r.parent = o
    V, F = _boxv((-.1, 0, .35), (1.7, .6, .28)); me = bpy.data.meshes.new('carriage'); me.from_pydata(V, [], F); c = bpy.data.objects.new('carriage', me); me.materials.append(wood); c.parent = o; bv = c.modifiers.new('bv', 'BEVEL'); bv.width = .02; bv.segments = 2
    for y in (.42, -.42):
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=.5, depth=.12, location=(-.05, y, .5)); w = bpy.context.object; w.rotation_euler = (math.radians(90), 0, 0); w.data.materials.append(wood); w.parent = o
    for ob in o.children:
        if ob.name not in [x.name for x in (col or bpy.context.scene.collection).objects]: util.link(ob, col)
    o.scale = (scale,) * 3; return o
def grave(p, col=None):
    x, y = p; o = util.empty('grave', (x, y, 0), col=col); o.scale = (1.7, 1.7, 1.7); soil = mats.image('grave_soil', texlib.soil(), rough=.95, spec=.05, bump=.6, coord='Object', scale=(1, 1), box=True)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=.5, location=(0, 0, 0.02)); m = bpy.context.object; m.scale = (.9, .5, .2); m.data.materials.append(soil); m.parent = o
    wood = mats.image('cross_wood', texlib.wood_planks(), rough=.85, spec=.1, bump=.4, coord='Object', scale=(1, 1), box=True)
    for (c, s) in (((0, .35, .42), (.07, .05, .85)), ((0, .35, .62), (.4, .05, .07))):
        V, F = _boxv(c, s); me = bpy.data.meshes.new('cross'); me.from_pydata(V, [], F); ob = bpy.data.objects.new('cross', me); me.materials.append(wood); ob.parent = o; bv = ob.modifiers.new('bv', 'BEVEL'); bv.width = .008; bv.segments = 2; util.link(ob, col)
    for (dx, dy, c) in ((-.45, -.2, '#ff7aa0'), (.42, -.18, '#ffd24a'), (.05, -.42, '#ff9a4a'), (-.15, .1, '#f7f2e8')):
        bpy.ops.mesh.primitive_cylinder_add(radius=.008, depth=.28, location=(dx, dy, .14)); st = bpy.context.object; st.data.materials.append(mats.flat('stem', (.2, .45, .12, 1), haze=True)); st.parent = o
        bpy.ops.mesh.primitive_uv_sphere_add(radius=.06, location=(dx, dy, .3)); fl = bpy.context.object; fl.scale = (1, .6, 1); fl.data.materials.append(mats.flat('petal_' + c, hexc(c), rough=.7, emit=hexc(c), emit_s=.25, haze=True)); fl.parent = o
    for ob in o.children:
        if ob.name not in [x.name for x in (col or bpy.context.scene.collection).objects]: util.link(ob, col)
    return o
class Puff:
    """baforada de fumaça: esfera translúcida que cresce e some"""
    def __init__(self, col=None):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=1.0); self.o = bpy.context.object; self.o.name = 'puff'; m, nt, out = mats._new('puff_m'); b = mats._bsdf(nt, (.62, .60, .66, 1), 1.0, 0.0, 0.0, (.55, .54, .6, 1), .25); mats.finish(m, nt, out, b.outputs['BSDF'], False); self.b = b; self.o.data.materials.append(m); self.o.visible_shadow = False
        for p in self.o.data.polygons: p.use_smooth = True
        if col is not None: util.link(self.o, col)
    def set(self, t, t0, pos, dur=1.6, r=.12, rise=.9, drift=(.3, 0)):
        u = (t - t0) / dur
        if u < 0 or u > 1: self.o.hide_render = self.o.hide_viewport = True; return
        self.o.hide_render = self.o.hide_viewport = False; self.o.location = (pos[0] + drift[0] * u, pos[1] + drift[1] * u, pos[2] + rise * u); s = r * (.5 + 1.8 * math.sqrt(u)); self.o.scale = (s, s, s); self.b.inputs['Alpha'].default_value = .8 * (1 - u)
class Flash:
    """clarão de boca em camadas (estrela laranja → amarela → núcleo branco) + luz pontual — legível contra nuvens brancas"""
    def _star(self, name, rin, mat_, pts=9):
        a = np.linspace(0, 2 * np.pi, pts * 2, endpoint=False); V = [(0, 0, 0)] + [((1 if i % 2 == 0 else rin) * math.cos(t), 0, (1 if i % 2 == 0 else rin) * math.sin(t)) for i, t in enumerate(a)]
        F = [(0, 1 + i, 1 + (i + 1) % len(a)) for i in range(len(a))]; me = bpy.data.meshes.new(name); me.from_pydata(V, [], F); me.update(); me.materials.append(mat_)
        o = bpy.data.objects.new(name, me); o.visible_shadow = False; util.link(o); return o
    def __init__(self, col=None):
        self.layers = [self._star('fl_o', .55, mats.glow('fl_orange', (1.0, .38, .05, 1), 6.0)), self._star('fl_y', .5, mats.glow('fl_yellow', (1.0, .78, .2, 1), 9.0)), self._star('fl_w', .6, mats.glow('fl_white', (1.0, .97, .85, 1), 14.0), 7)]
        ld = bpy.data.lights.new('flash_l', 'POINT'); ld.energy = 0; ld.color = (1.0, .75, .4); ld.shadow_soft_size = .1; self.l = bpy.data.objects.new('flash_l', ld); util.link(self.l, col)
    def set(self, t, t0, pos, s=.25):
        u = (t - t0) / .16
        if u < 0 or u > 1:
            for o in self.layers: o.hide_render = o.hide_viewport = True
            self.l.data.energy = 0; return
        k = s * (1.25 - u * .55)
        for i, (o, f) in enumerate(zip(self.layers, (1.0, .62, .3))):
            o.hide_render = o.hide_viewport = False; o.location = (pos[0], pos[1] - .02 * (i + 1), pos[2]); o.scale = (k * f * 1.6, 1, k * f * 1.4); o.rotation_euler = (0, u * (1.2 + i) + i, 0)
        self.l.location = pos; self.l.data.energy = 900 * (1 - u)
class Flag:
    """bandeira ondulando (malha recalculada por frame, determinística em t)"""
    def __init__(self, pos, w=2.2, h=1.4, tex=None, pole_h=6.0, col=None, flip=False):
        self.pos = pos; self.w = w; self.h = h; self.nu, self.nv = 14, 8; self.flip = flip
        nu, nv = self.nu, self.nv; V = np.zeros(((nu + 1) * (nv + 1), 3), np.float32); F = []
        for i in range(nu):
            for j in range(nv): a = i * (nv + 1) + j; F.append((a, a + nv + 1, a + nv + 2, a + 1))
        self.me = bpy.data.meshes.new('flag'); self.me.from_pydata(V.tolist(), [], F); uv = self.me.uv_layers.new(name='UVMap'); vuv = np.array([(i / nu, j / nv) for i in range(nu + 1) for j in range(nv + 1)], np.float32)
        idx = np.empty(len(self.me.loops), np.int32); self.me.loops.foreach_get('vertex_index', idx); uv.data.foreach_set('uv', vuv[idx].ravel()); self.me.materials.append(mats.cutout_img('flag_' + tex.split('/')[-1], tex, emit=.4, haze=True))
        self.o = bpy.data.objects.new('flag', self.me); util.link(self.o, col)
        from . import nature; pole = nature._cyl((pos[0], pos[1], pos[2] + pole_h / 2), (0, 0, 1), .05, pole_h, 8); Vp, Fp = nature._merge([pole]); mesh_np('flagpole', Vp, Fp, mats.flat('pole', (.7, .6, .4, 1), rough=.6), col); self.top = pos[2] + pole_h - h - .2
    def update(self, t):
        nu, nv = self.nu, self.nv; V = np.zeros((nu + 1, nv + 1, 3), np.float32); u = np.linspace(0, 1, nu + 1)[:, None]; v = np.linspace(0, 1, nv + 1)[None, :]
        sgn = -1 if self.flip else 1; V[..., 0] = self.pos[0] + sgn * u * self.w; V[..., 1] = self.pos[1] + (np.sin(u * 7 - t * 5.2) * .22 + np.sin(u * 3 - t * 2.1) * .1) * u; V[..., 2] = self.top + v * self.h + np.sin(u * 5 - t * 4) * .04 * u
        self.me.vertices.foreach_set('co', V.reshape(-1, 3).ravel()); self.me.update()
def tent(p, s=1.0, rot=0.0, col=None):
    from . import texlib, nature
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=2.1 * s, depth=2.9 * s, location=(p[0], p[1], p[2] + 1.45 * s)); o = bpy.context.object; o.rotation_euler = (0, 0, math.radians(45) + rot); o.scale = (1.35, 1.0, 1.0)
    o.data.materials.append(mats.image('tent_m', texlib.sail(), rough=.9, spec=.05, bump=.15, coord='Object', scale=(.4, .4), box=True, haze=True, emit=(.9, .85, .7, 1), emit_s=.12)); return o
