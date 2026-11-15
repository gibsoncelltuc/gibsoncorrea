"""Ficha de personagens do piloto (rubrica V2: character sheet). Renderiza, com o MESMO rig/materiais/contorno do vídeo, uma fileira por personagem:
corpo inteiro · pose de ação · 5 expressões (neutro, malicioso, choque, raiva, riso) — e a fileira do porco (comer, trotar, morto).
Uso: python sheets.py [amostras=14] [só=nome,nome]   →  design/char-tiles/<nome>_<coluna>.png  e  design/character-sheet.png (montada com Pillow)"""
import sys, os, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from lib import util, renderlib, char, pig, anim, props, texlib
from lib.shots import LOOKS
from lib.char import U
S = int(sys.argv[1]) if len(sys.argv) > 1 else 14; ONLY = sys.argv[2].split(',') if len(sys.argv) > 2 else None
ROOT = util.ROOT; TILES = os.path.join(ROOT, 'design', 'char-tiles'); os.makedirs(TILES, exist_ok=True)
TW, TH = 288, 360
util.reset(); sc = renderlib.setup((TW, TH), samples=S, bounces=3, view='Standard', look='None', exposure=-0.45)
sc.render.threads_mode = 'FIXED'; sc.render.threads = int(os.environ.get('THREADS', 2))
renderlib.world_gradient([(0.0, (0.80, 0.74, 0.90, 1)), (1.0, (0.93, 0.89, 0.97, 1))], strength=1.0)
renderlib.sun(40, 150, color=(1.0, 0.95, 0.88), strength=1.2, angle_deg=8)
cam = renderlib.camera(26, dof=False)
CAST = [('cutlar', 'Lyman Cutlar (fazendeiro americano)'), ('griffin', 'Charles Griffin (dono do porco, britânico)'), ('soldier', 'Soldado americano (multidão: 80 variações)'),
        ('baynes', 'Contra-almirante Baynes'), ('aide', 'Auxiliar do almirante')]
def base(**kw): d = anim.idle(0.4, x=0, y=0, z=0, face=1); d.update(kw); return d
EXPR = {'neutro': dict(lid=.42, mouth='line', brows=(0, 0)),
        'malicioso': dict(lid=.55, mouth='smirk', brows=(.35, -.4), tilt=.04),
        'choque': dict(eye='wide', brows=(.9, .9), mouth='oh', sweat=.35),
        'raiva': dict(lid=.78, angry=.8, brows=(-.4, -.4), mouth='shout'),
        'riso': dict(eye='arc', mouth='laugh', open=.8, brows=(.7, .7), tilt=-.1)}
ACTION = {'cutlar': lambda b: anim.aim_fire(1.0, b, 0.0, 1.0), 'griffin': lambda b: anim.laugh(1.0, b), 'soldier': lambda b: dict(b, **anim.march(0.13)),
          'baynes': lambda b: anim.stop_hand(1.0, b, 0.0), 'aide': lambda b: anim.point(1.0, b, 0.0, 'R')}
def shoot(path, pos, look, fov):
    renderlib.place_camera(cam, pos, look, fov=fov); sc.render.filepath = path; bpy.ops.render.render(write_still=True)
t0 = time.time(); done = 0
for key, label in CAST:
    if ONLY and key not in ONLY: continue
    ch = char.Char(key, LOOKS[key]); rf = None
    if key in ('cutlar', 'soldier'): rf = props.rifle(); ch.attach('R', rf, (0, 0, -.1), (0, math.pi + 1.1 if key == 'soldier' else 0, 0))
    ch.pose(base()); bpy.context.view_layer.update()
    # corpo inteiro
    if rf is not None and key == 'cutlar': rf.rotation_euler = (0, math.pi, 0)
    shoot(f'{TILES}/{key}_0corpo.png', (0, -6.6, 1.0), (0, 0, 1.0), 26); done += 1
    # ação
    ch.pose(ACTION[key](base())); bpy.context.view_layer.update()
    if rf is not None and key == 'cutlar': rf.rotation_euler = (0, 0, 0)
    shoot(f'{TILES}/{key}_1acao.png', (0, -6.6, 1.0), (0, 0, 1.0), 26); done += 1
    if rf is not None and key == 'cutlar': rf.rotation_euler = (0, math.pi, 0)
    # expressões (close do rosto) — sem o fuzil, que cobriria o corpo
    if rf is not None: rf.hide_render = True
    for i, (name, ex) in enumerate(EXPR.items()):
        d = base(); d.update(ex); ch.pose(d); bpy.context.view_layer.update(); hz = (1.38 + 1.79 + .12) * U
        shoot(f'{TILES}/{key}_{i + 2}{name}.png', (0, -4.6, hz), (0, 0, hz), 20); done += 1
    for o in ch.objs + [ch.root] + ([rf] + list(rf.children_recursive) if rf else []):
        o.hide_render = True
    print(key, 'ok', round(time.time() - t0), 's', flush=True)
if not ONLY or 'pig' in ONLY:
    pg = pig.Pig()
    for i, (mode, kw) in enumerate([('eat', {}), ('trot', {}), ('dead', dict(flip=1.0))]):
        pg.pose(dict(x=0, y=0, z=0, face=-1, t=0.31, mode=mode, scale=1.25 * 1.3, **kw)); bpy.context.view_layer.update()
        shoot(f'{TILES}/pig_{i}{mode}.png', (0, -9.0, 0.55), (0, 0, 0.55), 26); done += 1
print('FIM', done, 'tiles em', round(time.time() - t0), 's')
# ---- montagem da folha (Pillow) ----
from PIL import Image, ImageDraw, ImageFont
cols = ['corpo', 'ação', 'neutro', 'malicioso', 'choque', 'raiva', 'riso']; rows = [(k, l) for k, l in CAST] + [('pig', 'Porco do Griffin (cut-out 3D, contorno irregular)')]
import textwrap
LW = 190; sheet = Image.new('RGB', (LW + TW * len(cols), 30 + TH * len(rows)), (36, 26, 44)); dr = ImageDraw.Draw(sheet)
def _font(sz):
    for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', '/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf'):
        if os.path.exists(p): return ImageFont.truetype(p, sz)
    return ImageFont.load_default()
f = _font(14); f2 = _font(12)
for j, c in enumerate(cols): dr.text((LW + j * TW + TW // 2 - 24, 8), c, fill=(240, 232, 250), font=f)
for i, (k, l) in enumerate(rows):
    dr.multiline_text((8, 30 + i * TH + 8), '\n'.join(textwrap.wrap(l, 22)), fill=(240, 232, 250), font=f)
    for j in range(len(cols)):
        names = [n for n in os.listdir(TILES) if n.startswith(f'{k}_{j}')]
        if k == 'pig' and j >= 3: continue
        if names: sheet.paste(Image.open(os.path.join(TILES, names[0])).convert('RGB'), (LW + j * TW, 30 + i * TH)); dr.text((LW + j * TW + 8, 30 + i * TH + TH - 20), (['comer', 'trotar', 'morto'][j] if k == 'pig' else cols[j]), fill=(60, 40, 80), font=f2)
sheet.save(os.path.join(ROOT, 'design', 'character-sheet.png')); print('folha:', sheet.size)
