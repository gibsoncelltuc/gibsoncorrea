# FOLHA 2 - PRODUCAO: Teste do Modo de Acao

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/teste_acao/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py teste_acao` de novo ate esta folha sair sem risco.

## Cena b0 - Em mil oitocentos e doze, uma batalha estranha aconteceu na costa de P...
- Cenario: harbor | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa
- Personagens principais (2): GEI (variante 0, expressao stern); GEF (variante 0, expressao stern) | multidao: 5 de POV
- Animacao: conversar | interacao: insiste
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): batalha, costa, portugal
- RISCOS: nenhum

## Cena b1 - Os navios ingleses chegaram na praia, e o batalhão desembarcou na arei...
- Cenario: harbor | luz: day | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (2): ING (variante 0, expressao stern); ING (variante 1, expressao stern) | multidao: 12 de ING
- Animacao: encena
- Objetos/modelos: navios ao fundo, navio em movimento
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): areia, batalhao, navios, praia
- RISCOS: nenhum

## Cena b2 - Mas o batalhão francês do general Dupont já estava esperando atrás das...
- Cenario: harbor | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa
- Personagens principais (2): FRA (variante 0, expressao stern); FRA (variante 1, expressao smug) | multidao: 12 de FRA
- Animacao: conversar | interacao: vai ate o outro
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): batalhao, dunas, general
- RISCOS: nenhum

## Cena b3 - Começou a batalha. Os dois exércitos avançaram um contra o outro, com ...
- Cenario: harbor | luz: day | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (2): ING (variante 0, expressao shout); FRA (variante 0, expressao angry) | multidao: 18 de ING/FRA
- Animacao: encena | batalha encenada
- Objetos/modelos: cannon
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): batalha, contra, dois, tiros
- RISCOS: nenhum

## Cena b4 - Uma bomba explodiu no meio da praia, e soldados voaram pelos ares.
- Cenario: harbor | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa
- Personagens principais (2): ING (variante 1, expressao shock); FRA (variante 1, expressao scared) | multidao: 10 de ING/FRA
- Animacao: reagir | interacao: aproxima-se | batalha encenada
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): bomba, praia
- RISCOS: nenhum

## Cena b5 - No fim da tarde, os dois generais decidiram conversar no meio do campo...
- Cenario: countryside | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa
- Personagens principais (2): GEI (variante 0, expressao stern); GEF (variante 0, expressao suspicious)
- Animacao: conversar | interacao: avanca e o outro recua
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): campo, dois
- RISCOS: nenhum

## Cena b6 - Depois de horas negociando, eles apertaram as mãos e fizeram as pazes.
- Cenario: street | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa
- Personagens principais (2): GEI (variante 0, expressao smile); GEF (variante 0, expressao smile)
- Animacao: conversar | interacao: apertar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): maos, pazes
- RISCOS: nenhum

## Cena b7 - Os soldados comemoraram, e cada exército voltou para casa.
- Cenario: harbor | luz: day | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (2): ING (variante 0, expressao laugh); FRA (variante 0, expressao laugh) | multidao: 10 de ING/FRA
- Animacao: comemorar
- Objetos/modelos: buildings/house_small, nature/picket_fence, nature/tree_oak
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): soldados
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
cannon | b3 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
buildings/house_small | b7 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/picket_fence | b7 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/tree_oak | b7 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: ship | grandes momentos: b3, b4 | planos abertos: 3 | mistura: close 3% | medio 70% | aberto 26% | detalhe 0%
- Interacoes: b0 insiste, b2 vai ate o outro, b4 aproxima-se, b5 avanca e o outro recua, b6 apertar
- RISCOS GERAIS: 
  - objeto heroi (ship) sem close de camera -> CORRECAO: por o objeto em "props" de uma cena media de 8+ palavras
  - pouca variedade de cenario ({'harbor': 6, 'countryside': 1, 'street': 1}): o video fica parecendo todos os outros -> CORRECAO: pelo menos 3 lugares e nenhum em mais da metade das cenas: troque "set"/"interior" de algumas cenas (lugares: outback, countryside, arctic, palace, harbor, mountain, medieval, jungle, hall, stadium, street | interior: madeira, pedra, loja)

## RESUMO: 2 risco(s) em aberto
- geral: objeto heroi (ship) sem close de camera
- geral: pouca variedade de cenario ({'harbor': 6, 'countryside': 1, 'street': 1}): o video fica parecendo todos os outros

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh teste_acao bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh teste_acao` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
