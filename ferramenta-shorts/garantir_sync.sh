#!/usr/bin/env bash
# SINCRONIA AUTOMATICA DA FERRAMENTA, SEM DEPENDER DE NINGUEM (ordem do Gibson 24/11).
# Nas sessoes de producao (qualquer branch que nao seja o principal) mantem vivo um laco que puxa a ferramenta do branch principal a cada 60 s.
# E' chamado sozinho: no inicio da sessao (boot.sh), a cada mensagem recebida (hook UserPromptSubmit), e pela fila antes de cada video.
# Rodar a mao nunca e' necessario; rodar duas vezes nao duplica o laco.
cd "$(dirname "$0")" || exit 0; mkdir -p logs
BR=$(git -C .. rev-parse --abbrev-ref HEAD 2>/dev/null)
[ "$BR" = "claude/bold-sagan-dskrsj" ] && exit 0          # a principal e' a fonte: nao puxa de si mesma
pgrep -f "laco_sync_ferramenta" >/dev/null && exit 0
nohup setsid bash -c 'exec -a laco_sync_ferramenta bash -c "while true; do bash ./sync_ferramenta.sh >> logs/sync.log 2>&1; sleep 60; done"' > /dev/null 2>&1 &
echo "$(date +%T) laco de sincronia (60 s) ligado" >> logs/sync.log
exit 0
