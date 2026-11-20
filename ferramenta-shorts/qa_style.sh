#!/usr/bin/env bash
# usage: ./qa_style.sh <id>   (after ./build3.sh <id>)  -> renders 1 mid-frame per shot and compares style metrics with the Ricks Clips reference bands
set -e; cd "$(dirname "$0")"; ID="$1"; mkdir -p tmp/qs_$ID; rm -f tmp/qs_$ID/*
FR=$(node -e "import('./web/story.js').then(m=>console.log(JSON.stringify(m.SHOTS.map(s=>({f:Math.round((s.a+s.b)/2)})))))")
node shot.mjs tmp/qs_$ID/s.jpg "$FR" >/dev/null
python3 - "$ID" <<'PY'
import sys,glob; sys.path.insert(0,'.')
from stylemetrics import summarize
id=sys.argv[1]; fs=sorted(glob.glob(f'tmp/qs_{id}/s_*.jpg')); S=summarize(fs)
BANDS={'detail':(0.229,9),'edges':(0.039,9),'dark':(0.002,0.12),'lum_mean':(0.31,0.63),'lum_std':(0.15,9),'sat':(0.32,9),'colorful':(0.17,9)}   # = Ricks Clips p10..p90 band (measured on 45 reference frames)
ok=True
for k,(lo,hi) in BANDS.items():
    m=S[k][0]; good=(lo-0.002)<=m<=hi; ok&=good; print(f'{k:9s} {m:6.3f}  target {lo}-{hi if hi<9 else "+"}  {"OK" if good else "FAIL"}')
print('STYLE OK' if ok else 'STYLE FAIL', len(fs),'frames')
PY
