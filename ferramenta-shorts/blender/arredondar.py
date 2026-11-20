# Tira o aspecto "quadradao" dos objetos: abre cada kit/*.glb, chanfra as quinas (bevel), alisa o sombreamento e grava de volta.
# uso: blender -b --python blender/arredondar.py -- [nome1 nome2 ...]   (sem nomes = todos os objetos do kit, menos salas/varandas)
# Rode depois de modelar qualquer objeto novo. E' seguro rodar de novo (objeto ja arredondado e' pulado: marca "arredondado" no nome da malha).
import bpy, sys, os, glob, math
KIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'web', 'assets', 'library', 'kit')
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
files = [os.path.join(KIT, a + '.glb') for a in args] if args else sorted(glob.glob(os.path.join(KIT, '*.glb')))
for f in files:
    nm = os.path.basename(f)[:-4]
    if nm.startswith(('room_', 'porch')) or not os.path.exists(f): continue
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=f)
    obs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    if not obs or any(o.data.name.startswith('arr_') for o in obs): print('PULA', nm); continue
    for o in obs:
        bpy.context.view_layer.objects.active = o; o.select_set(True)
        import bmesh; bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0005); bm.to_mesh(o.data); bm.free()   # o .glb vem com as faces soltas: solda antes de chanfrar
        d = max(o.dimensions) or 1.0
        m = o.modifiers.new('bv', 'BEVEL'); m.width = min(0.06, d * 0.035); m.segments = 3; m.limit_method = 'ANGLE'; m.angle_limit = math.radians(40); m.harden_normals = False
        bpy.ops.object.modifier_apply(modifier='bv')
        for p in o.data.polygons: p.use_smooth = True
        try: o.data.use_auto_smooth = True; o.data.auto_smooth_angle = math.radians(50)
        except Exception: pass
        o.data.name = 'arr_' + nm
    bpy.ops.export_scene.gltf(filepath=f, export_format='GLB', export_yup=True, export_apply=True, export_cameras=False, export_lights=False)
    print('OK', nm, sum(len(o.data.polygons) for o in obs))
