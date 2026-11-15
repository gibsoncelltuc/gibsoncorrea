#!/usr/bin/env python3
"""Pós-produção FFmpeg: monta os planos (frames Blender) com dissolve por alfa, aplica grade/bloom/vinheta/grão, queima legendas ASS e junta o áudio.
Uso: python3 blender/post.py <frames_root> <saida.mp4> [--audio audio/final_mix.wav] [--fps 30] [--every 1] [--noscale]"""
import sys, os, subprocess, glob, json, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(ROOT, 'blender'))
from lib import anim
root, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]); args = sys.argv[3:]
def opt(k, d=None): return args[args.index(k) + 1] if k in args else d
fps = int(opt('--fps', 30)); every = int(opt('--every', 1)); audio = opt('--audio', os.path.join(ROOT, 'audio', 'final_mix.wav')); grade = '--nograde' not in args
ass = os.path.join(ROOT, 'renders', 'final.ass'); fontsdir = os.path.join(ROOT, 'blender', 'fonts')
clips = []
for sid, (a, b) in anim.SHOTS.items():
    files = sorted(glob.glob(os.path.join(root, sid, 'f*.png')))
    if not files: print('sem frames para', sid); continue
    nums = [int(re.search(r'f(\d+)\.png', f).group(1)) for f in files]; clips.append((sid, nums[0], nums[-1], files, a, b))
inputs = []; filt = []; dur = anim.TOTAL
for i, (sid, n0, n1, files, a, b) in enumerate(clips):
    lst = os.path.join(root, f'{sid}.txt')
    with open(lst, 'w') as f:
        step = every / fps
        for k, fn in enumerate(files): f.write(f"file '{fn}'\nduration {step}\n")
        f.write(f"file '{files[-1]}'\n")
    inputs += ['-f', 'concat', '-safe', '0', '-i', lst]
    start = n0 / fps; lbl = f'c{i}'
    fl = f'[{i}:v]fps={fps},format=yuva420p'
    if i > 0: fl += f',fade=t=in:st=0:d={anim.DIS}:alpha=1'
    filt.append(f'{fl},setpts=PTS-STARTPTS+{start}/TB[{lbl}]')
chain = f'color=c=black:s=WxH:r={fps}:d={dur}[base]'
W, H = 0, 0
import PIL.Image as I; W, H = I.open(clips[0][3][0]).size
chain = f'color=c=black:s={W}x{H}:r={fps}:d={dur},format=yuva420p[base0]'
filt.insert(0, chain); prev = 'base0'
for i in range(len(clips)): filt.append(f'[{prev}][c{i}]overlay=eof_action=pass:format=auto[o{i}]'); prev = f'o{i}'
last = prev
if grade:
    # grade (split-tone sombras azul/roxo + realces quentes), nitidez, contraste/saturação, bloom leve, vinheta suave e grão — calibrada contra as métricas da referência
    G = dict(gamma=float(os.environ.get('G_GAMMA', .94)), con=float(os.environ.get('G_CON', 1.06)), sat=float(os.environ.get('G_SAT', 1.03)), bloom=float(os.environ.get('G_BLOOM', .18)), vig=float(os.environ.get('G_VIG', .32)), sharp=float(os.environ.get('G_SHARP', .45)))
    filt.append(f"[{last}]format=yuv420p,unsharp=5:5:{G['sharp']}:5:5:0,eq=contrast={G['con']}:saturation={G['sat']}:gamma={G['gamma']},colorbalance=rs=0.015:gs=-0.008:bs=0.045:rh=0.03:gh=0.012:bh=-0.02,split[g0][g1]")
    filt.append('[g1]curves=all=\'0/0 0.7/0 0.9/0.4 1/1\',gblur=sigma=%d[bl]' % max(6, W // 45)); filt.append(f"[g0][bl]blend=all_mode=screen:all_opacity={G['bloom']}[g2]")
    filt.append(f"[g2]vignette=angle={G['vig']},noise=alls=4:allf=t[gf]"); last = 'gf'
if os.path.exists(ass): filt.append(f"[{last}]subtitles={ass}:fontsdir={fontsdir}[sub]"); last = 'sub'
filt.append(f'[{last}]format=yuv420p[v]')
cmd = ['ffmpeg', '-y', '-v', 'error', *inputs, '-i', audio, '-filter_complex', ';'.join(filt), '-map', '[v]', '-map', f'{len(clips)}:a', '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-af', f'apad=whole_dur={dur}', '-t', f'{dur}', '-movflags', '+faststart', out]
print(' '.join(cmd[:6]), '... ', len(clips), 'planos'); r = subprocess.run(cmd, capture_output=True, text=True); print(r.stderr[-1500:] if r.returncode else 'ok', out)
