#!/usr/bin/env bash
# usage: ./pipeline.sh   (reads queue.txt lines "id:Title-Dashed:frames"; processes READY stories in order; stops at line END when all done)
cd "$(dirname "$0")"; DEL=/tmp/claude-0/-home-user-gibsoncorrea/21c2e349-3945-5426-9f97-539e9fc21a3c/scratchpad/deliver
while pgrep -f "render.mjs out/emu" >/dev/null; do sleep 20; done
while true; do did=0; alldone=1
  while IFS=: read ID T N; do [ -z "$ID" ] && continue; [ "$ID" = END ] && continue
    [ -f stories/$ID/DONE ] && continue; alldone=0; [ -f stories/$ID/READY ] || continue
    mkdir -p out/$ID/frames; S=$(( (N + 2) / 3 ))
    for k in 0 1 2; do a=$((k*S)); b=$(( (k+1)*S - 1 )); [ $b -ge $N ] && b=$((N-1)); WEB=$(cd ../webs/$ID && pwd) RESUME=1 node render.mjs out/$ID/frames "$a-$b" > logs/${ID}_$k.log 2>&1 & done; wait
    python3 qa_frames.py out/$ID/frames > logs/${ID}_qa.txt 2>&1
    ./assemble.sh $ID $T > logs/${ID}_asm.txt 2>&1 && cp out/$ID/$T.mp4 $DEL/ && touch stories/$ID/DONE; did=1; break
  done < queue.txt
  if [ $did = 0 ]; then if [ $alldone = 1 ] && grep -q '^END' queue.txt; then break; fi; sleep 30; fi
done
