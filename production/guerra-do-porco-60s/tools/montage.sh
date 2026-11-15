#!/usr/bin/env bash
# Montagem final — rota Blender (3D) + Remotion (montagem/legendas/áudio) + FFmpeg (grade de cor e encode).
# Uso: tools/montage.sh [saida.mp4] [--every 2]   (--every 2: só a passada 1 do Blender, 15 fps efetivos; padrão: todos os quadros)
set -e
cd "$(dirname "$0")/.."
OUT=${1:-renders/pilot_540.mp4}; shift || true
python3 tools/make_montage_data.py "$@"                                   # planos, quadros disponíveis, legendas → montage/data.json (+ hardlinks em montage/public)
npx --no-install remotion render montage/index.ts Montage renders/_montage_raw.mp4 --public-dir=montage/public --concurrency=${CONC:-4} --log=warn
rm -rf renders/_captions && npx --no-install remotion render montage/index.ts Captions renders/_captions --sequence --image-format=png --public-dir=montage/public --concurrency=${CONC:-4} --log=warn
python3 blender/grade.py renders/_montage_raw.mp4 renders/_captions "$OUT"
