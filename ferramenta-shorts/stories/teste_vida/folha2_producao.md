# FOLHA 2 - PRODUCAO: Teste de Vida

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/teste_vida/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py teste_vida` de novo ate esta folha sair sem risco.

## Cena b0 - Três amigos caminhavam pela estrada numa manhã tranquila.
- Cenario: countryside | luz: day | clima: limpo
- Camera: track = travelling lateral acompanhando quem anda
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (3): N (variante 0, expressao smile); M (variante 1, expressao neutral); C (variante 2, expressao grin)
- Animacao: encena
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): -
- RISCOS: nenhum

## Cena b1 - Mas naquela noite, chovia sem parar.
- Cenario: interior madeira | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 1 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto
- Personagens principais (2): N (variante 0, expressao nervous); M (variante 1, expressao shock)
- Animacao: reagir | interacao: susto
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): -
- RISCOS: nenhum

## Cena b2 - Dias depois, no inverno, a neve cobriu tudo.
- Cenario: arctic | luz: day | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (2): N (variante 0, expressao pained); M (variante 1, expressao nervous) | multidao: 8 de M
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): inverno, neve
- RISCOS: nenhum

## Cena b3 - Sob um sol escaldante, ele bebeu a caneca inteira.
- Cenario: interior madeira | luz: day | clima: calor
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (2): N (variante 0, expressao grin); M (variante 1, expressao laugh)
- Animacao: conversar | interacao: vai ate o outro
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): caneca
- RISCOS: nenhum

## Cena b4 - No fim de tarde, o jornal trouxe a notícia.
- Cenario: mountain | luz: day | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (2): B (variante 0, expressao stern); N (variante 0, expressao shock) | multidao: 6 de POV
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): jornal, noticia
- RISCOS: nenhum

## Cena b5 - E no dia seguinte, a tropa chegou marchando.
- Cenario: countryside | luz: day | clima: limpo
- Camera: track = travelling lateral acompanhando quem anda
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (4): S (variante 0, expressao stern); S (variante 1, expressao stern); S (variante 2, expressao stern); S (variante 3, expressao stern) | multidao: 10 de POV
- Animacao: encena
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): tropa
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
(nenhum objeto 3D neste video: confira se o roteiro nao esta pobre de elementos)

## Video inteiro
- Objeto heroi: - | grandes momentos: - | planos abertos: 2 | mistura: close 0% | medio 65% | aberto 35% | detalhe 0%
- Interacoes: b1 susto, b3 vai ate o outro
- RISCOS GERAIS: 
  - nenhum mapa no video (o canal situa o lugar com mapa rapido) -> CORRECAO: "mapa": "NOME DO LUGAR" na cena 1 ou 2
  - menos de 2 grandes momentos -> CORRECAO: "batalha": true (ou "impact": true) em duas cenas de acao
  - video sem objeto heroi -> CORRECAO: "heroi": "kit/<objeto>" no topo do roteiro (modele se nao existir)

## RESUMO: 3 risco(s) em aberto
- geral: nenhum mapa no video (o canal situa o lugar com mapa rapido)
- geral: menos de 2 grandes momentos
- geral: video sem objeto heroi

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh teste_vida bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh teste_vida` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
