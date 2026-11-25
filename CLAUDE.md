# Projeto: shorts animados (ferramenta-shorts/)
Usuário: Gibson, fala português. Responda sempre em português, curto e honesto. NÃO use agentes/subagentes nem workflows (consomem a cota dele).
**ANTES DE TUDO leia `ferramenta-shorts/COMO_OLHAR.md` (como pensar, olhar e agir igual a sessao principal; abra as imagens de `treino_olhar/`).** **PRIMEIRO leia `ferramenta-shorts/MANUAL_SONNET.md` (manual completo de operação das 3 sessões, passo a passo, e como resolver problemas difíceis).** Depois leia `ferramenta-shorts/OPERACAO.md` e `ferramenta-shorts/PROTOCOLO_ACAO.md` (os 7 passos da fábrica, o que todo vídeo tem, o que é proibido, o que fazer quando dá errado). Depois `CAPACIDADES.md`, `GUIA_DO_ROTEIRISTA.md` e `MODO_RICKS.md`.
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
- PRODUCAO RELIGADA em 24/11 (ordem do Gibson: "distribuir os roteiros e produzir nas 3 sessoes"): PAUSA removida. Principal = `fila_principal.txt` (16, comeca pelo Roadster); A = `fila_sessao_A.txt` (19); B = `fila_sessao_B.txt` (18). Quase todo roteiro precisa de ajuste para passar nas travas v13 (etapa 4 do cronograma) antes do storyboard. AUTO-APROVACAO DESLIGADA por padrao (so' com o arquivo `AUTO_APROVAR_LIGADO`): storyboard so' e' aprovado por quem olhou. Conferencia final e entrega ao Gibson: sempre na principal.
- NAO usar agentes/subagentes/workflows (ordem repetida em 24/11).


## REVISAO FINAL FRASE A FRASE (ordem do Gibson 24/11) — vale para as 3 sessoes, sem excecao
- Padrao de qualidade = piloto do Roadster EP25. Todo mp4 (principal, A e B) passa por `bash ferramenta-shorts/revisao_final.sh <id>`: gera `out/<id>/frase_a_frase.jpg` (1 quadro por frase); ABRIR a imagem e escrever `stories/<id>/revisao_final.md` (f0..fN: OK/CORRIGIDO citando a frase + `gancho:` + `piloto:`). Frase cuja imagem nao mostra o que a narracao diz = refazer antes. Sem revisao valida: `enviar_para_principal.sh` recusa e a principal nao entrega.
- A principal confere DE NOVO, ela mesma, o frase_a_frase de todo video que chega das sessoes antes de mandar ao Gibson.
- Roteiro: gancho forte (cena 1 com impacto visual, trava "GANCHO sem impacto visual"), virada no meio, final curto + chamada para comentar.


## DIAGNOSTICO DAS FALHAS (24/11, pedido do Gibson) — onde cada defeito escapava e a trava que fecha
- Folha 2/3 (producao/acao) conferiam o ROTEIRO, nao a TELA: objeto citado escondido/cortado/pequeno, camera tapada/dentro de objeto, personagem cortado, casco virando parede -> `visivel.mjs` mede no motor e `autocorrigir_visibilidade.py` conserta sozinho (storyboard nao aprova com falha).
- Ferramenta (padroes ruins): farol como fachada no cais; regra "nada na frente" jogava o objeto heroi para fora do quadro; estimativa de duracao otimista; nome de veiculo sem pasta -> corrigidos no motor + teste.
- Roteiro/coerencia: predios de outro pais, regiao inexistente, lados de batalha com a mesma farda, gancho com data/ressalva -> `checagem_coerencia.py` (R1-R4) trava o render.
- Folha 4 (pesquisa) nao era cruzada com a producao: a R1 agora cruza o lugar (mapa) com os predios.
- ENQUADRAMENTO NA FONTE (pedido do Gibson): `enquadrar.py` roda antes do mkvideo e a folha 2 ganha `folha2_enquadramento.md`: para cada objeto da cena diz LUGAR (fundo atras dos personagens / meio ao lado / frente entre eles), TAMANHO NA TELA, RELACAO com os personagens e CAMERA; a cena e' montada com esses numeros (posicao, escala, distancia e mira calculadas pelo tamanho real do modelo). `"quadro_manual": true` na cena respeita o que o roteiro definiu.
- FICHA DENTRO DAS FOLHAS (pedido do Gibson 24/11): `ficha_nas_folhas.py` (roda depois de todo mkvideo) completa a FOLHA 2 de cada cena com FICHA TECNICA (local, camera, personagens com posicao, cada objeto com lugar/tamanho/estado, efeitos, som, texto) + TAKES (quantos, duracao, angulo de cada um) e a FOLHA 3 com FISICA E MOVIMENTO de cada acao. A ficha MANDA: `max_wide` sobe sozinho para o motor nao trocar plano aberto por plano de grupo.
- REVISAO EM LISTA UNICA (pedido do Gibson): `lista_revisao.py` gera stories/<id>/lista_revisao.md com TODOS os achados automaticos + uma linha por frase. Revisor fecha a lista inteira antes de devolver; quem refaz corrige todos os itens de uma vez e responde item por item. Limite: 1 refacao por video (contada em stories/<id>/refacoes.txt).
- Ainda no olho: acao citada que existe no catalogo mas nao se le na tela (ex.: saque, beber) -> grade de acoes + frase a frase.

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
- 30c3c71a ckpt(jenkins1739): pronto
- b2fb43f4 ckpt(jenkins1739): fim da sessao de render
- a369b664 ckpt(jenkins1739): etapa gate
- 9d58c2c2 ckpt(jenkins1739): etapa fit
- a6ff3abf ckpt(jenkins1739): etapa style

**In-progress files (81):**
- ferramenta-shorts/referencias/zz_coelho/DOSSIE.json
- ferramenta-shorts/referencias/zz_coelho/FICHA.md
- ferramenta-shorts/stories/banquinho1900/autocorrecoes.md
- ferramenta-shorts/stories/banquinho1900/cronograma.md
- ferramenta-shorts/stories/banquinho1900/folha2_producao.md
- ferramenta-shorts/stories/banquinho1900/folha3_acao.md
- ferramenta-shorts/stories/banquinho1900/lista_revisao.md
- ferramenta-shorts/stories/banquinho1900/precheck.jpg
- ferramenta-shorts/stories/banquinho1900/storyboard.cenas
- ferramenta-shorts/stories/banquinho1900/storyboard.hash
- ferramenta-shorts/stories/banquinho1900/visibilidade.txt
- ferramenta-shorts/stories/lagosta1961/autocorrecoes.md
- ferramenta-shorts/stories/lagosta1961/cronograma.md
- ferramenta-shorts/stories/lagosta1961/folha2_producao.md
- ferramenta-shorts/stories/lagosta1961/folha3_acao.md
- ferramenta-shorts/stories/lagosta1961/lista_revisao.md
- ferramenta-shorts/stories/lagosta1961/precheck.jpg
- ferramenta-shorts/stories/lagosta1961/storyboard.cenas
- ferramenta-shorts/stories/lagosta1961/storyboard.hash
- ferramenta-shorts/stories/lagosta1961/visibilidade.txt
- ferramenta-shorts/stories/melancia1856/cronograma.md
- ferramenta-shorts/stories/melancia1856/fails
- ferramenta-shorts/stories/melancia1856/folha2_producao.md
- [truncated — 58 more files]

**Project reminders:**
- Verify the file content before claiming an edit is done
- Run tests before declaring task complete
- Re-read CLAUDE.md if you're unsure of project conventions

**Hook generated:** 2026-11-25 15:36:51 UTC
<!-- post-compact-recovery-end -->

## PASTA DE ENTREGA SEM MISTURA (ordem do Gibson 24/11)
- `videos_prontos/<serie>/` tem SO' videos aprovados no padrao novo (conferidos frase a frase pela principal). Versoes antigas: `videos_prontos/_antigos_nao_entregar/` (nao entregar). Reprovados: `_reprovados/`.
- Video das sessoes chega em `videos_prontos/_a_conferir/` (receber_das_sessoes.sh); so' depois da conferencia: `bash ferramenta-shorts/aprovar_entrega.sh <arquivo.mp4>`. Video da principal: copiar de out/<id>/ para a pasta da serie depois da revisao final.

## ROTINA DA SESSAO PRINCIPAL (para qualquer modelo; escrita em 24/11 noite, antes da troca para Sonnet)
A ferramenta anda sozinha: fila (`run_queue.sh`, religada pelo boot.sh), autocorrecao de visibilidade (ate 3 voltas por cena), ficha de cena, travas de coerencia R1-R8 e de pesquisa. O papel da principal e' SO' o olho + corrigir na raiz. Laco:
1. Manter SEMPRE em segundo plano: `bash ferramenta-shorts/vigia.sh` (termina com 1 linha; tratar e relancar).
2. `STORYBOARD <id>`: Read `stories/<id>/storyboard.jpg` + `videos/<id>/beats.json` (frase de cada cena). Para cada cena: a imagem mostra o que a frase diz? (gente citada presente, objeto citado visivel e do tamanho certo, multidao quando a frase fala de muita gente, cenario do lugar/epoca, nenhum efeito de tiro/explosao em frase negada ou pacifica). Defeito -> corrigir o beats.json (who/props/crowd/shot/d0/d1/acoes/quadro_manual), `python3 mkvideo.py <id>`, `python3 ficha_nas_folhas.py <id>`, apagar storyboard.jpg/AGUARDA_STORYBOARD/visibilidade.json (a fila refaz). OK -> escrever `stories/<id>/revisao_storyboard.md` (linhas bN, `pesquisa:`, `defeitos procurados:`) e `./aprovar_storyboard.sh <id>` (se recusar por folha desatualizada: rodar mkvideo + ficha_nas_folhas e repetir).
3. `PRONTO_PRINCIPAL <id>`: `./conferir.sh <id>` e `bash revisao_final.sh <id>`; Read `out/<id>/frase_a_frase.jpg`; escrever `stories/<id>/revisao_final.md` linha a linha (f0..fN, `gancho:`, `piloto:`) e rodar revisao_final de novo. Copiar o mp4 de out/<id>/ para `videos_prontos/<serie>/`, `touch stories/<id>/ENTREGUE`, mandar ao Gibson (SendUserFile). Defeito numa cena: corrigir beats + `echo "<id> bN" >> refazer.txt` (a fila refaz antes do proximo).
4. `NOVO <branch> <id>` (sessao A/B): `bash ferramenta-shorts/frase_a_frase.sh <branch> <id> <mp4 em _a_conferir> <saida.jpg>`, Read e olhar frase a frase. OK -> `bash ferramenta-shorts/aprovar_entrega.sh <arquivo>` e mandar ao Gibson. Defeito -> mover para `_reprovados/` e send_message com LISTA UNICA e valores exatos (who/props/shot/d0...). 1 refacao por video; na 3a volta a principal assume o video na fila dela (copiar videos/<id> e stories/<id> do branch da sessao, apagar DONE/SKIP/STORYBOARD_OK, por na queue.txt).
5. `FALHOU`/`SKIP`: ler `logs/make_<id>.log`. Disco cheio: apagar ckpt/<id> de entregues. Pesquisa sem referencia: `"visual": {"buscas": {"<item>": "<termo em ingles>"}}` no beats + `python3 mkvideo.py <id>` + `python3 pesquisar.py <id>`, olhar `referencias/<id>/moodboard.jpg`, descartar print errado em `referencias/<id>/prints_ruins.txt`.
6. Defeito que vem da FERRAMENTA (padrao que vai se repetir): corrigir no motor/checagem + linha em `teste_ferramenta.sh` (`bash teste_ferramenta.sh` tem que dar OK). Mudanca em web/*.js, mkvideo.py ou audio_story.py faz os renders em andamento recomecarem (aqui e nas sessoes): aplicar entre um render e outro e em lote; guardar o patch em `pendencias_motor/` se nao for a hora.
7. Commit + push no branch a cada passo.
PATCH DE MOTOR da negacao ('o tiro nunca veio'): APLICADO 24/11 19:58.
MELANCIA: trecho 9 saiu com 95/150 quadros (disco cheio); seg apagado e DONE removido: a fila refaz o trecho; depois conferir (o conferir.sh agora reprova video mais curto que a voz).
PENDENCIAS EM 24/11 19:35: Lagosta b7 na refazer.txt (depois: revisao_final ja quase pronta, so' conferir b7 "o tiro nunca veio" sem explosao); Gansos na fila principal (b6 Manlio empurra/gaules cai, b9 gansos 1.7) -> olhar storyboard; Aroostook em videos_prontos/_a_conferir (conferir); Chaleira (A), Emus (A), Danca (B) devolvidos com lista unica; Tulipas, Curie e Post-it: storyboards refeitos esperando o olho. DECISAO DO GIBSON EM ABERTO: chamada final (manter "qual deve ser o tema do proximo video?" ou trocar por pergunta curta ligada a historia) -> nao mudar sem ele.

## REFAZER SO' O TRECHO (pedido do Gibson 24/11)
- `cenas_hash.py <id>` = impressao digital de cada cena (linha S('bN') do spec + ajuste de camera) e do global (motor de desenho web/*.js, voz, cabecalho/figurinos). Guardada em ckpt/<id>/cenas.txt a cada render.
- Mudou so' cena(s): a fila refaz so' os trechos de 150 quadros dessas cenas e remonta (log "so' estas cenas mudaram"). Mudou o global: video inteiro (nunca metade antigo, metade novo). Defeito numa cena ja renderizada: corrigir beats + `echo "<id> bN" >> refazer.txt`.

## SENTIDO + SUSPEITAS + PRE-CHECAGEM (24/11 noite, pedido do Gibson: resolver os 8 pontos)
- `sentido.py`: le a FRASE inteira (negacao antes/depois, "nunca veio", hipotese "quase/pediram/ameacou", arma so' citada sem verbo de disparo, valor "preco de uma casa", "misturou as etiquetas", expressoes figuradas). Ligado no mkvideo: palavra figurada nao e' encenada; frase sem violencia real = sem tiro/batalha; "casa" valor = sem interior; mistura de papeis = sem panela. Teste: `python3 sentido.py "<frase>"`.
- `suspeitas.py <id> [--corrigir]`: frase x cena (muita gente sem multidao, animal citado sem animal, frase pacifica com explosao, tiro real sem tiro, noite de dia, ar livre dentro de sala). A fila roda com --corrigir antes de montar (corrige animal e multidao sozinha); o resto vai para a lista_revisao como SUSPEITA = olhar primeiro.
- Cenario padrao: navio padrao do porto some quando a cena traz o navio da historia (_NAV_PROPRIO); navio posto no cais vai para a agua.
- `PRECHECK_ROTEIROS.md`: todas as travas rodadas nos 56 roteiros que faltam (42 com pendencia de texto: gancho longo, abre com data, video > 66 s, falta explica, sem pesquisa visual). Cada sessao corrige os DELA antes do storyboard.

## REVISAO GERAL DOS 50 ROTEIROS (24/11 23h, ordem do Gibson: "parar tudo, corrigir tudo, depois renderizar do comeco")
- As 3 sessoes foram paradas; a principal corrigiu TODOS os 50 roteiros pendentes (13 principal + Tulipas, 19 A, 17 B) frase a frase e cena a cena: 0 risco, 0 suspeita, coerencia OK. Renders/storyboards antigos apagados; as 3 filas religadas do comeco (queue.txt de cada uma).
- Regras novas na ferramenta (suspeitas.py --corrigir roda sozinho na fila; teste_ferramenta.sh cobre): celular/app/internet sem tela (celular so >=2007, TV >=1950); congresso/assembleia/eleitores = multidao; BATALHA escondida em frase sem luta e' desligada; MULTIDAO SEM MOTIVO em cena intima e' tirada; momento automatico nunca dentro de sala; tropa/armas so' em cena de luta; "Batalha dos X" (nome de evento) nao e' luta; "ninguem atirava" sem tiro; duracao nao usa voz de texto antigo.

## LEITURA ESCRITA DE CADA FRASE (25/11, pedido do Gibson: "solucao definitiva para a ferramenta entender o contexto")
- A ferramenta (codigo) nao entende frase; quem entende e' a IA. Toda frase leva no beats.json o "encena": {"sentido": afirmativa|negativa|hipotese|figurada|fato, "passos": [{quem, faz, alvo, na}]} escrito por quem LEU a frase (encenacao.py; GUIA "LEITURA ESCRITA"). A ferramenta so' executa; a folha 3 mostra a leitura passo a passo.
- aprovar_storyboard.sh RECUSA sem leitura em todas as frases. Passo com verbo que a ferramenta nao tem = FALTA ANIMACAO (trava): construir a animacao, nunca pular.
- Procedimento: rascunho automatico (stories/<id>/leitura.md) -> a IA LE e escreve com `encenacao.py revisar <id>` -> mkvideo -> `encenacao.py conferir` (mao dupla) -> `forcar` se preciso. A leitura MANDA: acao fora dela nao acontece. Fila principal 100% revisada em 25/11.
- Novos verbos de 25/11: anda_ate (entra andando ate o objeto), entra_em (entra e senta DENTRO do recipiente), transborda (agua azul espirrando pela borda na palavra).

- NUNCA editar make_video.sh/run_queue.sh com a fila rodando (bash le o script aos pedacos: edicao no meio = "syntax error" e o video para depois do render). Editar so' com a fila parada ou entre um video e outro.

## ESTRUTURA VIRAL (25/11, ordem do Gibson) — VALE ACIMA DAS REGRAS DE TAMANHO E CHAMADA FINAL
- Todo roteiro segue `ferramenta-shorts/ESTRUTURA_VIRAL.md` (documento "O roteiro vencedor para YouTube Shorts 2026"): 6 blocos por cena ("bloco": gancho, promessa, prova, escalada, pagamento, loop), 30-45 s (75-110 palavras), frase de ate 12 palavras, "gancho_tipo" (perda|ganho|crenca|segredo), texto na tela no gancho, micro-prova com numero/nome antes dos 20 s, final em LOOP (ultima frase emenda na primeira; a ultima imagem repete a 1a cena sozinha), SEM chamada falada para comentar, "loop_frase_ok" e "gancho_cumprido" no topo.
- `python3 estrutura_viral.py <id>` confere; `--todos` faz a varredura (VARREDURA_ESTRUTURA.md). mkvideo TRAVA roteiro fora da estrutura.
- TODOS os videos (inclusive os ja entregues) serao refeitos com as mesmas historias e titulos. Piloto: scilly1651 (roteiro antigo em videos/scilly1651/beats_v24.json). Fila antiga guardada em queue_antes_viral.txt.
- 25/11 noite: os 85 roteiros foram REESCRITOS pela principal (planos em ferramenta-shorts/planos_viral/<id>.json, aplicados com reescrever_viral.py; roteiro antigo em videos/<id>/beats_v24.json). Varredura 85/85. Os 37 videos antigos sairam da pasta de entrega (videos_prontos/_antigos_nao_entregar/estrutura_antiga_25-11/). Filas: principal = fila_principal.txt (queue.txt), A e B = as suas; E Se #PAUSADO seguem pausados. petrich1925 e' duplicado de cachorro1925 (fora das filas).
- Duracao: estrutura_viral.py conta palavras FALADAS (ano = 6) a 2,75/s e usa a voz real quando existe; limite 45 s.
- 2a PASSADA (25/11 noite, pedido do Gibson: 'resolva onde esta fraco'): gancho proprio em cada video (proibido 'Ninguem te conta'), LOOP de verdade (ultima frase termina aberta '...e foi assim que...' e a 1a completa), 30-36 s (palavras faladas, ano = 6) e voz +20% (medido: 95 palavras = 34 s). Travas novas no estrutura_viral.py (formula, loop aberto, 36 s, ganchos repetidos na varredura). Texto por lote em ferramenta-shorts/lotes2/*.json, aplicado com segunda_passada.py. Varredura 84/84 (petrich1925 = duplicado, fora).
