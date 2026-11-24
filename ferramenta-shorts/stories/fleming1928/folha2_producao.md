# FOLHA 2 - PRODUCAO: Curiosidade e Ciência EP 04 - Fleming e a Penicilina

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/fleming1928/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py fleming1928` de novo ate esta folha sair sem risco.

## Cena b0 - Um mofo esquecido no meio da bagunça acabou salvando milhões de vidas.
- Cenario: loc_campo | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): FLE (variante 0, expressao smile, segura book); COL (variante 0, expressao surprised)
- Animacao: conversar | interacao: aproxima-se
- Objetos/modelos: kit/marco_bigben, kit/petri
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): bagunca, mofo, vidas
- RISCOS: nenhum

## Cena b1 - Era mil novecentos e vinte e oito, num hospital de Londres, e o cienti...
- Cenario: loc_campo | luz: day | clima: limpo
- Camera: reveal = ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (2): MED (variante 0, expressao neutral); MED (variante 1, expressao smile) | multidao: 8 de MED/POV
- Animacao: -
- Objetos/modelos: kit/marco_bigben
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cientista, londres
- RISCOS: nenhum

## Cena b2 - Ele estudava bactérias, e deixava os pratos de cultura empilhados na b...
- Cenario: interior hospital | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto
- Personagens principais (2): FLE (variante 0, expressao neutral, segura book); COL (variante 0, expressao suspicious)
- Animacao: conversar | interacao: avanca e o outro recua
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): bancada, cultura, pratos
- RISCOS: 
  - frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada -> CORRECAO: "explica": {"objeto": "kit/<objeto>", "vfx": [{"k": "jato", "na": "<palavra>"}], "rotulos": [["NOME", "baixo", "<palavra>"]], "setas": [["cima", "FORCA"]], "medidor"/"passos"/"comparar": ...} (GUIA_DO_ROTEIRISTA.md "Cena de explicacao"); para so mostrar um numero em cima da cena com personagens: "hud": {"contador": {"de": 0, "para": -40, "un": "graus", "na": "<palavra>"}}; se a frase nao e' explicacao: "explica": false

## Cena b3 - Um dia, ele saiu de férias por duas semanas e não limpou nada.
- Cenario: interior hospital | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (2): FLE (variante 0, expressao grin, segura bag); COL (variante 0, expressao shock)
- Animacao: reagir | interacao: susto | o ultimo personagem ENTRA andando
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): ferias
- RISCOS: nenhum

## Cena b4 - Quando voltou, achou um prato com bolor verde e disse: "Que sujeira!"
- Cenario: interior hospital | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (2): COL (variante 0, expressao smug); FLE (variante 0, expressao angry)
- Animacao: conversar | interacao: discutir
- Objetos/modelos: kit/petri, kit/gosma
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): bolor, prato
- RISCOS: nenhum

## Cena b5 - Ele ia jogar o prato fora, mas olhou melhor.
- Cenario: loc_montanha | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (1): FLE (variante 0, expressao suspicious)
- Animacao: conversar
- Objetos/modelos: kit/petri, kit/gosma
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): prato
- RISCOS: nenhum

## Cena b6 - Acontece que, em volta do mofo, as bactérias tinham sumido.
- Cenario: hall | luz: day | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (2): FLE (variante 0, expressao shock); COL (variante 0, expressao surprised) | multidao: 10 de MED/COL
- Animacao: reagir | batalha encenada
- Objetos/modelos: kit/petri
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): bacterias, mofo
- RISCOS: nenhum

## Cena b7 - O mofo soltava algo que matava as bactérias, e ele deu a isso o nome d...
- Cenario: interior hospital | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto
- Personagens principais (2): FLE (variante 0, expressao smile); COL (variante 0, expressao relief)
- Animacao: conversar | interacao: cochichar
- Objetos/modelos: kit/petri
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): bacterias, isso, mofo, penicilina
- RISCOS: 
  - frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada -> CORRECAO: "explica": {"objeto": "kit/<objeto>", "vfx": [{"k": "jato", "na": "<palavra>"}], "rotulos": [["NOME", "baixo", "<palavra>"]], "setas": [["cima", "FORCA"]], "medidor"/"passos"/"comparar": ...} (GUIA_DO_ROTEIRISTA.md "Cena de explicacao"); para so mostrar um numero em cima da cena com personagens: "hud": {"contador": {"de": 0, "para": -40, "un": "graus", "na": "<palavra>"}}; se a frase nao e' explicacao: "explica": false

## Cena b8 - Anos depois, outros cientistas transformaram o bolor em remédio, e ele...
- Cenario: loc_montanha | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (3): MED (variante 0, expressao smile); MED (variante 1, expressao grin); POV (variante 0, expressao relief)
- Animacao: comemorar | interacao: pular
- Objetos/modelos: kit/petri
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): bolor, pessoas
- RISCOS: nenhum

## Cena b9 - Fleming ganhou, junto com dois colegas, o prêmio Nobel em mil novecent...
- Cenario: hall | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto
- Personagens principais (2): FLE (variante 0, expressao laugh); COL (variante 0, expressao laugh) | multidao: 14 de MED/COL/POV
- Animacao: comemorar | interacao: o outro se aproxima | batalha encenada
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): dois, premio
- RISCOS: nenhum

## Cena b10 - No fim, a bagunça dele valeu mais que qualquer faxina.
- Cenario: interior madeira | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (1): FLE (variante 0, expressao smug)
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): bagunca
- RISCOS: nenhum

## Cena b11 - Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?
- Cenario: loc_campo | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (1): FLE (variante 0, expressao grin)
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): comentar, proximo, tema
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
kit/marco_bigben | b0, b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/petri | b0, b4, b5, b6, b7, b8 | pronto (HEROI: aparece em close) | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/gosma | b4, b5 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: kit/petri | grandes momentos: b6, b9 | planos abertos: 2 | mistura: close 20% | medio 65% | aberto 10% | detalhe 5%
- Interacoes: b0 aproxima-se, b2 avanca e o outro recua, b3 susto, b4 discutir, b7 cochichar, b8 pular, b9 o outro se aproxima
- RISCOS GERAIS: 
  - FOLHA 4: a pesquisa de campo ainda nao foi feita -> CORRECAO: python3 pesquisar.py fleming1928  (busca cada item na internet, baixa os prints e monta o quadro de referencias); depois OLHE referencias/fleming1928/moodboard.jpg
  - roteiro sem pesquisa visual completa (falta: local, quando, participantes, roupas, cenario, objetos, fontes_visuais) -> CORRECAO: pesquisar fotos/quadros/videos do fato e preencher "visual" no topo do beats.json (veja GUIA_DO_ROTEIRISTA.md "Pesquisa visual") e ajustar figurino, cenario e objetos a ela

## RESUMO: 4 risco(s) em aberto
- b2: frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada
- b7: frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada
- geral: FOLHA 4: a pesquisa de campo ainda nao foi feita
- geral: roteiro sem pesquisa visual completa (falta: local, quando, participantes, roupas, cenario, objetos, fontes_visuais)

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh fleming1928 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh fleming1928` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
