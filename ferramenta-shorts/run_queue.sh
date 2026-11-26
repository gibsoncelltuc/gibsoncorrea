#!/usr/bin/env bash
# FILA RETOMAVEL + TRAVA DE SEGURANCA DE SESSAO. Le queue.txt (um id por linha, # comenta) e produz cada video em sequencia.
# Pode ser relancado a qualquer momento/apos qualquer reinicio: ids com stories/<id>/DONE sao pulados, etapas com selo sao puladas, trechos prontos nao sao refeitos.
# Trava: a sessao de nuvem reinicia ~a cada 60 min. Perto disso (SESSION_MIN - SAFETY_MIN desde o inicio do container) o render para de puxar quadros novos,
# termina os em curso, codifica os trechos completos, EMPURRA o checkpoint para o git e pausa. Se a sessao reiniciar: o hook de boot (boot.sh) relanca esta fila e ela continua.
# Se NAO reiniciar em GRACE_MIN minutos, a fila segue sozinha com novo prazo. SESSION_GUARD=0 desliga a trava.
cd "$(dirname "$0")"; mkdir -p logs
[ -f "$(dirname "$0")/PAUSA" ] || [ -f PAUSA ] && { echo "$(date +%T) PAUSA ativa: nao rodo (apague ferramenta-shorts/PAUSA)"; exit 0; }
exec 9>/tmp/run_queue.lock; flock -n 9 || { echo "$(date +%T) ja existe uma fila rodando: nao lanco outra"; exit 0; }   # uma fila so (duas juntas geram SKIP falso)
LOCK=logs/queue.lock
LP=$(cat $LOCK 2>/dev/null); if [ -n "$LP" ] && kill -0 "$LP" 2>/dev/null && tr "\0" " " < /proc/$LP/cmdline 2>/dev/null | grep -q run_queue; then echo "fila ja rodando (pid $(cat $LOCK))"; exit 0; fi
echo $$ > $LOCK; trap 'rm -f $LOCK' EXIT
SESSION_MIN=${SESSION_MIN:-60}; SAFETY_MIN=${SAFETY_MIN:-6}; GRACE_MIN=${GRACE_MIN:-3}
uptime_s() { ps -o etimes= -p 1 2>/dev/null | tr -d ' ' || echo 0; }
while true; do
  # CORRECOES PENDENTES (refazer.txt, uma por linha: "<id> b1 b4"): feitas ANTES do proximo video, so' as cenas marcadas
  while [ -s refazer.txt ] && L1=$(grep -v '^#' refazer.txt | grep -m1 .) && [ -n "$L1" ]; do
    echo "$(date +%T) >>> refazendo cenas: $L1"; FROM_QUEUE=1 bash refazer.sh $L1 9>&- >> logs/refazer_run.log 2>&1 || echo "$(date +%T) refazer falhou: $L1 (veja logs/refazer_run.log)"
    grep -vxF "$L1" refazer.txt > refazer.tmp; mv refazer.tmp refazer.txt
  done
  NEXT=""; ESPERA=0
  while read -r id _; do
    case "$id" in ""|\#*) continue;; esac
    case "$(git rev-parse --abbrev-ref HEAD 2>/dev/null)" in claude/prod-a*) grep -qx "$id" fila_sessao_A.txt || continue;; claude/prod-b*) grep -qx "$id" fila_sessao_B.txt || continue;; *) grep -qx "$id" fila_principal.txt || continue;; esac   # so' a fila DESTA sessao (nunca duplicar video de outra sessao)
    [ -f stories/$id/DONE ] && grep -q "^motor v13" stories/$id/DONE && continue   # DONE antigo (vazio, de antes da v13) NAO conta: o video e' refeito
    [ -f stories/$id/SKIP ] && continue   # reprovou 2x no gate: precisa de ajuste no roteiro/cena (veja logs/gate_<id>.txt); apague SKIP para tentar de novo
    [ -f stories/$id/AGUARDA_STORYBOARD ] && { ESPERA=1; continue; }   # storyboard pronto esperando aprovacao: a fila segue com o proximo
    NEXT=$id; break
  done < queue.txt
  [ -z "$NEXT" ] && [ "$ESPERA" = "1" ] && { echo "$(date +%T) so falta aprovar storyboard(s): ./aprovar_storyboard.sh <id>; espero 2 min"; sleep 120; continue; }
  [ -z "$NEXT" ] && { echo "$(date +%T) fila vazia: tudo pronto"; exit 0; }
  if [ "${SESSION_GUARD:-1}" != "0" ]; then
    UP=$(uptime_s); UP=${UP:-0}; LEFT=$(( SESSION_MIN*60 - UP - SAFETY_MIN*60 ))
    # container ja passou do prazo e NAO reiniciou: a estimativa estava errada -> novo ciclo inteiro (senao pausaria a cada 2 min)
    [ $LEFT -lt 120 ] && LEFT=$(( (SESSION_MIN - SAFETY_MIN)*60 ))
    export DEADLINE=$(( $(date +%s) + LEFT )); echo "$(date +%T) prazo de seguranca em $((LEFT/60)) min (container no ar ha $((UP/60)) min)"
  fi
  echo "$(date +%T) >>> $NEXT"
  bash garantir_sync.sh; [ "$(git -C .. rev-parse --abbrev-ref HEAD 2>/dev/null)" != "claude/bold-sagan-dskrsj" ] && bash sync_ferramenta.sh >> logs/sync.log 2>&1   # antes de CADA video: ferramenta na ultima versao
  bash make_video.sh "$NEXT" 9>&-; RC=$?   # 9>&-: os filhos nao herdam a trava (senao um processo orfao bloqueia a fila)
  if [ $RC -eq 76 ]; then echo "$(date +%T) $NEXT: storyboard pronto, AGUARDANDO APROVACAO (stories/$NEXT/storyboard.jpg)"; continue; fi
  if [ $RC -eq 75 ]; then
    echo "$(date +%T) PAUSA DE SEGURANCA: checkpoint salvo. Aguardando $GRACE_MIN min por reinicio; se nao reiniciar, continuo."; sleep $((GRACE_MIN*60)); continue
  fi
  if [ $RC -ne 0 ] && [ $RC -ne 75 ] && [ $RC -ne 76 ]; then N=$(( $(cat stories/$NEXT/fails 2>/dev/null || echo 0) + 1 )); echo $N > stories/$NEXT/fails; [ $N -ge 2 ] && { touch stories/$NEXT/SKIP; echo "$(date +%T) $NEXT reprovou $N vezes: PULADO (veja logs/gate_$NEXT.txt)"; continue; }; fi
  [ $RC -ne 0 ] && { echo "$(date +%T) falhou $NEXT (veja logs/make_$NEXT.log); tentando de novo em 60 s"; sleep 60; }
done
