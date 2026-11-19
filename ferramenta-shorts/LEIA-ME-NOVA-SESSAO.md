# COMO CONTINUAR EM UMA SESSÃO NOVA (do zero)
1. Descompacte este zip numa pasta e abra uma sessão do Claude Code dentro dela (a pasta `ferramenta-shorts/` fica na raiz; `CLAUDE.md` e `.claude/` ficam ao lado).
2. Cole para a sessão: "Leia CLAUDE.md e ferramenta-shorts/MANUAL_SONNET.md inteiros e continue a produção: refazer os vídeos da fila (queue.txt) seguindo o ciclo do §2 (revisar storyboard, aprovar, conferir, entregar). Responda em português, curto."
3. Instale as dependências: `cd ferramenta-shorts && npm install` (Playwright/Chromium e ffmpeg precisam estar instalados) e Blender se for modelar objeto novo.
4. Subir a fila: `cd ferramenta-shorts && bash run_queue.sh` (ids em `queue.txt`). Status: `bash status.sh`.
5. Roteiros: `ferramenta-shorts/videos/<id>/beats.json` (todos os vídeos feitos até agora). Lista do que falta/ordem: `queue.txt`, `fila_sessao_A.txt`, `fila_sessao_B.txt`.
6. O que NÃO está no zip (pesado e regenerável): vídeos prontos (mp4), quadros e ckpt de render. Os mp4 já entregues ficam no chat.
Regras do Gibson: REGRA MESTRA e ZERO RESSALVA (CLAUDE.md). Série "E Se" pausada.
