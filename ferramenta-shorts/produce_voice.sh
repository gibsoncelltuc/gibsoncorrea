#!/usr/bin/env bash
# usage: ./produce_voice.sh <id> [voice] [rate]   -> stories/<id>/voice.mp3 + work/{words,phrases}.json
# Tenta edge-tts (voz neural PT-BR). Se a rede bloquear (nuvem), cai para espeak-ng = VOZ DE TESTE (marca stories/<id>/VOICE_PLACEHOLDER).
set -e; cd "$(dirname "$0")/stories/$1"; VOICE="${2:-en-US-GuyNeural}"; RATE="${3:-+8%}"
tr '\n' ' ' < script.txt | sed 's/  */ /g' > script_one.txt
rm -f voice.mp3.part VOICE_PLACEHOLDER
TTS() { timeout 120 edge-tts ${HTTPS_PROXY:+--proxy "$HTTPS_PROXY"} --voice "$VOICE" --rate="$RATE" --file script_one.txt --write-media voice.mp3.part 2>/dev/null && [ -s voice.mp3.part ]; }
# 3 tentativas; na 2a em diante usa a CA do proxy da nuvem (em algumas maquinas o edge-tts falha por certificado e caia calado na voz de teste)
if TTS || { sleep 3; [ -f /root/.ccr/ca-bundle.crt ] && export SSL_CERT_FILE=/root/.ccr/ca-bundle.crt REQUESTS_CA_BUNDLE=/root/.ccr/ca-bundle.crt; TTS; } || { sleep 8; TTS; }; then
  :
else
  echo "AVISO: edge-tts indisponivel; usando espeak-ng (VOZ DE TESTE)"; touch VOICE_PLACEHOLDER
  espeak-ng -v ${ESPEAK_VOICE:-pt-br} -s 165 -p 45 -f script_one.txt -w voice_tmp.wav && ffmpeg -v error -y -i voice_tmp.wav -codec:a libmp3lame -q:a 4 -f mp3 voice.mp3.part && rm -f voice_tmp.wav
fi
mv voice.mp3.part voice.mp3
# 25/11 ESTRUTURA VIRAL (Gibson: 30-36 s): pausa entre frases fica curta e firme (silencio > 0,2 s vira 0,16 s) -> ritmo de Shorts, sem o vazio que esticava o video 4-6 s
if [ ! -f VOICE_PLACEHOLDER ] && python3 -c "import json,sys;sys.exit(0 if json.load(open('../../videos/$1/beats.json')).get('gancho_tipo') else 1)" 2>/dev/null; then
  ffmpeg -v error -y -i voice.mp3 -af "silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_duration=0.2:stop_threshold=-42dB:stop_silence=0.16" -codec:a libmp3lame -q:a 2 voice_curta.mp3 && [ -s voice_curta.mp3 ] && mv voice_curta.mp3 voice.mp3
fi
python3 ../../timing.py voice.mp3 script.txt --out work 2>&1 | head -80
