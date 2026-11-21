# FOLHA 2 - PRODUCAO: E Se EP 10 - E Se o Titanic Não Tivesse Afundado?

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/ese_titanic/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py ese_titanic` de novo ate esta folha sair sem risco.

## Cena b0 - Diziam que ele era praticamente impossível de afundar. Afundou na prim...
- Cenario: harbor | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): CAP (variante 0, expressao stern); POV (variante 0, expressao surprised)
- Animacao: conversar | interacao: aproxima-se
- Objetos/modelos: kit/iceberg, kit/marco_liberdade
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): afundar, iceberg, primeira
- RISCOS: nenhum

## Cena b1 - Abril de mil novecentos e doze. O Titanic levava mais de duas mil pess...
- Cenario: harbor | luz: day | clima: limpo
- Camera: reveal = ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (2): POV (variante 0, expressao smile); POV (variante 1, expressao grin) | multidao: 30 de POV
- Animacao: -
- Objetos/modelos: ship, kit/marco_liberdade
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): duas, titanic
- RISCOS: nenhum

## Cena b2 - Perto da meia-noite, o vigia gritou: iceberg à frente! Não deu tempo d...
- Cenario: arctic | luz: noite | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto
- Personagens principais (2): MAR (variante 0, expressao scared); CAP (variante 0, expressao shock)
- Animacao: discutir | interacao: discutir
- Objetos/modelos: kit/iceberg
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): desviar, frente, meianoite, vigia
- RISCOS: nenhum

## Cena b3 - O gelo rasgou o casco por baixo da água, onde fica a maior parte do ic...
- Cenario: arctic | luz: noite | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto
- Personagens principais (1): MAR (variante 0, expressao shock)
- Animacao: reagir
- Objetos/modelos: kit/iceberg
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): agua, casco, gelo, iceberg
- RISCOS: nenhum

## Cena b4 - Acontece que só havia botes para metade das pessoas. Cerca de mil e qu...
- Cenario: arctic | luz: noite | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (3): POV (variante 0, expressao scared); POV (variante 1, expressao shout); MAR (variante 0, expressao scared) | multidao: 22 de POV
- Animacao: encena | batalha encenada
- Objetos/modelos: boat, nature/picket_fence
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): pessoas
- RISCOS: nenhum

## Cena b5 - E se o Titanic tivesse chegado inteiro?
- Cenario: street | luz: noite | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 1 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto
- Personagens principais (2): PRO (variante 0, expressao suspicious, segura paper); POV (variante 0, expressao worried)
- Animacao: conversar | interacao: avanca e o outro recua | o ultimo personagem ENTRA andando
- Objetos/modelos: kit/marco_liberdade
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): titanic
- RISCOS: nenhum

## Cena b6 - Seria só mais um navio de luxo, esquecido. E as regras do mar continua...
- Cenario: countryside | luz: noite | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto
- Personagens principais (2): PRO (variante 0, expressao stern); POV (variante 1, expressao surprised)
- Animacao: conversar | interacao: cochichar
- Objetos/modelos: ship, kit/marco_liberdade
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): luxo, navio, regras
- RISCOS: 
  - a narracao cita agua e o cenario "countryside" nao tem agua -> CORRECAO: "set": "harbor" (cais com mar e navio) ou "set": "palace" (praia), ou "mapa" para so situar

## Cena b7 - Por causa do naufrágio, os países fizeram em mil novecentos e catorze ...
- Cenario: harbor | luz: noite | clima: limpo
- Camera: close = close no rosto; empurra devagar + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto -> direita baixa | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (1): PRO (variante 0, expressao shock)
- Animacao: reagir
- Objetos/modelos: kit/scroll, kit/marco_liberdade
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): naufragio, seguranca
- RISCOS: nenhum

## Cena b8 - E criaram uma patrulha só para vigiar icebergs. Ela existe até hoje.
- Cenario: harbor | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (2): MAR (variante 0, expressao grin); CAP (variante 0, expressao smile)
- Animacao: conversar | interacao: entregar
- Objetos/modelos: kit/iceberg
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): patrulha
- RISCOS: nenhum

## Cena b9 - Ou seja: a tragédia do Titanic ajudou a salvar milhares de vidas depoi...
- Cenario: street | luz: day | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (3): POV (variante 0, expressao smile); POV (variante 1, expressao grin); MAR (variante 0, expressao grin) | multidao: 30 de POV
- Animacao: comemorar | batalha encenada
- Objetos/modelos: ship, kit/marco_liberdade
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): salvar, titanic, tragedia, vidas
- RISCOS: nenhum

## Cena b10 - Às vezes, o pior dia da história é o que deixa o futuro mais seguro.
- Cenario: harbor | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto
- Personagens principais (1): PRO (variante 0, expressao smile)
- Animacao: conversar
- Objetos/modelos: kit/iceberg, kit/marco_liberdade
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): futuro, pior
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
kit/iceberg | b0, b2, b3, b8, b10 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/marco_liberdade | b0, b1, b5, b6, b7, b9, b10 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
ship | b1, b6, b9 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
boat | b4 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/picket_fence | b4 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/scroll | b7 | pronto (HEROI: aparece em close) | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: kit/scroll | grandes momentos: b4, b9 | planos abertos: 3 | mistura: close 33% | medio 49% | aberto 12% | detalhe 6%
- Interacoes: b0 aproxima-se, b2 discutir, b5 avanca e o outro recua, b6 cochichar, b8 entregar
- RISCOS GERAIS: nenhum

## RESUMO: 1 risco(s) em aberto
- b6: a narracao cita agua e o cenario "countryside" nao tem agua

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh ese_titanic bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh ese_titanic` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
