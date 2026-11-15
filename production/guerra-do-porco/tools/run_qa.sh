#!/usr/bin/env bash
# Bateria de QA do piloto: automáticos (qa.py, qa_extra.py), fidelidade vs referência, métrica de contorno, manifest e folha de contato.
# Uso: tools/run_qa.sh [video.mp4] [pasta_frames_referencia]
set -e
cd "$(dirname "$0")/.."
V=${1:-renders/pilot_540.mp4}; REF=${2:-/tmp/claude-0/ref2}
python3 tools/qa.py $V pilot 540x960@30 | tee qa/qa-run.txt
python3 tools/qa_extra.py $V pilot_extra | tee -a qa/qa-run.txt
python3 tools/fidelity_report.py $V $REF | tee -a qa/qa-run.txt
python3 tools/outline_metrics.py "referencia=$REF/[AB]_*.png" "piloto=blender/out/frames" --n 40 | tee -a qa/qa-run.txt
python3 tools/make_manifest.py $V | tee -a qa/qa-run.txt
python3 tools/contact_sheet.py $V renders/contact_540.png 6 3 270 | tee -a qa/qa-run.txt
