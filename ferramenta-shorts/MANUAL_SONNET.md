# MANUAL DE OPERAÇÃO — para o modelo que assume (Sonnet 5.5), nas 3 sessões
Escrito em 19/11 à noite, na troca de modelo pedida pelo Gibson. Leia INTEIRO antes de agir. Responda ao Gibson sempre em português, curto e honesto.

## 0. As 3 sessões e quem faz o quê
| Sessão | Branch | Fila | Papel |
|---|---|---|---|
| PRINCIPAL (session_01HE8Dy3UcXXZZMLa7uzjNJD) | claude/serene-dirac-ckwlt5 | `queue.txt` | produz vídeos, mantém a FERRAMENTA (motor), AUDITA as sessões A/B, entrega TODOS os vídeos ao Gibson pelo chat |
| A (session_01HE8Dy3Tz5Mgz6d3rSUrMHS) | claude/prod-a-karansebes | `fila_sessao_A.txt` | só produz vídeos e envia à principal |
| B (session_01HE8DxzBrskhVHznwqCpD4i) | claude/prod-b-emus | `fila_sessao_B.txt` | só produz vídeos e envia à principal |

Sessões A/B NÃO mexem no motor (`web/`, `mkvideo.py`, `blender/`): pegam as correções sozinhas pelo `sync_ferramenta.sh` (a cada 10 min). Se acharem defeito do motor, corrigem o ROTEIRO (`videos/<id>/beats.json`) e avisam a principal no relatório da entrega.

## 1. As ordens do Gibson (acima de tudo)
1. **REGRA MESTRA:** nunca conte um problema sem já ter resolvido. Achou → corrige → confere → só então relata (já corrigido). Erro = prioridade máxima.
2. **ZERO RESSALVA:** nenhum vídeo sai com defeito, nem de acabamento. Se você pensou "tem um detalhezinho mas dá pra mandar" → NÃO manda, refaz.
3. **Prioridade de produção:** refazer os vídeos que já existiam, com a ferramenta nova: Guerras Inusitadas e Poder e Fama primeiro, depois Curiosidade e Ciência. **Série "E Se" está PAUSADA** (ids `ese_*` comentados com `#PAUSADO` nas filas) — só volta quando todos os outros estiverem refeitos.
4. Todos os vídeos são entregues ao Gibson NA SESSÃO PRINCIPAL (SendUserFile), nunca só em pasta.
5. Não pergunte "quer que eu corrija?". Ordem dele = fazer tudo. Não use agentes/subagentes/workflows.
6. Commit + push ao fim de cada turno (o hook de parada cobra).

## 2. Ciclo de UM vídeo (passo a passo)
1. A fila (`run_queue.sh`) gera voz, as 3 folhas, o storyboard e a grade de ações, e para em `stories/<id>/AGUARDA_STORYBOARD`.
2. **Revisão do storyboard (você):**
   - `Read stories/<id>/storyboard.jpg` e `Read stories/<id>/grade_acoes.jpg`.
   - Leia a narração: `python3 -c "import json;B=json.load(open('videos/<id>/beats.json'));[print(f'b{i}:',b['say']) for i,b in enumerate(B['beats'])]"`
   - Para CADA frase pergunte: (a) a AÇÃO dita aparece (quem morre cai, quem come leva à boca, briga = empurrão/soco visível, explode = explosão)? (b) o LUGAR é o certo (época, país, nada moderno em história antiga, nada de porto com navio de guerra se a história não é no mar)? (c) objeto citado aparece e não está duplicado? (d) ninguém cortado, nada tapando a câmera?
   - Na dúvida, renderize a cena numa CÓPIA (nunca na pasta da fila): veja §4.
   - Tudo certo → escreva `stories/<id>/revisao_storyboard.md` (uma linha por cena: `bN: OK - <descrição com palavras da frase, 8+ palavras>` ou `bN: CORRIGIDO - <defeito> -> <correção>`) e rode `./aprovar_storyboard.sh <id>`.
   - Defeito → corrija `videos/<id>/beats.json`, `python3 mkvideo.py <id>`, confira na cópia, depois `rm -f stories/<id>/{storyboard.jpg,AGUARDA_STORYBOARD,STORYBOARD_OK}` para a fila gerar outro storyboard.
3. A fila renderiza (≈17 min) e cria `stories/<id>/DONE`.
4. **Conferência final (obrigatória, completa):**
   - `./conferir.sh <id>` (checagens automáticas).
   - `Read out/<id>/review_sheet.jpg` (folha de contato) lendo a narração.
   - **Quadro em cada ação** (pega o que a folha não pega): `bash /home/user/gibsoncorrea/ferramenta-shorts/auditar_acoes.sh <branch> <id> <caminho do mp4>` → abre `/tmp/claude-0/aud/<id>.jpg` (1 quadro 0,35 s depois de cada palavra de ação, com o rótulo). Cada quadro tem que MOSTRAR a ação do rótulo. Se a ação dura (queda, explosão), extraia mais quadros com ffmpeg (`ffmpeg -ss <t> -i <mp4> -frames:v 1 x.jpg`).
5. Aprovado → (principal) `mv out/<id>/*.mp4 /home/user/gibsoncorrea/videos_prontos/<Série>/`, `SendUserFile` com 1 linha, `rm -rf out/<id>/frames ckpt/<id>`. (Sessões A/B) `./enviar_para_principal.sh <id>`.
6. Reprovado → corrigir e refazer: `rm -f stories/<id>/{DONE,STORYBOARD_OK,storyboard.jpg,AGUARDA_STORYBOARD}; rm -rf ckpt/<id> out/<id>/frames out/<id>/*.mp4` → a fila refaz (com storyboard novo para revisar).

## 3. Como pensar um problema difícil (receita)
Use sempre esta ordem; não pule passos.
1. **Veja com os olhos.** Nunca conclua por log ou por um quadro só. Extraia quadros do vídeo/strip nos instantes certos (§4). Escreva para si: "na frase X deveria aparecer Y; aparece Z".
2. **Ache a CAMADA do defeito** (de cima para baixo):
   - Roteiro (`beats.json`): falta `set`, `interior`, `props`, `who`, `shot`? Uma palavra virou ação errada ("fabricar" → fábrica, "contou" → examina)?
   - Gerador (`mkvideo.py`): a regra que transforma palavra em ação/lugar está errada? Procure com `grep -n "<palavra>" mkvideo.py`.
   - Spec (`stories/<id>/spec.js`): a instrução saiu certa? `grep -o "poses[^;]*" stories/<id>/spec.js`, `grep -oE "S\('b[0-9]+', [^,]+, [^,]+, X[_a-z]*" spec.js` (cenário de cada cena).
   - Motor (`web/runtime.js`, `web/toonbase.js`, `web/main.js`): a instrução certa é desenhada errado (ex.: pose 'fall' só abria as pernas)?
   - Modelo 3D (`blender/*.py` → `web/assets/library/kit/*.glb`): o objeto não parece o que é (ex.: cova aberta em vez de lápide)?
3. **Conserte na camada mais baixa que resolve TODOS os vídeos** (motor/gerador), não só o vídeo da vez — mas só na sessão PRINCIPAL. Sessões A/B corrigem no roteiro.
4. **Teste na cópia** (§4) e OLHE o resultado. Se não ficou bom, volte ao passo 2.
5. **Rode as verificações:** `python3 -c "import ast;ast.parse(open('mkvideo.py').read())"` (sintaxe), `python3 verificar_execucao.py <id>` (tem que dar 100% ações e cenário), e para o motor `cat web/toonbase.js web/roman.js web/pig2d.js web/animals2d.js > web/toon.js`.
6. **Procure o mesmo defeito nos outros vídeos** (`grep -l "<palavra>" videos/*/beats.json`) e reponha na fila os afetados.
7. Commit com mensagem clara + push. Só então relate ao Gibson: "estava X, ficou Y, conferido".

## 4. Testar uma cena sem atrapalhar a fila (cópia)
```
cd /home/user/gibsoncorrea/ferramenta-shorts
rm -rf stories/zt videos/zt; cp -r stories/<id> stories/zt; mkdir -p videos/zt; cp -r videos/<id>/* videos/zt/
rm -f stories/zt/*.jpg stories/zt/DONE stories/zt/AGUARDA_STORYBOARD
./prechecar.sh zt b5 8        # 8 quadros da cena b5 -> stories/zt/precheck_b5.jpg  (Read para olhar)
./prechecar.sh zt acoes       # 1 quadro por ação
rm -rf stories/zt videos/zt   # SEMPRE apagar a cópia depois
```
Nunca rode `build3.sh`/`fit.sh`/`shot.mjs`/`storyboard.mjs` direto na pasta de um vídeo que está na fila.

## 5. Ferramentas de roteiro mais usadas (`videos/<id>/beats.json`, por cena)
- `set`: countryside, street, harbor (porto/mar), medieval (cidade europeia antiga), palace (deserto/palácio oriental, TEM palmeiras), outback (deserto/México, cactos), mountain, jungle, arctic, stadium.
- `interior`: 'loja' | 'madeira' | 'pedra' | 'hospital' (sala); `interior: false` proíbe sala.
- `props`: `[["kit/<objeto>", x, z, escala]]` (z negativo = atrás). Lista: `ls web/assets/library/kit/`.
- `who`: `["SIGLA:variação:expressão"]`; `shot`: two, close, group, crowd, reveal, low; `shot_lock: true` impede o diretor de trocar; `detalhe: false/true` (tomada de detalhe).
- `batalha: false`, `impact: false` tiram combate automático; `text`/`titulo` placa grande.
- Gestos/poses automáticos pela palavra (folha 3 mostra): morre/caiu (corpo tomba), ajoelha (de joelhos, súplica), dorme, senta, come (leva à boca), briga (golpe), paga, grita, etc. "morreu em <ano>" = lápide.
- Objeto que não existe: modele em `blender/objetos_detalhe.py` (copie o padrão de `chess_pc`/`lapide`), rode `blender -b --python blender/objetos_detalhe.py -- <nome>` (principal apenas).

## 6. Rotina da PRINCIPAL
- Espera em segundo plano sempre ativa (a máquina dorme se a conversa fica ociosa):
  `cd ferramenta-shorts; T=$(date +%s); until ls stories/*/AGUARDA_STORYBOARD 2>/dev/null | grep -qvE 'curie1898' || [ -n "$(find stories -maxdepth 2 -name DONE -newermt @$T)" ] || ! pgrep -f run_queue.sh >/dev/null; do sleep 30; done` (Bash run_in_background, timeout 7200000).
- Ronda de hora em hora (gatilho "Ronda horaria principal", :14): `bash receber_das_sessoes.sh` → para cada NOVO: folha de contato + `auditar_acoes.sh` → bom: SendUserFile dizendo "sessão A/B"; defeito: `rm` o mp4 de `videos_prontos`, apague a linha do id em `logs/recebidos.txt` e `send_message` à sessão com o defeito EXATO (frase, segundo, o que falta) terminando com "Não responda por mensagem."
- Watchdog: `pgrep -f watchdog.sh`; se parado: `nohup setsid bash -c 'while true; do bash watchdog.sh >> logs/watchdog.log 2>&1; sleep 60; done' >/dev/null 2>&1 &`. Fila parada: `nohup bash run_queue.sh > logs/queue_run.log 2>&1 &`.
- Sessão parada (list_sessions children=true, ociosa e sem commit há >15 min): `send_message` "Retome de onde parou: merge do principal, fila, sync. Não responda por mensagem."
- Disco: `df -h /`. Abaixo de 5 GB: apagar `out/<id>/frames`, `ckpt/<id>`, `stories/<id>/work` de vídeos já entregues e mp4 antigos reprovados. NUNCA `git gc` com render rodando (encheu o disco uma vez). Nunca apague vídeo aprovado em `videos_prontos`.

## 7. Rotina das sessões A e B
1. Ao começar/retomar: `git fetch origin claude/serene-dirac-ckwlt5 && git merge -X theirs FETCH_HEAD`; garantir o loop de sync: `nohup bash -c 'while true; do ./sync_ferramenta.sh >> logs/sync.log 2>&1; sleep 600; done' >/dev/null 2>&1 &`; `nohup bash run_queue.sh > logs/queue_run.log 2>&1 &`.
2. Correções pedidas pela principal (mensagens "AUDITORIA") vêm ANTES da fila nova.
3. Para cada vídeo: §2 inteiro (storyboard, render, conferir, folha, `auditar_acoes.sh`). Só então `./enviar_para_principal.sh <id>`.
4. Nunca mande vídeo "quase bom". A principal reprova e você perde o tempo do render.

## 8. Lições caras de 19/11 (não repetir)
- A folha de contato NÃO prova que a ação aparece: 11 vídeos "aprovados" tinham ação invisível. Por isso existe o `auditar_acoes.sh`.
- Quadro único engana: confira 3 instantes depois da palavra em ações que levam tempo (cair, explodir, pousar).
- Palavra ≠ ação literal: "fabricar dinheiro" não é fábrica; "a notícia correu" não é corrida; negação ("ninguém atirou") não é tiro.
- Cenário sorteado pela variedade pode cair errado (porto com navio de guerra, palmeiras na França, prédio moderno em 1518): fixe `set` nas cenas.
- Objeto grande não pode duplicar (dois balões); a ferramenta já filtra, mas confira.
- Disco cheio corrompe o render (trecho de 0,2 MB): se o disco encher, apague o trecho estragado (`ckpt/<id>/seg_NNN.mp4` pequeno) e deixe refazer.
