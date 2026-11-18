#!/usr/bin/env bash
# Gera a música (semente 23) dos episódios 11 a 30, em ordem, pulando os que já existem. Retomável: pode rodar de novo depois de um reinício.
# Cada música leva ~9-12 min em CPU. Saída: /home/user/musica/epNN/s23/req00.mp3 ; log em /home/user/musica/todas.log
HERE="$(cd "$(dirname "$0")" && pwd)"
ACE=/home/user/musica/acestep.cpp
SEED=${SEED:-23}
for EP in $(seq ${1:-11} ${2:-30}); do
  N=$(printf %02d $EP); D=/home/user/musica/ep$N/s$SEED
  [ -f "$D/req00.mp3" ] && continue
  [ -f "$HERE/../musica/ep${N}_acestep_seed${SEED}.mp3" ] && continue
  rm -rf "$D"; mkdir -p "$D"; cd "$D"
  python3 "$HERE/musica_pedido.py" $EP $SEED req.json > /dev/null
  T=$(date +%s)
  nice -n 10 $ACE/build/ace-lm --models $ACE/models --request req.json > lm.log 2>&1
  nice -n 10 $ACE/build/ace-synth --models $ACE/models --request req0.json > synth.log 2>&1
  if [ -f req00.mp3 ]; then
    cp req00.mp3 "$HERE/../musica/ep${N}_acestep_seed${SEED}.mp3"; cp req.json "$HERE/../musica/ep${N}_pedido_seed${SEED}.json"
    echo "ep$N pronto em $(( $(date +%s)-T ))s" >> /home/user/musica/todas.log
  else echo "ep$N FALHOU" >> /home/user/musica/todas.log; fi
done

