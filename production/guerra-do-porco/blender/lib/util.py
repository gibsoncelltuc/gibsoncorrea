"""Utilitários Blender (bpy 5.x) — coordenadas: X direita, Y para dentro da cena (câmera olha +Y), Z para cima. Unidade = metro."""
import bpy, bmesh, math, random, os, json
import numpy as np
from mathutils import Vector, Matrix, Euler, Quaternion

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEX = os.path.join(ROOT, 'blender', 'tex')

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for c in list(bpy.data.collections): bpy.data.collections.remove(c)
    try:
        from . import char; char._mesh.clear(); char._mat.clear(); char._ink.clear()   # caches de malhas/materiais referenciam dados já removidos
    except Exception: pass
def collection(name):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if c.name not in [x.name for x in bpy.context.scene.collection.children]: bpy.context.scene.collection.children.link(c)
    return c
def link(obj, col=None):
    (col or bpy.context.scene.collection).objects.link(obj); return obj
def mesh_obj(name, verts, faces, mat=None, col=None, smooth=True, edges=None):
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in verts], edges or [], [tuple(f) for f in faces]); me.update()
    if smooth: me.shade_smooth() if hasattr(me, 'shade_smooth') else [setattr(p, 'use_smooth', True) for p in me.polygons]
    o = bpy.data.objects.new(name, me)
    if mat is not None: me.materials.append(mat)
    return link(o, col)
def empty(name, loc=(0, 0, 0), parent=None, col=None):
    o = bpy.data.objects.new(name, None); o.empty_display_size = 0.05; o.location = loc
    if parent is not None: o.parent = parent
    return link(o, col)
def set_color_attr(me, name, rgba_per_vertex):
    a = me.color_attributes.get(name) or me.color_attributes.new(name=name, type='FLOAT_COLOR', domain='POINT')
    flat = np.asarray(rgba_per_vertex, np.float32).ravel(); a.data.foreach_set('color', flat)
def bevel(obj, width=0.01, segments=2, limit='ANGLE', angle=40):
    m = obj.modifiers.new('bevel', 'BEVEL'); m.width = width; m.segments = segments; m.limit_method = limit; m.angle_limit = math.radians(angle); return m
def smooth_by_angle(obj, angle=35):
    for p in obj.data.polygons: p.use_smooth = True
def rng(seed): return np.random.default_rng(seed)
def hex_rgb(h, lin=True):
    h = h.lstrip('#'); r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    if lin: f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4; r, g, b = f(r), f(g), f(b)
    return (r, g, b, 1.0)
def lerp(a, b, t): return a + (b - a) * t
def clamp(v, a=0.0, b=1.0): return max(a, min(b, v))
def smoother(t): t = clamp(t); return t * t * t * (t * (t * 6 - 15) + 10)
def look_rot(pos, target, roll=0.0):
    d = Vector(target) - Vector(pos); q = d.to_track_quat('-Z', 'Y'); e = q.to_euler()
    if roll: q = q @ Quaternion((0, 0, 1), roll)
    return q
def join(objs, name, col=None):
    for o in bpy.context.selected_objects: o.select_set(False)
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]; bpy.ops.object.join(); o = bpy.context.view_layer.objects.active; o.name = name; return o

def mesh_np(name, V, F, mat=None, col=None, smooth=False):
    """malha rápida a partir de arrays numpy: V (n,3) float, F (m,k) int (k=3 ou 4)."""
    V = np.asarray(V, np.float32); F = np.asarray(F, np.int32); k = F.shape[1]
    me = bpy.data.meshes.new(name); me.vertices.add(len(V)); me.vertices.foreach_set('co', V.ravel())
    me.loops.add(len(F) * k); me.polygons.add(len(F)); me.polygons.foreach_set('loop_start', np.arange(0, len(F) * k, k, dtype=np.int32)); me.polygons.foreach_set('loop_total', np.full(len(F), k, np.int32))
    me.loops.foreach_set('vertex_index', F.ravel()); me.update(calc_edges=True)
    if smooth: me.polygons.foreach_set('use_smooth', np.ones(len(F), bool))
    o = bpy.data.objects.new(name, me)
    if mat is not None: me.materials.append(mat)
    return link(o, col)
def noise2(x, y, seed=0):
    """ruído de valor suave 2D (numpy) — determinístico"""
    x = np.asarray(x, np.float64); y = np.asarray(y, np.float64); xi = np.floor(x).astype(np.int64); yi = np.floor(y).astype(np.int64); xf = x - xi; yf = y - yi
    def h(ix, iy): n = (ix * 374761393 + iy * 668265263 + seed * 1442695041) & 0xFFFFFFFF; n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF; return ((n ^ (n >> 16)) & 0xFFFF) / 65535.0
    sx = xf * xf * (3 - 2 * xf); sy = yf * yf * (3 - 2 * yf)
    a = h(xi, yi); b = h(xi + 1, yi); c = h(xi, yi + 1); d = h(xi + 1, yi + 1); return a + (b - a) * sx + (c - a) * sy + (a - b - c + d) * sx * sy
def fbm2(x, y, seed=0, octaves=4):
    t = 0; a = 1; f = 1; tot = 0
    for o in range(octaves): t = t + a * noise2(x * f, y * f, seed + o); tot += a; a *= .5; f *= 2
    return t / tot
def smoothstep(a, b, x): t = np.clip((np.asarray(x) - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)
