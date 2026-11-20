# Tulipas (objeto da historia): blender -b --python blender/make_tulip.py -> kit/tulip_red|yellow|purple|striped.glb (vaso + flor) e kit/tulip_bed.glb (canteiro colorido)
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
def tulip(box, x, z, col, col2, h=1.0, s=1.0):
    box((x, 0.5 * h * s, z), (0.07 * s, h * s, 0.07 * s), '#3f8a3a')                                   # haste
    box((x - 0.16 * s, 0.34 * h * s, z), (0.3 * s, 0.5 * s, 0.05 * s), '#4fa84a', 0.2); box((x + 0.16 * s, 0.3 * h * s, z), (0.3 * s, 0.44 * s, 0.05 * s), '#4fa84a', 0.2)   # folhas
    box((x, (h + 0.2) * s, z), (0.36 * s, 0.44 * s, 0.36 * s), col, 0.7)                                # calice
    for dx, dz in ((-0.13, 0), (0.13, 0), (0, -0.13), (0, 0.13)): box((x + dx * s, (h + 0.46) * s, z + dz * s), (0.14 * s, 0.2 * s, 0.14 * s), col2, 0.4)   # pontas das petalas
for nm, c1, c2 in (('tulip_red', '#e2332f', '#f0564a'), ('tulip_yellow', '#f2c230', '#ffe07a'), ('tulip_purple', '#8a3fb5', '#b06ad6'), ('tulip_striped', '#f4f0e6', '#d8282f')):
    box, done = start(nm)
    box((0, 0.28, 0), (0.62, 0.56, 0.62), '#c2703a', 1.25); box((0, 0.58, 0), (0.86, 0.1, 0.86), '#a85a2a'); box((0, 0.6, 0), (0.62, 0.06, 0.62), '#4a3222')   # vaso de barro
    tulip(box, 0, 0, c1, c2, h=1.15, s=1.25); done()
box, done = start('tulip_bed')
box((0, 0.18, 0), (5.2, 0.36, 1.3), '#8a5a34'); box((0, 0.37, 0), (4.9, 0.06, 1.0), '#4a3222')
cols = [('#e2332f', '#f0564a'), ('#f2c230', '#ffe07a'), ('#8a3fb5', '#b06ad6'), ('#f4f0e6', '#d8282f'), ('#f08a2a', '#ffb060'), ('#e2332f', '#f0564a'), ('#f2c230', '#ffe07a'), ('#d84a8a', '#f08ab5')]
for i, (c1, c2) in enumerate(cols): tulip(box, -2.1 + i * 0.6, (0.22 if i % 2 else -0.22), c1, c2, h=0.8 + 0.12 * (i % 3), s=1.0)
done()
