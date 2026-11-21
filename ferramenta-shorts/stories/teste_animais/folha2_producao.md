# FOLHA 2 - PRODUCAO: Teste de Animais

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/teste_animais/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py teste_animais` de novo ate esta folha sair sem risco.

## Cena b0 - Em mil oitocentos e cinquenta e nove, um fazendeiro viu um porco fuçan...
- Cenario: countryside | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto
- Personagens principais (1): FAZ (variante 0, expressao smile)
- Animacao: reagir
- Objetos/modelos: nature/flowerbed, nature/picket_fence, buildings/barn, nature/haybale, nature/scarecrow, pig
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): fazendeiro, horta, porco
- RISCOS: nenhum

## Cena b1 - Uma galinha ciscava no quintal enquanto um emu corria pelo campo.
- Cenario: countryside | luz: day | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): FAZ (variante 0, expressao smile)
- Animacao: reagir
- Objetos/modelos: chicken, emus
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): galinha, quintal
- RISCOS: nenhum

## Cena b2 - De repente um urso apareceu na cerca e o fazendeiro levou um susto.
- Cenario: countryside | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (1): FAZ (variante 0, expressao smile)
- Animacao: reagir
- Objetos/modelos: nature/picket_fence, buildings/barn, nature/haybale, nature/scarecrow, bear
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cerca, fazendeiro, repente, susto, urso
- RISCOS: nenhum

## Cena b3 - Ele atirou no porco, que caiu no chão.
- Cenario: countryside | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (1): FAZ (variante 0, expressao smile)
- Animacao: reagir
- Objetos/modelos: pig
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): chao, porco
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
nature/flowerbed | b0 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/picket_fence | b0, b2 | pronto (HEROI: aparece em close) | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
buildings/barn | b0, b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/haybale | b0, b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/scarecrow | b0, b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
pig | b0, b3 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
chicken | b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
emu | b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
bear | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: nature/picket_fence | grandes momentos: - | planos abertos: 1 | mistura: close 0% | medio 77% | aberto 23% | detalhe 0%
- Interacoes: -
- RISCOS GERAIS: 
  - nenhum mapa no video (o canal situa o lugar com mapa rapido) -> CORRECAO: "mapa": "NOME DO LUGAR" na cena 1 ou 2
  - menos de 2 grandes momentos -> CORRECAO: "batalha": true (ou "impact": true) em duas cenas de acao
  - objeto heroi (nature/picket_fence) sem close de camera -> CORRECAO: por o objeto em "props" de uma cena media de 8+ palavras

## RESUMO: 3 risco(s) em aberto
- geral: nenhum mapa no video (o canal situa o lugar com mapa rapido)
- geral: menos de 2 grandes momentos
- geral: objeto heroi (nature/picket_fence) sem close de camera

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh teste_animais bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh teste_animais` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
