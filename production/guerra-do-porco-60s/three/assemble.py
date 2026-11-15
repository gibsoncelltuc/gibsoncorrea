#!/usr/bin/env python3
"""Monta um take a partir dos PNGs do Three.js (out/three/<edição>/fNNNN.png, 15 fps): corta cada plano na janela [início, fim) da EDL, repete cada quadro (15→30 fps, "dois em dois"),
aplica a grade (lib/grade.py), queima as legendas (ASS) e mistura a narração. Uso: python3 three/assemble.py <saida.mp4> <t_max_s> [w h]"""
import json, os, subprocess, sys, tempfile
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); out = os.path.abspath(sys.argv[1]); tmax = float(sys.argv[2]); sys.path.insert(0, f'{R}/blender')
sb = json.load(open(f'{R}/storyboard/shots.json'))['shots']; FPS = 15; seq = []
for s in sb:
    if s['start'] >= tmax: break
    fj = f"{R}/out/gltf/{s['id']}/frames.json"; d = f"{R}/out/three/{s['id']}"
    if not os.path.exists(fj): sys.exit(f"falta o plano {s['id']} (rode three/take.sh {s['id']})")
    F = json.load(open(fj))['frames']
    for i, f in enumerate(F):
        if s['start'] - 1e-6 <= f['t'] < min(s['end'], tmax) - 1e-6: seq.append(f"{d}/f{i:04d}.png")
tmp = tempfile.mkdtemp(); lst = f'{tmp}/l.txt'
with open(lst, 'w') as fh:
    for p in seq: fh.write(f"file '{p}'\nduration {1 / FPS:.6f}\n")
raw = f'{tmp}/raw.mp4'; subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-vf', 'fps=30', '-pix_fmt', 'yuv420p', '-c:v', 'libx264', '-crf', '12', raw], check=True)
subprocess.run([sys.executable, f'{R}/blender/grade.py', raw, '-', f'{tmp}/graded.mp4'], check=True, capture_output=True)
ass = f'{R}/renders/final.ass'; fonts = f'{R}/blender/fonts'; W = sys.argv[3] if len(sys.argv) > 3 else None
vf = f"ass={ass}:fontsdir={fonts}"
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{tmp}/graded.mp4', '-i', f'{R}/audio/final_mix.wav' if os.path.exists(f'{R}/audio/final_mix.wav') else f'{R}/audio/voice.wav', '-vf', vf, '-t', str(tmax), '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '192k', '-metadata:s:a:0', 'language=por', '-shortest', '-movflags', '+faststart', out], check=True)
print('ok', out, len(seq), 'quadros-base')
