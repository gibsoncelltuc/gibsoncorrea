# FOLHA 2 - PRODUCAO: O Cardápio do Zoológico

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/paris1870/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py paris1870` de novo ate esta folha sair sem risco.

## Cena b0 - Em mil oitocentos e setenta, a Prússia cercou Paris. Ninguém entrava, ...
- Cenario: street | luz: pordosol | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): PAR (variante 0, expressao nervous); PAR (variante 1, expressao pained)
- Animacao: reagir | interacao: susto
- Objetos/modelos: kit/marco_notredame
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): comida, prussia
- RISCOS: nenhum

## Cena b1 - Primeiro, os parisienses comeram os cavalos. Depois, os cachorros e os...
- Cenario: interior loja | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto
- Personagens principais (3): PAR (variante 0, expressao pained, segura ); PAR (variante 1, expressao nervous); PAR (variante 2, expressao pained)
- Animacao: comer | interacao: susto
- Objetos/modelos: mk/Table_Large, horse, dog, cat
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cachorros, cavalos, gatos, parisienses
- RISCOS: nenhum

## Cena b2 - Depois, os roedores, que viraram um prato chique.
- Cenario: interior loja | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto
- Personagens principais (3): CHF (variante 0, expressao grin); PAR (variante 0, expressao shock); PAR (variante 1, expressao pained)
- Animacao: comer | interacao: avanca e o outro recua
- Objetos/modelos: mk/Table_Large, mk/Table_Plate, kit/rato
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): prato, roedores
- RISCOS: nenhum

## Cena b3 - Quando acabou tudo, olharam para o zoológico da cidade.
- Cenario: street | luz: day | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua) [momento criado pela ferramenta]
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (2): PAR (variante 1, expressao nervous); PAR (variante 3, expressao nervous) | multidao: 6 de PAR
- Animacao: reagir | batalha encenada
- Objetos/modelos: kit/marco_notredame, buildings/house_two, nature/lamppost, elephant, deer
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cidade, zoologico
- RISCOS: nenhum

## Cena b4 - O açougueiro comprou dois elefantes, Castor e Pólux, e vendeu a carne ...
- Cenario: arctic | luz: day | clima: neve
- Camera: close = close no rosto; empurra devagar + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (1): BUT (variante 0, expressao grin)
- Animacao: conversar
- Objetos/modelos: elephant
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): acougueiro, carne
- RISCOS: nenhum

## Cena b5 - No Natal, o restaurante Voisin serviu consomê de elefante, ensopado de...
- Cenario: interior loja | luz: day | clima: neve
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (2): CHF (variante 0, expressao grin); PAR (variante 2, expressao shock)
- Animacao: conversar | interacao: tremem de frio
- Objetos/modelos: elephant, wolf
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): canguru, elefante, lobo, natal, restaurante
- RISCOS: nenhum

## Cena b6 - Tinha até gato servido com roedores em volta.
- Cenario: arctic | luz: day | clima: neve
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (1): PAR (variante 3, expressao shock) | multidao: 12 de PAR
- Animacao: reagir | batalha encenada
- Objetos/modelos: cat
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): roedores
- RISCOS: nenhum

## Cena b7 - Para mandar notícias, os parisienses usavam balões e pombos-correio.
- Cenario: arctic | luz: day | clima: neve
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (2): PAR (variante 0, expressao smile); PAR (variante 1, expressao smile) | multidao: 6 de PAR
- Animacao: encena
- Objetos/modelos: kit/balloon_air, kit/balloon
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): parisienses
- RISCOS: nenhum

## Cena b8 - O cerco acabou em janeiro de mil oitocentos e setenta e um, e Paris se...
- Cenario: arctic | luz: dusk | clima: neve
- Camera: close = close no rosto; empurra devagar
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto
- Personagens principais (1): PAR (variante 2, expressao pained)
- Animacao: encena
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): barriga, cerco
- RISCOS: nenhum

## Cena b9 - Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?
- Cenario: street | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto
- Personagens principais (1): PAR (variante 0, expressao grin)
- Animacao: conversar
- Objetos/modelos: kit/marco_notredame
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): comentar, proximo, tema
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
kit/marco_notredame | b0, b1, b2, b3, b9 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
dog | b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
cat | b1, b6 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
barrel | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
buildings/house_two | b3 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/lamppost | b3 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
elephant | b3, b4, b5 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
deer | b3 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
wolf | b5 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/balloon_air | b7 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/balloon | b7 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: kit/panela | grandes momentos: b3, b6 | planos abertos: 4 | mistura: close 37% | medio 40% | aberto 18% | detalhe 6%
- Interacoes: b0 susto, b2 avanca e o outro recua, b5 tremem de frio
- RISCOS GERAIS: nenhum

## RESUMO: 0 risco(s) em aberto - pode renderizar

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh paris1870 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh paris1870` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
