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
B['beats'].insert(4, {"who": ["MUS:0:grin", "ENG:0:surprised"], "say": "Eles deixaram uma garrafa de aguardente na mesa."})
B['beats'][0] = {"who": ["MUS:0:grin", "ENG:0:surprised"], "say": "Diante de convidados, o carro dele saiu do chão.", "obj_acao": False}
json.dump(B, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
subprocess.run([sys.executable, 'mkvideo.py', v], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
s = open(f'stories/{v}/spec.js', encoding='utf-8').read()
pl = [l for l in open(f'stories/{v}/plano.md', encoding='utf-8') if l.startswith('b0 ')]
p3 = [l for l in open(f'stories/{v}/plano.md', encoding='utf-8') if l.startswith('b2 ')]
if p3 and 'tomba @' in p3[0]: sys.exit(1)
if 'asset: "barrel"' in s: sys.exit(1)   # barril de madeira em 2026 (aguardente) = fora de epoca   # "os assassinatos despencaram" = grafico, ninguem cai
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
grep -qF 'kit/prison$|presidio' mkvideo.py || f "prisao/muralha grande sem tamanho real"
grep -q 'texto do roteiro mudou: refazendo a voz' make_video.sh || f "voz nao e' refeita quando o texto do roteiro muda"
python3 - <<'NEG' || f "negacao ('ninguem morreu em combate') vira batalha"
import re
s = open('mkvideo.py').read()
m = re.search(r"_s = re\.sub\(r'(.+?)', ' ', _s\)", s)
sys_ok = m and re.sub(m.group(1), ' ', 'quase houve guerra e ninguem morreu em combate').find('combate') < 0
raise SystemExit(0 if sys_ok else 1)
NEG
grep -q "('nature/lamppost', 1800, 'tools/lantern')" mkvideo.py && grep -q "int(_ano.group(1)) < 1500: REGIAO = None" mkvideo.py || f "cenario medieval com poste de rua, cerca branca ou predio europeu de 4 andares"
grep -q 'k === "axe"' web/toonbase.js && grep -q "('axe', r'machado" mkvideo.py || f "lenhador sem machado na mao"
grep -q "K === 'feixe'" web/vfx.js && grep -q "asset == 'kit/searchlight' and 'vfx' not in ex" mkvideo.py || f "holofote a noite sem facho de luz no ceu"
grep -q "fila_sessao_B.txt" boot.sh && grep -q "grep -qx \"\$id\" fila_sessao_B.txt" run_queue.sh || f "sessao pode pegar a fila de outra sessao (video duplicado)"
grep -q "b.get('animais') is False or (b.get('montado')" mkvideo.py && grep -q "ERA_ANO < 1800" web/sets/mountain.js && grep -q "persons_out\[:1\] or list(B.get('outfits'" mkvideo.py && grep -q 'o video sairia sem EP no titulo' mkvideo.py || f "lote 24/11: animal servido como comida, castelo no morro moderno, ator X, serie sem EP"
grep -q "sem VIRADA no meio do video" mkvideo.py && grep -q "GANCHO longo" mkvideo.py || f "roteiro sem checagem de estrutura de retencao (gancho, virada, final)"
# ---- cena de batalha em 3 cameras + "a cavalo": codigo da cena tem que sair valido ----
node -e "const vm=require('vm');const s=require('fs').readFileSync('stories/texel1795/spec.js','utf8').replace(/^export /mg,'').replace(/^import .*\$/mg,'');new vm.Script('(function(){'+s+'\\n})')" 2>/dev/null || f "cena de batalha a cavalo gera codigo invalido (Texel b9)"
grep -q "and not _multi:" mkvideo.py || f "montado embrulha sequencia de cameras (erro de sintaxe)"
grep -q "cen == 'arctic' and re.search(r'congel|gelo', t)" mkvideo.py || f "mar congelado no artico acusado como cenario sem agua"
grep -q 'GANCHO sem impacto visual nos 5 primeiros segundos' mkvideo.py || f "cena 1 sem checagem de impacto visual (5 primeiros segundos)"
grep -q 'revisao_final.sh \$ID ||' enviar_para_principal.sh || f "sessao pode enviar video sem revisao final frase a frase"
grep -q 'node visivel.mjs' make_video.sh && grep -q 'VISIBILIDADE REPROVADA' aprovar_storyboard.sh && grep -q '__propPool' build3.sh || f "storyboard pode ser aprovado sem medir se o objeto citado aparece (causa raiz do retrabalho de 24/11)"
grep -q "if (globalThis.FAROL) libInst(.buildings/lighthouse" web/sets/harbor.js || f "farol do cais perto da camera (dominava o quadro no Kiska e no Bolos)"
grep -q 'conserto DESFEITO' autocorrigir_visibilidade.py && grep -q 'um personagem a menos' autocorrigir_visibilidade.py || f "autocorrecao pode esvaziar cena de acao ou criar risco novo"
grep -q "for b_ in beats) + 13) / 2.8" mkvideo.py || f "estimativa de duracao otimista (video saia com 53 s)"
grep -q "'harbor': \['buildings/shop', 'buildings/lighthouse'\]" mkvideo.py && f "farol entra como fachada no cais (tapava o quadro)"
grep -q 'OBJETO HEROI: no vao ENTRE os personagens' mkvideo.py || f "objeto heroi empurrado para fora do quadro pela regra nada-na-frente"
grep -q '_fixa_nome' mkvideo.py || f "veiculo sem pasta (locomotive) trava o carregamento do video"
grep -q 'cobrindo a tela' visivel.mjs && grep -q 'cobrindo a tela' autocorrigir_visibilidade.py || f "objeto grande cobrindo a tela (parede/casco) passa sem checagem"
T_=videos/_teste_coer; mkdir -p $T_; printf '{"regiao":"brasil","outfits":{"A":{"jacket":"#111"},"B":{"jacket":"#111"}},"beats":[{"say":"Segundo uma versao, tudo comecou assim.","mapa":"PERNAMBUCO"},{"say":"Eles brigaram.","batalha":true,"crowd":{"outfits":["A","B"]}}]}' > $T_/beats.json
_co=$(python3 checagem_coerencia.py _teste_coer 2>&1); for r_ in R1 R2 R3 R4; do echo "$_co" | grep -q "$r_ " || f "coerencia nao pega a regra $r_ (lugar/regiao/fardas/gancho)"; done; rm -rf $T_
grep -q 'R5 b' checagem_coerencia.py || f "coerencia nao confere a farda FINAL (depois da farda automatica da epoca)"
grep -q 'checagem_coerencia.py' verificar_folhas.py || f "verificar_folhas nao roda a checagem de coerencia"
grep -q 'python3 enquadrar.py' make_video.sh && grep -q 'FICHA DE CENA' enquadrar.py && grep -q 'a ficha de cena planejou' visivel.mjs || f "folha 2 sem enquadramento na fonte (objeto jogado na cena sem lugar/tamanho/camera)"
grep -q 'ficha_nas_folhas.py' make_video.sh && grep -q 'FISICA E MOVIMENTO' ficha_nas_folhas.py && grep -q 'lista_revisao.py' make_video.sh && grep -q 'refacoes.txt' refazer.sh || f "folhas sem ficha tecnica/takes/fisica ou revisao sem lista unica"
grep -q "B\['max_wide'\] = _nw" enquadrar.py || f "ficha de cena pode ser desobedecida pelo limite de planos abertos"
grep -q "globalThis.FAZENDA" mkvideo.py && grep -q "globalThis.FAZENDA" web/sets/outback.js || f "outback desenha celeiro e moinho holandes em qualquer historia"
python3 -c "import re,sys;s=open('mkvideo.py').read();r=re.search(r\"_CAVW = re.compile\\(r'(.+?)'\\)\",s).group(1);sys.exit(1 if re.search(r,'uma metralhadora montada em caminhao') else 0)" || f "'montada em caminhao' vira cavalaria"
grep -q "_tropa = False   # 24/11" mkvideo.py || f "soldado com fuzil vira batalha mesmo com crowd n 0"
grep -q "R7 b" checagem_coerencia.py || f "cenario palace (praia) passa sem praia na historia"
T_=videos/_teste_r8; mkdir -p $T_; printf '{"outfits":{"GAU":{"jacket":"#111"},"MAN":{"jacket":"#eee"}},"beats":[{"say":"O barulho acordou o soldado Marco Manlio.","who":["GAU:0:scared"]}]}' > $T_/beats.json
python3 checagem_coerencia.py _teste_r8 2>&1 | grep -q "R8 b0" || f "personagem citado pelo nome (Marco Manlio) pode faltar na cena (Gansos b6)"; rm -rf $T_
grep -q "want.includes(nm))) R.parede" visivel.mjs || f "predio citado colado na camera vira parede sem checagem (Gansos b4)"
grep -q "animal citado aparece pequeno demais" visivel.mjs && grep -q "'animal citado' in txt" autocorrigir_visibilidade.py || f "animal citado minusculo no fundo passa sem checagem (Gansos b9)"
T_=videos/_teste_r3b; mkdir -p $T_; printf '{"outfits":{"MAR":{"jacket":"#123"}},"beats":[{"say":"Marinheiros dos dois lados se encararam no mar.","who":["MAR:0:stern","MAR:1:angry"]}]}' > $T_/beats.json
python3 checagem_coerencia.py _teste_r3b 2>&1 | grep -q "R3 b0" || f "dois lados com o mesmo figurino passa sem checagem (Lagosta b6)"; rm -rf $T_
grep -q "a.i >= nWho" visivel.mjs || f "figurante de multidao na borda trava o storyboard como personagem cortado"
grep -q "if not _gente: cena\['crowd'\]" enquadrar.py || f "ficha de cena tira a multidao de 'cercaram o forte' (Banquinho b5)"
grep -q "chov.w\* dentro|goteira|teto furado" mkvideo.py || f "chovia dentro do galpao sai sem chuva (Curie b3)"
grep -q "def ingles(q)" pesquisar.py && grep -q "qs += \[ingles(q)" pesquisar.py || f "pesquisa visual so' busca em portugues (Goodyear/Abelhas travaram sem referencia)"
grep -q "personagem PONTINHO" visivel.mjs && grep -q "'PONTINHO' in txt" autocorrigir_visibilidade.py && grep -q "if n_p and d > 22.0" enquadrar.py || f "personagem vira pontinho com objeto grande (camera a 80 m, Gansos b4)"
grep -q "v.length < 0.13)" visivel.mjs || f "animal citado pequeno passa com 10% da tela (Gansos b9)"
grep -q "_hit_fx" mkvideo.py && grep -q "_can_fx" mkvideo.py || f "clarao do tiro sai nos personagens e nao no canhao/objeto atingido (Chaleira b5/b6)"
grep -q 'stories/$v/ENTREGUE" ] && rm -rf "$d"' make_video.sh || f "disco enche com checkpoints de videos ja entregues (Lagosta falhou na montagem 24/11)"
grep -q 'videos_prontos/_a_conferir/"' receber_das_sessoes.sh && [ -x aprovar_entrega.sh ] || f "video de sessao entra direto na pasta da serie sem conferencia (mistura de versoes 24/11)"
[ -x limpar_disco.sh ] && grep -q "limpar_disco.sh" vigia.sh || f "disco cheio para a fila sem limpeza automatica"
grep -q "VIDEO MAIS CURTO QUE A VOZ" make_video.sh && grep -q "video MAIS CURTO que a voz" conferir.sh && grep -q "trecho(s) incompleto(s)" make_video.sh || f "trecho incompleto (disco cheio) passa e o video sai mais curto que a voz (Melancia 24/11)"
python3 cenas_hash.py lagosta1961 | grep -q "^b7 " && grep -q "so' estas cenas mudaram" make_video.sh && grep -q "cenas_hash.py \$ID > ckpt/\$ID/cenas.txt" refazer.sh || f "mudanca numa cena joga fora o video inteiro (devia refazer so' os trechos dela)"
grep -q "o tiro NUNCA VEIO" mkvideo.py || f "'o tiro nunca veio' ganha explosao (Lagosta f14)"
grep -q "Tulipas): 'o preco de uma casa inteira'" mkvideo.py || f "'o preco de uma casa' joga a cena para dentro de casa (Tulipas gancho)"
T_=videos/_teste_r9; mkdir -p $T_; printf '{"outfits":{},"beats":[{"say":"Foi em Siracusa, ha mais de dois mil anos."}]}' > $T_/beats.json
python3 checagem_coerencia.py _teste_r9 2>&1 | grep -q "R9 " || f "historia antiga sem regiao classico sai com cidade moderna (Arquimedes)"; rm -rf $T_
grep -q "Emus): 'pediram metralhadoras'" mkvideo.py || f "'pediram metralhadoras' vira tiro dentro do gabinete (Emus b2)"
grep -q "america\\\\b(?! (central|latina|do sul))" mkvideo.py || f "mapa AMERICA CENTRAL vira regiao eua (predios de Nova York em Honduras, Futebol)"
grep -q "objeto ENORME" visivel.mjs && grep -q "'objeto ENORME' in txt" autocorrigir_visibilidade.py || f "objeto pequeno gigante cobrindo o quadro passa sem checagem (bola do Futebol)"
grep -q "sem tropa/multidao a grua termina a 34 m" mkvideo.py || f "sequencia de grua em cena sem multidao deixa os personagens minusculos (Emus b4, Danca b6)"
grep -q "no maximo 2,0x mais longe" fit_fast.mjs || f "ajuste de camera afasta sem limite (Tulipas gancho a 2,47x)"
grep -q "etiqueta|papel|papeis|carta|nome|ficha" mkvideo.py || f "'misturou as etiquetas' vira panela de cozinha (Darwin gancho)"
grep -q "NAVIO NO CAIS = navio em cima do concreto" mkvideo.py || f "navio posto em cima do cais de concreto no harbor (Zanzibar)"
python3 -c "
import sentido as S
ok = ('tiro' in S.explicar('Mas o tiro nunca veio.')[0] and S.cena('Agricultores pediram metralhadoras.').get('sem_violencia') and S.cena('Um cientista misturou as etiquetas.').get('nao_cozinha') and S.cena('Uma flor custou o preco de uma casa inteira.').get('nao_interior') and S.cena('quase entraram em guerra').get('sem_violencia') and not S.cena('os navios abriram fogo e bombardearam o palacio').get('sem_violencia') and not S.cena('catorze bombas cairam sobre Fordow').get('sem_violencia'))
raise SystemExit(0 if ok else 1)" || f "sentido.py nao entende negacao/figurado/hipotese/valor (o tiro nunca veio, pediram metralhadoras, misturou etiquetas, preco de uma casa)"
grep -q "_neg_idx_base(say) | _SENT.figurado(say)" mkvideo.py && grep -q "_SENT.cena(_b.get('say', ''))" mkvideo.py || f "mkvideo nao usa o sentido da frase"
grep -q "suspeitas.py \$ID --corrigir" make_video.sh && grep -q "suspeitas.py" lista_revisao.py || f "fila sem a conferencia automatica frase x cena (suspeitas.py)"
grep -q "voz antiga: o texto mudou" mkvideo.py || f "duracao medida na voz de um texto antigo (roteiro encurtado continua acusando video longo)"
grep -q "_negm" suspeitas.py || f "suspeitas acusa multidao em frase negada (nao foram pessoas)"
grep -q "_NAV_PROPRIO" mkvideo.py || f "navio padrao do porto aparece junto com o navio da historia (Zanzibar)"
# ---- marca de pronto: so' vale a da v13 (DONE vazio de versao antiga = refazer) ----
grep -q 'grep -q "^motor v13" stories/$id/DONE' run_queue.sh && grep -q 'echo "motor v13' make_video.sh || f "DONE antigo faria a fila pular video que precisa ser refeito na v13"
[ $ok = 0 ] && echo "TESTE DA FERRAMENTA: OK" || { echo "TESTE DA FERRAMENTA: FALHOU"; exit 1; }
