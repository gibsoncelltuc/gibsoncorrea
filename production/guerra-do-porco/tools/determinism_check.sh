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
echo "quadro $SHOT f$FR: hash do arquivo original=$A  re-render=$B"
RES=$(python3 - "$REF" "$TMP/f$(printf '%04d' $FR).png" <<'PY'
import sys, numpy as np
from PIL import Image
a = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(np.float32); b = np.asarray(Image.open(sys.argv[2]).convert('RGB')).astype(np.float32); d = np.abs(a - b)
print(f"diferença de pixels: média {d.mean():.4f}, máx {d.max():.0f} (0–255)"); print('IGUAIS' if d.max() == 0 else 'DIFERENTES')
PY
)
echo "$RES"; mkdir -p ../qa
if echo "$RES" | grep -q IGUAIS; then MSG="DETERMINISTICO: quadro $SHOT f$FR re-renderizado em processo separado → pixels idênticos (diferença máx 0); o hash do arquivo PNG difere só por metadados"; else MSG="DIFERENTE: $RES"; fi
echo "$MSG" | tee ../qa/determinism.txt
