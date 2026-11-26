#!/usr/bin/env bash
# renderiza os longos em sequencia (um por vez; www/spec.json e' compartilhado)
cd "$(dirname "$0")"
for v in v2_descida:v2 v3_saturno:v3 v4_plutao:v4 v1_fundo_mar:v1; do j=${v%%:*}; d=${v##*:}; [ -f $d/$j.mp4 ] && continue; python3 fazer_longo.py $j.json $d > $d/render.log 2>&1; echo "$(date +%T) $j: $(tail -1 $d/render.log)"; done
