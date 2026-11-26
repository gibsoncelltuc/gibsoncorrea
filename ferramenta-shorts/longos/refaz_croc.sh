#!/usr/bin/env bash
# re-renderiza os trechos 5400-12600 do crocodilo (modelos corrigidos) em paralelo com a fila, re-encoda os 4 trechos e remonta o mp4
F=/home/user/gibsoncorrea/ferramenta-shorts/fossil/v1; cd /home/user/gibsoncorrea/ferramenta-shorts/longos
WWW=www_croc PAGINA=fossil.html node render_longo.mjs $F/frames 5400 12599 3
for s in 5400 7200 9000 10800; do
  ffmpeg -v error -y -framerate 30 -start_number $s -i $F/frames/f%05d.jpg -frames:v 1800 -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p $F/segs/s$(printf %05d $s).mp4 && for ((f=s; f<s+1800; f++)); do rm -f $F/frames/$(printf f%05d.jpg $f); done
done
ls $F/segs/*.mp4 | sed "s#^#file #" > $F/segs.txt
ffmpeg -v error -y -f concat -safe 0 -i $F/segs.txt -i $F/audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $F/v1_croc.mp4 && echo CROC_OK
