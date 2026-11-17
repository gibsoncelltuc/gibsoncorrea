# FOLHA 2 - PRODUCAO: A Febre das Tulipas

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/tulipas1637/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py tulipas1637` de novo ate esta folha sair sem risco.

## Cena b0 - Uma única flor já custou o preço de uma casa inteira.
- Cenario: countryside | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Personagens principais (2): MER (variante 0, expressao grin, segura tulip); POV (variante 1, expressao shock)
- Animacao: reagir | interacao: susto
- Objetos/modelos: kit/tulip_bed, buildings/windmill, kit/tulip_red
- RISCOS: nenhum

## Cena b1 - Era a Holanda, e a tulipa tinha acabado de chegar do Oriente. Colorida...
- Cenario: countryside | luz: day | clima: limpo
- Camera: reveal = ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)
- Personagens principais (2): POV (variante 0, expressao smile, segura tulip); RIC (variante 0, expressao grin) | multidao: 6 de POV
- Animacao: -
- Objetos/modelos: kit/tulip_bed, buildings/windmill, kit/tulip_red
- RISCOS: nenhum

## Cena b2 - Os ricos queriam as mais raras. "Dou mil moedas por esse bulbo", dizia...
- Cenario: interior loja | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Personagens principais (2): RIC (variante 0, expressao stern, segura coin); RIC (variante 1, expressao shock, segura coin)
- Animacao: discutir | interacao: discutir
- Objetos/modelos: kit/tulip_striped
- RISCOS: nenhum

## Cena b3 - Logo, o país inteiro estava comprando. Padeiros, sapateiros, gente que...
- Cenario: countryside | luz: day | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua)
- Personagens principais (3): POV (variante 0, expressao grin, segura tulip); POV (variante 1, expressao laugh, segura coin); MER (variante 0, expressao grin) | multidao: 20 de POV/RIC
- Animacao: - | batalha encenada
- Objetos/modelos: kit/tulip_bed
- RISCOS: nenhum

## Cena b4 - Ninguém queria a flor de verdade. Queriam vender o papel mais caro na ...
- Cenario: countryside | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Personagens principais (2): POV (variante 2, expressao grin, segura paper); POV (variante 3, expressao smile, segura coin)
- Animacao: discutir | interacao: reverencia
- Objetos/modelos: kit/tulip_yellow, kit/tulip_purple
- RISCOS: nenhum

## Cena b5 - Contam que um marinheiro comeu um bulbo no almoço, achando que era ceb...
- Cenario: interior madeira | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Personagens principais (2): MAR (variante 0, expressao smile, segura tulip); MER (variante 0, expressao shock)
- Animacao: discutir | interacao: aproxima-se
- Objetos/modelos: kit/tulip_red
- RISCOS: nenhum

## Cena b6 - Acontece que, num leilão de fevereiro, o vendedor abriu os lances, e n...
- Cenario: interior loja | luz: dia | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Personagens principais (4): MER (variante 0, expressao nervous, segura tulip); POV (variante 0, expressao stern); POV (variante 1, expressao neutral); RIC (variante 0, expressao stern)
- Animacao: reagir | interacao: vai ate o outro
- Objetos/modelos: kit/stall
- RISCOS: nenhum

## Cena b7 - A notícia correu. Em poucos dias, todo mundo quis vender, e não havia ...
- Cenario: countryside | luz: day | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Personagens principais (2): POV (variante 2, expressao shock, segura tulip); RIC (variante 0, expressao pained, segura paper) | multidao: 20 de POV/RIC/MER
- Animacao: discutir | batalha encenada
- Objetos/modelos: kit/tulip_bed
- RISCOS: nenhum

## Cena b8 - Os preços desabaram. Quem tinha trocado a casa por flores ficou só com...
- Cenario: countryside | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Personagens principais (2): RIC (variante 0, expressao pained, segura tulip); MER (variante 0, expressao pained, segura paper)
- Animacao: - | interacao: avanca e o outro recua
- Objetos/modelos: kit/tulip_bed, kit/tulip_red
- RISCOS: nenhum

## Cena b9 - O marinheiro, pelo menos, almoçou bem.
- Cenario: countryside | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Personagens principais (1): MAR (variante 0, expressao grin)
- Animacao: conversar
- Objetos/modelos: -
- RISCOS: nenhum

## Video inteiro
- Objeto heroi: kit/tulip_red | grandes momentos: b3, b7 | planos abertos: 3 | mistura: close 8% | medio 71% | aberto 13% | detalhe 8%
- Interacoes: b0 susto, b2 discutir, b4 reverencia, b5 aproxima-se, b6 vai ate o outro, b8 avanca e o outro recua
- RISCOS GERAIS: nenhum

## RESUMO: 0 risco(s) em aberto - pode renderizar

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh tulipas1637 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh tulipas1637` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
