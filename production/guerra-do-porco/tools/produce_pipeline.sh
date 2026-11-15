#!/usr/bin/env bash
# PRODUÇÃO EM 2 ETAPAS COM PORTÃO: (1) PRÉVIA em 540×960 → quadro a quadro + reparo cirúrgico → montagem → portão de 53 checagens; (2) só se a prévia passar, o FINAL em 1080×1920 → mesmos portões.
# Nada é entregue sem `tools/gate.py --verify`. Retomável (render_shot pula quadros existentes). Uso: tools/produce_pipeline.sh <nome> [S_previa=6] [S_final=6]   (env: REF_DIR, GRASS)
set -e; cd "$(dirname "$0")/.."; N=${1:?nome}; SP=${2:-6}; SF=${3:-6}; G=${GRASS:-50000}; REF=${REF_DIR:-}
stage() { # $1=W $2=H $3=amostras $4=arquivo
  rm -rf blender/out/frames; for p in 1 2; do (cd blender && ./render_all.sh $1 $2 $3 $G 2 $((p-1))); done
  python3 tools/repair_frames.py W=$1 H=$2 S=$3 GRASS=$G --max 3                      # ETAPA A: quadro a quadro; refaz só os reprovados
  tools/montage.sh $4; python3 tools/gate.py $4 ${1}x${2}@30 $REF                    # ETAPA B: vídeo montado (se falhar: corrigir e repetir; trecho ruim → tools/patch_segment.py)
}
stage 540 960 $SP renders/${N}_previa_540.mp4
echo "PRÉVIA APROVADA — iniciando o FINAL em 1080×1920"
stage 1080 1920 $SF renders/${N}_final_1080.mp4
python3 tools/gate.py --verify renders/${N}_final_1080.mp4 && echo "PRONTO PARA ENTREGA: renders/${N}_final_1080.mp4"
