#!/usr/bin/env bash
F=/home/user/gibsoncorrea/ferramenta-shorts/fossil/v1; cd /home/user/gibsoncorrea/ferramenta-shorts/longos
rm -f $F/segs/s07200.mp4 $F/segs/s09000.mp4 $F/segs/s10800.mp4
../fossil/compacta.sh $F 12600 5400 > $F/compacta2.log 2>&1 &
WWW=www_croc PAGINA=fossil.html node render_longo.mjs $F/frames 5400 12599 4
wait
ls $F/segs/*.mp4 | sed "s#^#file #" > $F/segs.txt
ffmpeg -v error -y -f concat -safe 0 -i $F/segs.txt -i $F/audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $F/v1_croc.mp4 && echo "CROC_OK $(ffprobe -v error -show_entries format=duration -of csv=p=0 $F/v1_croc.mp4)"
