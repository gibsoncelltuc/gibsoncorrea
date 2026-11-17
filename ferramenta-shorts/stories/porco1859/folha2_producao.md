# FOLHA 2 - PRODUCAO: Guerras Inusitadas EP 06 - A Guerra do Porco

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/porco1859/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py porco1859` de novo ate esta folha sair sem risco.

## Cena b0 - Dois países quase entraram em guerra por causa de um porco.
- Cenario: countryside | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Personagens principais (2): FAZ (variante 0, expressao shock); IRL (variante 0, expressao stern)
- Animacao: reagir | interacao: o outro se aproxima | o ultimo personagem ENTRA andando
- Objetos/modelos: pig
- RISCOS: nenhum

## Cena b1 - Era uma ilha pequena, entre os Estados Unidos e o Canadá. Americanos e...
- Cenario: countryside | luz: day | clima: limpo
- Camera: reveal = ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)
- Personagens principais (2): FAZ (variante 0, expressao neutral); IRL (variante 0, expressao neutral) | multidao: 8 de FAZ/IRL
- Animacao: -
- Objetos/modelos: -
- RISCOS: nenhum

## Cena b2 - Um dia, um fazendeiro americano encontrou um porco comendo as batatas ...
- Cenario: countryside | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Personagens principais (1): FAZ (variante 0, expressao stern)
- Animacao: conversar
- Objetos/modelos: crate, nature/flowerbed, pig
- RISCOS: nenhum

## Cena b3 - Ele pegou a espingarda, e atirou. O porco era de um vizinho inglês.
- Cenario: countryside | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Personagens principais (1): FAZ (variante 0, expressao stern)
- Animacao: conversar
- Objetos/modelos: pig
- RISCOS: nenhum

## Cena b4 - "Eu pago dez dólares", disse o americano. "Ele vale cem", respondeu o ...
- Cenario: countryside | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Personagens principais (2): FAZ (variante 0, expressao nervous, segura coin); IRL (variante 0, expressao stern)
- Animacao: discutir | interacao: discutir
- Objetos/modelos: -
- RISCOS: nenhum

## Cena b5 - Os ingleses ameaçaram prender o fazendeiro. Então os Estados Unidos ma...
- Cenario: harbor | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Personagens principais (2): AME (variante 0, expressao stern); AME (variante 1, expressao stern) | multidao: 16 de AME
- Animacao: discutir | interacao: empurrar
- Objetos/modelos: -
- RISCOS: nenhum

## Cena b6 - Acontece que a Inglaterra respondeu com navios de guerra. Em poucas se...
- Cenario: harbor | luz: day | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua)
- Personagens principais (2): ING (variante 0, expressao stern); AME (variante 0, expressao stern) | multidao: 20 de ING/AME
- Animacao: discutir | batalha encenada
- Objetos/modelos: cannon, navios ao fundo
- RISCOS: nenhum

## Cena b7 - O almirante inglês recebeu a ordem de atacar. "Não vou começar uma gue...
- Cenario: interior madeira | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Personagens principais (2): ALM (variante 0, expressao stern); ING (variante 1, expressao nervous)
- Animacao: discutir | interacao: vai ate o outro
- Objetos/modelos: -
- RISCOS: nenhum

## Cena b8 - Os soldados passaram meses trocando insultos, e depois, visitas e fest...
- Cenario: countryside | luz: day | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Personagens principais (3): ING (variante 0, expressao grin); AME (variante 0, expressao laugh); ING (variante 1, expressao smile) | multidao: 18 de ING/AME
- Animacao: discutir | batalha encenada
- Objetos/modelos: -
- RISCOS: nenhum

## Cena b9 - Treze anos depois, um árbitro decidiu que a ilha era americana.
- Cenario: countryside | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Personagens principais (2): ALM (variante 0, expressao smile, segura paper); AME (variante 1, expressao smile)
- Animacao: conversar | interacao: insiste
- Objetos/modelos: -
- RISCOS: nenhum

## Cena b10 - A única baixa da guerra foi o porco.
- Cenario: countryside | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Personagens principais (1): FAZ (variante 0, expressao pained)
- Animacao: conversar
- Objetos/modelos: -
- RISCOS: nenhum

## Video inteiro
- Objeto heroi: - | grandes momentos: b6, b8 | planos abertos: 3 | mistura: close 26% | medio 56% | aberto 16% | detalhe 2%
- Interacoes: b0 o outro se aproxima, b4 discutir, b5 empurrar, b7 vai ate o outro, b9 insiste
- RISCOS GERAIS: nenhum

## RESUMO: 0 risco(s) em aberto - pode renderizar

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh porco1859 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh porco1859` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
