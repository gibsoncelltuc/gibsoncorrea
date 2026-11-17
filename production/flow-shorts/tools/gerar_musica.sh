#!/usr/bin/env bash
# Gera N versões da música de um episódio com ACE-Step (CPU). Uso: gerar_musica.sh <num_ep> <seed1> [seed2 ...]
# Requer o ACE-Step instalado em /home/user/musica (veja instalar_acestep.sh). Cada versão leva ~9 min.
set -euo pipefail
EP=$1; shift
HERE="$(cd "$(dirname "$0")" && pwd)"
ACE=/home/user/musica/acestep.cpp
for s in "$@"; do
  D=/home/user/musica/ep$(printf %02d $EP)/s$s; mkdir -p $D; cd $D
  python3 "$HERE/musica_pedido.py" $EP $s req.json > /dev/null
  T=$(date +%s)
  $ACE/build/ace-lm --models $ACE/models --request req.json > lm.log 2>&1
  $ACE/build/ace-synth --models $ACE/models --request req0.json > synth.log 2>&1
  echo "seed $s pronto em $(( $(date +%s)-T ))s: $D/req00.mp3" >> /home/user/musica/ep$(printf %02d $EP)/status.log
done
echo ALL_DONE >> /home/user/musica/ep$(printf %02d $EP)/status.log
