# (O globo em azulejos 3D foi descartado: furos e espinhos. Use make_globo.py.)
# Mapa-mundi 3D (formato countryballs): blender -b --python blender/make_mapa3d.py
# -> kit/mapa_mundi.glb (plano, paises extrudados como "azulejos", cada pais = 1 objeto com o NOME do pais; mar = objeto "OCEANO")
# -> kit/globo_paises.glb (globo, mesmos paises, cada um um objeto nomeado). Contorno real: world-atlas/Natural Earth 1:50m (mapas/countries-50m.json).
import bpy, bmesh, math, sys, os
from mathutils import Vector
ROOT = '/home/user/gibsoncorrea/ferramenta-shorts/'; OUT = ROOT + 'web/assets/library/kit/'
sys.path.insert(0, ROOT + 'mapas'); import mapas
G = mapas._load()
def mat(name, hexc, rough=.55):
    m = bpy.data.materials.new(name); m.use_nodes = True; h = hexc.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    lin = [(x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4) for x in c]; b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (*lin, 1); b.inputs['Roughness'].default_value = rough; return m
def simplify(r, tol):
    out = [r[0]]
    for p in r[1:]:
        if abs(p[0] - out[-1][0]) + abs(p[1] - out[-1][1]) >= tol: out.append(p)
    return out if len(out) >= 4 else r
def unwrap(r):
    out = [list(r[0])]
    for lo, la in r[1:]:
        while lo - out[-1][0] > 180: lo -= 360
        while lo - out[-1][0] < -180: lo += 360
        out.append([lo, la])
    return out
def build(globe):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    base = mat('base_pais', '#d9dde3'); sea = mat('base_mar', '#3aa0ff', .35)
    # paises: curva 2D -> preenchimento -> mesh (triangulacao do Blender), depois extrudado
    for name, polys in G:
        if name in ('Antarctica',): continue
        cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '2D'; cu.fill_mode = 'BOTH'; cu.extrude = 0.0
        n = 0
        for ring in polys:
            r = unwrap(simplify(ring, .5 if globe else .22))
            if len(r) < 4 or (max(p[0] for p in r) - min(p[0] for p in r)) < .35 and (max(p[1] for p in r) - min(p[1] for p in r)) < .35: continue
            sp = cu.splines.new('POLY'); sp.points.add(len(r) - 1); n += 1
            for i, (lo, la) in enumerate(r): sp.points[i].co = (lo, la, 0, 1)
            sp.use_cyclic_u = True
        if not n: continue
        ob = bpy.data.objects.new(name, cu); bpy.context.collection.objects.link(ob)
        bpy.context.view_layer.objects.active = ob; ob.select_set(True)
        bpy.ops.object.convert(target='MESH'); ob = bpy.context.active_object; ob.name = name
        me = ob.data; me.materials.clear(); me.materials.append(base)
        bm = bmesh.new(); bm.from_mesh(me)
        if globe:
            for _ in range(5):
                lg = [e for e in bm.edges if e.calc_length() > 8.0]
                if not lg: break
                bmesh.ops.subdivide_edges(bm, edges=lg, cuts=1, use_grid_fill=False)
                bmesh.ops.triangulate(bm, faces=bm.faces[:])
            R = 10.0
            for v in bm.verts:
                lo, la = math.radians(v.co.x), math.radians(v.co.y)
                v.co = Vector((R * math.cos(la) * math.sin(lo), -R * math.cos(la) * math.cos(lo), R * math.sin(la)))
        bm.to_mesh(me); bm.free()
        # espessura (azulejo) por solidify
        md = ob.modifiers.new('esp', 'SOLIDIFY'); md.thickness = -0.75 if globe else 0.9; md.offset = 1
        bpy.ops.object.modifier_apply(modifier='esp'); ob.select_set(False)
        if not globe: ob.scale = (1, 1, 1)
    # mar
    if globe:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=9.6, segments=96, ring_count=48, location=(0, 0, 0))
    else:
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, -0.5)); bpy.context.active_object.scale = (370, 190, 1)
    o = bpy.context.active_object; o.name = 'OCEANO'; o.data.materials.append(sea)
    # exporta (Z=cima do mapa -> Y-up do glTF: mapa deitado vira 'em pe' de frente; o motor gira)
    path = OUT + ('globo_paises.glb' if globe else 'mapa_mundi.glb')
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', export_yup=True, export_apply=True, export_cameras=False, export_lights=False)
    print('OK', path, os.path.getsize(path) // 1024, 'KB', len(bpy.data.objects), 'objetos')
build(globe=('--globo' in sys.argv))
