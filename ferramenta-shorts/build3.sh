#!/usr/bin/env bash
# usage: ./build3.sh <story-id>   -> web/story.js, web/toon.js, web/main.js
set -e; cd "$(dirname "$0")"; ID="${1:?story id}"
cd web
cat toonbase.js roman.js pig2d.js animals2d.js > toon.js
python3 - "$ID" > ../stories/$ID/timing.js <<'PYT'
import json,sys,os
i=sys.argv[1]; d=f'../stories/{i}/work/'
try:
    W=json.load(open(d+'words.json')); P=json.load(open(d+'phrases.json'))['phrases']
    PH=json.load(open(d+'phrases.json'))
    print('const TIMING = '+json.dumps({'total':int(PH.get('frames30',0)),'words':[[round(w['s']*30),round(w['e']*30),w['w']] for w in W],'phrases':[[round(p['s']*30),round(p['e']*30),p['text']] for p in P]})+';')
except Exception as e:
    print('const TIMING = { words: [], phrases: [] };')
PYT
if [ -f ../stories/$ID/retime_from ]; then (cd .. && python3 mkretime.py $ID) || exit 1; RT="../stories/$ID/retime.js retime.js"; else RT=""; fi
cat ../stories/$ID/timing.js ../stories/_h.js ../stories/$ID/spec.js $( [ -f ../stories/$ID/fit.js ] && echo ../stories/$ID/fit.js ) $RT runtime.js acting.js > story.js
sed -i "s#import { SHOTS, TOTAL, shotAt, camAt, dofAt, LIGHTS, lightFor, actorsAt, worldAt, fxAt } from './story.js';#import { SHOTS, TOTAL, shotAt, camAt, dofAt, LIGHTS, lightFor, actorsAt, worldAt, fxAt, ASSETS, SETS_USED, SETX, HEROES } from './story.js';#" head.js
cat head.js core.js sets/_base.js $(ls sets/*.js | grep -v _base | grep -v dress) sets/dress.js boot.js weather.js tail.js > main.js
sed -i 's|^window.TOTAL = TOTAL;|window.TOTAL = TOTAL; window.__scene = scene; window.__cam = camera;|' main.js
node --check main.js && echo "built $ID"
