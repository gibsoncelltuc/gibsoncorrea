# FOLHA 2 - PRODUCAO: Guerras Inusitadas EP 07 - A Guerra dos Bolos

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/bolos1838/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py bolos1838` de novo ate esta folha sair sem risco.

## Cena b0 - A França invadiu o México por causa de uma conta de confeitaria.
- Cenario: street | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Personagens principais (2): CON (variante 0, expressao shock); OFI (variante 0, expressao laugh) | multidao: 5 de CON/OFI
- Animacao: reagir | interacao: entregar
- Objetos/modelos: kit/cake_table
- RISCOS: nenhum

## Cena b1 - Um confeiteiro francês tinha uma loja perto da Cidade do México, famos...
- Cenario: street | luz: day | clima: limpo
- Camera: reveal = ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)
- Personagens principais (2): CON (variante 0, expressao smile); OFI (variante 1, expressao neutral) | multidao: 8 de CON/OFI
- Animacao: -
- Objetos/modelos: kit/cake_table
- RISCOS: nenhum

## Cena b2 - Um dia, oficiais mexicanos entraram, comeram tudo o que havia, quebrar...
- Cenario: interior loja | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Personagens principais (3): OFI (variante 0, expressao laugh); OFI (variante 1, expressao grin); CON (variante 0, expressao shock)
- Animacao: conversar | interacao: vai ate o outro | o ultimo personagem ENTRA andando
- Objetos/modelos: -
- RISCOS: nenhum

## Cena b3 - O confeiteiro escreveu ao rei da França. "Quero sessenta mil pesos", p...
- Cenario: interior pedra | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Personagens principais (2): CON (variante 0, expressao stern, segura paper); REI (variante 0, expressao neutral)
- Animacao: conversar | interacao: aproxima-se
- Objetos/modelos: kit/cake_table
- RISCOS: nenhum

## Cena b4 - O rei gostou da ideia, juntou outras queixas, e cobrou seiscentos mil....
- Cenario: interior pedra | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Personagens principais (1): REI (variante 0, expressao stern)
- Animacao: conversar
- Objetos/modelos: -
- RISCOS: nenhum

## Cena b5 - O México riu da cobrança, e não pagou um centavo.
- Cenario: street | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Personagens principais (2): GEN (variante 0, expressao laugh); OFI (variante 0, expressao grin)
- Animacao: comemorar | interacao: cochichar
- Objetos/modelos: -
- RISCOS: nenhum

## Cena b6 - Acontece que a França mandou mesmo. Navios de guerra fecharam todos os...
- Cenario: harbor | luz: day | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua)
- Personagens principais (2): FRA (variante 0, expressao stern); FRA (variante 1, expressao stern) | multidao: 18 de FRA
- Animacao: - | batalha encenada
- Objetos/modelos: navios ao fundo
- RISCOS: nenhum

## Cena b7 - Os canhões franceses bombardearam a fortaleza de Veracruz, e os soldad...
- Cenario: street | luz: day | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Personagens principais (2): FRA (variante 0, expressao stern); OFI (variante 0, expressao shock) | multidao: 20 de FRA/OFI
- Animacao: reagir | batalha encenada
- Objetos/modelos: cannon
- RISCOS: nenhum

## Cena b8 - Um general mexicano correu para o combate, e perdeu uma perna para um ...
- Cenario: street | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Personagens principais (2): GEN (variante 0, expressao pained); OFI (variante 1, expressao shock)
- Animacao: conversar | interacao: susto | o ultimo personagem ENTRA andando
- Objetos/modelos: cannon
- RISCOS: nenhum

## Cena b9 - Meses depois, o México pagou os seiscentos mil pesos, e a França foi e...
- Cenario: street | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Personagens principais (2): GEN (variante 0, expressao pained, segura paper); FRA (variante 0, expressao grin, segura coin)
- Animacao: - | interacao: insiste
- Objetos/modelos: -
- RISCOS: nenhum

## Cena b10 - Nunca um doce custou tão caro.
- Cenario: street | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Personagens principais (1): CON (variante 0, expressao grin, segura coin)
- Animacao: -
- Objetos/modelos: kit/cake_table
- RISCOS: nenhum

## Video inteiro
- Objeto heroi: kit/cake_table | grandes momentos: b6, b7 | planos abertos: 3 | mistura: close 20% | medio 61% | aberto 12% | detalhe 7%
- Interacoes: b0 entregar, b2 vai ate o outro, b3 aproxima-se, b5 cochichar, b8 susto, b9 insiste
- RISCOS GERAIS: nenhum

## RESUMO: 0 risco(s) em aberto - pode renderizar

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh bolos1838 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh bolos1838` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
