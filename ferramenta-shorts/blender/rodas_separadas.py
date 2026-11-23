# 23/11: separa as RODAS dos carros do kit em nos proprios ("wheelz_*") para girarem no motor conforme o carro anda (antes eram uma peca so': roda parada).
# blender -b --python blender/rodas_separadas.py   (originais guardados em web/assets/library/kit/_orig_veic/)
import bpy, bmesh, os, mathutils
K = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'web', 'assets', 'library', 'kit')
NOMES = ['carro_redondo', 'carro_50', 'carro_antigo', 'roadster', 'roadster26', 'cybertruck', 'roadster_air', 'roadster26_air']
def bb(o):
    ps = [o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    return mathutils.Vector((min(p.x for p in ps), min(p.y for p in ps), min(p.z for p in ps))), mathutils.Vector((max(p.x for p in ps), max(p.y for p in ps), max(p.z for p in ps)))
for n in NOMES:
    src = os.path.join(K, '_orig_veic', n + '.glb')
    if not os.path.exists(src): continue
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=src)
    ms = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    for o in ms: o.select_set(True)
    bpy.context.view_layer.objects.active = ms[0]
    for o in ms:
        bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active = o
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    allb = [bb(o) for o in ms]; mn = mathutils.Vector([min(b[0][i] for b in allb) for i in range(3)]); mx = mathutils.Vector([max(b[1][i] for b in allb) for i in range(3)])
    H = mx.z - mn.z; cx = (mn.x + mx.x) / 2; cy = (mn.y + mx.y) / 2
    # rodas ficam no terco de baixo do CARRO (o roadster_air tem jatos embaixo: a "base" do carro e' o topo dos jatos)
    parts = []
    for o in ms:
        bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active = o
        bpy.ops.mesh.separate(type='LOOSE')
        parts += [p for p in bpy.context.selected_objects]
    wheels = {}
    for p in parts:
        a, b = bb(p); c = (a + b) / 2; d = b - a
        if d.x < 0.08 or d.z < 0.08: continue
        round_ = abs(d.x - d.z) / max(d.x, d.z) < 0.25           # circulo visto de lado (x-z)
        thin = d.y < 0.75 * max(d.x, d.z)                          # fina na largura do carro
        small = max(d.x, d.z) < 0.42 * (mx.x - mn.x)
        offc = abs(c.x - cx) > 0.12 * (mx.x - mn.x)               # perto da frente ou de tras (nao no meio)
        if round_ and thin and small and offc:
            key = ('F' if c.x > cx else 'T') + ('E' if c.y > cy else 'D')
            wheels.setdefault(key, []).append(p)
    # anexa calota/pneu/aro concentricos que nao passaram no teste mas estao dentro do circulo de uma roda
    for p in parts:
        if any(p in v for v in wheels.values()): continue
        a, b = bb(p); c = (a + b) / 2; d = b - a
        for key, ws in wheels.items():
            wa, wb = bb(ws[0]); wc = (wa + wb) / 2; wd = wb - wa
            if abs(c.x - wc.x) < 0.12 * wd.x and abs(c.z - wc.z) < 0.12 * wd.z and abs(c.y - wc.y) < max(wd.y, 0.3) and max(d.x, d.z) <= wd.x * 1.02: ws.append(p); break
    if len(wheels) < 4:
        print('SEM_RODAS', n, len(wheels)); continue
    body = [p for p in parts if not any(p in v for v in wheels.values())]
    for key, ws in wheels.items():
        bpy.ops.object.select_all(action='DESELECT')
        for p in ws: p.select_set(True)
        bpy.context.view_layer.objects.active = ws[0]; bpy.ops.object.join(); w = bpy.context.view_layer.objects.active
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS'); w.name = 'wheelz_' + key; w.data.name = 'wheelz_' + key + '_m'
    bpy.ops.object.select_all(action='DESELECT')
    for p in body: p.select_set(True)
    bpy.context.view_layer.objects.active = body[0]; bpy.ops.object.join(); bpy.context.view_layer.objects.active.name = n
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(filepath=os.path.join(K, n + '.glb'), export_format='GLB', use_selection=True)
    print('RODAS_OK', n, sorted(wheels), [len(v) for v in wheels.values()])
