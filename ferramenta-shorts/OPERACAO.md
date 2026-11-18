# OPERAÇÃO DA FÁBRICA (leia isto primeiro, sempre)

Série atual: **Guerras Inusitadas** (EP numerado; `"serie": "Guerras Inusitadas", "ep": N` no topo do roteiro). Histórias reais e curiosas de guerras/conflitos absurdos, personagens originais, 150–175 palavras narradas (~60 s).
EPs já feitos: 01 Karánsebes, 02 Emus, 03 Toledo, 04 Balde, 05 Gansos, 06 Porco, 07 Bolos, 08 Zanzibar (38 minutos). Não repita tema.

## Os 7 passos (não pule nenhum)

1. **Ler** `CAPACIDADES.md` (o que a ferramenta tem) e `MODO_RICKS.md` (como o roteiro é escrito).
2. **Escrever** `videos/<id>/beats.json` (formato no `GUIA_DO_ROTEIRISTA.md`; copie um roteiro pronto, ex. `videos/porco1859/beats.json`, e troque). Ao escrever cada frase, pergunte: "a ferramenta consegue MOSTRAR isto?". Se não, mude a frase.
3. **Portão de entrada:** `./novo_video.sh <id>`. Ele gera as duas folhas e responde `LIBERADO` (entrou na fila) ou `BLOQUEADO: N riscos`.
4. Se bloqueado: abra `stories/<id>/folha2_producao.md`, cada risco traz a **CORREÇÃO** pronta. Corrija o `beats.json` e repita o passo 3. Risco visto e aceito: `"riscos_ok": true` na cena. Falta modelo 3D: copie um bloco de `blender/make_objetos.py`, rode `blender -b --python blender/make_objetos.py`, acrescente uma linha no `OBJ_DICT` do `mkvideo.py` e rode `python3 capacidades.py`.
5. **Esperar:** `bash status.sh`. Deixe SEMPRE uma espera em segundo plano (`until [ -f stories/<id>/DONE ] || [ -f stories/<id>/SKIP ]; do sleep 20; done`), senão a máquina dorme e a fila para.
6. **Verificação final:** `./conferir.sh <id>` e depois ABRIR `out/<id>/review_sheet.jpg` e olhar. Defeito crítico → corrigir o roteiro e `./refazer.sh <id> bN` (cenas) ou `./refazer_tudo.sh <id>` (inteiro). Não pergunte ao Gibson: corrija e relate.
7. **Entregar:** mandar pelo chat o mp4 ORIGINAL de `entregas/<id>/` (1080×1920) + relatório curto (o que passou, o que não passou, o que foi refeito). Commit + push.

## Todo vídeo tem (a folha 2 confere)

- Objeto herói abrindo e fechando o vídeo, com close de câmera.
- 2 grandes momentos em plano aberto com multidão, efeito e som; no mínimo 2 planos abertos.
- Mapa rápido quando cita lugar.
- Em toda cena média os personagens interagem (interações diferentes de cena para cena) e têm expressão própria (use expressões variadas no `who`: angry, shout, sad, cry, smug, surprised, scared, suspicious, além de smile, grin, laugh, shock, stern, nervous, pained).
- Efeito + som em toda palavra de ação.

## Proibido

- Renderizar com risco em aberto, ou entregar sem olhar a folha de contato.
- Editar `web/`, `mkvideo.py`, `stories/_h.js` só para "fazer passar" um vídeo. Só se mexe na ferramenta para corrigir defeito dela, testando antes num storyboard fora da pasta da fila.
- Rodar `build3.sh`, `fit.sh`, `shot.mjs`, `storyboard.mjs` na pasta da fila enquanto ela roda.
- Afrouxar gate/QA, apagar `SKIP` sem corrigir a causa, usar agentes/subagentes.
- Entregar prévia comprimida no lugar do original.

## Quando algo dá errado

| Sintoma | O que fazer |
|---|---|
| `BLOQUEADO` no `novo_video.sh` | corrigir o roteiro pela folha 2 e rodar de novo |
| `stories/<id>/SKIP` apareceu | ler `logs/gate_<id>.txt`; quase sempre é enquadramento: tire gente do `who`, troque `shot` para `group`; apague `SKIP` e `fails` e relance a fila |
| render terminou em 2 min sem mudar nada | reaproveitou quadro velho: `./refazer_tudo.sh <id>` |
| fila parada (`bash status.sh` sem processo) | `nohup bash run_queue.sh > logs/queue_run.log 2>&1 &` |
| máquina reiniciou | a fila volta sozinha; recrie a espera em segundo plano |
| personagem cortado / cena vazia / objeto fora do quadro | ver "Reparos" no fim da folha 2 |
| várias sessões no mesmo repositório | cada sessão trabalha no SEU branch e em ids diferentes; antes de começar: `git fetch origin claude/bold-sagan-dskrsj && git merge --no-edit FETCH_HEAD` para pegar a ferramenta mais nova |

## Arquivos

`novo_video.sh` portão de entrada · `conferir.sh` verificação final · `refazer.sh` / `refazer_tudo.sh` reparo · `status.sh` andamento · `run_queue.sh` fila · `mkvideo.py` diretor (gera spec, folhas, plano) · `capacidades.py` → `CAPACIDADES.md` · `GUIA_DO_ROTEIRISTA.md` formato do roteiro · `MODO_RICKS.md` estilo.
