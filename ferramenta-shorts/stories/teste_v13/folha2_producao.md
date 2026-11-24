# FOLHA 2 - PRODUCAO: Teste EP 13 - Teste v13 2026

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/teste_v13/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py teste_v13` de novo ate esta folha sair sem risco.

## Cena b0 - Em dois mil e vinte e seis, a Tesla mostrou um carro que sai do chão.
- Cenario: loc_pista | luz: noite | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa -> frente | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): MUS (variante 0, expressao grin); ENG (variante 0, expressao surprised)
- Animacao: conversar | interacao: o outro se aproxima
- Objetos/modelos: kit/roadster26
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): carro, chao, tesla
- RISCOS: nenhum

## Cena b1 - O segredo são propulsores de ar comprimido escondidos embaixo do carro...
- Cenario: loc_estudio | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa -> frente
- Personagens principais (0): - | multidao: 0 de 
- Animacao: -
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): carro, segredo
- RISCOS: nenhum

## Cena b2 - Diante dos convidados, o carro decolou e voou por cima da pista.
- Cenario: loc_pista | luz: noite | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa
- Personagens principais (1): MUS (variante 0, expressao laugh) | multidao: 0 de MUS
- Animacao: conversar
- Objetos/modelos: kit/roadster26
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): carro, convidados, pista
- RISCOS: nenhum

## Cena b3 - Segundo a Tesla, ele vai de zero a cem em menos de um segundo.
- Cenario: loc_estudio | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa -> frente
- Personagens principais (0): - | multidao: 0 de 
- Animacao: -
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): tesla, zero
- RISCOS: nenhum

## Cena b4 - Depois o carro acelerou e pulou bem alto diante de todos.
- Cenario: loc_pista | luz: noite | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa
- Personagens principais (1): ENG (variante 0, expressao shock) | multidao: 0 de ENG
- Animacao: reagir
- Objetos/modelos: kit/roadster26
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): carro
- RISCOS: nenhum

## Cena b5 - No fim ele desceu devagar e pousou no asfalto.
- Cenario: loc_patio | luz: noite | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa
- Personagens principais (2): POV (variante 0, expressao surprised); POV (variante 1, expressao grin) | multidao: 0 de POV/POV
- Animacao: conversar | interacao: insiste
- Objetos/modelos: kit/roadster26
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): asfalto
- RISCOS: nenhum

## Cena b6 - O ar sai do tanque, passa pela válvula e vira um jato.
- Cenario: loc_estudio | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa
- Personagens principais (0): - | multidao: 0 de 
- Animacao: -
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): jato, tanque
- RISCOS: nenhum

## Cena b7 - Carro comum demora três segundos, este demora um.
- Cenario: loc_estudio | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa
- Personagens principais (0): - | multidao: 0 de 
- Animacao: -
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): -
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
kit/roadster26 | b0, b2, b4, b5 | pronto (HEROI: aparece em close) | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: kit/roadster26 | grandes momentos: - | planos abertos: 0 | mistura: close 0% | medio 96% | aberto 0% | detalhe 4%
- Interacoes: b0 o outro se aproxima, b5 insiste
- RISCOS GERAIS: 
  - 1 palavra(s) de acao sem efeito + som -> CORRECAO: ver plano.md e por "fx"/"sfx" na cena

## RESUMO: 1 risco(s) em aberto
- geral: 1 palavra(s) de acao sem efeito + som

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh teste_v13 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh teste_v13` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
