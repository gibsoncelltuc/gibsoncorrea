#!/usr/bin/env bash
# encoda trechos de 1800 quadros ja prontos em video (sem audio) e apaga os jpg (disco pequeno)
D=$1; N=$2; mkdir -p $D/segs; s=${3:-0}
while [ $s -lt $N ]; do
  e=$(( s + 1800 )); [ $e -gt $N ] && e=$N
  ok=1; for ((f=s; f<e; f++)); do [ -f $D/frames/$(printf f%05d.jpg $f) ] || { ok=0; break; }; done
  if [ $ok = 1 ]; then
    ffmpeg -v error -y -framerate 30 -start_number $s -i $D/frames/f%05d.jpg -frames:v $(( e - s )) -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p $D/segs/s$(printf %05d $s).mp4 && \
    [ "$(ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames -of csv=p=0 $D/segs/s$(printf %05d $s).mp4)" = "$(( e - s ))" ] && \
    for ((f=s; f<e; f++)); do rm -f $D/frames/$(printf f%05d.jpg $f); done && echo "seg $s-$e ok"
    s=$e
  else sleep 30; fi
done
echo FIM
