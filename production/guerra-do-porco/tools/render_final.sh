#!/usr/bin/env bash
# Render final em chunks de 300 frames, com retomada (pula chunks prontos). Uso: tools/render_final.sh
cd "$(dirname "$0")/.."
TOTAL=$(python3 -c "import json,math;print(math.ceil(json.load(open('script/word-timings.json'))['total']*30))")
STEP=300; i=0
for ((s=0; s<TOTAL; s+=STEP)); do
  e=$((s+STEP-1)); [ $e -ge $TOTAL ] && e=$((TOTAL-1))
  f=$(printf "out/chunks/c%02d.mp4" $i)
  if [ ! -s "$f" ]; then
    echo "chunk $i frames $s-$e"
    npx remotion render src/index.tsx Tome "$f.part.mp4" --frames=$s-$e --crf=18 --pixel-format=yuv420p >> out/final.log 2>&1 && mv "$f.part.mp4" "$f"
  fi
  i=$((i+1))
done
echo ALLDONE > out/final.done
