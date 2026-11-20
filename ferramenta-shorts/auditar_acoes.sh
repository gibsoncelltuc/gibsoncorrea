#!/usr/bin/env bash
# AUDITORIA DE ACOES (19/11, ZERO RESSALVA): 1 quadro do mp4 entregue logo depois de cada palavra de acao da folha 3 -> /tmp/claude-0/aud/<id>.jpg
# uso: bash auditar_acoes.sh <branch> <id> <caminho absoluto do mp4>
# uso: grade.sh <branch> <id> <mp4>  -> /tmp/claude-0/aud/<id>.jpg (1 quadro por acao da folha 3, com rotulo)
BR=$1; ID=$2; MP4=$3; D=/tmp/claude-0/aud/$ID; rm -rf $D; mkdir -p $D
cd /home/user/gibsoncorrea
git show origin/$BR:ferramenta-shorts/stories/$ID/folha3_acao.md 2>/dev/null > $D/f3.md ; [ -s $D/f3.md ] || cp /home/user/gibsoncorrea/ferramenta-shorts/stories/$ID/folha3_acao.md $D/f3.md
n=0; cena=""
while IFS= read -r l; do
  [[ $l =~ ^##\ Cena\ (b[0-9]+) ]] && cena=${BASH_REMATCH[1]}
  if [[ $l =~ ^\|\ [0-9]+\ \|\ (.+)\ \(([0-9.]+)s\)\ \|\ ([^|]+)\| ]]; then
    w=${BASH_REMATCH[1]}; t=${BASH_REMATCH[2]}; a=$(echo "${BASH_REMATCH[3]}" | sed 's/ *$//')
    [[ $a == EFEITO* ]] && continue
    n=$((n+1)); t2=$(python3 -c "print(max(0,$t+0.35))")
    ffmpeg -loglevel error -y -ss $t2 -i "$MP4" -frames:v 1 -vf "scale=300:-1,drawbox=y=ih-34:w=iw:h=34:color=black@0.7:t=fill,drawtext=text='$cena $w $a':fontcolor=white:fontsize=13:x=4:y=h-26" $D/$(printf %03d $n).jpg 2>/dev/null
  fi
done < $D/f3.md
ls $D/*.jpg >/dev/null 2>&1 || { echo "$ID: sem quadros"; exit 1; }
N=$(ls $D/*.jpg | wc -l); C=8
ffmpeg -loglevel error -y -pattern_type glob -i "$D/*.jpg" -vf "tile=${C}x$(( (N+C-1)/C ))" -frames:v 1 /tmp/claude-0/aud/$ID.jpg
echo "$ID: $N acoes -> /tmp/claude-0/aud/$ID.jpg"
