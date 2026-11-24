#!/usr/bin/env bash
# LIMPEZA AUTOMATICA DE DISCO (24/11: render da Melancia e montagem do Lagosta falharam por disco cheio).
# Apaga so' o descartavel: checkpoints de videos ENTREGUES, quadros soltos de videos com DONE (o mp4 fica), versoes reprovadas, cache do pip.
# Roda sozinha pelo vigia.sh quando sobra menos de 3 GB. uso manual: bash ferramenta-shorts/limpar_disco.sh
cd "$(dirname "$0")"; RODANDO=$(pgrep -af "make_video.sh" | awk '{print $NF}' | head -1)
for d in ckpt/*; do v=$(basename "$d"); [ "$v" != "$RODANDO" ] && [ -f "stories/$v/ENTREGUE" ] && rm -rf "./ckpt/$v"; done
for d in out/*/frames; do [ -d "$d" ] || continue; v=$(basename "$(dirname "$d")"); [ "$v" != "$RODANDO" ] && [ -f "stories/$v/DONE" ] && rm -rf "./out/$v/frames"; done
find ../videos_prontos/_reprovados -maxdepth 1 -name '*.mp4' -delete 2>/dev/null
rm -rf /root/.cache/pip 2>/dev/null
echo "$(date +%T) limpeza de disco: $(df -Ph . | awk 'NR==2{print $4}') livres"
