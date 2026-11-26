# 26/11 Criaturas ORGANICAS: esqueleto (pontos + raios) -> Skin modifier + Subdivision = corpo liso e continuo,
# cor por vertice (dorso escuro -> barriga clara), olhos e dentes por cima. Substitui os bonecos de bolinhas.
# blender -b --python blender/criaturas_pele.py      (eixos do projeto: x = frente, y = cima, z = lado)
import bpy, bmesh, math, os
from mathutils import Vector
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'web', 'assets', 'library', 'kit') + os.sep
B = lambda p: Vector((p[0], -p[2], p[1]))   # (x, cima, lado) -> coordenadas do Blender

def hexc(h): h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]; return [(x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4) for x in c]

def limpar(): bpy.ops.wm.read_factory_settings(use_empty=True)

def corpo(galhos, costas, barriga, sub=2, mancha=None):
    """galhos: lista de cadeias [(x,y,z,r), ...]; cadeias que comecam num ponto ja existente se ligam a ele."""
    me = bpy.data.meshes.new('c'); bm = bmesh.new(); idx = {}; raios = []
    def vert(p):
        k = tuple(round(v, 4) for v in p[:3])
        if k in idx: return idx[k]
        v = bm.verts.new(B(p)); idx[k] = v; raios.append((v, p[3])); return v
    for cad in galhos:
        vs = [vert(p) for p in cad]
        for a, b in zip(vs, vs[1:]):
            if a is not b and not bm.edges.get((a, b)): bm.edges.new((a, b))
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new('corpo', me); bpy.context.collection.objects.link(ob); bpy.context.view_layer.objects.active = ob; ob.select_set(True)
    sk = ob.modifiers.new('skin', 'SKIN'); sk.use_smooth_shade = True
    lay = me.skin_vertices[0].data
    rm = {tuple(round(v, 4) for v in (vv.co.x, -vv.co.y if False else vv.co.y, vv.co.z)): None for vv in me.vertices}
    for i, v in enumerate(me.vertices):
        # acha o raio pelo ponto mais proximo
        best = min(raios_lista, key=lambda q: (Vector(q[0]) - v.co).length) if False else None
    pts = [(B(p), p[3]) for cad in galhos for p in cad]
    for i, v in enumerate(me.vertices):
        r = min(pts, key=lambda q: (q[0] - v.co).length)[1]; lay[i].radius = (r, r)
    lay[0].use_root = True
    ss = ob.modifiers.new('sub', 'SUBSURF'); ss.levels = sub; ss.render_levels = sub
    bpy.ops.object.modifier_apply(modifier='skin'); bpy.ops.object.modifier_apply(modifier='sub')
    # cor: dorso escuro, barriga clara (pela altura relativa ao eixo local + normal)
    me = ob.data; ca = me.color_attributes.new('Col', 'FLOAT_COLOR', 'POINT'); cb, cc = hexc(costas), hexc(barriga); cm = hexc(mancha) if mancha else None
    for i, v in enumerate(me.vertices):
        t = max(0., min(1., (v.normal.z + .75) / .9)) ** .8   # normal para cima = costas
        c = [cb[k] * t + cc[k] * (1 - t) for k in range(3)]
        if cm and (math.sin(v.co.x * 9) * math.sin(v.co.y * 7) > .55) and t > .5: c = [c[k] * .55 + cm[k] * .45 for k in range(3)]
        ca.data[i].color = (*c, 1)
    mat = bpy.data.materials.new('pele'); mat.use_nodes = True; nt = mat.node_tree; bsdf = nt.nodes['Principled BSDF']
    vc = nt.nodes.new('ShaderNodeVertexColor'); vc.layer_name = 'Col'; nt.links.new(vc.outputs['Color'], bsdf.inputs['Base Color']); bsdf.inputs['Roughness'].default_value = .6
    me.materials.append(mat)
    for p in me.polygons: p.use_smooth = True
    return ob

def peca(tipo, pos, raio, cor, esc=(1, 1, 1), rot=(0, 0, 0), prof=None):
    if tipo == 'bola': bpy.ops.mesh.primitive_uv_sphere_add(segments=14, ring_count=10, radius=raio, location=B(pos))
    else: bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=raio, radius2=0, depth=prof or raio * 3, location=B(pos))
    o = bpy.context.active_object; o.scale = (esc[0], esc[2], esc[1]); o.rotation_euler = rot
    m = bpy.data.materials.new('p'); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (*hexc(cor), 1); b.inputs['Roughness'].default_value = .3
    o.data.materials.append(m)
    # cor por vertice igual (para o material do glTF com vertex color nao zerar)
    ca = o.data.color_attributes.new('Col', 'FLOAT_COLOR', 'POINT')
    for d in ca.data: d.color = (*hexc(cor), 1)
    return o

def olhos(x, y, z, r, cor='#d9b23a'):
    for s in (1, -1): peca('bola', (x, y, z * s), r, cor); peca('bola', (x + r * .45, y, (z + r * .5) * s), r * .55, '#0c0c0c')
def dentes(x0, x1, y, z, n, tam, baixo=True):
    for i in range(n):
        x = x0 + (x1 - x0) * i / max(1, n - 1)
        for s in (1, -1): peca('cone', (x, y - (tam * .5 if baixo else -tam * .5), z * s), tam * .3, '#efe6cf', rot=(0, math.pi if baixo else 0, 0) if False else ((math.pi, 0, 0) if baixo else (0, 0, 0)), prof=tam)

def exportar(nome):
    bpy.ops.object.select_all(action='SELECT'); bpy.context.view_layer.objects.active = [o for o in bpy.context.scene.objects if o.name.startswith('corpo')][0]; bpy.ops.object.join()
    bpy.ops.export_scene.gltf(filepath=OUT + nome + '.glb', export_format='GLB', export_yup=True, export_apply=True, export_cameras=False, export_lights=False)
    print('OK', nome, len(bpy.context.active_object.data.polygons))

def perna(ombro, joelho, pe, r):   # cadeia ombro -> cotovelo -> pe -> dedos
    return [ombro, (*joelho, r), (*pe, r * .8), (pe[0] + r * 2.2, pe[1] - r * .3, pe[2], r * .55)]

def reptil(nome, L, costas, barriga, alto=.32, focinho=1.0, largo=1.0, patas_altas=False, mancha=None, n_dentes=8):
    limpar(); s = L / 4.2
    esp = [(-2.1 * s, alto * .6, 0, .03 * s), (-1.5 * s, alto * .75, 0, .1 * s), (-.9 * s, alto * .9, 0, .2 * s), (-.3 * s, alto, 0, .3 * s * largo), (.3 * s, alto, 0, .32 * s * largo),
           (.9 * s, alto, 0, .26 * s * largo), (1.25 * s, alto + .02, 0, .2 * s * largo), (1.55 * s, alto - .01, 0, .14 * s * largo * (1.25 if focinho > 1.1 else 1)),
           ((1.55 + .55 * focinho) * s, alto - .04, 0, .09 * s * largo * (1.4 if focinho > 1.1 else 1)), ((1.55 + .85 * focinho) * s, alto - .05, 0, .06 * s * largo), ((1.55 + .97 * focinho) * s, alto - .055, 0, .035 * s * largo)]
    ga = [esp]
    pa = .55 if patas_altas else 1
    for x in (.75 * s, -.35 * s):
        for z in (1, -1):
            sh = (x, alto, 0, .3 * s * largo) if x > 0 else (-.3 * s, alto, 0, .3 * s * largo)
            if x > 0: sh = (.9 * s, alto, 0, .26 * s * largo)
            ga.append(perna(sh, (sh[0] + .05 * s, alto * .55 if not patas_altas else alto * .6, z * .42 * s), (sh[0] + .1 * s, .03, z * .5 * s), .07 * s))
    corpo(ga, costas, barriga, mancha=mancha)
    hx = (1.55 + .85 * focinho) * s
    olhos(1.4 * s, alto + .14 * s, .12 * s * largo, .05 * s)
    dentes(1.6 * s, hx - .05 * s, alto - .06 * s, .07 * s * largo, n_dentes, .07 * s)
    for i in range(12): peca('cone', ((1.0 - i * .25) * s, alto + .27 * s * (1 - i / 16), 0), .035 * s, costas, prof=.08 * s)   # escudos do dorso
    exportar(nome)

def teropode(nome, L, costas, barriga, cabeca=1.0, bracos=.35, crista=None):
    limpar(); s = L / 5.0; H = 1.5 * s
    esp = [(-2.6 * s, H * .9, 0, .04 * s), (-1.8 * s, H * .95, 0, .12 * s), (-1.0 * s, H, 0, .25 * s), (-.3 * s, H, 0, .42 * s), (.4 * s, H + .1 * s, 0, .4 * s), (.9 * s, H + .4 * s, 0, .25 * s),
           (1.2 * s, H + .65 * s, 0, .22 * s * cabeca), (1.55 * s, H + .62 * s, 0, .26 * s * cabeca), (1.95 * s, H + .52 * s, 0, .18 * s * cabeca), (2.25 * s, H + .45 * s, 0, .1 * s * cabeca)]
    ga = [esp]
    for z in (1, -1):
        ga.append([(-.3 * s, H, 0, .42 * s), (-.1 * s, H * .6, z * .32 * s, .2 * s), (-.35 * s, H * .25, z * .34 * s, .12 * s), (-.15 * s, .05, z * .34 * s, .1 * s), (.25 * s, .03, z * .34 * s, .06 * s)])
        ga.append([(.6 * s, H + .15 * s, 0, .3 * s), (.75 * s, H - bracos * .5 * s, z * .25 * s, .05 * s), (.9 * s, H - bracos * s, z * .25 * s, .035 * s)])
    corpo(ga, costas, barriga)
    olhos(1.6 * s, H + .75 * s, .17 * s * cabeca, .045 * s, '#e0601a')
    dentes(1.7 * s, 2.25 * s, H + .4 * s, .1 * s * cabeca, 6, .09 * s)
    if crista:
        for i in range(5): peca('cone', ((1.4 + i * .1) * s, H + .9 * s, 0), .04 * s, crista, prof=.12 * s)
    exportar(nome)

def peixe(nome, L, costas, barriga, alt=1.0, dentao=False, couraca=False):
    limpar(); s = L / 4.0
    esp = [(-2.0 * s, 0, 0, .1 * s), (-1.5 * s, 0, 0, .22 * s * alt), (-.6 * s, 0, 0, .5 * s * alt), (.4 * s, 0, 0, .55 * s * alt), (1.2 * s, .02, 0, .45 * s * alt), (1.7 * s, 0, 0, .28 * s * alt), (2.05 * s, -.02 * s, 0, .1 * s * alt)]
    ga = [esp, [(-2.0 * s, 0, 0, .1 * s), (-2.45 * s, .55 * s * alt, 0, .04 * s)], [(-2.0 * s, 0, 0, .1 * s), (-2.4 * s, -.45 * s * alt, 0, .04 * s)],
          [(-.2 * s, .4 * s * alt, 0, .15 * s), (-.55 * s, .95 * s * alt, 0, .03 * s)]]
    for z in (1, -1): ga.append([(.6 * s, -.25 * s * alt, z * .3 * s, .1 * s), (.2 * s, -.6 * s * alt, z * .7 * s, .03 * s)])
    corpo(ga, costas, barriga)
    olhos(1.35 * s, .18 * s * alt, .33 * s * alt, .07 * s, '#cfcfcf')
    if dentao: dentes(1.25 * s, 1.75 * s, -.12 * s, .22 * s * alt, 6, .1 * s)
    if couraca:
        peca('bola', (1.35 * s, .06 * s, 0), .5 * s * alt, '#353b40', esc=(1.25, .95, 1.0))   # elmo osseo da cabeca
    exportar(nome)

def cobra(nome, L, costas, barriga, mancha):
    limpar(); s = L / 5.0; cad = []
    for i in range(30):
        t = i / 29; r = .26 * s * (1 - .7 * max(0, (t - .7) / .3)) * (.55 if t < .05 else 1)
        cad.append(((2.3 - t * 4.8) * s, .27 * s, 1.0 * s * math.sin(t * 5.5), max(.03 * s, r)))
    cad.insert(0, (2.6 * s, .26 * s, 0, .2 * s))
    corpo([cad], costas, barriga, mancha=mancha); olhos(2.55 * s, .36 * s, .13 * s, .028 * s); exportar(nome)

def mamifero(nome, L, costas, barriga):   # gorgonopsideo
    limpar(); s = L / 3.5; H = .95 * s
    esp = [(-1.8 * s, H * .7, 0, .04 * s), (-1.1 * s, H * .9, 0, .13 * s), (-.6 * s, H, 0, .3 * s), (.3 * s, H + .05 * s, 0, .36 * s), (.9 * s, H + .05 * s, 0, .28 * s), (1.25 * s, H + .15 * s, 0, .25 * s), (1.6 * s, H + .08 * s, 0, .17 * s), (1.85 * s, H, 0, .1 * s)]
    ga = [esp]
    for x in (.8 * s, -.5 * s):
        for z in (1, -1): ga.append(perna((x, H, 0, .3 * s), (x + .1 * s, H * .5, z * .3 * s), (x, .04, z * .32 * s), .09 * s))
    corpo(ga, costas, barriga)
    olhos(1.45 * s, H + .26 * s, .16 * s, .05 * s, '#e0a020')
    for z in (1, -1): peca('cone', (1.65 * s, H - .15 * s, z * .08 * s), .04 * s, '#efe6cf', rot=(math.pi, 0, 0), prof=.3 * s)
    exportar(nome)

reptil('crocodilo', 4.2, '#3f4a2a', '#d6cf9e', mancha='#2a3320')
reptil('deinosuchus', 4.6, '#363a2a', '#c4ba92', focinho=1.15, largo=1.1, mancha='#26291e')
reptil('purussaurus', 4.4, '#4e4430', '#d8c9a0', focinho=1.2, largo=1.3)
reptil('postosuchus', 3.4, '#6e4530', '#dcc09a', alto=.75, patas_altas=True, focinho=.8, mancha='#4f3020')
reptil('megalania', 3.8, '#5e574a', '#cfc6ac', alto=.36, focinho=.7, mancha='#3e3a30', n_dentes=6)
teropode('trex', 5.2, '#4e3f2c', '#d2bd98', cabeca=1.35, bracos=.25)
teropode('allosaurus', 5.0, '#6e5236', '#dcc6a0', cabeca=1.0, bracos=.5, crista='#a8401e')
peixe('dunkleosteus', 3.6, '#3f4a52', '#c4ccd0', alt=1.15, couraca=True)
peixe('megalodon', 5.2, '#4f5e6a', '#eef2f4', alt=1.0, dentao=True)
cobra('titanoboa', 5.0, '#3e4630', '#b8b088', '#22261a')
mamifero('inostrancevia', 3.5, '#7a5c40', '#d4b48c')
