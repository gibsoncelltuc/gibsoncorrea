#!/usr/bin/env python3
# RECONSTITUIR (24/11, pedido do Gibson: "nao e' renderizar do zero: so' as partes que precisam do reparo, e remonta").
# Video ja entregue cujos trechos (ckpt) foram apagados para liberar disco: recorta o mp4 entregue de volta em trechos de 150 quadros
# (com a legenda que ja esta queimada), compara o roteiro ENTREGUE com o corrigido e marca so' as cenas que mudaram.
# A fila (make_video.sh) refaz so' os trechos dessas cenas e remonta. Se a VOZ mudou (texto diferente), nao da: o video inteiro e' refeito.
# uso: python3 reconstituir.py <id> <mp4_entregue> <beats_entregue.json>
import json, os, re, subprocess, sys
ID, MP4, OLD = sys.argv[1:4]
VOL = {'quadro', 'cx', 'cz', 'h', 'd0', 'd1', '_auto_vis', '_susp_ok', 'susp_ok', '_susp_tela'}
nb = json.load(open(f'videos/{ID}/beats.json'))['beats']; ob = json.load(open(OLD))['beats']
if [b['say'] for b in nb] != [b['say'] for b in ob]:
    print(f'{ID}: o TEXTO mudou (voz nova) -> video inteiro'); sys.exit(2)
mud = [f'b{i}' for i, (a, b) in enumerate(zip(nb, ob)) if {k: v for k, v in a.items() if k not in VOL} != {k: v for k, v in b.items() if k not in VOL}]
subprocess.run(['./build3.sh', ID], capture_output=True)
novo = subprocess.run(['python3', 'cenas_hash.py', ID], capture_output=True, text=True).stdout
if not novo.strip(): print(f'{ID}: sem impressao das cenas'); sys.exit(3)
N = json.load(open(f'stories/{ID}/work/phrases.json'))['frames30']
nf = int(subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', MP4], capture_output=True, text=True).stdout.strip() or 0)
if abs(nf - N) > 2: print(f'{ID}: o mp4 tem {nf} quadros e a voz pede {N} -> video inteiro'); sys.exit(4)
C = f'ckpt/{ID}'; os.makedirs(C, exist_ok=True)
open(f'{C}/cenas.txt', 'w').write('reconstituindo antigo\n')   # marca ja' no inicio: a limpeza de disco nao apaga um ckpt em refacao
_cut = ','.join(str(k * 150) for k in range(1, (N + 149) // 150))   # um passe so': quadro-chave a cada 150 e corta em trechos
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', MP4, '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-g', '30', '-keyint_min', '30', '-sc_threshold', '0', '-r', '30',
                '-force_key_frames', 'expr:eq(mod(n,150),0)', '-f', 'segment', '-segment_frames', _cut, '-reset_timestamps', '1', f'{C}/seg_%03d.mp4'], check=True)
open(f'{C}/cenas.txt', 'w').write(''.join(('%s antigo\n' % l.split()[0]) if l.split()[0] in mud else l + '\n' for l in novo.strip().split('\n')))
for f in ('folha3.hash',):
    try: os.remove(f'{C}/{f}')
    except FileNotFoundError: pass
print(f'{ID}: {(N + 149) // 150} trechos recortados do video entregue; cenas a refazer: {" ".join(mud) or "nenhuma"}')
