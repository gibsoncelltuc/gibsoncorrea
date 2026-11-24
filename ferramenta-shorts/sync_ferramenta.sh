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
IGUAL=0; [ -z "$(git diff --diff-filter=MD --name-only FETCH_HEAD HEAD -- "${FERR[@]}" CLAUDE.md .claude)" ] && IGUAL=1
if [ $IGUAL = 1 ]; then cd ferramenta-shorts; for id in $(cat queue.txt $(cat logs/.fila_origem 2>/dev/null) 2>/dev/null | grep -v "^#" | awk "NF{print \$1}" | sort -u); do [ -f stories/$id/DONE ] || [ -f stories/$id/STORYBOARD_OK ] || [ ! -f videos/$id/beats.json ] && continue; grep -q "FICHA -->" stories/$id/folha2_producao.md 2>/dev/null && continue; pgrep -af "make_video.sh $id\$" >/dev/null && continue; python3 enquadrar.py $id >/dev/null 2>&1; python3 mkvideo.py $id >/dev/null 2>&1; python3 ficha_nas_folhas.py $id >/dev/null 2>&1 && echo "$(date +%T) $id: ficha de cena aplicada nas folhas"; done; exit 0; fi   # ferramenta ja identica a da principal (arquivos que so' a sessao tem nao contam)
# scripts bash que a fila esta EXECUTANDO nao podem mudar no meio: se mudaram, espera a fila ficar entre videos
SEGURA=()   # 24/11: com video rodando, so' os scripts que a fila esta EXECUTANDO esperam; o resto da ferramenta (ficha de cena, checagens, olhos) entra JA
if git diff --name-only HEAD FETCH_HEAD | grep -qE 'ferramenta-shorts/(make_video|run_queue|assemble|render)\.sh$' && pgrep -f make_video.sh >/dev/null; then
  SEGURA=(':!ferramenta-shorts/make_video.sh' ':!ferramenta-shorts/run_queue.sh' ':!ferramenta-shorts/assemble.sh' ':!ferramenta-shorts/render.sh'); echo "$(date +%T) scripts da fila seguram ate o video atual terminar; resto da ferramenta atualizado agora"; fi
git add -A >/dev/null 2>&1; git commit -qm "ckpt antes do sync automatico da ferramenta" >/dev/null 2>&1
git merge --no-edit -X theirs FETCH_HEAD >/dev/null 2>&1 || { git merge --abort 2>/dev/null; echo "$(date +%T) merge nao aplicou (historicos diferentes): copiando a ferramenta direto da principal"; }
# FORCA: depois do merge (ou sem ele), cada arquivo da ferramenta fica IGUAL ao da principal -- nenhuma edicao antiga da sessao sobrevive no motor
git checkout FETCH_HEAD -- "${FERR[@]}" "${SEGURA[@]}" CLAUDE.md .claude 2>/dev/null
git show FETCH_HEAD:ferramenta-shorts/PAUSA > /dev/null 2>&1 && git checkout FETCH_HEAD -- ferramenta-shorts/PAUSA 2>/dev/null   # a pausa da principal vale para as sessoes
[ -z "$(git diff --diff-filter=MD --name-only FETCH_HEAD -- "${FERR[@]}")" ] || echo "$(date +%T) AVISO: ainda ha arquivo do motor diferente da principal (git diff --diff-filter=MD FETCH_HEAD -- ferramenta-shorts)"   # arquivo que so a sessao tem (objeto que ela modelou) nao conta
cd ferramenta-shorts; cat web/toonbase.js web/roman.js web/pig2d.js web/animals2d.js > web/toon.js
N=0
FILAS="queue.txt"; for f_ in fila_principal.txt fila_sessao_A.txt fila_sessao_B.txt; do grep -qx "$(cat logs/.fila_origem 2>/dev/null)" <<< "$f_" && FILAS="$FILAS $f_"; done
for id in $(cat $FILAS 2>/dev/null | grep -v '^#' | awk 'NF{print $1}' | sort -u); do
  [ -f stories/$id/DONE ] && continue; [ -f videos/$id/beats.json ] || continue
  pgrep -af "make_video.sh $id\$" >/dev/null && continue
  [ -f stories/$id/STORYBOARD_OK ] || python3 enquadrar.py $id > /dev/null 2>&1   # 24/11: FICHA DE CENA em TODO roteiro da fila (storyboard aprovado nao e' mexido)
  python3 mkvideo.py $id > /dev/null 2>&1 || { echo "$(date +%T) $id: mkvideo falhou"; continue; }
  python3 ficha_nas_folhas.py $id > /dev/null 2>&1   # folha 2 com ficha tecnica + takes, folha 3 com fisica e movimento
  python3 verificar_execucao.py $id | grep -q '<-' && echo "$(date +%T) $id: EXECUCAO COM FALHA -> corrigir (python3 verificar_execucao.py $id)"
  N=$((N + 1))
done
cd ..; git add -A >/dev/null 2>&1; git commit -qm "sync automatico da ferramenta ($(git rev-parse --short FETCH_HEAD)); folhas de $N videos regeneradas" >/dev/null 2>&1
git push -q origin HEAD >/dev/null 2>&1
echo "$(date +%T) ferramenta sincronizada com $(git rev-parse --short FETCH_HEAD); $N videos reconferidos (storyboard que mudou sera refeito e REVISADO de novo)"
