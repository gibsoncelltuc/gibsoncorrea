# FOLHA 2 - PRODUCAO: Teste de Veiculos

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/teste_veiculos/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py teste_veiculos` de novo ate esta folha sair sem risco.

## Cena b0 - Um homem dirigia seu carro vermelho pela avenida.
- Cenario: street | luz: golden | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo
- Personagens principais (0): -
- Animacao: -
- Objetos/modelos: vehicles/car
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): homem
- RISCOS: 
  - personagens parados (so falam e piscam) -> CORRECAO: "acao": "conversar|discutir|comemorar", "interacao": "empurrar|cochichar|entregar|susto", objeto na mao (4o campo do "who") ou "chega": true

## Cena b1 - Do outro lado vinha um táxi amarelo, com pressa.
- Cenario: street | luz: golden | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo
- Personagens principais (0): -
- Animacao: -
- Objetos/modelos: vehicles/taxi
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): pressa, taxi
- RISCOS: 
  - personagens parados (so falam e piscam) -> CORRECAO: "acao": "conversar|discutir|comemorar", "interacao": "empurrar|cochichar|entregar|susto", objeto na mao (4o campo do "who") ou "chega": true

## Cena b2 - No quartel, o jipe e o caminhão esperavam os soldados.
- Cenario: street | luz: golden | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo
- Personagens principais (0): -
- Animacao: -
- Objetos/modelos: vehicles/truck, vehicles/jeep
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): caminhao, jipe, quartel, soldados
- RISCOS: 
  - 3a cena seguida com o mesmo plano, lugar e personagens: fica repetitivo -> CORRECAO: trocar o "shot", levar para "interior" ou trocar quem aparece
  - personagens parados (so falam e piscam) -> CORRECAO: "acao": "conversar|discutir|comemorar", "interacao": "empurrar|cochichar|entregar|susto", objeto na mao (4o campo do "who") ou "chega": true

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
vehicles/car | b0 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
vehicles/taxi | b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
vehicles/truck | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
vehicles/jeep | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: - | grandes momentos: - | planos abertos: 0 | mistura: close 0% | medio 100% | aberto 0% | detalhe 0%
- Interacoes: -
- RISCOS GERAIS: 
  - nenhum mapa no video (o canal situa o lugar com mapa rapido) -> CORRECAO: "mapa": "NOME DO LUGAR" na cena 1 ou 2
  - menos de 2 grandes momentos -> CORRECAO: "batalha": true (ou "impact": true) em duas cenas de acao
  - video sem objeto heroi -> CORRECAO: "heroi": "kit/<objeto>" no topo do roteiro (modele se nao existir)

## RESUMO: 7 risco(s) em aberto
- b0: personagens parados (so falam e piscam)
- b1: personagens parados (so falam e piscam)
- b2: 3a cena seguida com o mesmo plano, lugar e personagens: fica repetitivo
- b2: personagens parados (so falam e piscam)
- geral: nenhum mapa no video (o canal situa o lugar com mapa rapido)
- geral: menos de 2 grandes momentos
- geral: video sem objeto heroi

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh teste_veiculos bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh teste_veiculos` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
