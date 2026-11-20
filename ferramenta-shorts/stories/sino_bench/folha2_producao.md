# FOLHA 2 - PRODUCAO: O Sino (benchmark)

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/sino_bench/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py sino_bench` de novo ate esta folha sair sem risco.

## Cena b0 - Enterraram um homem vivo, com um sino amarrado no dedo.
- Cenario: countryside | luz: pordosol | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa
- Personagens principais (2): MOR (variante 0, expressao grin); COV (variante 0, expressao stern)
- Animacao: conversar | interacao: insiste
- Objetos/modelos: kit/grave, kit/cross, buildings/church
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): dedo, homem, sino
- RISCOS: 
  - ACAO SEM ANIMACAO na narracao: Enterraram -> CORRECAO: a cena precisa MOSTRAR a acao: reescreva com um verbo que a ferramenta encena (veja OPERACAO.md "MODO DE ACAO") ou marque a cena ("batalha", "interacao", "acao", "animals", "props")

## Cena b1 - Acontece que o povo tinha tanto medo de acordar dentro do caixão, que ...
- Cenario: countryside | luz: day | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua) [momento criado pela ferramenta]
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (2): COV (variante 0, expressao neutral, segura shovel); POV (variante 1, expressao nervous) | multidao: 12 de POV
- Animacao: reagir | batalha encenada
- Objetos/modelos: kit/grave, kit/cross
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): acordar, caixao, cordao, cova, morto, povo, sininho
- RISCOS: 
  - cena longa (29 palavras, ~10 s no mesmo lugar) -> CORRECAO: dividir em duas cenas com planos diferentes

## Cena b2 - Só que quando o sino dele começa a tocar, às duas da manhã, o vizinho ...
- Cenario: countryside | luz: noite | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa -> frente -> 3/4 pela direita, mais perto e mais baixo
- Personagens principais (2): VIZ (variante 0, expressao shock); POV (variante 0, expressao nervous)
- Animacao: reagir | interacao: susto
- Objetos/modelos: kit/porch, buildings/house_small, nature/picket_fence, nature/tree_oak
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): duas, sino, tocar, vento, vizinho
- RISCOS: nenhum

## Cena b3 - Aí ele toca mais rápido, e a rua inteira sai para a varanda. "Vai lá o...
- Cenario: street | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa -> frente -> 3/4 pela direita, mais perto e mais baixo
- Personagens principais (4): VIZ (variante 0, expressao shock); ESP (variante 1, expressao stern, segura lantern); POV (variante 2, expressao nervous); POV (variante 3, expressao shock)
- Animacao: conversar | interacao: vai ate o outro
- Objetos/modelos: kit/porch
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): varanda
- RISCOS: nenhum

## Cena b4 - Alguém arranca o médico da cama, e ele diz: "Corpo se mexe. Está morto...
- Cenario: countryside | luz: day | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (2): DOC (variante 0, expressao stern, segura paper); VIZ (variante 0, expressao nervous) | multidao: 6 de POV
- Animacao: conversar
- Objetos/modelos: kit/porch
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cama, medico, papel
- RISCOS: 
  - ACAO SEM ANIMACAO na narracao: assinei -> CORRECAO: a cena precisa MOSTRAR a acao: reescreva com um verbo que a ferramenta encena (veja OPERACAO.md "MODO DE ACAO") ou marque a cena ("batalha", "interacao", "acao", "animals", "props")

## Cena b5 - Mas a esposa não está na varanda. Está sentada no escuro, com a pá ao ...
- Cenario: interior madeira | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa -> frente -> 3/4 pela direita, mais perto e mais baixo
- Personagens principais (1): ESP (variante 0, expressao stern, segura shovel)
- Animacao: encena
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): escuro, esposa, porta, varanda
- RISCOS: nenhum

## Cena b6 - Três curtos, um longo. O sinal que os dois ensaiaram. Ele nunca esteve...
- Cenario: interior madeira | luz: dia | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (2): MOR (variante 0, expressao grin); ESP (variante 0, expressao smile) | multidao: 12 de POV
- Animacao: - | batalha encenada
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): dois, longo, sinal
- RISCOS: 
  - multidao/batalha dentro de sala: nao cabe -> CORRECAO: tirar "interior" desta cena (faz na rua/campo) ou reduzir o "crowd"

## Cena b7 - Devia dinheiro para meia cidade, então fingiu a própria morte. Quando ...
- Cenario: street | luz: dia | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa -> frente -> 3/4 pela direita, mais perto e mais baixo
- Personagens principais (4): MOR (variante 0, expressao nervous, segura coin); VIZ (variante 0, expressao stern); DOC (variante 0, expressao stern); POV (variante 2, expressao stern)
- Animacao: reagir | interacao: aproxima-se
- Objetos/modelos: kit/grave, buildings/church
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): marido, propria, sino
- RISCOS: nenhum

## Cena b8 - Em vez disso, ela fica ali a noite toda, ouvindo o sino tocar rápido, ...
- Cenario: interior madeira | luz: noite | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa -> frente -> 3/4 pela direita, mais perto e mais baixo
- Personagens principais (1): ESP (variante 0, expressao neutral)
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cada, sino
- RISCOS: nenhum

## Cena b9 - Até o sol nascer, quando ele finalmente para.
- Cenario: countryside | luz: amanhecer | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): COV (variante 0, expressao neutral, segura shovel) | multidao: 6 de POV
- Animacao: encena
- Objetos/modelos: kit/grave, kit/cross
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): -
- RISCOS: nenhum

## Cena b10 - Com ele debaixo da terra, as dívidas foram enterradas junto. E a casa ...
- Cenario: interior madeira | luz: dia | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: esquerda alta, aberto -> direita baixa -> frente
- Personagens principais (1): ESP (variante 0, expressao grin, segura coin)
- Animacao: encena
- Objetos/modelos: kit/grave
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): casa, dividas, terra
- RISCOS: 
  - ACAO SEM ANIMACAO na narracao: enterradas -> CORRECAO: a cena precisa MOSTRAR a acao: reescreva com um verbo que a ferramenta encena (veja OPERACAO.md "MODO DE ACAO") ou marque a cena ("batalha", "interacao", "acao", "animals", "props")

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
kit/grave | b0, b1, b7, b9, b10 | pronto (HEROI: aparece em close) | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/cross | b0, b1, b9 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
buildings/church | b0, b7 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/porch | b2, b3, b4 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
buildings/house_small | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/picket_fence | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/tree_oak | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: kit/grave | grandes momentos: b1, b6 | planos abertos: 4 | mistura: close 27% | medio 53% | aberto 20% | detalhe 0%
- Interacoes: b0 insiste, b2 susto, b3 vai ate o outro, b7 aproxima-se
- RISCOS GERAIS: 
  - nenhum mapa no video (o canal situa o lugar com mapa rapido) -> CORRECAO: "mapa": "NOME DO LUGAR" na cena 1 ou 2
  - objeto heroi (kit/grave) sem close de camera -> CORRECAO: por o objeto em "props" de uma cena media de 8+ palavras
  - 3 palavra(s) de acao sem efeito + som -> CORRECAO: ver plano.md e por "fx"/"sfx" na cena

## RESUMO: 8 risco(s) em aberto
- b0: ACAO SEM ANIMACAO na narracao: Enterraram
- b1: cena longa (29 palavras, ~10 s no mesmo lugar)
- b4: ACAO SEM ANIMACAO na narracao: assinei
- b6: multidao/batalha dentro de sala: nao cabe
- b10: ACAO SEM ANIMACAO na narracao: enterradas
- geral: nenhum mapa no video (o canal situa o lugar com mapa rapido)
- geral: objeto heroi (kit/grave) sem close de camera
- geral: 3 palavra(s) de acao sem efeito + som

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh sino_bench bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh sino_bench` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
