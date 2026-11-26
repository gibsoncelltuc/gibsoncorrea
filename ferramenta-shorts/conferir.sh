#!/usr/bin/env bash
# usage: ./conferir.sh <id>   -> VERIFICACAO FINAL depois do render. Diz se o video pode ser entregue e junta o pacote em entregas/<id>/.
cd "$(dirname "$0")"; ID="${1:?uso: ./conferir.sh <id>}"; OK=1; say() { echo "$1"; }
[ -f stories/$ID/DONE ] || { say "NAO PRONTO: sem stories/$ID/DONE (bash status.sh; se houver stories/$ID/SKIP veja logs/gate_$ID.txt)"; exit 1; }
MP4=$(ls -t out/$ID/*.mp4 2>/dev/null | head -1); [ -n "$MP4" ] || { say "FALHA: sem mp4 em out/$ID"; exit 1; }
read W H D < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -show_entries format=duration -of csv=p=0 "$MP4" | tr ',\n' '  ')
[ "$W" = "1080" ] && [ "$H" = "1920" ] && say "ok  video 1080x1920, ${D%.*} s, $(du -h "$MP4" | cut -f1)" || { say "FALHA: resolucao $W x $H"; OK=0; }
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of csv=p=0 "$MP4" | grep -q . && say "ok  tem audio" || { say "FALHA: sem audio"; OK=0; }
TOT=$(grep -o "[0-9]*/[0-9]* quadros" logs/make_$ID.log | tail -1 | cut -d/ -f2 | cut -d' ' -f1); NEW=$(grep "fim:" logs/make_$ID.log | tail -1 | awk '{print $3+0}')
[ -n "$TOT" ] && say "ok  quadros novos na ultima rodada: $NEW de $TOT (se for MUITO menor que o total apos mudar a ferramenta, o render reaproveitou quadro velho: ./refazer_tudo.sh $ID)"
[ -f stories/$ID/riscos.txt ] || python3 mkvideo.py $ID >/dev/null 2>&1; R=$(cat stories/$ID/riscos.txt 2>/dev/null || echo "?"); [ "$R" = "0" ] && say "ok  folha 2 sem riscos" || { say "ATENCAO: $R risco(s) na folha 2"; OK=0; }
[ -f stories/$ID/VOICE_PLACEHOLDER ] && { say "FALHA: voz de TESTE (robotica). Refaca a voz: rm stories/$ID/stages/voice stories/$ID/voice.mp3 e ./refazer_tudo.sh $ID"; OK=0; } || say "ok  voz neural"
_mv=$(ls -t out/$ID/*.mp4 2>/dev/null | head -1); _dv=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$_mv" 2>/dev/null); _da=$(ffprobe -v error -show_entries format=duration -of csv=p=0 stories/$ID/voice.mp3 2>/dev/null); python3 -c "import sys;sys.exit(0 if float('${_dv:-0}') >= float('${_da:-0}') - 0.4 else 1)" && say "ok  video inteiro (${_dv}s, voz ${_da}s)" || { say "FALHA: video MAIS CURTO que a voz (${_dv}s x ${_da}s): faltou trecho (disco cheio?). Apague o seg incompleto em ckpt/$ID e o DONE; a fila refaz"; OK=0; }
[ -f out/$ID/review_sheet.jpg ] && say "ok  folha de contato: out/$ID/review_sheet.jpg  << ABRA E OLHE (Read) antes de entregar" || { say "FALHA: sem folha de contato"; OK=0; }
mkdir -p ../entregas/$ID; cp "$MP4" out/$ID/review_sheet.jpg stories/$ID/folha1_roteiro.md stories/$ID/folha2_producao.md ../entregas/$ID/ 2>/dev/null
say "pacote: entregas/$ID/ (mp4 original, folha de contato, folha 1, folha 2)"
say "OLHAR NA FOLHA DE CONTATO: objeto heroi aparece no comeco e em close | ninguem cortado | nenhuma cena vazia | texto nao cobre legenda | os 2 grandes momentos em plano aberto | rostos e poses mudam de cena para cena. Defeito critico: corrija o beats.json e ./refazer.sh $ID bN (ou ./refazer_tudo.sh $ID)."
[ $OK = 1 ] && say "RESULTADO: checagens automaticas OK - falta so' o seu olho na folha de contato" || say "RESULTADO: ha falha acima - corrija antes de entregar"
