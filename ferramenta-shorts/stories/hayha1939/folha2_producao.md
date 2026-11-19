# FOLHA 2 - PRODUCAO: A Morte Branca

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/hayha1939/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py hayha1939` de novo ate esta folha sair sem risco.

## Cena b0 - Inverno de mil novecentos e trinta e nove. A União Soviética invadiu a...
- Cenario: arctic | luz: arctic | clima: limpo
- Camera: track = travelling lateral acompanhando quem anda
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: direita baixa -> frente -> 3/4 pela direita, mais perto e mais baixo
- Personagens principais (4): SOV (variante 0, expressao stern); SOV (variante 1, expressao stern); SOV (variante 2, expressao neutral); SOV (variante 3, expressao stern)
- Animacao: -
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): exercito, finlandia, uniao
- RISCOS: 
  - a narracao fala de BATALHA/ATAQUE e a cena nao encena a luta -> CORRECAO: "batalha": true nesta cena (tropa dos dois lados no "crowd", tiros/golpes e gente fugindo); cada batalha citada no roteiro = uma cena com "batalha": true

## Cena b1 - Os soldados finlandeses eram poucos, mas conheciam a floresta, a neve ...
- Cenario: arctic | luz: arctic | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (3): FIN (variante 0, expressao stern); FIN (variante 1, expressao nervous); FIN (variante 2, expressao stern) | multidao: 10 de FIN
- Animacao: reagir
- Objetos/modelos: nature/tree_pine, nature/tree_oak, nature/bush
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): floresta, frio, neve, quarenta, soldados, zero
- RISCOS: nenhum

## Cena b2 - Um deles era um fazendeiro baixinho chamado Simo Häyhä.
- Cenario: arctic | luz: arctic | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: direita baixa -> frente
- Personagens principais (1): FIN (variante 3, expressao smile)
- Animacao: conversar
- Objetos/modelos: buildings/barn, nature/picket_fence, nature/haybale, nature/scarecrow
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): fazendeiro
- RISCOS: 
  - a narracao cita "fazendeiro" e ninguem em cena esta vestido a carater -> CORRECAO: por no "who" um personagem com "profissao": "agricultor" no figurino (coroa/farda/chapeu proprios)

## Cena b3 - Vestido de branco, ele esperava imóvel no meio da neve, horas a fio.
- Cenario: arctic | luz: arctic | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua) [momento criado pela ferramenta]
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (1): FIN (variante 3, expressao stern) | multidao: 12 de FIN
- Animacao: - | batalha encenada
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): branco, neve
- RISCOS: nenhum

## Cena b4 - Dizem que ele mantinha neve na boca, para o vapor da respiração não en...
- Cenario: arctic | luz: arctic | clima: limpo
- Camera: close = close no rosto; empurra devagar + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: direita baixa -> frente -> 3/4 pela direita, mais perto e mais baixo | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (1): FIN (variante 3, expressao neutral)
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): boca, respiracao, vapor
- RISCOS: nenhum

## Cena b5 - Em cerca de cem dias, ele teve mais de quinhentos inimigos confirmados...
- Cenario: arctic | luz: arctic | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: direita baixa -> frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): FIN (variante 3, expressao stern); FIN (variante 0, expressao shock)
- Animacao: conversar | interacao: susto
- Objetos/modelos: nature/picket_fence
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): carabina, ferro, mira, quinhentos
- RISCOS: nenhum

## Cena b6 - Os soviéticos passaram a chamá-lo de Morte Branca.
- Cenario: arctic | luz: arctic | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: direita baixa -> frente
- Personagens principais (1): SOV (variante 1, expressao shock) | multidao: 6 de SOV
- Animacao: reagir
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): chamalo, morte, sovieticos
- RISCOS: nenhum

## Cena b7 - Em março de mil novecentos e quarenta, uma bala atingiu o rosto dele. ...
- Cenario: arctic | luz: arctic | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 5 take(s) de ~1,8 s, deslizando de um para o outro: direita baixa -> frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (2): FIN (variante 3, expressao pained); FIN (variante 1, expressao nervous) | multidao: 10 de FIN
- Animacao: conversar | interacao: cochichar | batalha encenada
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): bala, rosto
- RISCOS: nenhum

## Cena b8 - Viveu até os noventa e seis anos, e nunca se achou herói. Dizia que só...
- Cenario: arctic | luz: golden | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: direita baixa -> frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto
- Personagens principais (1): FIN (variante 3, expressao smile)
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): noventa
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
nature/tree_pine | b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/tree_oak | b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/bush | b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
buildings/barn | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/picket_fence | b2, b5 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/haybale | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/scarecrow | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: - | grandes momentos: b3, b7 | planos abertos: 2 | mistura: close 29% | medio 47% | aberto 17% | detalhe 6%
- Interacoes: b5 susto, b7 cochichar
- RISCOS GERAIS: 
  - nenhum mapa no video (o canal situa o lugar com mapa rapido) -> CORRECAO: "mapa": "NOME DO LUGAR" na cena 1 ou 2
  - pouca variedade de cenario ({'arctic': 9}): o video fica parecendo todos os outros -> CORRECAO: pelo menos 3 lugares e nenhum em mais da metade das cenas: troque "set"/"interior" de algumas cenas (lugares: outback, countryside, arctic, palace, harbor, mountain, medieval, jungle, hall, stadium, street | interior: madeira, pedra, loja)
  - video sem objeto heroi -> CORRECAO: "heroi": "kit/<objeto>" no topo do roteiro (modele se nao existir)
  - 1 palavra(s) de acao sem efeito + som -> CORRECAO: ver plano.md e por "fx"/"sfx" na cena

## RESUMO: 6 risco(s) em aberto
- b0: a narracao fala de BATALHA/ATAQUE e a cena nao encena a luta
- b2: a narracao cita "fazendeiro" e ninguem em cena esta vestido a carater
- geral: nenhum mapa no video (o canal situa o lugar com mapa rapido)
- geral: pouca variedade de cenario ({'arctic': 9}): o video fica parecendo todos os outros
- geral: video sem objeto heroi
- geral: 1 palavra(s) de acao sem efeito + som

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh hayha1939 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh hayha1939` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
