#!/usr/bin/env python3
"""Folha de contato de um MP4: N quadros uniformes com timecode (para revisão visual e entrega).
Uso: python3 tools/contact_sheet.py <video.mp4> <saida.png> [cols=6] [rows=3] [thumb_w=270] [--t 0.5,1.2,...]"""
import sys, os, subprocess, json, tempfile
from PIL import Image, ImageDraw, ImageFont
args = [a for a in sys.argv[1:] if not a.startswith('--')]; video, out = args[0], args[1]
cols = int(args[2]) if len(args) > 2 else 6; rows = int(args[3]) if len(args) > 3 else 3; tw = int(args[4]) if len(args) > 4 else 270
dur = float(json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', video]))['format']['duration'])
ts = [float(x) for x in sys.argv[sys.argv.index('--t') + 1].split(',')] if '--t' in sys.argv else [(k + .5) * dur / (cols * rows) for k in range(cols * rows)]
tmp = tempfile.mkdtemp(); ims = []
for k, t in enumerate(ts):
    p = os.path.join(tmp, f'{k:03d}.png')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', f'{t:.3f}', '-i', video, '-frames:v', '1', '-vf', f'scale={tw}:-2', p], check=True); ims.append((t, Image.open(p).convert('RGB')))
th = ims[0][1].size[1]; rows = (len(ims) + cols - 1) // cols; sheet = Image.new('RGB', (cols * tw, rows * th), (18, 14, 26)); d = ImageDraw.Draw(sheet)
try: f = ImageFont.truetype('/home/user/gibsoncorrea/production/guerra-do-porco/blender/fonts/Montserrat-ExtraBold.ttf', max(12, tw // 14))
except Exception: f = ImageFont.load_default()
for k, (t, im) in enumerate(ims):
    x, y = (k % cols) * tw, (k // cols) * th; sheet.paste(im, (x, y)); d.text((x + 6, y + 4), f'{t:05.2f}s', font=f, fill=(255, 255, 255), stroke_width=2, stroke_fill=(18, 14, 26))
sheet.save(out); print('ok', out, sheet.size)
