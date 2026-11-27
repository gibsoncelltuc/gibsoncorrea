#!/usr/bin/env bash
cd /home/user/gibsoncorrea/ferramenta-shorts/longos; F=/home/user/gibsoncorrea/ferramenta-shorts/fossil/v1
rm -rf $F/frames $F/segs
N=$(python3 -c "import json;print(int(json.load(open('www_croc/spec.json'))['blocos'][-1]['b']*30))")
../fossil/compacta.sh $F $N > $F/compacta.log 2>&1 &
WWW=www_croc PAGINA=fossil.html node render_longo.mjs $F/frames 0 $((N-1)) 4 > $F/render.log 2>&1
wait
ls $F/segs/*.mp4 | sed "s#^#file #" > $F/segs.txt
ffmpeg -v error -y -f concat -safe 0 -i $F/segs.txt -i $F/audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $F/v1_croc.mp4 && echo "CROC4_OK $(ffprobe -v error -show_entries format=duration -of csv=p=0 $F/v1_croc.mp4)"
