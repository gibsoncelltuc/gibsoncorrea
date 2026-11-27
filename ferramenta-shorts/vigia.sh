#!/usr/bin/env bash
# VIGIA DA SESSAO PRINCIPAL (24/11): roda em segundo plano e TERMINA com UMA linha quando algo pede o olho da principal.
# uso (sempre em segundo plano, e relancar depois de cada evento):  bash ferramenta-shorts/vigia.sh
# saidas:  PRONTO_PRINCIPAL <id>  -> video da fila principal renderizado: conferir.sh + revisao_final.sh + olhar frase_a_frase + entregar
#          STORYBOARD <id>        -> storyboard esperando o olho: olhar + revisao_storyboard.md + aprovar_storyboard.sh (ou corrigir)
#          SKIP <id>              -> fila pulou o video (bloqueio): ler logs/make_<id>.log e corrigir na raiz
#          FALHOU <linha>         -> render falhou: ler logs/make_<id>.log (disco cheio? roteiro?) e corrigir
#          NOVO <branch> <id> ... -> video de sessao chegou em videos_prontos/_a_conferir: frase_a_frase.sh + olhar + aprovar_entrega.sh ou devolver com lista unica
cd "$(dirname "$0")"; S=logs/vigia; mkdir -p $S
while true; do
  [ "$(df -Pm . | awk 'NR==2{print $4}')" -lt 3000 ] && bash limpar_disco.sh >> $S/limpeza.log 2>&1
  for d in stories/*/DONE; do id=$(basename $(dirname $d)); grep -q "^motor v13" $d || continue; [ -f stories/$id/ENTREGUE ] && [ ! $d -nt stories/$id/ENTREGUE ] && continue; [ -f stories/$id/VISTO_VIGIA ] && [ ! $d -nt stories/$id/VISTO_VIGIA ] && continue; { touch stories/$id/VISTO_VIGIA; echo "PRONTO_PRINCIPAL $id"; exit 0; }; done
  for id in $(grep -v '^#' queue.txt | awk 'NF{print $1}'); do
    [ -f stories/$id/AGUARDA_STORYBOARD ] && [ ! -f stories/$id/VISTO_SB ] && { touch stories/$id/VISTO_SB; echo "STORYBOARD $id"; exit 0; }
    [ -f stories/$id/SKIP ] && [ ! -f stories/$id/VISTO_SKIP ] && { touch stories/$id/VISTO_SKIP; echo "SKIP $id"; exit 0; }
  done
  FL=$(grep "falhou " logs/queue_run.log 2>/dev/null | tail -1); [ -n "$FL" ] && [ "$FL" != "$(cat $S/ultima_falha 2>/dev/null)" ] && { echo "$FL" > $S/ultima_falha; echo "FALHOU $FL"; exit 0; }
  o=$(bash receber_das_sessoes.sh 2>&1 | grep -E "^NOVO|^ERRO"); [ -n "$o" ] && { echo "$o" | tee -a $S/recebidos_novos.txt; exit 0; }
  sleep 60
done
