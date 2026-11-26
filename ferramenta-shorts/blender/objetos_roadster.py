# Falcon Heavy no ar (subindo, com 3 chamas) a partir do kit/rocket da sessao B. blender -b --python blender/objetos_roadster.py
import sys, os, bpy; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
K = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'web', 'assets', 'library', 'kit')
novo('falcon_air')
for x in (-.7, 0, .7):
    torno((x, 3.4, 0), [(0, 0), (.22, .7), (.32, 1.6), (.28, 1.9)], '#ff8a1a', 18)
    torno((x, 3.9, 0), [(0, 0), (.16, .5), (.22, 1.4)], '#ffe14a', 18)
for (x, y, r) in ((-1.2, 3.0, .6), (1.2, 3.1, .55), (0, 2.8, .7), (-.5, 2.6, .5), (.6, 2.7, .5)): bola((x, y, 0), r, '#e8e4dc', seg=12)   # fumaca
fim(0.0)
fl = bpy.context.active_object
bpy.ops.import_scene.gltf(filepath=os.path.join(K, 'rocket.glb'))
for o in bpy.context.selected_objects:
    if o.parent is None: o.location.z += 5.3
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=os.path.join(K, 'falcon_air.glb'), export_format='GLB', use_selection=True)
novo('roadster_air')                               # Roadster 2026 pulando com propulsores de ar comprimido (jatos brancos para baixo)
for (x, z) in ((-.9, -.5), (.9, -.5), (-.9, .5), (.9, .5)): torno((x, 1.6, z), [(0, 0), (.18, .5), (.3, 1.1)], '#eef4ff', 14)
for (x, z) in ((-1.2, 0), (1.2, 0), (0, .8)): bola((x, 1.4, z), .35, '#f4f6fa', seg=10)
fim(0.0)
bpy.ops.import_scene.gltf(filepath=os.path.join(K, 'roadster.glb'))
for o in bpy.context.selected_objects:
    if o.parent is None: o.location.z += 2.7; o.scale = (1.4, 1.4, 1.4)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=os.path.join(K, 'roadster_air.glb'), export_format='GLB', use_selection=True)
novo('helicopter_air')                             # helicoptero ja voando (a partir de vehicles/helicopter)
bola((0, 0, 0), .001, '#000000')
fim(0.0)
bpy.ops.import_scene.gltf(filepath=os.path.join(K, '..', 'vehicles', 'helicopter.glb'))
for o in bpy.context.selected_objects:
    if o.parent is None: o.location.z += 4.5
for mt in bpy.data.materials:                     # pinta de militar: vermelho -> verde-oliva escuro
    if mt.use_nodes and 'Principled BSDF' in mt.node_tree.nodes:
        c = mt.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value
        if c[0] > c[1] * 1.5 and c[0] > c[2] * 1.5: c[0], c[1], c[2] = .04, .05, .03
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=os.path.join(K, 'helicopter_air.glb'), export_format='GLB', use_selection=True)
