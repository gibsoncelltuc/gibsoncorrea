"""Modelagem 3D procedural do cenário (numpy → malhas): terreno com campos em retalhos, grama, flores, horta, cerca, cabana, árvores, nuvens, mar, montanhas."""
import bpy, math, numpy as np
from . import util, mats, texlib
from .util import rng, noise2, fbm2, smoothstep, mesh_np, set_color_attr

SEA_Z = -0.95
def height(x, y):
    h = 0.30 * (fbm2(x * .045, y * .045, 1, 3) - .5) + 0.07 * (fbm2(x * .35, y * .35, 2, 2) - .5)
    flat = 1 - smoothstep(9, 24, np.hypot(x * .8, (y - 2) * 1.1)); h = h * (1 - flat * .8)
    h += smoothstep(34, 80, np.abs(x)) * (7 + 9 * fbm2(x * .018, y * .018, 5, 3))
    h -= smoothstep(33, 43, y) * 0.95
    h -= smoothstep(43, 49, y) * 0.35
    return h
def _grid_faces(nx, ny):
    i = np.arange(nx - 1); j = np.arange(ny - 1); I, J = np.meshgrid(i, j); a = (J * nx + I).ravel(); return np.stack([a, a + 1, a + nx + 1, a + nx], 1)
PALETTE_FIELD = np.array([[.86, .72, .30], [.62, .66, .26], [.78, .62, .24], [.45, .58, .24], [.88, .80, .46], [.70, .55, .22]], np.float32)
def terrain(seed=1):
    xs = np.concatenate([np.arange(-300, -60, 8.0), np.arange(-60, -20, 2.0), np.arange(-20, 20, .5), np.arange(20, 60, 2.0), np.arange(60, 301, 8.0)])
    ys = np.concatenate([np.arange(-40, -10, 2.0), np.arange(-10, 36, .5), np.arange(36, 60, 1.0), np.arange(60, 140, 4.0)])
    X, Y = np.meshgrid(xs, ys); Z = height(X, Y); V = np.stack([X, Y, Z], -1).reshape(-1, 3); F = _grid_faces(len(xs), len(ys))
    # cor macro: campos em retalhos + variação suave (como o campo da referência)
    cx = np.floor(X / 18.0 + 0.35 * np.sin(Y * .04)).astype(int); cy = np.floor(Y / 13.0 + 0.3 * np.sin(X * .05)).astype(int)
    hsh = (cx * 73856093 ^ cy * 19349663) & 0xFFFF; pal = PALETTE_FIELD[hsh % len(PALETTE_FIELD)]
    var = (0.85 + 0.3 * fbm2(X * .2, Y * .2, 7, 3))[..., None]; col = pal * var
    near = np.exp(-((X / 22) ** 2 + ((Y - 4) / 26) ** 2))[..., None]; col = col * (1 - near * .25) + np.array([.62, .6, .26], np.float32) * near * .25
    shore = smoothstep(40, 47, Y)[..., None]; col = col * (1 - shore) + np.array([.88, .78, .52], np.float32) * shore
    rgba = np.concatenate([col.reshape(-1, 3), np.ones((len(V), 1), np.float32)], 1)
    m = mats.image('ground', texlib.grass_ground(), rough=.95, spec=.05, bump=.35, scale=(1 / 6, 1 / 6), coord='Object', box=True, haze=True)
    # multiplica pela cor de vértice (retalhos)
    nt = m.node_tree; vc = nt.nodes.new('ShaderNodeVertexColor'); vc.layer_name = 'Col'; mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = 1.0
    b = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeBsdfPrincipled'][0]; src = b.inputs['Base Color'].links[0].from_socket
    nt.links.new(src, mx.inputs['A']); nt.links.new(vc.outputs['Color'], mx.inputs['B']); nt.links.new(mx.outputs['Result'], b.inputs['Base Color'])
    o = mesh_np('terrain', V, F, m, smooth=True); set_color_attr(o.data, 'Col', rgba); return o
def grass(n=90000, area=(-16, 16, -9, 26), seed=2, hmin=.10, hmax=.46, name='grass', exclude=None):
    r = rng(seed); x = r.uniform(area[0], area[1], n); y = r.uniform(area[2], area[3], n)
    keep = r.random(n) < np.clip(1.2 - (y - area[2]) / (area[3] - area[2]) * .8, .15, 1)
    if exclude:
        for (ax0, ax1, ay0, ay1) in exclude: keep &= ~((x > ax0) & (x < ax1) & (y > ay0) & (y < ay1))
    x, y = x[keep], y[keep]; n = len(x); z = height(x, y)
    h = r.uniform(hmin, hmax, n) * (0.7 + 0.6 * fbm2(x * .3, y * .3, 3, 2)); w = r.uniform(.011, .022, n); a = r.uniform(0, 2 * np.pi, n); c, s_ = np.cos(a), np.sin(a)
    bend = r.normal(0, .08, (n, 2)) * (h / .3)[:, None]
    def P(t, ww):   # ponto da lâmina na altura t (0..1): curva quadrática
        k = bend * (t ** 2)[:, None] if hasattr(t, '__len__') else bend * t ** 2
        return k
    t1 = .5; k1 = bend * (t1 ** 2); k2 = bend
    bl = np.stack([x - w / 2 * c, y - w / 2 * s_, z], 1); br = np.stack([x + w / 2 * c, y + w / 2 * s_, z], 1)
    ml = np.stack([x - w * .32 * c + k1[:, 0], y - w * .32 * s_ + k1[:, 1], z + h * t1], 1); mr = np.stack([x + w * .32 * c + k1[:, 0], y + w * .32 * s_ + k1[:, 1], z + h * t1], 1)
    tp = np.stack([x + k2[:, 0], y + k2[:, 1], z + h], 1)
    V = np.stack([bl, br, ml, mr, tp], 1).astype(np.float32)                                   # (n,5,3)
    pal = np.array([[.92, .70, .16], [.95, .82, .36], [.50, .66, .14], [.34, .64, .16], [.86, .54, .12]], np.float32); w_ = np.array([.28, .12, .26, .22, .12]); pick = r.choice(len(pal), n, p=w_ / w_.sum())
    base = pal[pick] * (.55 + .22 * r.random((n, 1))); mid = pal[pick] * (.9 + .15 * r.random((n, 1))); tip = np.clip(pal[pick] * (1.22 + .2 * r.random((n, 1))) + np.array([.05, .04, 0]), 0, 1)
    C = np.empty((n, 5, 4), np.float32); C[:, 0, :3] = base; C[:, 1, :3] = base; C[:, 2, :3] = mid; C[:, 3, :3] = mid; C[:, 4, :3] = tip; C[..., 3] = 1
    off = (np.arange(n) * 5)[:, None]; F = np.concatenate([off + [0, 1, 3], off + [0, 3, 2], off + [2, 3, 4]], 0).reshape(3, n, 3).transpose(1, 0, 2).reshape(-1, 3).astype(np.int32)
    m = mats.vcol('grass_m', rough=.8, spec=.15, haze=True)
    o = mesh_np(name, V.reshape(-1, 3), F, m, smooth=False); set_color_attr(o.data, 'Col', C.reshape(-1, 4)); return o
def flowers(n=1500, area=(-14, 14, -8, 22), seed=4, name='flowers'):
    r = rng(seed); x = r.uniform(area[0], area[1], n); y = r.uniform(area[2], area[3], n); z = height(x, y); h = r.uniform(.16, .55, n); R = r.uniform(.035, .06, n)
    pal = np.array([[.96, .78, .12], [1, .55, .26], [1, .48, .66], [.97, .95, .9], [.6, .48, .86], [.85, .26, .22]], np.float32); col = pal[r.integers(0, len(pal), n)]
    # caule (triângulo fino) + cabeça (leque de 6 triângulos)
    V = []; F = []; C = []
    for k in range(6):
        pass
    a0 = r.uniform(0, 2 * np.pi, n); tilt = r.uniform(.2, .9, n); nx = np.sin(tilt) * np.cos(a0); ny = np.sin(tilt) * np.sin(a0); nz = np.cos(tilt)
    cx, cy, cz = x + r.normal(0, .02, n), y + r.normal(0, .02, n), z + h
    stem = np.stack([np.stack([x - .004, y, z], 1), np.stack([x + .004, y, z], 1), np.stack([cx, cy, cz], 1)], 1)
    parts = [stem]; cparts = [np.concatenate([np.tile([[.25, .42, .15, 1]], (n, 2, 1)), np.tile([[.36, .52, .2, 1]], (n, 1, 1))], 1)]
    # base ortonormal da cabeça
    t1 = np.stack([-np.sin(a0), np.cos(a0), np.zeros(n)], 1); nrm = np.stack([nx, ny, nz], 1); t2 = np.cross(nrm, t1)
    for k in range(6):
        ang0, ang1 = 2 * np.pi * k / 6, 2 * np.pi * (k + 1) / 6
        p0 = np.stack([cx, cy, cz], 1); p1 = p0 + R[:, None] * (np.cos(ang0) * t1 + np.sin(ang0) * t2); p2 = p0 + R[:, None] * (np.cos(ang1) * t1 + np.sin(ang1) * t2)
        parts.append(np.stack([p0, p1, p2], 1)); cc = np.concatenate([np.tile([[.95, .8, .2, 1]], (n, 1, 1)), np.concatenate([col, np.ones((n, 1))], 1)[:, None, :].repeat(2, 1)], 1); cparts.append(cc)
    V = np.concatenate(parts, 0).astype(np.float32); C = np.concatenate(cparts, 0).astype(np.float32); F = np.arange(len(V) * 3, dtype=np.int32).reshape(-1, 3)
    m = mats.vcol('flower_m', rough=.7, spec=.2, haze=True); o = mesh_np(name, V.reshape(-1, 3), F, m); set_color_attr(o.data, 'Col', C.reshape(-1, 4)); return o
def _box(c, s, rotz=0.0, roty=0.0):
    sx, sy, sz = s[0] / 2, s[1] / 2, s[2] / 2; v = np.array([[-sx, -sy, -sz], [sx, -sy, -sz], [sx, sy, -sz], [-sx, sy, -sz], [-sx, -sy, sz], [sx, -sy, sz], [sx, sy, sz], [-sx, sy, sz]], np.float32)
    cz, sz_ = math.cos(rotz), math.sin(rotz); cy, sy_ = math.cos(roty), math.sin(roty)
    Rz = np.array([[cz, -sz_, 0], [sz_, cz, 0], [0, 0, 1]], np.float32); Ry = np.array([[cy, 0, sy_], [0, 1, 0], [-sy_, 0, cy]], np.float32); v = (v @ Ry.T) @ Rz.T + np.asarray(c, np.float32)
    f = np.array([[0, 1, 2, 3], [4, 7, 6, 5], [0, 4, 5, 1], [1, 5, 6, 2], [2, 6, 7, 3], [3, 7, 4, 0]]); return v, f
def _cyl(c, d, r, L, sides=10, r2=None):
    d = np.asarray(d, np.float32); d /= np.linalg.norm(d); a = np.array([0, 0, 1], np.float32) if abs(d[2]) < .95 else np.array([1, 0, 0], np.float32); u = np.cross(d, a); u /= np.linalg.norm(u); w = np.cross(d, u)
    th = np.linspace(0, 2 * np.pi, sides, endpoint=False); ring = lambda rr: np.stack([np.cos(th) * rr, np.sin(th) * rr], 1)
    p0 = np.asarray(c, np.float32) - d * L / 2; p1 = np.asarray(c, np.float32) + d * L / 2; q = ring(1)
    v0 = p0 + (q[:, :1] * u + q[:, 1:] * w) * r; v1 = p1 + (q[:, :1] * u + q[:, 1:] * w) * (r2 if r2 is not None else r); V = np.concatenate([v0, v1, p0[None], p1[None]]).astype(np.float32)
    F = []; 
    for i in range(sides): j = (i + 1) % sides; F.append([i, j, j + sides, i + sides]); F.append([i, sides * 2, j, j]) ; F.append([i + sides, j + sides, sides * 2 + 1, sides * 2 + 1])
    return V, np.array([f if len(set(f)) == 4 else f[:3] for f in F], dtype=object)
def _merge(parts):
    """une listas de (V, F[list of tuples]) em arrays (F triângulos+quads → triangula)."""
    Vs = []; Fs = []; off = 0
    for V, F in parts:
        Vs.append(V)
        for f in F:
            f = list(f); 
            if len(f) == 4 and len(set(f)) == 4: Fs.append([f[0] + off, f[1] + off, f[2] + off]); Fs.append([f[0] + off, f[2] + off, f[3] + off])
            elif len(set(f)) >= 3: u = []; [u.append(i) for i in f if i not in u]; Fs.append([u[0] + off, u[1] + off, u[2] + off])
        off += len(V)
    return np.concatenate(Vs).astype(np.float32), np.array(Fs, np.int32)
def fence(pts, gap=None, seed=6, name='fence'):
    """cerca de toras (rail fence): pts = lista de (x,y) em polilinha; gap=(x,y,raio) sem postes/trilhos"""
    r = rng(seed); parts = []
    for (a, b) in zip(pts[:-1], pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1]); n = max(1, int(round(L / 2.4))); ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for i in range(n + 1):
            x = a[0] + (b[0] - a[0]) * i / n; y = a[1] + (b[1] - a[1]) * i / n
            if gap and math.hypot(x - gap[0], y - gap[1]) < gap[2]: continue
            z = float(height(x, y)); parts.append(_cyl((x, y, z + .55), (0, 0, 1), .07 + .012 * r.random(), 1.1 + .1 * r.random(), 8))
            if i < n:
                mx = x + (b[0] - a[0]) / n / 2; my = y + (b[1] - a[1]) / n / 2
                if gap and math.hypot(mx - gap[0], my - gap[1]) < gap[2]: continue
                for zz in (.45, .85): parts.append(_cyl((mx, my, float(height(mx, my)) + zz + r.normal(0, .02)), (math.cos(ang), math.sin(ang), r.normal(0, .02)), .05 + .01 * r.random(), L / n * 1.04, 8))
    V, F = _merge(parts); m = mats.image('fence_wood', texlib.logs(), rough=.9, spec=.1, bump=.5, scale=(1 / 1.3, 1 / 1.3), coord='Object', box=True, ao=.5, ao_dist=.3); return mesh_np(name, V, F, m, smooth=True)
def garden(x0=-5.0, x1=5.0, y0=-1.6, y1=5.0, rows=6, seed=7, clear=None):
    """canteiros de batata: montes de terra + folhagem (verde puxado a ouro) + flores brancas"""
    r = rng(seed); ys = np.linspace(y0, y1, rows); mounds = []; leaves = []; lcol = []
    for yy in ys:
        L = x1 - x0; nseg = 40; xs = np.linspace(x0, x1, nseg); prof = np.linspace(-1, 1, 9); V = []; 
        for xv in xs:
            for p in prof: V.append([xv, yy + p * .42, float(height(xv, yy)) + .26 * np.cos(p * 1.4) ** 2 * (1 + .12 * math.sin(xv * 3.1)) - .02])
        V = np.array(V, np.float32); F = _grid_faces(len(prof), nseg); mounds.append((V, F))
        for px in np.arange(x0 + .4, x1, .62):
            cx = px + r.normal(0, .06); cy = yy + r.normal(0, .05); cz = float(height(cx, cy)) + .3; scl = r.uniform(.8, 1.2)
            if clear and any(math.hypot(cx - c[0], cy - c[1]) < c[2] for c in clear): continue
            for k in range(11):
                a = r.uniform(0, 2 * np.pi); ln = r.uniform(.22, .42) * scl; wd = ln * .38; up = r.uniform(.25, .75); dx, dy = math.cos(a), math.sin(a); px_, py_ = -dy, dx
                base = np.array([cx, cy, cz]); tip = base + np.array([dx * ln, dy * ln, ln * up]); mid = base * .45 + tip * .55 + np.array([0, 0, ln * .18])
                leaves.append([base, mid + np.array([px_, py_, 0]) * wd, tip, mid - np.array([px_, py_, 0]) * wd]); t = r.random(); gcol = np.array([.40, .58, .22]) * (1 - t) + np.array([.80, .72, .26]) * t
                lcol.append([gcol * .6, gcol, gcol * 1.15, gcol])
            if r.random() < .5: leaves.append([np.array([cx, cy, cz + .32])] * 4); lcol.append([[.97, .95, .88]] * 4)
    Vm, Fm = _merge([(V, F.tolist()) for V, F in mounds]); soil = mats.image('soil_m', texlib.soil(), rough=.95, spec=.05, bump=.6, scale=(1 / 1.2, 1 / 1.2), coord='Object', box=True, ao=.4)
    om = mesh_np('garden_mounds', Vm, Fm, soil, smooth=True)
    LV = np.array(leaves, np.float32).reshape(-1, 3); LF = np.arange(len(LV), dtype=np.int32).reshape(-1, 4); LC = np.concatenate([np.array(lcol, np.float32).reshape(-1, 3), np.ones((len(LV), 1), np.float32)], 1)
    ol = mesh_np('garden_leaves', LV, LF, mats.vcol('leaf_m', rough=.7, spec=.2), smooth=False); set_color_attr(ol.data, 'Col', LC); return om, ol
def cabin(p=(-8.0, 5.0), rot=0.0, seed=9):
    """cabana de toras: paredes de toras horizontais com pontas nos cantos, telhado de tábuas, chaminé de pedra, porta, janela com luz"""
    r = rng(seed); W, D = 5.2, 4.2; x0, y0 = p; z0 = float(height(x0, y0)); parts = []; rows = 9
    for k in range(rows):
        z = z0 + .14 + k * .245
        for (cx, cy, d, L) in [(x0, y0 - D / 2, (1, 0, 0), W + .5), (x0, y0 + D / 2, (1, 0, 0), W + .5), (x0 - W / 2, y0, (0, 1, 0), D + .5), (x0 + W / 2, y0, (0, 1, 0), D + .5)]:
            if k % 2 == 1 and d == (1, 0, 0): L -= .3
            parts.append(_cyl((cx, cy, z + (r.random() - .5) * .01), d, .13 + .01 * r.random(), L, 10))
    V, F = _merge(parts); logs = mats.image('cabin_logs', texlib.logs(), rough=.9, spec=.1, bump=.6, scale=(1 / 1.0, 1 / 1.0), coord='Object', box=True, ao=.6, ao_dist=.25); o1 = mesh_np('cabin_logs', V, F, logs, smooth=True)
    ztop = z0 + .14 + rows * .245; roof = []
    for s_ in (1, -1):
        v, f = _box((x0, y0 + s_ * D * .28, ztop + .95), (W + 1.2, D * .62, .09)); 
        c, sn = math.cos(-s_ * .62), math.sin(-s_ * .62); pivot = np.array([x0, y0, ztop + .1], np.float32); rel = v - np.array([x0, y0 + s_ * D * .28, ztop + .95], np.float32)
        Rx = np.array([[1, 0, 0], [0, c, -sn], [0, sn, c]], np.float32); v = rel @ Rx.T + np.array([x0, y0 + s_ * D * .3, ztop + .88 - abs(s_) * .0], np.float32); roof.append((v, f.tolist()))
    Vr, Fr = _merge(roof); o2 = mesh_np('cabin_roof', Vr, Fr, mats.image('roof_m', texlib.shingles(), rough=.85, spec=.1, bump=.5, scale=(1 / 1.4, 1 / 1.4), coord='Object', box=True, ao=.4), smooth=False)
    ch = _box((x0 + W / 2 - .4, y0 - .6, ztop + 1.6), (.8, .8, 2.8)); o3 = mesh_np('cabin_chimney', ch[0], ch[1], mats.painted('stone_m', (.42, .38, .36, 1), (.7, .66, .6, 1), scale=14, detail=8, rough=.9, bump=.8, ao=.5), smooth=False)
    door = _box((x0 - 1.0, y0 - D / 2 - .16, z0 + 1.0), (.9, .06, 2.0)); o4 = mesh_np('cabin_door', door[0], door[1], mats.painted('door_m', (.28, .17, .1, 1), (.42, .26, .16, 1), scale=22, detail=3, rough=.8, bump=.3), smooth=False)
    win = _box((x0 + 1.2, y0 - D / 2 - .15, z0 + 1.3), (.85, .05, .8)); o5 = mesh_np('cabin_window', win[0], win[1], mats.glow('window_glow', (1.0, .72, .35, 1), 6.0), smooth=False)
    return [o1, o2, o3, o4, o5]
def sign(p=(9.0, 3.0), text='SAN JUAN\n1859', rotz=0.35):
    x, y = p; z = float(height(x, y)); parts = [_cyl((x, y, z + .9), (0, 0, 1), .06, 1.9, 8)]; V, F = _merge(parts); o1 = mesh_np('sign_post', V, F, mats.image('post_m', texlib.logs(), rough=.9, spec=.1, bump=.4, scale=(1, 1), coord='Object', box=True), smooth=True)
    bx, bf = _box((0, 0, 0), (1.5, .07, .75)); c, s = math.cos(rotz), math.sin(rotz); R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], np.float32); bx = bx @ R.T + np.array([x, y - .05, z + 1.75], np.float32)
    o2 = mesh_np('sign_board', bx, bf, mats.image('board_m', texlib.logs(), rough=.9, spec=.1, bump=.4, scale=(1, 1), coord='Object', box=True), smooth=False)
    # face com o texto (plano UV)
    fx = np.array([[-.72, 0, -.34], [.72, 0, -.34], [.72, 0, .34], [-.72, 0, .34]], np.float32) @ R.T + np.array([x, y - .09, z + 1.75], np.float32); me = bpy.data.meshes.new('sign_face'); me.from_pydata(fx.tolist(), [], [(0, 1, 2, 3)]); uv = me.uv_layers.new(name='UVMap'); 
    for i, (u, v) in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]): uv.data[i].uv = (u, v)
    o3 = bpy.data.objects.new('sign_face', me); util.link(o3); me.materials.append(mats.image('sign_txt', texlib.sign(text), rough=.85, spec=.1, bump=.15, coord='UV')); return [o1, o2, o3]
def fir_tree_mesh(seed, name):
    r = rng(seed); layers = 6; parts = []; C = []; Vs = []; Fs = []; off = 0; H = 1.0
    th = np.linspace(0, 2 * np.pi, 10, endpoint=False)
    def ring(zc, rr, jit): return np.stack([np.cos(th) * rr * (1 + jit * r.normal(0, 1, 10)), np.sin(th) * rr * (1 + jit * r.normal(0, 1, 10)), np.full(10, zc)], 1)
    trunk = _cyl((0, 0, .9), (0, 0, 1), .09, 1.8, 8)
    for k in range(layers):
        z = 1.4 + k * .75; rr = 1.25 * (1 - k / (layers + 1)) ** .9; hh = 1.2 + .2 * (layers - k) / layers
        base = ring(z, rr, .06); tip = np.array([[r.normal(0, .02), r.normal(0, .02), z + hh]]); lower = ring(z - .06, rr * .55, .04)
        V = np.concatenate([base, tip, lower]); F = [[i, (i + 1) % 10, 10] for i in range(10)] + [[i, (i + 1) % 10, 10 + 1 + (i + 1) % 10, 10 + 1 + i] for i in range(10)]
        parts.append((V, F)); t = k / (layers - 1); col = np.array([.17, .30, .27]) * (1 - t) + np.array([.42, .52, .28]) * t; C.append(np.concatenate([np.tile(col * 1.25, (10, 1)), [col * 1.55], np.tile(col * .7, (10, 1))]))
    parts.append(trunk); Vt, Ft = trunk; C.append(np.tile(np.array([.3, .2, .14]), (len(Vt), 1)))
    V, F = _merge(parts); Cc = np.concatenate(C)[: len(V)]; 
    if len(Cc) < len(V): Cc = np.concatenate([Cc, np.tile(Cc[-1], (len(V) - len(Cc), 1))])
    me = mesh_np(name, V, F, mats.vcol('fir_m', rough=.85, spec=.1), smooth=True); set_color_attr(me.data, 'Col', np.concatenate([Cc, np.ones((len(V), 1))], 1)); return me
def trees(n_each=14, seed=3):
    base = [fir_tree_mesh(s, f'fir{s}') for s in (11, 12, 13)]; r = rng(seed); objs = []
    for b in base: b.hide_render = True; b.hide_viewport = True
    spots = []
    for _ in range(n_each * 3):
        side = -1 if r.random() < .5 else 1; x = side * r.uniform(38, 95); y = r.uniform(-30, 40); spots.append((x, y))
    for _ in range(14): spots.append((r.uniform(-30, 30), r.uniform(70, 100)))   # ilhotas distantes são outra coisa; aqui só árvores de fundo da ilha
    for i, (x, y) in enumerate(spots[:n_each * 3]):
        o = bpy.data.objects.new(f'tree{i}', base[i % 3].data); s = r.uniform(2.8, 5.2); o.location = (x, y, float(height(x, y)) - .1); o.scale = (s * r.uniform(.8, 1.1), s * r.uniform(.8, 1.1), s); o.rotation_euler[2] = r.uniform(0, 6.28); util.link(o); objs.append(o)
    return objs
def cloud(p, size=40.0, seed=1, name='cloud'):
    r = rng(seed); import bmesh; bm = bmesh.new(); nb = int(r.integers(6, 10))
    for k in range(nb):
        c = (r.normal(0, .8, 3) * np.array([1.4, .8, .4])) * size * .35; rad = size * r.uniform(.22, .42) * (1 - .3 * abs(c[0]) / (size * .6)); bmesh.ops.create_icosphere(bm, subdivisions=4, radius=rad, matrix=util.Matrix.Translation(c.tolist()))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); V = np.array([v.co[:] for v in me.vertices], np.float32); nrm = np.array([v.normal[:] for v in me.vertices], np.float32)
    d = (fbm2(V[:, 0] * .05 + seed, V[:, 2] * .05, 5, 2) - .5) * size * .26; V = V + nrm * d[:, None]; V[:, 2] = np.maximum(V[:, 2], -size * .07 + (V[:, 2] + size * .07) * .35 * (V[:, 2] < -size * .07)); me.vertices.foreach_set('co', V.ravel()); me.update()
    for pl in me.polygons: pl.use_smooth = True
    m = mats.flat('cloud_m', (.97, .96, .95, 1), rough=1.0, spec=0.0, emit=(.95, .93, .92, 1), emit_s=.35, haze=False); me.materials.append(m)
    o = bpy.data.objects.new(name, me); o.location = p; o.visible_shadow = False; return util.link(o)
def sea(seed=1, size=2400.0):
    n = 200; xs = np.linspace(-size / 2, size / 2, n); ys = np.concatenate([np.linspace(46, 120, 70), np.linspace(125, 1800, 70)]); X, Y = np.meshgrid(xs, ys); V = np.stack([X, Y, np.full_like(X, SEA_Z)], -1).reshape(-1, 3); F = _grid_faces(n, len(ys))
    m, nt, out = mats._new('sea_m'); tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = .35; nz.inputs['Detail'].default_value = 8; mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1, 3.5, 1)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], nz.inputs['Vector']); bn = nt.nodes.new('ShaderNodeBump'); bn.inputs['Strength'].default_value = .9; bn.inputs['Distance'].default_value = .5; nt.links.new(nz.outputs['Fac'], bn.inputs['Height'])
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (.02, .20, .34, 1); cr.color_ramp.elements[1].color = (.07, .42, .55, 1); nt.links.new(nz.outputs['Fac'], cr.inputs['Fac'])
    b = mats._bsdf(nt, (.05, .3, .45, 1), .12, .6); nt.links.new(cr.outputs['Color'], b.inputs['Base Color']); nt.links.new(bn.outputs['Normal'], b.inputs['Normal']); b.inputs['Coat Weight'].default_value = .5; b.inputs['Coat Roughness'].default_value = .05
    mats.finish(m, nt, out, b.outputs['BSDF'], True); return mesh_np('sea', V, F, m, smooth=True)
def mountain(p, scale=(150, 150, 110), seed=2, snow=0.62, name='mountain'):
    n = 80; th = np.linspace(0, 2 * np.pi, n, endpoint=False); rings = 36; V = []; C = []
    for k in range(rings + 1):
        t = k / rings; rr = (1 - t) ** .85; h = t
        for a in th:
            wob = 1 + .28 * (fbm2(math.cos(a) * 3 + t * 2 + seed, math.sin(a) * 3, seed, 3) - .5) * (1 - t * .5); V.append([math.cos(a) * rr * wob * scale[0], math.sin(a) * rr * wob * scale[1], h * scale[2] * (1 + .12 * (fbm2(a * 2, t * 6, seed + 3, 3) - .5))])
            sn = smoothstep(snow, snow + .07, t + .06 * (fbm2(a * 4, t * 9, seed + 9, 3) - .5)); base = np.array([.42, .47, .66]) * (1 - t * .3); C.append(base * (1 - sn) + np.array([.96, .95, .98]) * sn)
    V = np.array(V, np.float32); F = []
    for k in range(rings):
        for i in range(n): a, b = k * n + i, k * n + (i + 1) % n; F.append([a, b, b + n, a + n])
    m = mats.vcol('mtn_m', rough=.9, spec=.1, haze=True); o = mesh_np(name, V + np.array(p, np.float32), np.array(F), m, smooth=True); set_color_attr(o.data, 'Col', np.concatenate([np.array(C), np.ones((len(V), 1))], 1)); return o

def hill(p, scale, seed, name):
    """colinas verdes/douradas com campos em retalhos (profundidade da paisagem)"""
    n = 60; rings = 18; th = np.linspace(0, 2 * np.pi, n, endpoint=False); V = []; C = []
    for k in range(rings + 1):
        t = k / rings; rr = (1 - t ** 1.6)
        for a in th:
            wob = 1 + .22 * (fbm2(math.cos(a) * 2 + seed, math.sin(a) * 2, seed, 3) - .5); V.append([math.cos(a) * rr * wob * scale[0], math.sin(a) * rr * wob * scale[1], (1 - rr ** 2) ** .7 * scale[2] * (1 + .15 * (fbm2(a * 3, t * 5, seed + 2, 3) - .5))])
            cx = int(math.floor(math.cos(a) * rr * 6 + seed)); cy = int(math.floor(math.sin(a) * rr * 5 + t * 3)); pal = PALETTE_FIELD[((cx * 73856093) ^ (cy * 19349663)) % len(PALETTE_FIELD)]; fir = smoothstep(.3, .75, t + .1 * (fbm2(a * 5, t * 8, seed + 7, 2) - .5)); C.append(pal * (1 - fir * .55) + np.array([.12, .28, .24]) * fir * .55)
    V = np.array(V, np.float32); F = []
    for k in range(rings):
        for i in range(n): a_, b_ = k * n + i, k * n + (i + 1) % n; F.append([a_, b_, b_ + n, a_ + n])
    m = mats.vcol('hill_m', rough=.95, spec=.05, haze=True); o = mesh_np(name, V + np.array([p[0], p[1], SEA_Z - 3.0], np.float32), np.array(F), m, smooth=True); set_color_attr(o.data, 'Col', np.concatenate([np.array(C), np.ones((len(V), 1))], 1)); return o
