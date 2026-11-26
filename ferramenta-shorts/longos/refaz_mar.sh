#!/usr/bin/env bash
cd /home/user/gibsoncorrea/ferramenta-shorts/longos; D=$PWD/v1
rm -rf $D/frames $D/segs $D/*_teste.mp4
python3 fazer_longo.py v1_fundo_mar.json v1 0 0.04 > /dev/null 2>&1; rm -rf $D/frames $D/*_teste.mp4
N=$(python3 -c "import json;print(int(json.load(open('www/spec.json'))['blocos'][-1]['b']*30))")
../fossil/compacta.sh $D $N > $D/compacta.log 2>&1 &
node render_longo.mjs $D/frames 0 $((N-1)) 4 > $D/render.log 2>&1
wait
ls $D/segs/*.mp4 | sed "s#^#file #" > $D/segs.txt
ffmpeg -v error -y -f concat -safe 0 -i $D/segs.txt -i $D/audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $D/v1_fundo_mar.mp4 && echo "MAR_OK $(ffprobe -v error -show_entries format=duration -of csv=p=0 $D/v1_fundo_mar.mp4)"
