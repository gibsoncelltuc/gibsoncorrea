#!/usr/bin/env bash
# REFAZ SO' ALGUMAS CENAS de um video ja renderizado (2-5 min em vez de 20):  ./refazer.sh <id> b4 b8
#  - edite a cena no videos/<id>/beats.json (camera, personagens, objetos, batalha, texto na imagem...) e rode.
#  - so' vale se a NARRACAO nao mudou (mesmo texto = mesmos tempos). Se mudou o texto falado, o video inteiro precisa ser refeito (run_queue.sh).
#  - nunca rode com a fila rodando.
set -e; cd "$(dirname "$0")"; ID="$1"; shift; [ -z "$ID" ] || [ $# -eq 0 ] && { echo "uso: ./refazer.sh <id> b3 b4 ..."; exit 2; }
pgrep -f run_queue.sh >/dev/null && { echo "a fila esta rodando; espere terminar"; exit 2; }
ls ckpt/$ID/seg_*.mp4 >/dev/null 2>&1 || { echo "$ID ainda nao tem render completo; use a fila"; exit 2; }
L=logs/make_$ID.log; export CKPT_GIT=0
H0=$(md5sum stories/$ID/script.txt 2>/dev/null | cut -d' ' -f1); python3 mkvideo.py $ID >> $L 2>&1; H1=$(md5sum stories/$ID/script.txt | cut -d' ' -f1)
[ "$H0" != "$H1" ] && { echo "a narracao mudou: refaca o video inteiro (ponha $ID no queue.txt, apague stories/$ID/DONE e stages)"; exit 3; }
./build3.sh $ID >/dev/null 2>&1
[ "${FIT:-1}" = 1 ] && ./fit.sh $ID >> $L 2>&1 && ./build3.sh $ID >/dev/null 2>&1
N=$(python3 -c "import json;print(json.load(open('stories/$ID/work/phrases.json'))['frames30'])")
SEGS=$(node -e "
import('$PWD/web/story.js').then(m=>{const want=process.argv.slice(1);const S=m.SHOTS.filter(s=>want.includes(s.id.split('~')[0]));const k=new Set();for(const s of S)for(let f=Math.max(0,s.a-10);f<=Math.min($N-1,s.b+10);f++)k.add(Math.floor(f/150));console.log([...k].sort((a,b)=>a-b).join(' '))})" "$@")
[ -z "$SEGS" ] && { echo "cenas nao encontradas: $*"; exit 2; }
echo "trechos a refazer: $SEGS"; for k in $SEGS; do rm -f ckpt/$ID/seg_$(printf %03d $k).mp4; for f in $(seq $((k*150)) $((k*150+149))); do rm -f out/$ID/frames/f$(printf %04d $f).jpg; done; done   # apaga tambem os quadros antigos desses trechos (senao seriam reaproveitados)
rm -f stories/$ID/DONE; ./snap.sh $ID $N >> $L 2>&1; (cd stories/$ID && python3 ../../caps.py >/dev/null)
node render_pool.mjs $ID $N >> $L 2>&1
T=$(python3 -c "import json;print(json.load(open('stories/$ID/meta.json'))['file'])")
./assemble.sh $ID "$T" >> $L 2>&1; ./review_video.sh out/$ID/$T.mp4 out/$ID/review | tail -2
touch stories/$ID/DONE; echo "PRONTO out/$ID/$T.mp4 (cenas refeitas: $*)"
