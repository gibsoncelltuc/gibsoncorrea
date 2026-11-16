#!/usr/bin/env bash
# status.sh -- mostra onde a producao esta (fila, etapas, trechos, ultimas linhas do log)
cd "$(dirname "$0")"
echo "fila:"; grep -v '^#' queue.txt | sed '/^$/d' | while read -r id _; do
  if [ -f stories/$id/DONE ]; then echo "  [PRONTO] $id"; else
    S=$(ls stories/$id/stages 2>/dev/null | tr '\n' ' '); NS=$(ls ckpt/$id/seg_*.mp4 2>/dev/null | wc -l); NF=$(ls out/$id/frames/f*.jpg 2>/dev/null | wc -l)
    echo "  [em curso/pendente] $id  etapas: ${S:-nenhuma}| trechos prontos: $NS | quadros soltos: $NF"; fi; done
[ -f logs/queue.lock ] && kill -0 "$(cat logs/queue.lock)" 2>/dev/null && echo "fila RODANDO (pid $(cat logs/queue.lock))" || echo "fila PARADA (rode: bash run_queue.sh)"
for f in logs/make_*.log; do [ -f "$f" ] && { echo "--- $f"; tail -4 "$f"; }; done
