#!/usr/bin/env bash
# usage: ./fit.sh <id>  -> enquadra a camera de cada take ate o inspetor passar; grava stories/<id>/fit.js (1 navegador so', ver fit_fast.mjs)
cd "$(dirname "$0")"; ID=$1; rm -f stories/$ID/fit.js; ./build3.sh $ID >/dev/null && node fit_fast.mjs $ID 2>&1 | grep -v MODULE_TYPELESS && ./build3.sh $ID >/dev/null
