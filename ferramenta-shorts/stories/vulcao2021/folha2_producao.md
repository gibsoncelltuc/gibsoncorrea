# FOLHA 2 - PRODUCAO: Poder e Fama EP 17 - Bitcoin Feito com Vulcão

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/vulcao2021/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py vulcao2021` de novo ate esta folha sair sem risco.

## Cena b0 - O presidente de El Salvador resolveu fabricar dinheiro digital com a e...
- Cenario: loc_campo | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (2): BUK (variante 0, expressao smug); ENG (variante 0, expressao surprised)
- Animacao: conversar | interacao: o outro se aproxima
- Objetos/modelos: kit/bitcoin, kit/volcano
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): energia, presidente, vulcao
- RISCOS: nenhum

## Cena b1 - El Salvador é um país pequeno da América Central, cheio de vulcões.
- Cenario: loc_campo | luz: day | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): POV (variante 0, expressao smile) | multidao: 0 de 
- Animacao: -
- Objetos/modelos: kit/volcano
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): america, vulcoes
- RISCOS: nenhum

## Cena b2 - Em dois mil e vinte e um, Nayib Bukele fez do bitcoin uma moeda oficia...
- Cenario: loc_pista | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): BUK (variante 0, expressao grin); ENA (variante 0, expressao suspicious)
- Animacao: conversar | interacao: insiste
- Objetos/modelos: kit/bitcoin, kit/coin
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): bitcoin, dolar, moeda, nayib
- RISCOS: nenhum

## Cena b3 - Só que, para criar bitcoins novos, computadores fazem contas sem parar...
- Cenario: interior loja | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (2): ENG (variante 0, expressao worried, segura paper); BUK (variante 0, expressao suspicious)
- Animacao: discutir | interacao: discutir
- Objetos/modelos: kit/miners, kit/bitcoin
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): -
- RISCOS: nenhum

## Cena b4 - Então ele mandou a empresa de energia do governo usar o calor do vulcã...
- Cenario: loc_campo | luz: day | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): BUK (variante 0, expressao smug) | multidao: 0 de 
- Animacao: encena
- Objetos/modelos: kit/volcano
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): calor, empresa, energia, governo, vulcao
- RISCOS: nenhum

## Cena b5 - O vapor quente que sai de dentro da terra gira turbinas, e vira eletri...
- Cenario: loc_pista | luz: day | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): ENA (variante 0, expressao grin) | multidao: 0 de 
- Animacao: -
- Objetos/modelos: kit/volcano, kit/turbina
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): dentro, terra, vapor
- RISCOS: 
  - frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada -> CORRECAO: "explica": {"objeto": "kit/<objeto>", "vfx": [{"k": "jato", "na": "<palavra>"}], "rotulos": [["NOME", "baixo", "<palavra>"]], "setas": [["cima", "FORCA"]], "medidor"/"passos"/"comparar": ...} (GUIA_DO_ROTEIRISTA.md "Cena de explicacao"); para so mostrar um numero em cima da cena com personagens: "hud": {"contador": {"de": 0, "para": -40, "un": "graus", "na": "<palavra>"}}; se a frase nao e' explicacao: "explica": false

## Cena b6 - Acontece que, ao lado da usina, instalaram centenas de computadores só...
- Cenario: interior loja | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (2): ENG (variante 0, expressao surprised); ENA (variante 0, expressao grin)
- Animacao: conversar | interacao: vai ate o outro
- Objetos/modelos: kit/miners, kit/bitcoin
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): computadores, usina
- RISCOS: nenhum

## Cena b7 - Em outubro saiu o primeiro: um pedacinho de bitcoin que valia uns duze...
- Cenario: loc_pista | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (1): BUK (variante 0, expressao grin)
- Animacao: comemorar
- Objetos/modelos: kit/bitcoin
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): bitcoin, pedacinho
- RISCOS: nenhum

## Cena b8 - Bukele comemorou nas redes sociais, com um vídeo da usina no vulcão.
- Cenario: loc_pista | luz: day | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (1): BUK (variante 0, expressao laugh) | multidao: 0 de 
- Animacao: comemorar | batalha encenada
- Objetos/modelos: kit/volcano
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): redes, usina, video, vulcao
- RISCOS: nenhum

## Cena b9 - Anos depois, o governo contava quase quinhentos bitcoins minerados com...
- Cenario: loc_patio | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): ENA (variante 0, expressao smile, segura paper); ENG (variante 0, expressao grin)
- Animacao: conversar | interacao: aproxima-se
- Objetos/modelos: kit/bitcoin, kit/volcano
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): forca, governo, vulcao
- RISCOS: nenhum

## Cena b10 - E ele ainda anunciou o plano de uma Cidade Bitcoin, construída aos pés...
- Cenario: loc_cidade | luz: day | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (1): POV (variante 0, expressao surprised) | multidao: 0 de 
- Animacao: encena | batalha encenada
- Objetos/modelos: kit/volcano, kit/bitcoin, buildings/apartment, buildings/house_two, nature/lamppost
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cidade, plano
- RISCOS: nenhum

## Cena b11 - Dinheiro tirado de vulcão. Parece ficção, mas aconteceu de verdade.
- Cenario: loc_patio | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto
- Personagens principais (1): BUK (variante 0, expressao smile)
- Animacao: comemorar
- Objetos/modelos: kit/bitcoin, kit/volcano
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): vulcao
- RISCOS: nenhum

## Cena b12 - Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?
- Cenario: loc_campo | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto
- Personagens principais (1): BUK (variante 0, expressao grin)
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): comentar, proximo, tema
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
kit/bitcoin | b0, b2, b3, b6, b7, b9, b10, b11 | pronto (HEROI: aparece em close) | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/volcano | b0, b1, b4, b5, b8, b9, b10, b11 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/coin | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/miners | b3, b6 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/turbina | b5 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
buildings/apartment | b10 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
buildings/house_two | b10 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/lamppost | b10 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: kit/bitcoin | grandes momentos: b8, b10 | planos abertos: 5 | mistura: close 10% | medio 56% | aberto 27% | detalhe 6%
- Interacoes: b0 o outro se aproxima, b2 insiste, b3 discutir, b6 vai ate o outro, b9 aproxima-se
- RISCOS GERAIS: 
  - video com ~72 s (o padrao e' 60 s; aceito de 54 a 66, ja com a chamada final) -> CORRECAO: cortar frases que nao mudam a imagem ate ficar em ~60 s (com esta voz, ~150 palavras no total)
  - FOLHA 4: a pesquisa de campo ainda nao foi feita -> CORRECAO: python3 pesquisar.py vulcao2021  (busca cada item na internet, baixa os prints e monta o quadro de referencias); depois OLHE referencias/vulcao2021/moodboard.jpg
  - roteiro sem pesquisa visual completa (falta: local, quando, participantes, roupas, cenario, objetos, fontes_visuais) -> CORRECAO: pesquisar fotos/quadros/videos do fato e preencher "visual" no topo do beats.json (veja GUIA_DO_ROTEIRISTA.md "Pesquisa visual") e ajustar figurino, cenario e objetos a ela

## RESUMO: 4 risco(s) em aberto
- b5: frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada
- geral: video com ~72 s (o padrao e' 60 s; aceito de 54 a 66, ja com a chamada final)
- geral: FOLHA 4: a pesquisa de campo ainda nao foi feita
- geral: roteiro sem pesquisa visual completa (falta: local, quando, participantes, roupas, cenario, objetos, fontes_visuais)

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh vulcao2021 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh vulcao2021` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
