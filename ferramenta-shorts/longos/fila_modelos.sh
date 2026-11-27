#!/usr/bin/env bash
cd /home/user/gibsoncorrea/ferramenta-shorts/longos
./refaz_mar.sh
cp /home/user/gibsoncorrea/ferramenta-shorts/longos/v1/v1_fundo_mar.mp4 "/home/user/gibsoncorrea/videos_prontos/longos_16x9/As Criaturas do Fundo do Mar que NAO Deveriam Existir.mp4" && rm -rf v1/segs
./refaz_croc4.sh
cp /home/user/gibsoncorrea/ferramenta-shorts/fossil/v1/v1_croc.mp4 "/home/user/gibsoncorrea/videos_prontos/longos_16x9/Could a Saltwater Crocodile Survive Every Prehistoric Era.mp4" && rm -rf /home/user/gibsoncorrea/ferramenta-shorts/fossil/v1/segs
echo FILA_MODELOS_FIM
