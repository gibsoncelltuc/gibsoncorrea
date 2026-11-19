#!/usr/bin/env bash
# TESTE RAPIDO DA FERRAMENTA (npm test): sintaxe do motor, biblioteca 3D consistente e regras do diretor. Nao renderiza nada.
cd "$(dirname "$0")"; ok=0; f() { echo "FALHOU: $1"; ok=1; }
for j in web/runtime.js web/toonbase.js web/acting.js web/tail.js stories/_h.js; do node --check "$j" 2>/dev/null || f "sintaxe $j"; done
python3 -m py_compile mkvideo.py capacidades.py || f "sintaxe python"
bash -n run_queue.sh make_video.sh novo_video.sh conferir.sh prechecar.sh refazer.sh refazer_tudo.sh || f "sintaxe bash"
python3 - <<'EOF' || f "biblioteca 3D: palavra aponta para modelo que nao existe"
import json, glob, os, re, sys
bad = [(f_, e[1]) for f_ in glob.glob('obj_dict.d/*.json') for e in json.load(open(f_)) if not os.path.exists(f'web/assets/library/{e[1]}.glb')]
for e in json.load(open('obj_dict.d/principal.json')): re.compile(e[0])
print('modelos faltando:', bad) if bad else None; sys.exit(1 if bad else 0)
EOF
T=_teste_$$; mkdir -p videos/$T
cat > videos/$T/beats.json <<'EOF'
{"voice":"pt-BR-AntonioNeural","rate":"+10%","serie":"Curiosidade e Ciência","ep":99,"title":"teste","set":"countryside","heroi":"kit/kettle",
 "outfits":{"REI":{"profissao":"rei"},"TRU":{"jacket":"#1f2f5c","hat":"hair","hair":"#f2c84a","pele":"#f5c49a"},"ANA":{"jacket":"#7a3a6a","hat":"hair","hairStyle":"bun"},"POV":{"jacket":"#3f6fb5","hats":["cap","straw"]}},
 "beats":[{"shot":"two","who":["REI:0:smile","TRU:0:grin"],"props":[["kit/kettle",0,-1.4,1.0]],"say":"O cachorro e a vaca olhavam a chaleira do rei."},
  {"shot":"two","who":["ANA:0:smile"],"hora":"noite","say":"Numa noite gelada, ela acendeu a lareira."},
  {"shot":"two","who":["TRU:0:smile","ANA:0:grin"],"say":"No dia seguinte, todos acordaram cedo e conversaram na praça."}]}
EOF
python3 mkvideo.py $T > /dev/null 2>&1 || f "mkvideo nao rodou no roteiro de teste"
S=stories/$T/spec.js
grep -q '"dog"' $S && grep -q '"cow"' $S || f "animal citado nao entrou sozinho"
grep -o 'TRU: (v = 0[^;]*' $S | grep -q '&& true) ? { beard' && f "famoso (pele) ganhou barba sorteada"
grep -o 'ANA: (v = 0[^;]*' $S | grep -q '&& true) ? { beard' && f "mulher (coque) ganhou barba sorteada"
grep -o "S('b2'[^;]*" $S | grep -q '"night"' && f "noite da cena b1 vazou para b2"
node -e "import('./web/animals2d.js').catch(()=>0)" 2>/dev/null; for a in wolf fox deer rabbit lion elephant; do grep -q "  $a: " web/toon.js || f "animal $a sem desenho 2D (trava o render)"; done
grep -q "keepFam" web/acting.js || f "rosto do roteiro nao esta protegido (keepFam)"
grep -q '"snarl"' web/toonbase.js && grep -q 'expr === "cry"' web/toonbase.js || f "raiva/choro sem desenho proprio"
rm -rf videos/$T stories/$T
[ $ok = 0 ] && echo "TESTE DA FERRAMENTA: OK" || { echo "TESTE DA FERRAMENTA: FALHOU"; exit 1; }
