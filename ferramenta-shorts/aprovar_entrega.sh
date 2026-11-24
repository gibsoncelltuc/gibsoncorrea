#!/usr/bin/env bash
# 24/11 (ordem do Gibson: "nao misture os videos"): move um video CONFERIDO de videos_prontos/_a_conferir/ para a pasta da serie.
# So' a principal roda, depois de olhar o frase_a_frase inteiro. A pasta da serie tem SO' videos aprovados no padrao novo.
# uso: bash ferramenta-shorts/aprovar_entrega.sh <arquivo.mp4 dentro de _a_conferir>
cd "$(dirname "$0")/.."; f="videos_prontos/_a_conferir/$1"; [ -f "$f" ] || { echo "nao achei $f"; exit 1; }
serie=$(echo "$1" | sed -E 's/-EP-.*//; s/-/ /g'); case "$serie" in "Curiosidade e Ciencia"|"Guerras Inusitadas"|"Poder e Fama"|"E Se") ;; *) echo "sem serie/EP no nome: nao entra"; exit 1;; esac
mkdir -p "videos_prontos/$serie"; mv "$f" "videos_prontos/$serie/" && echo "APROVADO -> videos_prontos/$serie/$1"
