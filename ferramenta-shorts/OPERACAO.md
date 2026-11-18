# OPERAÇÃO DA FÁBRICA (leia isto primeiro, sempre)

Série atual: **Guerras Inusitadas** (EP numerado; `"serie": "Guerras Inusitadas", "ep": N` no topo do roteiro). Histórias reais e curiosas de guerras/conflitos absurdos, personagens originais, 150–175 palavras narradas (~60 s).
EPs já feitos: 01 Karánsebes, 02 Emus, 03 Toledo, 04 Balde, 05 Gansos, 06 Porco, 07 Bolos, 08 Zanzibar (38 minutos), 09 Futebol (1969), 10 Chaleira (1784). Não repita tema. Dança e Tulipas ficaram FORA da série (pasta `fora_do_tema/`): só entra guerra/conflito.
Ideias ainda livres: Orelha de Jenkins (1739), Banquinho Dourado (1900), 335 anos de Scilly, Guerra do Bacalhau, Guerra do Uísque, Guerra das Laranjas (1801), Guerra dos Pastéis não (já é Bolos).
Cuidado visto na prática: se a narração diz "noite", a cena e as seguintes ficam de noite até outra cena ter `"hora": "dia"`. Todo figurino precisa das cores `jacket`, `pants`, `boots`; chapéu `cap`/`beret`/`bonnet` usa a cor `cap`.

## Os 7 passos (não pule nenhum)

1. **Ler** `CAPACIDADES.md` (o que a ferramenta tem) e `MODO_RICKS.md` (como o roteiro é escrito).
2. **Escrever** `videos/<id>/beats.json` (formato no `GUIA_DO_ROTEIRISTA.md`; copie um roteiro pronto, ex. `videos/porco1859/beats.json`, e troque). Ao escrever cada frase, pergunte: "a ferramenta consegue MOSTRAR isto?". Se não, mude a frase.
3. **Portão de entrada:** `./novo_video.sh <id>`. Ele gera as duas folhas e responde `LIBERADO` (entrou na fila) ou `BLOQUEADO: N riscos`.
4. Se bloqueado: abra `stories/<id>/folha2_producao.md`, cada risco traz a **CORREÇÃO** pronta. Corrija o `beats.json` e repita o passo 3. Risco visto e aceito: `"riscos_ok": true` na cena. Falta modelo 3D: copie um bloco de `blender/make_objetos.py`, rode `blender -b --python blender/make_objetos.py`, acrescente uma linha `["regex da palavra", "kit/nome", escala, false]` no arquivo da SUA sessão em `obj_dict.d/` (`principal.json`, `sessao_a.json` ou `sessao_b.json` — nunca no `mkvideo.py`, para o merge entre sessões não apagar o objeto de ninguém; regex sempre com `\\b` de palavra inteira) e rode `python3 capacidades.py`. Faça commit + push do `.glb`, do `blender/` e do seu `obj_dict.d/` logo depois de modelar.
5. **Esperar:** `bash status.sh`. Deixe SEMPRE uma espera em segundo plano (`until [ -f stories/<id>/DONE ] || [ -f stories/<id>/SKIP ]; do sleep 20; done`), senão a máquina dorme e a fila para.
6. **Verificação final:** `./conferir.sh <id>` e depois ABRIR `out/<id>/review_sheet.jpg` e olhar. Defeito crítico → corrigir o roteiro e `./refazer.sh <id> bN` (cenas) ou `./refazer_tudo.sh <id>` (inteiro). Não pergunte ao Gibson: corrija e relate.
7. **Entregar:** mandar pelo chat o mp4 ORIGINAL de `entregas/<id>/` (1080×1920) + relatório curto (o que passou, o que não passou, o que foi refeito). Commit + push.

## Regra número 1: seguir o roteiro À RISCA

Tudo que a narração cita tem que aparecer na tela, na mesma cena: se diz "fazenda", tem fazenda (celeiro, cerca, feno); se diz "notas de dólar", o personagem segura as notas; se diz "navios", tem navio. A ferramenta já põe sozinha lugares (`LUGARES` no `mkvideo.py`: fazenda, casa, igreja, mercado, floresta, acampamento, castelo, cidade, praça) e objetos (`OBJ_DICT`). Cada cena da folha 2 tem a linha **CONFERIR NA FOLHA DE CONTATO** com as palavras da narração: confira uma por uma no storyboard/folha de contato. Faltou → ponha em `props`, na mão (`who`), ou modele. Não entregue vídeo em que a narração fala de algo que não se vê.

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
| log diz `voz de TESTE` / a fila para com `PARADO: voz de TESTE` | o edge-tts falhou (certificado do proxy). Teste: `cd stories/<id> && SSL_CERT_FILE=/root/.ccr/ca-bundle.crt edge-tts --proxy "$HTTPS_PROXY" --voice pt-BR-AntonioNeural --text oi --write-media /tmp/t.mp3`. Se só funcionar assim, acrescente a CA ao certifi: `cat /root/.ccr/ca-bundle.crt >> $(python3 -c 'import certifi;print(certifi.where())')`. Depois relance a fila. NUNCA entregue vídeo com voz de teste |
| dois `run_queue.sh` ao mesmo tempo (SKIP falso, ENOENT em `ckpt/`) | sempre `pgrep -f run_queue.sh` antes de lançar; se houver dois, `pkill -f run_queue; pkill -f make_video; pkill -f render_pool` e lance um só |
| render com `erro de pagina` / `No space left on device` / quadros `DESISTIDO` | disco cheio: `df -h .`; apague `out/<id>/frames` dos vídeos já entregues e `/root/.cache/pip` (NÃO apague `/root/.cache/huggingface`). Se o log do vídeo tiver quadro DESISTIDO, rode `./refazer_tudo.sh <id>` depois de liberar espaço |
| fila parada (`bash status.sh` sem processo) | `nohup bash run_queue.sh > logs/queue_run.log 2>&1 &` |
| máquina reiniciou | a fila volta sozinha; recrie a espera em segundo plano |
| personagem cortado / cena vazia / objeto fora do quadro | ver "Reparos" no fim da folha 2 |
| várias sessões no mesmo repositório | cada sessão trabalha no SEU branch e em ids diferentes; antes de começar: `git fetch origin claude/bold-sagan-dskrsj && git merge --no-edit FETCH_HEAD` para pegar a ferramenta mais nova |

## Arquivos

`novo_video.sh` portão de entrada · `conferir.sh` verificação final · `refazer.sh` / `refazer_tudo.sh` reparo · `status.sh` andamento · `run_queue.sh` fila · `mkvideo.py` diretor (gera spec, folhas, plano) · `capacidades.py` → `CAPACIDADES.md` · `GUIA_DO_ROTEIRISTA.md` formato do roteiro · `MODO_RICKS.md` estilo.
