# FOLHA 2 - PRODUCAO: Guerras Inusitadas EP 08 - A Guerra de 38 Minutos

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/zanzibar1896/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py zanzibar1896` de novo ate esta folha sair sem risco.

## Cena b0 - A guerra mais curta da história durou menos que um almoço.
- Cenario: palace | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Personagens principais (2): SUL (variante 0, expressao stern); GUA (variante 0, expressao stern)
- Animacao: conversar | interacao: avanca e o outro recua
- Objetos/modelos: -
- RISCOS: nenhum

## Cena b1 - Era em Zanzibar, uma ilha da costa da África, controlada pela Inglater...
- Cenario: palace | luz: day | clima: limpo
- Camera: reveal = ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)
- Personagens principais (2): SUL (variante 0, expressao neutral); POV (variante 1, expressao neutral) | multidao: 8 de SUL/POV
- Animacao: -
- Objetos/modelos: -
- RISCOS: nenhum

## Cena b2 - O sultão morreu de repente, e um primo dele correu para o palácio, e s...
- Cenario: interior pedra | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Personagens principais (2): SUL (variante 0, expressao grin); GUA (variante 1, expressao stern)
- Animacao: conversar | interacao: o outro se aproxima | o ultimo personagem ENTRA andando
- Objetos/modelos: kit/throne
- RISCOS: 
  - acao sem animacao propria: sentou -> CORRECAO: mostrar o RESULTADO (objeto em cena, reacao, efeito + som) ou reescrever a frase com acao que a ferramenta faz (andar, chegar, discutir, empurrar, entregar, comemorar, atirar, fugir)

## Cena b3 - Os ingleses não gostaram. "Saia do palácio até as nove da manhã", avis...
- Cenario: palace | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Personagens principais (2): ALM (variante 0, expressao stern, segura paper); ING (variante 0, expressao stern)
- Animacao: conversar | interacao: insiste
- Objetos/modelos: buildings/castle_tower
- RISCOS: nenhum

## Cena b4 - O novo sultão juntou quase três mil homens, alguns canhões velhos, e s...
- Cenario: palace | luz: day | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua)
- Personagens principais (2): GUA (variante 0, expressao stern); GUA (variante 1, expressao stern) | multidao: 18 de GUA/POV
- Animacao: - | batalha encenada
- Objetos/modelos: cannon
- RISCOS: nenhum

## Cena b5 - "Eles não vão atirar", disse ele.
- Cenario: interior pedra | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Personagens principais (1): SUL (variante 0, expressao grin)
- Animacao: conversar
- Objetos/modelos: -
- RISCOS: nenhum

## Cena b6 - Acontece que, às nove e dois, os navios ingleses abriram fogo. O palác...
- Cenario: palace | luz: day | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Personagens principais (2): ING (variante 0, expressao stern); GUA (variante 0, expressao shock) | multidao: 20 de ING/GUA
- Animacao: reagir | batalha encenada
- Objetos/modelos: navios ao fundo
- RISCOS: nenhum

## Cena b7 - O sultão fugiu pela porta dos fundos, e foi pedir abrigo no consulado ...
- Cenario: palace | luz: day | clima: limpo
- Camera: track = travelling lateral acompanhando quem anda
- Personagens principais (2): SUL (variante 0, expressao shock); GUA (variante 1, expressao shock)
- Animacao: discutir
- Objetos/modelos: -
- RISCOS: nenhum

## Cena b8 - Às nove e quarenta, a bandeira do palácio caiu, e os canhões pararam.
- Cenario: palace | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Personagens principais (2): GUA (variante 0, expressao pained, segura flag); ING (variante 1, expressao stern) | multidao: 5 de GUA/ING
- Animacao: conversar | interacao: vai ate o outro
- Objetos/modelos: cannon, war/flagpole
- RISCOS: nenhum

## Cena b9 - Trinta e oito minutos. No mesmo dia, os ingleses colocaram outro sultã...
- Cenario: palace | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Personagens principais (3): ALM (variante 0, expressao smile, segura paper); ING (variante 0, expressao grin); POV (variante 0, expressao nervous)
- Animacao: conversar | interacao: aproxima-se
- Objetos/modelos: -
- RISCOS: nenhum

## Cena b10 - E ainda mandaram a conta das balas para Zanzibar.
- Cenario: palace | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Personagens principais (1): ALM (variante 0, expressao grin)
- Animacao: conversar
- Objetos/modelos: -
- RISCOS: nenhum

## Video inteiro
- Objeto heroi: cannon | grandes momentos: b4, b6 | planos abertos: 3 | mistura: close 24% | medio 56% | aberto 13% | detalhe 7%
- Interacoes: b0 avanca e o outro recua, b2 o outro se aproxima, b3 insiste, b8 vai ate o outro, b9 aproxima-se
- RISCOS GERAIS: nenhum

## RESUMO: 1 risco(s) em aberto
- b2: acao sem animacao propria: sentou

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh zanzibar1896 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh zanzibar1896` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
