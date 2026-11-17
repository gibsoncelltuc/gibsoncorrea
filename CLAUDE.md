# Projeto: shorts animados (ferramenta-shorts/)
Usuário: Gibson, fala português. Responda sempre em português, curto e honesto. NÃO use agentes/subagentes nem workflows (consomem a cota dele).
Para produzir um vídeo leia, nesta ordem: `ferramenta-shorts/GUIA_DO_ROTEIRISTA.md` (como escrever o beats.json e rodar) e `ferramenta-shorts/MODO_RICKS.md` (regras de roteiro e estilo medidas no canal de referência).
Regras: histórias e personagens sempre originais; olhar o storyboard e a folha de contato antes de entregar; enviar o vídeo pronto (prévia comprimida) pelo chat; não editar o motor (`web/`, `mkvideo.py`) só para fazer um vídeo; nunca rodar `build3.sh`/`shot.mjs`/`storyboard.mjs` enquanto a fila roda; commit + push no branch de trabalho ao terminar.
Fila: `cd ferramenta-shorts && bash status.sh` | `bash run_queue.sh` (ids em `queue.txt`). Retoma sozinha após reinício (hook em `.claude/settings.json`).
