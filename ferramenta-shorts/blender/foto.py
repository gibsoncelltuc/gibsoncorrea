# Foto rapida de um ou mais .glb para conferir o FORMATO sem renderizar video: blender -b --python blender/foto.py -- saida.png a.glb b.glb ...
import bpy, sys, math, mathutils
a = sys.argv[sys.argv.index('--') + 1:]; out, files = a[0], a[1:]
bpy.ops.wm.read_factory_settings(use_empty=True); x = 0
for f in files:
    before = set(bpy.context.scene.objects); bpy.ops.import_scene.gltf(filepath=f); new = [o for o in bpy.context.scene.objects if o not in before]
    ms = [o for o in new if o.type == 'MESH']; pts = [o.matrix_world @ mathutils.Vector(c) for o in ms for c in o.bound_box]
    w = max(p.x for p in pts) - min(p.x for p in pts); cx = (max(p.x for p in pts) + min(p.x for p in pts)) / 2
    for o in new:
        if o.parent is None: o.location.x += x + w / 2 - cx
    x += w + 0.6
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 12; sc.cycles.device = 'CPU'; sc.cycles.use_denoising = False; sc.render.resolution_x = 1400; sc.render.resolution_y = 500
allp = [o.matrix_world @ mathutils.Vector(c) for o in sc.objects if o.type == 'MESH' for c in o.bound_box]; hz = max(p.z for p in allp)
cam = bpy.data.objects.new('c', bpy.data.cameras.new('c')); sc.collection.objects.link(cam); sc.camera = cam; cam.data.type = 'ORTHO'; cam.data.ortho_scale = max(x, hz * 2.9) * 1.05
cam.location = (x / 2 - 0.3 + x * 0.25, -x * 1.2 - 6, hz * 0.5 + x * 0.3); d = mathutils.Vector((x / 2 - 0.3, 0, hz * 0.45)) - cam.location; cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
sun = bpy.data.objects.new('s', bpy.data.lights.new('s', 'SUN')); sc.collection.objects.link(sun); sun.rotation_euler = (0.9, 0.2, 0.6); sun.data.energy = 3.5
w_ = bpy.data.worlds.new('w'); sc.world = w_; w_.use_nodes = True; w_.node_tree.nodes['Background'].inputs[0].default_value = (0.75, 0.82, 0.9, 1)
sc.render.filepath = out; bpy.ops.render.render(write_still=True); print('FOTO', out)
