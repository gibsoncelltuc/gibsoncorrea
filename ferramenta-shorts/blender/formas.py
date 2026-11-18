# FORMAS para modelar objetos SEM cara de caixote. Use este arquivo em objeto novo:
#   import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from formas import *
#   novo('bolo'); cil((0, .15, 0), .5, .3, '#f6c9d4'); bola((0, .45, 0), .08, '#d8282f'); fim()
# Eixos: x = largura, y = ALTURA, z = profundidade (frente +). Medidas em metros (personagem ~2 m de altura). Tudo sai chanfrado e liso.
import bpy, bmesh, math, os
from mathutils import Vector, Matrix
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'web', 'assets', 'library', 'kit') + os.sep
_S = {}
def _mat(hexc):
    nm = _S['name'] + hexc; m = bpy.data.materials.get(nm) or bpy.data.materials.new(nm); m.use_nodes = True; h = hexc.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [(x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4) for x in c]; b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (*lin, 1); b.inputs['Roughness'].default_value = 1
    if _S.get('luz'): b.inputs['Emission Color'].default_value = (*lin, 1); b.inputs['Emission Strength'].default_value = 1.0   # luz(True): brilha no escuro (lampada, LED, satelite no ceu)
    if m not in _S['mats']: _S['mats'].append(m)
    return _S['mats'].index(m)
def _put(verts, col, c, rot=(0, 0, 0)):
    k = _mat(col); R = Matrix.Rotation(rot[2], 4, 'Y') @ Matrix.Rotation(rot[0], 4, 'X') @ Matrix.Rotation(rot[1], 4, 'Z')   # rot = (inclina p/ frente, inclina p/ lado, gira em pe) em radianos
    for v in verts: p = R @ v.co; v.co = Vector((p.x + c[0], p.y - c[2], p.z + c[1]))
    for f in {f for v in verts for f in v.link_faces}: f.material_index = k
def luz(on=True): _S['luz'] = on
def novo(name): bpy.ops.wm.read_factory_settings(use_empty=True); _S.update(name=name, bm=bmesh.new(), mats=[], luz=False)
def caixa(c, tam, col, afina=1.0, rot=(0, 0, 0)):          # tam = (largura, altura, profundidade); afina < 1 estreita o topo
    r = bmesh.ops.create_cube(_S['bm'], size=1.0)
    for v in r['verts']: t = afina if v.co.z > 0 else 1.0; v.co = Vector((v.co.x * tam[0] * t, v.co.y * tam[2] * t, v.co.z * tam[1]))
    _put(r['verts'], col, c, rot)
def cil(c, raio, alt, col, raio_topo=None, rot=(0, 0, 0), lados=20):   # cilindro em pe (ou cone/tronco com raio_topo); c = centro
    r = bmesh.ops.create_cone(_S['bm'], cap_ends=True, segments=lados, radius1=raio, radius2=raio if raio_topo is None else raio_topo, depth=alt); _put(r['verts'], col, c, rot)
def bola(c, raio, col, achata=1.0, rot=(0, 0, 0), seg=18, esc=(1, 1, 1)):   # esc = (largura, altura, profundidade) estica a bola (ovo, casco, folha, almofada)
    r = bmesh.ops.create_uvsphere(_S['bm'], u_segments=seg, v_segments=max(4, seg * 2 // 3), radius=raio)
    for v in r['verts']: v.co.z *= achata * esc[1]; v.co.x *= esc[0]; v.co.y *= esc[2]
    _put(r['verts'], col, c, rot)
def torno(c, perfil, col, lados=24, tampa=True):   # tampa=False deixa aberto (anel, friso, borda)                          # perfil = [(raio, altura), ...] de baixo para cima -> gira em volta do eixo (vaso, garrafa, sino, taca)
    bm = _S['bm']; aneis = []
    for rr, hh in perfil: aneis.append([bm.verts.new((max(rr, 0.001) * math.cos(2 * math.pi * i / lados), max(rr, 0.001) * math.sin(2 * math.pi * i / lados), hh)) for i in range(lados)])
    vs = [v for a in aneis for v in a]
    for a, b in zip(aneis, aneis[1:]):
        for i in range(lados): bm.faces.new((a[i], a[(i + 1) % lados], b[(i + 1) % lados], b[i]))
    if tampa: bm.faces.new(list(reversed(aneis[0]))); bm.faces.new(aneis[-1])
    _put(vs, col, c)
def tubo(pontos, raio, col, passo=1.0):                      # cano/alca/bico/galho: passa por uma lista de pontos (x, y, z); fica continuo
    for a, b in zip(pontos, pontos[1:]):
        d = math.dist(a, b); n = max(2, int(d / (raio * passo)))
        for i in range(n + 1): t = i / n; bola((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t), raio, col, seg=8)
def arco(c, raio, col, esp=0.04, de=0.0, ate=math.pi, n=14):  # arco em pe no plano x-y (alca de balde, chaleira, cesta)
    tubo([(c[0] + raio * math.cos(de + (ate - de) * i / n), c[1] + raio * math.sin(de + (ate - de) * i / n), c[2]) for i in range(n + 1)], esp, col)
def pano(c, larg, alt, cores, onda=0.14, nx=16):   # PANO ONDULADO continuo (bandeira, toldo, cortina): faixas horizontais de cores, de cima para baixo; c = canto superior junto ao mastro
    bm = _S['bm']; nf = len(cores); hb = alt / nf
    for fi, col in enumerate(cores):
        k = _mat(col); vs = []
        for side in (-1, 1):
            g = []
            for j in range(2):
                row = []
                for i in range(nx + 1):
                    t = i / nx; x = c[0] + larg * t; y = c[1] - hb * (fi + j) - .05 * t; z = c[2] + onda * math.sin(t * 5.5) * t ** .5 + side * .012
                    row.append(bm.verts.new((x, -z, y)))
                g.append(row)
            vs += [v for r in g for v in r]
            for i in range(nx):
                q = (g[0][i], g[0][i + 1], g[1][i + 1], g[1][i])
                f = bm.faces.new(q if side > 0 else tuple(reversed(q))); f.material_index = k
def prisma(c, pts, esp, col):   # SILHUETA 2D com espessura (raio, estrela, seta, coracao): pts = [(x, y), ...] no plano da tela, em volta; esp = grossura
    bm = _S['bm']; fr = [bm.verts.new((x, -esp / 2, y)) for x, y in pts]; bk = [bm.verts.new((x, esp / 2, y)) for x, y in pts]; n = len(pts)
    bm.faces.new(fr); bm.faces.new(list(reversed(bk)))
    for i in range(n): bm.faces.new((fr[i], bk[i], bk[(i + 1) % n], fr[(i + 1) % n]))
    _put(fr + bk, col, c)
def fim(chanfro=0.03):
    bm = _S['bm']
    me = bpy.data.meshes.new('red_' + _S['name']); bm.to_mesh(me); bm.free()
    for m in _S['mats']: me.materials.append(m)
    o = bpy.data.objects.new(_S['name'], me); bpy.context.collection.objects.link(o); bpy.context.view_layer.objects.active = o; o.select_set(True)
    if chanfro: m = o.modifiers.new('bv', 'BEVEL'); m.width = chanfro; m.segments = 3; m.limit_method = 'ANGLE'; m.angle_limit = math.radians(40); bpy.ops.object.modifier_apply(modifier='bv')
    for p in me.polygons: p.use_smooth = True
    try: me.use_auto_smooth = True; me.auto_smooth_angle = math.radians(50)
    except Exception: pass
    bpy.ops.export_scene.gltf(filepath=OUT + _S['name'] + '.glb', export_format='GLB', export_yup=True, export_apply=True, export_cameras=False, export_lights=False); print('OK', _S['name'], len(me.polygons))
