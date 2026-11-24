# Projeto: shorts animados (ferramenta-shorts/)
Usuário: Gibson, fala português. Responda sempre em português, curto e honesto. NÃO use agentes/subagentes nem workflows (consomem a cota dele).
**PRIMEIRO leia `ferramenta-shorts/MANUAL_SONNET.md` (manual completo de operação das 3 sessões, passo a passo, e como resolver problemas difíceis).** Depois leia `ferramenta-shorts/OPERACAO.md` e `ferramenta-shorts/PROTOCOLO_ACAO.md` (os 7 passos da fábrica, o que todo vídeo tem, o que é proibido, o que fazer quando dá errado). Depois `CAPACIDADES.md`, `GUIA_DO_ROTEIRISTA.md` e `MODO_RICKS.md`.
## ESTADO EM 23/11 (leia antes de tudo; sessao nova comeca aqui)
- Branch de trabalho: `claude/bold-sagan-dskrsj` (tudo esta nele: ferramenta, roteiros, objetos 3D). Sessao nova: `git fetch origin claude/bold-sagan-dskrsj && git checkout claude/bold-sagan-dskrsj` e trabalhe nele. O hook `boot.sh` (SessionStart) instala dependencias, conserta o certificado da voz (certifi), recria a fila de `fila_principal.txt` e relanca fila/watchdog.
- Ferramenta atual: v12 (Gemini) + correcoes de 23/11: fisica (boneco nao atravessa boneco nem objeto), dicionario universal de acoes por RAIZ do verbo (qualquer conjugacao), montado a cavalo com tiro, carros em tamanho real com rodas girando e animacao pela palavra (pulou/voou/decolou/pousou/rampa de cabeca para baixo/espaco), cenario variado (>=4 lugares, salas diferentes), camera variada, interior "galpao", close de objeto mirando o centro real (achatado = de cima), navio a vela antes de 1820, CHAMADA FINAL automatica ("Agora nao deixe de comentar: qual deve ser o tema do proximo video?"). Detalhes: `ferramenta-shorts/PROTOCOLO_ACAO.md` §19.
- **PESQUISA VISUAL OBRIGATORIA (ordem do Gibson 23/11):** todo roteiro (novo ou refeito) pesquisa a HISTORIA e a FONTE VISUAL (fotos, quadros, videos): onde, quando (dia/noite/estacao), quem, roupas da epoca, cenario real, objetos/utensilios/veiculos, e preenche `"visual"` no topo do beats.json (formato em `GUIA_DO_ROTEIRISTA.md` "Pesquisa visual"). Depois ajusta figurino/cenario/props a ela, tira fala entre aspas sem fonte e fato nao confirmado, e modela no Blender o que faltar (`blender/objetos_curadoria.py`, `formas.py`). Sem `"visual"` completo o mkvideo acusa risco e nao renderiza.
- Refacao de TODOS os videos com a ferramenta nova: fila principal (`fila_principal.txt`, 16 roteiros JA CURADOS: roadsterpulo2026, toledo, karansebes, porco, losangeles, kiska, texel, paris, petrich, hayha, kekule, postit, goodyear, curie, abelhas, tulipas); sessao A (`fila_sessao_A.txt`, 19) e sessao B (`fila_sessao_B.txt`, 18) fazendo a curadoria e o render das delas. Nada antigo e' entregue: so' a versao refeita, conferida (storyboard + grade de acoes + conferir.sh + auditar_acoes.sh) e sem defeito.
- Sessoes de producao (mesma conta; guiar com send_message terminando em "Nao responda por mensagem."): A = `session_01HE8Dy2wiQov2uhW6ZYikBX` (branch claude/prod-a2), B = `session_01HE8Dy2XpEMgdYAHCmWZFay` (branch claude/prod-b2). Videos delas chegam por `bash receber_das_sessoes.sh`. PAUSADAS em 23/11 a pedido do Gibson; ao retomar, a 1a ordem a elas e': `bash sync_ferramenta.sh` (as duas ainda estavam com mkvideo.py/runtime.js diferentes da principal) e religar o loop de sync a cada 1 MINUTO (ordem do Gibson 24/11; `sleep 60`). Ronda horaria (trigger) desativada; fila principal parada (fila em fila_principal.txt).
- Licoes do storyboard (corrigir antes de aprovar): palavra "plateia/multidao" enche a tela de gente (use "convidados" quando a cena e' de objeto); objeto grande precisa de plano aberto com camera mirando nele (cx/cz/h/d0/d1 no beat); "fachada": false e "regiao" certa para nao aparecer predio de cidade no campo.

## ESTADO EM 24/11 — FERRAMENTA v13 (leia junto com o de 23/11)
- Piloto do Roadster avaliado em "50%" pelo Gibson (sem propulsao embaixo do carro, carro nao voou, explicacao com personagem, "fazendinha" no fundo). Pente fino v13 feito: `ferramenta-shorts/PROTOCOLO_ACAO.md` §20 e `GUIA_DO_ROTEIRISTA.md` "v13".
- Regras novas para TODO roteiro: frase de ciencia/mecanismo = cena `"explica"` SEM personagem (ou `"hud"`); "o carro/objeto decolou, voou, pulou, pousou" = cena do objeto com VFX preso nele; cenario tematico (outback/mountain/countryside...) so' com tema pedido, senao `loc_*`; objeto fora de epoca bloqueia; 1a frase sem data; 55-75 s. Conferir `stories/<id>/orquestracao.json` (4 metricas em 100%).
- Producao segue PAUSADA (arquivo `ferramenta-shorts/PAUSA`; apagar para religar fila/watchdog). O Roadster so' e' refeito depois do "pode" do Gibson; ao refazer: `"set": "loc_pista"`, `explica` nas frases dos propulsores e do zero a cem, voo com VFX. Sessoes A/B: ao retomar, `bash sync_ferramenta.sh` primeiro.
- v13b (mesmo dia, 2a rodada de ordens): QUATRO folhas (a 4a e' a PESQUISA: `python3 pesquisar.py <id>` baixa prints e monta `referencias/<id>/moodboard.jpg`; OLHAR antes do storyboard; a fila roda sozinha); herois (um ou varios); tamanho real de todo objeto grande; queda sem corpo dentro do chao; medidor de km/h = carro correndo. Detalhes: PROTOCOLO_ACAO §21 e GUIA "v13b".
- v13c (3a rodada, apos o piloto da Guerra do Porco): CRONOGRAMA por video (`stories/<id>/cronograma.md`, 14 etapas; seguir a ordem), embarcacao da epoca modelada e pintada, batalhao de 32/48 em blocos por farda, multidao nunca clona personagem, cidade so' com tema de cidade, guerra sem tiro sem explosao. REGRA: defeito achado num video = corrigir NA FERRAMENTA + teste em `teste_ferramenta.sh` (PROTOCOLO_ACAO §22, GUIA "v13c").
- SINCRONIA A CADA 1 MIN (ordem do Gibson 24/11): sessoes A/B puxam a ferramenta a cada 60 s (`sync_ferramenta.sh` em laco; `boot.sh` religa). O `make_video.sh` carimba os trechos com a versao do motor: ferramenta atualizada no meio = video renderizado INTEIRO de novo na versao nova (nunca metade antigo, metade novo).
- A sincronia e' AUTOMATICA POR SCRIPT (`ferramenta-shorts/garantir_sync.sh`): liga sozinha no inicio da sessao (boot.sh, antes da trava de pausa), a cada mensagem (hook UserPromptSubmit) e antes de cada video (run_queue.sh). Ninguem precisa mandar sincronizar.
- SESSOES A/B ZERADAS em 24/11 (ordem do Gibson): as antigas foram ARQUIVADAS (branches antigos claude/prod-a-karansebes e claude/prod-b-emus ficam no GitHub so' como copia; os 37 roteiros curados e os objetos 3D delas ja estao na principal). NOVAS: A = `session_01HE8Dy2wiQov2uhW6ZYikBX` (branch claude/prod-a2), B = `session_01HE8Dy2XpEMgdYAHCmWZFay` (branch claude/prod-b2), Sonnet 5.5, nascidas PARADAS. Elas NAO editam o motor; defeito de ferramenta vem por `ferramenta-shorts/pendencias_motor/<A|B>_<id>.md` + send_message para a principal.
- NAO usar agentes/subagentes/workflows (ordem repetida em 24/11).

## REGRA MESTRA (ordem do Gibson, 19/11) — vale acima de todas as outras
1. **Nunca informe um problema ao Gibson sem antes já ter resolvido.** Achou o defeito: corrige, confere (teste, quadro, folha de contato) e só então conta o que estava errado e como ficou.
2. **Todo erro encontrado é PRIORIDADE MÁXIMA:** para o que estiver fazendo, resolve primeiro, depois informa as falhas (já corrigidas) no relatório.
- Não pergunte se deve corrigir; não entregue "achei X, quer que eu arrume?"; não deixe nada pela metade. Ordem dele = fazer tudo de uma vez.
- **ZERO RESSALVA (ordem do Gibson, 19/11):** nenhum vídeo é entregue com ressalva, nem de acabamento (prédio de outra época, árvore na frente da câmera, briga que não aparece). Viu defeito = refaz antes de entregar. Vídeo de sessão com defeito = devolve para a sessão refazer e só entrega depois de corrigido. Verificação completa em todo vídeo (sem economizar cota).
- Só fale de um problema ainda aberto se for IMPOSSÍVEL resolver daqui (ex.: acesso/credencial que só ele tem). Aí diga o que já fez, o que bloqueia e o único passo que falta dele.

Resumo das ordens do Gibson (valem para toda sessão):
- QUATRO FOLHAS por vídeo (a 4ª é `folha4_pesquisa.md`, ver ESTADO 24/11). As três primeiras: `./novo_video.sh <id>` gera `stories/<id>/folha1_roteiro.md` (história, narração, som), `folha2_producao.md` (cenário, câmera, takes, personagens, objetos, RISCOS com a correção) e `folha3_acao.md` (CATÁLOGO DE AÇÕES frase por frase: cada ação do roteiro, o instante e a animação executada; "FALTA" trava o render). Só renderiza com 0 risco e 0 ação faltando. Catálogo geral: `CATALOGO_ACOES.md`. Ao escrever o roteiro pense nos contras: cada frase precisa de algo que a ferramenta mostra (ex.: chegada de barco/tropa = plano aberto no `harbor`).
- BIBLIOTECA 3D PRIMEIRO: animais (todos) e 80+ objetos JÁ ESTÃO PRONTOS e entram sozinhos quando a narração cita (veja `CAPACIDADES.md`). NUNCA modele animal; só modele objeto que a folha 2 marcar como FALTA. Pré-checagem antes do render (OPERACAO.md, "Lições de 18/11").
- CORRIGIR SEM PERGUNTAR: defeito visto na folha de contato (personagem cortado, cena vazia, texto cobrindo legenda, luz estourada, objeto herói sumido, personagens parados) é corrigido na hora (`./refazer.sh <id> bN` ou `./refazer_tudo.sh <id>`). Para o Gibson vai só o relatório. Defeito de acabamento TAMBÉM se refaz (ZERO RESSALVA).
- TODO VÍDEO: objeto herói com close; 2 grandes momentos; mínimo 2 planos abertos; personagens interagindo e com expressões variadas; efeito + som nas palavras de ação; mapa quando cita lugar; histórias e personagens originais; série Guerras Inusitadas com EP no título.
- STORYBOARD OBRIGATÓRIO: a fila gera `stories/<id>/storyboard.jpg` e só renderiza depois de você OLHAR e rodar `./aprovar_storyboard.sh <id>`.
- Entregar o mp4 ORIGINAL (1080×1920) pelo chat, depois de `./conferir.sh <id>` e de OLHAR a folha de contato. Commit + push no branch de trabalho ao terminar.
- Não editar o motor (`web/`, `mkvideo.py`) só para fazer um vídeo; nunca rodar `build3.sh`/`fit.sh`/`shot.mjs`/`storyboard.mjs` na pasta da fila enquanto ela roda; manter sempre uma espera em segundo plano (a máquina dorme se a conversa fica ociosa).
Fila: `cd ferramenta-shorts && bash status.sh` | `bash run_queue.sh` (ids em `queue.txt`). Retoma sozinha após reinício (hook em `.claude/settings.json`).

## Session Recovery (auto-generated by context-recovery hook)

**Branch:** claude/bold-sagan-dskrsj

**Recent commits:**
- 696f0e5 progresso (tulipas em render)
- 6adbcf5 batalha automatica so com tropa em cena (civil atirando nao vira multidao de clones); Porco b3/b4 na lista de refacao
- 1108315 tulipa no Blender (vasos e canteiro), flor na mao, acao de discutir, close de objeto alto; Tulipas refeito do zero em campo holandes; EP 06 Porco renderizado
- 62e48bb ckpt(porco1859): pronto
- 9a47742 ckpt(porco1859): trecho 12

**In-progress files (5):**
- ferramenta-shorts/mkvideo.py
- ferramenta-shorts/stories/tulipas1637/fit.js
- ferramenta-shorts/web/runtime.js
- ferramenta-shorts/web/story.js
- ferramenta-shorts/stories/tulipas1637/stages/style

**Project reminders:**
- Verify the file content before claiming an edit is done
- Run tests before declaring task complete
- Re-read CLAUDE.md if you're unsure of project conventions

**Hook generated:** 2026-11-17 23:26:39 UTC
<!-- post-compact-recovery-end -->

<!-- post-compact-recovery-start -->
## Session Recovery (auto-generated by context-recovery hook)

**Branch:** claude/bold-sagan-dskrsj

**Recent commits:**
- 93ddb6b6 Trava PAUSA: reinicio do ambiente nao religa fila/watchdog/auto-aprovacao (producao parada para o pente fino v13)
- 173d98f0 ckpt(karansebes): pronto
- ee3fa7c8 ckpt(karansebes): trecho 11
- fd9a517b ckpt(karansebes): trecho 13
- 7dc6e03e ckpt(karansebes): trecho 12

**Project reminders:**
- Verify the file content before claiming an edit is done
- Run tests before declaring task complete
- Re-read CLAUDE.md if you're unsure of project conventions

**Hook generated:** 2026-11-23 23:36:45 UTC
<!-- post-compact-recovery-end -->
