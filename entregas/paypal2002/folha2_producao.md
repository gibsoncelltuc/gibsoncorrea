# FOLHA 2 - PRODUCAO: Poder e Fama EP 14 - O Dia em que o PayPal Foi Vendido

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/paypal2002/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py paypal2002` de novo ate esta folha sair sem risco.

## Cena b0 - Em julho de dois mil e dois, nos Estados Unidos, a empresa eBay anunci...
- Cenario: street | luz: golden | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto -> direita baixa | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): EBY (variante 0, expressao grin); MUS (variante 0, expressao surprised)
- Animacao: conversar | interacao: insiste
- Objetos/modelos: kit/coin
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): compra, dois, empresa, estados, paypal
- RISCOS: nenhum

## Cena b1 - O PayPal era um serviço para pagar e receber dinheiro pela internet.
- Cenario: street | luz: golden | clima: limpo
- Camera: reveal = ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (2): MUS (variante 0, expressao smile); EBY (variante 0, expressao neutral) | multidao: 8 de EBY/POV
- Animacao: conversar
- Objetos/modelos: kit/coin
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): paypal, servico
- RISCOS: nenhum

## Cena b2 - O valor do negócio foi de um bilhão e meio de dólares, pagos em ações.
- Cenario: street | luz: golden | clima: limpo
- Camera: close = close no rosto; empurra devagar + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto -> direita baixa | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (1): EBY (variante 0, expressao shock)
- Animacao: reagir
- Objetos/modelos: kit/coin
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): bilhao, dolares, negocio, valor
- RISCOS: nenhum

## Cena b3 - Elon Musk era o maior acionista do PayPal.
- Cenario: street | luz: golden | clima: limpo
- Camera: reveal = ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (2): MUS (variante 0, expressao smug); EBY (variante 0, expressao smile) | multidao: 10 de POV
- Animacao: - | batalha encenada
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): paypal
- RISCOS: nenhum

## Cena b4 - Com o dinheiro da venda, ele pôde investir em novos projetos, como a S...
- Cenario: street | luz: golden | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto -> direita baixa | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): MUS (variante 0, expressao grin); POV (variante 0, expressao surprised)
- Animacao: conversar | interacao: vai ate o outro
- Objetos/modelos: kit/rocket, kit/roadster
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): dinheiro, spacex, tesla, venda
- RISCOS: nenhum

## Cena b5 - A SpaceX foi fundada naquele mesmo ano, em dois mil e dois.
- Cenario: street | luz: golden | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (2): MUS (variante 0, expressao laugh); POV (variante 0, expressao shock) | multidao: 10 de POV
- Animacao: reagir | batalha encenada
- Objetos/modelos: kit/rocket
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): spacex
- RISCOS: nenhum

## Cena b6 - Uma venda de internet que ajudou a pagar foguetes e carros elétricos.
- Cenario: street | luz: golden | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (3): MUS (variante 0, expressao laugh); EBY (variante 0, expressao smile); POV (variante 0, expressao grin)
- Animacao: conversar | interacao: entregar
- Objetos/modelos: kit/coin, kit/rocket
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): internet, pagar, venda
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
kit/coin | b0, b1, b2, b6 | pronto (HEROI: aparece em close) | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/rocket | b4, b5, b6 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/roadster | b4 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: kit/coin | grandes momentos: b3, b5 | planos abertos: 3 | mistura: close 16% | medio 56% | aberto 15% | detalhe 13%
- Interacoes: b0 insiste, b4 vai ate o outro, b6 entregar
- RISCOS GERAIS: nenhum

## RESUMO: 0 risco(s) em aberto - pode renderizar

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh paypal2002 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh paypal2002` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
