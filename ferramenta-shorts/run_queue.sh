#!/usr/bin/env bash
# FILA RETOMAVEL + TRAVA DE SEGURANCA DE SESSAO. Le queue.txt (um id por linha, # comenta) e produz cada video em sequencia.
# Pode ser relancado a qualquer momento/apos qualquer reinicio: ids com stories/<id>/DONE sao pulados, etapas com selo sao puladas, trechos prontos nao sao refeitos.
# Trava: a sessao de nuvem reinicia ~a cada 60 min. Perto disso (SESSION_MIN - SAFETY_MIN desde o inicio do container) o render para de puxar quadros novos,
# termina os em curso, codifica os trechos completos, EMPURRA o checkpoint para o git e pausa. Se a sessao reiniciar: o hook de boot (boot.sh) relanca esta fila e ela continua.
# Se NAO reiniciar em GRACE_MIN minutos, a fila segue sozinha com novo prazo. SESSION_GUARD=0 desliga a trava.
cd "$(dirname "$0")"; mkdir -p logs
LOCK=logs/queue.lock
LP=$(cat $LOCK 2>/dev/null); if [ -n "$LP" ] && kill -0 "$LP" 2>/dev/null && tr "\0" " " < /proc/$LP/cmdline 2>/dev/null | grep -q run_queue; then echo "fila ja rodando (pid $(cat $LOCK))"; exit 0; fi
echo $$ > $LOCK; trap 'rm -f $LOCK' EXIT
SESSION_MIN=${SESSION_MIN:-60}; SAFETY_MIN=${SAFETY_MIN:-6}; GRACE_MIN=${GRACE_MIN:-3}
uptime_s() { ps -o etimes= -p 1 2>/dev/null | tr -d ' ' || echo 0; }
while true; do
  NEXT=""
  while read -r id _; do
    case "$id" in ""|\#*) continue;; esac
    [ -f stories/$id/DONE ] && continue
    [ -f stories/$id/SKIP ] && continue   # reprovou 2x no gate: precisa de ajuste no roteiro/cena (veja logs/gate_<id>.txt); apague SKIP para tentar de novo
    NEXT=$id; break
  done < queue.txt
  [ -z "$NEXT" ] && { echo "$(date +%T) fila vazia: tudo pronto"; exit 0; }
  if [ "${SESSION_GUARD:-1}" != "0" ]; then
    UP=$(uptime_s); UP=${UP:-0}; LEFT=$(( SESSION_MIN*60 - UP - SAFETY_MIN*60 ))
    # container ja passou do prazo e NAO reiniciou: a estimativa estava errada -> novo ciclo inteiro (senao pausaria a cada 2 min)
    [ $LEFT -lt 120 ] && LEFT=$(( (SESSION_MIN - SAFETY_MIN)*60 ))
    export DEADLINE=$(( $(date +%s) + LEFT )); echo "$(date +%T) prazo de seguranca em $((LEFT/60)) min (container no ar ha $((UP/60)) min)"
  fi
  echo "$(date +%T) >>> $NEXT"
  bash make_video.sh "$NEXT"; RC=$?
  if [ $RC -eq 75 ]; then
    echo "$(date +%T) PAUSA DE SEGURANCA: checkpoint salvo. Aguardando $GRACE_MIN min por reinicio; se nao reiniciar, continuo."; sleep $((GRACE_MIN*60)); continue
  fi
  if [ $RC -ne 0 ] && [ $RC -ne 75 ]; then N=$(( $(cat stories/$NEXT/fails 2>/dev/null || echo 0) + 1 )); echo $N > stories/$NEXT/fails; [ $N -ge 2 ] && { touch stories/$NEXT/SKIP; echo "$(date +%T) $NEXT reprovou $N vezes: PULADO (veja logs/gate_$NEXT.txt)"; continue; }; fi
  [ $RC -ne 0 ] && { echo "$(date +%T) falhou $NEXT (veja logs/make_$NEXT.log); tentando de novo em 60 s"; sleep 60; }
done
