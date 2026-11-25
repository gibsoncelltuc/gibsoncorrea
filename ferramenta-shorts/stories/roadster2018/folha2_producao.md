# FOLHA 2 - PRODUCAO: Poder e Fama EP 08 - O Carro que Foi Parar no Espaço

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/roadster2018/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py roadster2018` de novo ate esta folha sair sem risco.

## Cena b0 - Um carro de verdade está dando voltas em torno do Sol.
- Cenario: arctic | luz: espaco | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): MUS (variante 0, expressao grin) | multidao: 0 de POV
- Animacao: -
- Objetos/modelos: kit/roadster
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): carro
- RISCOS: nenhum

## Cena b1 - E o motorista dele não respira.
- Cenario: interior loja | luz: day | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): STA (variante 0, expressao smile) | multidao: 0 de POV
- Animacao: -
- Objetos/modelos: kit/roadster
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): motorista
- RISCOS: nenhum

## Cena b2 - Em 2018, a SpaceX testou o Falcon Heavy, seu maior foguete.
- Cenario: loc_pista | luz: day | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): MUS (variante 0, expressao smile) | multidao: 0 de POV
- Animacao: -
- Objetos/modelos: kit/rocket
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): falcon, spacex
- RISCOS: nenhum

## Cena b3 - Em vez de um peso de concreto, Musk mandou o próprio carro.
- Cenario: loc_pista | luz: day | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): ENG (variante 0, expressao suspicious) | multidao: 0 de POV
- Animacao: conversar
- Objetos/modelos: kit/roadster
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): concreto, peso, proprio
- RISCOS: nenhum

## Cena b4 - O foguete decolou com um estrondo!
- Cenario: loc_pista | luz: day | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): ENG (variante 0, expressao shock) | multidao: 0 de POV
- Animacao: reagir | grande momento (efeito + som, sem tiro)
- Objetos/modelos: kit/falcon_air
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): estrondo, foguete
- RISCOS: nenhum

## Cena b5 - Acontece que no volante ia um boneco astronauta, o Starman.
- Cenario: interior loja | luz: day | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): STA (variante 0, expressao smile) | multidao: 0 de POV
- Animacao: -
- Objetos/modelos: kit/roadster
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): boneco, starman, volante
- RISCOS: nenhum

## Cena b6 - No painel, um aviso: não entre em pânico.
- Cenario: arctic | luz: espaco | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): STA (variante 0, expressao neutral) | multidao: 0 de POV
- Animacao: -
- Objetos/modelos: kit/roadster
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): aviso, painel
- RISCOS: nenhum

## Cena b7 - O carro deixou a Terra e foi girar em torno do Sol.
- Cenario: arctic | luz: espaco | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (0): - | multidao: 0 de POV
- Animacao: -
- Objetos/modelos: kit/roadster, kit/globe
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): carro, terra
- RISCOS: nenhum

## Cena b8 - Ele continua lá até hoje. Porque...
- Cenario: arctic | luz: espaco | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): MUS (variante 0, expressao grin) | multidao: 0 de POV
- Animacao: -
- Objetos/modelos: kit/roadster
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): -
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
kit/roadster | b0, b1, b3, b5, b6, b7, b8 | pronto (HEROI: aparece em close) | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/rocket | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/falcon_air | b4 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/globe | b7 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: kit/roadster | grandes momentos: b4 | planos abertos: 8 | mistura: close 1% | medio 18% | aberto 81% | detalhe 0%
- Interacoes: -
- RISCOS GERAIS: nenhum

## RESUMO: 0 risco(s) em aberto - pode renderizar

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh roadster2018 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh roadster2018` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
