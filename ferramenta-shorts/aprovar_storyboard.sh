#!/usr/bin/env bash
# APROVAR O STORYBOARD (obrigatorio antes do render, ordem do Gibson 19/11). So' rode DEPOIS de abrir e olhar stories/<id>/storyboard.jpg
# conferindo frase por frase com a folha 3 (cada acao acontecendo, ninguem cortado, cenario certo, objeto heroi visivel).
# uso: ./aprovar_storyboard.sh <id>        (a aprovacao vale para ESTA versao das folhas; mudou o roteiro/ferramenta -> novo storyboard e nova aprovacao)
cd "$(dirname "$0")"; ID="${1:?id}"
[ -f stories/$ID/storyboard.jpg ] || { echo "sem storyboard: a fila gera sozinha (ou ./prechecar.sh $ID && cp stories/$ID/precheck.jpg stories/$ID/storyboard.jpg)"; exit 1; }
python3 verificar_folhas.py $ID || exit 1
H=$(python3 -c "import json;print(json.load(open('stories/$ID/folhas.json'))['hash_folha3'])")
[ "$(cat stories/$ID/storyboard.hash 2>/dev/null)" = "$H" ] || { echo "o storyboard e' de uma versao ANTIGA das folhas: gere de novo (rm stories/$ID/storyboard.jpg e relance a fila)"; exit 1; }
echo "$H" > stories/$ID/STORYBOARD_OK; rm -f stories/$ID/AGUARDA_STORYBOARD; echo "STORYBOARD APROVADO: $ID ($H). A fila renderiza na proxima volta."
