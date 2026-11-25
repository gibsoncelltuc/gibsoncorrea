#!/usr/bin/env bash
# LIMPEZA AUTOMATICA DE DISCO (24/11: render da Melancia e montagem do Lagosta falharam por disco cheio).
# Apaga so' o descartavel: checkpoints de videos ENTREGUES, quadros soltos de videos com DONE (o mp4 fica), versoes reprovadas, cache do pip.
# Roda sozinha pelo vigia.sh quando sobra menos de 3 GB. uso manual: bash ferramenta-shorts/limpar_disco.sh
cd "$(dirname "$0")"; RODANDO=$(pgrep -af "make_video.sh" | awk '{print $NF}' | head -1)
for d in ckpt/*; do v=$(basename "$d"); [ "$v" != "$RODANDO" ] && [ -f "stories/$v/ENTREGUE" ] && ! grep -q " antigo" "$d/cenas.txt" 2>/dev/null && ! grep -qx "$v" queue.txt 2>/dev/null && rm -rf "./ckpt/$v"; done   # ckpt reconstituido (cenas "antigo") ou video na fila = em refacao: fica
for d in out/*/frames; do [ -d "$d" ] || continue; v=$(basename "$(dirname "$d")"); [ "$v" != "$RODANDO" ] && [ -f "stories/$v/DONE" ] && ! grep -q "^$v " refazer.txt 2>/dev/null && rm -rf "./out/$v/frames"; done   # video com refacao pendente guarda os quadros (refazer so a cena)
for m in out/*/*.mp4; do [ -f "$m" ] || continue; v=$(basename "$(dirname "$m")"); [ -f "stories/$v/ENTREGUE" ] || continue; c=$(find ../videos_prontos -path ../videos_prontos/_reprovados -prune -o -name "$(basename "$m")" -size +1M -print 2>/dev/null | head -1); [ -n "$c" ] && cmp -s "$m" "$c" && rm -f "./$m"; done   # mp4 de video entregue: a copia fica em videos_prontos (so apaga se for identica)
for m in ../entregas/*/*.mp4; do [ -f "$m" ] || continue; v=$(basename "$(dirname "$m")"); [ -f "stories/$v/ENTREGUE" ] || continue; c=$(find ../videos_prontos -path ../videos_prontos/_reprovados -prune -o -name "$(basename "$m")" -print 2>/dev/null | head -1); [ -n "$c" ] && cmp -s "$m" "$c" && rm -f "./$m"; done   # copia do pacote de entrega (identica a de videos_prontos)
for d in tmp/qs_*; do [ -d "$d" ] || continue; v=${d#tmp/qs_}; [ -f "stories/$v/ENTREGUE" ] && rm -rf "./$d"; done
find ../videos_prontos/_reprovados -maxdepth 1 -name '*.mp4' -delete 2>/dev/null
rm -rf /root/.cache/pip 2>/dev/null; (cd .. && git prune-packed 2>/dev/null; find .git/objects -name "tmp_obj_*" -mmin +30 -delete 2>/dev/null)   # objetos soltos do git que ja estao nos pacotes (seguro)
echo "$(date +%T) limpeza de disco: $(df -Ph . | awk 'NR==2{print $4}') livres"
