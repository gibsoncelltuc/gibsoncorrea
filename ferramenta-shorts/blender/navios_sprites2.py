# 26/11 v2 dos modelos de GUERRA (mais detalhe): porta-avioes da 2a Guerra e avioes de mergulho/caca com insignia certa.
# Render em 16 rumos (vista 3/4 de cima, estilo Age of Empires) em geo/dados/sprites/<nome>_<k>.png
import bpy, bmesh, math, os
from mathutils import Vector
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'geo', 'dados', 'sprites') + os.sep; os.makedirs(OUT, exist_ok=True)
def hexc(h): h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]; return [(x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4) for x in c]
def mat(nome, cor, rough=.55, metal=0.0):
    m = bpy.data.materials.get(nome) or bpy.data.materials.new(nome); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*hexc(cor), 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal; return m
def madeira():   # conves de tabuas: textura procedural (ondas) para as linhas das tabuas
    m = bpy.data.materials.new('conves'); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    wv = nt.nodes.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'Y'; wv.inputs['Scale'].default_value = 30; wv.inputs['Distortion'].default_value = 1.5
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (*hexc('#6e5232'), 1); cr.color_ramp.elements[1].color = (*hexc('#a48056'), 1)
    nt.links.new(wv.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], b.inputs['Base Color']); b.inputs['Roughness'].default_value = .8; return m
def caixa(loc, dim, m, rot=(0, 0, 0), bev=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.active_object; o.scale = dim; o.data.materials.append(m)
    if bev: bpy.ops.object.transform_apply(scale=True); b = o.modifiers.new('b', 'BEVEL'); b.width = bev; b.segments = 2
    return o
def cil(loc, r, h, m, rot=(0, 0, 0), v=16, r2=None):
    bpy.ops.mesh.primitive_cone_add(vertices=v, radius1=r, radius2=r if r2 is None else r2, depth=h, location=loc, rotation=rot); o = bpy.context.active_object; o.data.materials.append(m); return o
def bola(loc, r, m, esc=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=20, ring_count=12); o = bpy.context.active_object; o.scale = esc; o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o
def casco(L, B, D, m):
    # casco de navio: secoes em U ao longo do comprimento, proa afilada e alteada (bow flare), popa reta
    bm = bmesh.new(); secs = []; N = 24
    for i in range(N + 1):
        t = i / N; x = -L / 2 + L * t
        larg = B / 2 * (min(1, (t / .08) ** .3) if t < .08 else (1 if t < .62 else (1 - ((t - .62) / .38) ** 1.7)))
        larg = max(larg, .02); top = D * (1 + .35 * max(0, (t - .8) / .2) ** 2)
        pts = [(-larg, top), (-larg * .98, D * .1), (-larg * .7, -D * .55), (0, -D * .7), (larg * .7, -D * .55), (larg * .98, D * .1), (larg, top)]
        secs.append([bm.verts.new((x, y, z)) for y, z in pts])
    for a, b in zip(secs, secs[1:]):
        for j in range(len(a) - 1): bm.faces.new((a[j], a[j + 1], b[j + 1], b[j]))
    bm.faces.new(list(reversed(secs[0]))); me = bpy.data.meshes.new('casco'); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('casco', me); bpy.context.collection.objects.link(o); o.data.materials.append(m)
    for p in me.polygons: p.use_smooth = True
    return o
def limpar(): bpy.ops.wm.read_factory_settings(use_empty=True)

def aviao_modelo(cor, insignia, loc=(0, 0, 0), esc=1.0, rot=0.0, so_corpo=False):
    c = mat('fus' + cor, cor, .45, .15); vid = mat('vidro', '#8fc6ee', .05, .6); preto = mat('preto', '#202022', .4, .3); objs = []
    x0, y0, z0 = loc
    def P(x, y, z): ca, sa = math.cos(rot), math.sin(rot); return (x0 + (x * ca - y * sa) * esc, y0 + (x * sa + y * ca) * esc, z0 + z * esc)
    f = bola(P(0, 0, 0), .5, c, (2.3 * esc, .42 * esc, .42 * esc)); f.rotation_euler = (0, 0, rot); objs.append(f)                      # fuselagem arredondada
    objs.append(cil(P(1.12, 0, 0), .2 * esc, .22 * esc, preto, rot=(0, math.pi / 2, rot)))                                                 # capo do motor
    w = bola(P(.15, 0, -.08), .5, c, (.55 * esc, 2.6 * esc, .05 * esc)); w.rotation_euler = (0, 0, rot); objs.append(w)                     # asas com ponta arredondada
    t = bola(P(-1.0, 0, .02), .5, c, (.28 * esc, .95 * esc, .035 * esc)); t.rotation_euler = (0, 0, rot); objs.append(t)                   # estabilizador
    v = bola(P(-1.02, 0, .22), .5, c, (.32 * esc, .035 * esc, .42 * esc)); v.rotation_euler = (0, 0, rot); objs.append(v)                   # leme
    if not so_corpo:
        cv = bola(P(.2, 0, .17), .5, vid, (.62 * esc, .22 * esc, .2 * esc)); cv.rotation_euler = (0, 0, rot); objs.append(cv)               # cabine de vidro
        h = caixa(P(1.25, 0, 0), (.02 * esc, .95 * esc, .07 * esc), preto, rot=(0, 0, rot)); objs.append(h)                                 # helice
    for s in (-1, 1):   # insignia em cima das asas
        if insignia == 'us':
            objs.append(cil(P(.15, s * .85, -.04), .2 * esc, .02 * esc, mat('az', '#1d3a7a'), v=24))
            cx, cy, cz = P(.15, s * .85, -.025); me = bpy.data.meshes.new('estrela'); bm = bmesh.new()   # estrela de 5 pontas
            vs = [bm.verts.new((cx + (.15 if k % 2 == 0 else .06) * esc * math.cos(rot + math.pi / 2 + k * math.pi / 5), cy + (.15 if k % 2 == 0 else .06) * esc * math.sin(rot + math.pi / 2 + k * math.pi / 5), cz)) for k in range(10)]
            bm.faces.new(vs); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new('estrela', me); bpy.context.collection.objects.link(o); o.data.materials.append(mat('br', '#f2f2f2')); objs.append(o)
        else: objs.append(cil(P(.15, s * .85, -.04), .19 * esc, .02 * esc, mat('vm', '#c81e26'), v=24))
    return objs

def porta_avioes():
    limpar(); cinza = mat('cinza', '#5f666d', .5, .35); claro = mat('claro', '#7c838a', .5, .3); verm = mat('verm', '#6e2420', .7); escuro = mat('esc', '#2e3237', .4, .4); br = mat('br2', '#e8e8e8', .7)
    casco(10, 1.7, .9, cinza)
    caixa((-.2, 0, -.5), (9.0, 1.2, .14), verm)                                                                    # linha d'agua
    caixa((.0, 0, .98), (10.6, 2.0, .1), madeira(), bev=.02)                                                       # convés de voo
    for x in (-3.8, -1.2, 1.4, 3.8): caixa((x, 0, 1.04), (.55, .05, .005), br)
    caixa((4.6, 0, 1.04), (.9, .05, .005), br); caixa((-5.1, 0, 1.04), (.06, 1.8, .005), br)
    for s in (-1, 1):                                                                                             # galerias de canhao nas laterais
        for x in (-3.5, -1, 2.5): caixa((x, s * 1.02, .8), (.7, .22, .08), claro); cil((x, s * 1.08, .92), .04, .3, escuro, rot=(math.pi / 2.6 * s, 0, 0), v=8)
    caixa((.9, .82, 1.55), (1.8, .34, 1.0), claro, bev=.03); caixa((.7, .82, 2.15), (.9, .3, .35), claro, bev=.03)   # ilha + ponte
    for k in range(5): caixa((.3 + k * .2, .64, 2.2), (.12, .01, .08), escuro)                                     # janelas da ponte
    cil((1.5, .82, 2.3), .2, .8, escuro, rot=(0, .25, 0), v=12)                                                    # chamine inclinada
    cil((.4, .82, 2.8), .025, 1.3, escuro, v=6); caixa((.4, .82, 3.2), (.6, .03, .03), escuro); caixa((.4, .82, 3.35), (.15, .35, .08), escuro)   # mastro e radar
    for i in range(3):
        for j, y in enumerate((-.5, .25)): aviao_modelo('#4c5c70', 'us', loc=(-4.2 + i * 1.0, y, 1.12), esc=.38, rot=math.pi * (0 if j else .05))
    return 6.0

def aviao(nome, cor, ins):
    limpar(); aviao_modelo(cor, ins); return 1.45

def render(nome, raio, angulos=16, tam=448, el=50):
    sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 48; sc.cycles.use_denoising = False; sc.cycles.device = 'CPU'; sc.render.film_transparent = True
    sc.render.resolution_x = sc.render.resolution_y = tam; sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Color'].default_value = (.55, .68, .9, 1); w.node_tree.nodes['Background'].inputs['Strength'].default_value = 1.0
    bpy.ops.object.light_add(type='SUN'); s = bpy.context.active_object; s.data.energy = 4.5; s.rotation_euler = (math.radians(38), 0, math.radians(35)); s.data.angle = math.radians(3)
    objs = [o for o in sc.objects if o.type == 'MESH']; piv = bpy.data.objects.new('piv', None); sc.collection.objects.link(piv)
    for o in objs: o.parent = piv
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam; cam.data.type = 'ORTHO'; cam.data.ortho_scale = raio * 2.2
    e = math.radians(el); d = 30; cam.location = (0, -d * math.cos(e), d * math.sin(e)); cam.rotation_euler = (math.radians(90) - e, 0, 0)
    for k in range(angulos):
        piv.rotation_euler = (0, 0, -k * 2 * math.pi / angulos); sc.render.filepath = f'{OUT}{nome}_{k:02d}.png'; bpy.ops.render.render(write_still=True)
    print('OK', nome)

import sys
if 'so_avioes' not in sys.argv: render('porta_avioes', porta_avioes())
render('aviao_us', aviao('us', '#4c5c70', 'us'), el=65)
render('aviao_jp', aviao('jp', '#d4d2c2', 'jp'), el=65)
