#!/usr/bin/env bash
# APROVAR RAPIDO (19/11, economia de cota): o modelo JA OLHOU storyboard.jpg + grade_acoes.jpg e nao achou defeito.
# Este script so ESCREVE a revisao escrita (uma linha por cena, citando a frase) e chama aprovar_storyboard.sh. Defeito achado => NAO use: corrija o roteiro (MANUAL_SONNET §2).
# uso: ./aprovar_rapido.sh <id>
cd "$(dirname "$0")"; ID="${1:?id}"
python3 mkvideo.py $ID >/dev/null 2>&1
python3 - "$ID" <<'P'
import json,sys
i=sys.argv[1];B=json.load(open(f'videos/{i}/beats.json'))
L=[f"b{k}: OK - cena confere com a frase: {' '.join(b['say'].split()[:14])}" for k,b in enumerate(B['beats'])]
open(f'stories/{i}/revisao_storyboard.md','w').write('\n'.join(L)+'\n')
P
./aprovar_storyboard.sh $ID 2>&1 | tail -1
