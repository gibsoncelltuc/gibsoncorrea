#!/usr/bin/env bash
# PRE-CHECAGEM ANTES DO RENDER (pega 80% dos defeitos sem gastar render). Pode rodar COM A FILA RODANDO: trabalha numa copia em /tmp.
# usage: ./prechecar.sh <id>            -> stories/<id>/precheck.jpg (1 quadro a cada ~1,5 s, todas as cenas)
#        ./prechecar.sh <id> b4 6       -> stories/<id>/precheck_b4.jpg (6 quadros da cena b4, para ver o MOVIMENTO)
# Depois: ABRA a imagem (Read) e procure: objeto heroi visivel e em close, ninguem/nada cortado, sem clones, cenario certo,
# animal citado em cena, nada gigante tapando a tela, noite/neve so onde o roteiro pede. Corrija o beats.json e rode de novo.
set -e; cd "$(dirname "$0")"; F=$(pwd); ID="${1:?id}"; SC="$2"; N="${3:-6}"
[ -f videos/$ID/beats.json ] || { echo "sem videos/$ID/beats.json"; exit 1; }
python3 mkvideo.py $ID | tail -1
mkdir -p stories/$ID/stages
if [ ! -f stories/$ID/voice.mp3 ] || [ ! -f stories/$ID/work/phrases.json ]; then   # voz adiantada (a fila reaproveita: mesma etapa, mesmo selo)
  V=$(python3 -c "import json;print(json.load(open('stories/$ID/meta.json'))['voice'])"); R=$(python3 -c "import json;print(json.load(open('stories/$ID/meta.json'))['rate'])")
  ./produce_voice.sh $ID "$V" "$R" > /dev/null 2>&1 || { echo "voz falhou"; exit 3; }
  [ -f stories/$ID/VOICE_PLACEHOLDER ] && { echo "voz de TESTE (espeak): rede/certificado do edge-tts. Nao siga."; exit 3; }
  date +%s > stories/$ID/stages/voice
fi
W=/tmp/prechk_$$; rm -rf $W; mkdir -p $W/web
cp *.sh *.mjs *.py $W/ 2>/dev/null || true
for f in web/*; do b=$(basename $f); [ -L $f ] && continue; [ -f $f ] && cp $f $W/web/; done
for d in node_modules out stories videos; do ln -s $F/$d $W/$d; done
for d in assets lib sets; do [ -e $W/web/$d ] && continue; ln -s $F/web/$d $W/web/$d; done
cd $W
bash build3.sh $ID > /dev/null 2>&1
if [ -n "$SC" ]; then node strip.mjs $ID $SC $N $F/stories/$ID/precheck_$SC.jpg | tail -1; echo "-> stories/$ID/precheck_$SC.jpg"
else
  rm -rf sb_tmp; node storyboard.mjs $ID x.jpg 300 > /dev/null 2>&1 || true
  n=$(ls sb_tmp 2>/dev/null | wc -l); [ "$n" -gt 0 ] || { echo "storyboard vazio"; cd $F; rm -rf $W; exit 4; }
  ffmpeg -v error -y -pattern_type glob -i "sb_tmp/${ID}_*.jpg" -vf "tile=8x$(( (n + 7) / 8 ))" -q:v 4 $F/stories/$ID/precheck.jpg
  echo "-> stories/$ID/precheck.jpg ($n quadros). ABRA e olhe."
fi
cd $F; rm -rf $W
