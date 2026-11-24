#!/usr/bin/env bash
# usage: ./make_video.sh <id>   (videos/<id>/beats.json) -> out/<id>/<Titulo>.mp4
# Tudo automatico e RETOMAVEL: cada etapa grava um selo em stories/<id>/stages/ (apague o selo para refazer so' aquela etapa; apague stories/<id>/DONE para refazer tudo).
# Apos cada etapa o progresso e' salvo no git (ckpt.sh). O render e' feito em trechos de 150 quadros (render_pool.mjs) que tambem sao pontos de retomada.
# Codigos de saida: 0 pronto | 1 erro/gate reprovou | 75 pausado pela trava de seguranca (relance para continuar de onde parou)
set -e; cd "$(dirname "$0")"; ID="$1"; mkdir -p logs out/$ID stories/$ID/stages; L=logs/make_$ID.log
if [ -f stories/$ID/DONE ] && ! grep -q "^motor v13" stories/$ID/DONE; then rm -rf stories/$ID/DONE stories/$ID/stages stories/$ID/fit.js stories/$ID/STORYBOARD_OK stories/$ID/AGUARDA_STORYBOARD stories/$ID/ENTREGUE stories/$ID/AUTO_APROVADO stories/$ID/revisao_storyboard.md stories/$ID/storyboard.jpg stories/$ID/storyboard.hash stories/$ID/grade_acoes.jpg stories/$ID/SKIP ckpt/$ID; echo "$ID: marca de pronto de versao ANTIGA da ferramenta -> refazendo com a v13"; fi   # todo video e' refeito na v13 (ordem do Gibson)
[ -f stories/$ID/DONE ] && { echo "$ID ja pronto"; exit 0; }
# DISCO: com menos de 4 GB livres, apaga os quadros soltos dos videos JA PRONTOS (o mp4 e os trechos ficam; so' o refazer.sh por cena deixa de valer para eles -> use refazer_tudo.sh). Disco cheio derruba o render com "erro de pagina".
if [ "$(df -Pm . | awk 'NR==2{print $4}')" -lt 4000 ]; then for d in out/*/frames; do [ -d "$d" ] || continue; v=$(basename "$(dirname "$d")"); if [ "$v" != "$ID" ] && [ -f "stories/$v/DONE" ]; then rm -rf "$d"; fi; done; for d in ckpt/*; do v=$(basename "$d"); [ "$v" != "$ID" ] && [ -f "stories/$v/ENTREGUE" ] && rm -rf "$d"; done; rm -rf out/_tmp_* /tmp/claude-0/receb_* 2>/dev/null; rm -rf /root/.cache/pip; echo "$(date +%T) disco baixo (checkpoints de entregues tambem): quadros de videos prontos apagados ($(df -Ph . | awk 'NR==2{print $4}') livres)"; fi
log() { echo "$(date +%T) $*" | tee -a $L; }
st() { [ -f stories/$ID/stages/$1 ]; }; mark() { mkdir -p stories/$ID/stages; date +%s > stories/$ID/stages/$1; python3 cronograma.py $ID >/dev/null 2>&1 || true; bash ckpt.sh $ID "etapa $1" >/dev/null 2>&1 || true; }
j() { python3 -c "import json;print(json.load(open('stories/$ID/meta.json'))['$1'])"; }
[ -f stories/$ID/STORYBOARD_OK ] || [ "${AUTOVIS:-0}" -gt 0 ] || python3 suspeitas.py $ID --corrigir >> $L 2>&1 || true   # 24/11: frase x cena (animal citado sem animal, muita gente sem multidao) corrigido antes de montar
[ -f stories/$ID/STORYBOARD_OK ] || [ "${AUTOVIS:-0}" -gt 0 ] || python3 enquadrar.py $ID >> $L 2>&1 || true   # 24/11 ENQUADRAMENTO NA FONTE: a folha 2 descreve lugar/tamanho/camera de cada objeto e a cena e' montada com isso (storyboard ja aprovado nao e' mexido)
python3 mkvideo.py $ID >> $L 2>&1; python3 ficha_nas_folhas.py $ID >> $L 2>&1 || true
# FOLHA 4 (v13): pesquisa de campo automatica antes de tudo (busca cada item do roteiro na internet, baixa os prints e monta o quadro de referencias)
if [ ! -f referencias/$ID/pesquisa.json ]; then log "pesquisa de campo (folha 4)"; python3 pesquisar.py $ID >> $L 2>&1 || true; python3 mkvideo.py $ID >> $L 2>&1; python3 ficha_nas_folhas.py $ID >> $L 2>&1 || true; fi
VOICE=$(j voice); RATE=$(j rate); T=$(j file)
VH=$(python3 -c "import json,hashlib;B=json.load(open('videos/$ID/beats.json'));print(hashlib.md5(' '.join(b['say'] for b in B['beats']).encode()).hexdigest()[:12])")   # texto narrado mudou = voz nova (pendencia da sessao B: a voz antiga ia para o video)
if st voice && [ -f stories/$ID/stages/voice.hash ] && [ "$(cat stories/$ID/stages/voice.hash)" != "$VH" ]; then log "o texto do roteiro mudou: refazendo a voz"; rm -rf stories/$ID/stages/voice stories/$ID/voice.mp3 stories/$ID/work; fi
if st voice && [ ! -f stories/$ID/stages/voice.hash ] && [ -f stories/$ID/script_one.txt ] && ! python3 -c "
import json,re,sys;n=lambda t: re.sub(r'\W+',' ',t.lower()).strip()
B=json.load(open('videos/$ID/beats.json'));sys.exit(0 if n(' '.join(b['say'] for b in B['beats'])) in n(open('stories/$ID/script_one.txt').read()) else 1)"; then log "voz antiga com texto diferente do roteiro: refazendo a voz"; rm -rf stories/$ID/stages/voice stories/$ID/voice.mp3 stories/$ID/work; fi
st voice && [ ! -f stories/$ID/stages/voice.hash ] && echo "$VH" > stories/$ID/stages/voice.hash
if st voice && [ -f stories/$ID/voice.mp3 ] && [ ! -f stories/$ID/work/phrases.json ]; then log "refazendo so a temporizacao (work/ ausente)"; (cd stories/$ID && python3 ../../timing.py voice.mp3 script.txt --out work >> ../../$L 2>&1); fi
if ! st voice || [ ! -f stories/$ID/voice.mp3 ]; then log "voz"; rm -f stories/$ID/voice.mp3; ./produce_voice.sh $ID "$VOICE" "$RATE" >> $L 2>&1; mark voice; echo "$VH" > stories/$ID/stages/voice.hash; fi
if [ -f stories/$ID/VOICE_PLACEHOLDER ] && [ "${ALLOW_TEST_VOICE:-0}" != "1" ]; then log "PARADO: voz de TESTE (espeak, robotica). NAO se entrega video assim. Conserte a rede/certificado do edge-tts (veja OPERACAO.md) e apague stories/$ID/stages/voice e stories/$ID/voice.mp3"; rm -f stories/$ID/stages/voice; exit 3; fi
python3 mkvideo.py $ID >> $L 2>&1; python3 ficha_nas_folhas.py $ID >> $L 2>&1 || true   # de novo, com a voz pronta: a folha 3 sai com o instante exato de cada acao
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
  if [ ! -f stories/$ID/visibilidade.json ] || [ stories/$ID/visibilidade.json -ot stories/$ID/storyboard.jpg ]; then log "visibilidade (objeto citado aparece? algo tapando a camera? camera dentro de objeto?)"; ./build3.sh $ID >/dev/null 2>&1; node visivel.mjs $ID > stories/$ID/visibilidade.txt 2>&1 || true; cat stories/$ID/visibilidade.txt >> $L; fi
  if grep -q '^FALHA' stories/$ID/visibilidade.txt 2>/dev/null; then
    # AUTOCORRECAO (ordem do Gibson 24/11): a ferramenta conserta sozinha o enquadramento e gera o storyboard de novo (ate 3 voltas)
    if [ "${AUTOVIS:-0}" -lt 3 ] && python3 autocorrigir_visibilidade.py $ID >> $L 2>&1; then log "VISIBILIDADE: $(grep -c '^FALHA' stories/$ID/visibilidade.txt) falha(s) CORRIGIDA(S) SOZINHA(S) (stories/$ID/autocorrecoes.md) -> storyboard de novo"; rm -f stories/$ID/storyboard.jpg stories/$ID/storyboard.hash stories/$ID/visibilidade.json stories/$ID/visibilidade.txt; AUTOVIS=$(( ${AUTOVIS:-0} + 1 )) exec bash make_video.sh $ID; fi
    log "VISIBILIDADE: $(grep -c '^FALHA' stories/$ID/visibilidade.txt) falha(s) que a autocorrecao nao resolveu (stories/$ID/visibilidade.txt)"
  fi
  python3 lista_revisao.py $ID >> $L 2>&1 || true   # 24/11: lista UNICA com tudo o que a ferramenta achou + uma linha por frase (revisar tudo de uma vez)
  touch stories/$ID/AGUARDA_STORYBOARD; log "AGUARDANDO APROVACAO DO STORYBOARD: abra stories/$ID/storyboard.jpg, confira com a folha 3 e rode ./aprovar_storyboard.sh $ID"; exit 76
fi
rm -f stories/$ID/AGUARDA_STORYBOARD
# trechos ja renderizados de OUTRA versao das folhas nao servem: apaga e renderiza de novo (nunca juntar quadro antigo no video novo)
# VERSAO DA FERRAMENTA (24/11, Gibson: "uma parte do video nao pode sair do jeito antigo e o resto do jeito novo"): o selo dos trechos junta a versao das folhas
# com a versao do motor. Se a ferramenta foi atualizada, os trechos ja renderizados sao descartados e o video e' renderizado INTEIRO na versao nova.
tv() { cat web/head.js web/core.js web/tail.js web/runtime.js web/acting.js web/vfx.js web/weather.js web/toonbase.js web/sets/*.js mkvideo.py audio_story.py 2>/dev/null | md5sum | cut -c1-10; }
TV0=$(tv); H3="$H3-$TV0"
if [ "$(cat ckpt/$ID/folha3.hash 2>/dev/null)" != "$H3" ]; then
  # 24/11 (pedido do Gibson: "refazer so' o trecho com defeito e remontar"): compara a impressao digital de CADA CENA com a do ultimo render.
  # So' cenas mudaram (e o global igual: motor de desenho, voz, figurinos) -> apaga e refaz so' os trechos dessas cenas; o resto do video fica.
  mkdir -p ckpt/$ID; ./build3.sh $ID >/dev/null 2>&1; python3 cenas_hash.py $ID > ckpt/$ID/cenas_novo.txt 2>/dev/null || true
  if [ -f ckpt/$ID/cenas.txt ] && [ -s ckpt/$ID/cenas_novo.txt ] && [ "$(grep '^global ' ckpt/$ID/cenas.txt)" = "$(grep '^global ' ckpt/$ID/cenas_novo.txt)" ] && ls ckpt/$ID/seg_*.mp4 >/dev/null 2>&1; then
    MUD=$(python3 -c "
a=dict(l.split() for l in open('ckpt/$ID/cenas.txt') if l.strip()); b=dict(l.split() for l in open('ckpt/$ID/cenas_novo.txt') if l.strip())
print(' '.join(k for k in b if k != 'global' and a.get(k) != b[k]))")
    NQ=$(python3 -c "import json;print(json.load(open('stories/$ID/work/phrases.json'))['frames30'])")
    SEGS=""; [ -n "$MUD" ] && SEGS=$(node -e "
import('$PWD/web/story.js').then(m=>{const want=process.argv.slice(1);const S=m.SHOTS.filter(s=>want.includes(s.id.split('~')[0].split('_')[0]));const k=new Set();for(const s of S)for(let f=Math.max(0,s.a-10);f<=Math.min($NQ-1,s.b+10);f++)k.add(Math.floor(f/150));console.log([...k].sort((a,b)=>a-b).join(' '))})" $MUD)
    for k in $SEGS; do rm -f ckpt/$ID/seg_$(printf %03d $k).mp4; for f in $(seq $((k*150)) $((k*150+149))); do rm -f out/$ID/frames/f$(printf %04d $f).jpg; done; done
    echo "$H3" > ckpt/$ID/folha3.hash; log "so' estas cenas mudaram: ${MUD:-nenhuma} -> refazendo so' os trechos: ${SEGS:-nenhum} (o resto do video foi aproveitado)"
  else
    rm -rf ckpt/$ID out/$ID/frames; mkdir -p ckpt/$ID; echo "$H3" > ckpt/$ID/folha3.hash; log "trechos antigos descartados (mudou o que vale para o video inteiro: motor de desenho, voz ou figurinos)"
  fi
fi
./build3.sh $ID >/dev/null 2>&1; python3 verificar_folhas.py $ID --render >> $L 2>&1 || { log "BLOQUEADO: o render nao carrega a folha 3"; exit 1; }; N=$(python3 -c "import json;print(json.load(open('stories/$ID/work/phrases.json'))['frames30'])")
./snap.sh $ID $N >> $L 2>&1; (cd stories/$ID && python3 ../../caps.py >/dev/null)
log "render $N quadros (trechos de 150, retomavel)"
set +e; node render_pool.mjs $ID $N >> $L 2>&1; RC=$?; set -e; tail -3 $L
[ $RC -eq 75 ] && { log "PAUSADO pela trava de seguranca; relance run_queue.sh para continuar"; exit 75; }
[ $RC -ne 0 ] && { log "render incompleto (codigo $RC)"; exit 1; }
python3 cenas_hash.py $ID > ckpt/$ID/cenas.txt 2>/dev/null || true   # impressao digital das cenas deste render (para a proxima refacao ser so' dos trechos que mudarem)
# 24/11 (Melancia): disco cheio no meio do render deixou um trecho com 95 de 150 quadros e o video saiu 1,8 s mais curto que a voz.
# Confere cada trecho (150 quadros, o ultimo o resto) e refaz sozinho o que veio incompleto (ate 2 vezes).
for _volta in 1 2; do _ruins=$(python3 - "$ID" "$N" <<'PYS'
import sys, subprocess, glob, os
i, n = sys.argv[1], int(sys.argv[2]); out = []
for k in range((n + 149) // 150):
    f = f'ckpt/{i}/seg_{k:03d}.mp4'; esp = min(150, n - k * 150)
    if not os.path.exists(f): out.append(f); continue
    r = subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v', '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout.strip()
    if not r.isdigit() or int(r) < esp: out.append(f)
print(' '.join(out))
PYS
); [ -z "$_ruins" ] && break; log "trecho(s) incompleto(s) ($_ruins): apagando e renderizando de novo"; for _s in $_ruins; do rm -f "$_s"; _k=$((10#$(basename $_s .mp4 | sed 's/seg_//'))); for _q in $(seq $((_k*150)) $((_k*150+149))); do rm -f out/$ID/frames/f$(printf %04d $_q).jpg; done; done; bash limpar_disco.sh >> $L 2>&1; set +e; node render_pool.mjs $ID $N >> $L 2>&1; set -e; done
if [ "$(tv)" != "$TV0" ]; then log "a ferramenta foi atualizada DURANTE o render: na proxima rodada compara cena a cena e refaz so' o que mudou (motor de desenho mudou = video inteiro)"; rm -rf stories/$ID/stages/fit stories/$ID/stages/gate stories/$ID/stages/style; exit 75; fi
./assemble.sh $ID "$T" >> $L 2>&1; _dv=$(ffprobe -v error -show_entries format=duration -of csv=p=0 out/$ID/$T.mp4 2>/dev/null); _da=$(ffprobe -v error -show_entries format=duration -of csv=p=0 stories/$ID/voice.mp3 2>/dev/null); python3 -c "import sys;sys.exit(0 if float('${_dv:-0}') >= float('${_da:-0}') - 0.4 else 1)" || { log "VIDEO MAIS CURTO QUE A VOZ (${_dv}s x ${_da}s): falta trecho; refazendo"; rm -f out/$ID/$T.mp4; exit 1; }; ./review_video.sh out/$ID/$T.mp4 out/$ID/review | tee -a $L
echo "motor v13 $(date +%F_%T)" > stories/$ID/DONE; python3 cronograma.py $ID >/dev/null 2>&1 || true; bash ckpt.sh $ID "pronto" >/dev/null 2>&1 || true; log "PRONTO out/$ID/$T.mp4 (+ out/$ID/review_sheet.jpg)"
