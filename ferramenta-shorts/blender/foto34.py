# Foto 3/4 DE CIMA de um .glb (comparativo referencia x modelo: mostra o formato por dentro, como nas fotos de museu).
# blender -b --python blender/foto34.py -- saida.png objeto.glb
import bpy, sys, math, mathutils
out, f = sys.argv[sys.argv.index('--') + 1:][:2]
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=f)
sc = bpy.context.scene; ms = [o for o in sc.objects if o.type == 'MESH']; pts = [o.matrix_world @ mathutils.Vector(c) for o in ms for c in o.bound_box]
lo = mathutils.Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts))); hi = mathutils.Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
c = (lo + hi) / 2; r = (hi - lo).length / 2
sc.render.engine = 'CYCLES'; sc.cycles.samples = 16; sc.cycles.device = 'CPU'; sc.cycles.use_denoising = False; sc.render.resolution_x = 760; sc.render.resolution_y = 520
cam = bpy.data.objects.new('c', bpy.data.cameras.new('c')); sc.collection.objects.link(cam); sc.camera = cam; cam.data.lens = 50
cam.location = c + mathutils.Vector((r * 1.6, -r * 2.6, r * 2.0)); cam.rotation_euler = (c - cam.location).to_track_quat('-Z', 'Y').to_euler()
sun = bpy.data.objects.new('s', bpy.data.lights.new('s', 'SUN')); sc.collection.objects.link(sun); sun.rotation_euler = (0.7, 0.2, 0.5); sun.data.energy = 3.0
w_ = bpy.data.worlds.new('w'); sc.world = w_; w_.use_nodes = True; w_.node_tree.nodes['Background'].inputs[0].default_value = (0.75, 0.78, 0.82, 1)
sc.render.filepath = out; bpy.ops.render.render(write_still=True); print('FOTO', out)
