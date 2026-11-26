#!/usr/bin/env bash
# espera a fila dos documentarios e refaz os 5 shorts de geografia (trilha nova + titulo de gancho)
while ! grep -q FILA_FIM /home/user/gibsoncorrea/ferramenta-shorts/longos/depois_croc.log 2>/dev/null; do sleep 60; done
cd /home/user/gibsoncorrea/ferramenta-shorts/geo
for v in geo1_missing geo2_renamed geo3_neighbor geo4_extreme geo5_borders; do rm -rf out/$v/frames out/$v/$v.mp4; python3 geo.py $v 2>&1 | grep -E "pronto|Error|Trace"; python3 thumb.py $v 2>&1 | tail -1; rm -rf out/$v/frames; done
echo GEO_FIM
