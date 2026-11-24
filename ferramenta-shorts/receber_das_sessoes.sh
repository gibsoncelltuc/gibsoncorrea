#!/usr/bin/env bash
# SESSAO PRINCIPAL: busca nos branches A/B as entregas em pedacos, remonta o mp4, confere o sha256 e poe em videos_prontos/<serie>/.
# Reprovado: deixe a linha "id sha" em logs/recebidos.txt (o mesmo arquivo nao volta); versao corrigida tem outro sha e chega como NOVO.
# Lista na saida os arquivos novos (a principal OLHA a folha de contato e manda pelo chat). Ja recebidos ficam em logs/recebidos.txt.
cd "$(dirname "$0")/.."; R=ferramenta-shorts/logs/recebidos.txt; touch $R
git fetch -q --depth=1 origin claude/prod-a2 claude/prod-b2   # so a ponta (disco: o historico dos pedacos de mp4 nao vem)
for BR in claude/prod-a2 claude/prod-b2; do
  for nf in $(git ls-tree -r --name-only origin/$BR entregas | grep '/mp4.nome$'); do
    d=$(dirname $nf); id=$(basename $d); sha=$(git show origin/$BR:$d/mp4.sha256 2>/dev/null)
    grep -q "^$id $sha$" $R && continue
    nome=$(git show origin/$BR:$nf); T=/tmp/claude-0/receb_$id; rm -rf $T; mkdir -p $T
    for p in $(git ls-tree --name-only origin/$BR $d/ | grep 'mp4.part_' | sort); do git show origin/$BR:$p >> $T/$nome; done
    [ "$(sha256sum $T/$nome | cut -d' ' -f1)" = "$sha" ] || { echo "ERRO $id: sha256 nao confere"; continue; }
    serie=$(echo $nome | sed -E 's/-EP-.*//; s/-/ /g'); case "$serie" in "Curiosidade e Ciencia"|"Guerras Inusitadas"|"Poder e Fama"|"E Se") ;; *) serie=Avulsos;; esac
    mkdir -p "videos_prontos/$serie"; mv $T/$nome "videos_prontos/$serie/"
    git show origin/$BR:$d/review_sheet.jpg > "/tmp/claude-0/receb_${id}_folha.jpg" 2>/dev/null
    echo "$id $sha" >> $R; echo "NOVO $BR $id -> videos_prontos/$serie/$nome | folha: /tmp/claude-0/receb_${id}_folha.jpg"
  done
done
