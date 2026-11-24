# FOLHA 2 - PRODUCAO: Guerras Inusitadas EP 05 - Os Gansos que Salvaram Roma

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/gansos390/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py gansos390` de novo ate esta folha sair sem risco.

## Cena b0 - Um bando de gansos barulhentos salvou Roma de um ataque noturno.
- Cenario: loc_campo | luz: dia | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (2): ROM (variante 0, expressao nervous); ROM (variante 1, expressao pained)
- Animacao: reagir | interacao: susto
- Objetos/modelos: goose
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): ataque, bando, gansos
- RISCOS: 
  - a narracao fala de BATALHA/ATAQUE e a cena nao encena a luta -> CORRECAO: "batalha": true nesta cena (tropa dos dois lados no "crowd", tiros/golpes e gente fugindo); cada batalha citada no roteiro = uma cena com "batalha": true

## Cena b1 - Em trezentos e noventa antes de Cristo, os gauleses de Breno tomaram a...
- Cenario: loc_campo | luz: day | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (3): GAU (variante 0, expressao angry, segura torch); GAU (variante 1, expressao shout, segura torch); GAU (variante 2, expressao grin, segura torch) | multidao: 16 de GAU/ROM
- Animacao: encena | batalha encenada
- Objetos/modelos: kit/fire, buildings/apartment, buildings/house_two, nature/lamppost
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): breno, cidade, cristo, gauleses
- RISCOS: nenhum

## Cena b2 - Os romanos que sobraram se trancaram no Capitólio, uma colina fortific...
- Cenario: mountain | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (3): ROM (variante 0, expressao nervous); ROM (variante 1, expressao pained); MAN (variante 0, expressao stern)
- Animacao: reagir | interacao: insiste
- Objetos/modelos: buildings/castle_tower
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): capitolio, colina, romanos
- RISCOS: nenhum

## Cena b3 - Os gauleses cercaram a colina, e a fome apertou os dois lados.
- Cenario: mountain | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (2): ROM (variante 1, expressao pained); GAU (variante 0, expressao stern)
- Animacao: conversar | interacao: o outro se aproxima
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): colina, dois, fome, gauleses
- RISCOS: nenhum

## Cena b4 - Numa noite, eles tentaram escalar em silêncio, e os guardas não ouvira...
- Cenario: loc_montanha | luz: noite | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (2): GAU (variante 0, expressao stern); GAU (variante 1, expressao grin) | multidao: 8 de GAU
- Animacao: encena
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): guardas
- RISCOS: nenhum

## Cena b5 - Acontece que os gansos sagrados da deusa Juno ouviram, e começaram a g...
- Cenario: loc_montanha | luz: noite | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (1): ROM (variante 2, expressao shock)
- Animacao: reagir
- Objetos/modelos: goose
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): deusa, gansos, gritar
- RISCOS: nenhum

## Cena b6 - O barulho acordou o soldado Marco Mânlio, que correu para a muralha e ...
- Cenario: loc_montanha | luz: noite | clima: limpo
- Camera: track = travelling lateral acompanhando quem anda
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto -> direita baixa
- Personagens principais (2): MAN (variante 0, expressao angry); GAU (variante 0, expressao scared)
- Animacao: encena
- Objetos/modelos: buildings/castle_tower
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): barulho, muralha, soldado, subida
- RISCOS: nenhum

## Cena b7 - O ataque fracassou, mas o cerco ainda durou sete meses.
- Cenario: loc_montanha | luz: noite | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (3): ROM (variante 0, expressao angry); MAN (variante 0, expressao shout); GAU (variante 0, expressao scared) | multidao: 18 de ROM/GAU
- Animacao: encena | batalha encenada
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): ataque, cerco
- RISCOS: nenhum

## Cena b8 - No fim, Roma pagou mil libras de ouro, e os gauleses foram embora.
- Cenario: interior pedra | luz: dia | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (2): ROM (variante 0, expressao sad, segura coin); GAU (variante 0, expressao grin, segura coin)
- Animacao: encena | interacao: entregar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): gauleses, ouro
- RISCOS: nenhum

## Cena b9 - Os gansos salvaram a colina, mas o ouro foi embora do mesmo jeito.
- Cenario: mountain | luz: dia | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (2): ROM (variante 0, expressao smile); ROM (variante 1, expressao grin)
- Animacao: conversar | interacao: aproxima-se
- Objetos/modelos: goose
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): colina, gansos, ouro
- RISCOS: nenhum

## Cena b10 - Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?
- Cenario: loc_campo | luz: dia | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (1): ROM (variante 0, expressao grin)
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): comentar, proximo, tema
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
goose | b0, b5, b9 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/fire | b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
buildings/apartment | b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
buildings/house_two | b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/lamppost | b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
buildings/castle_tower | b2, b6 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: - | grandes momentos: b1, b7 | planos abertos: 3 | mistura: close 13% | medio 67% | aberto 16% | detalhe 4%
- Interacoes: b0 susto, b2 insiste, b3 o outro se aproxima, b8 entregar, b9 aproxima-se
- RISCOS GERAIS: 
  - video com ~66 s (o padrao e' 60 s; aceito de 54 a 66, ja com a chamada final) -> CORRECAO: cortar frases que nao mudam a imagem ate ficar em ~60 s (com esta voz, ~150 palavras no total)

## RESUMO: 2 risco(s) em aberto
- b0: a narracao fala de BATALHA/ATAQUE e a cena nao encena a luta
- geral: video com ~66 s (o padrao e' 60 s; aceito de 54 a 66, ja com a chamada final)

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh gansos390 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh gansos390` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
