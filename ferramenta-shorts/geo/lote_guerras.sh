#!/usr/bin/env bash
cd /home/user/gibsoncorrea/ferramenta-shorts/geo
for v in war2_pearl war3_doolittle war4_coralsea; do
  SSL_CERT_FILE=/root/.ccr/ca-bundle.crt python3 voz.py $v >> out/lote.log 2>&1
  rm -rf out/$v/frames; python3 guerra.py $v 2>&1 | grep -E "pronto|Error|Trace" >> out/lote.log
  cp out/$v/$v.mp4 /home/user/gibsoncorrea/videos_prontos/guerras_usa/ 2>/dev/null; rm -rf out/$v/frames
done
echo LOTE_FIM >> out/lote.log
