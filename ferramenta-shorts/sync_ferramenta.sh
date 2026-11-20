#!/usr/bin/env bash
# SINCRONIZA A FERRAMENTA AUTOMATICAMENTE (ordem do Gibson 19/11: as sessoes recebem e aplicam as correcoes sozinhas).
# Puxa o branch principal (claude/serene-dirac-ckwlt5), faz o merge, regenera as folhas dos videos ainda nao prontos, roda a
# verificacao de execucao e invalida storyboards que mudaram (a fila gera outro e a sessao revisa com grade + revisao escrita).
# Uso nas sessoes: nohup bash -c 'while true; do ./sync_ferramenta.sh >> logs/sync.log 2>&1; sleep 600; done' > /dev/null 2>&1 &
cd "$(dirname "$0")"; [ -f auto_aprovar.sh ] && { pgrep -f auto_aprovar.sh >/dev/null || nohup setsid bash auto_aprovar.sh >/dev/null 2>&1 & }   # auto-aprovacao de seguranca
MAIN=claude/serene-dirac-ckwlt5; cd ..
git fetch -q origin $MAIN || exit 0
[ -z "$(git log --oneline HEAD..FETCH_HEAD -- ferramenta-shorts ':!ferramenta-shorts/stories' ':!ferramenta-shorts/ckpt' 2>/dev/null)" ] && exit 0   # nada novo na ferramenta
# scripts bash que a fila esta EXECUTANDO nao podem mudar no meio: se mudaram, espera a fila ficar entre videos
if git diff --name-only HEAD FETCH_HEAD | grep -qE 'ferramenta-shorts/(make_video|run_queue|assemble|render)\.sh$' && pgrep -f make_video.sh >/dev/null; then
  echo "$(date +%T) atualizacao com scripts da fila: espera o video atual terminar"; exit 0; fi
git add -A >/dev/null 2>&1; git commit -qm "ckpt antes do sync automatico da ferramenta" >/dev/null 2>&1
if ! git merge --no-edit -X theirs FETCH_HEAD >/dev/null 2>&1; then git merge --abort 2>/dev/null; echo "$(date +%T) MERGE FALHOU: resolver na mao"; exit 1; fi
cd ferramenta-shorts; cat web/toonbase.js web/roman.js web/pig2d.js web/animals2d.js > web/toon.js
N=0
for id in $(grep -v '^#' "$(bash qfile.sh)" 2>/dev/null); do
  [ -f stories/$id/DONE ] && continue; [ -f videos/$id/beats.json ] || continue
  pgrep -af "make_video.sh $id\$" >/dev/null && continue
  python3 mkvideo.py $id > /dev/null 2>&1 || { echo "$(date +%T) $id: mkvideo falhou"; continue; }
  python3 verificar_execucao.py $id | grep -q '<-' && echo "$(date +%T) $id: EXECUCAO COM FALHA -> corrigir (python3 verificar_execucao.py $id)"
  N=$((N + 1))
done
cd ..; git add -A >/dev/null 2>&1; git commit -qm "sync automatico da ferramenta ($(git rev-parse --short FETCH_HEAD)); folhas de $N videos regeneradas" >/dev/null 2>&1
git push -q origin HEAD >/dev/null 2>&1
echo "$(date +%T) ferramenta sincronizada com $(git rev-parse --short FETCH_HEAD); $N videos reconferidos (storyboard que mudou sera refeito e REVISADO de novo)"
