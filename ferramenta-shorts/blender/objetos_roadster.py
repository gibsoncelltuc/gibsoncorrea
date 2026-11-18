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
