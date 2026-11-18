#!/usr/bin/env bash
# usage: ./novo_video.sh <id>   -> PORTAO DE ENTRADA da fabrica. Gera as duas folhas, confere os riscos e so' poe na fila se estiver tudo zerado.
# Passos: escreva videos/<id>/beats.json -> ./novo_video.sh <id> -> leia stories/<id>/folha2_producao.md -> corrija o beats.json -> repita ate "LIBERADO".
cd "$(dirname "$0")"; ID="${1:?uso: ./novo_video.sh <id>}"
[ -f videos/$ID/beats.json ] || { echo "ERRO: falta videos/$ID/beats.json"; exit 1; }
python3 -c "import json,sys; json.load(open('videos/$ID/beats.json'))" || { echo "ERRO: beats.json com JSON invalido (virgula ou aspas)"; exit 1; }
mkdir -p stories/$ID logs
python3 mkvideo.py $ID > logs/mkvideo_$ID.log 2>&1 || { echo "ERRO no mkvideo (roteiro com campo errado):"; tail -5 logs/mkvideo_$ID.log; exit 1; }
node --check stories/$ID/spec.js || { echo "ERRO: spec.js invalido - nao e' culpa do roteiro, avise no relatorio"; exit 1; }
grep -E "^(DUAS FOLHAS|mistura|plano de acao|pre-producao)" logs/mkvideo_$ID.log
N=$(cat stories/$ID/riscos.txt 2>/dev/null || echo 99)
if [ "$N" != "0" ]; then echo; echo "BLOQUEADO: $N risco(s). Leia stories/$ID/folha2_producao.md (secao RESUMO), corrija videos/$ID/beats.json e rode de novo."; sed -n '/^## RESUMO/,/^## Reparos/p' stories/$ID/folha2_producao.md | head -20; exit 2; fi
grep -q "AVISO" logs/mkvideo_$ID.log && echo "(ha AVISO de mistura de planos acima: corrija se der, nao bloqueia)"
if [ -f stories/$ID/DONE ]; then echo "ja existe video pronto deste id: para refazer inteiro use ./refazer_tudo.sh $ID"; exit 0; fi
grep -qx "$ID" queue.txt || echo "$ID" >> queue.txt
pgrep -f run_queue.sh >/dev/null || { nohup bash run_queue.sh > logs/queue_run.log 2>&1 & sleep 1; }
echo "LIBERADO: $ID esta na fila. Acompanhe com  bash status.sh  e, no fim,  ./conferir.sh $ID"
