#!/usr/bin/env bash
# Gera as 10 canções originais (60 s). Retomável: pula as que já têm mp3 em ../musicas-virais/.
# Uso: gerar_virais.sh [seed]   (padrão 23). Cada uma leva ~9-12 min em CPU.
HERE="$(cd "$(dirname "$0")" && pwd)"; ACE=/home/user/musica/acestep.cpp; SEED=${1:-23}
OUT="$HERE/../musicas-virais"; mkdir -p "$OUT"
for N in 1 2 3 4 5 6 7 8 9 10; do
  SLUG=$(python3 -c "import sys;sys.path.insert(0,'$HERE');import musicas_virais as m;print(m.SONGS[$N]['slug'])")
  F="$OUT/$(printf %02d $N)-$SLUG.mp3"; [ -f "$F" ] && continue
  D=/home/user/musica/virais/$(printf %02d $N)_s$SEED; rm -rf "$D"; mkdir -p "$D"; cd "$D"
  python3 "$HERE/musicas_virais.py" $N $SEED req.json
  T=$(date +%s)
  $ACE/build/ace-lm --models $ACE/models --request req.json > lm.log 2>&1
  $ACE/build/ace-synth --models $ACE/models --request req0.json > synth.log 2>&1
  if [ -f req00.mp3 ]; then cp req00.mp3 "$F"; cp req.json "$OUT/$(printf %02d $N)-$SLUG.json"; echo "$N pronto em $(( $(date +%s)-T ))s" >> /home/user/musica/virais.log
  else echo "$N FALHOU" >> /home/user/musica/virais.log; fi
done
echo FIM >> /home/user/musica/virais.log
