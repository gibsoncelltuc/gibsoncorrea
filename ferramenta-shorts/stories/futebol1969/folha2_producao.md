# FOLHA 2 - PRODUCAO: Guerras Inusitadas EP 09 - A Guerra do Futebol

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/futebol1969/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py futebol1969` de novo ate esta folha sair sem risco.

## Cena b0 - Dois países entraram em guerra por causa de um jogo de futebol.
- Cenario: stadium | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): HON (variante 0, expressao angry); SAL (variante 0, expressao shout) | multidao: 16 de HON/SAL
- Animacao: conversar | interacao: aproxima-se | o ultimo personagem ENTRA andando
- Objetos/modelos: kit/ball
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): futebol, jogo
- RISCOS: nenhum

## Cena b1 - Em mil novecentos e sessenta e nove, Honduras e El Salvador já brigava...
- Cenario: street | luz: day | clima: limpo
- Camera: reveal = ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (2): TOR (variante 0, expressao stern); TOR (variante 1, expressao angry) | multidao: 8 de TOR
- Animacao: discutir
- Objetos/modelos: kit/volcano
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): -
- RISCOS: nenhum

## Cena b2 - Aí veio a disputa por uma vaga na Copa do Mundo: três jogos, um contra...
- Cenario: stadium | luz: day | clima: limpo
- Camera: aereo = - + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa -> frente | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): HON (variante 0, expressao grin); SAL (variante 0, expressao stern) | multidao: 16 de HON/SAL
- Animacao: conversar | interacao: avanca e o outro recua | o ultimo personagem ENTRA andando
- Objetos/modelos: kit/ball
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): contra, copa, disputa, vaga
- RISCOS: nenhum

## Cena b3 - No primeiro, Honduras venceu por um a zero, em casa.
- Cenario: stadium | luz: day | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (2): HON (variante 0, expressao laugh); SAL (variante 0, expressao sad) | multidao: 18 de TOR/HON
- Animacao: comemorar
- Objetos/modelos: kit/panela, buildings/house_small, nature/picket_fence, nature/tree_oak
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): zero
- RISCOS: nenhum

## Cena b4 - No segundo, El Salvador devolveu por três a zero, e a tensão explodiu ...
- Cenario: street | luz: dia | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa -> frente
- Personagens principais (2): TOR (variante 0, expressao angry); TOR (variante 1, expressao shout)
- Animacao: discutir | interacao: empurrar
- Objetos/modelos: kit/volcano
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): ruas, tensao, zero
- RISCOS: 
  - ACAO-CHAVE sem briefing de efeito (corpo + emissao + luz/camera) -> CORRECAO: por o objeto da acao em "props" (veiculo/objeto grande) para a ferramenta animar com VFX, ou "batalha"/"explica" na cena
  - a narracao fala de EXPLOSAO e nao ha explosao -> CORRECAO: "fx": ["burst@30"], "sfx": ["cannon@30"] (acerte o numero para o quadro da palavra)

## Cena b5 - Acontece que, na véspera do terceiro jogo, El Salvador cortou relações...
- Cenario: interior madeira | luz: dia | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa
- Personagens principais (2): PRE (variante 0, expressao angry, segura paper); PRE (variante 1, expressao nervous)
- Animacao: reagir | interacao: susto
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): honduras, vespera
- RISCOS: nenhum

## Cena b6 - O jogo foi na Cidade do México, e El Salvador venceu por três a dois, ...
- Cenario: stadium | luz: dia | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa -> frente | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (3): SAL (variante 0, expressao laugh); SAL (variante 1, expressao grin); HON (variante 0, expressao sad)
- Animacao: comemorar | interacao: pular
- Objetos/modelos: kit/ball, kit/trave, buildings/apartment, buildings/house_two, nature/lamppost
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cidade, dois, jogo, mexico, prorrogacao
- RISCOS: nenhum

## Cena b7 - Semanas depois, o exército salvadorenho atacou Honduras.
- Cenario: street | luz: dia | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (1): SOL (variante 0, expressao stern) | multidao: 0 de 
- Animacao: - | batalha encenada
- Objetos/modelos: vehicles/airplane, kit/volcano
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): exercito
- RISCOS: nenhum

## Cena b8 - A guerra durou cem horas, até a Organização dos Estados Americanos imp...
- Cenario: street | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa -> frente
- Personagens principais (2): SOL (variante 0, expressao nervous); PRE (variante 0, expressao stern, segura paper) | multidao: 10 de SOL/TOR
- Animacao: reagir | interacao: o outro se aproxima | batalha encenada
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cessarfogo, estados, organizacao
- RISCOS: nenhum

## Cena b9 - Na Copa, El Salvador perdeu os três jogos, sem fazer um único gol.
- Cenario: stadium | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa
- Personagens principais (1): SAL (variante 0, expressao sad)
- Animacao: conversar
- Objetos/modelos: kit/ball, kit/trave
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): copa, tres
- RISCOS: nenhum

## Cena b10 - Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?
- Cenario: stadium | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa
- Personagens principais (1): HON (variante 0, expressao grin)
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): comentar, proximo, tema
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
kit/ball | b0, b2, b6, b9 | pronto (HEROI: aparece em close) | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/volcano | b1, b4, b7 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/panela | b3 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
buildings/house_small | b3 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/picket_fence | b3 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/tree_oak | b3 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/trave | b6, b9 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
buildings/apartment | b6 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
buildings/house_two | b6 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/lamppost | b6 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
vehicles/airplane | b7 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: kit/ball | grandes momentos: b7, b8 | planos abertos: 3 | mistura: close 10% | medio 67% | aberto 16% | detalhe 7%
- Interacoes: b0 aproxima-se, b2 avanca e o outro recua, b4 empurrar, b5 susto, b6 pular, b8 o outro se aproxima
- RISCOS GERAIS: 
  - pouca variedade de cenario ({'stadium': 6, 'street': 4, 'interior madeira': 1}): o video fica parecendo todos os outros -> CORRECAO: pelo menos 3 lugares e nenhum em mais da metade das cenas: troque "set"/"interior" de algumas cenas (lugares: outback, countryside, arctic, palace, harbor, mountain, medieval, jungle, hall, stadium, street, loc_pista, loc_patio, loc_deserto, loc_campo, loc_montanha, loc_cidade, loc_estudio | interior: madeira, pedra, loja)
  - FOLHA 4: 10 item(ns) sem referencia visual: Estadios de Tegucigalpa (Honduras), San Salvador (El Salvador) e Cidade do Mexic, torcedores e jogadores de Honduras (camisa azul), torcedores e jogadores de El -> CORRECAO: por a consulta em ingles em "visual": {"buscas": {"<item>": "<consulta>"}} e rodar pesquisar.py de novo, ou registrar a referencia vista em "visual": {"referencias": {"<item>": "<url/descricao>"}}

## RESUMO: 4 risco(s) em aberto
- b4: ACAO-CHAVE sem briefing de efeito (corpo + emissao + luz/camera)
- b4: a narracao fala de EXPLOSAO e nao ha explosao
- geral: pouca variedade de cenario ({'stadium': 6, 'street': 4, 'interior madeira': 1}): o video fica parecendo todos os outros
- geral: FOLHA 4: 10 item(ns) sem referencia visual: Estadios de Tegucigalpa (Honduras), San Salvador (El Salvador) e Cidade do Mexic, torcedores e jogadores de Honduras (camisa azul), torcedores e jogadores de El

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh futebol1969 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh futebol1969` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
