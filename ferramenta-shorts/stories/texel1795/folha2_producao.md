# FOLHA 2 - PRODUCAO: A Cavalaria que Capturou uma Frota

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/texel1795/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py texel1795` de novo ate esta folha sair sem risco.

## Cena b0 - Em mil setecentos e noventa e cinco, a França invadia a Holanda, e faz...
- Cenario: arctic | luz: arctic | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa -> frente
- Personagens principais (0): -
- Animacao: -
- Objetos/modelos: ship
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): franca, frio, holanda
- RISCOS: 
  - personagens parados (so falam e piscam) -> CORRECAO: "acao": "conversar|discutir|comemorar", "interacao": "empurrar|cochichar|entregar|susto", objeto na mao (4o campo do "who") ou "chega": true

## Cena b1 - A frota holandesa estava ancorada perto de Den Helder, e o mar congelo...
- Cenario: arctic | luz: arctic | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (2): NED (variante 0, expressao nervous); NED (variante 1, expressao shock) | multidao: 10 de NED
- Animacao: reagir
- Objetos/modelos: ship
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): frota
- RISCOS: 
  - a narracao cita agua e o cenario "arctic" nao tem agua -> CORRECAO: "set": "harbor" (cais com mar e navio) ou "set": "palace" (praia), ou "mapa" para so situar

## Cena b2 - Os navios ficaram presos no gelo, como carros num congestionamento.
- Cenario: arctic | luz: arctic | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): NED (variante 2, expressao pained) | multidao: 6 de NED
- Animacao: encena
- Objetos/modelos: ship
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): gelo, navios
- RISCOS: 
  - veiculo citado e nao aparece -> CORRECAO: "veiculo": {"asset": "vehicles/truck"} (ou wagon, locomotive, car, tank, airplane) ou "caminhoes": true na batalha

## Cena b3 - Do outro lado, os franceses tinham cavalaria, os hussardos, e nenhum n...
- Cenario: arctic | luz: arctic | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa
- Personagens principais (3): FRA (variante 0, expressao stern); FRA (variante 1, expressao neutral); OFF (variante 0, expressao stern)
- Animacao: conversar | interacao: aproxima-se
- Objetos/modelos: horse
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): franceses, hussardos
- RISCOS: nenhum

## Cena b4 - O comandante teve uma ideia maluca: atacar a frota a cavalo.
- Cenario: arctic | luz: arctic | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (1): OFF (variante 1, expressao grin) | multidao: 5 de OFF
- Animacao: conversar
- Objetos/modelos: horse
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cavalo, comandante, frota
- RISCOS: 
  - a narracao cita "comandante" e ninguem em cena esta vestido a carater -> CORRECAO: por no "who" um personagem com "profissao": "general" no figurino (coroa/farda/chapeu proprios)

## Cena b5 - Na noite de vinte e três de janeiro, os hussardos atravessaram o gelo,...
- Cenario: arctic | luz: tense | clima: limpo
- Camera: track = travelling lateral acompanhando quem anda
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa -> frente -> 3/4 pela direita, mais perto e mais baixo
- Personagens principais (2): FRA (variante 0, expressao stern); FRA (variante 2, expressao neutral)
- Animacao: -
- Objetos/modelos: horse
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cascos, cavalos, gelo, hussardos, janeiro, panos, vinte
- RISCOS: nenhum

## Cena b6 - Os marinheiros holandeses viram a cavalaria chegar, e a frota se rende...
- Cenario: arctic | luz: arctic | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua) [momento criado pela ferramenta]
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (2): NED (variante 0, expressao shock); FRA (variante 1, expressao grin) | multidao: 5 de NED/FRA
- Animacao: reagir | batalha encenada
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cavalaria, frota, marinheiros
- RISCOS: nenhum

## Cena b7 - Foram mais de uma dezena de navios capturados por soldados a cavalo.
- Cenario: arctic | luz: arctic | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa
- Personagens principais (2): FRA (variante 0, expressao laugh); FRA (variante 2, expressao grin) | multidao: 5 de FRA
- Animacao: conversar | interacao: avanca e o outro recua
- Objetos/modelos: ship, horse
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cavalo, dezena, navios
- RISCOS: nenhum

## Cena b8 - Dizem que foi a única vez na história em que uma cavalaria capturou um...
- Cenario: arctic | luz: arctic | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa -> frente
- Personagens principais (1): OFF (variante 0, expressao laugh) | multidao: 10 de OFF
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cavalaria, frota
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
ship | b0, b1, b2, b7 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
horse | b3, b4, b5, b7 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: - | grandes momentos: b6 | planos abertos: 3 | mistura: close 14% | medio 61% | aberto 24% | detalhe 2%
- Interacoes: b3 aproxima-se, b7 avanca e o outro recua
- RISCOS GERAIS: 
  - menos de 2 grandes momentos -> CORRECAO: "batalha": true (ou "impact": true) em duas cenas de acao
  - pouca variedade de cenario ({'arctic': 9}): o video fica parecendo todos os outros -> CORRECAO: pelo menos 3 lugares e nenhum em mais da metade das cenas: troque "set"/"interior" de algumas cenas (lugares: outback, countryside, arctic, palace, harbor, mountain, medieval, jungle, hall, stadium, street | interior: madeira, pedra, loja)
  - video sem objeto heroi -> CORRECAO: "heroi": "kit/<objeto>" no topo do roteiro (modele se nao existir)
  - 1 palavra(s) de acao sem efeito + som -> CORRECAO: ver plano.md e por "fx"/"sfx" na cena

## RESUMO: 8 risco(s) em aberto
- b0: personagens parados (so falam e piscam)
- b1: a narracao cita agua e o cenario "arctic" nao tem agua
- b2: veiculo citado e nao aparece
- b4: a narracao cita "comandante" e ninguem em cena esta vestido a carater
- geral: menos de 2 grandes momentos
- geral: pouca variedade de cenario ({'arctic': 9}): o video fica parecendo todos os outros
- geral: video sem objeto heroi
- geral: 1 palavra(s) de acao sem efeito + som

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh texel1795 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh texel1795` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
