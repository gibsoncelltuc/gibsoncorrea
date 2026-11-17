# Kit de INTERIOR (canal: 44% dos quadros sao interiores, parede a 2-8 m dos personagens, chao com tabuas/juntas desenhadas)
# blender -b --python blender/make_room.py  -> web/assets/library/kit/{room_wood,room_stone,room_shop}.glb   (y = cima, z+ = camera)
import bpy, bmesh, math
from mathutils import Vector
OUT = '/home/user/gibsoncorrea/ferramenta-shorts/web/assets/library/kit/'
def mat(name, hexc):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes = True; h = hexc.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    lin = [(x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4) for x in c]; b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (*lin, 1); b.inputs['Roughness'].default_value = 1; return m
G = lambda x, y, z: Vector((x, -z, y))
def build(name, P):
    bpy.ops.wm.read_factory_settings(use_empty=True); bm = bmesh.new(); mats = []
    def mi(m):
        if m not in mats: mats.append(m)
        return mats.index(m)
    def box(c, size, col):
        m = mat(name + col, col); r = bmesh.ops.create_cube(bm, size=1.0); k = mi(m)
        for v in r['verts']: v.co = G(v.co.x * size[0] + c[0], v.co.z * size[1] + c[1], -v.co.y * size[2] + c[2])
        for f in {f for v in r['verts'] for f in v.link_faces}: f.material_index = k
    W, D, H, zb = 30.0, 12.0, 24.0, -4.2                               # largura, profundidade, altura da parede, z da parede do fundo
    # chao: tabuas (ou lajotas) alternando dois tons com junta escura fina
    n = int(W / P['bw']); box((0, -0.06, zb + D / 2), (W, 0.1, D), P['joint'])
    for i in range(n):
        x = -W / 2 + (i + 0.5) * P['bw']
        if P['tile']:
            for j in range(int(D / P['bw'])): box((x, 0.0, zb + (j + 0.5) * P['bw']), (P['bw'] - 0.07, 0.06, P['bw'] - 0.07), P['floor'][(i + j) % 2])
        else: box((x, 0.0, zb + D / 2), (P['bw'] - 0.035, 0.06, D), P['floor'][i % 3 % 2 if i % 5 else 1])
    # paredes: fundo + duas laterais, rodape, faixa superior
    box((0, H / 2, zb - 0.15), (W, H, 0.3), P['wall']); box((0, 0.3, zb + 0.03), (W, 0.6, 0.08), P['base']); box((0, 4.4, zb + 0.02), (W, 0.12, 0.06), P['base'])
    box((0, (4.4 + H) / 2, zb + 0.01), (W, H - 4.4, 0.04), P['wall2'])
    for sx in (-1, 1): box((sx * (W / 2 + 0.15), H / 2, zb + D / 2), (0.3, H, D), P['wall2']); box((sx * (W / 2 - 0.02), 0.3, zb + D / 2), (0.08, 0.6, D), P['base'])
    # janela com caixilho em cruz e luz do dia
    wx = -4.6; box((wx, 3.1, zb + 0.05), (2.6, 2.6, 0.12), P['frame']); box((wx, 3.1, zb + 0.09), (2.2, 2.2, 0.1), '#bfe6f7'); box((wx, 3.1, zb + 0.13), (0.1, 2.2, 0.08), P['frame']); box((wx, 3.1, zb + 0.13), (2.2, 0.1, 0.08), P['frame']); box((wx, 1.72, zb + 0.2), (2.9, 0.14, 0.4), P['frame'])
    # porta com almofadas e macaneta
    dx = 5.2; box((dx, 2.0, zb + 0.05), (2.1, 4.0, 0.12), P['frame']); box((dx, 1.95, zb + 0.1), (1.7, 3.7, 0.1), P['door']); box((dx, 2.9, zb + 0.14), (1.2, 1.2, 0.06), P['door2']); box((dx, 1.1, zb + 0.14), (1.2, 1.4, 0.06), P['door2']); box((dx - 0.62, 1.95, zb + 0.2), (0.14, 0.14, 0.12), '#e8c45a')
    # quadros na parede
    for qx, qc in ((0.4, '#d96a4a'), (2.4, '#5a8fd0')): box((qx, 3.6, zb + 0.05), (1.3, 1.6, 0.1), P['frame']); box((qx, 3.6, zb + 0.09), (1.0, 1.3, 0.08), qc); box((qx, 3.3, zb + 0.12), (1.0, 0.5, 0.06), '#f2e6c4')
    if P.get('shop'):                                                  # balcao e prateleiras com produtos
        box((0.5, 0.7, zb + 2.0), (7.0, 1.4, 1.1), P['door']); box((0.5, 1.45, zb + 2.0), (7.3, 0.14, 1.3), P['frame'])
        for sy in (4.6, 5.5): box((1.4, sy, zb + 0.4), (5.0, 0.12, 0.6), P['frame']); [box((-0.8 + i * 0.62, sy + 0.32, zb + 0.4), (0.36, 0.5, 0.36), ['#e2453c', '#f2b632', '#4a9a5a', '#5a8fd0'][i % 4]) for i in range(8)]
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in mats: me.materials.append(m)
    o = bpy.data.objects.new('room', me); bpy.context.collection.objects.link(o)
    bpy.ops.export_scene.gltf(filepath=OUT + name + '.glb', export_format='GLB', export_yup=True, export_apply=True, export_cameras=False, export_lights=False); print('OK', name, len(me.polygons))
build('room_wood', dict(bw=0.7, tile=False, floor=['#c9955a', '#b98448'], joint='#7a5230', wall='#f2dfb8', wall2='#e9cf9c', base='#8b5a34', frame='#7a4a2a', door='#a8733f', door2='#96642f'))
build('room_stone', dict(bw=1.3, tile=True, floor=['#b9b4aa', '#a59f94'], joint='#5d584f', wall='#cfc8bb', wall2='#bdb5a6', base='#7d766a', frame='#5a4a3a', door='#7a5a3a', door2='#6a4c30'))
build('room_shop', dict(bw=1.1, tile=True, floor=['#f1ece0', '#7fb9c9'], joint='#56727a', wall='#ffe9a8', wall2='#f6c95a', base='#c8402f', frame='#8b3a2a', door='#b9643a', door2='#a2532c', shop=True))
