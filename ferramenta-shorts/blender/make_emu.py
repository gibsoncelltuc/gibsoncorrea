# Emu estilizado (desenho animado, felpudo) -> web/assets/emu.glb.   blender -b --python blender/make_emu.py
# Convencao do motor (web/core.js): nos raiz com NOMES que o motor anima: body, neckp (pescoco; filho: head), legL/legR (quadril; filho: shinL/shinR = joelho).
# Coordenadas escritas em glTF (x direita, y cima, z frente do bicho) e convertidas para Blender: (x, -z, y).
import bpy, bmesh, math, random
from mathutils import Vector, Matrix
random.seed(7)
bpy.ops.wm.read_factory_settings(use_empty=True)
def mat(name, hexc):
    m = bpy.data.materials.new(name); m.use_nodes = True; h = hexc.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    lin = [(x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4) for x in c]; b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (*lin, 1); b.inputs['Roughness'].default_value = 1; return m
M = {k: mat(k, v) for k, v in dict(fd='#6e4c33', f1='#92683f', f2='#b38650', f3='#d2ac72', neck='#8d9fae', neck2='#a9b8c4', beak='#5a4e44', eye='#ffd23a', pup='#15110e', leg='#b9a998', toe='#3e342c', white='#fffdf6').items()}
G = lambda x, y, z: Vector((x, -z, y))                       # glTF -> Blender
parts = {}
class Part:
    def __init__(s, name, joint, parent=None):
        s.name, s.joint, s.parent = name, Vector(joint), parent; s.bm = bmesh.new(); s.mats = []; parts[name] = s
    def mi(s, m):
        if m not in s.mats: s.mats.append(m)
        return s.mats.index(m)
    def blob(s, c, r, m, seg=10, rings=7, rot=None):            # elipsoide centrado em c (coordenadas de mundo glTF), raios r=(rx,ry,rz)
        bmesh.ops.create_uvsphere(s.bm, u_segments=seg, v_segments=rings, radius=1.0)
        new = [v for v in s.bm.verts if not v.tag]; mi = s.mi(m)
        for v in new: v.tag = True; v.co = Vector((v.co.x * r[0], v.co.y * r[2], v.co.z * r[1]))   # (x, z_b, y_b) em espaco local glTF
        # v.co agora esta em (x, y_gltf=co.z*ry, z_gltf = co.y*rz) -> reordena para blender: (x, -zg, yg)
        for v in new:
            xg, yg, zg = v.co.x, v.co.z, v.co.y
            if rot: q = Vector((xg, yg, zg)); q.rotate(rot); xg, yg, zg = q
            v.co = G(xg + c[0] - s.joint.x, yg + c[1] - s.joint.y, zg + c[2] - s.joint.z)
        for f in s.bm.faces:
            if all(v in new for v in f.verts): f.material_index = mi; f.smooth = True
    def tube(s, a, b, r0, r1, m, seg=8, cap=True):                          # tronco de cone entre dois pontos glTF
        a, b = Vector(a), Vector(b); d = b - a; L = d.length
        bmesh.ops.create_cone(s.bm, cap_ends=cap, segments=seg, radius1=r0, radius2=r1, depth=L)
        new = [v for v in s.bm.verts if not v.tag]; mi = s.mi(m)
        q = Vector((0, 0, 1)).rotation_difference(Vector((d.x, -d.z, d.y)).normalized()).to_matrix().to_4x4()      # eixo do cone (z) -> direcao em Blender
        mid = G(*((a + b) / 2)) - G(*s.joint)
        for v in new: v.tag = True; v.co = q @ v.co + mid
        for f in s.bm.faces:
            if all(v in new for v in f.verts): f.material_index = mi; f.smooth = True
def feather(p, base, dirv, L, w, m, seg=8, rings=5):                              # pena = elipsoide alongado apontando em dirv
    d = Vector(dirv).normalized(); c = Vector(base) + d * L * .5
    up = Vector((0, 1, 0)) if abs(d.y) < .9 else Vector((1, 0, 0)); q = Vector((0, 0, 1)).rotation_difference(d)
    p.blob(c, (w, w * .7, L * .5), m, seg=seg, rings=rings, rot=q)
# ---------------- corpo felpudo ----------------
body = Part('body', (0, 1.15, 0))
body.blob((0, 1.15, -0.05), (0.5, 0.58, 0.82), M['f1'], 14, 9)
for i in range(42):                                              # penas em camadas
    th, ph = random.uniform(0, math.tau), math.acos(random.uniform(-.85, .75)); nx, ny, nz = math.sin(ph) * math.cos(th), math.cos(ph), math.sin(ph) * math.sin(th)
    pos = Vector((0 + .5 * nx, 1.15 + .58 * ny, -0.05 + .82 * nz)); out = Vector((nx, ny, nz)); dirv = (out * .55 + Vector((0, -.45, -.8))).normalized()
    m = random.choice([M['fd'], M['f1'], M['f1'], M['f1'], M['f2'], M['f2']]); feather(body, pos * 0.96 + Vector((0, 0.02, 0)), dirv, random.uniform(.45, .7), random.uniform(.16, .21), m)
for i in range(16):                                               # pluma da garupa
    a = random.uniform(-.9, .9); feather(body, Vector((a * .25, 1.35 + random.uniform(-.1, .15), -0.8)), Vector((a * .35, -.35, -1)), random.uniform(.35, .55), .09, random.choice([M['f2'], M['f3'], M['f1']]))
for i in range(10):                                               # peito mais claro
    a = random.uniform(-.6, .6); feather(body, Vector((a * .4, 1.05 + random.uniform(-.15, .2), 0.72)), Vector((a * .4, -.4, .5)), random.uniform(.16, .26), .07, M['f3'])
# ---------------- pescoco (+ cabeca) ----------------
neck = Part('neckp', (0, 1.55, 0.6))
pts = [(0, 1.55, 0.6), (0, 1.8, 0.78), (0, 2.05, 0.86), (0, 2.28, 0.98)]; rs = [0.15, 0.12, 0.095, 0.085]
def bez(t): return [ (1-t)**3*a + 3*(1-t)**2*t*b + 3*(1-t)*t*t*c + t**3*d for a,b,c,d in zip((0,1.55,0.6),(0,1.95,0.55),(0,2.15,1.0),(0,2.28,0.98)) ]
N = 44
for i in range(N + 1): t = i / N; neck.blob(bez(t), (0.15 - 0.065 * t,) * 3, M['neck'], 12, 8)
head = Part('head', (0, 2.3, 1.0), neck)
head.blob((0, 2.32, 1.03), (0.12, 0.11, 0.17), M['neck'], 12, 8)
head.blob((0, 2.27, 1.22), (0.07, 0.045, 0.17), M['beak'], 10, 6); head.blob((0, 2.31, 1.17), (0.085, 0.05, 0.14), M['beak'], 10, 6)
for sx in (-1, 1):
    head.blob((sx * .09, 2.36, 1.06), (.055, .065, .055), M['white'], 12, 8); head.blob((sx * .125, 2.36, 1.095), (.034, .042, .034), M['pup'], 8, 6)
for i in range(7): feather(head, Vector((random.uniform(-.06, .06), 2.43, 0.94)), Vector((random.uniform(-.3, .3), .6, -.6)), random.uniform(.1, .18), .02, M['fd'])
# ---------------- pernas ----------------
legs = {}
for nm, sx in (('L', 1), ('R', -1)):
    hip = (sx * .24, 1.02, -0.18); knee = (sx * .24, 0.58, -0.12)
    th = Part('leg' + nm, hip); th.blob((sx * .24, 0.86, -0.17), (.17, .26, .19), M['f1'], 10, 7)
    for i in range(10): feather(th, Vector((sx * .24 + random.uniform(-.1, .1), 1.0 - random.uniform(0, .28), -0.17 + random.uniform(-.12, .08))), Vector((random.uniform(-.2, .2), -.5, -.8)), random.uniform(.13, .22), .06, random.choice([M['f1'], M['f2'], M['fd']]))
    th.tube((sx * .24, 0.78, -0.16), knee, .075, .06, M['leg'])
    sh = Part('shin' + nm, knee, th); sh.blob(knee, (.065, .065, .065), M['leg'], 8, 6)
    sh.tube(knee, (sx * .24, 0.1, -0.2), .055, .04, M['leg']); sh.blob((sx * .24, 0.08, -0.17), (.08, .05, .1), M['toe'], 8, 6)
    for ang, ln in ((-.35, .24), (0, .3), (.35, .24)):
        d = (math.sin(ang), -.05, math.cos(ang)); a = Vector((sx * .24, .07, -0.17)); b = a + Vector(d) * ln
        sh.tube(a, b, .045, .018, M['toe'], 6); sh.blob(b + Vector((0, -.005, .01)), (.025, .02, .035), M['toe'], 6, 4)
# ---------------- constroi objetos ----------------
objs = {}
for name, p in parts.items():
    me = bpy.data.meshes.new(name); p.bm.normal_update(); p.bm.to_mesh(me); p.bm.free()
    for m in p.mats: me.materials.append(m)
    o = bpy.data.objects.new(name, me); o.location = G(*p.joint); bpy.context.collection.objects.link(o); objs[name] = o
for name, p in parts.items():
    if p.parent: o = objs[name]; o.parent = objs[p.parent.name]; o.location = G(*(p.joint - p.parent.joint)); 
bpy.ops.export_scene.gltf(filepath='/home/user/gibsoncorrea/ferramenta-shorts/web/assets/emu.glb', export_format='GLB', export_yup=True, export_apply=True, export_materials='EXPORT', export_cameras=False, export_lights=False)
print('EMU OK', {n: len(o.data.polygons) for n, o in objs.items()})
