"""Materiais (Cycles): pintados à mão via imagens procedurais + ruído, AO de contato, neblina atmosférica por distância."""
import bpy, math
from . import util
HAZE = {'on': True, 'color': (0.72, 0.80, 0.95, 1.0), 'start': 60.0, 'end': 420.0, 'strength': 1.0}
def _new(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); out = nt.nodes.new('ShaderNodeOutputMaterial'); return m, nt, out
def _bsdf(nt, color=(.5, .5, .5, 1), rough=.8, spec=.3, metallic=0.0, emit=None, emit_s=0.0, alpha=1.0, coat=0.0):
    b = nt.nodes.new('ShaderNodeBsdfPrincipled'); b.inputs['Base Color'].default_value = color; b.inputs['Roughness'].default_value = rough
    b.inputs['Specular IOR Level'].default_value = spec; b.inputs['Metallic'].default_value = metallic; b.inputs['Alpha'].default_value = alpha
    if emit is not None: b.inputs['Emission Color'].default_value = emit; b.inputs['Emission Strength'].default_value = emit_s
    if coat: b.inputs['Coat Weight'].default_value = coat
    return b
def finish(m, nt, out, surf, haze=True):
    """liga a superfície ao output, inserindo neblina atmosférica (mistura com Emission da cor do ar pela distância à câmera)."""
    if haze and HAZE['on']:
        cam = nt.nodes.new('ShaderNodeCameraData'); mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = HAZE['start']; mr.inputs['From Max'].default_value = HAZE['end']
        mr.inputs['To Min'].default_value = 0.0; mr.inputs['To Max'].default_value = HAZE['strength']; mr.clamp = True
        nt.links.new(cam.outputs['View Distance'], mr.inputs['Value'])
        em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = HAZE['color']; em.inputs['Strength'].default_value = 1.0
        mx = nt.nodes.new('ShaderNodeMixShader'); nt.links.new(mr.outputs['Result'], mx.inputs['Fac']); nt.links.new(surf, mx.inputs[1]); nt.links.new(em.outputs['Emission'], mx.inputs[2]); surf = mx.outputs['Shader']
    nt.links.new(surf, out.inputs['Surface']); return m
def flat(name, color, rough=.85, spec=.25, emit=None, emit_s=0.0, haze=True, metallic=0.0, coat=0.0):
    m, nt, out = _new(name); b = _bsdf(nt, color, rough, spec, metallic, emit, emit_s, coat=coat); return finish(m, nt, out, b.outputs['BSDF'], haze)
def ink(name='ink'):
    m, nt, out = _new(name); b = _bsdf(nt, (0.012, 0.010, 0.02, 1), 1.0, 0.0); return finish(m, nt, out, b.outputs['BSDF'], False)
def cutout(name, color, emit=0.28, rough=.92, haze=False):
    """personagem cut-out: recebe luz/sombra, mas nunca fica escuro (mistura com emissão da própria cor)"""
    m, nt, out = _new(name); b = _bsdf(nt, color, rough, 0.0, 0.0, color, emit); return finish(m, nt, out, b.outputs['BSDF'], haze)
def cutout_img(name, path, emit=0.28, rough=.92, scale=(1, 1), haze=False):
    m, nt, out = _new(name); tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (scale[0], scale[1], 1)
    ti = nt.nodes.new('ShaderNodeTexImage'); ti.image = bpy.data.images.load(path, check_existing=True); ti.interpolation = 'Linear'
    nt.links.new(tc.outputs['UV'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], ti.inputs['Vector']); b = _bsdf(nt, (1, 1, 1, 1), rough, 0.0); nt.links.new(ti.outputs['Color'], b.inputs['Base Color']); nt.links.new(ti.outputs['Color'], b.inputs['Emission Color']); b.inputs['Emission Strength'].default_value = emit
    return finish(m, nt, out, b.outputs['BSDF'], haze)
def image(name, path, rough=.8, spec=.25, bump=0.25, scale=(1, 1), coord='UV', tint=None, tint_f=0.0, ao=0.0, ao_dist=0.5, haze=True, emit=None, emit_s=0.0, metallic=0.0, box=False):
    m, nt, out = _new(name); tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (scale[0], scale[1], scale[0] if coord != 'UV' else 1)
    ti = nt.nodes.new('ShaderNodeTexImage'); ti.image = bpy.data.images.load(path, check_existing=True); ti.interpolation = 'Cubic'
    if box: ti.projection = 'BOX'; ti.projection_blend = 0.25
    nt.links.new(tc.outputs[coord if coord == 'UV' else 'Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], ti.inputs['Vector']); col = ti.outputs['Color']
    if tint is not None:
        mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = tint_f; nt.links.new(col, mx.inputs['A']); mx.inputs['B'].default_value = tint; col = mx.outputs['Result']
    if ao > 0:
        a = nt.nodes.new('ShaderNodeAmbientOcclusion'); a.inputs['Distance'].default_value = ao_dist; a.samples = 4
        mx2 = nt.nodes.new('ShaderNodeMix'); mx2.data_type = 'RGBA'; mx2.blend_type = 'MULTIPLY'; mx2.inputs['Factor'].default_value = ao; nt.links.new(col, mx2.inputs['A']); nt.links.new(a.outputs['Color'], mx2.inputs['B']); col = mx2.outputs['Result']
    b = _bsdf(nt, (1, 1, 1, 1), rough, spec, metallic, emit, emit_s); nt.links.new(col, b.inputs['Base Color'])
    if bump > 0:
        bw = nt.nodes.new('ShaderNodeRGBToBW'); bn = nt.nodes.new('ShaderNodeBump'); bn.inputs['Strength'].default_value = bump; bn.inputs['Distance'].default_value = 0.02
        nt.links.new(ti.outputs['Color'], bw.inputs['Color']); nt.links.new(bw.outputs['Val'], bn.inputs['Height']); nt.links.new(bn.outputs['Normal'], b.inputs['Normal'])
    return finish(m, nt, out, b.outputs['BSDF'], haze)
def decal(name, path, rough=.85, spec=.1, emit_s=.06, haze=True):
    """decalque RGBA (letras estampadas, papéis, caminho de terra): imagem com alfa sobre superfície com UV"""
    m, nt, out = _new(name); tc = nt.nodes.new('ShaderNodeTexCoord'); ti = nt.nodes.new('ShaderNodeTexImage'); ti.image = bpy.data.images.load(path, check_existing=True); ti.interpolation = 'Linear'; ti.extension = 'CLIP'
    nt.links.new(tc.outputs['UV'], ti.inputs['Vector']); b = _bsdf(nt, (1, 1, 1, 1), rough, spec); nt.links.new(ti.outputs['Color'], b.inputs['Base Color']); nt.links.new(ti.outputs['Alpha'], b.inputs['Alpha'])
    if emit_s: nt.links.new(ti.outputs['Color'], b.inputs['Emission Color']); b.inputs['Emission Strength'].default_value = emit_s
    return finish(m, nt, out, b.outputs['BSDF'], haze)
def painted(name, c1, c2, scale=3.0, detail=6.0, rough=.85, spec=.2, bump=.2, ao=0.0, haze=True, coord='Object', metallic=0.0):
    """pintura procedural: ruído fractal entre duas cores (sem imagem)"""
    m, nt, out = _new(name); tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = scale; nz.inputs['Detail'].default_value = detail
    nt.links.new(tc.outputs[coord], nz.inputs['Vector']); cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = c1; cr.color_ramp.elements[1].color = c2; nt.links.new(nz.outputs['Fac'], cr.inputs['Fac']); col = cr.outputs['Color']
    if ao > 0:
        a = nt.nodes.new('ShaderNodeAmbientOcclusion'); a.inputs['Distance'].default_value = .5; a.samples = 4; mx2 = nt.nodes.new('ShaderNodeMix'); mx2.data_type = 'RGBA'; mx2.blend_type = 'MULTIPLY'; mx2.inputs['Factor'].default_value = ao
        nt.links.new(col, mx2.inputs['A']); nt.links.new(a.outputs['Color'], mx2.inputs['B']); col = mx2.outputs['Result']
    b = _bsdf(nt, (1, 1, 1, 1), rough, spec, metallic); nt.links.new(col, b.inputs['Base Color'])
    if bump > 0: bn = nt.nodes.new('ShaderNodeBump'); bn.inputs['Strength'].default_value = bump; nt.links.new(nz.outputs['Fac'], bn.inputs['Height']); nt.links.new(bn.outputs['Normal'], b.inputs['Normal'])
    return finish(m, nt, out, b.outputs['BSDF'], haze)
def vcol(name, attr='Col', rough=.9, spec=.1, emit_s=0.0, bump=0.0, haze=True, double=False):
    m, nt, out = _new(name); vc = nt.nodes.new('ShaderNodeVertexColor'); vc.layer_name = attr; b = _bsdf(nt, (1, 1, 1, 1), rough, spec)
    nt.links.new(vc.outputs['Color'], b.inputs['Base Color'])
    if emit_s > 0: nt.links.new(vc.outputs['Color'], b.inputs['Emission Color']); b.inputs['Emission Strength'].default_value = emit_s
    return finish(m, nt, out, b.outputs['BSDF'], haze)
def shaft(name, color=(1.0, 0.82, 0.5, 1), strength=1.0):
    """raio de luz falso: plano translúcido com gradiente (só visível à câmera)"""
    m, nt, out = _new(name); tc = nt.nodes.new('ShaderNodeTexCoord'); sp = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['UV'], sp.inputs['Vector'])
    gx = nt.nodes.new('ShaderNodeMath'); gx.operation = 'SINE'; mu = nt.nodes.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = math.pi; nt.links.new(sp.outputs['X'], mu.inputs[0]); nt.links.new(mu.outputs['Value'], gx.inputs[0])
    gy = nt.nodes.new('ShaderNodeMath'); gy.operation = 'MULTIPLY'; nt.links.new(sp.outputs['Y'], gy.inputs[0]); gy.inputs[1].default_value = 1.0
    pw = nt.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; nt.links.new(gx.outputs['Value'], pw.inputs[0]); pw.inputs[1].default_value = 2.0
    mu2 = nt.nodes.new('ShaderNodeMath'); mu2.operation = 'MULTIPLY'; nt.links.new(pw.outputs['Value'], mu2.inputs[0]); nt.links.new(gy.outputs['Value'], mu2.inputs[1])
    mu3 = nt.nodes.new('ShaderNodeMath'); mu3.operation = 'MULTIPLY'; mu3.inputs[1].default_value = 0.55 * strength; nt.links.new(mu2.outputs['Value'], mu3.inputs[0])
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = color; em.inputs['Strength'].default_value = 3.0; tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(mu3.outputs['Value'], mx.inputs['Fac']); nt.links.new(tr.outputs['BSDF'], mx.inputs[1]); nt.links.new(em.outputs['Emission'], mx.inputs[2]); nt.links.new(mx.outputs['Shader'], out.inputs['Surface']); return m
def glow(name, color, strength=8.0):
    m, nt, out = _new(name); em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = color; em.inputs['Strength'].default_value = strength; nt.links.new(em.outputs['Emission'], out.inputs['Surface']); return m
def camera_only(obj):
    obj.visible_diffuse = False; obj.visible_glossy = False; obj.visible_transmission = False; obj.visible_volume_scatter = False; obj.visible_shadow = False
