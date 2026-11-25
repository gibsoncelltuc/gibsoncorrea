#!/usr/bin/env bash
# 25/11 (Gibson: "versao em ingles do mesmo video: narracao, legenda e placas em ingles"). Faz a versao em OUTRA LINGUA de um video pronto,
# reaproveitando a animacao: voz nova -> retime (cada frase da voz nova casada com a frase original) -> placas traduzidas -> render -> mp4.
# Pre-requisito: stories/<id>_<lang>/script.txt com as MESMAS frases e a MESMA pontuacao do original (uma frase por linha, inclusive a chamada final).
# Placas: traducoes.json no mesmo lugar, {"TEXTO ORIGINAL": "TRANSLATION"}.
# uso: bash mk_lingua.sh <id> <lang> "<Titulo-Com-Tracos>" [voz] [velocidade]     ex.: bash mk_lingua.sh roadsterpulo2026 en "Power-and-Fame-EP-25-..." en-US-AndrewNeural -4%
# NUNCA rode com a fila montando outro video no mesmo instante (build3 escreve em web/); o render usa o snapshot proprio (webs/<id>_<lang>) e pode correr junto.
set -e; cd "$(dirname "$0")"; I="$1"; L="$2"; T="$3"; V="${4:-en-US-AndrewNeural}"; R="${5:--4%}"; P="${I}_${L}"
[ -f stories/$P/script.txt ] || { echo "falta stories/$P/script.txt"; exit 1; }
./produce_voice.sh $P "$V" "$R" | tail -1
python3 - "$I" "$P" <<'PY'
import json, re, sys, os
I, P = sys.argv[1:3]
s = open(f'stories/{I}/spec.js', encoding='utf-8').read().replace(f'id: "{I}"', f'id: "{P}"')
tr = json.load(open(f'stories/{P}/traducoes.json', encoding='utf-8')) if os.path.exists(f'stories/{P}/traducoes.json') else {}
for a, b in tr.items(): s = s.replace(json.dumps(a), json.dumps(b)).replace(json.dumps(a, ensure_ascii=False), json.dumps(b, ensure_ascii=False))
t = open(f'stories/{I}/timing.js', encoding='utf-8').read().strip(); assert t.startswith('const TIMING = ')
s = s.replace("const WS = (i, off = 0) => TIMING.words[Math.min(i, TIMING.words.length - 1)][0] + off;",
              'const TIMING_SRC = ' + t[len('const TIMING = '):] + "\nconst WS = (i, off = 0) => TIMING_SRC.words[Math.min(i, TIMING_SRC.words.length - 1)][0] + off;   // a cena e' escrita na linha do tempo da lingua ORIGINAL (o retime converte)", 1).replace('TOTAL_F()', '(TIMING_SRC.total || TOTAL_F())')
open(f'stories/{P}/spec.js', 'w', encoding='utf-8').write(s)
left = sorted(set(re.findall(r'"[A-ZÁÉÍÓÚÂÊÔÃÕÇ][A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9 =!/.,%$-]{3,}"', s)) - set(json.dumps(v) for v in tr.values()))
print('PLACAS SEM TRADUCAO (confira):', left)
c = open(f'stories/{I}/cues.py', encoding='utf-8').read(); c = re.sub(r'(?<![A-Za-z0-9_])F\(', 'FE(', c); open(f'stories/{P}/cues.py', 'w', encoding='utf-8').write(c)
PY
cp stories/$I/fit.js stories/$P/fit.js; sed -i "s/\"$I\"/\"$P\"/g; s/'$I'/'$P'/g" stories/$P/fit.js
echo "$I" > stories/$P/retime_from; echo "$L" > stories/$P/retime_lang
./build3.sh $P | tail -2
N=$(python3 -c "import json;print(json.load(open('stories/$P/work/phrases.json'))['frames30'])")
./snap.sh $P $N | tail -1; (cd stories/$P && python3 ../../caps.py >/dev/null)
mkdir -p out/$P ckpt/$P; node render_pool.mjs $P $N > logs/make_$P.log 2>&1
./assemble.sh $P "$T" | tail -2
echo "PRONTO out/$P/$T.mp4 -> conferir frase a frase antes de entregar"
