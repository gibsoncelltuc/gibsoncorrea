"""Objetos de cena (set dressing) com texturas pintadas à mão: barris, caixotes com repolho, fardos e montes de feno, carrinho de mão, balde, ferramentas, toco com machado, lenha,
carroça/vagão, celeiro, poço, ovelhas, galinhas, espantalho, varal, lampião, cordas, leme, sino, balas de canhão, escada, fogueira, cerca de estacas, caminho de terra e detalhes no chão.
Tudo modelado em numpy (malhas fundidas por material), coordenadas de mundo; frente das peças voltada para -Y (câmera)."""
import bpy, math, numpy as np
from . import util, mats, texlib, paint, nature
from .util import mesh_np
_M = {}
def _hx(h, a=1.0): c = util.hex_rgb(h); return (c[0], c[1], c[2], a)
def M(k):
    if k in _M: return _M[k]
    img = mats.image
    mk = {
     'wood': lambda: img('d_wood', paint.planks('crate_planks.png', 21), rough=.85, spec=.12, bump=.7, scale=(1 / 1.1, 1 / 1.1), coord='Object', box=True, ao=.55, ao_dist=.3),
     'wood_dark': lambda: img('d_wood_dark', paint.planks('plank_dark.png', 23, '#8a6038', '#2a1a10', 5), rough=.9, spec=.08, bump=.7, scale=(1 / 1.3, 1 / 1.3), coord='Object', box=True, ao=.55, ao_dist=.3),
     'stave': lambda: img('d_stave', paint.staves(), rough=.85, spec=.12, bump=.6, scale=(1 / .9, 1 / .9), coord='Object', box=True, ao=.5, ao_dist=.25),
     'straw': lambda: img('d_straw', paint.straw(), rough=.95, spec=.04, bump=.6, scale=(1 / 1.4, 1 / 1.4), coord='Object', box=True, ao=.4, ao_dist=.3),
     'barn': lambda: img('d_barn', paint.barn_red(), rough=.88, spec=.08, bump=.6, scale=(1 / 2.2, 1 / 2.2), coord='Object', box=True, ao=.5, ao_dist=.4),
     'rope': lambda: img('d_rope', paint.rope(), rough=.95, spec=.05, bump=.5, scale=(1 / .5, 1 / .5), coord='Object', box=True),
     'iron': lambda: img('d_iron', paint.iron(), rough=.5, spec=.5, metallic=.55, bump=.3, scale=(1 / .8, 1 / .8), coord='Object', box=True),
     'canvas': lambda: img('d_canvas', paint.canvas(), rough=.95, spec=.03, bump=.25, scale=(1 / 1.6, 1 / 1.6), coord='Object', box=True, emit=(.9, .84, .7, 1), emit_s=.10),
     'stone': lambda: img('d_stone', paint.stone(), rough=.92, spec=.06, bump=.8, scale=(1 / 1.4, 1 / 1.4), coord='Object', box=True, ao=.5),
     'rock': lambda: img('d_rock', paint.rock(), rough=.92, spec=.06, bump=.7, scale=(1 / 1.2, 1 / 1.2), coord='Object', box=True, ao=.4),
     'logs': lambda: img('d_logs', texlib.logs(), rough=.9, spec=.08, bump=.6, scale=(1 / .9, 1 / .9), coord='Object', box=True, ao=.5, ao_dist=.25),
     'shingle': lambda: img('d_shingle', texlib.shingles(), rough=.85, spec=.1, bump=.6, scale=(1 / 1.4, 1 / 1.4), coord='Object', box=True, ao=.4),
     'cabbage': lambda: mats.painted('d_cabbage', _hx('#3f6a2a'), _hx('#a9c46a'), scale=9, detail=7, rough=.8, spec=.15, bump=.5, ao=.4),
     'cabbage2': lambda: mats.painted('d_cabbage2', _hx('#5a7a2c'), _hx('#d8d06a'), scale=9, detail=7, rough=.8, spec=.15, bump=.5, ao=.4),
     'wool': lambda: mats.painted('d_wool', _hx('#d8d2c2'), _hx('#fffaf0'), scale=22, detail=8, rough=.95, spec=.03, bump=.9, ao=.3, coord='Object'),
     'sheep_face': lambda: mats.flat('d_sheepface', _hx('#3a3434'), rough=.9),
     'white': lambda: mats.painted('d_white', _hx('#d9d2c0'), _hx('#f6f1e4'), scale=10, detail=5, rough=.85, bump=.2),
     'feather_w': lambda: mats.painted('d_chick_w', _hx('#e9e2d2'), _hx('#fffaf0'), scale=14, detail=6, rough=.9, bump=.5, ao=.3),
     'feather_b': lambda: mats.painted('d_chick_b', _hx('#7a3f1e'), _hx('#c27a3a'), scale=14, detail=6, rough=.9, bump=.5, ao=.3),
     'orange': lambda: mats.flat('d_orange', _hx('#e89a2a'), rough=.7, emit=_hx('#e89a2a'), emit_s=.15),
     'red': lambda: mats.flat('d_red', _hx('#c8372f'), rough=.7, emit=_hx('#c8372f'), emit_s=.15),
     'twine': lambda: mats.flat('d_twine', _hx('#5a3c22'), rough=.95),
     'glass': lambda: mats.glow('d_glass', (1.0, .72, .32, 1), 5.0),
     'flame': lambda: mats.glow('d_flame', (1.0, .42, .08, 1), 3.2),
     'flame_in': lambda: mats.glow('d_flame_in', (1.0, .78, .25, 1), 4.5),
     'gold': lambda: mats.flat('d_gold', _hx('#d7a63a'), rough=.35, spec=.7, metallic=.8),
     'rings': lambda: img('d_rings', paint.rings(), rough=.85, spec=.08, bump=.35, coord='UV', scale=(1, 1)),
     'bark': lambda: img('d_bark', texlib.logs(), rough=.92, spec=.05, bump=.7, scale=(1 / .8, 1 / .8), coord='Object', box=True, ao=.5, ao_dist=.2, tint=(.62, .5, .38, 1), tint_f=.7),
     'burlap': lambda: img('d_burlap', paint.canvas('burlap.png', 82, '#b8975a'), rough=.95, spec=.03, bump=.4, scale=(1 / .8, 1 / .8), coord='Object', box=True),
    }
    _M[k] = mk[k](); return _M[k]
def Mdecal(path, **kw):
    k = 'dec:' + path
    if k not in _M: _M[k] = mats.decal('d_dec_' + path.split('/')[-1][:20], path, **kw)
    return _M[k]
def Mcloth(color, seed=1):
    k = 'cl:' + color
    if k not in _M: _M[k] = mats.cutout_img('d_cloth_' + color.strip('#'), paint.cloth('cloth_' + color.strip('#') + '.png', color, seed), emit=.2, haze=True)
    return _M[k]
# ---------------------------------------------------------------- geometria
def _Rz(a): c, s = math.cos(a), math.sin(a); return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], np.float32)
def xf(V, pos, rz=0.0, sc=1.0): return (np.asarray(V, np.float32) * sc) @ _Rz(rz).T + np.asarray(pos, np.float32)
def lathe(prof, sides=20, cap_bottom=True, cap_top=True):
    th = np.linspace(0, 2 * np.pi, sides, endpoint=False); n = len(prof); V = []
    for (r, z) in prof: V += [(r * math.cos(t), r * math.sin(t), z) for t in th]
    F = [(i * sides + j, i * sides + (j + 1) % sides, i * sides + (j + 1) % sides + sides, i * sides + j + sides) for i in range(n - 1) for j in range(sides)]
    if cap_bottom: c = len(V); V.append((0, 0, prof[0][1])); F += [(c, (j + 1) % sides, j) for j in range(sides)]
    if cap_top: c = len(V); V.append((0, 0, prof[-1][1])); b = (n - 1) * sides; F += [(c, b + j, b + (j + 1) % sides) for j in range(sides)]
    return np.array(V, np.float32), F
def ball(c, r, sx=1, sy=1, sz=1, seg=10, rings=6):
    a = np.linspace(0, np.pi, rings + 1); V, F = lathe([(max(r * math.sin(t), 1e-4), -r * math.cos(t)) for t in a], seg, False, False); return V * np.array([sx, sy, sz], np.float32) + np.asarray(c, np.float32), F
def B(c, s, rz=0.0, ry=0.0): v, f = nature._box(c, s, rz, ry); return v, f.tolist()
def C(c, d, r, L, sides=8, r2=None): return nature._cyl(c, d, r, L, sides, r2)
def torus(c, R, r, axis='z', n=24, m=8):
    u = np.linspace(0, 2 * np.pi, n, endpoint=False); v = np.linspace(0, 2 * np.pi, m, endpoint=False); V = []
    for a in u:
        for b in v: V.append(((R + r * math.cos(b)) * math.cos(a), (R + r * math.cos(b)) * math.sin(a), r * math.sin(b)))
    V = np.array(V, np.float32); F = [(i * m + j, i * m + (j + 1) % m, ((i + 1) % n) * m + (j + 1) % m, ((i + 1) % n) * m + j) for i in range(n) for j in range(m)]
    if axis == 'x': V = V[:, [2, 0, 1]]
    elif axis == 'y': V = V[:, [0, 2, 1]]
    return V + np.asarray(c, np.float32), F
def emit(name, parts, mat, smooth=False):
    parts = [p for p in parts if p is not None]
    if not parts: return None
    V, F = nature._merge(parts); return mesh_np(name, V, F, mat, smooth=smooth)
def quad_front(c, w, h, rz=0.0, curl=0.0):
    """plano vertical voltado para -Y (câmera) com UV — para letras/decalques; curl curva as bordas para trás"""
    nx = 8; xs = np.linspace(-w / 2, w / 2, nx + 1); V = []; UV = []
    for z in (-h / 2, h / 2):
        for x in xs: V.append((x, curl * (x / (w / 2)) ** 2 if curl else 0.0, z)); UV.append(((x + w / 2) / w, (z + h / 2) / h))
    F = [(i, i + 1, i + 2 + nx, i + 1 + nx) for i in range(nx)]
    V = xf(np.array(V, np.float32), c, rz); me = bpy.data.meshes.new('decal'); me.from_pydata(V.tolist(), [], F); me.update()
    uv = me.uv_layers.new(name='UVMap'); idx = np.empty(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', idx); uv.data.foreach_set('uv', np.asarray(UV, np.float32)[idx].ravel()); return me
def decal_obj(me, mat, name='decal'):
    o = bpy.data.objects.new(name, me); me.materials.append(mat); util.link(o); return o
def quad_up(c, w, h, rz=0.0):
    V = xf(np.array([(-w / 2, -h / 2, 0), (w / 2, -h / 2, 0), (w / 2, h / 2, 0), (-w / 2, h / 2, 0)], np.float32), c, rz); me = bpy.data.meshes.new('decal_up'); me.from_pydata(V.tolist(), [], [(0, 1, 2, 3)]); me.update()
    uv = me.uv_layers.new(name='UVMap')
    for i, p in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]): uv.data[i].uv = p
    return me
def gz(x, y): return float(nature.height(x, y))
def caps(items, name='caps'):
    """discos com UV radial (anéis de tora) — items = [(centro, eixo, raio)]"""
    V = []; F = []; UV = []
    for (c, ax, R) in items:
        ax = np.asarray(ax, np.float32); ax /= np.linalg.norm(ax); a = np.array([0, 0, 1], np.float32) if abs(ax[2]) < .9 else np.array([1, 0, 0], np.float32); u = np.cross(ax, a); u /= np.linalg.norm(u); w = np.cross(ax, u); k = len(V); n = 12
        V.append(np.asarray(c, np.float32)); UV.append((.5, .5))
        for i in range(n): t = 2 * math.pi * i / n; V.append(np.asarray(c, np.float32) + (u * math.cos(t) + w * math.sin(t)) * R); UV.append((.5 + .5 * math.cos(t), .5 + .5 * math.sin(t)))
        F += [(k, k + 1 + i, k + 1 + (i + 1) % n) for i in range(n)]
    me = bpy.data.meshes.new(name); me.from_pydata(np.array(V, np.float32).tolist(), [], F); me.update(); uv = me.uv_layers.new(name='UVMap'); idx = np.empty(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', idx); uv.data.foreach_set('uv', np.asarray(UV, np.float32)[idx].ravel())
    return decal_obj(me, M('rings'), name)
# ---------------------------------------------------------------- peças
def barrel(x, y, h=1.0, r=.42, rz=0.0, label=None, seed=1):
    z0 = gz(x, y); zs = np.linspace(0, h, 9); rr = r * (1 - .17 * (2 * zs / h - 1) ** 2); V, F = lathe(list(zip(rr, zs)), 20, True, True); parts = [(xf(V, (x, y, z0), rz), F)]
    hoops = []
    for zf in (.1, .3, .7, .9):
        z = zf * h; rb = r * (1 - .17 * (2 * zf - 1) ** 2) + .012; Vh, Fh = lathe([(rb, z - .03), (rb + .012, z - .03), (rb + .012, z + .03), (rb, z + .03)], 20, False, False); hoops.append((xf(Vh, (x, y, z0), rz), Fh))
    o = [emit('barrel', parts, M('stave'), True), emit('barrel_hoops', hoops, M('iron'), True)]
    if label:
        # decalque curvo acompanhando o bojo (frente = -Y)
        n = 9; angs = np.linspace(-.55, .55, n); zz = (h * .42, h * .7); V = []; UV = []; rb = lambda z: r * (1 - .17 * (2 * z / h - 1) ** 2) + .02
        for zi, z in enumerate(zz):
            for a in angs: V.append((rb(z) * math.sin(a), -rb(z) * math.cos(a), z)); UV.append(((a + .55) / 1.1, zi))
        F = [(i, i + 1, i + 1 + n, i + n) for i in range(n - 1)]; V = xf(np.array(V, np.float32), (x, y, z0), rz); me = bpy.data.meshes.new('lab'); me.from_pydata(V.tolist(), [], F); me.update()
        uv = me.uv_layers.new(name='UVMap'); idx = np.empty(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', idx); uv.data.foreach_set('uv', np.asarray(UV, np.float32)[idx].ravel())
        o.append(decal_obj(me, Mdecal(paint.stencil(label, size=(512, 256), sz=100))))
    return [q for q in o if q]
def crate(x, y, s=(.9, .7, .65), rz=0.0, label=None, fill=None, seed=3, lid=False):
    r = np.random.default_rng(seed); z0 = gz(x, y); sx, sy, sz = s; parts = []; t = .045; bh = sz / 3
    def L(c, sz_, ry=0.0): v, f = B(c, sz_); return (xf(v, (x, y, z0 + sz / 2), rz), f)
    for k in range(3):                                                                         # tábuas das 4 paredes
        zc = -sz / 2 + bh * (k + .5)
        parts += [L((0, -sy / 2 + t / 2, zc), (sx, t, bh * .94)), L((0, sy / 2 - t / 2, zc), (sx, t, bh * .94)), L((-sx / 2 + t / 2, 0, zc), (t, sy - 2 * t, bh * .94)), L((sx / 2 - t / 2, 0, zc), (t, sy - 2 * t, bh * .94))]
    for ix in (-1, 1):
        for iy in (-1, 1): parts.append(L((ix * (sx / 2 - .035), iy * (sy / 2 - .035), 0), (.07, .07, sz)))   # quinas
    parts.append(L((0, 0, -sz / 2 + .03), (sx - .1, sy - .1, .05)))                              # fundo
    if lid or not fill: parts += [L((0, (k - 1) * sy / 3, sz / 2 + .02), (sx, sy / 3 * .95, .05)) for k in range(3)]
    o = [emit('crate', parts, M('wood'))]
    if fill == 'cabbage':
        g1, g2 = [], []
        for i in range(int(sx * sy * 14)):
            lx, ly = r.uniform(-sx / 2 + .14, sx / 2 - .14), r.uniform(-sy / 2 + .14, sy / 2 - .14); rr = r.uniform(.12, .16); c = xf(np.array([[lx, ly, sz / 2 - .02 + rr * .55 * r.uniform(.6, 1.2)]], np.float32), (x, y, z0 + sz / 2), rz)[0]
            (g1 if i % 3 else g2).append(ball(c, rr, 1, 1, .9, 9, 5))
        o += [emit('cabbages', g1, M('cabbage'), True), emit('cabbages2', g2, M('cabbage2'), True)]
    if label: o.append(decal_obj(quad_front((0, -sy / 2 - .005, 0), min(sx * .8, .75), sz * .55), Mdecal(paint.stencil(label, size=(512, 256), sz=96))))
    if label: o[-1].location = (0, 0, 0); o[-1].rotation_euler = (0, 0, rz); o[-1].location = (x, y, z0 + sz / 2); 
    return [q for q in o if q]
def hay_bale(x, y, rz=0.0, s=(1.1, .55, .55), seed=2):
    z0 = gz(x, y); parts = [(xf(B((0, 0, 0), s)[0], (x, y, z0 + s[2] / 2), rz), B((0, 0, 0), s)[1])]
    o = emit('bale', parts, M('straw')); bv = o.modifiers.new('bv', 'BEVEL'); bv.width = .07; bv.segments = 3
    tw = [(xf(B((dx, 0, 0), (.025, s[1] + .02, s[2] + .02))[0], (x, y, z0 + s[2] / 2), rz), B((0, 0, 0), (1, 1, 1))[1]) for dx in (-s[0] / 4, s[0] / 4)]
    return [o, emit('twine', tw, M('twine'))]
def haystack(x, y, R=1.4, H=2.2, seed=4):
    z0 = gz(x, y); t = np.linspace(0, 1, 10); prof = [(R * (1 - tt ** 1.7) + .02, H * tt ** .75) for tt in t]; V, F = lathe(prof, 24, True, False)
    r = np.random.default_rng(seed); V = V + r.normal(0, .035, V.shape).astype(np.float32) * np.array([1, 1, .5], np.float32); return [emit('haystack', [(xf(V, (x, y, z0)), F)], M('straw'), True)]
def wheelbarrow(x, y, rz=0.0, fill=None):
    z0 = gz(x, y); P = []; I = []; Wd = []
    def L(parts, v, f): parts.append((xf(v, (x, y, z0), rz), f))
    # caçamba (tronco de pirâmide, frente = +X local → rotacionar para -Y: usa rz)
    top = np.array([(-.45, -.36, .62), (.35, -.4, .66), (.35, .4, .66), (-.45, .36, .62)], np.float32); bot = np.array([(-.3, -.2, .38), (.18, -.2, .38), (.18, .2, .38), (-.3, .2, .38)], np.float32)
    V = np.concatenate([bot, top]); F = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]; L(P, V, F)
    for sd in (-1, 1): v, f = B((-.2, sd * .22, .38), (1.5, .05, .05), 0, -.09); L(P, v, f); v, f = B((-.78, sd * .22, .62), (.5, .05, .05), 0, -.0); L(P, v, f)             # longarinas + cabos
    for sd in (-1, 1): v, f = B((-.45, sd * .22, .2), (.05, .05, .42), 0, 0); L(P, v, f)                                                                                 # pés
    for (vv, ff) in wheel_y((.62, 0, .27), .25): Wd.append((xf(vv, (x, y, z0), rz), ff))                                                                                      # roda com raios
    o = [emit('wbarrow', P, M('wood')), emit('wbarrow_wheel', Wd, M('wood_dark'), True)]
    if fill == 'cabbage':
        g = [ball(xf(np.array([[-.12 + (i % 3) * .17, -.12 + (i // 3) * .2, .7]], np.float32), (x, y, z0), rz)[0], .14, 1, 1, .9, 9, 5) for i in range(6)]; o.append(emit('wb_cabbage', g, M('cabbage'), True))
    return [q for q in o if q]
def bucket(x, y, z=None, h=.32, r=.17):
    z0 = gz(x, y) if z is None else z; prof = [(0, 0), (r * .85, 0), (r, h), (r * .93, h), (r * .78, .03), (0, .03)]; V, F = lathe(prof, 14, False, False)
    ring = lathe([(r * .88 + .01, h * .3), (r * .88 + .02, h * .3), (r * .88 + .02, h * .34), (r * .88 + .01, h * .34)], 14, False, False)
    return [emit('bucket', [(xf(V, (x, y, z0)), F)], M('wood')), emit('bucket_h', [(xf(ring[0], (x, y, z0)), ring[1])], M('iron'))]
def tool(kind, base, top, seed=1):
    """ferramenta encostada: kind 'rake' | 'hoe' | 'fork'; base=(x,y) no chão, top=(x,y,z) ponta do cabo"""
    z0 = gz(*base); b = np.array([base[0], base[1], z0 + .03], np.float32); t = np.array(top, np.float32); d = t - b; L = float(np.linalg.norm(d)); d /= L
    P = [C((b + t) / 2, d, .022, L, 6)]; H = []
    perp = np.cross(d, np.array([0, -1, 0], np.float32)); perp /= np.linalg.norm(perp) + 1e-6; bar_c = b + d * .02
    if kind == 'rake':
        v, f = B((0, 0, 0), (.5, .03, .04)); R = _basis(perp, d); H.append(((v @ R.T) + bar_c, f))
        for k in range(7): c = bar_c + perp * (-.21 + k * .07) - d * .05; H.append(C(c, d, .008, .1, 4))
    elif kind == 'hoe': v, f = B((0, 0, 0), (.2, .02, .13)); R = _basis(perp, d); H.append(((v @ R.T) + bar_c, f))
    else:
        for k in range(3): c = bar_c + perp * (-.08 + k * .08) - d * .12; H.append(C(c, d, .01, .26, 4))
        v, f = B((0, 0, 0), (.22, .02, .03)); R = _basis(perp, d); H.append(((v @ R.T) + bar_c + d * .02, f))
    return [emit('tool_h', P, M('wood_dark'), True), emit('tool_head', H, M('iron'))]
def _basis(a, b):
    a = a / (np.linalg.norm(a) + 1e-9); b = b / (np.linalg.norm(b) + 1e-9); c = np.cross(a, b); c /= np.linalg.norm(c) + 1e-9; return np.stack([a, c, b], 1).astype(np.float32)
def stump(x, y, r=.32, h=.38, axe=True, seed=5):
    z0 = gz(x, y); V, F = lathe([(r * 1.12, -.05), (r * 1.04, h * .3), (r, h)], 14, False, False); o = [emit('stump', [(xf(V, (x, y, z0)), F)], M('bark'), True)]
    o.append(caps([((x, y, z0 + h + .002), (0, 0, 1), r)], 'stump_top'))
    if axe: o += tool('hoe', (x + .05, y - .02), (x + .1, y - .02, z0 + h + .55))[:1] + [emit('axe_head', [B((x + .12, y - .02, z0 + h + .5), (.17, .03, .13), 0, .3)], M('iron'))]
    return [q for q in o if q]
def firewood(x, y, rz=0.0, cols=7, rows=4, L=1.1, seed=6):
    r = np.random.default_rng(seed); z0 = gz(x, y); P = []
    for k in range(rows):
        n = cols - (k % 2)
        for i in range(n):
            lx = (i - (n - 1) / 2) * .27; lz = .14 + k * .25; rr = .115 + .02 * r.random(); P.append((xf(np.array(C((lx, 0, lz), (0, 1, 0), rr, L * (.9 + .15 * r.random()), 9)[0]), (x, y, z0), rz), C((lx, 0, lz), (0, 1, 0), rr, L, 9)[1]))
    cp = []
    for k in range(rows):
        n = cols - (k % 2)
        for i in range(n):
            lx = (i - (n - 1) / 2) * .27; lz = .14 + k * .25
            for sd in (-1, 1): cp.append((xf(np.array([[lx, sd * (L / 2 + .003), lz]], np.float32), (x, y, z0), rz)[0], xf(np.array([[0, sd, 0]], np.float32), (0, 0, 0), rz)[0], .105))
    return [emit('firewood', P, M('bark'), True), caps(cp, 'firewood_caps')]
def wheel_y(c, R=.55, r=.05, spokes=8):
    """roda de carroça com eixo em Y local: aro (lathe), cubo e raios"""
    Vr, Fr = lathe([(R, -.07), (R + .04, -.07), (R + .04, .07), (R, .07)], 22, False, False); Vr = Vr[:, [0, 2, 1]]; Fl = [Fr]; P = [(Vr + np.asarray(c, np.float32), Fr)]
    Vh, Fh = lathe([(.09, -.1), (.09, .1)], 10, True, True); P.append((Vh[:, [0, 2, 1]] + np.asarray(c, np.float32), Fh))
    for k in range(spokes): a = k * math.pi / spokes * 2; d = np.array([math.cos(a), 0, math.sin(a)], np.float32); P.append(C(np.asarray(c, np.float32) + d * R / 2, d, .022, R, 5))
    return P
def wagon(x, y, rz=0.0, cover=True, L=2.4, W=1.2, label=None):
    z0 = gz(x, y); P = []; Wh = []; Cv = []
    def A(parts, v, f): parts.append((xf(v, (x, y, z0), rz), f))
    v, f = B((0, 0, .62), (L, W, .08)); A(P, v, f)
    for sd in (-1, 1): v, f = B((0, sd * W / 2, .78), (L, .06, .34)); A(P, v, f)
    for sx_ in (-1, 1): v, f = B((sx_ * L / 2, 0, .78), (.06, W, .34)); A(P, v, f)
    v, f = B((-L / 2 - .9, 0, .5), (1.9, .07, .07), 0, -.16); A(P, v, f)                                      # timão
    for sx_ in (-.7, .75):
        for sd in (-1, 1):
            for (vv, ff) in wheel_y((sx_, sd * (W / 2 + .12), .55), .52): A(Wh, vv, ff)
    if cover:
        n = 14; m = 7; V = []
        for i in range(m + 1):
            xx = -L / 2 + i * L / m
            for j in range(n + 1): a = math.pi * j / n; V.append((xx, -(W / 2 + .02) * math.cos(a), .78 + .72 * math.sin(a) * (1 - .12 * (2 * i / m - 1) ** 2)))
        F = [(i * (n + 1) + j, i * (n + 1) + j + 1, (i + 1) * (n + 1) + j + 1, (i + 1) * (n + 1) + j) for i in range(m) for j in range(n)]; A(Cv, np.array(V, np.float32), F)
    o = [emit('wagon', P, M('wood_dark')), emit('wagon_wheels', Wh, M('wood_dark'), True)]
    if cover: o.append(emit('wagon_cover', Cv, M('canvas'), True))
    return [q for q in o if q]
def barn(x, y, rz=0.0, W=9.0, D=6.5, H=4.2):
    z0 = gz(x, y) - .1; P = []; T = []; Rf = []; Dr = []
    def A(parts, v, f): parts.append((xf(v, (x, y, z0), rz), f))
    v, f = B((0, 0, H / 2), (W, D, H)); A(P, v, f)
    gab = np.array([(-W / 2 - .3, -D / 2, H), (W / 2 + .3, -D / 2, H), (0, -D / 2, H + 2.4), (-W / 2 - .3, D / 2, H), (W / 2 + .3, D / 2, H), (0, D / 2, H + 2.4)], np.float32); A(P, gab, [(0, 1, 2), (3, 5, 4)])      # empenas
    for sd in (-1, 1):
        v = np.array([(-W / 2 - .3, sd * (D / 2 + .5), H - .3 * (1 if sd > 0 else 1)), (W / 2 + .3, sd * (D / 2 + .5), H - .3), (W / 2 + .3, 0, H + 2.45), (-W / 2 - .3, 0, H + 2.45)], np.float32); A(Rf, v, [(0, 1, 2, 3)] if sd < 0 else [(3, 2, 1, 0)])
    for sx_ in (-1, 1): v, f = B((sx_ * 1.0, -D / 2 - .06, 1.6), (1.9, .12, 3.2)); A(Dr, v, f)                  # portões
    for sx_ in (-1, 1):
        for ang in (.78, -.78): v, f = B((sx_ * 1.0, -D / 2 - .13, 1.6), (.12, .06, 3.5), 0, ang); A(T, v, f)    # travessas em X
    for z_ in (0.06, 3.2): v, f = B((0, -D / 2 - .1, z_), (4.2, .1, .14)); A(T, v, f)
    for sx_ in (-W / 2, W / 2):
        for sy_ in (-D / 2, D / 2): v, f = B((sx_, sy_, H / 2), (.22, .22, H + .1)); A(T, v, f)               # quinas brancas
    v, f = B((0, -D / 2 - .06, H + 1.1), (.9, .1, .9)); A(Dr, v, f)                                           # janela do sótão
    wh = Mcloth('#e8e2d0'); o = [emit('barn', P, M('barn')), emit('barn_roof', Rf, M('shingle')), emit('barn_doors', Dr, M('wood_dark')), emit('barn_trim', T, wh)]
    return [q for q in o if q]
def well(x, y, rz=0.0):
    z0 = gz(x, y); Vs, Fs = lathe([(.78, 0), (.78, .85), (.58, .85), (.58, .1)], 16, False, False); P = [(xf(Vs, (x, y, z0), rz), Fs)]; W = []
    for sd in (-1, 1): v, f = B((sd * .7, 0, 1.4), (.1, .1, 1.1)); W.append((xf(v, (x, y, z0), rz), f))
    v, f = B((0, 0, 1.95), (1.7, .08, .08)); W.append((xf(v, (x, y, z0), rz), f))
    for sd in (-1, 1): v, f = B((0, sd * .42, 2.15), (1.9, .75, .06), 0, 0); W.append((xf(v, (x, y, z0), rz + 0), f))
    return [emit('well', P, M('stone'), True), emit('well_wood', W, M('wood_dark'))]
def sheep(x, y, rz=0.0, seed=7, grazing=True):
    r = np.random.default_rng(seed); z0 = gz(x, y); body = []; dark = []
    for i in range(14): lx, ly, lz = r.uniform(-.32, .32), r.uniform(-.17, .17), .46 + r.uniform(-.06, .1); body.append(ball(xf(np.array([[lx, ly, lz]], np.float32), (x, y, z0), rz)[0], r.uniform(.18, .24), 1, 1, .9, 8, 5))
    hx = .5 if not grazing else .52; hz = .5 if not grazing else .3; dark.append(ball(xf(np.array([[hx, 0, hz]], np.float32), (x, y, z0), rz)[0], .15, 1.3, .85, 1.0, 8, 5))
    for sx_ in (-.22, .22):
        for sd in (-.09, .09): dark.append(C(xf(np.array([[sx_, sd, .16]], np.float32), (x, y, z0), rz)[0], (0, 0, 1), .04, .32, 6))
    for sd in (-1, 1): dark.append(ball(xf(np.array([[hx - .02, sd * .13, hz + .06]], np.float32), (x, y, z0), rz)[0], .045, 1.6, .5, .7, 6, 4))
    return [emit('sheep', body, M('wool'), True), emit('sheep_dark', dark, M('sheep_face'), True)]
def chicken(x, y, rz=0.0, white=True, seed=8):
    z0 = gz(x, y); P = lambda *a: xf(np.array([a], np.float32), (x, y, z0), rz)[0]; body = [ball(P(0, 0, .2), .13, 1.25, .95, 1.0, 9, 6), ball(P(.14, 0, .33), .065, 1, .9, 1, 8, 5), ball(P(-.15, 0, .27), .09, 1.3, .5, 1.3, 7, 5)]
    beak = [(P(.2, 0, .33), [(0, 0, 0)])]; parts_o = [C(P(.21, 0, .335), (1, 0, 0), .018, .06, 4, .001)]; legs = [C(P(0, sd * .04, .06), (0, 0, 1), .01, .12, 4) for sd in (-1, 1)]; comb = [ball(P(.14, 0, .4), .025, 1, .5, 1.2, 6, 4)]
    return [emit('chick', body, M('feather_w' if white else 'feather_b'), True), emit('chick_o', parts_o + legs, M('orange')), emit('chick_r', comb, M('red'))]
def scarecrow(x, y, seed=9):
    z0 = gz(x, y); P = [C((x, y, z0 + .95), (0, 0, 1), .03, 1.9, 6), C((x, y, z0 + 1.45), (1, 0, 0), .025, 1.5, 6)]; sh = []; hd = [ball((x, y - .02, z0 + 1.78), .17, 1, 1, 1.05, 10, 6)]; st = []
    v, f = B((x, y - .03, z0 + 1.25), (.62, .06, .62)); sh.append((v, f)); v, f = B((x, y - .03, z0 + 1.48), (1.4, .05, .22)); sh.append((v, f))
    for sd in (-1, 1): st.append(C((x + sd * .72, y, z0 + 1.4), (sd, 0, -.3), .035, .22, 5))
    hat = [(xf(lathe([(.36, 0), (.36, .02), (.14, .04), (.14, .22), (0, .22)], 14, False, False)[0], (x, y - .02, z0 + 1.93)), lathe([(.36, 0), (.36, .02), (.14, .04), (.14, .22), (0, .22)], 14, False, False)[1])]
    return [emit('scare_post', P, M('wood_dark')), emit('scare_shirt', sh, Mcloth('#3f6aa8', 3)), emit('scare_head', hd, M('burlap'), True), emit('scare_straw', st, M('straw')), emit('scare_hat', hat, M('straw'), True)]
def clothesline(x, y, rz=0.0, L=3.0, colors=('#f3ead6', '#c8372f', '#3f6aa8', '#f3ead6', '#e8c068')):
    z0 = gz(x, y); P = [C(xf(np.array([[-L / 2, 0, 1.0]], np.float32), (x, y, z0), rz)[0], (0, 0, 1), .04, 2.0, 6), C(xf(np.array([[L / 2, 0, 1.0]], np.float32), (x, y, z0), rz)[0], (0, 0, 1), .04, 2.0, 6)]
    wire = [(xf(np.array([(-L / 2 + t * L, 0, 1.92 - .2 * math.sin(math.pi * t)) for t in np.linspace(0, 1, 9)], np.float32), (x, y, z0), rz), None)]
    o = [emit('line_posts', P, M('wood_dark'))]
    for k, c in enumerate(colors):
        t0 = (k + .5) / len(colors); cx = -L / 2 + t0 * L; w = .46; top = 1.92 - .2 * math.sin(math.pi * t0); V = []
        for i in range(5):
            for zz in (0, 1): u = i / 4; V.append((cx + (u - .5) * w, .02 * math.sin(u * 6 + k), top - zz * (.5 + .08 * math.sin(k * 2 + u * 3))))
        F = [(i * 2, i * 2 + 1, i * 2 + 3, i * 2 + 2) for i in range(4)]; V = xf(np.array(V, np.float32), (x, y, z0), rz); o.append(emit(f'cloth{k}', [(V, F)], Mcloth(c, k + 1), True))
    return [q for q in o if q]
def lantern(x, y, z=None, on=True):
    z0 = gz(x, y) if z is None else z; Vb, Fb = lathe([(.09, 0), (.09, .06), (.07, .06), (.07, .26), (.09, .26), (.09, .3)], 8, True, True); P = [(Vb + np.array([x, y, z0], np.float32), Fb)]
    Vg, Fg = lathe([(.065, .06), (.065, .26)], 8, False, False); return [emit('lantern', P, M('iron')), emit('lantern_glass', [(Vg + np.array([x, y, z0], np.float32), Fg)], M('glass'))]
def picket_fence(pts, h=.55, gap=.16, seed=10):
    r = np.random.default_rng(seed); P = []; R = []
    for (a, b) in zip(pts[:-1], pts[1:]):
        Lx = math.hypot(b[0] - a[0], b[1] - a[1]); n = max(2, int(Lx / (gap + .08))); ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for i in range(n + 1):
            xx = a[0] + (b[0] - a[0]) * i / n; yy = a[1] + (b[1] - a[1]) * i / n; z = gz(xx, yy); hh = h * r.uniform(.92, 1.08)
            v, f = B((xx, yy, z + hh / 2), (.07, .03, hh), ang + math.pi / 2 * 0 + r.normal(0, .03)); P.append((v, f))
        for zz in (.14, .38): v, f = B(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, gz((a[0] + b[0]) / 2, (a[1] + b[1]) / 2) + zz), (Lx, .03, .05), ang); R.append((v, f))
    return [emit('pickets', P, M('white')), emit('picket_rails', R, M('wood_dark'))]
def rock(x, y, s=.4, seed=11):
    r = np.random.default_rng(seed); z0 = gz(x, y); V, F = ball((0, 0, 0), 1.0, 1, 1, .7, 9, 6); V = V * (1 + r.normal(0, .12, (len(V), 1))).astype(np.float32); V = V * np.array([s * r.uniform(.9, 1.4), s * r.uniform(.8, 1.2), s], np.float32) + np.array([x, y, z0 + s * .3], np.float32)
    return [emit('rock', [(V, F)], M('rock'), True)]
def rope_coil(x, y, z, R=.5, turns=5, rz=0.0):
    P = []
    for i in range(turns): P.append(torus((x, y, z + .04 + i * .075), R - i * .02, .045, 'z', 20, 6))
    return [emit('rope_coil', P, M('rope'), True)]
def ship_wheel(x, y, rz=0.0, R=.55):
    z0 = 1.15; P = [torus((0, 0, 0), R, .035, 'y', 28, 6)]; H = []
    for k in range(8):
        a = k * math.pi / 4; d = np.array([math.cos(a), 0, math.sin(a)], np.float32); P.append(C(d * R / 2, d, .018, R * 2.0 if k < 4 else .01, 5)); H.append(C(d * (R + .13), d, .028, .26, 6))
    pre = lambda parts: [(xf(v, (x, y, z0), rz), f) for v, f in parts]; hub = lathe([(.1, -.06), (.1, .06)], 10, True, True); hub = (xf(hub[0][:, [0, 2, 1]], (x, y, z0), rz), hub[1])
    ped = [B((x, y, .55), (.34, .34, 1.1))]; return [emit('wheel', pre(P) + [hub], M('wood_dark'), True), emit('wheel_handles', pre(H), M('wood'), True), emit('wheel_ped', ped, M('wood_dark'))]
def bell(x, y, z, s=1.0):
    Vb, Fb = lathe([(.16 * s, 0), (.14 * s, .08 * s), (.09 * s, .22 * s), (.06 * s, .3 * s), (.03 * s, .34 * s)], 14, False, True); P = [(Vb + np.array([x, y, z], np.float32), Fb)]
    br = [B((x, y, z + .5), (.8, .06, .06)), B((x - .38, y, z + .2), (.06, .06, .6)), B((x + .38, y, z + .2), (.06, .06, .6))]; return [emit('bell', P, M('gold'), True), emit('bell_bracket', br, M('wood_dark'))]
def cannonballs(x, y, z, layers=3, r=.09):
    P = []
    for k in range(layers):
        n = layers - k
        for i in range(n):
            for j in range(n): P.append(ball((x + (i - (n - 1) / 2) * r * 2, y + (j - (n - 1) / 2) * r * 2, z + r + k * r * 1.6), r, 1, 1, 1, 8, 5))
    return [emit('cannonballs', P, M('iron'), True)]
def ladder(x, y, z0, z1, rz=0.0, lean=.25, w=.5):
    P = []; L = z1 - z0
    for sd in (-1, 1): v, f = B((sd * w / 2, 0, L / 2), (.05, .04, L), 0, lean); P.append((xf(v, (x, y, z0), rz), f))
    for k in range(1, int(L / .28)): zz = k * .28; v, f = B((0, 0, zz), (w, .035, .035)); v = v + np.array([math.sin(lean) * zz * -1 * 0, 0, 0], np.float32); P.append((xf(v, (x, y, z0), rz), f))
    return [emit('ladder', P, M('wood'))]
def campfire(x, y):
    z0 = gz(x, y); R = [ball((x + math.cos(a) * .55, y + math.sin(a) * .55, z0 + .08), .14, 1, 1, .7, 7, 4) for a in np.linspace(0, 2 * np.pi, 9, endpoint=False)]
    L_ = [C((x, y, z0 + .13), (math.cos(a), math.sin(a), .35), .05, .8, 6) for a in (0.3, 1.9, 3.6)]
    V, F = lathe([(.2, 0), (.14, .22), (.07, .45), (0.0, .7)], 7, False, False); V2, F2 = lathe([(.1, 0), (.06, .18), (0.0, .38)], 7, False, False)
    return [emit('fire_rocks', R, M('rock'), True), emit('fire_logs', L_, M('wood_dark'), True), emit('fire_flame', [(V + np.array([x, y, z0 + .12], np.float32), F)], M('flame'), True), emit('fire_flame_in', [(V2 + np.array([x, y, z0 + .12], np.float32), F2)], M('flame_in'), True)]
def rifle_stack(x, y, rz=0.0):
    z0 = gz(x, y); P = []; Wd = []
    for k in range(3):
        a = k * 2 * math.pi / 3 + .3; top = np.array([x + .02 * math.cos(a), y + .02 * math.sin(a), z0 + 1.15], np.float32); base = np.array([x + .24 * math.cos(a), y + .24 * math.sin(a), z0 + .03], np.float32); d = top - base; L = np.linalg.norm(d)
        P.append(C((base + top) / 2, d / L, .012, L, 5)); Wd.append(C(base + d / L * .22, d / L, .028, .44, 5))
    return [emit('rifles', P, M('iron')), emit('rifle_stocks', Wd, M('wood_dark'))]
def path_decals(points, width=1.6, seed=3, zoff=.025):
    """caminho de terra batida seguindo o terreno: tira com UV (textura tileada ao longo do comprimento)"""
    pts = np.asarray(points, np.float32); seg = [np.linalg.norm(pts[i + 1] - pts[i]) for i in range(len(pts) - 1)]; Ls = np.concatenate([[0], np.cumsum(seg)]); n = max(6, int(Ls[-1] / .6))
    ts = np.linspace(0, Ls[-1], n); xs = np.interp(ts, Ls, pts[:, 0]); ys = np.interp(ts, Ls, pts[:, 1]); V = []; UV = []
    for i in range(n):
        j = min(i + 1, n - 1); k = max(i - 1, 0); d = np.array([xs[j] - xs[k], ys[j] - ys[k]]); d /= np.linalg.norm(d) + 1e-9; nx, ny = -d[1], d[0]
        for sd, v in ((-1, 0), (1, 1)): px, py = xs[i] + nx * sd * width / 2, ys[i] + ny * sd * width / 2; V.append((px, py, gz(px, py) + zoff)); UV.append((ts[i] / (width * 4), v))
    F = [(2 * i, 2 * i + 1, 2 * i + 3, 2 * i + 2) for i in range(n - 1)]; me = bpy.data.meshes.new('path'); me.from_pydata(V, [], F); me.update()
    uv = me.uv_layers.new(name='UVMap'); idx = np.empty(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', idx); uv.data.foreach_set('uv', np.asarray(UV, np.float32)[idx].ravel()); return decal_obj(me, Mdecal(paint.dirt_path(), rough=.95, emit_s=.03), 'dirt_path')
def ground_scatter(kind, area, n, seed, size=1.3):
    """decalques espalhados no chão (palha, folhas de repolho, lascas): n quadrados com o padrão, em posições aleatórias dentro de area=(x0,x1,y0,y1)"""
    r = np.random.default_rng(seed); path = paint.scatter(f'sc_{kind}_{seed}.png', kind, seed); out = []
    for i in range(n):
        x, y = r.uniform(area[0], area[1]), r.uniform(area[2], area[3]); out.append(decal_obj(quad_up((x, y, gz(x, y) + .03), size, size, r.uniform(0, 6.28)), Mdecal(path, rough=.95, emit_s=.05), 'scatter'))
    return out
