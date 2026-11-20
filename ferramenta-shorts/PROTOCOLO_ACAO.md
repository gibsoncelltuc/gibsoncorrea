# PROTOCOLO DE ACAO (ordem do Gibson, 19/11) — o video MOSTRA tudo o que a narracao conta

## REGRA MESTRA (ordem do Gibson, 19/11) — vale acima de todas as outras
1. **Nunca informe um problema ao Gibson sem antes já ter resolvido.** Achou o defeito: corrige, confere (teste, quadro, folha de contato) e só então conta o que estava errado e como ficou.
2. **Todo erro encontrado é PRIORIDADE MÁXIMA:** para o que estiver fazendo, resolve primeiro, depois informa as falhas (já corrigidas) no relatório.
- Não pergunte se deve corrigir; não entregue "achei X, quer que eu arrume?"; não deixe nada pela metade. Ordem dele = fazer tudo de uma vez.
- Só fale de um problema ainda aberto se for IMPOSSÍVEL resolver daqui (ex.: acesso/credencial que só ele tem). Aí diga o que já fez, o que bloqueia e o único passo que falta dele.

Regra de ouro: **cada frase do roteiro e' uma cena, e cada verbo de acao da frase acontece na tela, no instante da palavra.**
A ferramenta faz isso sozinha (MODO DE ACAO no mkvideo.py) e TRAVA o render quando nao consegue (risco "ACAO SEM ANIMACAO").

## 1. Como a ferramenta le o roteiro (frase por frase)
1. LUGAR: o lugar citado vira o cenario (praia -> areia com mar; estadio -> arquibancada lotada; hospital; fazenda; deserto...) + MAPA do pais/cidade + MARCO do lugar (so se ja existia no ano).
2. EPOCA: o ano (titulo, id, placa ou "mil oitocentos e...") escolhe farda, chapeu, carro, chao (terra/pedra/asfalto) e cavalaria.
3. QUEM: cada codigo de figurino e' um personagem; soldados com codigo de pais (ING, FRA, ALE, EUA...) ganham a farda do exercito.
4. ACOES (vocabulario abaixo): verbo -> gesto do personagem + objeto + efeito + som NA PALAVRA.
5. EMOCAO: palavra de sentimento -> o rosto muda na palavra e a camera fecha no rosto.
6. VERIFICACAO: verbo de acao sem animacao = risco que impede o render. Corrija o roteiro ou marque a cena.

## 2. Vocabulario de acoes (o que a ferramenta ja encena)
- GUERRA: "chegaram de navio / desembarcaram" -> navios chegando e tropa descendo na praia | "estava esperando / emboscada" -> batalhao parado com a placa "BATALHAO <nome>" |
  "comecou a batalha / avancaram um contra o outro / atacaram" -> os DOIS exercitos correndo um contra o outro, tiros, canhoes | "bomba / explodiu / voaram" -> explosao e soldados voando girando |
  "atirou / pegou a espingarda" -> arma na mao, aponta, clarao | ate 1918: cavalaria | "marchavam" -> tropa marchando | "rendeu-se" -> maos para cima | "invadiu / entrou escondido" -> chega andando.
- CONVERSA E PAZ: "conversaram / negociaram / reuniram / discutiram" -> os dois conversando, gesticulando | "apertaram as maos / fizeram as pazes / tratado" -> aperto de mao + brilho |
  "brigou / discutiu" -> bate-boca | "pediu / implorou" -> plano medio, um suplicando ao outro | "abracou" -> abraco | "entregou / pagou / vendeu / comprou" -> entrega + moeda.
- PROCESSO E INVENCAO: "misturou / mexeu" -> panela borbulhando | "caiu / jogou / derramou" -> material voa e cai no alvo | "esquentou / ferveu / fogao" -> vapor | "virou / endureceu / nasceu" -> o produto surge girando |
  "construiu / montou" -> martela e o objeto cresce | "examinou / descobriu / mediu" -> lupa / microscopio / balanca | "quimico / experiencia" -> frasco e tubos | "escreveu / assinou" -> escrevendo | "cavou" -> poeira | "cortou arvore" -> machado e toras.
- CORPO: "caiu no chao / nocaute / desmaiou" -> cai sentado no chao | "dormia" -> dormindo | "sentou" -> sentado | "foi embora / voltou para casa / partiu" -> sai andando pela lateral | "correu / fugiu" -> corrida |
  "pensou / percebeu" -> mao no queixo + brilho | "olhou / viu / apontou" -> aponta | "gritou / venceu / comemorou" -> bracos para cima | "perdeu / fracassou" -> mao na testa | "socou / lutou (luta)" -> soco | "raspou a cabeca" -> maquina + cabelo voando.
- MUNDO: "desabou / afundou / ruiu" -> nuvem de poeira e tremor | "pegou fogo / queimou" -> fogo e fumaca | "sirenes / sinos tocaram" -> onda de som | "luzes apagaram" -> noite | "decolou / voou" -> poeira no chao, olhar para cima | "votaram / urnas" -> urna | "tirou foto / selfie" -> celular e flash.
- ANIMAIS: animal citado entra em cena; em cena andando ele anda junto.

## 3. Como escrever o roteiro para a acao aparecer
- Uma acao concreta por frase, com o VERBO e o OBJETO: "o fazendeiro pegou a espingarda e atirou no porco", "a gosma caiu no fogao quente".
- Diga ONDE: "na praia", "no ringue", "no hospital", "na Casa Branca".
- Diga QUEM: nome/cargo do personagem que esta em "who".
- Evite frase que so comenta ("foi incrivel"); se precisar, junte com uma acao.

## 4. Objeto que nao existe na biblioteca (ordem do Gibson)
TODO objeto novo e' modelado a partir de REFERENCIA REAL da internet: pesquisar imagens ("<objeto> photo"), tirar um print (firecrawl_scrape da pagina de resultados com formato screenshot,
baixar o PNG de storage.googleapis.com) e modelar no Blender com os detalhes da foto (ex.: moeda de bitcoin com borda serrilhada, anel de texto, circuitos, B em relevo).
Sessoes sem ferramenta de busca: anotar em "FALTA MODELAR" da folha 2 e pedir a sessao principal.

## 5. Verificacao antes do render (obrigatorio)
`python3 mkvideo.py <id>` -> folha2_producao.md lista os riscos. "ACAO SEM ANIMACAO na narracao: X" = a cena nao mostra X. Corrija e rode de novo. So renderiza com 0 risco.
Prechecar a cena (`./prechecar.sh <id> bN 6`) e OLHAR se a acao acontece; para o instante exato: `FRAMES=640,650 ./prechecar.sh <id> bN`.

## 6. FOLHA 3 - ACOES (obrigatoria em todo projeto)
`python3 mkvideo.py <id>` gera `stories/<id>/folha3_acao.md`: cada frase (cena bN, inicio e fim em segundos, numero de palavras) com a tabela das acoes catalogadas
(palavra + instante, tipo, animacao que a ferramenta executa, OK/FALTA). Linha "FALTA" = acao do roteiro sem animacao -> nao renderiza.
O resumo de todos os videos fica em `CATALOGO_ACOES.md`. A ferramenta so faz o que o ROTEIRO pede: cada video tem as acoes da sua propria historia (o exemplo da batalha na praia era so' um exemplo).
- Na batalha (tiros/explosoes): soldados caem no chao ao longo da luta; explosao/canhao/bomba joga soldados voando no meio da tropa.
- Animais: "comendo" -> fuca/bica; "entrou/chegou/apareceu" -> entra caminhando; "fugiu/correu" -> sai correndo; "atirou/matou" o animal -> cai (desenho, sem sangue); "assustou/latiu" -> alerta.

## 7. GRAVIDADE (fisica de verdade)
Boneco de ~3,15 m representa pessoa de 1,75 m -> escala 1,8 -> g da cena = 9,8 x 1,8 = 17,6 m/s2 (GRAV no mkvideo). Tudo que sobe e cai segue projetil (sobe desacelerando, cai acelerando):
pulo (sobe 1,2 m, ~0,74 s; "todo mundo pula" -> a multidao inteira pula), soldado arremessado pela explosao (1,6 s no ar, sobe ~5,6 m), material que cai no alvo (parabola), bola chutada (parabola).
A folha 3 mostra a fisica de cada uma dessas acoes.
## 8. Mais acoes do corpo
correr / sair correndo / fugir -> sai correndo pela lateral + poeira | pular / saltar -> pulo com gravidade | acenar / despedir -> acena | empurrar / puxar / arrastar -> empurra |
deitar / ajoelhar -> abaixa | atirar / disparar -> arma na mao, aponta, clarao e som.

## 9. BLOQUEIO DAS 3 FOLHAS (o render nao roda sem elas)
`make_video.sh` roda `python3 verificar_folhas.py <id>` antes do render e `--render` depois de montar: BLOQUEIA se faltar folha, se alguma estiver desatualizada,
se a folha 2 tiver risco, se a folha 3 tiver acao FALTANDO, se a folha 3 tiver sido mexida a mao ou se a producao (spec.js / web/story.js) nao carregar a assinatura da folha 3 atual.
Conferir na mao: `python3 verificar_folhas.py <id>` -> "3 FOLHAS OK: lidas e seguidas".
## 10. Mais acoes gerais (gesto + objeto/efeito + som na palavra)
beber, comer, chorar, cantar, ler, telefonar/postar, lavar/limpar, beijar/abracar, plantar/colher, pescar, costurar, pintar/desenhar, cozinhar, bater, procurar, vigiar, bater continencia, rezar,
aplaudir, acordar (estava dormindo), esperar (bracos cruzados), tremer, tossir/espirrar, nadar/mergulhar, rir, abrir/fechar, soltar/libertar, entregar/receber, medir/contar, apresentar/mostrar.

## 11. STORYBOARD OBRIGATORIO ANTES DO RENDER (ordem do Gibson 19/11)
A fila (make_video.sh) gera `stories/<id>/storyboard.jpg` (o video inteiro, 1 quadro a cada ~1,5 s) e PARA aquele video ate alguem aprovar; enquanto isso segue com o proximo.
Quem aprova: a sessao dona do video. ABRA o storyboard.jpg, confira cena por cena com a folha 3 (cada acao acontecendo, ninguem cortado, cenario/lugar/epoca certos, objeto heroi visivel)
e so' entao rode `./aprovar_storyboard.sh <id>`. Viu defeito -> corrija o roteiro, rode mkvideo, apague storyboard.jpg (a fila gera outro) e olhe de novo.
A aprovacao vale so' para aquela versao das folhas; o render tambem confere isso (verificar_folhas.py --render bloqueia sem storyboard aprovado).

## 12. REVISAO ESCRITA DO STORYBOARD (ordem do Gibson 19/11 — vale para TODAS as sessoes)
`./aprovar_storyboard.sh <id>` so aprova com `stories/<id>/revisao_storyboard.md` feito DEPOIS do storyboard atual, com UMA linha por frase:
`bN: OK - <o que aparece na tela nessa frase>` ou `bN: CORRIGIDO - <defeito> -> <correcao feita>`. Linha curta, sem citar a frase, ou defeito sem correcao = nao aprova.
"Igual ao que ja conferi" NAO vale: storyboard novo = revisao nova. Achou defeito: corrija (ferramenta ou roteiro), gere de novo e revise de novo (REGRA MESTRA).
GRADE DE ACOES: `stories/<id>/grade_acoes.jpg` (a fila gera junto com o storyboard; ou `./prechecar.sh <id> acoes`) tem 1 quadro no INSTANTE EXATO de cada acao da folha 3, com a palavra e a animacao escritas embaixo. Olhe quadro por quadro: a acao escrita esta acontecendo na tela? Se nao, corrija antes de aprovar. Sem grade atualizada a aprovacao e' recusada.
O que procurar em CADA frase (defeitos reais achados em 19/11):
- a acao da frase acontece? (cochilou = dormindo; morreu = cai; de joelhos = ajoelhado; atirou = arma + clarao; chegou = entra andando)
- a acao aparece a tempo? (palavra no fim da frase: objeto/pose tem que aparecer antes)
- HORA certa e CONTINUA: "numa noite" vale para as frases seguintes do mesmo episodio; "as noites no laboratorio" = escuro
- LUGAR certo: espaco = ceu preto estrelado; castelo/observatorio citado = o marco, sem predio tapando; morto so onde morreu
- QUEM faz a acao: atomos/cobras dancando no sonho nao fazem o personagem dancar; "os turcos venceram" mostra os turcos
- OBJETO certo: corte no dedo nao e machado; lareira, cadeira, microscopio citados aparecem grandes e perto
- roupa certa: astronauta de branco (nao farda); epoca e pais certos

## 13. SESSOES EM AUTOMATICO (ordem do Gibson 19/11)
Cada sessao de producao deixa rodando em segundo plano, desde o inicio:
`nohup bash -c 'while true; do ./sync_ferramenta.sh >> logs/sync.log 2>&1; sleep 600; done' > /dev/null 2>&1 &`
A cada 10 min ela puxa a ferramenta do branch principal, regenera as folhas dos videos ainda nao prontos e roda `verificar_execucao.py`.
Storyboard que mudou volta para a fila; a sessao REVISA de novo (grade de acoes + revisao_storyboard.md). Falha de execucao no log = corrigir na hora (REGRA MESTRA).
Toda revisao com defeito achado vira linha "CORRIGIDO" no revisao_storyboard.md, e o commit diz o que foi corrigido (a sessao principal confere pelo git).

## 14. REFACAO DOS VIDEOS JA PRONTOS (ordem do Gibson 19/11)
Os 63 roteiros que ja tinham video sao TODOS refeitos com a ferramenta final, divididos assim:
sessao principal = queue.txt (24) | sessao A = fila_sessao_A.txt (20) | sessao B = fila_sessao_B.txt (19).
ORDEM DE PRIORIDADE (Gibson, 19/11 tarde): 1o GUERRAS INUSITADAS e PODER E FAMA; depois Curiosidade e Ciencia; a serie "E SE" (tema novo) SO DEPOIS de todos os outros. NADA de tema novo ate terminar a refacao. Cada video: storyboard + grade de acoes + revisao_storyboard.md + verificar_execucao; so depois render; entrega so depois de conferir.sh e olhar a folha de contato.

## 15. WATCHDOG (ordem do Gibson 19/11)
- Toda sessao: o hook de inicio (boot.sh) relanca a FILA e, nas sessoes A/B, o loop do sync_ferramenta.sh assim que a maquina reinicia.
- Sessao principal: `watchdog.sh` em segundo plano verifica a cada 5 min a fila local (relanca sozinho) e as sessoes A/B (branch sem commit ha 15 min = parada) e acorda a principal para mandar a sessao retomar de onde parou.
- Tarefas agendadas a cada ~10 min na sessao principal (:04 :14 :24 :34 :44 :54) relancam o watchdog se a propria sessao principal tiver reiniciado.
- Sessao A/B que receber "WATCHDOG: retome": merge do principal, fila, sync, e continua exatamente do video/etapa onde estava.

## 16. ENTREGA PARA A CONVERSA PRINCIPAL (ordem do Gibson 19/11)
O Gibson baixa TODOS os videos na conversa da sessao principal. Sessao A/B: depois de conferir.sh e de OLHAR a folha de contato,
rode `./enviar_para_principal.sh <id>` (manda o mp4 em pedacos de 90 MB + sha256 + folha de contato pelo git). A principal roda
`./receber_das_sessoes.sh`, remonta, confere o sha256, olha a folha e manda o video no chat. Video com defeito conhecido NAO e' enviado.

## 17. ZERO RESSALVA (ordem do Gibson 19/11, acima de tudo depois da regra mestra)
Nenhum vídeo sai com ressalva. Defeito de acabamento também se corrige antes de entregar: prédio/objeto de outra época, árvore ou objeto tapando a câmera, ação que não aparece (briga parada, tiro sem tiro), cenário que não é o lugar citado. Vídeo de sessão com qualquer defeito volta para a sessão; só vai para o Gibson corrigido. Verificação completa (storyboard + grade de ações + revisão escrita + folha de contato) em TODO vídeo, sem economizar cota.

## 18. AUTO-APROVACAO DE SEGURANCA (ordem do Gibson 19/11)
`auto_aprovar.sh` roda em segundo plano nas 3 sessoes (boot.sh e sync_ferramenta.sh o relancam). Storyboard parado >45 min sem aprovacao (era 5; 20/11: com as sessoes ativas a revisao vem antes), com folha 2 sem risco e verificar_execucao 100%, e' aprovado sozinho e marcado `stories/<id>/AUTO_APROVADO`. Log: `logs/auto_aprovar.log`. Quando houver cota: REVER todo video com AUTO_APROVADO (conferir.sh + auditar_acoes.sh) antes de entregar; defeito = refazer. Nao entregue video AUTO_APROVADO sem essa revisao.
