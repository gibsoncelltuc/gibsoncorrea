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



box, done = start('golden_stool')    # banquinho dourado ashanti (herói do EP 13)
GD, GL = '#d9a630', '#f2d060'
box((0, 0.06, 0), (0.95, 0.12, 0.55), GD); box((0, 0.3, 0), (0.3, 0.36, 0.34), GL); box((-0.32, 0.28, 0), (0.18, 0.3, 0.3), GD); box((0.32, 0.28, 0), (0.18, 0.3, 0.3), GD)
box((0, 0.58, 0), (1.0, 0.14, 0.62), GL); box((-0.5, 0.66, 0), (0.12, 0.14, 0.62), GD); box((0.5, 0.66, 0), (0.12, 0.14, 0.62), GD)   # assento curvo
box((0, 0.7, 0), (0.7, 0.04, 0.4), '#b0282f')
done()
