# FOLHA 2 - PRODUCAO: Guerras Inusitadas EP 05 - Os Gansos que Salvaram Roma

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/gansos390/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py gansos390` de novo ate esta folha sair sem risco.

## Cena b0 - Um bando de gansos barulhentos salvou Roma numa noite.
- Cenario: medieval | luz: noite | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (1): ROM (variante 2, expressao shock)
- Animacao: reagir
- Objetos/modelos: goose
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): bando, gansos
- RISCOS: nenhum

## Cena b1 - Mas o ouro de Roma foi embora mesmo assim.
- Cenario: medieval | luz: dia | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (1): ROM (variante 0, expressao sad) | multidao: 0 de POV
- Animacao: encena
- Objetos/modelos: goose
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): ouro, roma
- RISCOS: nenhum

## Cena b2 - Em 390 antes de Cristo, os gauleses tomaram Roma.
- Cenario: loc_campo | luz: day | clima: limpo
- Camera: reveal = ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): GAU (variante 0, expressao angry, segura torch) | multidao: 8 de GAU
- Animacao: encena
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cristo, gauleses
- RISCOS: nenhum

## Cena b3 - Os romanos que sobraram se trancaram no Capitólio, uma colina.
- Cenario: loc_montanha | luz: day | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): ROM (variante 0, expressao nervous) | multidao: 0 de POV
- Animacao: reagir | grande momento (efeito + som, sem tiro)
- Objetos/modelos: buildings/castle_tower
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): capitolio, colina, romanos
- RISCOS: nenhum

## Cena b4 - Numa noite sem lua, os gauleses chegaram em silêncio à muralha.
- Cenario: loc_campo | luz: noite | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): GAU (variante 0, expressao stern) | multidao: 0 de POV
- Animacao: -
- Objetos/modelos: buildings/castle_tower
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): gauleses, muralha
- RISCOS: nenhum

## Cena b5 - Acontece que os gansos sagrados de Juno ouviram e gritaram.
- Cenario: loc_campo | luz: noite | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): ROM (variante 2, expressao shock)
- Animacao: reagir
- Objetos/modelos: goose
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): gansos, juno
- RISCOS: nenhum

## Cena b6 - O barulho acordou o soldado Marco Mânlio, que barrou a subida.
- Cenario: loc_campo | luz: noite | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (2): MAN (variante 0, expressao angry); GAU (variante 0, expressao scared) | multidao: 0 de POV
- Animacao: conversar | interacao: cochichar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): barulho, soldado, subida
- RISCOS: nenhum

## Cena b7 - Depois de sete meses de fome, Roma pagou mil libras de ouro.
- Cenario: interior madeira | luz: dia | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (2): ROM (variante 0, expressao sad, segura coin); GAU (variante 0, expressao grin, segura coin)
- Animacao: encena | interacao: entregar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): fome, ouro, sete
- RISCOS: nenhum

## Cena b8 - Os guardas não ouviram, os gansos sim. E foi assim que...
- Cenario: medieval | luz: noite | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (1): ROM (variante 2, expressao shock)
- Animacao: reagir
- Objetos/modelos: goose
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): gansos, guardas
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
goose | b0, b1, b5, b8 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
buildings/castle_tower | b3, b4 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: - | grandes momentos: b3 | planos abertos: 4 | mistura: close 2% | medio 65% | aberto 32% | detalhe 0%
- Interacoes: b6 cochichar, b7 entregar
- RISCOS GERAIS: nenhum

## RESUMO: 0 risco(s) em aberto - pode renderizar

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh gansos390 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh gansos390` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
