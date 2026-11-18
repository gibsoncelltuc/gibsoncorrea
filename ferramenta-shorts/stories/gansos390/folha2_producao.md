# FOLHA 2 - PRODUCAO: Guerras Inusitadas EP 05 - Os Gansos que Salvaram Roma

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/gansos390/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py gansos390` de novo ate esta folha sair sem risco.

## Cena b0 - Roma inteira foi salva por um bando de gansos barulhentos.
- Cenario: medieval | luz: dia | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (2): ROM (variante 0, expressao nervous); ROM (variante 1, expressao pained)
- Animacao: reagir | interacao: susto
- Objetos/modelos: goose
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): bando, gansos
- RISCOS: nenhum

## Cena b1 - Os gauleses tinham invadido a cidade, e queimado quase tudo. Quem não ...
- Cenario: medieval | luz: day | clima: limpo
- Camera: reveal = ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (3): GAU (variante 0, expressao grin); GAU (variante 1, expressao stern); GAU (variante 2, expressao stern) | multidao: 8 de GAU
- Animacao: -
- Objetos/modelos: buildings/apartment, buildings/house_two, nature/lamppost
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cidade, gauleses
- RISCOS: nenhum

## Cena b2 - Os romanos que sobraram se trancaram no Capitólio, uma colina cercada ...
- Cenario: medieval | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto -> direita baixa | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (3): ROM (variante 0, expressao nervous); ROM (variante 1, expressao pained); MAN (variante 0, expressao stern)
- Animacao: reagir | interacao: insiste
- Objetos/modelos: buildings/castle_tower
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): capitolio, colina, muralhas, romanos
- RISCOS: nenhum

## Cena b3 - Lá em cima, a fome apertava. "Vamos comer os gansos", pediu um soldado...
- Cenario: medieval | luz: day | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (2): ROM (variante 1, expressao pained); ROM (variante 2, expressao stern) | multidao: 10 de ROM
- Animacao: discutir
- Objetos/modelos: goose
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): fome, gansos, sacerdote, soldado
- RISCOS: nenhum

## Cena b4 - Numa noite sem lua, os gauleses escalaram a colina em silêncio. Os gua...
- Cenario: medieval | luz: noite | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto -> direita baixa
- Personagens principais (3): GAU (variante 0, expressao stern); GAU (variante 1, expressao nervous); GAU (variante 2, expressao stern)
- Animacao: conversar | interacao: aproxima-se
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cachorros, colina, gauleses, guardas
- RISCOS: 
  - animal sem modelo: cachorros -> CORRECAO: modelar o animal antes, ou tirar da narracao desta cena, ou mostrar so a reacao das pessoas
  - acao sem animacao propria: dormiam, escalaram -> CORRECAO: mostrar o RESULTADO (objeto em cena, reacao, efeito + som) ou reescrever a frase com acao que a ferramenta faz (andar, chegar, discutir, empurrar, entregar, comemorar, atirar, fugir)
  - objeto sem modelo 3D: cachorros -> CORRECAO: modelar em blender/make_objetos.py e por no OBJ_DICT, ou trocar a palavra

## Cena b5 - Acontece que os gansos acordaram, e começaram a gritar e a bater as as...
- Cenario: medieval | luz: day | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua) [momento criado pela ferramenta]
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (1): ROM (variante 2, expressao shock) | multidao: 12 de ROM
- Animacao: reagir | batalha encenada
- Objetos/modelos: goose
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): asas, bater, gansos, gritar
- RISCOS: nenhum

## Cena b6 - Um soldado chamado Mânlio pulou da cama, e empurrou o primeiro invasor...
- Cenario: medieval | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto -> direita baixa -> frente
- Personagens principais (2): MAN (variante 0, expressao shock); GAU (variante 0, expressao shock)
- Animacao: reagir | interacao: empurrar
- Objetos/modelos: buildings/castle_tower
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cama, gaules, soldado
- RISCOS: nenhum

## Cena b7 - O alarme acordou todo mundo, os romanos correram para a muralha, e o a...
- Cenario: medieval | luz: day | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (3): ROM (variante 0, expressao stern); MAN (variante 0, expressao stern); GAU (variante 0, expressao shock) | multidao: 16 de ROM/GAU
- Animacao: reagir | batalha encenada
- Objetos/modelos: buildings/castle_tower
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): alarme, ataque, muralha, romanos
- RISCOS: nenhum

## Cena b8 - Desde então, todo ano, os gansos ganhavam um desfile pelas ruas de Rom...
- Cenario: medieval | luz: dia | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): ROM (variante 0, expressao smile); ROM (variante 1, expressao grin)
- Animacao: conversar | interacao: o outro se aproxima
- Objetos/modelos: goose
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): desfile, gansos, roma
- RISCOS: nenhum

## Cena b9 - E os cachorros, que dormiram a noite inteira, um castigo.
- Cenario: medieval | luz: dia | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (1): ROM (variante 2, expressao grin)
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cachorros, castigo
- RISCOS: 
  - animal sem modelo: cachorros -> CORRECAO: modelar o animal antes, ou tirar da narracao desta cena, ou mostrar so a reacao das pessoas
  - objeto sem modelo 3D: cachorros -> CORRECAO: modelar em blender/make_objetos.py e por no OBJ_DICT, ou trocar a palavra

## Video inteiro
- Objeto heroi: - | grandes momentos: b5, b7 | planos abertos: 4 | mistura: close 10% | medio 61% | aberto 24% | detalhe 5%
- Interacoes: b0 susto, b2 insiste, b4 aproxima-se, b6 empurrar, b8 o outro se aproxima
- RISCOS GERAIS: 
  - video sem objeto heroi -> CORRECAO: "heroi": "kit/<objeto>" no topo do roteiro (modele se nao existir)
  - 2 palavra(s) de acao sem efeito + som -> CORRECAO: ver plano.md e por "fx"/"sfx" na cena

## RESUMO: 7 risco(s) em aberto
- b4: animal sem modelo: cachorros
- b4: acao sem animacao propria: dormiam, escalaram
- b4: objeto sem modelo 3D: cachorros
- b9: animal sem modelo: cachorros
- b9: objeto sem modelo 3D: cachorros
- geral: video sem objeto heroi
- geral: 2 palavra(s) de acao sem efeito + som

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh gansos390 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh gansos390` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
