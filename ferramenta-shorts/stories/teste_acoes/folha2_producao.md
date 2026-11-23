# FOLHA 2 - PRODUCAO: Teste de Acoes

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/teste_acoes/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py teste_acoes` de novo ate esta folha sair sem risco.

## Cena b0 - Em mil oitocentos e quarenta, no interior da Franca, um soldado correu...
- Cenario: countryside | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto -> direita baixa -> frente
- Personagens principais (2): SOL (variante 0, expressao determined); FAZ (variante 0, expressao shock)
- Animacao: conversar | interacao: susto
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): alto, cavalo, franca, interior, soldado
- RISCOS: nenhum

## Cena b1 - Dias depois, o rei e o fazendeiro fizeram um acordo, apertaram as maos...
- Cenario: countryside | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto -> direita baixa
- Personagens principais (2): REI (variante 0, expressao stern); FAZ (variante 0, expressao smile)
- Animacao: comemorar | interacao: apertar
- Objetos/modelos: buildings/barn, nature/picket_fence, nature/haybale, nature/scarecrow
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): acordo, fazendeiro, maos
- RISCOS: nenhum

## Cena b2 - O fazendeiro entrou no carro, acelerou pela estrada e o carro decolou ...
- Cenario: countryside | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto -> direita baixa
- Personagens principais (2): FAZ (variante 0, expressao smile); SOL (variante 0, expressao stern)
- Animacao: conversar | o ultimo personagem ENTRA andando
- Objetos/modelos: buildings/barn, nature/picket_fence, nature/haybale, nature/scarecrow, vehicles/car
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): carro, cerca, fazendeiro
- RISCOS: nenhum

## Cena b3 - No mercado, os homens discutiram, um empurrou o outro e todo mundo cai...
- Cenario: street | luz: day | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (3): SOL (variante 0, expressao stern); FAZ (variante 1, expressao smile); REI (variante 0, expressao smile) | multidao: 30 de SOL/FAZ/REI
- Animacao: conversar | batalha encenada
- Objetos/modelos: kit/stall, buildings/shop
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): chao, empurrou, homens, mercado
- RISCOS: nenhum

## Cena b4 - No fim, o rei comemorou, pulou de alegria e chorou de rir.
- Cenario: countryside | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (1): REI (variante 0, expressao grin)
- Animacao: comemorar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): alegria
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
buildings/barn | b1, b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/picket_fence | b1, b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/haybale | b1, b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/scarecrow | b1, b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
vehicles/car | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/stall | b3 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
buildings/shop | b3 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: - | grandes momentos: b3 | planos abertos: 1 | mistura: close 18% | medio 76% | aberto 6% | detalhe 0%
- Interacoes: b0 susto, b1 apertar
- RISCOS GERAIS: nenhum

## RESUMO: 0 risco(s) em aberto - pode renderizar

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh teste_acoes bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh teste_acoes` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
