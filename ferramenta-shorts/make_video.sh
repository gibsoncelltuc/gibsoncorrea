#!/usr/bin/env bash
# usage: ./make_video.sh <id>   (videos/<id>/beats.json) -> out/<id>/<Titulo>.mp4
# Tudo automatico e RETOMAVEL: cada etapa grava um selo em stories/<id>/stages/ (apague o selo para refazer so' aquela etapa; apague stories/<id>/DONE para refazer tudo).
# Apos cada etapa o progresso e' salvo no git (ckpt.sh). O render e' feito em trechos de 150 quadros (render_pool.mjs) que tambem sao pontos de retomada.
# Codigos de saida: 0 pronto | 1 erro/gate reprovou | 75 pausado pela trava de seguranca (relance para continuar de onde parou)
set -e; cd "$(dirname "$0")"; ID="$1"; mkdir -p logs out/$ID stories/$ID/stages; L=logs/make_$ID.log
[ -f stories/$ID/DONE ] && { echo "$ID ja pronto"; exit 0; }
log() { echo "$(date +%T) $*" | tee -a $L; }
st() { [ -f stories/$ID/stages/$1 ]; }; mark() { date +%s > stories/$ID/stages/$1; bash ckpt.sh $ID "etapa $1" >/dev/null 2>&1 || true; }
j() { python3 -c "import json;print(json.load(open('stories/$ID/meta.json'))['$1'])"; }
python3 mkvideo.py $ID >> $L 2>&1
VOICE=$(j voice); RATE=$(j rate); T=$(j file)
if st voice && [ -f stories/$ID/voice.mp3 ] && [ ! -f stories/$ID/work/phrases.json ]; then log "refazendo so a temporizacao (work/ ausente)"; (cd stories/$ID && python3 ../../timing.py voice.mp3 script.txt --out work >> ../../$L 2>&1); fi
if ! st voice || [ ! -f stories/$ID/voice.mp3 ]; then log "voz"; rm -f stories/$ID/voice.mp3; ./produce_voice.sh $ID "$VOICE" "$RATE" >> $L 2>&1; mark voice; fi
if [ -f stories/$ID/VOICE_PLACEHOLDER ] && [ "${ALLOW_TEST_VOICE:-0}" != "1" ]; then log "PARADO: voz de TESTE (espeak, robotica). NAO se entrega video assim. Conserte a rede/certificado do edge-tts (veja OPERACAO.md) e apague stories/$ID/stages/voice e stories/$ID/voice.mp3"; rm -f stories/$ID/stages/voice; exit 3; fi
if ! st style; then log "estilo (autoajuste)"; python3 autostyle.py $ID >> $L 2>&1 || log "AVISO: estilo nao convergiu"; mark style; fi
if ! st fit; then log "enquadramento"; ./fit.sh $ID >> $L 2>&1; mark fit; fi
if ! st gate; then
  ./gate_all.sh $ID; G=logs/gate_$ID.txt
  if ! { grep -q "camera OK" $G && grep -q "ALL TAKES OK" $G && grep -q "STYLE OK" $G; }; then log "GATE FALHOU (veja $G)"; cat $G >> $L; exit 1; fi
  mark gate
fi
./build3.sh $ID >/dev/null 2>&1; N=$(python3 -c "import json;print(json.load(open('stories/$ID/work/phrases.json'))['frames30'])")
./snap.sh $ID $N >> $L 2>&1; (cd stories/$ID && python3 ../../caps.py >/dev/null)
log "render $N quadros (trechos de 150, retomavel)"
set +e; node render_pool.mjs $ID $N >> $L 2>&1; RC=$?; set -e; tail -3 $L
[ $RC -eq 75 ] && { log "PAUSADO pela trava de seguranca; relance run_queue.sh para continuar"; exit 75; }
[ $RC -ne 0 ] && { log "render incompleto (codigo $RC)"; exit 1; }
./assemble.sh $ID "$T" >> $L 2>&1; ./review_video.sh out/$ID/$T.mp4 out/$ID/review | tee -a $L
touch stories/$ID/DONE; bash ckpt.sh $ID "pronto" >/dev/null 2>&1 || true; log "PRONTO out/$ID/$T.mp4 (+ out/$ID/review_sheet.jpg)"
