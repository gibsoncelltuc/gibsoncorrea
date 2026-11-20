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
if [ "$SC" = "acoes" ]; then   # GRADE DE ACOES (19/11): 1 quadro no INSTANTE EXATO de cada acao catalogada na folha 3, com a palavra escrita embaixo
  python3 - "$ID" > acoes_frames.txt <<'PYA'
import re, sys
rows = []
for l in open(f'stories/{sys.argv[1]}/folha3_acao.md'):
    m = re.match(r'## Cena (b\d+)', l)
    if m: cena = m.group(1)
    r = re.match(r'\| \d+ \| (.+?) \(([\d.]+)s\) \| (.+?) \|', l)
    if r: rows.append((round(float(r.group(2)) * 30) + 9, f"{cena} {r.group(1)} | {r.group(3)[:34]}"))
for f, t in rows: print(f"{f}\t{t}")
PYA
  FR=$(cut -f1 acoes_frames.txt | paste -sd,); NF=$(wc -l < acoes_frames.txt)
  FRAMES=$FR node strip.mjs $ID b0 $NF x_strip.jpg > /dev/null 2>&1
  python3 - acoes_frames.txt $F/stories/$ID/grade_acoes.jpg <<'PYB'
import sys
from PIL import Image, ImageDraw
L = [l.rstrip('\n').split('\t') for l in open(sys.argv[1])]; im = Image.open('x_strip.jpg'); n = len(L); w = im.width // max(1, n); h = im.height; C = 7
out = Image.new('RGB', (C * w, ((n + C - 1) // C) * (h + 26)), 'white'); d = ImageDraw.Draw(out)
for i, (f, t) in enumerate(L):
    x, y = (i % C) * w, (i // C) * (h + 26); out.paste(im.crop((i * w, 0, (i + 1) * w, h)), (x, y)); d.text((x + 3, y + h + 2), t[:46], fill='black'); d.text((x + 3, y + h + 13), t[46:92], fill='black')
out.save(sys.argv[2], quality=85); print(f'-> {sys.argv[2]} ({n} acoes)')
PYB
elif [ -n "$SC" ]; then node strip.mjs $ID $SC $N $F/stories/$ID/precheck_$SC.jpg | tail -1; echo "-> stories/$ID/precheck_$SC.jpg"
else
  rm -rf sb_tmp; node storyboard.mjs $ID x.jpg 300 > /dev/null 2>&1 || true
  n=$(ls sb_tmp 2>/dev/null | wc -l); [ "$n" -gt 0 ] || { echo "storyboard vazio"; cd $F; rm -rf $W; exit 4; }
  ffmpeg -v error -y -pattern_type glob -i "sb_tmp/${ID}_*.jpg" -vf "tile=8x$(( (n + 7) / 8 ))" -q:v 4 $F/stories/$ID/precheck.jpg
  echo "-> stories/$ID/precheck.jpg ($n quadros). ABRA e olhe."
fi
cd $F; rm -rf $W
