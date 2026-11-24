# FOLHA 2 - PRODUCAO: Poder e Fama EP 05 - Cem Dias ou de Graça

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/bateria2017/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py bateria2017` de novo ate esta folha sair sem risco.

## Cena b0 - Em março de dois mil e dezessete, Elon Musk respondeu no Twitter ao em...
- Cenario: interior loja | luz: golden | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto
- Personagens principais (1): MUS (variante 0, expressao smug)
- Animacao: conversar
- Objetos/modelos: kit/megapack
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): dois, twitter
- RISCOS: nenhum

## Cena b1 - Musk escreveu que a Tesla instalaria baterias gigantes na Austrália do...
- Cenario: outback | luz: golden | clima: limpo
- Camera: reveal = ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (2): MUS (variante 0, expressao grin); CAN (variante 0, expressao shock) | multidao: 8 de POV
- Animacao: reagir
- Objetos/modelos: kit/megapack, kit/marco_goldengate, kit/roadster
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): australia, graca, tesla
- RISCOS: 
  - frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada -> CORRECAO: "explica": {"objeto": "kit/<objeto>", "vfx": [{"k": "jato", "na": "<palavra>"}], "rotulos": [["NOME", "baixo", "<palavra>"]], "setas": [["cima", "FORCA"]], "medidor"/"passos"/"comparar": ...} (GUIA_DO_ROTEIRISTA.md "Cena de explicacao"); para so mostrar um numero em cima da cena com personagens: "hud": {"contador": {"de": 0, "para": -40, "un": "graus", "na": "<palavra>"}}; se a frase nao e' explicacao: "explica": false

## Cena b2 - Os jornais calcularam que ele podia perder mais de cinquenta milhões d...
- Cenario: outback | luz: golden | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo
- Personagens principais (3): MUS (variante 0, expressao worried); CAN (variante 0, expressao suspicious); POV (variante 0, expressao shock) | multidao: 10 de POV
- Animacao: conversar | interacao: aproxima-se | batalha encenada
- Objetos/modelos: kit/megapack, kit/marco_goldengate
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cinquenta, dolares, jornais
- RISCOS: nenhum

## Cena b3 - O contrato foi fechado no fim de setembro, e o prazo de cem dias começ...
- Cenario: interior pedra | luz: golden | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto
- Personagens principais (2): MUS (variante 0, expressao nervous); JOR (variante 0, expressao suspicious)
- Animacao: reagir | interacao: avanca e o outro recua
- Objetos/modelos: kit/megapack
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): contrato, prazo, setembro
- RISCOS: nenhum

## Cena b4 - Acontece que a bateria ficou pronta em cerca de cinquenta e cinco dias...
- Cenario: outback | luz: golden | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (1): MUS (variante 0, expressao grin) | multidao: 10 de POV
- Animacao: - | batalha encenada
- Objetos/modelos: kit/megapack, kit/marco_goldengate, nature/picket_fence
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): bateria, cinquenta, prazo
- RISCOS: nenhum

## Cena b5 - A imprensa chamou de a maior bateria do mundo, com cem megawatts de po...
- Cenario: outback | luz: golden | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): JOR (variante 0, expressao shock); JOR2 (variante 0, expressao laugh)
- Animacao: reagir | interacao: o outro se aproxima
- Objetos/modelos: kit/megapack, kit/marco_goldengate
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): imprensa, potencia
- RISCOS: 
  - frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada -> CORRECAO: "explica": {"objeto": "kit/<objeto>", "vfx": [{"k": "jato", "na": "<palavra>"}], "rotulos": [["NOME", "baixo", "<palavra>"]], "setas": [["cima", "FORCA"]], "medidor"/"passos"/"comparar": ...} (GUIA_DO_ROTEIRISTA.md "Cena de explicacao"); para so mostrar um numero em cima da cena com personagens: "hud": {"contador": {"de": 0, "para": -40, "un": "graus", "na": "<palavra>"}}; se a frase nao e' explicacao: "explica": false

## Cena b6 - Mike Cannon-Brookes disse que nunca tinha ficado tão feliz de perder u...
- Cenario: interior loja | luz: golden | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo
- Personagens principais (1): CAN (variante 0, expressao laugh)
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): aposta, perder
- RISCOS: nenhum

## Cena b7 - Ou seja, uma conversa no Twitter virou uma obra de cinquenta e cinco d...
- Cenario: outback | luz: golden | clima: limpo
- Camera: close = close no rosto; empurra devagar + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (1): CAN (variante 0, expressao grin)
- Animacao: conversar
- Objetos/modelos: kit/megapack, kit/marco_goldengate
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cinquenta, conversa, obra, twitter
- RISCOS: nenhum

## Cena b8 - E tudo começou com uma resposta curta, escrita no celular.
- Cenario: loc_campo | luz: golden | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): MUS (variante 0, expressao laugh); JOR (variante 0, expressao shock)
- Animacao: conversar | interacao: susto
- Objetos/modelos: kit/megapack, kit/marco_goldengate, kit/phone
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): celular
- RISCOS: nenhum

## Cena b9 - Moral da história: antes de apostar cinquenta milhões num prazo, leia ...
- Cenario: loc_campo | luz: golden | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (2): MUS (variante 0, expressao laugh); CAN (variante 0, expressao grin) | multidao: 30 de POV
- Animacao: encena
- Objetos/modelos: kit/megapack, kit/marco_goldengate
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): apostar, contrato
- RISCOS: nenhum

## Cena b10 - Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?
- Cenario: loc_campo | luz: golden | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo
- Personagens principais (1): MUS (variante 0, expressao grin)
- Animacao: conversar
- Objetos/modelos: kit/marco_goldengate
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): comentar, proximo, tema
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
kit/megapack | b0, b1, b2, b3, b4, b5, b7, b8, b9 | pronto (HEROI: aparece em close) | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/marco_goldengate | b1, b2, b4, b5, b7, b8, b9, b10 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/roadster | b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/picket_fence | b4 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/phone | b8 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: kit/megapack | grandes momentos: b2, b4 | planos abertos: 3 | mistura: close 36% | medio 39% | aberto 19% | detalhe 6%
- Interacoes: b2 aproxima-se, b3 avanca e o outro recua, b5 o outro se aproxima, b8 susto
- RISCOS GERAIS: 
  - o video ABRE com a data (gancho fraco: o canal abre com o fato estranho e so depois situa) -> CORRECAO: reescrever a 1a frase com o fato mais absurdo da historia (sem ano); a data entra na 2a frase ou no mapa
  - FOLHA 4: a pesquisa de campo ainda nao foi feita -> CORRECAO: python3 pesquisar.py bateria2017  (busca cada item na internet, baixa os prints e monta o quadro de referencias); depois OLHE referencias/bateria2017/moodboard.jpg
  - roteiro sem pesquisa visual completa (falta: local, quando, participantes, roupas, cenario, objetos, fontes_visuais) -> CORRECAO: pesquisar fotos/quadros/videos do fato e preencher "visual" no topo do beats.json (veja GUIA_DO_ROTEIRISTA.md "Pesquisa visual") e ajustar figurino, cenario e objetos a ela

## RESUMO: 5 risco(s) em aberto
- b1: frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada
- b5: frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada
- geral: o video ABRE com a data (gancho fraco: o canal abre com o fato estranho e so depois situa)
- geral: FOLHA 4: a pesquisa de campo ainda nao foi feita
- geral: roteiro sem pesquisa visual completa (falta: local, quando, participantes, roupas, cenario, objetos, fontes_visuais)

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh bateria2017 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh bateria2017` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
