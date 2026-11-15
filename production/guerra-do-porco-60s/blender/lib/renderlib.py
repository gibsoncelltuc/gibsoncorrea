"""Configuração de render Cycles CPU + utilitários de câmera/mundo/luz."""
import bpy, math
from mathutils import Vector, Quaternion
from . import util
def setup(res=(540, 960), samples=24, denoise=True, bounces=4, fps=30, view='AgX', look='None', exposure=0.0, persistent=True):
    sc = bpy.context.scene; r = sc.render
    r.engine = 'CYCLES'; r.resolution_x, r.resolution_y = res; r.resolution_percentage = 100; r.fps = fps; r.use_persistent_data = persistent
    r.image_settings.file_format = 'PNG'; r.image_settings.color_mode = 'RGB'; r.image_settings.compression = 3
    c = sc.cycles; c.device = 'CPU'; c.samples = samples; c.use_adaptive_sampling = True; c.adaptive_threshold = 0.04; c.adaptive_min_samples = 6
    c.use_denoising = denoise; c.denoiser = 'OPENIMAGEDENOISE'; c.denoising_input_passes = 'RGB_ALBEDO_NORMAL'; c.denoising_prefilter = 'ACCURATE'
    c.max_bounces = bounces; c.diffuse_bounces = min(3, bounces); c.glossy_bounces = 2; c.transmission_bounces = 2; c.transparent_max_bounces = 10; c.volume_bounces = 0
    c.caustics_reflective = False; c.caustics_refractive = False; c.sample_clamp_indirect = 4.0; sc.view_settings.exposure = exposure
    c.pixel_filter_type = 'BLACKMAN_HARRIS'; c.filter_width = 1.1
    sc.view_settings.view_transform = view
    try: sc.view_settings.look = look
    except Exception: pass
    sc.display_settings.display_device = 'sRGB'; return sc
def world_sky(elevation_deg=18.0, rotation_deg=200.0, strength=1.0, sun_disc=False, air=1.0, dust=1.5, ozone=1.0, ground=(0.3, 0.28, 0.2, 1)):
    w = bpy.data.worlds.new('world'); w.use_nodes = True; bpy.context.scene.world = w; nt = w.node_tree; nt.nodes.clear()
    sky = nt.nodes.new('ShaderNodeTexSky'); sky.sky_type = 'SINGLE_SCATTERING'; sky.sun_elevation = math.radians(elevation_deg); sky.sun_rotation = math.radians(rotation_deg); sky.sun_disc = sun_disc
    sky.air_density = air; sky.aerosol_density = dust; sky.ozone_density = ozone; sky.altitude = 0.0
    bg = nt.nodes.new('ShaderNodeBackground'); bg.inputs['Strength'].default_value = strength; out = nt.nodes.new('ShaderNodeOutputWorld')
    nt.links.new(sky.outputs['Color'], bg.inputs['Color']); nt.links.new(bg.outputs['Background'], out.inputs['Surface']); return w
def sun(elevation_deg=18.0, azimuth_deg=200.0, color=(1.0, 0.78, 0.5), strength=4.0, angle_deg=2.5, name='sun'):
    d = bpy.data.lights.new(name, 'SUN'); d.energy = strength; d.color = color; d.angle = math.radians(angle_deg); o = bpy.data.objects.new(name, d); util.link(o)
    # direção: luz vem do azimute/elevação; objeto sol aponta -Z local
    el = math.radians(elevation_deg); az = math.radians(azimuth_deg); v = Vector((math.cos(el) * math.sin(az), math.cos(el) * math.cos(az), math.sin(el)))   # para o sol
    o.rotation_euler = (-v).to_track_quat('-Z', 'Y').to_euler(); return o
def camera(fov_deg=60, name='cam', dof=False, fstop=2.8, focus=5.0, sensor=24.0):
    cd = bpy.data.cameras.new(name); cd.sensor_fit = 'VERTICAL'; cd.sensor_height = sensor; cd.lens_unit = 'FOV'; cd.angle = math.radians(fov_deg); cd.clip_start = 0.05; cd.clip_end = 3000
    cd.dof.use_dof = dof; cd.dof.aperture_fstop = fstop; cd.dof.focus_distance = focus
    o = bpy.data.objects.new(name, cd); util.link(o); bpy.context.scene.camera = o; return o
def place_camera(cam, pos, target, fov=None, roll=0.0, focus=None, fstop=None):
    cam.location = pos; q = (Vector(target) - Vector(pos)).to_track_quat('-Z', 'Y')
    if roll: q = q @ Quaternion((0, 0, 1), roll)
    cam.rotation_mode = 'QUATERNION'; cam.rotation_quaternion = q
    if fov is not None: cam.data.angle = math.radians(fov)
    if focus is not None: cam.data.dof.focus_distance = focus
    if fstop is not None: cam.data.dof.aperture_fstop = fstop
def render_still(path):
    bpy.context.scene.render.filepath = path; bpy.ops.render.render(write_still=True)

def world_gradient(stops, sun_dir=None, sun_col=(1.0, 0.8, 0.5), glow=0.0, glow_pow=6.0, strength=1.0, zrange=(-0.12, 1.0)):
    """céu em degradê saturado (estilo do canal): stops = [(pos 0..1, (r,g,b,a)), ...] de baixo (horizonte) para cima (zênite); brilho do sol opcional."""
    w = bpy.data.worlds.new('world'); w.use_nodes = True; bpy.context.scene.world = w; nt = w.node_tree; nt.nodes.clear(); out = nt.nodes.new('ShaderNodeOutputWorld'); bg = nt.nodes.new('ShaderNodeBackground'); bg.inputs['Strength'].default_value = strength
    tc = nt.nodes.new('ShaderNodeTexCoord'); sp = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], sp.inputs['Vector'])
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = zrange[0]; mr.inputs['From Max'].default_value = zrange[1]; mr.clamp = True; nt.links.new(sp.outputs['Z'], mr.inputs['Value'])
    cr = nt.nodes.new('ShaderNodeValToRGB'); el = cr.color_ramp.elements
    while len(el) < len(stops): el.new(0.5)
    for e, (pos, col) in zip(el, stops): e.position = pos; e.color = col
    nt.links.new(mr.outputs['Result'], cr.inputs['Fac']); col = cr.outputs['Color']
    if sun_dir is not None and glow > 0:
        d = nt.nodes.new('ShaderNodeVectorMath'); d.operation = 'DOT_PRODUCT'; d.inputs[1].default_value = tuple(Vector(sun_dir).normalized()); nt.links.new(tc.outputs['Object'], d.inputs[0])
        m2 = nt.nodes.new('ShaderNodeMapRange'); m2.inputs['From Min'].default_value = 0.35; m2.inputs['From Max'].default_value = 1.0; m2.clamp = True; nt.links.new(d.outputs['Value'], m2.inputs['Value'])
        pw = nt.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = glow_pow; nt.links.new(m2.outputs['Result'], pw.inputs[0])
        gm = nt.nodes.new('ShaderNodeMix'); gm.data_type = 'RGBA'; gm.blend_type = 'ADD'; nt.links.new(pw.outputs['Value'], gm.inputs['Factor']); nt.links.new(col, gm.inputs['A']); gm.inputs['B'].default_value = (sun_col[0] * glow, sun_col[1] * glow, sun_col[2] * glow, 1); col = gm.outputs['Result']
    nt.links.new(col, bg.inputs['Color']); nt.links.new(bg.outputs['Background'], out.inputs['Surface']); return w
def sun_vec(el_deg, az_deg):
    el = math.radians(el_deg); az = math.radians(az_deg); return (math.cos(el) * math.sin(az), math.cos(el) * math.cos(az), math.sin(el))
