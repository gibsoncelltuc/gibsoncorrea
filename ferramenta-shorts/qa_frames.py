#!/usr/bin/env python3
"""Frame-by-frame QA for a rendered short. Usage: python3 qa_frames.py frames [story.js] [--sheet out.jpg]
Per frame: black/white/flat, blur, isolated temporal glitches (frame differs from BOTH neighbours while the neighbours agree),
exposure jumps, and big colour drift. Frames at known hard cuts (CUTS in story.js) are exempt from the spike test.
Writes qa_report.json {frames:[{f,reasons}]} and, with --sheet, a contact sheet of the flagged frames.
Re-render only the flagged ones:  python3 qa_frames.py ... --rerender  (deletes them, then run render.mjs with RESUME=1)."""
import sys, os, re, json
import numpy as np
from PIL import Image
_skip = {sys.argv[i + 1] for i, a in enumerate(sys.argv) if a in ('--sheet', '--range', '--report') and i + 1 < len(sys.argv)}
args = [a for a in sys.argv[1:] if not a.startswith('--') and a not in _skip]; D = args[0]; story = args[1] if len(args) > 1 else 'web/story.js'
sheet = sys.argv[sys.argv.index('--sheet') + 1] if '--sheet' in sys.argv else None
fs = sorted(f for f in os.listdir(D) if f.startswith('f') and f.endswith('.jpg'))
if '--range' in sys.argv:   # so' os quadros a-b (QA por trecho)
    _a, _b = map(int, sys.argv[sys.argv.index('--range') + 1].split('-')); fs = [f for f in fs if _a <= int(f[1:5]) <= _b]
REPORT = sys.argv[sys.argv.index('--report') + 1] if '--report' in sys.argv else 'qa_report.json'
n = len(fs)
cuts = set()
try:
    m = re.search(r'const CUTS = \[([^\]]*)\]', open(story).read())
    cuts = {int(x) for x in re.findall(r'\d+', m.group(1))} if m else set()
except Exception: pass
def load(i):
    im = Image.open(os.path.join(D, fs[i])).convert('RGB').resize((135, 240)); return np.asarray(im, np.float32)
prev = None; L = []; S = []; B = []; DP = []; cur = load(0); mean_rgb = []; BAND = []
frames = []
for i in range(n):
    a = cur; nxt = load(i + 1) if i + 1 < n else None
    g = a.mean(2); L.append(g.mean()); S.append(g.std())
    lap = np.abs(4 * g[1:-1, 1:-1] - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:]).mean(); B.append(lap)
    mean_rgb.append(a.reshape(-1, 3).mean(0))
    _dk = (a.max(2) < 72).mean(1); _sd = a.mean(2).std(1); BAND.append(int((((_dk > 0.85) & (_sd < 14))[20:190]).sum()))   # rows that are one uniform near-black strip (ink on grazing ground / camera under the floor); dusk shadow stripes vary along the row, so they do not count
    DP.append(0 if prev is None else np.abs(a - prev).mean())
    prev = a; cur = nxt if nxt is not None else a
DP = np.array(DP); DN = np.append(DP[1:], 0); med = np.median(DP[DP > 0]) if (DP > 0).any() else 1.0
flag = {}
def add(i, r): flag.setdefault(i, []).append(r)
for i in range(n):
    f = int(fs[i][1:5])
    if L[i] < 14: add(i, 'black')
    if L[i] > 238: add(i, 'white')
    if S[i] < 9 and L[i] > 14: add(i, 'flat (almost no detail)')
    if B[i] < 0.5 and S[i] < 20: add(i, 'blurry/empty')
    if BAND[i] >= 2 and L[i] > 80: add(i, 'dark horizon band (%d rows)' % BAND[i])
    near_cut = any(abs(f - c) <= 4 for c in cuts)
    if not near_cut and 0 < i < n - 1:
        if DP[i] > 6 * med + 2 and DN[i] > 6 * med + 2 and np.abs(DP[i] - DN[i]) < 0.6 * max(DP[i], DN[i]): add(i, 'isolated glitch (differs from both neighbours)')
        if abs(L[i] - 0.5 * (L[i - 1] + L[i + 1])) > 28: add(i, 'exposure flicker')
        dc = np.abs(mean_rgb[i] - 0.5 * (mean_rgb[i - 1] + mean_rgb[i + 1])).max()
        if dc > 22: add(i, 'colour flicker')
rep = {'total': n, 'median_diff': float(med), 'frames': [{'f': int(fs[i][1:5]), 'reasons': r} for i, r in sorted(flag.items())]}
json.dump(rep, open(REPORT, 'w'), indent=1)
print(f"{n} frames checked, {len(flag)} flagged"); [print(' ', e['f'], '; '.join(e['reasons'])) for e in rep['frames'][:60]]
if sheet and flag:
    ids = sorted(flag)[:60]; ims = [Image.open(os.path.join(D, fs[i])).resize((180, 320)) for i in ids]; cols = 12; rows = (len(ims) + cols - 1) // cols
    sh = Image.new('RGB', (180 * cols, 320 * rows)); [sh.paste(im, ((k % cols) * 180, (k // cols) * 320)) for k, im in enumerate(ims)]; sh.save(sheet, quality=85)
if '--rerender' in sys.argv:
    for e in rep['frames']: os.remove(os.path.join(D, 'f%04d.jpg' % e['f']))
    print('deleted', len(rep['frames']), 'flagged frames; re-run render.mjs with RESUME=1 to redo only those')
