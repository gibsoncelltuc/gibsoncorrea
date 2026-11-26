# 26/11 Navios e avioes 3D para os shorts de GUERRA (estilo Age of Empires: modelo 3D renderizado em 16 rumos, vista 3/4 de cima).
# Saida: geo/dados/sprites/<nome>_<rumo>.png (fundo transparente). blender -b --python blender/navios_sprites.py
import bpy, math, os
from mathutils import Vector
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'geo', 'dados', 'sprites') + os.sep
os.makedirs(OUT, exist_ok=True)
def hexc(h): h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]; return [(x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4) for x in c]
def mat(nome, cor, rough=.6, metal=0.0, emit=None):
    m = bpy.data.materials.get(nome) or bpy.data.materials.new(nome); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*hexc(cor), 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    if emit: b.inputs['Emission Color'].default_value = (*hexc(emit), 1); b.inputs['Emission Strength'].default_value = 2
    return m
def caixa(loc, dim, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.active_object; o.scale = dim; o.data.materials.append(m); return o
def cil(loc, r, h, m, rot=(0, 0, 0), v=16, r2=None):
    bpy.ops.mesh.primitive_cone_add(vertices=v, radius1=r, radius2=r if r2 is None else r2, depth=h, location=loc, rotation=rot); o = bpy.context.active_object; o.data.materials.append(m); return o
def casco(comprimento, largura, altura, m, proa=.22):
    # casco afinado na proa (x+) e popa arredondada: cubo subdividido e moldado
    bpy.ops.mesh.primitive_cube_add(size=1); o = bpy.context.active_object; o.scale = (comprimento, largura, altura); bpy.ops.object.transform_apply(scale=True)
    me = o.data
    for v in me.vertices:
        if v.co.x > comprimento * (.5 - proa): k = (v.co.x - comprimento * (.5 - proa)) / (comprimento * proa); v.co.y *= 1 - .92 * k ** 1.3
        if v.co.z < 0: v.co.y *= .72
    o.data.materials.append(m); sub = o.modifiers.new('s', 'SUBSURF'); sub.levels = 1; return o
def limpar(): bpy.ops.wm.read_factory_settings(use_empty=True)

def porta_avioes():
    limpar(); cinza = mat('cinza', '#6e757c', .5, .3); conves = mat('conves', '#8a6a44', .8); faixa = mat('faixa', '#eeeeee', .7); verm = mat('verm', '#7a2a22', .7); escuro = mat('esc', '#3a3e44', .5, .3)
    casco(10, 1.5, 1.0, cinza); caixa((0, 0, -.42), (9.6, 1.25, .18), verm)               # linha d'agua vermelha
    caixa((0, 0, .6), (10.4, 1.9, .12), conves)                                                 # convés de voo
    for x in (-3.5, 0, 3.5): caixa((x, 0, .67), (.9, .06, .01), faixa)
    caixa((-4.9, 0, .67), (.1, 1.6, .01), faixa); caixa((4.9, 0, .67), (.1, 1.6, .01), faixa)
    caixa((.8, .78, 1.15), (1.6, .32, 1.0), cinza); cil((.4, .78, 1.9), .2, .7, escuro, v=10)   # ilha + chamine
    cil((1.2, .78, 2.0), .03, 1.2, escuro, v=6); caixa((1.2, .78, 2.4), (.5, .04, .04), escuro)  # mastro
    for i, x in enumerate((-4.2, -3.4, -2.6, -1.8)):                                             # avioes estacionados
        for y in (-.4, .3):
            caixa((x, y, .72), (.42, .07, .06), cinza); caixa((x + .02, y, .72), (.08, .55, .03), cinza)
    for x in (-2, 2): cil((x, -.95, .25), .06, .5, escuro, rot=(0, math.pi / 2, 0), v=8)         # canhoes laterais
    return 6.0

def aviao(nome, cor, marca):
    limpar(); c = mat('c' + nome, cor, .45, .2); m2 = mat('m' + nome, marca, .5); vidro = mat('v', '#9ad0ff', .1, .5); preto = mat('p', '#1a1a1a', .5)
    cil((0, 0, 0), .22, 2.4, c, rot=(0, math.pi / 2, 0), v=14, r2=.1)                             # fuselagem
    caixa((.2, 0, -.02), (.55, 2.6, .05), c)                                                     # asas
    caixa((-1.0, 0, .02), (.3, .9, .04), c); caixa((-1.05, 0, .25), (.3, .04, .45), c)           # cauda
    bpy.ops.mesh.primitive_uv_sphere_add(radius=.16, location=(.35, 0, .17)); o = bpy.context.active_object; o.scale = (1.6, .8, .7); o.data.materials.append(vidro)
    cil((1.25, 0, 0), .05, .1, preto, rot=(0, math.pi / 2, 0)); caixa((1.3, 0, 0), (.03, .9, .08), preto)   # helice
    for y in (-.85, .85):                                                                        # insignia nas asas
        cil((.2, y, .02), .2, .02, m2, v=20)
    return 1.3

def fragata(nome, casco_cor, vela_cor):   # navio a vela (para guerras antigas)
    limpar(); madeira = mat('mad', casco_cor, .8); vela = mat('vela', vela_cor, .9); escuro = mat('e', '#2a1e14', .7)
    casco(7, 1.6, 1.2, madeira, proa=.3); caixa((-2.6, 0, .9), (1.6, 1.3, .7), madeira)
    for x, h in ((-1.6, 4.0), (.4, 4.6), (2.2, 3.6)):
        cil((x, 0, h / 2 + .4), .06, h, escuro, v=6)
        for k, w in ((.45, 1.5), (.72, 1.2)): caixa((x, 0, .4 + h * k), (.06, w * 1.2, h * .22), vela)
    return 5.0

def render(nome, alvo_raio, angulos=16, tam=320):
    sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.cycles.device = 'CPU'; sc.cycles.use_denoising = False; sc.render.film_transparent = True
    sc.render.resolution_x = sc.render.resolution_y = tam; sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Color'].default_value = (.6, .7, .85, 1); w.node_tree.nodes['Background'].inputs['Strength'].default_value = .9
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10)); s = bpy.context.active_object; s.data.energy = 4; s.rotation_euler = (math.radians(40), 0, math.radians(30))
    objs = [o for o in sc.objects if o.type == 'MESH']; piv = bpy.data.objects.new('piv', None); sc.collection.objects.link(piv)
    for o in objs: o.parent = piv
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam; cam.data.type = 'ORTHO'; cam.data.ortho_scale = alvo_raio * 2.2
    el = math.radians(55); d = 30; cam.location = (0, -d * math.cos(el), d * math.sin(el)); cam.rotation_euler = (math.radians(90) - el, 0, 0)
    for k in range(angulos):
        piv.rotation_euler = (0, 0, -k * 2 * math.pi / angulos)   # rumo k: 0 = proa para a DIREITA da tela, sentido horario
        sc.render.filepath = f'{OUT}{nome}_{k:02d}.png'; bpy.ops.render.render(write_still=True)
    print('OK', nome)

render('porta_avioes', porta_avioes())
render('aviao_us', aviao('us', '#4a5a70', '#f4f4f4'))
render('aviao_jp', aviao('jp', '#c8c8b8', '#d0202a'))
render('fragata', fragata('fragata', '#6a4a2e', '#efe6d2'))
