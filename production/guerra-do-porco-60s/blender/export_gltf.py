"""Blender SÓ como produtor de ativos 3D: monta a cena de uma edição (mesmo código de cenário/personagens do render Cycles), simplifica os materiais para PBR/unlit compatíveis com glTF
e exporta (a) scene.glb com TODOS os objetos e (b) frames.json com câmera, matrizes de mundo e visibilidade por quadro. O render é feito por three/render.js (Three.js headless).
Uso: python export_gltf.py <edição> <fps=15> <pasta_saída> [grass=20000] [t0 t1]"""
import sys, os, json, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import numpy as np
from mathutils import Matrix
from lib import util, renderlib, shots, anim
eid = sys.argv[1]; FPS = float(sys.argv[2]) if len(sys.argv) > 2 else 15; out = sys.argv[3]; grass = int(sys.argv[4]) if len(sys.argv) > 4 else 20000
os.makedirs(out, exist_ok=True)
util.reset(); sc = renderlib.setup((540, 960), samples=1)
shot = shots.SHOT_CLASSES[eid]({'grass': grass}); shot.build(); a, b = anim.EDIT[eid]; pad = .2
t0 = float(sys.argv[5]) if len(sys.argv) > 5 else a - pad; t1 = float(sys.argv[6]) if len(sys.argv) > 6 else b + pad
def simplify_materials():
    """cada material vira: textura (se houver imagem) | cor de vértice | cor base; sem nós procedurais (glTF não os exporta). Emissivos "cutout" viram unlit (Emission)."""
    for m in list(bpy.data.materials):
        if not m.use_nodes: continue
        nt = m.node_tree; img = next((n.image for n in nt.nodes if n.type == 'TEX_IMAGE' and n.image), None); vc = next((n for n in nt.nodes if n.type in ('ATTRIBUTE', 'VERTEX_COLOR')), None)
        bs = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None); em = next((n for n in nt.nodes if n.type == 'EMISSION' and n.inputs['Strength'].default_value >= 1 and n.outputs[0].is_linked is not None), None)
        col = tuple(bs.inputs['Base Color'].default_value) if bs else (.5, .5, .5, 1)
        if bs is None and em is not None: col = tuple(em.inputs['Color'].default_value)
        emis = float(bs.inputs['Emission Strength'].default_value) if bs else 0.0; metal = float(bs.inputs['Metallic'].default_value) if bs else 0
        glow = (bs is None) or (emis >= .2 and not vc)                         # cutouts (emissão própria) e brilhos → unlit
        if not bs and em is None: continue
        nt.nodes.clear(); o = nt.nodes.new('ShaderNodeOutputMaterial')
        if glow:
            e = nt.nodes.new('ShaderNodeEmission')
            if img: t = nt.nodes.new('ShaderNodeTexImage'); t.image = img; nt.links.new(t.outputs['Color'], e.inputs['Color'])
            else: e.inputs['Color'].default_value = col
            nt.links.new(e.outputs[0], o.inputs['Surface'])
        else:
            p = nt.nodes.new('ShaderNodeBsdfPrincipled'); p.inputs['Roughness'].default_value = .9; p.inputs['Metallic'].default_value = min(metal, .5)
            if img: t = nt.nodes.new('ShaderNodeTexImage'); t.image = img; nt.links.new(t.outputs['Color'], p.inputs['Base Color'])
            elif vc: c = nt.nodes.new('ShaderNodeVertexColor'); c.layer_name = 'Col'; nt.links.new(c.outputs['Color'], p.inputs['Base Color'])
            else: p.inputs['Base Color'].default_value = col
            nt.links.new(p.outputs[0], o.inputs['Surface'])
# animação por quadro: matrizes de mundo (só dos objetos que mudam) + visibilidade + câmera
shot_obs = [o for o in bpy.data.objects if o.type in ('MESH', 'EMPTY')]; last = {}; lastvis = {}; frames = []; t = t0; dt = 1.0 / FPS
orig = {}
while t < t1 - 1e-6:
    shot.update(t); bpy.context.view_layer.update(); d = {}; v = {}
    for o in shot_obs:
        m = [round(x, 5) for row in o.matrix_world for x in row]
        if last.get(o.name) != m: d[o.name] = m; last[o.name] = m
        hv = bool(o.hide_render)
        if lastvis.get(o.name) != hv: v[o.name] = hv; lastvis[o.name] = hv
    cam = shot.cam; frames.append(dict(t=round(t, 4), cam=[round(x, 5) for row in cam.matrix_world for x in row], fov=round(math.degrees(cam.data.angle), 4), m=d, hide=v)); t += dt
simplify_materials()   # DEPOIS de amostrar os quadros (props como Puff/Flash ainda usam seus nós)
for ob in bpy.data.objects: ob.hide_render = False; ob.hide_viewport = False                 # exporta TUDO; a visibilidade por quadro vai em frames.json
bpy.context.view_layer.update(); n_before = len(bpy.data.objects)
bpy.ops.export_scene.gltf(filepath=os.path.join(out, 'scene.glb'), export_format='GLB', export_cameras=False, export_lights=False, use_visible=False, export_apply=False, export_yup=True, export_vertex_color='ACTIVE', export_active_vertex_color_when_no_material=True)
sun = next((o for o in bpy.data.objects if o.type == 'LIGHT' and o.data.type == 'SUN'), None)
json.dump(dict(eid=eid, fps=FPS, t0=t0, frames=frames, sun=[round(x, 4) for x in sun.matrix_world.to_quaternion()] if sun else None, sun_energy=sun.data.energy if sun else 0,
               sun_color=list(sun.data.color) if sun else [1, 1, 1], objs=n_before), open(os.path.join(out, 'frames.json'), 'w'))
print('OK', eid, len(frames), 'quadros', os.path.getsize(os.path.join(out, 'scene.glb')) // 1024, 'KB glb')
