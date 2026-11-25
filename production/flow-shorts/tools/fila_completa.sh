#!/usr/bin/env bash
# Fila completa de músicas (semente 23), retomável: pula o que já existe. Ordem: 5-10, 3, 11-30, 31-51.
# Para retomar depois de um reinício do ambiente: rode este arquivo de novo (setsid nohup ./fila_completa.sh &).
HERE="$(cd "$(dirname "$0")" && pwd)"
for R in "5 10" "3 3" "11 30" "31 51"; do "$HERE/gerar_todas_musicas.sh" $R; done
echo FIM-COMPLETO >> /home/user/musica/todas.log
