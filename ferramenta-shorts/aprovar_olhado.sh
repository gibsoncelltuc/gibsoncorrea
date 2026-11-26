#!/bin/bash
# Aprova o storyboard que a principal OLHOU: $1 = id, $2 = arquivo com "bN: OK - ..." + pesquisa: + defeitos procurados:
# Refaz as folhas se a ferramenta mudou depois (o spec tem que ficar igual ao do storyboard olhado).
ID=$1; cd "$(dirname "$0")"
cp "$2" stories/$ID/revisao_storyboard.md
out=$(./aprovar_storyboard.sh $ID 2>&1)
if echo "$out" | grep -q "DESATUALIZADA"; then cp stories/$ID/spec.js /tmp/ap_$ID.js; python3 mkvideo.py $ID >/dev/null 2>&1; python3 ficha_nas_folhas.py $ID >/dev/null 2>&1
  if ! cmp -s /tmp/ap_$ID.js stories/$ID/spec.js; then echo "SPEC MUDOU: storyboard precisa ser refeito"; rm -f stories/$ID/{storyboard.jpg,AGUARDA_STORYBOARD,visibilidade.json}; exit 1; fi
  touch stories/$ID/revisao_storyboard.md; out=$(./aprovar_storyboard.sh $ID 2>&1); fi
echo "$out" | tail -2
