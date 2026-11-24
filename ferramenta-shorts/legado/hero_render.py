"""Renderizador oficial de Hero Shots 3D no Blender para o Modo 3 da Ferramenta Shorts v10.
Uso: blender -b --python blender/hero_render.py -- <story_id>
Lê stories/<id>/hero_manifest.json e renderiza cada hero_shot em stories/<id>/blender_clips/bN.mp4 (1080x1920 @ 30fps).
"""
import json, os, sys, math
try:
    import bpy
except ImportError:
    print("Execute este script dentro do Blender: blender -b --python blender/hero_render.py -- <id>")
    sys.exit(1)

argv = sys.argv
sid = argv[argv.index('--') + 1] if '--' in argv else sys.exit("Informe o story_id apos '--'")
man = json.load(open(f'stories/{sid}/hero_manifest.json', encoding='utf-8'))
out_dir = f'stories/{sid}/blender_clips'
os.makedirs(out_dir, exist_ok=True)

for hs in man.get('hero_shots', []):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_EEVEE'
    sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
    sc.render.fps = 30
    dur = max(1.5, float(hs['t_end']) - float(hs['t_start']))
    sc.frame_start, sc.frame_end = 1, int(round(dur * 30))
    sc.render.image_settings.file_format = 'FFMPEG'
    sc.render.ffmpeg.format = 'MPEG4'
    sc.render.ffmpeg.codec = 'H264'
    sc.render.filepath = os.path.abspath(os.path.join(out_dir, f"{hs['beat']}.mp4"))

    # Iluminacao dramatica + camera cinematografica em arco
    bpy.ops.object.light_add(type='SUN', location=(6, -6, 12))
    bpy.context.active_object.data.energy = 4.5
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
    bpy.ops.object.camera_add(location=(0, -10, 3.2), rotation=(math.radians(78), 0, 0))
    cam = bpy.context.active_object
    sc.camera = cam
    cam.keyframe_insert(data_path='location', frame=1)
    cam.location = (1.8, -6.5, 4.4)
    cam.keyframe_insert(data_path='location', frame=sc.frame_end)
    bpy.ops.render.render(animation=True)
    print(f"[blender/hero_render] Renderizado {sc.render.filepath}")
