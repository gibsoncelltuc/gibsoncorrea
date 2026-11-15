"""Convés da fragata (S5): tábuas, amurada com canhões, mastro com cordame, bandeira, mar e frota ao fundo."""
import bpy, math, numpy as np
from . import util, mats, texlib, renderlib, nature, props, ships, farm, paint
from .util import mesh_np
def build(env='bright'):
    E = farm.ENVS[env]; mats.HAZE.update(color=E['haze'], start=60, end=500, strength=.7)
    renderlib.world_gradient(E['sky'], renderlib.sun_vec(40, 236), E['sun_col'], E['glow'], strength=E['sky_str']); sun = renderlib.sun(40, 236, E['sun_col'], 5.5, angle_deg=2.0)
    objs = {'sun': sun}
    planks = mats.image('deck_planks', texlib.wood_planks(base='#c79a62', dark='#4a2f1e'), rough=.8, spec=.15, bump=.7, scale=(1 / 3.0, 1 / 3.0), coord='Object', box=True, ao=.5, ao_dist=.35, haze=True)
    V = [(-12, -9, 0), (12, -9, 0), (12, 7, 0), (-12, 7, 0)]; me = bpy.data.meshes.new('deck_floor'); me.from_pydata(V, [], [(0, 1, 2, 3)]); me.materials.append(planks); fl = bpy.data.objects.new('deck_floor', me); util.link(fl)
    wood = mats.image('rail_wood', texlib.logs(), rough=.85, spec=.1, bump=.5, scale=(1, 1), coord='Object', box=True, ao=.5, ao_dist=.3, haze=True)
    def box(c, s, m=wood, bev=.025):
        v, f = nature._box(c, s); o = mesh_np('b', v, f, m, smooth=False); b = o.modifiers.new('bv', 'BEVEL'); b.width = bev; b.segments = 2; return o
    bw = mats.image('bulwark', paint.bulwark(), rough=.8, spec=.2, bump=.4, scale=(1 / 3.0, 1 / 1.1), coord='Object', box=True, ao=.4, ao_dist=.3)
    objs['rail_back'] = box((0, 5.6, .55), (26, .35, 1.1), bw); objs['rail_top'] = box((0, 5.6, 1.15), (26, .55, .14)); objs['rail_left'] = box((-12.3, 0, .55), (.35, 14, 1.1))
    for x in (-9, -4.5, 0, 4.5, 9): box((x, 5.6, .8), (.35, .5, 1.6))
    objs['cannons'] = [props.cannon(scale=1.0) for _ in range(2)]
    for c, x in zip(objs['cannons'], (-2.8, 3.4)): c.location = (x, 4.0, 0); c.rotation_euler = (0, 0, math.radians(90))
    mast = nature._cyl((-3.6, 5.0, 7), (0, 0, 1), .5, 14.0, 14, .38); Vm, Fm = nature._merge([mast]); objs['mast'] = mesh_np('mast', Vm, Fm, wood, smooth=True)
    for i in range(3): bpy.ops.mesh.primitive_torus_add(major_radius=.8 - i * .1, minor_radius=.13, location=(-3.6, 5.0, .13 + i * .2)); t = bpy.context.object; t.data.materials.append(mats.flat('rope_c', (.55, .42, .22, 1), rough=.95)); 
    rop = []; 
    for sd in (-1, 1):
        for k in range(5): rop.append(nature._cyl((-3.6 + sd * 1.4 + k * .0, 5.0 + 0.2 * sd, 3.2 + k * .0), (-sd * .32, -sd * .02, 1.0), .03, 7.6, 4))
    Vr, Fr = nature._merge(rop); mesh_np('shrouds', Vr, Fr, mats.flat('rope', (.30, .22, .13, 1), rough=.95), smooth=True)
    yard = nature._cyl((-3.6, 5.0, 8.2), (1, 0, 0), .09, 6.0, 8); Vy, Fy = nature._merge([yard]); mesh_np('yard', Vy, Fy, wood, smooth=True)
    nu_, nv_ = 10, 6; SV = []; SUV = []; SF = []
    for i in range(nu_ + 1):
        for j in range(nv_ + 1): u, v = i / nu_, j / nv_; SV.append((-3.6 - 2.9 + u * 5.8, 5.0 - .25 - math.sin(u * math.pi) * .45 * (.4 + v * .6), 8.1 - v * 3.2)); SUV.append((u, v))
    for i in range(nu_):
        for j in range(nv_): a = i * (nv_ + 1) + j; SF.append((a, a + nv_ + 1, a + nv_ + 2, a + 1))
    so = mesh_np('sail', np.array(SV, np.float32), np.array(SF, np.int32), mats.cutout_img('sail_m', texlib.sail(), emit=.3, haze=True), smooth=True); ships._uv(so.data, np.array(SUV, np.float32))
    rl = []
    for sd in (-1, 1):
        for k in range(8): z = 1.3 + k * .42; xa = -3.6 + sd * (1.5 - k * .12); rl.append(nature._cyl((xa, 5.05, z), (1, 0, 0), .014, 1.0 - k * .08 if False else 1.2 - k * .1, 4))
    Vl, Fl = nature._merge(rl); mesh_np('ratlines', Vl, Fl, mats.flat('rope', (.30, .22, .13, 1), rough=.95), smooth=True)
    fg = bpy.data.meshes.new('flag'); nu, nv = 14, 8; fw, fh = 4.0, 2.5; FV = []; FUV = []; FF = []
    for i in range(nu + 1):
        for j in range(nv + 1): u, v = i / nu, j / nv; FV.append((3.2 + u * fw, 5.6 + math.sin(u * 7) * .35 * u + math.sin(u * 3) * .12 * u, 5.0 + v * fh)); FUV.append((u, v))
    for i in range(nu):
        for j in range(nv): a = i * (nv + 1) + j; FF.append((a, a + nv + 1, a + nv + 2, a + 1))
    fo = mesh_np('flag', np.array(FV, np.float32), np.array(FF, np.int32), mats.cutout_img('uk_flag_big', texlib.flag_uk(), emit=.35, haze=True), smooth=True); ships._uv(fo.data, np.array(FUV, np.float32))
    pol = nature._cyl((3.2, 5.6, 4.7), (0, 0, 1), .07, 5.0, 8); Vp, Fp = nature._merge([pol]); mesh_np('flagpole', Vp, Fp, wood)
    # mar, frota ao fundo, céu/nuvens
    n = 60; xs = np.linspace(-800, 800, n); ys = np.linspace(8, 1200, 60); X, Y = np.meshgrid(xs, ys); Vs = np.stack([X, Y, np.full_like(X, -3.2)], -1).reshape(-1, 3)
    mesh_np('deck_sea', Vs, nature._grid_faces(n, 60), nature.sea().data.materials[0], smooth=True); bpy.data.objects.remove(bpy.data.objects['sea'], do_unlink=True)
    for i, (x, y, s) in enumerate([(-30, 70, 1.0), (22, 105, 1.1), (-70, 140, 1.2)]):
        sh = ships.ship(f'bgship{i}', seed=4 + i); sh.location = (x, y, -3.1); sh.scale = (s, s, s); sh.rotation_euler = (0, 0, math.radians(200 + i * 14))
    rr = util.rng(5); objs['clouds'] = [nature.cloud((float(rr.uniform(-300, 300)), float(rr.uniform(300, 700)), float(rr.uniform(70, 160))), float(rr.uniform(60, 130)), int(rr.integers(1, 99)), f'dcloud{i}') for i in range(7)]
    return objs
