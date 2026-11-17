#!/usr/bin/env bash
# Monta um episódio de 6 clipes de 10 s (cortes secos, no compasso) e, se houver, põe uma música por cima.
# Uso: montar_ep.sh <pasta_com_V??-1..6.mp4> <saida.mp4> [musica.(mp3|wav|m4a)]
# Sem música: mantém o áudio original dos clipes (versão-guia), com volume igualado.
# Com música: troca o áudio pela música, ajustada a 60 s (estica/encurta até 6%), com fade final e -14 LUFS.
set -euo pipefail
DIR="$1"; OUT="$2"; MUSIC="${3:-}"
shopt -s nullglob
CLIPS=("$DIR"/V*-1.mp4 "$DIR"/V*-2.mp4 "$DIR"/V*-3.mp4 "$DIR"/V*-4.mp4 "$DIR"/V*-5.mp4 "$DIR"/V*-6.mp4)
[ "${#CLIPS[@]}" -eq 6 ] || { echo "preciso de 6 clipes V??-1..6.mp4 em $DIR"; exit 1; }
ARGS=(); FC=""
for i in 0 1 2 3 4 5; do
  ARGS+=(-i "${CLIPS[$i]}")
  FC+="[$i:v]fps=24,scale=1080:1920,setsar=1,trim=duration=10,setpts=PTS-STARTPTS[v$i];"
  FC+="[$i:a]aresample=48000,atrim=duration=10,asetpts=PTS-STARTPTS[a$i];"
done
FC+="[v0][v1][v2][v3][v4][v5]concat=n=6:v=1:a=0[v];[a0][a1][a2][a3][a4][a5]concat=n=6:v=0:a=1[a]"
TMP="$(mktemp -d)"
ffmpeg -v error -y "${ARGS[@]}" -filter_complex "$FC" -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -c:a pcm_s16le "$TMP/raw.mkv"
if [ -z "$MUSIC" ]; then
  ffmpeg -v error -y -i "$TMP/raw.mkv" -af "loudnorm=I=-14:TP=-1.5:LRA=7,afade=t=out:st=59.3:d=0.7" \
    -c:v copy -c:a aac -b:a 192k -movflags +faststart "$OUT"
else
  DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$MUSIC")
  F=$(python3 - "$DUR" <<'PY'
import sys
d=float(sys.argv[1]); r=d/60.0
print(f"atempo={r:.5f}," if abs(r-1)<=0.06 and abs(r-1)>0.002 else "")
PY
)
  ffmpeg -v error -y -i "$TMP/raw.mkv" -i "$MUSIC" -map 0:v -map 1:a \
    -af "${F}atrim=duration=60,loudnorm=I=-14:TP=-1.5:LRA=7,afade=t=out:st=58.6:d=1.4,apad=whole_dur=60" \
    -t 60 -c:v copy -c:a aac -b:a 192k -movflags +faststart "$OUT"
fi
rm -rf "$TMP"; ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$OUT"
