#!/usr/bin/env python3
"""render-manifest.json do piloto (Blender): ffprobe do MP4, hash, ferramentas, parâmetros de render e tempos por plano (lidos dos logs).
Uso: python3 tools/make_manifest.py [renders/pilot_540.mp4] [saida=render-manifest.json] [--determinism "texto"]"""
import json, os, re, sys, glob, hashlib, subprocess, platform
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = [a for a in sys.argv[1:] if not a.startswith('--')]; video = os.path.join(R, args[0] if args else 'renders/pilot_540.mp4'); out = os.path.join(R, args[1] if len(args) > 1 else 'render-manifest.json')
det = sys.argv[sys.argv.index('--determinism') + 1] if '--determinism' in sys.argv else 'não executado'
pr = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', video]))
v = next(s for s in pr['streams'] if s['codec_type'] == 'video'); a = next((s for s in pr['streams'] if s['codec_type'] == 'audio'), {})
num, den = map(int, v['r_frame_rate'].split('/'))
h = hashlib.sha256(open(video, 'rb').read()).hexdigest()
shots = {}
for lg in sorted(glob.glob(os.path.join(R, 'blender', 'out', 'log_S*_o*.txt'))):
    m = re.match(r'log_(S\d)_o(\d)\.txt', os.path.basename(lg)); sid, off = m.group(1), int(m.group(2)); txt = open(lg, errors='ignore').read()
    f = re.search(r'FIM (\d+) frames em ([\d.]+) s', txt); b = re.search(r'build ([\d.]+) s (\d+) objetos', txt)
    d = shots.setdefault(sid, {'frames_por_passada': {}, 'segundos_por_passada': {}})
    if f: d['frames_por_passada'][f'p{off + 1}'] = int(f.group(1)); d['segundos_por_passada'][f'p{off + 1}'] = float(f.group(2))
    if b: d['objetos'] = int(b.group(2))
for sid, d in shots.items(): d['frames'] = sum(d['frames_por_passada'].values()); d['seg_total'] = round(sum(d['segundos_por_passada'].values()), 1); d['s_por_frame'] = round(d['seg_total'] / max(1, d['frames']), 1)
try:
    import bpy; bl = bpy.app.version_string
except Exception: bl = 'indisponível'
ff = subprocess.check_output(['ffmpeg', '-version']).decode().splitlines()[0]
tot = sum(d['seg_total'] for d in shots.values())
M = {'video': os.path.relpath(video, R), 'sha256_16': h[:16], 'tamanho_mb': round(os.path.getsize(video) / 1e6, 2), 'duracao_s': round(float(pr['format']['duration']), 3),
     'fps': round(num / den, 3), 'frames_video': int(v.get('nb_frames', 0)), 'resolucao': f"{v['width']}x{v['height']}", 'codec_video': f"{v['codec_name']} {v['pix_fmt']}", 'codec_audio': f"{a.get('codec_name', '-')} {a.get('sample_rate', '')} Hz",
     'renderer': {'blender': bl, 'motor': 'Cycles CPU (4 vCPU, sem GPU)', 'amostras': 12, 'denoiser': 'OpenImageDenoise (RGB+albedo+normal)', 'bounces': 3, 'view_transform': 'Standard', 'exposicao_ev': -0.45, 'resolucao_render': f"{v['width']}x{v['height']}", 'filtro': 'Blackman-Harris 1.1'},
     'pos': {'ffmpeg': ff, 'etapas': 'dissolve 0,4 s por alfa, unsharp, eq/colorbalance, bloom (screen), vinheta, grão, legendas ASS (Montserrat ExtraBold), AAC 192k'},
     'passadas': 'p1 = quadros pares (15 fps efetivos), p2 = quadros ímpares (30 fps completos)', 'planos': shots, 'tempo_total_render_s': round(tot, 1), 'maquina': platform.platform(),
     'determinismo': det, 'audio': 'audio/final_mix.wav → aac 192k (mix.py: -14 LUFS, ducking sidechain)'}
json.dump(M, open(out, 'w'), indent=1, ensure_ascii=False); print('ok', out, f"{M['resolucao']} @ {M['fps']} fps, {M['duracao_s']} s, render total {M['tempo_total_render_s']} s")
