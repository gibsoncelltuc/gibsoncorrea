# FOLHA 2 - PRODUCAO: Curiosidade e Ciência EP 14 - O Químico que Sonhou com uma Cobra

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/kekule1865/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py kekule1865` de novo ate esta folha sair sem risco.

## Cena b0 - Um dos maiores segredos da química foi resolvido num cochilo, e com a ...
- Cenario: street | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): KEK (variante 0, expressao grin); COL (variante 0, expressao surprised)
- Animacao: conversar | interacao: cochichar
- Objetos/modelos: kit/snake_ring, kit/marco_viena, kit/cobra
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): ajuda, cobra, maiores, quimica
- RISCOS: nenhum

## Cena b1 - Era mil oitocentos e sessenta e cinco, na cidade de Gante, na Bélgica.
- Cenario: street | luz: day | clima: limpo
- Camera: reveal = ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (2): POV (variante 0, expressao smile); POV (variante 1, expressao grin) | multidao: 18 de POV
- Animacao: - | batalha encenada
- Objetos/modelos: kit/marco_viena, buildings/house_two, nature/lamppost
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): belgica, cidade, gante
- RISCOS: nenhum

## Cena b2 - O professor August Kekulé tinha um problema: o benzeno, um líquido com...
- Cenario: interior madeira | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto
- Personagens principais (2): KEK (variante 0, expressao worried); ALU (variante 0, expressao suspicious, segura paper)
- Animacao: discutir | interacao: discutir
- Objetos/modelos: kit/snake_ring
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): benzeno, carbono, liquido, problema, professor, seis
- RISCOS: 
  - frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada -> CORRECAO: "explica": {"objeto": "kit/<objeto>", "vfx": [{"k": "jato", "na": "<palavra>"}], "rotulos": [["NOME", "baixo", "<palavra>"]], "setas": [["cima", "FORCA"]], "medidor"/"passos"/"comparar": ...} (GUIA_DO_ROTEIRISTA.md "Cena de explicacao"); para so mostrar um numero em cima da cena com personagens: "hud": {"contador": {"de": 0, "para": -40, "un": "graus", "na": "<palavra>"}}; se a frase nao e' explicacao: "explica": false

## Cena b3 - Os químicos desenhavam correntes retas, e nada fechava a conta. Era um...
- Cenario: interior madeira | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (2): COL (variante 0, expressao bored); KEK (variante 0, expressao sad, segura paper)
- Animacao: conversar | interacao: entregar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): quebracabeca, quimicos
- RISCOS: nenhum

## Cena b4 - Numa noite fria, ele virou a cadeira para a lareira, e cochilou.
- Cenario: interior madeira | luz: noite | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto
- Personagens principais (1): KEK (variante 0, expressao bored)
- Animacao: reagir
- Objetos/modelos: kit/fireplace, mk/Chair_1
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cadeira, lareira
- RISCOS: nenhum

## Cena b5 - No sonho, os átomos dançavam como cobras. Até que uma delas mordeu o p...
- Cenario: interior madeira | luz: study | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (1): KEK (variante 0, expressao surprised)
- Animacao: reagir
- Objetos/modelos: kit/snake_ring, mk/Chair_1, kit/cobra
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): atomos, proprio, sonho
- RISCOS: 
  - frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada -> CORRECAO: "explica": {"objeto": "kit/<objeto>", "vfx": [{"k": "jato", "na": "<palavra>"}], "rotulos": [["NOME", "baixo", "<palavra>"]], "setas": [["cima", "FORCA"]], "medidor"/"passos"/"comparar": ...} (GUIA_DO_ROTEIRISTA.md "Cena de explicacao"); para so mostrar um numero em cima da cena com personagens: "hud": {"contador": {"de": 0, "para": -40, "un": "graus", "na": "<palavra>"}}; se a frase nao e' explicacao: "explica": false

## Cena b6 - Kekulé acordou num pulo, como se tivesse levado um raio. O benzeno não...
- Cenario: interior madeira | luz: study | clima: limpo
- Camera: low = camera baixa, dramatica (virada)
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto
- Personagens principais (1): KEK (variante 0, expressao shock)
- Animacao: reagir
- Objetos/modelos: kit/snake_ring
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): anel, benzeno, corrente, raio
- RISCOS: nenhum

## Cena b7 - Passou o resto da noite desenhando o anel de seis carbonos. E a conta ...
- Cenario: interior loja | luz: study | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (1): KEK (variante 0, expressao grin, segura paper)
- Animacao: reagir
- Objetos/modelos: kit/snake_ring
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): anel, resto, seis
- RISCOS: nenhum

## Cena b8 - Os colegas ficaram de boca aberta. O anel explicava dezenas de substân...
- Cenario: interior madeira | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (2): KEK (variante 0, expressao smug); COL (variante 0, expressao shock)
- Animacao: conversar | interacao: entregar
- Objetos/modelos: kit/snake_ring
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): anel, boca, colegas, substancias
- RISCOS: nenhum

## Cena b9 - Vinte e cinco anos depois, numa festa em Berlim em honra ao anel, ele ...
- Cenario: interior pedra | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto
- Personagens principais (3): KEK (variante 0, expressao laugh); COL (variante 0, expressao grin); ALU (variante 0, expressao laugh)
- Animacao: comemorar | interacao: pular
- Objetos/modelos: kit/snake_ring
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): sonho
- RISCOS: nenhum

## Cena b10 - Até hoje há quem duvide da história. Mas o anel do benzeno virou base ...
- Cenario: street | luz: day | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (2): COL (variante 0, expressao suspicious); KEK (variante 0, expressao smile) | multidao: 18 de POV
- Animacao: - | batalha encenada
- Objetos/modelos: kit/marco_viena, kit/snake_ring
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): anel, benzeno, remedios
- RISCOS: nenhum

## Cena b11 - E ele deixou um conselho: aprendam a sonhar. Mas confiram tudo acordad...
- Cenario: street | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (1): KEK (variante 0, expressao smile)
- Animacao: reagir
- Objetos/modelos: kit/snake_ring, kit/marco_viena
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): conselho, sonhar
- RISCOS: nenhum

## Cena b12 - Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?
- Cenario: street | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto
- Personagens principais (1): KEK (variante 0, expressao grin)
- Animacao: conversar
- Objetos/modelos: kit/marco_viena
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): comentar, proximo, tema
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
kit/snake_ring | b0, b2, b5, b6, b7, b8, b9, b10, b11 | pronto (HEROI: aparece em close) | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/marco_viena | b0, b1, b10, b11, b12 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
buildings/house_two | b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/lamppost | b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/fireplace | b4 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
mk/Chair_1 | b4, b5 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: kit/snake_ring | grandes momentos: b1, b10 | planos abertos: 2 | mistura: close 15% | medio 76% | aberto 5% | detalhe 3%
- Interacoes: b0 cochichar, b2 discutir, b3 entregar, b8 entregar, b9 pular
- RISCOS GERAIS: 
  - FOLHA 4: a pesquisa de campo ainda nao foi feita -> CORRECAO: python3 pesquisar.py kekule1865  (busca cada item na internet, baixa os prints e monta o quadro de referencias); depois OLHE referencias/kekule1865/moodboard.jpg

## RESUMO: 3 risco(s) em aberto
- b2: frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada
- b5: frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada
- geral: FOLHA 4: a pesquisa de campo ainda nao foi feita

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh kekule1865 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh kekule1865` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
