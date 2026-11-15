#!/usr/bin/env python3
"""Narração pt-BR com voz de LICENÇA ABERTA: Piper (voz `cadu`, dataset CC0 — OHF-Voice/voice-datasets; ajustada de modelo base também CC0) sintetizada FRASE A FRASE,
com o tempo de cada palavra obtido por alinhamento determinístico (programação dinâmica sobre o envelope de energia × pesos fonêmicos), refinado nos mínimos de energia;
faster-whisper (MIT) só como verificação cruzada opcional (CROSSCHECK=1).
Gera audio/lines/*.wav, audio/voice.wav e script/word-timings.json (mesmo formato do pipeline anterior).
Uso: python3 tools/build_voice.py [--voice cadu] [--length 0.93]"""
import json, os, re, subprocess, sys, difflib
import numpy as np, wave
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
VOICE = arg('--voice', 'cadu'); LENGTH = float(arg('--length', .93)); MODELS = os.environ.get('PIPER_MODELS', '/tmp/piper_models')
SEG_GAP, LEAD, TAIL = 0.10, 0.25, 0.85; SR = 44100
story = json.load(open(f"{ROOT}/script/story.json")); os.makedirs(f"{ROOT}/audio/lines", exist_ok=True)
def run(cmd): subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
norm = lambda s: re.sub(r"[^\w]", "", s.lower())
from piper import PiperVoice, SynthesisConfig
voice = PiperVoice.load(f"{MODELS}/pt_BR-{VOICE}-medium.onnx", config_path=f"{MODELS}/pt_BR-{VOICE}-medium.onnx.json")
_asr = []
def asr_model():
    if not _asr:
        from faster_whisper import WhisperModel; _asr.append(WhisperModel('base', device='cpu', compute_type='int8'))   # só para CROSSCHECK=1
    return _asr[0]
def synth(sentence):
    ch = list(voice.synthesize(sentence, SynthesisConfig(length_scale=LENGTH))); sr = ch[0].sample_rate
    parts = []
    for c in ch: parts += [c.audio_float_array, np.zeros(int(.12 * sr), np.float32)]
    return np.concatenate(parts[:-1]).astype(np.float32), sr
def save_wav(path, a, sr):
    with wave.open(path, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())
def align(a16, tokens):
    """tempos [(start,end)] por token do roteiro, via Whisper (palavras) casadas ao texto conhecido"""
    pad = int(.5 * 16000); ap = np.concatenate([np.zeros(pad, np.float32), a16, np.zeros(pad, np.float32)])
    segs, _ = asr_model().transcribe(ap, language='pt', word_timestamps=True, beam_size=5, condition_on_previous_text=False, vad_filter=False)
    W = [(w.word.strip(), w.start - .5, w.end - .5) for s in segs for w in (s.words or [])]
    if not W: raise RuntimeError('sem palavras: ' + ' '.join(tokens))
    a = [norm(t) for t in tokens]; b = [norm(w[0]) for w in W]; sm = difflib.SequenceMatcher(None, a, b, autojunk=False); out = [None] * len(tokens)
    for tag, i0, i1, j0, j1 in sm.get_opcodes():
        if tag == 'equal':
            for k in range(i1 - i0): out[i0 + k] = (W[j0 + k][1], W[j0 + k][2])
        elif tag in ('replace',) and (i1 - i0) == (j1 - j0):
            for k in range(i1 - i0): out[i0 + k] = (W[j0 + k][1], W[j0 + k][2])
    # lacunas: interpola entre vizinhos conhecidos
    known = [i for i, v in enumerate(out) if v]
    if not known: raise RuntimeError('alinhamento falhou: ' + ' '.join(tokens))
    for i in range(len(out)):
        if out[i]: continue
        l = max([k for k in known if k < i], default=None); r = min([k for k in known if k > i], default=None)
        t0 = out[l][1] if l is not None else W[0][1]; t1 = out[r][0] if r is not None else W[-1][2]; nl = (r if r is not None else len(out)) - (l if l is not None else -1) - 1; idx = i - (l if l is not None else -1) - 1
        out[i] = (t0 + (t1 - t0) * idx / nl, t0 + (t1 - t0) * (idx + 1) / nl)
    return out
VOW = set('aeiouɐɛɔəɪʊãẽĩõũ')
def weights(tokens):
    """peso de duração por palavra: fonemas do espeak (via Piper); vogais longas, tônicas ainda maiores"""
    out = []
    for t in tokens:
        try: ph = ''.join(''.join(x) for x in voice.phonemize(re.sub(r"[^\w']", '', t))[0])
        except Exception: ph = t
        w = 0.0
        for i, c in enumerate(ph):
            if c in 'ˈˌːˑ ': continue
            w += (1.7 if c in VOW else 1.0) + (.6 if i > 0 and ph[i - 1] == 'ˈ' and c in VOW else 0)
        out.append(max(w, 1.5))
    return np.array(out)
def align_dp(a, sr, tokens):
    """fronteiras entre palavras por DP: mínimos de energia (pausas/transições) + prior proporcional ao peso fonético; devolve [(start,end)] por token"""
    hop = .005; n = int(len(a) / sr / hop); env = np.array([np.sqrt((a[int(i * hop * sr):int((i + 1) * hop * sr)] ** 2).mean() + 1e-12) for i in range(n)]); env = np.convolve(env, np.ones(4) / 4, 'same'); env = env / env.max()
    idx = np.where(env > .05)[0]; i0, i1 = int(idx[0]), int(idx[-1]) + 1; K = len(tokens)
    if K == 1: return [(i0 * hop, i1 * hop)]
    W = weights(tokens); cum = np.cumsum(W) / W.sum(); T = [i0 + (i1 - i0) * cum[k] for k in range(K - 1)]; win = int(.25 / hop); mind = int(.06 / hop); sig = .12 / hop
    cand = [np.arange(max(i0 + mind, int(T[k]) - win), min(i1 - mind, int(T[k]) + win) + 1) for k in range(K - 1)]
    cost = [env[c] * 1.0 + .35 * ((c - T[k]) / sig) ** 2 for k, c in enumerate(cand)]; best = [cost[0].copy()]; back = [None]
    for k in range(1, K - 1):
        cur = np.full(len(cand[k]), 1e9); bk = np.zeros(len(cand[k]), int)
        for j, p in enumerate(cand[k]):
            ok = np.where(cand[k - 1] + mind <= p)[0]
            if len(ok): m = ok[np.argmin(best[k - 1][ok])]; cur[j] = best[k - 1][m] + cost[k][j]; bk[j] = m
        best.append(cur); back.append(bk)
    j = int(np.argmin(best[-1])); P = [cand[-1][j]]
    for k in range(K - 2, 0, -1): j = back[k][j]; P.append(cand[k - 1][j])
    P = [i0] + P[::-1] + [i1]; out = []
    for k in range(K):
        st, en = P[k] * hop, P[k + 1] * hop; gl = 0.012 if (k > 0 and env[P[k]] < .12) else 0; gr = 0.012 if (k < K - 1 and env[P[k + 1]] < .12) else 0; out.append((st + gl, en - gr))
    return out
def align_energy(a, sr, tokens):
    """alinhamento de reserva: intervalo de fala por energia, repartido entre os tokens por nº de sílabas (grupos de vogais), refinado depois por snap()"""
    env = np.convolve(np.abs(a), np.ones(int(.02 * sr)) / int(.02 * sr), 'same'); idx = np.where(env > .06 * env.max())[0]; t0, t1 = idx[0] / sr, idx[-1] / sr
    w = np.array([max(1, len(re.findall(r"[aeiouáéíóúâêôãõàü]+", t.lower()))) for t in tokens], float); c = np.concatenate([[0], np.cumsum(w) / w.sum()]) * (t1 - t0) + t0
    return [(float(c[i]), float(c[i + 1])) for i in range(len(tokens))]
def snap(times, a, sr):
    """move cada fronteira entre palavras para o mínimo de energia próximo (±60 ms) — fronteiras naturais"""
    env = np.convolve(np.abs(a), np.ones(int(.008 * sr)) / int(.008 * sr), 'same'); res = [list(t) for t in times]
    for i in range(len(res) - 1):
        mid = (res[i][1] + res[i + 1][0]) / 2; lo, hi = int(max(0, mid - .06) * sr), int(min(len(a) / sr, mid + .06) * sr)
        if hi - lo < 10: continue
        m = (lo + int(np.argmin(env[lo:hi]))) / sr
        if res[i][1] - .02 <= m <= res[i + 1][0] + .02 or abs(res[i + 1][0] - res[i][1]) < .15: res[i][1] = max(res[i][0] + .05, min(m, res[i + 1][1] - .05)); res[i + 1][0] = res[i][1] if res[i + 1][0] - res[i][1] < .12 else res[i + 1][0]
    return res
t = LEAD; lines_out, words_out, placed = [], [], []
for ln in story["lines"]:
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", ln["text"].strip()) if s]
    t += ln["pause_before"]; l_start = t; l_end = t
    for si, sent in enumerate(sentences):
        name = f"{ln['id']}_{si}"; a, sr = synth(sent); tmp = f"{ROOT}/audio/lines/{name}_raw.wav"; save_wav(tmp, a, sr)
        toks = sent.split(); from scipy.signal import resample_poly; a16 = resample_poly(a, 16000, sr).astype(np.float32); 
        tm = align_dp(a, sr, toks)                                                                   # método principal (determinístico)
        if os.environ.get('CROSSCHECK'):                                                              # verificação cruzada com Whisper
            try:
                tw = align(a16, toks); dif = [abs(x[0] - y[0]) for x, y in zip(tm, tw)]; print(f"  {name}: dif. média DP×Whisper {np.mean(dif)*1000:.0f} ms, máx {np.max(dif)*1000:.0f} ms")
            except RuntimeError: pass
        s0 = max(0.0, tm[0][0] - .05); e0 = min(len(a) / sr, tm[-1][1] + .13); d = e0 - s0
        seg = a[int(s0 * sr):int(e0 * sr)].copy(); fade = int(.006 * sr); seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
        wav22 = f"{ROOT}/audio/lines/{name}_22k.wav"; save_wav(wav22, seg, sr); wav = f"{ROOT}/audio/lines/{name}.wav"; run(["ffmpeg", "-y", "-i", wav22, "-ar", str(SR), "-ac", "1", wav])
        os.remove(tmp); os.remove(wav22); placed.append((wav, t))
        for tok, (ws, we) in zip(toks, tm): words_out.append({"line": ln["id"], "text": tok, "start": round(t + ws - s0, 3), "end": round(t + we - s0, 3)})
        l_end = t + d; gap = SEG_GAP + (ln.get('sentence_gaps', []) + [0] * 9)[si]; t += d + gap   # sentence_gaps: pausa extra (s) depois de cada frase da linha (respiração/comédia)
    t -= gap; lines_out.append({**ln, "start": round(l_start, 3), "end": round(l_end, 3), "dur": round(l_end - l_start, 3)})
total = round(t + TAIL, 3); inputs, filt = [], []
for i, (wav, st) in enumerate(placed): inputs += ["-i", wav]; filt.append(f"[{i}:a]adelay={int(st*1000)}|{int(st*1000)}[a{i}]")
mix = "".join(f"[a{i}]" for i in range(len(placed))) + f"amix=inputs={len(placed)}:normalize=0,apad=whole_dur={total}[v]"
run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(filt) + ";" + mix, "-map", "[v]", "-ar", str(SR), "-ac", "1", f"{ROOT}/audio/voice.wav"])
json.dump({"voice": f"Piper pt_BR-{VOICE}-medium (dataset CC0)", "length_scale": LENGTH, "engine": "piper-tts (síntese local) + alinhamento de palavras por programação dinâmica (envelope de energia × pesos fonêmicos); faster-whisper só como verificação cruzada opcional", "license_voice": "CC0 (OHF-Voice/voice-datasets; modelo ajustado de base CC0)",
           "total": total, "lines": lines_out, "words": words_out}, open(f"{ROOT}/script/word-timings.json", "w"), ensure_ascii=False, indent=1)
print("total", total, "palavras", len(words_out))
