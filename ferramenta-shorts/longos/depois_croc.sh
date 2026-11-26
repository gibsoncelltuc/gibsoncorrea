#!/usr/bin/env bash
# espera o render do crocodilo, monta o mp4 (trechos + audio) e depois refaz os 4 documentarios (fila)
F=/home/user/gibsoncorrea/ferramenta-shorts/fossil/v1
while pgrep -f "render_longo.mjs" >/dev/null; do sleep 30; done
while ! grep -q FIM $F/compacta.log; do sleep 30; done
ls $F/segs/*.mp4 | sed "s#^#file #" > $F/segs.txt
ffmpeg -v error -y -f concat -safe 0 -i $F/segs.txt -i $F/audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $F/v1_croc.mp4 && echo "croc pronto $(ffprobe -v error -show_entries format=duration -of csv=p=0 $F/v1_croc.mp4)"
cd /home/user/gibsoncorrea/ferramenta-shorts/longos && bash fila_longos.sh
echo FILA_FIM
