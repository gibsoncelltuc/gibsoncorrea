# FOLHA 2 - PRODUCAO: As Guerras do Bacalhau

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/bacalhau1958/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py bacalhau1958` de novo ate esta folha sair sem risco.

## Cena b0 - Entre mil novecentos e cinquenta e oito e mil novecentos e setenta e s...
- Cenario: harbor | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 5 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): ICE (variante 0, expressao stern); BRI (variante 0, expressao stern)
- Animacao: conversar | interacao: o outro se aproxima
- Objetos/modelos: ship, kit/cod
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): inglaterra, islandia, peixe
- RISCOS: 
  - objeto sem modelo 3D: peixe -> CORRECAO: modelar em blender/make_objetos.py e por no OBJ_DICT, ou trocar a palavra

## Cena b1 - A Islândia é pequena, e vivia da pesca. Mas barcos ingleses pescavam b...
- Cenario: harbor | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): ICE (variante 1, expressao nervous); PES (variante 0, expressao grin)
- Animacao: conversar | interacao: insiste
- Objetos/modelos: crate, kit/cod
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): costa, islandia, pesca
- RISCOS: nenhum

## Cena b2 - Então a Islândia aumentou os limites do seu mar: doze milhas, cinquent...
- Cenario: street | luz: day | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): ICE (variante 2, expressao stern) | multidao: 6 de POV
- Animacao: reagir
- Objetos/modelos: ship
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): islandia, limites
- RISCOS: 
  - a narracao cita agua e o cenario "street" nao tem agua -> CORRECAO: "set": "harbor" (cais com mar e navio) ou "set": "palace" (praia), ou "mapa" para so situar

## Cena b3 - A Inglaterra mandou a marinha para proteger os barcos de pesca.
- Cenario: harbor | luz: day | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua) [momento criado pela ferramenta]
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (3): BRI (variante 1, expressao stern); BRI (variante 2, expressao grin); PES (variante 1, expressao smile) | multidao: 12 de POV
- Animacao: conversar | batalha encenada
- Objetos/modelos: ship, navios ao fundo
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): barcos, inglaterra, marinha, pesca
- RISCOS: nenhum

## Cena b4 - A Islândia só tinha uns barquinhos da guarda costeira, mas eles tinham...
- Cenario: interior madeira | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto
- Personagens principais (1): ICE (variante 0, expressao grin)
- Animacao: reagir
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): arma, guarda, islandia, rede
- RISCOS: nenhum

## Cena b5 - Eles cortavam os cabos das redes inglesas, e os navios batiam um no ou...
- Cenario: harbor | luz: day | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (1): ICE (variante 0, expressao neutral) | multidao: 6 de POV
- Animacao: encena | batalha encenada
- Objetos/modelos: ship, navios ao fundo
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cabos, navios, proposito, redes
- RISCOS: nenhum

## Cena b6 - A Islândia ainda ameaçou fechar a base da Otan no país.
- Cenario: street | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): ICE (variante 1, expressao stern); BRI (variante 0, expressao shock)
- Animacao: conversar | interacao: susto
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): base, islandia, otan
- RISCOS: nenhum

## Cena b7 - Em mil novecentos e setenta e seis, os ingleses cederam, e a ideia de ...
- Cenario: street | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (2): BRI (variante 0, expressao pained); ICE (variante 0, expressao laugh)
- Animacao: conversar | interacao: vai ate o outro
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): duzentas, ingleses, zona
- RISCOS: nenhum

## Cena b8 - Foi uma guerra de navios batendo e de redes cortadas, e tudo por causa...
- Cenario: harbor | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto
- Personagens principais (1): PES (variante 0, expressao laugh)
- Animacao: reagir
- Objetos/modelos: crate, kit/cod
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): navios, peixe, redes
- RISCOS: 
  - objeto sem modelo 3D: peixe -> CORRECAO: modelar em blender/make_objetos.py e por no OBJ_DICT, ou trocar a palavra

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
ship | b0, b2, b3, b5 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/cod | b0, b1, b8 | pronto (HEROI: aparece em close) | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
crate | b1, b8 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
peixe (citado na narracao) | b0, b8 | FALTA | pesquisar referencia (referencias/LEIA.md) e modelar: `blender/objetos_<sessao>.py` com formas.py -> `kit/peixe.glb` (altura real em metros; cores chapadas; partes redondas com cil/bola/torno); cadastrar em `obj_dict.d/<sessao>.json`; `blender -b --python blender/objetos_<sessao>.py`; `python3 capacidades.py`; depois rodar este roteiro de novo


## Video inteiro
- Objeto heroi: kit/cod | grandes momentos: b3, b5 | planos abertos: 3 | mistura: close 26% | medio 50% | aberto 16% | detalhe 8%
- Interacoes: b0 o outro se aproxima, b1 insiste, b6 susto, b7 vai ate o outro
- RISCOS GERAIS: 
  - pouca variedade de cenario ({'harbor': 5, 'street': 3, 'interior madeira': 1}): o video fica parecendo todos os outros -> CORRECAO: pelo menos 3 lugares e nenhum em mais da metade das cenas: troque "set"/"interior" de algumas cenas (lugares: outback, countryside, arctic, palace, harbor, mountain, medieval, jungle, hall, stadium, street | interior: madeira, pedra, loja)

## RESUMO: 4 risco(s) em aberto
- b0: objeto sem modelo 3D: peixe
- b2: a narracao cita agua e o cenario "street" nao tem agua
- b8: objeto sem modelo 3D: peixe
- geral: pouca variedade de cenario ({'harbor': 5, 'street': 3, 'interior madeira': 1}): o video fica parecendo todos os outros

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh bacalhau1958 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh bacalhau1958` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
