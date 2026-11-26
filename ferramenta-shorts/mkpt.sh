#!/usr/bin/env bash
# usage: ./mkpt.sh <id> [voice] [rate]  -> creates stories/<id>_pt (PT-BR script, voice, retimed spec/cues from the EN story) and builds it
set -e; cd "$(dirname "$0")"; ID="$1"; VOICE="${2:-pt-BR-AntonioNeural}"; RATE="${3:-+10%}"; P="${ID}_pt"
mkdir -p stories/$P; python3 -c "
import ptscripts; open('stories/$P/script.txt','w').write(ptscripts.PT['$ID'])"
sed "s/id: '$ID'/id: '$P'/" stories/$ID/spec.js > stories/$P/spec.js
python3 - "$ID" "$P" <<'PY'
import re,sys
i,p=sys.argv[1:3]; c=open(f'stories/{i}/cues.py').read(); c=re.sub(r'(?<![A-Za-z0-9_])F\(','FE(',c); open(f'stories/{p}/cues.py','w').write(c)
PY
echo "$ID" > stories/$P/retime_from; echo pt > stories/$P/retime_lang
./produce_voice.sh $P "$VOICE" "$RATE" 2>&1 | grep -E "source=" 
./build3.sh $P 2>&1 | tail -2
