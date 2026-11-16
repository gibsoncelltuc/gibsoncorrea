"""Audio kit: music + SFX primitives, mix at 50% of voice. Usage: python3 audio_story.py <story> <frames>  (cues in stories/<id>/cues.py)"""
import numpy as np, subprocess, wave, math, sys, os
SR = 48000; STORY = sys.argv[1]; FR = int(sys.argv[2]); DUR = FR / 30; N = int(DUR * SR); rng = np.random.default_rng(23)
F = lambda f: f / 30
midi = lambda m: 440 * 2 ** ((m - 69) / 12)
import json as _json, unicodedata as _ud
_WORDS = _json.load(open(f'stories/{STORY}/work/words.json'))
_nrm = lambda s: ''.join(ch for ch in _ud.normalize('NFD', s.lower()) if ch.isalnum() and ord(ch) < 128)
# FE(frame): frame on the SOURCE-language timeline -> seconds on this story's voice (retimed stories); identity otherwise
_RT = _json.load(open(f'stories/{STORY}/retime.json'))['anchors'] if os.path.exists(f'stories/{STORY}/retime.json') else None
def FE(f):
    if not _RT: return f / 30
    A = _RT
    if f <= A[0][0]: return (f - A[0][0] + A[0][1]) / 30
    for i in range(len(A) - 1):
        if f <= A[i + 1][0]:
            t = 1 if A[i + 1][0] == A[i][0] else (f - A[i][0]) / (A[i + 1][0] - A[i][0]); return (A[i][1] + (A[i + 1][1] - A[i][1]) * t) / 30
    return (f - A[-1][0] + A[-1][1]) / 30
def Wf(token, nth=1, off=0):   # frame (30 fps) where the nth occurrence of `token` starts -- cues tied to words, any language
    c = 0
    for w in _WORDS:
        if _nrm(w['w']) == _nrm(token):
            c += 1
            if c == nth: return int(round(w['s'] * 30)) + off
    raise SystemExit('cue anchor not found: %s #%d' % (token, nth))
def place(buf, sig, t0, gain=1.0):
    i = int(t0 * SR); j = min(N, i + len(sig))
    if 0 <= i < N and j > i: buf[i:j] += sig[: j - i] * gain
def lpf(x, c): X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X *= 1 / (1 + (f / c) ** 4); return np.fft.irfft(X, len(x)).astype(np.float32)
def hpf(x, c): X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X *= 1 - 1 / (1 + (f / c) ** 4); return np.fft.irfft(X, len(x)).astype(np.float32)
def noise(d): return rng.standard_normal(int(d * SR)).astype(np.float32)
def tt(d): return np.arange(int(d * SR)) / SR
def env(n, a=0.005, r=0.2): t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / r)
def tone(f, d, a=0.01, r=0.3, harm=3, b=0.5): t = tt(d); s = sum((b ** k) * np.sin(2 * np.pi * f * (k + 1) * t) / (k + 1) for k in range(harm)); return (s * env(len(t), a, r)).astype(np.float32)
# ---------------- music ----------------
music = np.zeros(N, np.float32)
def section(f0, f1, fn):
    t0 = F(f0); t1 = F(f1); fn(t0, t1)
def snare(): return (lpf(hpf(noise(0.14), 1500), 7000) * np.exp(-tt(0.14) * 26) * 0.7 + np.sin(2 * np.pi * 200 * tt(0.14)) * np.exp(-tt(0.14) * 30) * 0.4).astype(np.float32)
def kick(): t = tt(0.25); fr = 55 + 90 * np.exp(-t * 28); return (np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 11)).astype(np.float32)
def fife(f, d): t = tt(d); return (np.sin(2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 5.5 * t)) * 0.7 + 0.25 * np.sin(2 * np.pi * 2 * f * t)) * np.minimum(1, t / 0.02) * np.exp(-t / (d * 1.1)) * 0.6
def pluckw(f, d=0.35): return tone(f, d, 0.003, d * 0.3, 5, 0.55)
def pad(f, d): t = tt(d); s = sum(np.sin(2 * np.pi * f * k * t + k) / k for k in (1, 2, 3)) * 0.4; return (s * np.minimum(1, t / (d * 0.3)) * np.minimum(1, (d - t) / (d * 0.3))).astype(np.float32)
def playful(t0, t1, bpm=120):
    b = 60 / bpm; t = t0; k = 0
    chords = [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]]
    while t < t1:
        ch = chords[(k // 4) % 4]
        place(music, pluckw(midi(ch[k % 3] + 12), 0.28), t, 0.35); place(music, tone(midi(ch[0] - 12), 0.3, 0.005, 0.15, 2), t, 0.45) if k % 2 == 0 else None
        t += b / 2; k += 1
def march(t0, t1, bpm=112):
    b = 60 / bpm; t = t0; k = 0; mel = [67, 67, 71, 74, 72, 71, 69, 67]
    while t < t1:
        place(music, snare(), t, 0.5 if k % 2 == 0 else 0.3); place(music, snare(), t + b / 4, 0.18); place(music, kick(), t, 0.5) if k % 2 == 0 else None
        if k % 2 == 0: place(music, fife(midi(mel[(k // 2) % 8] + 0), b * 1.6), t, 0.4)
        t += b / 2; k += 1
def drone(t0, t1, f=55):
    d = t1 - t0; place(music, pad(f, d) * 0.9, t0, 0.35); place(music, pad(f * 1.5, d) * 0.5, t0, 0.2)
def heartbeat(t0, t1, bpm=60, g=0.8):
    t = t0
    while t < t1: place(music, kick() * 0.9, t, g); place(music, kick() * 0.6, t + 0.28, g * 0.6); t += 60 / bpm
def harp(t0, t1):
    t = t0; notes = [72, 76, 79, 84, 79, 76]; k = 0
    while t < t1: place(music, pluckw(midi(notes[k % 6]), 0.9), t, 0.4); t += 0.42; k += 1
exec(open(f'stories/{STORY}/cues.py').read().split('#--SFX--')[0])
g = np.ones(N, np.float32); ts = np.arange(N) / SR
g *= np.where(ts > F((FR-38)), np.clip(1 - (ts - F((FR-38))) / (F(FR) - F((FR-38))), 0, 1), 1)
music *= g
# ---------------- sfx ----------------
sfx = np.zeros(N, np.float32)
def gun(t, g=1.0):
    d = 1.4; x = tt(d); s = lpf(noise(d), 4000) * np.exp(-x * 14) + np.sin(2 * np.pi * (70 * np.exp(-x * 5) + 38) * x) * np.exp(-x * 7) * 0.9 + lpf(noise(d), 900) * np.exp(-x * 3.2) * 0.3
    place(sfx, s.astype(np.float32), t, g)
def cannon(t, g=1.0):
    d = 2.0; x = tt(d); s = lpf(noise(d), 1800) * np.exp(-x * 5) + np.sin(2 * np.pi * (45 * np.exp(-x * 2.5) + 28) * np.cumsum(np.ones_like(x)) / SR * 20) * 0.0 + np.sin(2 * np.pi * np.cumsum(40 * np.exp(-x * 2) + 24) / SR) * np.exp(-x * 2.6)
    place(sfx, s.astype(np.float32), t, g)
def squeal(t, d=0.7, g=0.7):
    x = tt(d); fr = 900 + 700 * np.sin(np.pi * np.minimum(1, x / d * 1.4)) ** 2 + 60 * np.sin(2 * np.pi * 28 * x); s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * 0.6 + 0.3 * np.sin(2 * np.pi * np.cumsum(fr * 2) / SR); s = s * np.minimum(1, x / 0.02) * np.minimum(1, (d - x) / 0.12)
    place(sfx, hpf(s.astype(np.float32), 300), t, g)
def snuffle(t, n=4, g=0.5):
    for i in range(n): d = 0.12; place(sfx, (lpf(hpf(noise(d), 300), 2500) * np.exp(-tt(d) * 18) * 0.8).astype(np.float32), t + i * 0.19, g)
def whoosh(t, d=0.4, g=0.4):
    x = noise(d); e = np.sin(np.pi * np.linspace(0, 1, len(x))) ** 2; place(sfx, lpf(hpf(x, 400), 4000) * e, t, g)
def ding(t, g=0.6, f=1320):
    x = tt(0.9); s = (np.sin(2 * np.pi * f * x) + 0.4 * np.sin(2 * np.pi * f * 2.76 * x)) * np.exp(-x * 5); place(sfx, s.astype(np.float32) * 0.5, t, g)
def sting(t, g=0.7):
    for i, n in enumerate([62, 59, 56]): place(sfx, tone(midi(n), 0.5, 0.01, 0.3, 4), t + i * 0.12, g * 0.5)
def thump(t, g=0.9):
    x = tt(0.4); s = np.sin(2 * np.pi * np.cumsum(70 * np.exp(-x * 14) + 38) / SR) * np.exp(-x * 9) + lpf(noise(0.4), 1200) * np.exp(-x * 30) * 0.5; place(sfx, s.astype(np.float32), t, g)
def tick(t, g=0.5): place(sfx, hpf(noise(0.02), 2500) * np.exp(-tt(0.02) * 160) + np.sin(2 * np.pi * 1300 * tt(0.02)) * np.exp(-tt(0.02) * 200), t, g)
def steps(t0, t1, per=0.26, g=0.25):
    t = t0
    while t < t1: place(sfx, (lpf(noise(0.08), 900) * np.exp(-tt(0.08) * 40)).astype(np.float32), t, g); t += per
def sea(t0, t1, g=0.16):
    d = t1 - t0; x = lpf(noise(d), 700); sw = 0.6 + 0.4 * np.sin(2 * np.pi * np.arange(len(x)) / SR / 7.0); place(sfx, (x * sw).astype(np.float32), t0, g)
def gulls(t0, t1, n=6, g=0.12):
    for i in range(n):
        t = t0 + (t1 - t0) * (i + 0.3) / n; d = 0.5; x = tt(d); fr = 1700 + 500 * np.sin(np.pi * x / d) ** 2; place(sfx, (np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * x / d)).astype(np.float32), t, g)
def birds(t0, t1, n=10, g=0.1):
    for i in range(n):
        t = t0 + (t1 - t0) * (i + 0.5) / n; x = tt(0.18); fr = 3200 + 900 * np.sin(2 * np.pi * (6 + i % 3) * x); place(sfx, (np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * x / 0.18)).astype(np.float32), t, g)
def creak(t, g=0.3): d = 0.5; x = tt(d); fr = 130 + 70 * np.sin(2 * np.pi * 6 * x); place(sfx, (np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-x * 3.5) * np.minimum(1, x / 0.03)).astype(np.float32), t, g)
def paper(t, g=0.3): d = 0.25; place(sfx, (hpf(noise(d), 2000) * np.exp(-tt(d) * 12)).astype(np.float32), t, g)
exec(open(f'stories/{STORY}/cues.py').read().split('#--SFX--')[1])
def save(name, x): x = np.clip(x, -1, 1); w = wave.open(name, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype('<i2').tobytes()); w.close()
save(f'stories/{STORY}/work/music.wav', music / (np.abs(music).max() + 1e-9) * 0.9); save(f'stories/{STORY}/work/sfx.wav', sfx / (np.abs(sfx).max() + 1e-9) * 0.9)
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", "stories/%s/voice.mp3" % STORY, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
v = np.frombuffer(raw, np.float32).copy(); voice = np.zeros(N, np.float32); voice[:min(N, len(v))] = v[:N]
def grms(x):
    w = int(0.4 * SR); fr = x[: len(x) // w * w].reshape(-1, w); r = np.sqrt((fr ** 2).mean(1)); ok = r > 0.05 * r.max(); return r[ok].mean() if ok.any() else 1e-9
vr = grms(voice); lock = lambda x, ratio: x * (vr * ratio / grms(x))
m = lock(music, 0.5); s = lock(sfx, 0.5); pk = np.abs(voice).max() * 0.7
if np.abs(s).max() > pk: s = s * (pk / np.abs(s).max())
mix = voice + m + s
print("music %.1f dB, sfx %.1f dB vs voice" % (20 * np.log10(grms(m) / vr), 20 * np.log10(max(grms(s), 1e-9) / vr)))
save(f'stories/{STORY}/work/mix_raw.wav', mix / max(1, np.abs(mix).max() / 0.95))
