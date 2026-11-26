#!/usr/bin/env bash
# espera a fila dos longos acabar e refaz so' os quadros do bloco 1 (intro) do v1
cd "$(dirname "$0")"
while pgrep -f fila_longos.sh >/dev/null; do sleep 30; done
dur(){ ffprobe -v error -show_entries format=duration -of csv=p=0 "$1"; }
read f0 f1 < <(python3 -c "a=$(dur v1/voz/b00.mp3)+1.4; b=a+$(dur v1/voz/b01.mp3)+1.4; print(int(a*30), int(b*30))")
for ((f=f0; f<=f1; f++)); do rm -f v1/frames/$(printf f%05d.jpg $f); done
python3 fazer_longo.py v1_fundo_mar.json v1 > v1/render2.log 2>&1; echo "v1 intro refeito: $(tail -1 v1/render2.log)"
