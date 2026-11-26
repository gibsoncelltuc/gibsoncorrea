# Monta um video longo 16:9: voz por bloco (ja gerada em <dir>/voz/bNN.mp3) -> tempos -> spec.json -> frames (render_longo.mjs) -> mp4
# uso: python3 fazer_longo.py v1_fundo_mar.json v1 [teste_inicio_s teste_dur_s]
import json, subprocess, sys, os, re
S = json.load(open(sys.argv[1])); D = sys.argv[2]; os.chdir(os.path.dirname(os.path.abspath(__file__)))
dur = lambda p: float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)
GAP = 1.4; t = 0.0; blocos = []; lista = []
for i, b in enumerate(S['blocos']):
    v = f'{D}/voz/b{i:02d}.mp3'; d = dur(v); a = t; t += d + GAP
    fr = [s.strip() for s in re.split(r'(?<=[.!?:])\s+', b['texto']) if s.strip()]
    tot = sum(len(x) for x in fr); c = a + .25; frases = []
    for x in fr: L = d * len(x) / tot; frases.append([round(c, 2), round(c + L, 2), x]); c += L
    blocos.append({**{k: b[k] for k in b if k != 'texto'}, 'a': round(a, 2), 'b': round(t, 2), 'frases': frases}); lista.append((v, a))
json.dump({'titulo': S['titulo'], 'ambiente': S.get('ambiente', 'mar'), 'blocos': blocos}, open('www/spec.json', 'w'), ensure_ascii=False)
TOTAL = t; print('duracao', round(TOTAL, 1), 's')
# audio: voz posicionada + fundo grave (drone) baixo
inp = []; flt = []
for k, (v, a) in enumerate(lista): inp += ['-i', v]; flt.append(f'[{k}]adelay={int(a * 1000 + 250)}|{int(a * 1000 + 250)}[v{k}]')
n = len(lista)
flt.append(''.join(f'[v{k}]' for k in range(n)) + f'amix=inputs={n}:normalize=0[voz]')
flt.append(f'sine=f=55:d={TOTAL}[s1];sine=f=82.5:d={TOTAL}[s2];anoisesrc=d={TOTAL}:c=brown:a=0.4[nz];[s1][s2][nz]amix=3,lowpass=f=300,volume=0.10,afade=t=in:d=2,afade=t=out:st={TOTAL - 3}:d=3[amb]')
flt.append('[voz][amb]amix=2:normalize=0,loudnorm=I=-14:TP=-1.5[out]')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(flt), '-map', '[out]', '-ar', '48000', f'{D}/audio.wav'], check=True)
ini, du = (float(sys.argv[3]), float(sys.argv[4])) if len(sys.argv) > 4 else (0, TOTAL)
f0, f1 = int(ini * 30), int(min(TOTAL, ini + du) * 30) - 1
subprocess.run(['node', 'render_longo.mjs', f'{D}/frames', str(f0), str(f1), '4'], check=True)
nome = f'{D}/{S["id"]}' + ('_teste' if len(sys.argv) > 4 else '') + '.mp4'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '30', '-start_number', str(f0), '-i', f'{D}/frames/f%05d.jpg', '-ss', str(ini), '-t', str((f1 - f0 + 1) / 30), '-i', f'{D}/audio.wav',
                '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', nome], check=True)
print('pronto', nome)
