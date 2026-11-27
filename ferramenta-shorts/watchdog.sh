#!/usr/bin/env bash
# WATCHDOG (ordem do Gibson 19/11): a cada 5 min verifica se a fila desta maquina e as sessoes A e B estao trabalhando.
# - fila local parada -> relanca sozinho (sem acordar ninguem)
# - sessao A ou B sem commit ha mais de 15 min (reiniciou/parou) -> SAI com o aviso: a sessao principal acorda, manda a sessao retomar e relanca o watchdog
# uso (sessao principal, em segundo plano): bash watchdog.sh
cd "$(dirname "$0")"; ST=logs/watchdog.state; touch $ST
[ -f "$(dirname "$0")/PAUSA" ] || [ -f PAUSA ] && { echo "$(date +%T) PAUSA ativa: nao rodo (apague ferramenta-shorts/PAUSA)"; exit 0; }
declare -A BR=([A]=claude/prod-a-karansebes [B]=claude/prod-b-emus)
while true; do
  if ! pgrep -f run_queue.sh >/dev/null && grep -qv '^#' queue.txt; then
    nohup bash run_queue.sh > logs/queue_run.log 2>&1 &
    echo "$(date +%T) watchdog: fila local estava parada -> relancada" >> logs/watchdog.log
  fi
  ALERTA=""
  (cd .. && git fetch -q --depth=1 origin ${BR[A]} ${BR[B]} 2>/dev/null)
  for s in A B; do
    t=$(cd .. && git log -1 --format=%ct origin/${BR[$s]} 2>/dev/null || echo 0); idade=$(( $(date +%s) - t ))
    ult=$(grep "^$s " $ST | tail -1 | cut -d' ' -f2); ult=${ult:-0}
    if [ $idade -gt 900 ] && [ $(( $(date +%s) - ult )) -gt 900 ]; then ALERTA="$ALERTA $s(${idade}s sem commit)"; echo "$s $(date +%s)" >> $ST; fi
  done
  if [ -n "$ALERTA" ]; then echo "$(date +%T) WATCHDOG: sessao parada:$ALERTA"; echo "$(date +%T) alerta:$ALERTA" >> logs/watchdog.log; exit 0; fi
  sleep 300
done
