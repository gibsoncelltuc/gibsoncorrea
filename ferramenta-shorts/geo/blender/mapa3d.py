# Mapa 3D estilizado (paises em relevo, chanfro, sombra suave, mar com ondinhas) renderizado de cima em ortografica.
# uso: blender -b -P mapa3d.py -- <roteiro.json> <saida.png> <largura_px>
import bpy, bmesh, json, math, sys
a = sys.argv[sys.argv.index('--') + 1:]; R = json.load(open(a[0])); OUT = a[1]; PX = int(a[2])
L0, L1, A0, A1 = R['mapa']; K = math.cos(math.radians((A0 + A1) / 2))
GJ = json.load(open(__file__.rsplit('/', 2)[0] + '/dados/paises.geojson'))['features']
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
def mat(nome, cor, rough=.55):
    m = bpy.data.materials.new(nome); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*[(c / 255) ** 2.2 for c in cor], 1); b.inputs['Roughness'].default_value = rough; return m
cores = R.get('cores', {}); padrao = R.get('cor_terra', [236, 226, 196])
for f in GJ:
    code = f['properties']['ADM0_A3']; g = f['geometry']; polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
    for p in polys:
        ring = p[0]
        if max(x for x, _ in ring) < L0 - 5 or min(x for x, _ in ring) > L1 + 5 or max(y for _, y in ring) < A0 - 5 or min(y for _, y in ring) > A1 + 5: continue
        bm = bmesh.new(); vs = [bm.verts.new(((x - L0) * K, y - A0, 0)) for x, y in ring[:-1]]
        try:
            fc = bm.faces.new(vs); fc.normal_update()
            if fc.normal.z < 0: fc.normal_flip()
        except Exception: bm.free(); continue
        me = bpy.data.meshes.new(code); bm.to_mesh(me); bm.free(); ob = bpy.data.objects.new(code, me); sc.collection.objects.link(ob)
        s = ob.modifiers.new('s', 'SOLIDIFY'); s.thickness = R.get('relevo', .06); s.offset = 1
        bv = ob.modifiers.new('b', 'BEVEL'); bv.width = R.get('relevo', .06) * .6; bv.segments = 3; bv.limit_method = 'ANGLE'
        ob.data.materials.append(mat(code, cores.get(code, padrao)))
for i, ex in enumerate(R.get('extras', [])):   # ilhas/territorios a mais (ex.: ilha disputada), um pouco mais altos
    bm = bmesh.new(); vs = [bm.verts.new(((x - L0) * K, y - A0, 0)) for x, y in ex['pts']]; fc = bm.faces.new(vs); fc.normal_update()
    if fc.normal.z < 0: fc.normal_flip()
    me = bpy.data.meshes.new('ex%d' % i); bm.to_mesh(me); bm.free(); ob = bpy.data.objects.new('ex%d' % i, me); sc.collection.objects.link(ob)
    s_ = ob.modifiers.new('s', 'SOLIDIFY'); s_.thickness = R.get('relevo', .06) * 1.6; s_.offset = 1; b_ = ob.modifiers.new('b', 'BEVEL'); b_.width = R.get('relevo', .06) * .7; b_.segments = 3
    ob.data.materials.append(mat('ex%d' % i, ex['cor']))
# mar: plano com ruido leve (ondinhas) em azul vivo
W, H = (L1 - L0) * K, A1 - A0
bpy.ops.mesh.primitive_plane_add(size=1, location=(W / 2, H / 2, -.01)); mar = bpy.context.object; mar.scale = (W * 1.2, H * 1.2, 1)
m = mat('mar', R.get('cor_mar', [96, 178, 236]), .35); nt = m.node_tree; nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 18; nz.inputs['Detail'].default_value = 2
cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = .4; cr.color_ramp.elements[1].position = .75
c0 = [(c / 255) ** 2.2 for c in R.get('cor_mar', [96, 178, 236])]; cr.color_ramp.elements[0].color = (*c0, 1); cr.color_ramp.elements[1].color = (*[min(1, x * 1.12 + .015) for x in c0], 1)
nt.links.new(nz.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], nt.nodes['Principled BSDF'].inputs['Base Color']); mar.data.materials.append(m)
# luz: sol inclinado (sombra a direita-baixo) + ceu claro
bpy.ops.object.light_add(type='SUN', rotation=(math.radians(38), 0, math.radians(35))); sol = bpy.context.object; sol.data.energy = 4.0; sol.data.angle = math.radians(8)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Color'].default_value = (.75, .82, 1, 1); w.node_tree.nodes['Background'].inputs['Strength'].default_value = .9
bpy.ops.object.camera_add(location=(W / 2, H / 2, 10)); cam = bpy.context.object; cam.data.type = 'ORTHO'; cam.data.ortho_scale = max(W, H); sc.camera = cam
sc.render.resolution_x = PX; sc.render.resolution_y = int(PX * H / W); sc.render.engine = 'CYCLES'; sc.cycles.samples = 24; sc.cycles.use_denoising = False; sc.cycles.device = 'CPU'
sc.view_settings.view_transform = 'Standard'; sc.render.filepath = OUT; bpy.ops.render.render(write_still=True)
