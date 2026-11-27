#!/usr/bin/env bash
cd /home/user/gibsoncorrea/ferramenta-shorts/geo
for v in war3_doolittle war4_coralsea; do rm -rf out/$v/frames; python3 guerra.py $v 2>&1 | grep -E "pronto|Error|Trace" >> out/lote2.log; cp out/$v/$v.mp4 /home/user/gibsoncorrea/videos_prontos/guerras_usa/; rm -rf out/$v/frames; done
echo LOTE2_FIM >> out/lote2.log
