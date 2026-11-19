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
# ---- SALAS POR REGIAO (19/11: acabar com a "sala marrom" igual em todo video) ----
_R = {  # regiao: (madeira: parede, parede2, piso a, piso b, rodape/moldura) | pedra: (parede, parede2, piso a, piso b)
 'europa':  (('#f3ead2', '#e2d2ae', '#8a5a34', '#7a4a2a', '#4a2f1e'), ('#d9d2c4', '#c4bba8', '#9d968a', '#8a8378')),
 'franca':  (('#e9e2f0', '#cfc4e0', '#c9955a', '#b98448', '#f4f0e8'), ('#f4efe2', '#e6dcc4', '#efe9dc', '#2b2b30')),
 'holanda': (('#f4f0e8', '#dfe8f0', '#b9b4aa', '#2b2b30', '#3a5a8a'), ('#e8e4dc', '#d4cfc4', '#f4f0e8', '#2b2b30')),
 'eua':     (('#b9d4c4', '#9fc0ae', '#c9955a', '#b98448', '#f4f0e8'), ('#d4d8de', '#bcc2ca', '#9aa0a8', '#c8ccd2')),
 'oriente': (('#f2dcb0', '#e6c890', '#c9763a', '#a85a2a', '#3a6a8a'), ('#efe2c8', '#e2d0aa', '#3a8aa0', '#f2e6cc')),
 'colonial':(('#f6f1e6', '#e8c45a', '#a8603a', '#94502e', '#2f6a9a'), ('#f6f1e6', '#dfe8f0', '#c0603a', '#a8502e')),
 'japao':   (('#f4ead6', '#e6d6b4', '#c9b07a', '#b89c66', '#3a3a44'), ('#e8e0cc', '#d6cbb2', '#9a8a6a', '#8a7a5a')),
 'russia':  (('#f2e2c0', '#c8302a', '#8a5a34', '#7a4a2a', '#e8c45a'), ('#f4efe6', '#3a6ab8', '#b9b4aa', '#a59f94')),
 'africa':  (('#d9a46a', '#c98e5a', '#a86a3e', '#94582e', '#4a3020'), ('#e6c99a', '#d4b07c', '#b07a4a', '#a06a3a')),
 'classico':(('#f4efe2', '#c0603a', '#d9d2c4', '#c4bba8', '#8a3a2a'), ('#f1ece0', '#e2dccd', '#e8e2d4', '#c9c2b4')),
 'azul':    (('#cfe0f0', '#b4cce4', '#c9955a', '#b98448', '#f4f0e8'), ('#dfe8f0', '#c4d4e4', '#b9b4aa', '#a59f94')),
 'verde':   (('#d4e8c8', '#bcd8ac', '#b98448', '#a8733f', '#f4f0e8'), ('#e2ecd8', '#cadcbc', '#c4bba8', '#b0a894')),
 'rosa':    (('#f4d8d8', '#e8bcbc', '#c9955a', '#b98448', '#f4f0e8'), ('#f4e4e0', '#e8ccc4', '#efe9dc', '#d4ccbb')),
}
for rg, (wd, st) in _R.items():
    build(f'room_{rg}_wood', dict(bw=0.7, tile=False, floor=[wd[2], wd[3]], joint='#5a3a24', wall=wd[0], wall2=wd[1], base=wd[4], frame=wd[4], door='#a8733f', door2='#96642f'))
    build(f'room_{rg}_stone', dict(bw=1.3, tile=True, floor=[st[2], st[3]], joint='#5d584f', wall=st[0], wall2=st[1], base='#7d766a', frame='#5a4a3a', door='#7a5a3a', door2='#6a4c30'))
    build(f'room_{rg}_shop', dict(bw=1.1, tile=True, floor=[st[2], wd[2]], joint='#56727a', wall=wd[0], wall2=wd[1], base=wd[4], frame='#8b3a2a', door='#b9643a', door2='#a2532c', shop=True))
