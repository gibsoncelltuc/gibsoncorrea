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
ls web/assets/library/kit/rg_franca_1.glb web/assets/library/kit/room_azul_wood.glb >/dev/null 2>&1 || f "kit de cidades por regiao/salas coloridas sumiu"
grep -q "keepFam" web/acting.js || f "rosto do roteiro nao esta protegido (keepFam)"
grep -q '"snarl"' web/toonbase.js && grep -q 'expr === "cry"' web/toonbase.js || f "raiva/choro sem desenho proprio"
[ -n "$T" ] && rm -rf "videos/$T" "stories/$T"
# ---- v13: cenario limpo, cena de explicacao, objeto como sujeito, epoca ----
V=_v13_$$; mkdir -p "videos/$V"
cat > "videos/$V/beats.json" <<'V13'
{"voice":"pt-BR-AntonioNeural","rate":"+10%","serie":"Teste","ep":98,"title":"teste v13 2026","ano":2026,"set":"outback","heroi":"kit/roadster26","cta":false,"outfits":{"MUS":{"jacket":"#4a505c","hat":"hair"},"ENG":{"jacket":"#1f3f6a","hat":"cap"}},"beats":[{"who":["MUS:0:grin","ENG:0:surprised"],"say":"A empresa mostrou um carro que sai do chão diante de todos.","props":[["kit/roadster26",0,-4.0,1.0]],"mapa":"ESTADOS UNIDOS"},{"say":"O segredo são propulsores de ar comprimido escondidos embaixo do carro, que empurram ele para cima.","explica":{"raiox":"escondidos","vfx":[{"k":"jato","na":"empurram"}],"rotulos":[["PROPULSORES","baixo","propulsores"]],"setas":[["cima","EMPUXO"]],"medidor":{"de":0,"para":100,"un":"km/h","na":"cima"}}},{"who":["MUS:0:laugh"],"say":"Diante dos convidados, o carro decolou e voou por cima da pista.","props":[["kit/roadster26",0,-4.0,1.0]]},{"who":["ENG:0:smile","MUS:0:grin"],"interior":"galpao","say":"Os engenheiros conversaram sobre o motor elétrico que funciona com bateria nova."}]}
V13
python3 mkvideo.py $V > /dev/null 2>&1 || f "v13: mkvideo nao rodou no roteiro de teste"
S=stories/$V/spec.js
grep -q 'sets: \[[^]]*"outback"' $S && f "v13: historia de 2026 ficou no cenario de fazenda (outback)"
grep -q 'loc_estudio' $S || f "v13: cena de explicacao nao foi para o estudio"
{ grep -q "k: 'rotulo'" $S && grep -q "k: 'seta'" $S && grep -q 'k: "medidor"' $S && grep -q "xray:" $S; } || f "v13: cena de explicacao sem rotulo/seta/medidor/raio-X"
{ grep -q "k: 'jato'" $S && grep -q "camFollow" $S && grep -q "k: 'onda'" $S; } || f "v13: voo do carro sem jato/onda/camera seguindo"
grep -q 'mk/Barrel\|mk/Crate_Wooden' $S && f "v13: barril/caixote em cena de 2026"
grep -q 'EXPLICATIVA' stories/$V/folha2_producao.md || f "v13: frase explicativa sem explica nao foi bloqueada"
python3 -c "import json,sys;o=json.load(open('stories/$V/orquestracao.json'));c=[x['classe'] for x in o['cenas']];sys.exit(0 if c[1]=='explicativa' and c[2]=='chave' and o['metricas']['cenario_e_epoca_ok']==100 else 1)" || f "v13: triagem das frases errada"
{ [ -f referencias/$V/DOSSIE.json ] && [ -f referencias/$V/FICHA.md ]; } || f "v13: dossie nao foi gravado"
node --check web/vfx.js 2>/dev/null || f "sintaxe web/vfx.js"
grep -q "vfx.js" build3.sh || f "v13: vfx.js fora do build"
# ---- v13b: tamanho real, folha 4, herois, carro correndo no medidor, queda ----
grep -q 'asset: "kit/roadster26", at: \[X + 0, -4.0\], s: 1.3' $S || f "v13: carro fora do tamanho real (deveria ter ~6 unidades)"
{ [ -f stories/$V/folha4_pesquisa.md ] && [ -f referencias/$V/plano_pesquisa.json ] && grep -q 'HEROIS' stories/$V/folha4_pesquisa.md; } || f "v13: folha 4 (pesquisa) nao foi gerada"
python3 - "$V" <<'V13B' || f "v13: medidor de km/h nao poe o carro correndo com propulsor traseiro"
import json, sys, re, subprocess
v = sys.argv[1]; p = f'videos/{v}/beats.json'; B = json.load(open(p, encoding='utf-8'))
B['beats'][1] = {"say": "Segundo a empresa, o carro vai de zero a cem em menos de um segundo.", "explica": {"medidor": {"de": 0, "para": 100, "un": "km/h", "na": "zero"}}}
B['beats'][3] = {"who": ["ENG:0:angry", "MUS:0:surprised"], "say": "O engenheiro empurrou o chefe e ele caiu no chão diante de todos."}
B['beats'][2] = {"who": ["MUS:0:grin", "ENG:0:surprised"], "say": "Depois disso, os assassinatos despencaram no pais inteiro."}
B['beats'][0] = {"who": ["MUS:0:grin", "ENG:0:surprised"], "say": "Diante de convidados, o carro dele saiu do chão.", "obj_acao": False}
json.dump(B, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
subprocess.run([sys.executable, 'mkvideo.py', v], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
s = open(f'stories/{v}/spec.js', encoding='utf-8').read()
pl = [l for l in open(f'stories/{v}/plano.md', encoding='utf-8') if l.startswith('b0 ')]
p3 = [l for l in open(f'stories/{v}/plano.md', encoding='utf-8') if l.startswith('b2 ')]
if p3 and 'tomba @' in p3[0]: sys.exit(1)   # "os assassinatos despencaram" = grafico, ninguem cai
if not pl or 'sai @' in pl[0] or 'tomba @' in pl[0]: sys.exit(1)   # "saiu do chao" = decolou: ninguem sai andando nem cai
ok = "dir: \"tras\"" in s and "k: \"velocidade\"" in s and 'camFollow' in s and "'fall'" in s
sys.exit(0 if ok else 1)
V13B
grep -q "L_.y += 0.3 \* L_.s" web/runtime.js || f "v13: queda sem a correcao do corpo dentro do chao"
[ -n "$V" ] && rm -rf "videos/$V" "stories/$V" "referencias/$V"
# ---- v13c: navio da epoca, batalhao, sem clone, sem cidade no campo, cronograma ----
G=_v13g_$$; mkdir -p "videos/$G"
cat > "videos/$G/beats.json" <<'V13G'
{"voice":"pt-BR-AntonioNeural","rate":"+10%","serie":"Teste","ep":97,"title":"teste guerra 1859","ano":1859,"set":"countryside","cta":false,"outfits":{"FAZ":{"jacket":"#7a9ac2","hat":"straw"},"IRL":{"jacket":"#5d7a3a","hat":"bowler"},"ING":{"jacket":"#c0262d","hat":"shako","rifle":true},"AME":{"jacket":"#27408b","hat":"kepi","rifle":true}},"beats":[{"who":["FAZ:0:shock","IRL:0:angry"],"say":"Na ilha, o fazendeiro brigou com o vizinho por causa de um porco.","mapa":"ILHA"},{"who":["FAZ:0:neutral","IRL:0:neutral"],"say":"Era uma ilha pequena de fazendas e hortas, longe de tudo."},{"who":["FAZ:0:angry"],"say":"O fazendeiro olhou a horta destruída e ficou furioso."},{"who":["IRL:0:shout","FAZ:0:surprised"],"say":"O vizinho exigiu dinheiro e ninguém cedeu naquele dia."},{"shot":"crowd","who":["ING:0:stern","AME:0:stern"],"batalha":true,"tiros":false,"crowd":{"n":10,"outfits":["ING","AME"],"march":false},"set":"harbor","say":"Os dois países mandaram soldados, navios de guerra e canhões para a ilha."},{"who":["FAZ:0:sad"],"say":"No fim a única baixa da guerra foi o porco."}]}
V13G
python3 mkvideo.py $G > /dev/null 2>&1 || f "v13: mkvideo nao rodou no roteiro de guerra de teste"
SG=stories/$G/spec.js
grep -q 'navio_fragata' $SG || f "v13: historia de 1859 sem a fragata da epoca"
grep -q 'sets: \[[^]]*"street"' $SG && f "v13: historia rural ganhou rua de cidade"
grep -q 'rg_eua' $SG && f "v13: predio de cidade da regiao em historia rural"
[ "$(grep -o 'pp(X_harbor, "ING"\|pp(X_harbor, "AME"' $SG | wc -l)" -ge 40 ] || f "v13: batalhao pequeno (menos de 40 soldados no plano aberto)"
python3 -c "import json,sys;o=json.load(open('stories/$G/orquestracao.json'));sys.exit(0 if o['cenas'][1]['multidao'] in (0, None) and o['cenas'][4]['multidao']>=40 else 1)" || f "v13: multidao clonou personagem ou batalhao pequeno"
grep -q 'voando' stories/$G/plano.md && f "v13: soldado voando em guerra sem tiro"
{ [ -f stories/$G/cronograma.md ] && grep -q 'Etapa atual' stories/$G/cronograma.md; } || f "v13: cronograma nao foi gerado"
[ -n "$G" ] && rm -rf "videos/$G" "stories/$G" "referencias/$G"
# ---- filas: nenhum roteiro em duas filas (duas sessoes fazendo o mesmo video), nem roteiro sem arquivo ----
D=$(cat fila_principal.txt fila_sessao_A.txt fila_sessao_B.txt | grep -v '^#' | awk 'NF{print $1}' | sort | uniq -d | tr '\n' ' '); [ -z "$D" ] || f "roteiro em mais de uma fila (video duplicado): $D"
for i in $(cat fila_principal.txt fila_sessao_A.txt fila_sessao_B.txt | grep -v '^#' | awk 'NF{print $1}'); do [ -f videos/$i/beats.json ] || f "fila aponta para roteiro que nao existe: $i"; done
# ---- marca de pronto: so' vale a da v13 (DONE vazio de versao antiga = refazer) ----
grep -q 'grep -q "^motor v13" stories/$id/DONE' run_queue.sh && grep -q 'echo "motor v13' make_video.sh || f "DONE antigo faria a fila pular video que precisa ser refeito na v13"
[ $ok = 0 ] && echo "TESTE DA FERRAMENTA: OK" || { echo "TESTE DA FERRAMENTA: FALHOU"; exit 1; }
