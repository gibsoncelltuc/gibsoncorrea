#!/usr/bin/env bash
# usage: ./assemble.sh <id> "<Title-With-Dashes>"  -> out/<id>/<Title>.mp4
# Junta os trechos ckpt/<id>/seg_*.mp4 (ja' com legenda, SEM re-codificar) + audio normalizado (loudnorm). So' copia/mux: segundos.
set -e; cd "$(dirname "$0")"; ID="$1"; T="$2"; W=stories/$ID/work; C=ckpt/$ID
( cd stories/$ID && python3 ../../caps.py >/dev/null )
ffmpeg -v error -y -i $W/mix_raw.wav -af loudnorm=I=-14:TP=-1.5:LRA=9 -ar 48000 $W/mix.wav
ls $C/seg_*.mp4 | sed "s#^#file '$PWD/#; s#\$#'#" > $C/list.txt
ffmpeg -v error -y -f concat -safe 0 -i $C/list.txt -i $W/mix.wav -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart -f mp4 "out/$ID/$T.mp4.part" && mv "out/$ID/$T.mp4.part" "out/$ID/$T.mp4"
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "out/$ID/$T.mp4"
