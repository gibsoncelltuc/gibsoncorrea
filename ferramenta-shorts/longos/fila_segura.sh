#!/usr/bin/env bash
# fila SEGURA (disco pequeno): espera o croc; depois cada documentario renderiza com compactacao de trechos; depois os 5 shorts de geografia.
cd /home/user/gibsoncorrea/ferramenta-shorts/longos
while ! grep -q CROC_OK refaz_croc2.log 2>/dev/null; do sleep 30; done
for v in v1_fundo_mar:v1 v2_descida:v2 v3_saturno:v3 v4_plutao:v4; do
  j=${v%%:*}; d=${v##*:}; [ -f $d/$j.mp4 ] && continue
  rm -rf $d/frames $d/segs; python3 fazer_longo.py $j.json $d 0 0.04 > /dev/null 2>&1; rm -rf $d/frames $d/*_teste.mp4   # gera voz/audio/spec
  N=$(python3 -c "import json;print(int(json.load(open('www/spec.json'))['blocos'][-1]['b']*30))")
  ../fossil/compacta.sh $PWD/$d $N > $d/compacta.log 2>&1 &
  node render_longo.mjs $d/frames 0 $((N-1)) 4 > $d/render.log 2>&1
  wait
  ls $PWD/$d/segs/*.mp4 | sed "s#^#file #" > $d/segs.txt
  ffmpeg -v error -y -f concat -safe 0 -i $d/segs.txt -i $d/audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $d/$j.mp4 && rm -rf $d/segs && echo "$(date +%T) $j OK $(ffprobe -v error -show_entries format=duration -of csv=p=0 $d/$j.mp4)"
done
echo DOCS_FIM
cd ../geo
for v in geo1_missing geo2_renamed geo3_neighbor geo4_extreme geo5_borders; do rm -rf out/$v/frames out/$v/$v.mp4; python3 geo.py $v 2>&1 | grep -E "pronto|Error|Trace"; python3 thumb.py $v 2>&1 | tail -1; rm -rf out/$v/frames; done
echo GEO_FIM
