#!/usr/bin/env bash
# PT-BR production line: for each story: framing fit -> take/style gate (must pass, one refit retry) -> audio+captions -> 3-shard render -> frame QA (+1 repair pass) -> assemble -> deliver folder.
# Idempotent (RESUME=1 + DONE markers): after a worker restart just launch it again.  NEVER run build3.sh by hand while this runs (web/ is shared).
cd "$(dirname "$0")"; DEL=/tmp/claude-0/-home-user-gibsoncorrea/21c2e349-3945-5426-9f97-539e9fc21a3c/scratchpad/deliver; mkdir -p $DEL
L="emu:Guerra-dos-Emus ghost:O-Exercito-Feito-de-Baloes bucket:A-Guerra-do-Balde onoda:O-Soldado-que-Nunca-se-Rendeu whisky:A-Guerra-do-Uisque zanzibar:A-Guerra-de-38-Minutos pastry:A-Guerra-dos-Bolos jenkins:A-Guerra-da-Orelha-de-Jenkins football:A-Guerra-do-Futebol wojtek:O-Urso-que-Entrou-no-Exercito"
gate_ok() { grep -q "camera OK" logs/gate_$1.txt && grep -q "ALL TAKES OK" logs/gate_$1.txt && grep -q "STYLE OK" logs/gate_$1.txt; }
render3() { ./render_missing.sh $1 $2; }
for it in $L; do I=${it%%:*}; T="PT_${it#*:}"; P=${I}_pt; [ -f stories/$P/DONE ] && continue
  if [ -n "$ONLY" ]; then case " $ONLY " in *" $I "*) ;; *) continue;; esac; fi   # ONLY="emu ghost" limits the run (so each story can be storyboard-reviewed before its render)
  echo "$(date +%T) START $P" >> logs/pipeline_pt.log
  [ -f stories/$P/fit.js ] || ./fit.sh $P >> logs/fit_$P.log 2>&1
  ./gate_all.sh $P
  if ! gate_ok $P; then echo "$(date +%T) GATE FAIL $P -> refit" >> logs/pipeline_pt.log; rm -f stories/$P/fit.js; ./fit.sh $P >> logs/fit_$P.log 2>&1; ./gate_all.sh $P; fi
  if ! gate_ok $P; then echo "$(date +%T) GATE FAILED AFTER REFIT $P (story skipped, needs manual fix)" >> logs/pipeline_pt.log; continue; fi
  ./build3.sh $P > /dev/null 2>&1
  N=$(python3 -c "import json;print(json.load(open('stories/$P/work/phrases.json'))['frames30'])")
  ./snap.sh $P $N >> logs/snap_$P.log 2>&1 || { echo "$(date +%T) SNAP FAILED $P" >> logs/pipeline_pt.log; continue; }
  (cd stories/$P && python3 ../../caps.py > /dev/null)
  mkdir -p out/$P/frames; render3 $P $N
  python3 qa_frames.py out/$P/frames > logs/${P}_qa.txt 2>&1
  if grep -qE "^ +[0-9]+ .*(band|black|white|glitch)" logs/${P}_qa.txt; then   # one repair pass: delete only the flagged frames and render them again
    python3 qa_frames.py out/$P/frames --rerender > /dev/null 2>&1; echo "$(date +%T) REPAIR PASS $P" >> logs/pipeline_pt.log; render3 $P $N
    python3 qa_frames.py out/$P/frames > logs/${P}_qa2.txt 2>&1
  fi
  ./assemble.sh $P $T > logs/${P}_asm.txt 2>&1 && cp out/$P/$T.mp4 $DEL/ && touch stories/$P/DONE && echo "$(date +%T) DONE $P -> $T.mp4" >> logs/pipeline_pt.log
done
echo "$(date +%T) ALL DONE" >> logs/pipeline_pt.log
