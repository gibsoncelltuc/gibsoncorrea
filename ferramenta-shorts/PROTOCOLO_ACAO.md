# PROTOCOLO DE ACAO (ordem do Gibson, 19/11) — o video MOSTRA tudo o que a narracao conta

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
