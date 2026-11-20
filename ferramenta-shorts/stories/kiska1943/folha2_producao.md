# FOLHA 2 - PRODUCAO: A Invasão da Ilha Vazia

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/kiska1943/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py kiska1943` de novo ate esta folha sair sem risco.

## Cena b0 - Agosto de mil novecentos e quarenta e três. Os Aliados prepararam uma ...
- Cenario: arctic | luz: arctic | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto -> direita baixa
- Personagens principais (0): -
- Animacao: -
- Objetos/modelos: ship
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): alasca, aliados, grande, ilha, kiska
- RISCOS: 
  - a narracao cita agua e o cenario "arctic" nao tem agua -> CORRECAO: "set": "harbor" (cais com mar e navio) ou "set": "palace" (praia), ou "mapa" para so situar
  - personagens parados (so falam e piscam) -> CORRECAO: "acao": "conversar|discutir|comemorar", "interacao": "empurrar|cochichar|entregar|susto", objeto na mao (4o campo do "who") ou "chega": true

## Cena b1 - Foram mais de trinta e quatro mil soldados americanos e canadenses, co...
- Cenario: harbor | luz: arctic | clima: limpo
- Camera: reveal = ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (3): USA (variante 0, expressao stern); CAN (variante 0, expressao stern); USA (variante 1, expressao grin) | multidao: 8 de 
- Animacao: -
- Objetos/modelos: kit/marco_alpes, navios ao fundo
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): navios, trinta
- RISCOS: 
  - veiculo citado e nao aparece -> CORRECAO: "veiculo": {"asset": "vehicles/truck"} (ou wagon, locomotive, car, tank, airplane) ou "caminhoes": true na batalha

## Cena b2 - Antes do desembarque, bombardearam a ilha durante semanas.
- Cenario: arctic | luz: arctic | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (1): USA (variante 2, expressao grin) | multidao: 10 de USA
- Animacao: conversar | batalha encenada
- Objetos/modelos: cannon, kit/marco_alpes
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): desembarque, ilha
- RISCOS: 
  - a narracao cita agua e o cenario "arctic" nao tem agua -> CORRECAO: "set": "harbor" (cais com mar e navio) ou "set": "palace" (praia), ou "mapa" para so situar

## Cena b3 - No meio do nevoeiro, os soldados desceram em silêncio, prontos para um...
- Cenario: arctic | luz: overcast | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (3): USA (variante 0, expressao stern); CAN (variante 1, expressao stern); USA (variante 3, expressao nervous) | multidao: 18 de USA/CAN
- Animacao: - | batalha encenada
- Objetos/modelos: kit/marco_alpes
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): combate, nevoeiro, soldados
- RISCOS: nenhum

## Cena b4 - Mas teve um problema: os japoneses já tinham ido embora.
- Cenario: interior madeira | luz: overcast | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (1): USA (variante 1, expressao shock)
- Animacao: reagir
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): japoneses, problema
- RISCOS: nenhum

## Cena b5 - Duas semanas antes, uma frota tinha evacuado cerca de cinco mil homens...
- Cenario: mountain | luz: overcast | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): USA (variante 0, expressao neutral) | multidao: 10 de USA
- Animacao: -
- Objetos/modelos: ship, kit/marco_alpes, nature/picket_fence
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cinco, frota, neblina
- RISCOS: nenhum

## Cena b6 - Sem inimigo à vista, os Aliados começaram a atirar uns nos outros, no ...
- Cenario: arctic | luz: overcast | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (3): USA (variante 0, expressao shock); CAN (variante 0, expressao shock); USA (variante 2, expressao pained)
- Animacao: reagir | interacao: susto
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): aliados, atirar, escuro, neblina, vista
- RISCOS: nenhum

## Cena b7 - No fim, só acharam na ilha alguns cachorros abandonados.
- Cenario: arctic | luz: arctic | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (1): USA (variante 1, expressao laugh)
- Animacao: conversar
- Objetos/modelos: dog
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): ilha
- RISCOS: 
  - a narracao cita agua e o cenario "arctic" nao tem agua -> CORRECAO: "set": "harbor" (cais com mar e navio) ou "set": "palace" (praia), ou "mapa" para so situar

## Cena b8 - Uma das maiores invasões do Pacífico Norte tomou uma ilha completament...
- Cenario: arctic | luz: arctic | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (1): OFF (variante 0, expressao pained)
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): ilha, maiores, pacifico
- RISCOS: 
  - a narracao cita agua e o cenario "arctic" nao tem agua -> CORRECAO: "set": "harbor" (cais com mar e navio) ou "set": "palace" (praia), ou "mapa" para so situar

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
ship | b0, b5 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/marco_alpes | b1, b2, b3, b5 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
cannon | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/picket_fence | b5 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
dog | b7 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: - | grandes momentos: b2, b3 | planos abertos: 3 | mistura: close 20% | medio 53% | aberto 24% | detalhe 3%
- Interacoes: b6 susto
- RISCOS GERAIS: 
  - nenhum mapa no video (o canal situa o lugar com mapa rapido) -> CORRECAO: "mapa": "NOME DO LUGAR" na cena 1 ou 2
  - pouca variedade de cenario ({'arctic': 6, 'harbor': 1, 'interior madeira': 1, 'mountain': 1}): o video fica parecendo todos os outros -> CORRECAO: pelo menos 3 lugares e nenhum em mais da metade das cenas: troque "set"/"interior" de algumas cenas (lugares: outback, countryside, arctic, palace, harbor, mountain, medieval, jungle, hall, stadium, street | interior: madeira, pedra, loja)
  - video sem objeto heroi -> CORRECAO: "heroi": "kit/<objeto>" no topo do roteiro (modele se nao existir)

## RESUMO: 9 risco(s) em aberto
- b0: a narracao cita agua e o cenario "arctic" nao tem agua
- b0: personagens parados (so falam e piscam)
- b1: veiculo citado e nao aparece
- b2: a narracao cita agua e o cenario "arctic" nao tem agua
- b7: a narracao cita agua e o cenario "arctic" nao tem agua
- b8: a narracao cita agua e o cenario "arctic" nao tem agua
- geral: nenhum mapa no video (o canal situa o lugar com mapa rapido)
- geral: pouca variedade de cenario ({'arctic': 6, 'harbor': 1, 'interior madeira': 1, 'mountain': 1}): o video fica parecendo todos os outros
- geral: video sem objeto heroi

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh kiska1943 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh kiska1943` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
