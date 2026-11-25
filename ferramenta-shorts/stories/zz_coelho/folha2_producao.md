# FOLHA 2 - PRODUCAO: Teste EP 99 - Teste Coelhinho

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/zz_coelho/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py zz_coelho` de novo ate esta folha sair sem risco.

## Cena b0 - Escova, escova, vai, vai, vai!
- Cenario: interior hospital | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 1 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo
- Personagens principais (1): COE (variante 0, expressao grin, segura toothbrush)
- Animacao: encena
- Objetos/modelos: kit/sink, mk/Stool
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): -
- RISCOS: nenhum

## Cena b1 - Um pinguinho de pasta, só isso!
- Cenario: interior hospital | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 1 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo
- Personagens principais (1): COE (variante 0, expressao smile, segura toothbrush)
- Animacao: encena
- Objetos/modelos: kit/sink
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): pasta, pinguinho
- RISCOS: nenhum

## Cena b2 - Pra cima e pra baixo, bem devagar.
- Cenario: interior hospital | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 1 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo
- Personagens principais (1): COE (variante 0, expressao laugh, segura toothbrush)
- Animacao: encena
- Objetos/modelos: kit/sink
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): -
- RISCOS: nenhum

## Cena b3 - Tchau, bichinhos! Meus dentes vão brilhar!
- Cenario: interior hospital | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 1 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo
- Personagens principais (1): COE (variante 0, expressao grin)
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): -
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
kit/sink | b0, b1, b2 | pronto (HEROI: aparece em close) | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
mk/Stool | b0 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: kit/sink | grandes momentos: - | planos abertos: 0 | mistura: close 50% | medio 50% | aberto 0% | detalhe 0%
- Interacoes: -
- RISCOS GERAIS: 
  - nenhum mapa no video (o canal situa o lugar com mapa rapido) -> CORRECAO: "mapa": "NOME DO LUGAR" na cena 1 ou 2
  - menos de 2 grandes momentos -> CORRECAO: "impact": true em duas cenas de acao ("batalha": true SO' se a frase for de luta de verdade)
  - objeto heroi (kit/sink) sem close de camera -> CORRECAO: por o objeto em "props" de uma cena media de 8+ palavras

## RESUMO: 3 risco(s) em aberto
- geral: nenhum mapa no video (o canal situa o lugar com mapa rapido)
- geral: menos de 2 grandes momentos
- geral: objeto heroi (kit/sink) sem close de camera

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh zz_coelho bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh zz_coelho` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
