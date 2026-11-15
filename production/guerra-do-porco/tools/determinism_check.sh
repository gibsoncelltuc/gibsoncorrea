#!/usr/bin/env bash
# Teste de determinismo do render: re-renderiza um quadro em processo separado e compara o hash com o quadro já existente.
# Uso: tools/determinism_check.sh [SHOT=S3] [FRAME=247] [W=540] [H=960] [SPP=12] [GRASS=50000]
set -e
cd "$(dirname "$0")/../blender"
SHOT=${1:-S3}; FR=${2:-247}; W=${3:-540}; H=${4:-960}; S=${5:-12}; G=${6:-50000}
REF=out/frames/$SHOT/f$(printf '%04d' $FR).png; TMP=out/_det/$SHOT; rm -rf $TMP
# o 1º quadro do plano define a paridade da passada; OFFSET escolhe a passada correta
F0=$(python3 -c "import sys; sys.path.insert(0,'.'); from lib import anim; a,b=anim.SHOTS['$SHOT']; print(int(round((a-(0.2 if '$SHOT'!='S1' else 0))*30)))" 2>/dev/null | tail -n1)
OFF=$(( (FR - F0) % 2 ))
OFFSET=$OFF python3 render_shot.py $SHOT $W $H $S $TMP 2 $G $FR:$((FR+1)) > /dev/null 2>&1
A=$(sha256sum $REF | cut -c1-16); B=$(sha256sum $TMP/f$(printf '%04d' $FR).png | cut -c1-16)
echo "quadro $SHOT f$FR: original=$A  re-render=$B"; [ "$A" = "$B" ] && echo "DETERMINISTICO: hashes idênticos" || echo "DIFERENTE: investigar (tolerância/pixel diff)"
