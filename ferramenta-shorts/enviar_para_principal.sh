#!/usr/bin/env bash
# ENVIA O VIDEO PRONTO PARA A SESSAO PRINCIPAL (ordem do Gibson 19/11: ele quer receber TODOS os videos na conversa principal).
# O GitHub nao aceita arquivo > 100 MB: o mp4 vai em pedacos de 90 MB + sha256; a principal remonta, confere e manda pelo chat.
# uso (sessoes A/B, depois de conferir.sh e de OLHAR a folha de contato): ./enviar_para_principal.sh <id>
cd "$(dirname "$0")"; ID="${1:?id}"; cd ..
MP4=$(ls ferramenta-shorts/out/$ID/*.mp4 2>/dev/null | head -1); [ -f "$MP4" ] || { echo "sem mp4 em out/$ID"; exit 1; }
# DISCO (19/11): pedaços de vídeos que a principal JÁ recebeu saem do branch (o repositório não cresce sem fim)
git fetch -q origin claude/serene-dirac-ckwlt5 2>/dev/null; for r in $(git show FETCH_HEAD:ferramenta-shorts/logs/recebidos.txt 2>/dev/null | cut -d' ' -f1); do [ "$r" != "$ID" ] && [ -n "$(ls entregas/$r/mp4.part_* 2>/dev/null)" ] && git rm -q --cached entregas/$r/mp4.part_* && rm -f entregas/$r/mp4.part_*; done
D=entregas/$ID; mkdir -p $D; rm -f $D/mp4.part_* $D/mp4.sha256 $D/mp4.nome
split -b 90m -d "$MP4" $D/mp4.part_
sha256sum "$MP4" | cut -d' ' -f1 > $D/mp4.sha256; basename "$MP4" > $D/mp4.nome
cp ferramenta-shorts/out/$ID/review_sheet.jpg $D/review_sheet.jpg 2>/dev/null
git add -f $D/mp4.part_* $D/mp4.sha256 $D/mp4.nome $D/review_sheet.jpg 2>/dev/null; git add $D
git commit -qm "entrega $ID para a sessao principal ($(ls $D/mp4.part_* | wc -l) partes)" && for k in 1 2 3 4; do git push -q origin HEAD && break; sleep $((k * 5)); done
echo "enviado: $D ($(ls $D/mp4.part_* | wc -l) partes, $(cat $D/mp4.nome))"
