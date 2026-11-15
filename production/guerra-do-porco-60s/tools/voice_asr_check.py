#!/usr/bin/env python3
"""Teste objetivo de clareza da voz ("ouvir apenas a faixa de voz para clareza, ritmo e pronúncia"): um reconhecedor de fala INDEPENDENTE (faster-whisper) transcreve
o stem de voz sozinho; compara com o roteiro (WER e CER, normalizados) e cruza os tempos das palavras com script/word-timings.json.
É um proxy automático — NÃO substitui ouvir o vídeo com som (revisão humana). Saída: qa/voice-asr.json + resumo.   Uso: python3 tools/voice_asr_check.py [audio/voice.wav]"""
import json, os, re, sys, unicodedata
import numpy as np
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); A = sys.argv[1] if len(sys.argv) > 1 else 'audio/voice.wav'
def norm(s): s = unicodedata.normalize('NFD', s.lower()); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn'); return re.findall(r"[a-z0-9$]+", s)
def edit(a, b):
    d = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        p, d[0] = d[0], i
        for j in range(1, len(b) + 1): p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (a[i - 1] != b[j - 1]))
    return d[-1]
import subprocess
wav = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{R}/{A}', '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True, check=True).stdout; x = np.frombuffer(wav, np.float32)
from faster_whisper import WhisperModel
model = WhisperModel(os.environ.get('WHISPER', 'base'), device='cpu', compute_type='int8', cpu_threads=int(os.environ.get('THREADS', 1)))
segs, info = model.transcribe(x, language='pt', word_timestamps=True, vad_filter=False, beam_size=5, condition_on_previous_text=False)
words = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
hyp = norm(' '.join(w for w, _, _ in words)); wt = json.load(open(f'{R}/script/word-timings.json', encoding='utf-8')); ref_words = [w for w in wt['words']]
ref = norm(' '.join(w['text'] for w in ref_words))
# números: o roteiro usa "cem"/"dez"; o ASR pode escrever 100/10 → normaliza dígitos para palavras
num = {'100': 'cem', '10': 'dez', '5': 'cinco', '1859': 'mil oitocentos e cinquenta e nove'}; hyp = sum([num.get(h, h).split() for h in hyp], [])
wer = edit(ref, hyp) / len(ref); cer = edit(list(' '.join(ref)), list(' '.join(hyp))) / len(' '.join(ref))
# tempos: alinha por palavra normalizada (monotônico) e mede o desvio de início
rw = [(norm(w['text'])[0] if norm(w['text']) else '', w['start']) for w in ref_words]; dev = []; j = 0
for h, s, e in words:
    hn = norm(h); hn = hn[0] if hn else ''
    for k in range(j, min(j + 4, len(rw))):
        if rw[k][0] == hn: dev.append(abs(s - rw[k][1])); j = k + 1; break
rep = {'modelo': f"faster-whisper {os.environ.get('WHISPER', 'base')} (int8, CPU)", 'idioma_detectado': info.language, 'prob_idioma': round(float(info.language_probability), 3), 'palavras_roteiro': len(ref), 'palavras_reconhecidas': len(hyp),
       'WER': round(wer, 3), 'CER': round(cer, 3), 'transcricao': ' '.join(hyp), 'roteiro': ' '.join(ref), 'palavras_casadas_p/tempo': len(dev), 'desvio_inicio_medio_s': round(float(np.mean(dev)), 3) if dev else None, 'desvio_inicio_max_s': round(float(np.max(dev)), 3) if dev else None,
       'nota': 'proxy automático de clareza; o ASR tem viés de primeira palavra e erra nomes próprios — a escuta humana segue pendente'}
json.dump(rep, open(f'{R}/qa/voice-asr.json', 'w'), ensure_ascii=False, indent=1)
print(f"ASR {rep['modelo']}: idioma {info.language} ({rep['prob_idioma']}) · WER {rep['WER']:.1%} · CER {rep['CER']:.1%} · {rep['palavras_casadas_p/tempo']} palavras casadas, desvio médio {rep['desvio_inicio_medio_s']} s, máx {rep['desvio_inicio_max_s']} s")
print('hip:', rep['transcricao']); print('ref:', rep['roteiro'])
sys.exit(0 if wer <= 0.15 else 1)
