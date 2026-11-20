#!/usr/bin/env bash
# build + camera + inspetor de takes + estilo, para cada story; grava logs/gate_<id>.txt
# Rapido: o inspetor de takes ja' rodou dentro do fit.sh (selo stories/<id>/takes_ok) -> so' repete se o selo faltar (ou GATE_FULL=1).
cd "$(dirname "$0")"; mkdir -p logs
for s in "$@"; do ./build3.sh $s >/dev/null 2>&1; { echo "## $s"; node qa_camera.mjs 2>&1 | tail -1
  if [ -f stories/$s/takes_ok ] && [ -z "$GATE_FULL" ]; then echo "ALL TAKES OK (selo do fit)"; else node qa_takes.mjs 4 2>&1 | grep -E "FAIL|e\.g\.|ALL TAKES|fail|rror|TINY" | head -12; fi
  ./qa_style.sh $s 2>&1 | tail -9; } > logs/gate_$s.txt 2>&1; done
echo finished > logs/gate_done.txt
