#!/usr/bin/env bash
# crocodilo v3: modelos reais + trilha orquestral + voz nova. Render em trechos (disco pequeno).
cd /home/user/gibsoncorrea/ferramenta-shorts/longos; F=/home/user/gibsoncorrea/ferramenta-shorts/fossil/v1
rm -rf $F/frames $F/segs $F/*_teste.mp4
python3 fazer_longo.py ../fossil/v1_croc.json $F 0 0.04 > /dev/null 2>&1; rm -rf $F/frames $F/*_teste.mp4   # audio + spec
cp www/spec.json www_croc/spec.json
N=$(python3 -c "import json;print(int(json.load(open('www_croc/spec.json'))['blocos'][-1]['b']*30))")
../fossil/compacta.sh $F $N > $F/compacta.log 2>&1 &
WWW=www_croc PAGINA=fossil.html node render_longo.mjs $F/frames 0 $((N-1)) 4 > $F/render.log 2>&1
wait
ls $F/segs/*.mp4 | sed "s#^#file #" > $F/segs.txt
ffmpeg -v error -y -f concat -safe 0 -i $F/segs.txt -i $F/audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $F/v1_croc.mp4 && echo "CROC3_OK $(ffprobe -v error -show_entries format=duration -of csv=p=0 $F/v1_croc.mp4)"
