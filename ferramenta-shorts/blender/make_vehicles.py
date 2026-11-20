# Veiculos de desenho animado (arredondados, com janelas, farois, para-choques, rodas com calota) -> web/assets/library/vehicles/{car,car_blue,taxi,jeep,truck}.glb
# blender -b --python blender/make_vehicles.py     Convencao do motor: no 'body' + nos 'wheel*' (giram sozinhos conforme a distancia). Frente = +z (glTF), y = cima.
import bpy, bmesh, math
from mathutils import Vector, Matrix
OUT = '/home/user/gibsoncorrea/ferramenta-shorts/web/assets/library/vehicles/'
def mat(name, hexc):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes = True; h = hexc.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    lin = [(x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4) for x in c]; b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (*lin, 1); b.inputs['Roughness'].default_value = 1; return m
G = lambda x, y, z: Vector((x, -z, y))
class Part:
    def __init__(s, joint): s.j = Vector(joint); s.bm = bmesh.new(); s.mats = []
    def mi(s, m):
        if m not in s.mats: s.mats.append(m)
        return s.mats.index(m)
    def box(s, c, size, m, bev=0.08, taper=None):                    # caixa arredondada; taper=(fx, fz) estreita o topo (cabine)
        r = bmesh.ops.create_cube(s.bm, size=1.0); vs = r['verts']; mi = s.mi(m)
        for v in vs:
            x, y, z = v.co.x * size[0], v.co.z * size[1], -v.co.y * size[2]   # rotacao (nao espelho): mantem as faces viradas para fora
            if taper and y > 0: x *= taper[0]; z = z * taper[1] + (taper[2] if len(taper) > 2 else 0)
            v.co = G(x + c[0] - s.j.x, y + c[1] - s.j.y, z + c[2] - s.j.z)
        fs = list({f for v in vs for f in v.link_faces}); es = list({e for v in vs for e in v.link_edges})
        for f in fs: f.material_index = mi
        if bev > 0:
            nb = bmesh.ops.bevel(s.bm, geom=es, offset=bev, segments=3, profile=0.5, affect='EDGES')
            for f in nb['faces']: f.material_index = mi; f.smooth = True
    def cyl(s, c, r, w, m, axis='x', seg=20, bev=0.0):              # cilindro com eixo em x (roda) ou z (farol)
        res = bmesh.ops.create_cone(s.bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=w); vs = res['verts']; mi = s.mi(m)
        for v in vs:
            a, b, d = v.co.x, v.co.y, v.co.z                          # d = ao longo do eixo
            p = (d, a, b) if axis == 'x' else (a, b, d)
            v.co = G(p[0] + c[0] - s.j.x, p[1] + c[1] - s.j.y, p[2] + c[2] - s.j.z)
        for f in {f for v in vs for f in v.link_faces}: f.material_index = mi; f.smooth = len(f.verts) == 4
    def ball(s, c, r, m, sc=(1, 1, 1)):
        res = bmesh.ops.create_uvsphere(s.bm, u_segments=12, v_segments=8, radius=r); mi = s.mi(m)
        for v in res['verts']: v.co = G(v.co.x * sc[0] + c[0] - s.j.x, v.co.z * sc[1] + c[1] - s.j.y, -v.co.y * sc[2] + c[2] - s.j.z)
        for f in {f for v in res['verts'] for f in v.link_faces}: f.material_index = mi; f.smooth = True
def build(name, spec):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    M = {k: mat(k, v) for k, v in dict(paint=spec['paint'], paint2=spec.get('paint2', spec['paint']), glass='#a9dcf2', tire='#2b2a30', hub='#d9dde2', chrome='#c9ccd2', light='#ffe27a', tail='#d8312b', dark='#3a3d45', seat='#7a4a2e', wood='#a8733f', plate='#f4f1e6').items()}
    L, W, r, wz, wy = spec['L'], spec['W'], spec['r'], spec['wz'], spec['r']
    b = Part((0, spec['by'], 0)); y0 = r * 0.75; H = spec['H']
    kind = spec['kind']
    if kind in ('car', 'taxi'):   # hatch de desenho animado: cabine ABERTA de colunas finas (o motorista aparece sentado dentro), capo curto, superficies lisas
        fz0 = L / 2; cz0, cz1 = -L * 0.3, L * 0.16; top = y0 + H + 1.3; pw = 0.11
        b.box((0, y0 + H / 2, 0), (W, H, L), M['paint'], 0.1)                                         # carroceria baixa
        b.box((0, y0 + H + 0.08, (-fz0 + cz0) / 2 - 0.02), (W * 0.94, 0.18, cz0 + fz0 - 0.1), M['paint'], 0.08)   # tampa traseira
        b.box((0, y0 + H + 0.1, (cz1 + fz0) / 2 + 0.05), (W * 0.94, 0.22, fz0 - cz1 - 0.15), M['paint'], 0.09)   # capo
        b.box((0, top, (cz0 + cz1) / 2 - 0.05), (W * 0.98, 0.12, cz1 - cz0 + 0.1), M['paint'], 0.05)     # teto
        for sx in (-1, 1):
            b.box((sx * (W / 2 - pw / 2), (y0 + H + top) / 2, cz0 + pw / 2), (pw, top - y0 - H, pw), M['paint'], 0.02)          # coluna traseira
            b.box((sx * (W / 2 - pw / 2), (y0 + H + top) / 2, (cz0 + cz1) / 2 - 0.2), (pw, top - y0 - H, pw), M['paint'], 0.02)  # coluna do meio
            b.box((sx * (W / 2 - pw / 2), (y0 + H + top) / 2, cz1 + 0.16), (pw, top - y0 - H + 0.1, pw), M['paint'], 0.02, taper=(1, 1, -0.42))   # coluna do para-brisa (inclinada)
            b.box((sx * (W / 2 - 0.02), y0 + H * 0.55, (cz0 + cz1) / 2 - 0.2), (0.03, H * 0.8, 0.04), M['dark'], 0.0)               # linha da porta
            b.box((sx * (W / 2 + 0.01), y0 + H * 0.72, (cz0 + cz1) / 2 + 0.25), (0.04, 0.06, 0.24), M['chrome'], 0.01)             # macaneta
            b.box((sx * (W / 2 + 0.1), y0 + H + 0.32, cz1 + 0.05), (0.16, 0.14, 0.1), M['paint'], 0.03)                           # retrovisor
            b.box((sx * W * 0.24, y0 + H + 0.3, (cz0 + cz1) / 2 - 0.35), (W * 0.36, 0.9, 0.16), M['seat'], 0.06)                   # encosto do banco
            b.box((sx * W * 0.24, y0 + H + 0.02, (cz0 + cz1) / 2 - 0.05), (W * 0.36, 0.16, 0.6), M['seat'], 0.05)                  # assento
        b.box((0, y0 + H + 0.2, cz1 - 0.02), (W * 0.9, 0.3, 0.22), M['dark'], 0.05)                    # painel
        b.cyl((W * 0.24, y0 + H + 0.5, cz1 - 0.3), 0.26, 0.06, M['dark'], 'z', 18); b.cyl((W * 0.24, y0 + H + 0.5, cz1 - 0.27), 0.17, 0.07, M['seat'], 'z', 14)   # volante
        b.box((0, top + 0.02, cz1 + 0.02), (W * 0.9, 0.05, 0.06), M['dark'], 0.0)                      # moldura do para-brisa
        if kind == 'taxi': b.box((0, top + 0.2, (cz0 + cz1) / 2), (0.7, 0.26, 0.3), M['plate'], 0.06); [b.box((sx * (W / 2 + 0.005), y0 + H * 0.5, 0), (0.02, 0.16, L * 0.6), M['dark'], 0.0) for sx in (-1, 1)]
    elif kind == 'jeep':
        b.box((0, y0 + H / 2, 0), (W, H, L), M['paint'], 0.1)
        b.box((0, y0 + H + 0.08, L * 0.3), (W * 0.96, 0.18, L * 0.36), M['paint'], 0.06)           # capo
        b.box((0, y0 + H + 0.42, L * 0.1), (W * 0.9, 0.56, 0.07), M['glass'], 0.02); b.box((0, y0 + H + 0.42, L * 0.1 - 0.02), (W * 0.96, 0.62, 0.05), M['dark'], 0.02)   # para-brisa com moldura
        b.box((0, y0 + H + 0.2, -0.25), (W * 0.8, 0.44, 0.16), M['seat'], 0.06); b.box((0, y0 + H + 0.02, -0.02), (W * 0.8, 0.14, 0.5), M['seat'], 0.05)     # banco
        b.cyl((0, y0 + H * 0.75, -L / 2 - 0.16), r * 0.95, 0.26, M['tire'], 'z'); b.cyl((0, y0 + H * 0.75, -L / 2 - 0.3), r * 0.45, 0.04, M['hub'], 'z')   # estepe
        b.ball((0, y0 + H + 0.2, L * 0.3), 0.12, M['plate'], (1.6, 0.2, 1.6))                     # estrela/insignia no capo
    else:                                                                                           # truck
        b.box((0, y0 + H * 0.3, 0), (W, H * 0.6, L), M['dark'], 0.08)                             # chassi
        b.box((0, y0 + H * 0.6 + 0.62, L * 0.33), (W, 1.24, L * 0.3), M['paint'], 0.14, taper=(0.94, 0.86, -0.06))   # cabine
        b.box((0, y0 + H * 0.6 + 0.86, L * 0.33 + L * 0.13 - 0.05), (W * 0.8, 0.5, 0.06), M['glass'], 0.02)
        for sx in (-1, 1): b.box((sx * W * 0.485, y0 + H * 0.6 + 0.86, L * 0.33), (0.05, 0.46, L * 0.16), M['glass'], 0.02)
        b.box((0, y0 + H * 0.6 + 0.08, -L * 0.16), (W * 1.04, 0.16, L * 0.62), M['wood'], 0.04)   # assoalho da carroceria
        for sx in (-1, 1): b.box((sx * W * 0.5, y0 + H * 0.6 + 0.5, -L * 0.16), (0.09, 0.8, L * 0.62), M['paint2'], 0.03)
        b.box((0, y0 + H * 0.6 + 0.5, -L * 0.47), (W * 1.04, 0.8, 0.09), M['paint2'], 0.03); b.box((0, y0 + H * 0.6 + 0.5, L * 0.15), (W * 1.04, 0.8, 0.09), M['paint2'], 0.03)
        for i in range(3):
            for sx in (-1, 1): b.box((sx * W * 0.555, y0 + H * 0.6 + 0.5, -L * 0.4 + i * L * 0.2), (0.05, 0.86, 0.1), M['wood'], 0.01)   # sarrafos
    fz = L / 2 + (0.02 if kind != 'truck' else 0.0)
    b.box((0, y0 + 0.16, fz), (W * 1.04, 0.2, 0.2), M['chrome'], 0.07); b.box((0, y0 + 0.16, -fz), (W * 1.04, 0.2, 0.2), M['chrome'], 0.07)   # para-choques
    hy = y0 + H * 0.66 if kind != 'truck' else y0 + H * 0.6 + 0.3
    for sx in (-1, 1):
        b.cyl((sx * W * 0.33, hy, fz - 0.02), 0.17, 0.1, M['chrome'], 'z'); b.cyl((sx * W * 0.33, hy, fz + 0.04), 0.13, 0.04, M['light'], 'z')   # farois
        b.box((sx * W * 0.36, hy, -fz + 0.0), (0.26, 0.14, 0.06), M['tail'], 0.02)                 # lanternas
        for z in wz: b.box((sx * W * 0.47, y0 + r * 0.95, z), (0.16, 0.12, r * 2.5), M['paint'], 0.05)   # para-lamas
    b.box((0, hy - 0.02, fz + 0.03), (W * 0.36, 0.2, 0.04), M['dark'], 0.01)                       # grade
    for i in range(4): b.box((-W * 0.15 + i * W * 0.1, hy - 0.02, fz + 0.055), (0.03, 0.16, 0.02), M['chrome'], 0.0)
    b.box((0, y0 + 0.2, -fz - 0.1), (0.5, 0.2, 0.02), M['plate'], 0.0)                             # placa
    objs = []
    def emit(part, nm):
        me = bpy.data.meshes.new(nm); part.bm.normal_update(); part.bm.to_mesh(me); part.bm.free()   # normais para fora (senao a carroceria some)
        for m in part.mats: me.materials.append(m)
        o = bpy.data.objects.new(nm, me); o.location = G(*part.j); bpy.context.collection.objects.link(o); objs.append(o)
    emit(b, 'body')
    tags = ['F', 'M', 'B'] if len(wz) == 3 else ['F', 'B']
    for z, t in zip(wz, tags):
        for sx, sd in ((1, 'L'), (-1, 'R')):
            w = Part((sx * (W / 2 - 0.1), wy, z)); c = (sx * (W / 2 - 0.1), wy, z)
            w.cyl(c, r, 0.34, M['tire'], 'x', 24); w.cyl((c[0] + sx * 0.15, c[1], c[2]), r * 0.58, 0.08, M['hub'], 'x', 16); w.cyl((c[0] + sx * 0.2, c[1], c[2]), r * 0.2, 0.06, M['chrome'], 'x', 10)
            for k in range(5): a = k * math.tau / 5; w.ball((c[0] + sx * 0.19, c[1] + r * 0.38 * math.sin(a), c[2] + r * 0.38 * math.cos(a)), 0.045, M['dark'])
            emit(w, f'wheel{t}{sd}')
    bpy.ops.export_scene.gltf(filepath=OUT + name + '.glb', export_format='GLB', export_yup=True, export_apply=True, export_cameras=False, export_lights=False)
    print('OK', name, sum(len(o.data.polygons) for o in objs))
build('car', dict(kind='car', paint='#d8312b', L=4.6, W=2.3, H=0.95, r=0.46, wz=[1.5, -1.45], by=0.62))
build('car_blue', dict(kind='car', paint='#2f6fd0', L=4.6, W=2.3, H=0.95, r=0.46, wz=[1.5, -1.45], by=0.62))
build('taxi', dict(kind='taxi', paint='#f2b632', L=4.6, W=2.3, H=0.95, r=0.46, wz=[1.5, -1.45], by=0.62))
build('jeep', dict(kind='jeep', paint='#6f7a3d', L=4.2, W=2.2, H=0.9, r=0.52, wz=[1.4, -1.35], by=0.75))
build('truck', dict(kind='truck', paint='#6f7a3d', paint2='#5d6733', L=6.4, W=2.5, H=0.9, r=0.6, wz=[2.3, -1.3, -2.6], by=0.9))
