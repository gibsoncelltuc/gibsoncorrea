# FOLHA 2 - PRODUCAO: Poder e Fama EP 25 - O Carro que Voou de Cabeça para Baixo

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/roadsterpulo2026/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py roadsterpulo2026` de novo ate esta folha sair sem risco.

## Cena b0 - Elon Musk prometeu um carro que voa. Em outubro de dois mil e vinte e ...
- Cenario: loc_deserto | luz: noite | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (2): MUS (variante 0, expressao grin); ENA (variante 0, expressao surprised) | multidao: 0 de MUS/ENA
- Animacao: conversar | interacao: insiste
- Objetos/modelos: kit/roadster26, kit/torre_luz, kit/tower
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): carro, dois
- RISCOS: nenhum

## Cena b1 - Foi à noite, numa base de testes da SpaceX em McGregor, no Texas, dian...
- Cenario: loc_deserto | luz: noite | clima: limpo
- Camera: reveal = ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (2): POV (variante 0, expressao smile); POV (variante 1, expressao grin) | multidao: 6 de POV
- Animacao: encena
- Objetos/modelos: kit/rampa_curva, kit/torre_luz, kit/tower
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): convidados, spacex, testes, texas
- RISCOS: nenhum

## Cena b2 - O novo Roadster da Tesla tinha sido prometido em dois mil e dezessete....
- Cenario: interior galpao | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto
- Personagens principais (2): ENG (variante 0, expressao suspicious, segura paper); MUS (variante 0, expressao smug)
- Animacao: conversar | interacao: vai ate o outro
- Objetos/modelos: kit/roadster26
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): atraso, novo, tesla
- RISCOS: nenhum

## Cena b3 - O segredo eram propulsores da SpaceX escondidos no carro, e ventilador...
- Cenario: interior galpao | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto
- Personagens principais (2): ENA (variante 0, expressao grin, segura paper); ENG (variante 0, expressao surprised)
- Animacao: conversar | interacao: cochichar | o ultimo personagem ENTRA andando
- Objetos/modelos: kit/roadster26
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): carro, pista, segredo, spacex
- RISCOS: 
  - frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada -> CORRECAO: "explica": {"objeto": "kit/<objeto>", "vfx": [{"k": "jato", "na": "<palavra>"}], "rotulos": [["NOME", "baixo", "<palavra>"]], "setas": [["cima", "FORCA"]], "medidor"/"passos"/"comparar": ...} (GUIA_DO_ROTEIRISTA.md "Cena de explicacao"); para so mostrar um numero em cima da cena com personagens: "hud": {"contador": {"de": 0, "para": -40, "un": "graus", "na": "<palavra>"}}; se a frase nao e' explicacao: "explica": false

## Cena b4 - Acontece que, diante dos convidados, o carro acelerou, subiu uma rampa...
- Cenario: loc_deserto | luz: noite | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): MUS (variante 0, expressao grin) | multidao: 0 de POV
- Animacao: encena
- Objetos/modelos: kit/roadster26, kit/torre_luz, kit/tower
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cabeca, carro, convidados, rampa
- RISCOS: nenhum

## Cena b5 - Então se soltou, voou girando no ar e pousou numa nuvem de fumaça bran...
- Cenario: loc_deserto | luz: noite | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto
- Personagens principais (1): ENA (variante 0, expressao shock) | multidao: 0 de POV
- Animacao: reagir
- Objetos/modelos: kit/roadster26, kit/torre_luz, kit/tower
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): fumaca
- RISCOS: nenhum

## Cena b6 - Musk comemorou no palco, e tudo foi transmitido ao vivo na rede X.
- Cenario: loc_deserto | luz: noite | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo
- Personagens principais (2): MUS (variante 0, expressao laugh); ENG (variante 0, expressao surprised)
- Animacao: comemorar | interacao: pular
- Objetos/modelos: kit/torre_luz, kit/tower
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): palco, rede
- RISCOS: nenhum

## Cena b7 - Mas especialistas lembraram: aquilo durou poucos segundos, não foi um ...
- Cenario: loc_cidade | luz: day | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (2): ENG (variante 0, expressao suspicious); ENA (variante 0, expressao bored) | multidao: 12 de POV
- Animacao: - | batalha encenada
- Objetos/modelos: kit/tower
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): -
- RISCOS: nenhum

## Cena b8 - Segundo a Tesla, ele vai de zero a cem em menos de um segundo.
- Cenario: loc_cidade | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto
- Personagens principais (2): ENG (variante 0, expressao grin, segura paper); POV (variante 0, expressao surprised)
- Animacao: conversar | interacao: aproxima-se
- Objetos/modelos: kit/roadster26, kit/tower
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): tesla, zero
- RISCOS: 
  - frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada -> CORRECAO: "explica": {"objeto": "kit/<objeto>", "vfx": [{"k": "jato", "na": "<palavra>"}], "rotulos": [["NOME", "baixo", "<palavra>"]], "setas": [["cima", "FORCA"]], "medidor"/"passos"/"comparar": ...} (GUIA_DO_ROTEIRISTA.md "Cena de explicacao"); para so mostrar um numero em cima da cena com personagens: "hud": {"contador": {"de": 0, "para": -40, "un": "graus", "na": "<palavra>"}}; se a frase nao e' explicacao: "explica": false

## Cena b9 - O vídeo correu o mundo. Metade ficou impressionada, a outra metade des...
- Cenario: loc_cidade | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo
- Personagens principais (1): POV (variante 0, expressao laugh)
- Animacao: conversar
- Objetos/modelos: kit/tower
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): video
- RISCOS: nenhum

## Cena b10 - Carro voador ou carro que pula? Você decide.
- Cenario: interior galpao | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo
- Personagens principais (1): MUS (variante 0, expressao smile) | multidao: 0 de MUS
- Animacao: conversar
- Objetos/modelos: kit/roadster26
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): -
- RISCOS: nenhum

## Cena b11 - Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?
- Cenario: interior galpao | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo
- Personagens principais (1): MUS (variante 0, expressao grin)
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): comentar, proximo, tema
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
kit/roadster26 | b0, b2, b3, b4, b5, b8, b10 | pronto (HEROI: aparece em close) | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/torre_luz | b0, b1, b4, b5, b6 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/tower | b0, b1, b4, b5, b6, b7, b8, b9 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/rampa_curva | b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: kit/roadster26 | grandes momentos: b7 | planos abertos: 3 | mistura: close 16% | medio 66% | aberto 19% | detalhe 0%
- Interacoes: b0 insiste, b2 vai ate o outro, b3 cochichar, b6 pular, b8 aproxima-se
- RISCOS GERAIS: nenhum

## RESUMO: 2 risco(s) em aberto
- b3: frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada
- b8: frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh roadsterpulo2026 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh roadsterpulo2026` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
