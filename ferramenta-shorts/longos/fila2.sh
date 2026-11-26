#!/usr/bin/env bash
cd /home/user/gibsoncorrea/ferramenta-shorts/longos
while ! grep -q FILA_MODELOS_FIM fila_modelos.log; do sleep 30; done
./refaz_mar.sh && cp v1/v1_fundo_mar.mp4 "/home/user/gibsoncorrea/videos_prontos/longos_16x9/As Criaturas do Fundo do Mar que NAO Deveriam Existir.mp4" && rm -rf v1/segs
echo FILA2_FIM
