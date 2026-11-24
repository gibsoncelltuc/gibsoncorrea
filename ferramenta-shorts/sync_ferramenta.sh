#!/usr/bin/env bash
# SINCRONIZA A FERRAMENTA AUTOMATICAMENTE (ordem do Gibson 19/11: as sessoes recebem e aplicam as correcoes sozinhas).
# Puxa o branch principal (claude/bold-sagan-dskrsj), faz o merge, regenera as folhas dos videos ainda nao prontos, roda a
# verificacao de execucao e invalida storyboards que mudaram (a fila gera outro e a sessao revisa com grade + revisao escrita).
# Uso nas sessoes: nohup bash -c 'while true; do ./sync_ferramenta.sh >> logs/sync.log 2>&1; sleep 60; done' > /dev/null 2>&1 &
cd "$(dirname "$0")"; exec 9>/tmp/sync_ferramenta.lock; flock -n 9 || exit 0   # a cada 1 min: nunca duas sincronizacoes ao mesmo tempo
[ -f auto_aprovar.sh ] && { pgrep -f auto_aprovar.sh >/dev/null || nohup setsid bash auto_aprovar.sh >/dev/null 2>&1 & }   # auto-aprovacao de seguranca
MAIN=claude/bold-sagan-dskrsj; cd ..
git fetch -q origin $MAIN || exit 0
# FERRAMENTA = tudo em ferramenta-shorts menos o que e' da sessao (roteiros, folhas, trechos, pesquisas, filas). A comparacao e' pelo CONTEUDO dos arquivos
# (nao pelo historico): mesmo que a sessao tenha editado o motor ou copiado arquivos a mao, se ficou diferente da principal ela volta a ficar IDENTICA.
FERR=(ferramenta-shorts ':!ferramenta-shorts/stories' ':!ferramenta-shorts/videos' ':!ferramenta-shorts/ckpt' ':!ferramenta-shorts/referencias' ':!ferramenta-shorts/queue.txt' ':!ferramenta-shorts/web/story.js' ':!ferramenta-shorts/web/main.js' ':!ferramenta-shorts/web/toon.js' ':!ferramenta-shorts/PAUSA')
git diff --quiet HEAD FETCH_HEAD -- "${FERR[@]}" CLAUDE.md .claude && exit 0   # ferramenta ja identica a da principal
# scripts bash que a fila esta EXECUTANDO nao podem mudar no meio: se mudaram, espera a fila ficar entre videos
if git diff --name-only HEAD FETCH_HEAD | grep -qE 'ferramenta-shorts/(make_video|run_queue|assemble|render)\.sh$' && pgrep -f make_video.sh >/dev/null; then
  echo "$(date +%T) atualizacao com scripts da fila: espera o video atual terminar"; exit 0; fi
git add -A >/dev/null 2>&1; git commit -qm "ckpt antes do sync automatico da ferramenta" >/dev/null 2>&1
git merge --no-edit -X theirs FETCH_HEAD >/dev/null 2>&1 || { git merge --abort 2>/dev/null; echo "$(date +%T) merge nao aplicou (historicos diferentes): copiando a ferramenta direto da principal"; }
# FORCA: depois do merge (ou sem ele), cada arquivo da ferramenta fica IGUAL ao da principal -- nenhuma edicao antiga da sessao sobrevive no motor
git checkout FETCH_HEAD -- "${FERR[@]}" CLAUDE.md .claude 2>/dev/null
git show FETCH_HEAD:ferramenta-shorts/PAUSA > /dev/null 2>&1 && git checkout FETCH_HEAD -- ferramenta-shorts/PAUSA 2>/dev/null   # a pausa da principal vale para as sessoes
git diff --quiet FETCH_HEAD -- "${FERR[@]}" || echo "$(date +%T) AVISO: ainda ha diferenca para a principal (ver git diff FETCH_HEAD -- ferramenta-shorts)"
cd ferramenta-shorts; cat web/toonbase.js web/roman.js web/pig2d.js web/animals2d.js > web/toon.js
N=0
for id in $(grep -v '^#' queue.txt 2>/dev/null); do
  [ -f stories/$id/DONE ] && continue; [ -f videos/$id/beats.json ] || continue
  pgrep -af "make_video.sh $id\$" >/dev/null && continue
  python3 mkvideo.py $id > /dev/null 2>&1 || { echo "$(date +%T) $id: mkvideo falhou"; continue; }
  python3 verificar_execucao.py $id | grep -q '<-' && echo "$(date +%T) $id: EXECUCAO COM FALHA -> corrigir (python3 verificar_execucao.py $id)"
  N=$((N + 1))
done
cd ..; git add -A >/dev/null 2>&1; git commit -qm "sync automatico da ferramenta ($(git rev-parse --short FETCH_HEAD)); folhas de $N videos regeneradas" >/dev/null 2>&1
git push -q origin HEAD >/dev/null 2>&1
echo "$(date +%T) ferramenta sincronizada com $(git rev-parse --short FETCH_HEAD); $N videos reconferidos (storyboard que mudou sera refeito e REVISADO de novo)"
