# Globo (formato countryballs): primeiro gera kit/globo_paises_tex.png (mapa equirretangular com contorno real, ver estudos/) e depois: blender -b --python blender/make_globo.py -> kit/globo_paises.glb (esfera lisa + textura; o motor pode REPINTAR a textura por pais para mostrar conquistas).
import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_uv_sphere_add(radius=10, segments=128, ring_count=64); o=bpy.context.active_object; o.name='GLOBO'
bpy.ops.object.shade_smooth()
m=bpy.data.materials.new('globo'); m.use_nodes=True; n=m.node_tree.nodes; b=n['Principled BSDF']; b.inputs['Roughness'].default_value=.45
t=n.new('ShaderNodeTexImage'); t.image=bpy.data.images.load('/home/user/gibsoncorrea/ferramenta-shorts/web/assets/library/kit/globo_paises_tex.png')
m.node_tree.links.new(t.outputs['Color'], b.inputs['Base Color']); o.data.materials.append(m)
bpy.ops.export_scene.gltf(filepath='/home/user/gibsoncorrea/ferramenta-shorts/web/assets/library/kit/globo_paises.glb', export_format='GLB', export_yup=True, export_cameras=False, export_lights=False)
