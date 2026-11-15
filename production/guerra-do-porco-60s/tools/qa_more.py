#!/usr/bin/env python3
"""ETAPA B (parte 2): 15 checagens EXTRAS do vídeo montado (somam-se às 17 de qa.py + 4 de qa_extra.py = 36). Foco no que o olho humano pega e as outras não: fluidez, dinamismo,
travamento, ritmo de cortes, cobertura de legenda, silêncios, clipping, equilíbrio de stems, sincronia A/V, bitrate e consistência de cor entre planos.
Uso: python3 tools/qa_more.py <video.mp4> [saida.json]   → linhas PASS/FAIL"""
import json, os, re, subprocess, sys
import numpy as np
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); V = sys.argv[1]; OUT = sys.argv[2] if len(sys.argv) > 2 else 'qa/more.json'; res = []
def rec(n, ok, d=''): res.append(dict(name=n, **{'pass': bool(ok)}, detail=str(d))); print(('PASS ' if ok else 'FAIL ') + n + (' — ' + str(d) if d else ''))
pr = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', V])); vs = next(s for s in pr['streams'] if s['codec_type'] == 'video'); au = next((s for s in pr['streams'] if s['codec_type'] == 'audio'), None)
dur = float(pr['format']['duration']); fps = eval(vs['r_frame_rate']); W, H = int(vs['width']), int(vs['height'])
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', V, '-vf', 'scale=108:192,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout; A = np.frombuffer(raw, np.uint8).reshape(-1, 192, 108).astype(np.float32); n = len(A)
d = np.abs(np.diff(A, axis=0)).mean((1, 2)) if n > 1 else np.zeros(1)
# 1 fps constante e contagem de quadros coerente
rec('fps constante (r_frame_rate = avg_frame_rate) e nb_frames ≈ duração×fps', abs(eval(vs['avg_frame_rate']) - fps) < .01 and abs(n - dur * fps) <= 3, f'{fps:g} fps, {n} quadros, {dur:.2f} s')
# 2 fluidez: o estilo "dois em dois" repete 1 quadro; mais que isso = travando. Fração de pares de quadros praticamente iguais (limiar sobre ruído de grão)
dup = float((d < 1.2).mean()); rec('fluidez: ≤ 15 % de quadros repetidos (30 fps reais ≈ 5 %; "dois em dois" = 48 % e TRAVA — reprovado pelo usuário)', dup <= .15, f'{dup:.0%} repetidos')
# 3 nenhum trecho parado > 0,7 s (sequência de quadros com movimento < limiar)
run = best = 0
for x in d: run = run + 1 if x < 1.2 else 0; best = max(best, run)
rec('nenhum trecho parado > 0,7 s', best / fps <= .7, f'maior trecho parado {best / fps:.2f} s')
# 4 energia de movimento: mediana dos deslocamentos por segundo ≥ piso (vídeo dinâmico)
ms = np.array([d[int(i * fps):int((i + 1) * fps)].mean() for i in range(int(dur)) if len(d[int(i * fps):int((i + 1) * fps)])]); rec('dinamismo: movimento médio por segundo ≥ 2,0 em ≥ 90 % dos segundos', (ms >= 2.0).mean() >= .9, f'{(ms >= 2.0).mean():.0%} dos segundos; mediana {np.median(ms):.1f}')
# 5–6 ritmo de edição pela EDL (storyboard/shots.json): 15–40 cortes/min, média 1,4–3,0 s, nenhum plano > 4,5 s (os dissolves de 0,4 s não geram salto de imagem, por isso não se mede pelo vídeo)
try:
    sh = json.load(open(f'{R}/storyboard/shots.json'))['shots']; dd = np.array([x['dur'] for x in sh]); rate = (len(sh) - 1) / dd.sum() * 60
    rec('ritmo de edição: 15–40 cortes por minuto (prints ≈ 25)', 15 <= rate <= 40, f'{rate:.0f}/min, {len(sh)} planos')
    rec('duração média do plano 1,4–3,0 s e nenhum plano > 4,5 s', 1.4 <= dd.mean() <= 3.0 and dd.max() <= 4.5, f'média {dd.mean():.2f} s, máx {dd.max():.2f} s')
except Exception as ex: rec('ritmo de edição (EDL)', False, repr(ex)[:100])
# 7 consistência de brilho entre segundos (sem flicker de exposição)
lum = np.array([A[int(i * fps):int((i + 1) * fps)].mean() for i in range(int(dur))]); rec('brilho médio por segundo varia < 35 % da mediana', (np.abs(lum - np.median(lum)) / np.median(lum)).max() < .35, f'máx {(np.abs(lum - np.median(lum)) / np.median(lum)).max():.0%}')
# 8 bitrate de vídeo saudável (qualidade) para a resolução
br = float(pr['format'].get('bit_rate', 0)) / 1e6; need = 0.9 * (W * H) / (540 * 960); rec('bitrate de vídeo ≥ 0,9 Mb/s por 540×960 equivalente', br >= need, f'{br:.2f} Mb/s (mín {need:.2f})')
if au:
    # 9 duração de áudio ≈ vídeo
    ad = float(au.get('duration', dur)); rec('áudio e vídeo com a mesma duração (±0,15 s)', abs(ad - dur) <= .15, f'v {dur:.2f} s × a {ad:.2f} s')
    pcm = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', V, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout, np.int16).astype(np.float32) / 32768
    # 10 sem clipping
    rec('sem clipping (amostras ≥ 0,999 < 0,01 %)', (np.abs(pcm) >= .999).mean() < 1e-4, f'{(np.abs(pcm) >= .999).mean():.4%}')
    # 11 silêncios: nenhum buraco > 1,2 s abaixo de −50 dBFS no meio (exceto cauda)
    w = int(.05 * 16000); e = np.sqrt(np.convolve(pcm ** 2, np.ones(w) / w, 'same')); db = 20 * np.log10(e + 1e-9); r = b = 0
    for x in db[:int((dur - 1.0) * 16000)]: r = r + 1 if x < -50 else 0; b = max(b, r)
    rec('sem silêncio morto > 1,2 s (música/ambiência cobrem as pausas)', b / 16000 <= 1.2, f'maior silêncio {b / 16000:.2f} s')
    # 12 LRA (variação de loudness) ≤ 7 LU
    o = subprocess.run(['ffmpeg', '-nostats', '-i', V, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr; lra = float(re.findall(r'LRA:\s+([\d.]+)', o)[-1]); rec('variação de loudness (LRA) ≤ 7 LU', lra <= 7, f'{lra:.1f} LU')
    # 13 banda de graves não domina (mix equilibrado): energia < 200 Hz < 55 % do total
    X = np.abs(np.fft.rfft(pcm[:len(pcm) // 2 * 2])) ** 2; fr = np.fft.rfftfreq(len(pcm[:len(pcm) // 2 * 2]), 1 / 16000); lowr = X[fr < 200].sum() / X.sum(); rec('graves (< 200 Hz) < 55 % da energia (mix equilibrado)', lowr < .55, f'{lowr:.0%}')
# 14 consistência de cor entre planos: saturação média por segundo dentro de ±45 % da mediana
sat = []
for i in range(int(dur)):
    fr_ = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(i + .5), '-i', V, '-frames:v', '1', '-vf', 'scale=54:96', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    if len(fr_) == 54 * 96 * 3: a = np.frombuffer(fr_, np.uint8).reshape(-1, 3).astype(float) / 255; sat.append(float(((a.max(1) - a.min(1)) / np.maximum(a.max(1), 1e-4)).mean()))
sat = np.array(sat); rec('saturação consistente entre segundos (±45 % da mediana)', (np.abs(sat - np.median(sat)) / np.median(sat)).max() < .45, f'máx {(np.abs(sat - np.median(sat)) / np.median(sat)).max():.0%}')
# 15 cobertura de legenda: legendas existem durante a fala (SRT cobre ≥ 75 % do tempo de voz)
try:
    srt = open(f'{R}/renders/final.srt', encoding='utf-8').read().strip().split('\n\n'); tt = lambda x: sum(float(p) * m for p, m in zip(re.split('[:,]', x), (3600, 60, 1, .001))); cov = 0
    for blk in srt: a_, b_ = [tt(x.strip()) for x in blk.split('\n')[1].split('-->')]; cov += min(b_, dur) - a_
    wt = json.load(open(f'{R}/script/word-timings.json')); sp = sum(l['dur'] for l in wt['lines']); rec('legendas cobrem ≥ 75 % do tempo de fala', cov / sp >= .75, f'{cov / sp:.0%} (legendas {cov:.1f} s / fala {sp:.1f} s)')
except Exception as ex: rec('legendas cobrem ≥ 75 % do tempo de fala', False, repr(ex)[:100])
json.dump(dict(video=V, checks=res, passed=sum(r['pass'] for r in res), total=len(res)), open(f'{R}/{OUT}', 'w'), ensure_ascii=False, indent=1); print(f"{sum(r['pass'] for r in res)}/{len(res)}"); sys.exit(0 if all(r['pass'] for r in res) else 1)
