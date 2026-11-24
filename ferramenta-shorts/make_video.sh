#!/usr/bin/env bash
# usage: ./make_video.sh <id>   (videos/<id>/beats.json) -> out/<id>/<Titulo>.mp4
# Tudo automatico e RETOMAVEL: cada etapa grava um selo em stories/<id>/stages/ (apague o selo para refazer so' aquela etapa; apague stories/<id>/DONE para refazer tudo).
# Apos cada etapa o progresso e' salvo no git (ckpt.sh). O render e' feito em trechos de 150 quadros (render_pool.mjs) que tambem sao pontos de retomada.
# Codigos de saida: 0 pronto | 1 erro/gate reprovou | 75 pausado pela trava de seguranca (relance para continuar de onde parou)
set -e; cd "$(dirname "$0")"; ID="$1"; mkdir -p logs out/$ID stories/$ID/stages; L=logs/make_$ID.log
if [ -f stories/$ID/DONE ] && ! grep -q "^motor v13" stories/$ID/DONE; then rm -rf stories/$ID/DONE stories/$ID/stages stories/$ID/fit.js stories/$ID/STORYBOARD_OK stories/$ID/AGUARDA_STORYBOARD stories/$ID/ENTREGUE stories/$ID/AUTO_APROVADO stories/$ID/revisao_storyboard.md stories/$ID/storyboard.jpg stories/$ID/storyboard.hash stories/$ID/grade_acoes.jpg stories/$ID/SKIP ckpt/$ID; echo "$ID: marca de pronto de versao ANTIGA da ferramenta -> refazendo com a v13"; fi   # todo video e' refeito na v13 (ordem do Gibson)
[ -f stories/$ID/DONE ] && { echo "$ID ja pronto"; exit 0; }
# DISCO: com menos de 4 GB livres, apaga os quadros soltos dos videos JA PRONTOS (o mp4 e os trechos ficam; so' o refazer.sh por cena deixa de valer para eles -> use refazer_tudo.sh). Disco cheio derruba o render com "erro de pagina".
if [ "$(df -Pm . | awk 'NR==2{print $4}')" -lt 4000 ]; then for d in out/*/frames; do [ -d "$d" ] || continue; v=$(basename "$(dirname "$d")"); if [ "$v" != "$ID" ] && [ -f "stories/$v/DONE" ]; then rm -rf "$d"; fi; done; rm -rf /root/.cache/pip; echo "$(date +%T) disco baixo: quadros de videos prontos apagados ($(df -Ph . | awk 'NR==2{print $4}') livres)"; fi
log() { echo "$(date +%T) $*" | tee -a $L; }
st() { [ -f stories/$ID/stages/$1 ]; }; mark() { mkdir -p stories/$ID/stages; date +%s > stories/$ID/stages/$1; python3 cronograma.py $ID >/dev/null 2>&1 || true; bash ckpt.sh $ID "etapa $1" >/dev/null 2>&1 || true; }
j() { python3 -c "import json;print(json.load(open('stories/$ID/meta.json'))['$1'])"; }
python3 mkvideo.py $ID >> $L 2>&1
# FOLHA 4 (v13): pesquisa de campo automatica antes de tudo (busca cada item do roteiro na internet, baixa os prints e monta o quadro de referencias)
if [ ! -f referencias/$ID/pesquisa.json ]; then log "pesquisa de campo (folha 4)"; python3 pesquisar.py $ID >> $L 2>&1 || true; python3 mkvideo.py $ID >> $L 2>&1; fi
VOICE=$(j voice); RATE=$(j rate); T=$(j file)
if st voice && [ -f stories/$ID/voice.mp3 ] && [ ! -f stories/$ID/work/phrases.json ]; then log "refazendo so a temporizacao (work/ ausente)"; (cd stories/$ID && python3 ../../timing.py voice.mp3 script.txt --out work >> ../../$L 2>&1); fi
if ! st voice || [ ! -f stories/$ID/voice.mp3 ]; then log "voz"; rm -f stories/$ID/voice.mp3; ./produce_voice.sh $ID "$VOICE" "$RATE" >> $L 2>&1; mark voice; fi
if [ -f stories/$ID/VOICE_PLACEHOLDER ] && [ "${ALLOW_TEST_VOICE:-0}" != "1" ]; then log "PARADO: voz de TESTE (espeak, robotica). NAO se entrega video assim. Conserte a rede/certificado do edge-tts (veja OPERACAO.md) e apague stories/$ID/stages/voice e stories/$ID/voice.mp3"; rm -f stories/$ID/stages/voice; exit 3; fi
python3 mkvideo.py $ID >> $L 2>&1   # de novo, com a voz pronta: a folha 3 sai com o instante exato de cada acao
if ! python3 verificar_folhas.py $ID >> $L 2>&1; then log "BLOQUEADO: as 3 folhas nao foram lidas/seguidas (veja $L)"; tail -6 $L; exit 1; fi; log "3 folhas lidas e seguidas"
if ! st style; then log "estilo (autoajuste)"; python3 autostyle.py $ID >> $L 2>&1 || log "AVISO: estilo nao convergiu"; mark style; fi
if ! st fit; then log "enquadramento"; ./fit.sh $ID >> $L 2>&1; mark fit; fi
if ! st gate; then
  ./gate_all.sh $ID; G=logs/gate_$ID.txt
  if ! { grep -q "camera OK" $G && grep -q "ALL TAKES OK" $G && grep -q "STYLE OK" $G; }; then log "GATE FALHOU (veja $G)"; cat $G >> $L; exit 1; fi
  mark gate
fi
# STORYBOARD OBRIGATORIO (ordem do Gibson 19/11): antes do render completo, o video inteiro vira storyboard e ESPERA aprovacao (./aprovar_storyboard.sh <id>)
H3=$(python3 -c "import json;print(json.load(open('stories/$ID/folhas.json'))['hash_producao'])")
if [ "$(cat stories/$ID/STORYBOARD_OK 2>/dev/null)" != "$H3" ]; then
  if [ ! -f stories/$ID/storyboard.jpg ] || [ "$(cat stories/$ID/storyboard.hash 2>/dev/null)" != "$H3" ]; then log "storyboard (video inteiro, 1 quadro a cada ~1,5 s)"; ./prechecar.sh $ID >> $L 2>&1 && cp stories/$ID/precheck.jpg stories/$ID/storyboard.jpg && echo "$H3" > stories/$ID/storyboard.hash && { log "grade de acoes (1 quadro no instante de cada acao da folha 3)"; ./prechecar.sh $ID acoes >> $L 2>&1; }; fi
  touch stories/$ID/AGUARDA_STORYBOARD; log "AGUARDANDO APROVACAO DO STORYBOARD: abra stories/$ID/storyboard.jpg, confira com a folha 3 e rode ./aprovar_storyboard.sh $ID"; exit 76
fi
rm -f stories/$ID/AGUARDA_STORYBOARD
# trechos ja renderizados de OUTRA versao das folhas nao servem: apaga e renderiza de novo (nunca juntar quadro antigo no video novo)
# VERSAO DA FERRAMENTA (24/11, Gibson: "uma parte do video nao pode sair do jeito antigo e o resto do jeito novo"): o selo dos trechos junta a versao das folhas
# com a versao do motor. Se a ferramenta foi atualizada, os trechos ja renderizados sao descartados e o video e' renderizado INTEIRO na versao nova.
tv() { cat web/head.js web/core.js web/tail.js web/runtime.js web/acting.js web/vfx.js web/weather.js web/toonbase.js web/sets/*.js mkvideo.py audio_story.py 2>/dev/null | md5sum | cut -c1-10; }
TV0=$(tv); H3="$H3-$TV0"
if [ "$(cat ckpt/$ID/folha3.hash 2>/dev/null)" != "$H3" ]; then rm -rf ckpt/$ID out/$ID/frames; mkdir -p ckpt/$ID; echo "$H3" > ckpt/$ID/folha3.hash; log "trechos antigos descartados (versao nova das folhas)"; fi
./build3.sh $ID >/dev/null 2>&1; python3 verificar_folhas.py $ID --render >> $L 2>&1 || { log "BLOQUEADO: o render nao carrega a folha 3"; exit 1; }; N=$(python3 -c "import json;print(json.load(open('stories/$ID/work/phrases.json'))['frames30'])")
./snap.sh $ID $N >> $L 2>&1; (cd stories/$ID && python3 ../../caps.py >/dev/null)
log "render $N quadros (trechos de 150, retomavel)"
set +e; node render_pool.mjs $ID $N >> $L 2>&1; RC=$?; set -e; tail -3 $L
[ $RC -eq 75 ] && { log "PAUSADO pela trava de seguranca; relance run_queue.sh para continuar"; exit 75; }
[ $RC -ne 0 ] && { log "render incompleto (codigo $RC)"; exit 1; }
if [ "$(tv)" != "$TV0" ]; then log "a ferramenta foi atualizada DURANTE o render: descartando e refazendo o video inteiro na versao nova"; rm -rf ckpt/$ID out/$ID/frames stories/$ID/stages/fit stories/$ID/stages/gate stories/$ID/stages/style; exit 75; fi
./assemble.sh $ID "$T" >> $L 2>&1; ./review_video.sh out/$ID/$T.mp4 out/$ID/review | tee -a $L
echo "motor v13 $(date +%F_%T)" > stories/$ID/DONE; python3 cronograma.py $ID >/dev/null 2>&1 || true; bash ckpt.sh $ID "pronto" >/dev/null 2>&1 || true; log "PRONTO out/$ID/$T.mp4 (+ out/$ID/review_sheet.jpg)"
