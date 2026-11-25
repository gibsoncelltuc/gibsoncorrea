# 24/11 (Gibson, Paris 1870): "nada de cabeca de elefante no restaurante: um bife bem grande no prato com uma plaquinha espetada: ELEFANTE".
# blender -b --python blender/objetos_paris.py  ->  web/assets/library/kit/bife_elefante.glb
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
import bpy, formas; _S = formas._S

novo('bife_elefante')
cil((0, 0.03, 0), 0.62, 0.05, '#f2f0ea', raio_topo=0.66)            # prato branco
cil((0, 0.065, 0), 0.5, 0.012, '#e2ded4')                            # fundo do prato
bola((0, 0.15, 0), 0.46, '#7a3a24', esc=(1.15, 0.34, 0.82))         # bife grande e grosso
bola((-0.05, 0.2, 0.05), 0.36, '#9a4a2e', esc=(1.0, 0.22, 0.72))    # parte de cima tostada
for x in (-0.25, 0.0, 0.25): caixa((x, 0.245, 0.05), (0.05, 0.012, 0.45), '#4a2216', rot=(0, 0, 0.5))   # marcas da grelha
tubo([(0.0, 0.18, 0.0), (0.0, 1.08, 0.0)], 0.014, '#d9c08a')      # palito espetado no meio, alto (a plaquinha fica acima das cabecas)
caixa((0.0, 0.98, 0.0), (0.66, 0.24, 0.02), '#ffffff')             # plaquinha branca centrada
# acabamento proprio: junta o texto "ELEFANTE" na plaquinha e exporta
bm = _S['bm']; me = bpy.data.meshes.new('red_bife'); bm.to_mesh(me); bm.free()
for m in _S['mats']: me.materials.append(m)
o = bpy.data.objects.new('bife_elefante', me); bpy.context.collection.objects.link(o)
bpy.ops.object.text_add(location=(0.0, -0.02, 0.96)); t = bpy.context.object; t.data.body = 'ELEFANTE'; t.data.size = 0.13; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.004
t.rotation_euler = (math.pi / 2, 0, 0)
mt = bpy.data.materials.new('txt'); mt.use_nodes = True; mt.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.55, 0.02, 0.02, 1); t.data.materials.append(mt)
bpy.ops.object.convert(target='MESH')
for x in bpy.context.selected_objects: x.select_set(False)
t.select_set(True); o.select_set(True); bpy.context.view_layer.objects.active = o; bpy.ops.object.join()
for p in o.data.polygons: p.use_smooth = True
bpy.ops.export_scene.gltf(filepath=OUT + 'bife_elefante.glb', export_format='GLB', export_yup=True, export_apply=True, export_cameras=False, export_lights=False)
print('OK bife_elefante', len(o.data.polygons))
