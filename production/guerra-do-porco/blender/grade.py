#!/usr/bin/env python3
"""Rota Blender + Remotion + FFmpeg: aplica a grade de cor à montagem do Remotion, sobrepõe as legendas (sequência PNG com alfa) e codifica o MP4 final.
Uso: python3 blender/grade.py <montagem.mp4> <pasta_legendas_png|-> <saida.mp4> [--crf 17]"""
import sys, os, subprocess, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import grade as GR
a = [x for x in sys.argv[1:] if not x.startswith('--')]; mont, caps, out = os.path.abspath(a[0]), a[1], os.path.abspath(a[2])
crf = sys.argv[sys.argv.index('--crf') + 1] if '--crf' in sys.argv else '17'
pr = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', mont]))
v = next(s for s in pr['streams'] if s['codec_type'] == 'video'); W = v['width']; num, den = map(int, v['r_frame_rate'].split('/')); fps = num / den
inputs = ['-i', mont]; filt, last = GR.filters('0:v', W)
if caps != '-':
    files = sorted(glob.glob(os.path.join(caps, '*.png'))); pat = os.path.join(caps, os.path.basename(files[0]).rsplit('-', 1)[0] + '-%0' + str(len(os.path.basename(files[0]).rsplit('-', 1)[1].split('.')[0])) + 'd.png')
    inputs += ['-framerate', str(fps), '-start_number', str(int(os.path.basename(files[0]).rsplit('-', 1)[1].split('.')[0])), '-i', pat]; filt.append(f'[{last}][1:v]overlay=format=auto[ov]'); last = 'ov'
filt.append(f'[{last}]format=yuv420p[v]')
cmd = ['ffmpeg', '-y', '-v', 'error', *inputs, '-filter_complex', ';'.join(filt), '-map', '[v]', '-map', '0:a?', '-c:v', 'libx264', '-crf', crf, '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-shortest', '-movflags', '+faststart', out]
r = subprocess.run(cmd, capture_output=True, text=True); print(r.stderr[-1200:] if r.returncode else 'ok', out)
