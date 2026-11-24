# FOLHA 2 - PRODUCAO: A Invasão da Ilha Vazia

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/kiska1943/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py kiska1943` de novo ate esta folha sair sem risco.

## Cena b0 - Trinta e quatro mil soldados invadiram uma ilha onde não havia inimigo...
- Cenario: harbor | luz: overcast | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (0): -
- Animacao: conversar
- Objetos/modelos: ship
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): ilha
- RISCOS: nenhum

## Cena b1 - Era agosto de mil novecentos e quarenta e três. A ilha de Kiska, no Al...
- Cenario: arctic | luz: overcast | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto -> direita baixa | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (3): USA (variante 0, expressao stern); CAN (variante 0, expressao stern); USA (variante 1, expressao grin) | multidao: 8 de 
- Animacao: conversar | interacao: aproxima-se
- Objetos/modelos: vehicles/airplane, kit/navio_vapor
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): alasca, ilha, kiska
- RISCOS: nenhum

## Cena b2 - Americanos e canadenses chegaram com navios, aviões e tanques.
- Cenario: harbor | luz: overcast | clima: limpo
- Camera: reveal = ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (0): -
- Animacao: -
- Objetos/modelos: kit/aviao_ww2, kit/tanque_ww2, navios de guerra ao fundo, no tamanho real, navio em movimento
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): navios
- RISCOS: 
  - veiculo citado e nao aparece -> CORRECAO: "veiculo": {"asset": "vehicles/truck"} (ou wagon, locomotive, car, tank, airplane) ou "caminhoes": true na batalha

## Cena b3 - Antes do desembarque, bombardearam Kiska durante semanas.
- Cenario: arctic | luz: overcast | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (1): USA (variante 2, expressao grin) | multidao: 48 de USA
- Animacao: encena | batalha encenada
- Objetos/modelos: kit/canhao_moderno
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): desembarque
- RISCOS: nenhum

## Cena b4 - No meio do nevoeiro, os soldados desceram em silêncio, prontos para um...
- Cenario: mountain | luz: overcast | clima: neblina
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (3): USA (variante 0, expressao stern); CAN (variante 1, expressao stern); USA (variante 3, expressao nervous) | multidao: 48 de USA/CAN
- Animacao: encena | batalha encenada
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): combate, nevoeiro, soldados
- RISCOS: nenhum

## Cena b5 - Mas teve um problema: os japoneses já tinham ido embora.
- Cenario: interior pedra | luz: overcast | clima: neblina
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (2): USA (variante 1, expressao shock); CAN (variante 0, expressao shock)
- Animacao: reagir | interacao: susto
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): japoneses, problema
- RISCOS: nenhum

## Cena b6 - Mesmo assim, eles procuraram o inimigo por dias, em túneis e trincheir...
- Cenario: mountain | luz: dia | clima: limpo
- Camera: track = travelling lateral acompanhando quem anda
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (0): -
- Animacao: -
- Objetos/modelos: war/sandbags
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): inimigo
- RISCOS: nenhum

## Cena b7 - Semanas antes, navios japoneses tinham levado cerca de cinco mil homen...
- Cenario: harbor | luz: overcast | clima: neblina
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (0): -
- Animacao: -
- Objetos/modelos: ship, nature/picket_fence, navios de guerra ao fundo, no tamanho real
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cinco, neblina
- RISCOS: nenhum

## Cena b8 - Sem inimigo à vista, os Aliados começaram a atirar uns nos outros, no ...
- Cenario: mountain | luz: overcast | clima: neblina
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto
- Personagens principais (3): USA (variante 0, expressao shock); CAN (variante 0, expressao shock); USA (variante 2, expressao pained)
- Animacao: reagir | interacao: avanca e o outro recua
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): aliados, atirar, escuro, neblina, vista
- RISCOS: nenhum

## Cena b9 - Mais de vinte soldados morreram nesses tiros, e um navio americano ain...
- Cenario: arctic | luz: noite | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto
- Personagens principais (2): USA (variante 0, expressao sad); CAN (variante 0, expressao sad) | multidao: 5 de USA/CAN
- Animacao: conversar | interacao: empurrar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): navio, vinte
- RISCOS: nenhum

## Cena b10 - No fim, só acharam na ilha alguns cachorros abandonados.
- Cenario: harbor | luz: arctic | clima: neblina
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (1): USA (variante 1, expressao laugh)
- Animacao: conversar
- Objetos/modelos: kit/dog_sit, dog
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): ilha
- RISCOS: nenhum

## Cena b11 - Uma das maiores invasões do Pacífico Norte tomou uma ilha completament...
- Cenario: harbor | luz: overcast | clima: neblina
- Camera: close = close no rosto; empurra devagar
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (1): OFF (variante 0, expressao pained)
- Animacao: conversar
- Objetos/modelos: kit/dog_sit
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): ilha, maiores, pacifico
- RISCOS: nenhum

## Cena b12 - Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?
- Cenario: harbor | luz: overcast | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (1): USA (variante 0, expressao grin)
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): comentar, proximo, tema
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
ship | b0, b7 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
vehicles/airplane | b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/navio_vapor | b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/aviao_ww2 | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/tanque_ww2 | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/canhao_moderno | b3 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
war/sandbags | b6 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/picket_fence | b7 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/dog_sit | b10, b11 | pronto (HEROI: aparece em close) | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
dog | b10 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: kit/dog_sit | grandes momentos: b3, b4 | planos abertos: 4 | mistura: close 9% | medio 66% | aberto 19% | detalhe 6%
- Interacoes: b1 aproxima-se, b5 susto, b8 avanca e o outro recua, b9 empurrar
- RISCOS GERAIS: 
  - 1 palavra(s) de acao sem efeito + som -> CORRECAO: ver plano.md e por "fx"/"sfx" na cena

## RESUMO: 2 risco(s) em aberto
- b2: veiculo citado e nao aparece
- geral: 1 palavra(s) de acao sem efeito + som

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh kiska1943 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh kiska1943` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
