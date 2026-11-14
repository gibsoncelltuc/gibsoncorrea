#!/usr/bin/env bash
set -euo pipefail

# Uso:
#   bash scripts/mix_audio.sh voice.wav music.wav sfx.wav output.wav
# voice.wav e sfx.wav devem estar alinhados ao início do vídeo; music.wav será repetida.

if [[ $# -ne 4 ]]; then
  echo "Uso: $0 voice.wav music.wav sfx.wav output.wav" >&2
  exit 2
fi
VOICE="$1"
MUSIC="$2"
SFX="$3"
OUTPUT="$4"

for file in "$VOICE" "$MUSIC" "$SFX"; do
  [[ -f "$file" ]] || { echo "Arquivo não encontrado: $file" >&2; exit 2; }
done
command -v ffmpeg >/dev/null 2>&1 || { echo "FFmpeg não encontrado no PATH" >&2; exit 2; }

mkdir -p "$(dirname "$OUTPUT")"
ffmpeg -y \
  -i "$VOICE" \
  -stream_loop -1 -i "$MUSIC" \
  -i "$SFX" \
  -filter_complex \
  "[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,volume=1.0[voice];\
   [1:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,volume=0.18[music];\
   [2:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,volume=0.72[sfx];\
   [music][voice]sidechaincompress=threshold=0.035:ratio=7:attack=20:release=320[ducked];\
   [voice][ducked][sfx]amix=inputs=3:duration=first:dropout_transition=2:normalize=0,\
   loudnorm=I=-15:TP=-1.0:LRA=8,alimiter=limit=0.89[out]" \
  -map "[out]" -c:a pcm_s24le -ar 48000 "$OUTPUT"

echo "Mix renderizada: $OUTPUT"
