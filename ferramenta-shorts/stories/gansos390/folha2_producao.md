# FOLHA 2 - PRODUCAO: Guerras Inusitadas EP 05 - Os Gansos que Salvaram Roma

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/gansos390/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py gansos390` de novo ate esta folha sair sem risco.

## Cena b0 - Um bando de gansos barulhentos salvou Roma numa só noite.
- Cenario: medieval | luz: dia | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (1): ROM (variante 0, expressao nervous)
- Animacao: reagir
- Objetos/modelos: goose
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): bando, gansos
- RISCOS: nenhum

## Cena b1 - Em trezentos e noventa antes de Cristo, os gauleses de Breno tomaram R...
- Cenario: loc_campo | luz: day | clima: limpo
- Camera: reveal = ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): GAU (variante 0, expressao angry, segura torch) | multidao: 8 de GAU
- Animacao: encena
- Objetos/modelos: kit/fire
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): breno, cristo, gauleses
- RISCOS: nenhum

## Cena b2 - Os romanos que sobraram se trancaram no Capitólio, uma colina fortific...
- Cenario: mountain | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (3): ROM (variante 0, expressao nervous); ROM (variante 1, expressao pained); MAN (variante 0, expressao stern)
- Animacao: reagir | interacao: susto
- Objetos/modelos: buildings/castle_tower
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): capitolio, colina, romanos
- RISCOS: nenhum

## Cena b3 - Os gauleses cercaram a colina, e a fome apertou os dois lados.
- Cenario: mountain | luz: day | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua) [momento criado pela ferramenta]
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (2): ROM (variante 1, expressao pained); GAU (variante 0, expressao stern) | multidao: 6 de POV
- Animacao: encena | batalha encenada
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): colina, dois, fome, gauleses
- RISCOS: nenhum

## Cena b4 - Numa noite sem lua, eles tentaram escalar em silêncio, e os guardas nã...
- Cenario: loc_campo | luz: noite | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): GAU (variante 0, expressao stern) | multidao: 6 de GAU
- Animacao: -
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): guardas
- RISCOS: nenhum

## Cena b5 - Acontece que os gansos sagrados da deusa Juno ouviram, e começaram a g...
- Cenario: loc_campo | luz: noite | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): ROM (variante 2, expressao shock)
- Animacao: reagir
- Objetos/modelos: goose
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): asas, bater, deusa, gansos, gritar
- RISCOS: nenhum

## Cena b6 - O barulho acordou o soldado Marco Mânlio, que correu até a muralha e i...
- Cenario: loc_campo | luz: noite | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto -> direita baixa
- Personagens principais (2): MAN (variante 0, expressao angry); GAU (variante 0, expressao scared)
- Animacao: tomba | interacao: cochichar
- Objetos/modelos: buildings/castle_tower
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): barulho, gauleses, muralha, soldado, subida
- RISCOS: 
  - a narracao fala de FUGA/CORRERIA e ninguem corre -> CORRECAO: "shot": "track" (os personagens atravessam a tela andando/correndo) ou "batalha": true (a tropa foge no plano aberto)

## Cena b7 - A subida fracassou, mas os gauleses mantiveram o cerco.
- Cenario: loc_campo | luz: noite | clima: limpo
- Camera: reveal = ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): ROM (variante 0, expressao angry) | multidao: 10 de ROM
- Animacao: encena
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cerco, gauleses, subida
- RISCOS: nenhum

## Cena b8 - No fim, depois de sete meses com fome, Roma pagou mil libras de ouro, ...
- Cenario: interior madeira | luz: dia | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto -> direita baixa -> frente
- Personagens principais (2): ROM (variante 0, expressao sad, segura coin); GAU (variante 0, expressao grin, segura coin)
- Animacao: encena | interacao: entregar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): fome, gauleses, ouro, sete
- RISCOS: nenhum

## Cena b9 - Os gansos salvaram a colina, mas o ouro foi embora do mesmo jeito.
- Cenario: medieval | luz: dia | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): ROM (variante 0, expressao smile)
- Animacao: encena
- Objetos/modelos: goose
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): colina, gansos, ouro
- RISCOS: nenhum

## Cena b10 - Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?
- Cenario: medieval | luz: dia | clima: limpo
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
buildings/castle_tower | b2, b6 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: - | grandes momentos: b3 | planos abertos: 6 | mistura: close 10% | medio 46% | aberto 42% | detalhe 2%
- Interacoes: b2 susto, b6 cochichar, b8 entregar
- RISCOS GERAIS: nenhum

## RESUMO: 1 risco(s) em aberto
- b6: a narracao fala de FUGA/CORRERIA e ninguem corre

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh gansos390 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh gansos390` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
