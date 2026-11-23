# Sessao nova (atualizado 23/11)
1. `git fetch origin claude/bold-sagan-dskrsj && git checkout claude/bold-sagan-dskrsj` (a ferramenta inteira e todos os roteiros estao nesse branch; nao precisa copiar arquivo nenhum).
2. Leia o topo do `CLAUDE.md` ("ESTADO EM 23/11") e depois `ferramenta-shorts/MANUAL_SONNET.md`.
3. `cd ferramenta-shorts && bash boot.sh` (se o hook nao rodou): dependencias, certificado da voz, fila (`fila_principal.txt` -> `queue.txt`), watchdog.
4. `bash status.sh` para ver a fila; storyboard em AGUARDA_STORYBOARD -> olhar `storyboard.jpg` e `grade_acoes.jpg`, corrigir o beats.json se tiver defeito, aprovar com `./aprovar_rapido.sh <id>`.
5. Vídeo pronto -> `./conferir.sh <id>`, olhar `out/<id>/review_sheet.jpg`, `bash auditar_acoes.sh claude/bold-sagan-dskrsj <id> <mp4>` e olhar o jpg; sem defeito -> entregar ao Gibson.
6. Roteiro novo: pesquisa historica + PESQUISA VISUAL (bloco "visual") ANTES de escrever (GUIA_DO_ROTEIRISTA.md).
