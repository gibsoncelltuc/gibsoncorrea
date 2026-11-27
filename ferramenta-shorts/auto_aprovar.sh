#!/usr/bin/env bash
# AUTO-APROVACAO DE SEGURANCA (ordem do Gibson 19/11, para quando a cota do modelo acabar e ninguem olha o storyboard).
# Loop (roda em segundo plano, sem token): a cada 2 min, para cada stories/<id>/AGUARDA_STORYBOARD parado ha mais de ESPERA_MIN (5) min
# e que passe nas verificacoes AUTOMATICAS (folha 2 com 0 risco, verificar_execucao 100% acoes e cenario), aprova sozinho (aprovar_rapido.sh)
# e marca stories/<id>/AUTO_APROVADO (o modelo REVE o video quando a cota voltar: conferir.sh + auditar_acoes.sh). Nunca aprova curie1898 nem ese_* (pausados).
cd "$(dirname "$0")"; ESPERA_MIN=${ESPERA_MIN:-5}
[ -f "$(dirname "$0")/PAUSA" ] || [ -f PAUSA ] && { echo "$(date +%T) PAUSA ativa: nao rodo (apague ferramenta-shorts/PAUSA)"; exit 0; }
while true; do
  for f in stories/*/AGUARDA_STORYBOARD; do
    [ -e "$f" ] || continue; id=$(basename "$(dirname "$f")")
    case "$id" in curie1898|ese_*|z*|teste*) continue;; esac
    [ -f stories/$id/STORYBOARD_OK ] && continue
    idade=$(( ( $(date +%s) - $(stat -c %Y stories/$id/storyboard.jpg 2>/dev/null || date +%s) ) / 60 ))
    [ "$idade" -ge "$ESPERA_MIN" ] || continue
    python3 mkvideo.py $id >/dev/null 2>&1 || continue
    R=$(sed -n '/## RESUMO/,$p' stories/$id/folha2_producao.md | head -1)
    case "$R" in *" 0 risco"*) ;; *) echo "$(date +%T) $id: NAO auto-aprova (riscos: $R)" >> logs/auto_aprovar.log; continue;; esac
    V=$(python3 verificar_execucao.py $id 2>/dev/null | head -1)
    echo "$V" | grep -q '<-' && { echo "$(date +%T) $id: NAO auto-aprova (execucao: $V)" >> logs/auto_aprovar.log; continue; }
    ./aprovar_rapido.sh $id 2>&1 | tail -1 | grep -q APROVADO && { touch stories/$id/AUTO_APROVADO; echo "$(date +%T) $id: AUTO-APROVADO (sem olho humano, ${idade} min parado)" >> logs/auto_aprovar.log; }
  done
  sleep 120
done
