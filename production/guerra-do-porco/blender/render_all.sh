#!/bin/bash
# Render do piloto (Blender Cycles CPU) — passada 1: quadros pares (15 fps efetivos); passada 2: quadros ímpares (30 fps completos). Retomável (pula frames existentes).
# Uso: ./render_all.sh <W> <H> <samples> <grass> [every=2] [offset=0]
cd "$(dirname "$0")"
W=${1:-540}; H=${2:-960}; S=${3:-12}; G=${4:-50000}; EV=${5:-2}; OFF=${6:-0}
for s in S1 S2 S3 S4 S5 S6; do
  OFFSET=$OFF python3 render_shot.py $s $W $H $S out/frames/$s $EV $G > out/log_${s}_o${OFF}.txt 2>&1
done
echo done > out/pass_o${OFF}.done
