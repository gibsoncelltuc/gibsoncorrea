#!/usr/bin/env bash
# usage: ./produce_voice.sh <id> [voice] [rate]   -> stories/<id>/voice.mp3 + work/{words,phrases}.json
# Tenta edge-tts (voz neural PT-BR). Se a rede bloquear (nuvem), cai para espeak-ng = VOZ DE TESTE (marca stories/<id>/VOICE_PLACEHOLDER).
set -e; cd "$(dirname "$0")/stories/$1"; VOICE="${2:-en-US-GuyNeural}"; RATE="${3:-+8%}"
tr '\n' ' ' < script.txt | sed 's/  */ /g' > script_one.txt
rm -f voice.mp3.part VOICE_PLACEHOLDER
if timeout 120 edge-tts ${HTTPS_PROXY:+--proxy "$HTTPS_PROXY"} --voice "$VOICE" --rate="$RATE" --file script_one.txt --write-media voice.mp3.part 2>/dev/null && [ -s voice.mp3.part ]; then
  :
else
  echo "AVISO: edge-tts indisponivel; usando espeak-ng (VOZ DE TESTE)"; touch VOICE_PLACEHOLDER
  espeak-ng -v ${ESPEAK_VOICE:-pt-br} -s 165 -p 45 -f script_one.txt -w voice_tmp.wav && ffmpeg -v error -y -i voice_tmp.wav -codec:a libmp3lame -q:a 4 -f mp3 voice.mp3.part && rm -f voice_tmp.wav
fi
mv voice.mp3.part voice.mp3
python3 ../../timing.py voice.mp3 script.txt --out work 2>&1 | head -80
