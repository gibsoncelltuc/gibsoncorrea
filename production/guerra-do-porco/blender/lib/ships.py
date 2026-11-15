"""Navios de guerra (fragata genérica, não é um navio específico), frota, convés. Modelagem procedural: casco loftado com UV (portinholas), mastros, vergas, velas com bojo, enxárcias, bandeira."""
import bpy, math, numpy as np
from . import util, mats, texlib, nature
from .util import mesh_np, set_color_attr
def _uv(me, vuv):
    uv = me.uv_layers.new(name='UVMap'); idx = np.empty(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', idx); uv.data.foreach_set('uv', np.asarray(vuv, np.float32)[idx].ravel())
def hull_mesh(L=14.0, beam=4.2, h=2.2, nx=26, nz=7):
    xs = np.linspace(-L / 2, L / 2, nx); V = []; UV = []
    for sd in (-1, 1):
        for i, x in enumerate(xs):
            xn = 2 * x / L; w = beam / 2 * np.clip(1 - abs(xn) ** 2.6, 0, 1) ** .62 + .02; sheer = .55 * abs(xn) ** 3 + (.35 * max(0, xn) ** 2)
            for j in range(nz):
                zn = j / (nz - 1); z = -.55 + zn * (h + sheer + .55); ww = w * (.30 + .70 * math.sqrt(zn)) * (1 + .06 * zn)
                V.append((x, sd * ww, z)); UV.append((i / (nx - 1) * 1.0, zn))
    V = np.array(V, np.float32); F = []
    def idx(sd, i, j): return (0 if sd < 0 else nx * nz) + i * nz + j
    for sd in (-1, 1):
        for i in range(nx - 1):
            for j in range(nz - 1):
                a, b, c, d = idx(sd, i, j), idx(sd, i + 1, j), idx(sd, i + 1, j + 1), idx(sd, i, j + 1); F.append((a, b, c, d) if sd > 0 else (a, d, c, b))
    # convés (tira entre as bordas superiores)
    for i in range(nx - 1): a, b, c, d = idx(-1, i, nz - 1), idx(-1, i + 1, nz - 1), idx(1, i + 1, nz - 1), idx(1, i, nz - 1); F.append((a, b, c, d))
    return V, np.array(F, np.int32), np.array(UV, np.float32)
def ship(name='ship', col=None, seed=1, L=14.0):
    r = util.rng(seed); root = util.empty(name, col=col); parts = []
    V, F, UV = hull_mesh(L); hm = mesh_np(name + '_hull', V, F, mats.image('hull_m', texlib.hull(), rough=.55, spec=.35, bump=.2, coord='UV', haze=True), col, smooth=True); _uv(hm.data, UV); hm.parent = root
    wood = mats.image('deck_wood', texlib.logs(), rough=.85, spec=.1, bump=.4, coord='Object', scale=(.7, .7), box=True, haze=True); rope = mats.flat('rope', (.30, .22, .13, 1), rough=.95, haze=True); sailm = mats.image('sail_m', texlib.sail(), rough=.9, spec=.05, bump=.1, coord='UV', haze=True, emit=(.95, .9, .8, 1), emit_s=.18)
    cyl = []; sails = []; ropes = []
    masts = [(L * .27, 6.2, 3.6, 3), (-L * .03, 7.4, 4.4, 3), (-L * .34, 5.2, 3.2, 2)]
    for (x, hgt, w, n) in masts:
        cyl.append(nature._cyl((x, 0, 1.6 + hgt / 2), (0, 0, 1), .11, hgt, 10, .07))
        for k in range(n):
            y0 = 1.9 + k * (hgt - 2.3) / n; ww = w * (1 - k * .18); hh = (hgt - 2.3) / n * .86; cyl.append(nature._cyl((x, 0, y0 + hh + .06), (0, 1, 0), .05, ww + .5, 8))
            nu, nv = 8, 6; SV = []; SUV = []; SF = []
            for i in range(nu + 1):
                for j in range(nv + 1):
                    u, v = i / nu, j / nv; SV.append((x + math.sin(u * math.pi) * math.sin(v * math.pi * .9 + .15) * .55 + .06, (u - .5) * ww, y0 + v * hh)); SUV.append((u, v))
            for i in range(nu):
                for j in range(nv): a = i * (nv + 1) + j; SF.append((a, a + 1, a + nv + 2, a + nv + 1))
            sails.append((np.array(SV, np.float32), np.array(SF, np.int32), np.array(SUV, np.float32)))
        for sd in (-1, 1):
            for dx in (-.7, 0, .7): ropes.append(nature._cyl(((x + dx) * .5 + x * .5, sd * (beam_half := 1.2) * .5, 1.6 + hgt * .33), (dx * .3, sd * 1.0, hgt * .9), .012, hgt * 1.0, 4))
    # gurupés e velas de proa
    cyl.append(nature._cyl((L * .5 + .6, 0, 1.55), (1, 0, .35), .09, 3.4, 8)); cyl.append(nature._cyl((-L * .45, 0, 2.3), (0, 0, 1), .05, 2.0, 6))
    # popa elevada com janelas
    stern = nature._box((-L * .38, 0, 2.2), (L * .16, 3.4, 1.0)); parts.append((stern, wood)); win = nature._box((-L * .46, 0, 2.15), (.06, 2.6, .35))
    # canhões saindo das portinholas (lados)
    gun = []
    for i in range(6):
        xx = -L * .28 + i * (L * .56 / 5)
        for sd in (-1, 1): gun.append(nature._cyl((xx, sd * 2.0, .85), (0, sd, 0), .11, .5, 8))
    from .nature import _merge
    Vc, Fc = _merge(cyl); om = mesh_np(name + '_spars', Vc, Fc, wood, col, smooth=True); om.parent = root
    Vr, Fr = _merge(ropes); orp = mesh_np(name + '_rigging', Vr, Fr, rope, col, smooth=True); orp.parent = root
    Vg, Fg = _merge(gun); og = mesh_np(name + '_guns', Vg, Fg, mats.flat('gun_iron', (.05, .05, .06, 1), rough=.4, spec=.6, metallic=.9, haze=True), col, smooth=True); og.parent = root
    Vs, Fs = _merge([(stern[0], stern[1].tolist())]); osn = mesh_np(name + '_stern', Vs, Fs, wood, col, smooth=False); osn.parent = root
    ow = mesh_np(name + '_windows', win[0], win[1], mats.glow('win_glow', (1.0, .75, .35, 1), 5.0), col, smooth=False); ow.parent = root
    # velas: uma malha por vela (UV) → junta
    SVall = []; SFall = []; SUVall = []; off = 0
    for (sv, sf, suv) in sails: SVall.append(sv); SFall.append(sf + off); SUVall.append(suv); off += len(sv)
    osl = mesh_np(name + '_sails', np.concatenate(SVall), np.concatenate(SFall), sailm, col, smooth=True); _uv(osl.data, np.concatenate(SUVall)); osl.parent = root
    # bandeira (plano com UV)
    fg = bpy.data.meshes.new(name + '_flag'); fw, fh = 1.6, 1.0; fv = [(-L * .5 - .1, 0, 5.2), (-L * .5 - .1 - fw, 0, 5.2), (-L * .5 - .1 - fw, 0, 5.2 + fh), (-L * .5 - .1, 0, 5.2 + fh)]; fg.from_pydata(fv, [], [(0, 1, 2, 3)]); uv = fg.uv_layers.new(name='UVMap')
    for i, uvv in enumerate([(1, 0), (0, 0), (0, 1), (1, 1)]): uv.data[i].uv = uvv
    fg.materials.append(mats.cutout_img('uk_flag', texlib.flag_uk(), emit=.4, haze=True)); of = bpy.data.objects.new(name + '_flag', fg); of.parent = root; util.link(of, col)
    pole = nature._cyl((-L * .5 - .1, 0, 4.7), (0, 0, 1), .04, 2.0, 6); Vp, Fp = _merge([pole]); op = mesh_np(name + '_pole', Vp, Fp, wood, col); op.parent = root
    return root
def fleet(col=None, n=5):
    """cinco navios em escalão (formação), proa para a praia"""
    cfg = [(-24, 64, 1.7, .0, -1.0), (-11, 72, 1.8, 1.3, -.92), (2, 62, 1.65, 2.1, -1.05), (15, 70, 1.8, 3.4, -.95), (28, 66, 1.7, 4.2, -1.0)]
    base = ship('ship_base', col, 3); ships = [base]; 
    for i, (x, y, s, ph, rot) in enumerate(cfg[:n]):
        if i == 0: o = base
        else:
            o = util.empty(f'ship{i}', col=col)
            for ch in base.children: c2 = bpy.data.objects.new(f'{ch.name}_{i}', ch.data); c2.parent = o; c2.location = ch.location; c2.rotation_euler = ch.rotation_euler; c2.scale = ch.scale; util.link(c2, col)
        o.location = (x, y, nature.SEA_Z + .1); o.scale = (s, s, s); o.rotation_euler = (0, 0, math.radians(90) + rot + math.radians(180)); ships.append(o)
    return ships[:1] + ships[1:]
