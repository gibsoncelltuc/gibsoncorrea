#!/usr/bin/env bash
# usage: ./snap.sh <id> <frames>   (after build3 + QA pass) -> snapshot web + audio + READY marker
set -e; cd "$(dirname "$0")"; ID="$1"; N="$2"; D=../webs/$ID
rm -rf $D; mkdir -p $D; cp web/*.js web/index.html $D/ 2>/dev/null; ls web | grep -v '\.js$' | grep -v index.html | while read f; do ln -s "$(pwd)/web/$f" $D/$f; done
ln -s "$(pwd)/web/sets" $D/sets 2>/dev/null || true
python3 audio_story.py $ID $N | tail -1; touch stories/$ID/READY; echo "snap $ID ready"
