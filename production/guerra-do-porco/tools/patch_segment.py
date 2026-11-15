#!/usr/bin/env python3
"""REPARO DE TRECHO DO VÍDEO MONTADO: refaz só [t0,t1] (Remotion --frames, grade e legenda do trecho) e costura com o resto SEM recodificar o que já estava bom.
Uso: python3 tools/patch_segment.py <video.mp4> <t0> <t1>   (depois de refazer os quadros ruins com tools/repair_frames.py e regenerar montage/data.json)"""
import os, subprocess, sys, tempfile, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(R); v = os.path.abspath(sys.argv[1]); t0, t1 = float(sys.argv[2]), float(sys.argv[3])
pr = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'stream=r_frame_rate,width,height', '-show_entries', 'format=duration', '-of', 'json', v])); fps = eval(pr['streams'][0]['r_frame_rate']); dur = float(pr['format']['duration'])
a, b = int(round(t0 * fps)), int(round(t1 * fps)); tmp = tempfile.mkdtemp(); sh = lambda c, **k: subprocess.run(c, check=True, **k)
sh(['python3', 'tools/make_montage_data.py']); raw = f'{tmp}/seg_raw.mp4'
sh(['npx', '--no-install', 'remotion', 'render', 'montage/index.ts', 'Montage', raw, f'--frames={a}-{b - 1}', '--public-dir=montage/public', '--concurrency=3', '--log=warn'])
sh(['python3', 'blender/grade.py', raw, '-', f'{tmp}/seg_g.mp4']); fonts = f'{R}/blender/fonts'
sh(['ffmpeg', '-v', 'error', '-y', '-i', f'{tmp}/seg_g.mp4', '-vf', f"ass=renders/final.ass:fontsdir={fonts},setpts=PTS+{t0}/TB", '-an', '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p', f'{tmp}/seg.mp4'])
# a legenda foi queimada com tempo absoluto: o setpts acima desloca o trecho para t0 antes de queimar? → refazer na ordem certa
sh(['ffmpeg', '-v', 'error', '-y', '-i', f'{tmp}/seg_g.mp4', '-vf', f"setpts=PTS+{t0}/TB,ass=renders/final.ass:fontsdir={fonts},setpts=PTS-{t0}/TB", '-an', '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', str(fps), f'{tmp}/seg.mp4'])
parts = []
def cut(s, e, name):
    out = f'{tmp}/{name}.mp4'; sh(['ffmpeg', '-v', 'error', '-y', '-ss', str(s), '-to', str(e), '-i', v, '-an', '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', str(fps), out]); parts.append(out)
if t0 > 0: cut(0, t0, 'p0')
parts.append(f'{tmp}/seg.mp4')
if t1 < dur: cut(t1, dur, 'p2')
open(f'{tmp}/l.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts)); sh(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/l.txt', '-i', v, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'copy', '-shortest', '-movflags', '+faststart', f'{tmp}/out.mp4'])
os.replace(f'{tmp}/out.mp4', v); print(f'trecho {t0}–{t1} s refeito e costurado em {v}')
