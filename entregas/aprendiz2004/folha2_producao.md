# FOLHA 2 - PRODUCAO: Poder e Fama EP 13 - Você Está Demitido

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/aprendiz2004/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py aprendiz2004` de novo ate esta folha sair sem risco.

## Cena b0 - Em janeiro de dois mil e quatro, estreou na televisão americana um pro...
- Cenario: street | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto -> direita baixa | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): TRU (variante 0, expressao grin); CND (variante 0, expressao smile)
- Animacao: conversar | interacao: vai ate o outro
- Objetos/modelos: kit/tv
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): aprendiz, dois, programa, televisao
- RISCOS: nenhum

## Cena b1 - O apresentador era Donald Trump, e os participantes disputavam um empr...
- Cenario: street | luz: day | clima: limpo
- Camera: reveal = ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (2): TRU (variante 0, expressao smug); CND (variante 0, expressao surprised) | multidao: 8 de POV
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): apresentador, emprego, empresas, participantes
- RISCOS: nenhum

## Cena b2 - A cada episódio, eles faziam tarefas de negócios, como vender coisas n...
- Cenario: street | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto -> direita baixa | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): CND (variante 0, expressao smile); POV (variante 0, expressao surprised)
- Animacao: conversar | interacao: cochichar
- Objetos/modelos: kit/chest
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cada, emprego, negocios
- RISCOS: nenhum

## Cena b3 - No fim, alguém era eliminado, e a frase que fechava o programa era: Vo...
- Cenario: street | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto -> direita baixa
- Personagens principais (1): TRU (variante 0, expressao shout) | multidao: 10 de POV
- Animacao: conversar | batalha encenada
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): frase, programa
- RISCOS: nenhum

## Cena b4 - A frase ficou tão famosa que virou piada e foi repetida pelo mundo int...
- Cenario: street | luz: day | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (2): CND (variante 0, expressao laugh); POV (variante 0, expressao grin) | multidao: 8 de POV
- Animacao: - | batalha encenada
- Objetos/modelos: kit/globe
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): frase
- RISCOS: nenhum

## Cena b5 - Um programa de negócios que ficou conhecido por duas palavras: você es...
- Cenario: street | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (3): TRU (variante 0, expressao laugh); CND (variante 0, expressao smile); POV (variante 0, expressao grin)
- Animacao: conversar | interacao: aproxima-se
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): negocios, programa
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
kit/tv | b0 | pronto (HEROI: aparece em close) | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/chest | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/globe | b4 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: kit/tv | grandes momentos: b3, b4 | planos abertos: 2 | mistura: close 20% | medio 55% | aberto 16% | detalhe 9%
- Interacoes: b0 vai ate o outro, b2 cochichar, b5 aproxima-se
- RISCOS GERAIS: nenhum

## RESUMO: 0 risco(s) em aberto - pode renderizar

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh aprendiz2004 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh aprendiz2004` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
