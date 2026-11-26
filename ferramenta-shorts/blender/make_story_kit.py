# Pecas de cenario POR HISTORIA (canal: cada video tem cenario proprio). blender -b --python blender/make_story_kit.py
#  -> kit/grave.glb (cova aberta + monte de terra + caixao + poste com sino), kit/cross.glb (cruz de cemiterio), kit/porch.glb (varanda de madeira com parede, porta, lampiao, grade e telhado)
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
# ---- cova
box, done = start('grave')
box((0, 0.02, 0), (1.5, 0.04, 2.9), '#3a2418')                      # buraco (fundo escuro)
box((0, 0.03, 0), (1.05, 0.05, 2.3), '#e6dccb'); box((0, 0.06, 0), (0.85, 0.04, 2.0), '#f4eee2')   # caixao claro visto de cima
for sx in (-1, 1): box((sx * 0.84, 0.05, 0), (0.18, 0.1, 3.1), '#6a4630')
for sz in (-1, 1): box((0, 0.05, sz * 1.5), (1.86, 0.1, 0.18), '#6a4630')
box((-2.3, 0.45, 0.2), (2.4, 0.9, 3.2), '#7a4a30', 0.45); box((-2.5, 0.95, 0.0), (1.3, 0.5, 1.8), '#8a5636', 0.4)   # monte de terra
for sx in (-0.45, 0.45): box((1.9 + sx, 1.0, -1.4), (0.14, 2.0, 0.14), '#6b4a2e')   # poste do sino
box((1.9, 2.05, -1.4), (1.3, 0.14, 0.2), '#6b4a2e'); box((1.9, 1.72, -1.4), (0.34, 0.4, 0.34), '#e2b33a', 0.55); box((1.9, 1.5, -1.4), (0.1, 0.1, 0.1), '#8a6a1c')
box((1.2, 0.9, -0.7), (0.03, 0.03, 1.6), '#d8d0c0')                # cordao ate a cova
done()
box, done = start('cross'); box((0, 0.7, 0), (0.16, 1.4, 0.12), '#d8d2c6'); box((0, 0.95, 0), (0.8, 0.16, 0.12), '#d8d2c6'); box((0, 0.06, 0.5), (0.9, 0.12, 1.4), '#7a6a50', 0.8); done()
# ---- varanda
box, done = start('porch')
W, D, zb = 14.0, 6.0, -3.0
box((0, 0.1, zb + D / 2), (W, 0.2, D), '#6a4a30')
n = int(W / 0.6)
for i in range(n): box((-W / 2 + (i + 0.5) * 0.6, 0.22, zb + D / 2), (0.56, 0.06, D), ['#b98a58', '#a87a4a'][i % 2])
H = 22.0
box((0, H / 2, zb - 0.15), (W + 12, H, 0.3), '#3f8f8a')                # parede de ripas verde-azulada
for j in range(18): box((0, 0.5 + j * 0.55, zb + 0.02), (W + 12, 0.05, 0.06), '#2f6f6c')
box((-3.2, 2.2, zb + 0.06), (2.2, 4.4, 0.14), '#e9e2d0'); box((-3.2, 2.1, zb + 0.12), (1.8, 4.0, 0.12), '#c98a4a'); box((-2.5, 2.1, zb + 0.2), (0.14, 0.14, 0.12), '#e8c45a')   # porta
box((2.6, 3.0, zb + 0.06), (2.6, 2.4, 0.14), '#e9e2d0'); box((2.6, 3.0, zb + 0.12), (2.2, 2.0, 0.1), '#ffd98a'); box((2.6, 3.0, zb + 0.18), (0.1, 2.0, 0.08), '#e9e2d0'); box((2.6, 3.0, zb + 0.18), (2.2, 0.1, 0.08), '#e9e2d0')   # janela acesa
box((-1.3, 3.9, zb + 0.3), (0.34, 0.5, 0.34), '#ffd75a', 0.7); box((-1.3, 4.25, zb + 0.3), (0.42, 0.1, 0.42), '#3a3d47'); box((-1.3, 4.1, zb + 0.12), (0.08, 0.08, 0.3), '#3a3d47')   # lampiao
for px in (-W / 2 + 0.3, W / 2 - 0.3): box((px, 2.6, zb + D - 0.3), (0.3, 5.0, 0.3), '#efe8d8')   # colunas
box((W / 2 - 0.2, 1.25, zb + D / 2), (0.12, 0.14, D), '#efe8d8')       # grade lateral
for k in range(11): box((W / 2 - 0.2, 0.72, zb + 0.3 + k * 0.55), (0.1, 1.0, 0.1), '#efe8d8')
box((0, 5.25, zb + D / 2), (W + 0.8, 0.3, D + 0.8), '#5a6a7a')          # telhado
done()
