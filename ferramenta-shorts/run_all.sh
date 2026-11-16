#!/usr/bin/env bash
# roda TODOS os videos de videos/*/beats.json em sequencia (retomavel: se o ambiente reiniciar, rode de novo)
cd "$(dirname "$0")"; for d in videos/*/; do id=$(basename $d); [ "${id:0:1}" = "_" ] && continue; [ -f $d/beats.json ] || continue
  ./make_video.sh $id || echo "$(date +%T) FALHOU $id" >> logs/run_all.log; done; echo "$(date +%T) FIM" >> logs/run_all.log
