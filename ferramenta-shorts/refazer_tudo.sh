#!/usr/bin/env bash
# usage: ./refazer_tudo.sh <id>...  -> apaga TUDO que faria o render reaproveitar a versao antiga (quadros, trechos, selos, snapshot) e poe o id no fim da fila.
# Use quando a FERRAMENTA mudou (animacao, camera, objetos) e o video precisa sair inteiro de novo. Para mexer so' em cenas, use refazer.sh.
cd "$(dirname "$0")"
for ID in "$@"; do
  [ -f videos/$ID/beats.json ] || { echo "sem videos/$ID/beats.json"; continue; }
  rm -rf out/$ID/frames out/$ID/qa_seg*.json ckpt/$ID ../webs/$ID stories/$ID/DONE stories/$ID/SKIP stories/$ID/fails stories/$ID/READY stories/$ID/stages
  grep -qx "$ID" queue.txt || echo "$ID" >> queue.txt; echo "$ID: limpo e na fila"
done
pgrep -f run_queue.sh >/dev/null || echo "fila parada: rode  nohup bash run_queue.sh > logs/queue_run.log 2>&1 &"
