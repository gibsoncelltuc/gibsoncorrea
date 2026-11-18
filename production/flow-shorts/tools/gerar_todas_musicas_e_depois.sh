#!/usr/bin/env bash
# Espera a fila 11-30 terminar (FIM em todas.log) e depois gera 31-51.
HERE="$(cd "$(dirname "$0")" && pwd)"
until grep -q FIM /home/user/musica/todas.log 2>/dev/null; do sleep 30; done
"$HERE/gerar_todas_musicas.sh" 31 51
