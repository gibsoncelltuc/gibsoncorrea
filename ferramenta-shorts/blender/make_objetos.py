# Objetos de historia que a pre-producao acusou como FALTA MODELAR: blender -b --python blender/make_objetos.py -> kit/cake_table, throne, campfire, tent, chest, stall
import bpy, bmesh, math
from mathutils import Vector
OUT = '/home/user/gibsoncorrea/ferramenta-shorts/web/assets/library/kit/'
def mat(name, hexc):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes = True; h = hexc.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    lin = [(x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4) for x in c]; b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (*lin, 1); b.inputs['Roughness'].default_value = 1; return m
G = lambda x, y, z: Vector((x, -z, y))
def start(name):
    bpy.ops.wm.read_factory_settings(use_empty=True); bm = bmesh.new(); mats = []
    def box(c, size, col, taper=1.0):
        m = mat(name + col, col)
        if m not in mats: mats.append(m)
        k = mats.index(m); r = bmesh.ops.create_cube(bm, size=1.0)
        for v in r['verts']:
            t = taper if v.co.z > 0 else 1.0
            v.co = G(v.co.x * size[0] * t + c[0], v.co.z * size[1] + c[1], -v.co.y * size[2] * t + c[2])
        for f in {f for v in r['verts'] for f in v.link_faces}: f.material_index = k
    def done():
        me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
        for m in mats: me.materials.append(m)
        o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
        bpy.ops.export_scene.gltf(filepath=OUT + name + '.glb', export_format='GLB', export_yup=True, export_apply=True, export_cameras=False, export_lights=False); print('OK', name, len(me.polygons))
    return box, done

box, done = start('cake_table')    # mesa de confeitaria com bolos
box((0, 0.86, 0), (2.4, 0.12, 1.1), '#a8703c')
for x in (-1.05, 1.05):
    for z in (-0.42, 0.42): box((x, 0.4, z), (0.14, 0.8, 0.14), '#7a4a26')
box((0, 0.95, 0), (2.2, 0.06, 0.95), '#f4efe2')                                                             # toalha
box((0, 1.02, 0), (0.86, 0.06, 0.86), '#d9d2c0'); box((0, 1.2, 0), (0.74, 0.3, 0.74), '#f6c9d4'); box((0, 1.37, 0), (0.78, 0.06, 0.78), '#fff6f0')   # bolo grande: prato, massa rosa, glace
box((0, 1.53, 0), (0.5, 0.26, 0.5), '#f6c9d4'); box((0, 1.68, 0), (0.54, 0.05, 0.54), '#fff6f0'); box((0, 1.78, 0), (0.16, 0.16, 0.16), '#d8282f', 0.6)   # andar de cima + cereja
box((-0.8, 1.1, 0.05), (0.5, 0.24, 0.5), '#7a4a26'); box((-0.8, 1.24, 0.05), (0.54, 0.05, 0.54), '#f4e3b0'); box((-0.8, 1.31, 0.05), (0.12, 0.1, 0.12), '#d8282f', 0.6)   # bolo de chocolate
box((0.78, 1.04, 0.18), (0.26, 0.14, 0.26), '#e8b46a', 0.7); box((1.0, 1.04, -0.2), (0.26, 0.14, 0.26), '#e8b46a', 0.7); box((0.62, 1.04, -0.24), (0.26, 0.14, 0.26), '#f0d28a', 0.7)   # doces
done()
box, done = start('throne')
box((0, 0.15, 0), (1.9, 0.3, 1.6), '#8a2f2f'); box((0, 0.62, 0.05), (1.2, 0.64, 1.0), '#d9a630'); box((0, 0.98, 0.1), (1.0, 0.1, 0.8), '#b0282f')   # degrau, assento, almofada
box((0, 1.9, -0.42), (1.2, 2.0, 0.18), '#d9a630', 0.8); box((0, 1.9, -0.32), (0.86, 1.5, 0.06), '#b0282f', 0.8)                                   # encosto
for x in (-0.62, 0.62): box((x, 1.2, 0.05), (0.16, 0.5, 1.0), '#d9a630'); box((x, 3.0, -0.42), (0.18, 0.3, 0.18), '#f2d060', 0.4)
box((0, 3.05, -0.42), (0.3, 0.36, 0.2), '#f2d060', 0.4)
done()
box, done = start('campfire')
for i in range(8):
    a = i * 0.785; box((0.55 * math.cos(a), 0.1, 0.55 * math.sin(a)), (0.26, 0.2, 0.26), '#8d8d86')
box((0, 0.14, 0), (0.9, 0.14, 0.16), '#6a4426'); box((0, 0.2, 0), (0.16, 0.14, 0.9), '#7a4a26')
box((0, 0.5, 0), (0.5, 0.7, 0.5), '#f08a2a', 0.35); box((0.08, 0.62, 0.05), (0.3, 0.8, 0.3), '#f2c230', 0.3); box((-0.1, 0.4, -0.06), (0.26, 0.5, 0.26), '#e2332f', 0.4)
done()
box, done = start('tent')
box((0, 1.0, 0), (2.6, 2.0, 2.8), '#e8dcc0', 0.06); box((0, 0.6, 1.36), (0.7, 1.2, 0.08), '#4a3a2a', 0.3)
box((0, 2.05, 0), (0.08, 0.5, 0.08), '#6a4426'); box((0.16, 2.2, 0), (0.3, 0.18, 0.02), '#d8282f')
done()
box, done = start('chest')
box((0, 0.3, 0), (1.1, 0.6, 0.7), '#8a5a34'); box((0, 0.68, 0), (1.14, 0.2, 0.74), '#a8703c', 0.9)
for x in (-0.4, 0.4): box((x, 0.4, 0), (0.1, 0.84, 0.76), '#d9a630')
box((0, 0.56, 0.36), (0.16, 0.2, 0.06), '#f2d060')
done()
box, done = start('stall')     # barraca de feira
for x in (-1.2, 1.2):
    for z in (-0.5, 0.5): box((x, 1.1, z), (0.12, 2.2, 0.12), '#7a4a26')
box((0, 0.85, 0), (2.6, 0.12, 1.2), '#a8703c'); box((0, 0.4, 0.55), (2.6, 0.8, 0.08), '#c98a4a')
for i in range(6): box((-1.1 + i * 0.44, 2.3, 0), (0.44, 0.14, 1.5), '#d8282f' if i % 2 else '#f4efe2')
box((-0.6, 1.0, 0), (0.6, 0.2, 0.5), '#e8b46a', 0.8); box((0.5, 1.0, 0.1), (0.5, 0.2, 0.5), '#e2332f', 0.8); box((0.1, 1.0, -0.2), (0.3, 0.2, 0.3), '#4fa84a', 0.8)
done()

def sphere(name, r, cy, col, extra=None):   # objetos redondos (bola, chaleira)
    bpy.ops.wm.read_factory_settings(use_empty=True); bm = bmesh.new(); mats = [mat(name + col, col)]
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=r)
    for v in bm.verts: v.co.z += cy
    if extra: extra(bm, mats)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in mats: me.materials.append(m)
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
    bpy.ops.export_scene.gltf(filepath=OUT + name + '.glb', export_format='GLB', export_yup=True, export_apply=True, export_cameras=False, export_lights=False); print('OK', name, len(me.polygons))
def _ball(bm, mats):
    mats.append(mat('ballk', '#22252c'))
    for i, f in enumerate(bm.faces):
        if i % 5 == 0: f.material_index = 1
sphere('ball', 0.42, 0.42, '#f4f1e8', _ball)
def _kettle(bm, mats):   # chaleira de cobre: corpo achatado, tampa com pegador, bico inclinado e alca em arco por cima
    for v in bm.verts: v.co.z = (v.co.z - 0.56) * 0.78 + 0.5; v.co.x *= 1.15; v.co.y *= 1.15
    mats.append(mat('ketd', '#2a2d33')); mats.append(mat('ketl', '#e8b46a'))
    def cube(c, sz, mi=1, rot=0.0):
        r = bmesh.ops.create_cube(bm, size=1.0)
        for v in r['verts']:
            x, y = v.co.x * sz[0], v.co.z * sz[1]; x, y = x * math.cos(rot) - y * math.sin(rot), x * math.sin(rot) + y * math.cos(rot)
            v.co = Vector((x + c[0], v.co.y * sz[2] + c[2], y + c[1]))
        for f in {f for v in r['verts'] for f in v.link_faces}: f.material_index = mi
    cube((0, 0.93, 0), (0.62, 0.1, 0.62), 2); cube((0, 1.03, 0), (0.16, 0.14, 0.16), 1)            # tampa + pegador
    cube((0.78, 0.72, 0), (0.62, 0.16, 0.16), 2, 0.6); cube((1.02, 0.92, 0), (0.2, 0.12, 0.14), 2)   # bico
    cube((-0.5, 1.12, 0), (0.1, 0.5, 0.1), 1, 0.35); cube((0.5, 1.12, 0), (0.1, 0.5, 0.1), 1, -0.35); cube((0, 1.36, 0), (0.86, 0.1, 0.1), 1)   # alca em arco
    cube((0, 0.08, 0), (0.8, 0.1, 0.8), 1)                                                          # base
sphere('kettle', 0.5, 0.56, '#c9743a', _kettle)
def _apple(bm, mats):   # maca vermelha: esfera levemente achatada, cabinho marrom e folha verde
    for v in bm.verts: v.co.z = (v.co.z - 0.5) * 0.9 + 0.45; v.co.x *= 1.05; v.co.y *= 1.05
    mats.append(mat('applst', '#5a3a1e')); mats.append(mat('applf', '#4fa84a'))
    def cube(c, sz, mi, rot=0.0):
        r = bmesh.ops.create_cube(bm, size=1.0)
        for v in r['verts']:
            x, y = v.co.x * sz[0], v.co.z * sz[1]; x, y = x * math.cos(rot) - y * math.sin(rot), x * math.sin(rot) + y * math.cos(rot)
            v.co = Vector((x + c[0], v.co.y * sz[2] + c[2], y + c[1]))
        for f in {f for v in r['verts'] for f in v.link_faces}: f.material_index = mi
    cube((0, 0.88, 0), (0.07, 0.2, 0.07), 1, 0.15)                                                   # cabinho
    cube((0.16, 0.92, 0), (0.26, 0.05, 0.14), 2, 0.5)                                                # folha
sphere('apple', 0.45, 0.45, '#d8282f', _apple)
box, done = start('bathtub')    # banheira de madeira e bronze com agua transbordando
box((0, 0.07, 0), (1.9, 0.14, 1.0), '#8a5a2e')
for z in (-0.46, 0.46): box((0, 0.42, z), (1.9, 0.62, 0.1), '#b87a3c')          # laterais
for x in (-0.9, 0.9): box((x, 0.42, 0), (0.1, 0.62, 1.0), '#b87a3c')            # pontas
box((0, 0.5, 0), (1.7, 0.06, 0.82), '#5aa9e6')                                  # agua
box((0.2, 0.28, 0.54), (0.7, 0.5, 0.05), '#7cc0f2'); box((-0.5, 0.2, 0.54), (0.3, 0.3, 0.05), '#7cc0f2')   # agua escorrendo
box((0.2, 0.03, 0.72), (1.1, 0.04, 0.5), '#5aa9e6')                             # poca no chao
for x in (-0.8, 0.8):
    for z in (-0.4, 0.4): box((x, 0.0, z), (0.16, 0.1, 0.16), '#5a3a1e')
done()
box, done = start('crown')      # coroa de ouro com pedras vermelhas
for i in range(10):
    a = i * 0.628; x, z = 0.42 * math.cos(a), 0.42 * math.sin(a)
    box((x, 0.12, z), (0.22, 0.24, 0.12), '#e8b830'); box((x, 0.34, z), (0.12, 0.2, 0.08), '#f2d060', 0.4)
    if i % 2 == 0: box((x * 1.06, 0.14, z * 1.06), (0.08, 0.08, 0.06), '#d8282f')
box((0, 0.03, 0), (0.9, 0.06, 0.9), '#b8901c')
done()
box, done = start('pisa_tower')   # torre de Pisa inclinada: 8 andares de marmore claro + sino, deslocando a cada andar
for i in range(8):
    sx = 0.09 * i + 0.012 * i * i
    box((sx, 0.35 + i * 0.78, 0), (1.5, 0.7, 1.5), '#eee7d4')
    box((sx, 0.74 + i * 0.78, 0), (1.62, 0.08, 1.62), '#cdbfa0')                  # varanda
    for k in range(6):
        box((sx - 0.55 + k * 0.22, 0.35 + i * 0.78, 0.76), (0.1, 0.5, 0.04), '#b8a888')   # arcos da fachada
sx = 0.09 * 8 + 0.012 * 64
box((sx, 6.6, 0), (1.0, 0.7, 1.0), '#d9cfb5'); box((sx, 7.1, 0), (1.1, 0.12, 1.1), '#b0282f', 0.7)
box((0, 0.04, 0), (2.4, 0.08, 2.4), '#7f9a5c')
done()
box, done = start('feather')      # pena branca
box((0, 0.04, 0), (0.05, 0.05, 0.9), '#e8e2d0')
for k in range(6):
    z = -0.3 + k * 0.12; w = 0.3 - abs(k - 2.5) * 0.04
    box((0.12, 0.05, z), (w, 0.02, 0.1), '#ffffff'); box((-0.12, 0.05, z), (w, 0.02, 0.1), '#f4f0e6')
done()
