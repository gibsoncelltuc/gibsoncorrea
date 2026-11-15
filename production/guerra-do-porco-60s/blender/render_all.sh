#!/bin/bash
# Render do piloto (Blender Cycles CPU) — passada 1: quadros pares (15 fps efetivos); passada 2: quadros ímpares (30 fps completos). Retomável (pula frames existentes).
# Uso: ./render_all.sh <W> <H> <samples> <grass> [every=2] [offset=0]
cd "$(dirname "$0")"
W=${1:-540}; H=${2:-960}; S=${3:-12}; G=${4:-50000}; EV=${5:-2}; OFF=${6:-0}
for s in $(python3 -c "import sys; sys.path.insert(0,'.'); from lib import anim; print(' '.join(e[0] for e in anim.EDL))" 2>/dev/null); do
  OFFSET=$OFF python3 render_shot.py $s $W $H $S out/frames/$s $EV $G > out/log_${s}_o${OFF}.txt 2>&1
done
echo done > out/pass_o${OFF}.done
