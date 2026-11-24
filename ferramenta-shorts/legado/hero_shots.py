#!/usr/bin/env python3
"""Orquestrador oficial dos 2 Modos 100% locais da Ferramenta Shorts v10 (ZERO API externa / ZERO IA generativa):
  Modo 1: 100% Codigo (Three.js + WebGL + Canvas 2D)
  Modo 2: Hibrido Blender (Codigo v10 + Hero Shots 3D renderizados localmente via blender/hero_render.py)
Uso: python3 hero_shots.py <id> --modo <1|2> --base <base.mp4> --out <final.mp4> [--audio <wav>] [--ass <caps.ass>]
"""
import argparse, json, os, shutil, subprocess

def run(cmd):
    print('[hero_shots]', ' '.join(cmd), flush=True)
    subprocess.run(cmd, check=True)

def get_dur(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', path], capture_output=True, text=True, check=True)
    return float(r.stdout.strip())

def stitch_hero_clips(base_mp4, clips_map, out_mp4, audio_path=None, ass_path=None):
    total_dur = get_dur(base_mp4)
    tmp_dir = '/tmp/hero_stitch_' + str(os.getpid())
    os.makedirs(tmp_dir, exist_ok=True)
    intervals = sorted(clips_map, key=lambda x: x['t_start'])
    segs, cur, idx = [], 0.0, 0
    for iv in intervals:
        ts, te, clip = max(0.0, iv['t_start']), min(total_dur, iv['t_end']), iv['clip']
        if ts > cur + 0.05:
            seg = os.path.join(tmp_dir, f'seg_{idx:02d}.mp4')
            run(['ffmpeg', '-y', '-ss', f'{cur:.3f}', '-to', f'{ts:.3f}', '-i', base_mp4,
                 '-an', '-r', '30', '-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1',
                 '-c:v', 'libx264', '-preset', 'fast', '-crf', '17', '-pix_fmt', 'yuv420p', seg])
            segs.append(seg); idx += 1
        hdur = max(0.5, te - ts)
        seg = os.path.join(tmp_dir, f'seg_{idx:02d}.mp4')
        run(['ffmpeg', '-y', '-stream_loop', '-1', '-i', clip, '-t', f'{hdur:.3f}',
             '-an', '-r', '30', '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1',
             '-c:v', 'libx264', '-preset', 'fast', '-crf', '17', '-pix_fmt', 'yuv420p', seg])
        segs.append(seg); idx += 1
        cur = te
    if cur < total_dur - 0.05:
        seg = os.path.join(tmp_dir, f'seg_{idx:02d}.mp4')
        run(['ffmpeg', '-y', '-ss', f'{cur:.3f}', '-to', f'{total_dur:.3f}', '-i', base_mp4,
             '-an', '-r', '30', '-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1',
             '-c:v', 'libx264', '-preset', 'fast', '-crf', '17', '-pix_fmt', 'yuv420p', seg])
        segs.append(seg)
    lst = os.path.join(tmp_dir, 'list.txt')
    with open(lst, 'w') as fp:
        for sg in segs: fp.write(f"file '{sg}'\n")
    concat_raw = os.path.join(tmp_dir, 'concat.mp4')
    run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', concat_raw])
    cmd = ['ffmpeg', '-y', '-i', concat_raw, '-i', audio_path if (audio_path and os.path.exists(audio_path)) else base_mp4]
    if ass_path and os.path.exists(ass_path):
        esc = ass_path.replace('\\', '/').replace(':', '\\:')
        cmd += ['-vf', f"ass='{esc}'"]
    cmd += ['-map', '0:v:0', '-map', '1:a:0?', '-r', '30', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', out_mp4]
    run(cmd)
    shutil.rmtree(tmp_dir, ignore_errors=True)
    print(f'[hero_shots] PRONTO -> {out_mp4}')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('id')
    ap.add_argument('--modo', type=int, choices=[1, 2], required=True)
    ap.add_argument('--base', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--audio', default=None)
    ap.add_argument('--ass', default=None)
    args = ap.parse_args()

    manifest_path = f'stories/{args.id}/hero_manifest.json'
    if args.modo == 1 or not os.path.exists(manifest_path):
        shutil.copy2(args.base, args.out)
        print(f'[hero_shots] Modo 1 (100% codigo) -> {args.out}')
        return

    man = json.load(open(manifest_path, encoding='utf-8'))
    folder = f'stories/{args.id}/blender_clips'
    if shutil.which('blender') and os.path.exists('blender/hero_render.py'):
        run(['blender', '-b', '--python', 'blender/hero_render.py', '--', args.id])

    clips_map = []
    for hs in man.get('hero_shots', []):
        cand = os.path.join(folder, f"{hs['beat']}.mp4")
        if os.path.exists(cand):
            clips_map.append({'t_start': hs['t_start'], 't_end': hs['t_end'], 'clip': cand})
        else:
            print(f"[hero_shots] AVISO: {cand} nao encontrado; mantendo base 100% codigo para {hs['beat']}")
    if not clips_map:
        shutil.copy2(args.base, args.out)
        return
    stitch_hero_clips(args.base, clips_map, args.out, audio_path=args.audio, ass_path=args.ass)

if __name__ == '__main__':
    main()
