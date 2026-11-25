#!/usr/bin/env bash
# Edição final de um episódio: 6 clipes de 10 s + música, com transições, movimento de câmera suave,
# correção de cor leve, efeitos sonoros discretos nas trocas, fade final e volume padrão do YouTube.
# Uso: montar_ep_pro.sh <pasta_clipes V01-1..6.mp4> <musica> <saida.mp4>
# Duração final sempre 60 s. Os cortes caem em 10, 20, 30, 40 e 50 s (a transição começa no corte).
set -euo pipefail
DIR="$1"; MUSIC="$2"; OUT="$3"
TR=0.35                       # duração de cada transição (s)
EFFECTS=(smoothleft zoomin circleopen smoothleft fadewhite)   # fadewhite = "brilho" antes do sorriso final
ARGS=(); FC=""
for i in 0 1 2 3 4 5; do
  n=$((i+1)); ARGS+=(-i "$DIR/V01-$n.mp4")
  PAD=""; [ $i -lt 5 ] && PAD=",tpad=stop_mode=clone:stop_duration=$TR"
  # push-in suave de 0 a 5% ao longo do clipe + cor levemente mais viva
  FC+="[$i:v]fps=24,scale=1080:1920,setsar=1,trim=duration=10,setpts=PTS-STARTPTS$PAD,"
  FC+="scale=w='trunc(1080*(1+0.05*min(t,10)/10)/2)*2':h=-2:eval=frame,crop=1080:1920,"
  FC+="eq=saturation=1.07:contrast=1.03,format=yuv420p[v$i];"
done
prev="v0"
for k in 0 1 2 3 4; do
  off=$(( (k+1)*10 ))
  FC+="[$prev][v$((k+1))]xfade=transition=${EFFECTS[$k]}:duration=$TR:offset=$off[x$k];"
  prev="x$k"
done
FC+="[$prev]fade=t=out:st=59.4:d=0.6[v];"
# --- áudio: música ajustada a 60 s + 5 "whooshes" discretos + 1 brilho no último corte
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$MUSIC")
ATEMPO=$(python3 -c "
d=float('$DUR'); r=d/60.0
print(f'atempo={r:.5f},' if 0.002<abs(r-1)<=0.06 else '')")
M=${#ARGS[@]}; MI=6          # índice da entrada da música
ARGS+=(-i "$MUSIC")
FC+="[$MI:a]${ATEMPO}atrim=duration=60,asetpts=PTS-STARTPTS,apad=whole_dur=60[mus];"
SFXIN=""
for k in 0 1 2 3 4; do
  ms=$(( (k+1)*10000 - 60 ))
  if [ $k -eq 4 ]; then
    FC+="aevalsrc='(sin(2*PI*2093*t)+0.8*sin(2*PI*2637*t)+0.6*sin(2*PI*3136*t))*exp(-5*t)*0.10':d=0.7:s=48000,adelay=${ms}|${ms}[s$k];"
  else
    FC+="anoisesrc=d=0.45:c=pink:a=0.5:r=48000,bandpass=f=1700:w=1.6,afade=t=in:d=0.15,afade=t=out:st=0.18:d=0.27,volume=0.16,aformat=channel_layouts=stereo,adelay=${ms}|${ms}[s$k];"
  fi
  SFXIN+="[s$k]"
done
FC+="[mus]aformat=channel_layouts=stereo[m2];[m2]${SFXIN}amix=inputs=6:normalize=0:duration=first[mix];"
FC+="[mix]loudnorm=I=-14:TP=-1.5:LRA=7,afade=t=out:st=58.6:d=1.4[a]"
ffmpeg -v error -y "${ARGS[@]}" -filter_complex "$FC" -map "[v]" -map "[a]" -t 60 \
  -c:v libx264 -preset slow -crf "${CRF:-21}" -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "$OUT"
ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$OUT"
