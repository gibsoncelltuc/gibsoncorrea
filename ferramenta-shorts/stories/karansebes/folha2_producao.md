# FOLHA 2 - PRODUCAO: Guerras Inusitadas EP 01 - A Batalha de Karánsebes

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/karansebes/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py karansebes` de novo ate esta folha sair sem risco.

## Cena b0 - Um exército inteiro conseguiu perder uma batalha contra si mesmo.
- Cenario: countryside | luz: golden | clima: limpo
- Camera: track = travelling lateral acompanhando quem anda
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: direita baixa -> frente
- Personagens principais (4): AUT (variante 0, expressao neutral); AUT (variante 1, expressao stern); AUT (variante 2, expressao neutral); AUT (variante 3, expressao stern)
- Animacao: -
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): batalha, exercito
- RISCOS: 
  - a narracao fala de BATALHA/ATAQUE e a cena nao encena a luta -> CORRECAO: "batalha": true nesta cena (tropa dos dois lados no "crowd", tiros/golpes e gente fugindo); cada batalha citada no roteiro = uma cena com "batalha": true

## Cena b1 - Era o exército austríaco, marchando contra os turcos, com soldados de ...
- Cenario: countryside | luz: golden | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (4): AUT (variante 0, expressao smile); HUS (variante 0, expressao nervous); AUT (variante 1, expressao neutral); OFF (variante 0, expressao stern) | multidao: 10 de AUT/HUS/OFF/TUR
- Animacao: reagir
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): exercito, soldados, turcos, varios
- RISCOS: nenhum

## Cena b2 - Numa noite, os hussardos foram na frente procurar o inimigo.
- Cenario: street | luz: dusk | clima: limpo
- Camera: track = travelling lateral acompanhando quem anda
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: direita baixa -> frente
- Personagens principais (2): HUS (variante 0, expressao stern, segura lantern); HUS (variante 1, expressao neutral)
- Animacao: encena
- Objetos/modelos: tools/lantern
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): frente, hussardos, inimigo
- RISCOS: nenhum

## Cena b3 - Não acharam turco nenhum. Acharam moradores vendendo aguardente.
- Cenario: street | luz: dusk | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: direita baixa -> frente
- Personagens principais (2): HUS (variante 0, expressao shock); LOC (variante 0, expressao grin, segura bottle)
- Animacao: reagir | interacao: aproxima-se
- Objetos/modelos: barrel
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): -
- RISCOS: nenhum

## Cena b4 - Compraram tudo, beberam, e a festa começou.
- Cenario: mountain | luz: dusk | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 1 take(s) de ~1,8 s, deslizando de um para o outro: direita baixa
- Personagens principais (2): HUS (variante 0, expressao laugh, segura mug); HUS (variante 1, expressao grin, segura bottle)
- Animacao: comemorar | interacao: brindar
- Objetos/modelos: barrel, tools/lantern
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): festa
- RISCOS: nenhum

## Cena b5 - Aí chegou a infantaria, querendo a parte dela. "Não tem pra vocês", di...
- Cenario: mountain | luz: dusk | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 5 take(s) de ~1,8 s, deslizando de um para o outro: direita baixa -> frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (3): AUT (variante 0, expressao stern); HUS (variante 0, expressao laugh); AUT (variante 1, expressao shock) | multidao: 18 de AUT/HUS/TUR
- Animacao: conversar | interacao: empurrar | o ultimo personagem ENTRA andando
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): discussao, hussardos, infantaria, tiro
- RISCOS: nenhum

## Cena b6 - No escuro, alguém gritou: "Turcos! Turcos!" E o pânico tomou o acampam...
- Cenario: countryside | luz: dusk | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: direita baixa -> frente
- Personagens principais (1): HUS (variante 1, expressao shock) | multidao: 10 de HUS/TUR
- Animacao: conversar | batalha encenada
- Objetos/modelos: kit/campfire, kit/tent
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): acampamento, escuro, panico
- RISCOS: nenhum

## Cena b7 - Acontece que ninguém entendia a língua do vizinho. Todo mundo atirava ...
- Cenario: countryside | luz: dusk | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (3): AUT (variante 0, expressao shock); AUT (variante 1, expressao pained); HUS (variante 0, expressao shock) | multidao: 30 de 
- Animacao: reagir | batalha encenada
- Objetos/modelos: buildings/house_small, nature/picket_fence, nature/tree_oak
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): lingua, turcos, vizinho
- RISCOS: nenhum

## Cena b8 - Um oficial mandou usar a artilharia, e os canhões dispararam contra o ...
- Cenario: mountain | luz: dusk | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: direita baixa -> frente -> 3/4 pela direita, mais perto e mais baixo | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): OFF (variante 0, expressao shock); AUT (variante 0, expressao pained) | multidao: 5 de OFF/AUT/TUR
- Animacao: reagir | interacao: susto
- Objetos/modelos: cannon
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): artilharia, canhoes, oficial, proprio
- RISCOS: nenhum

## Cena b9 - Dois dias depois, os turcos chegaram de verdade, e acharam o acampamen...
- Cenario: mountain | luz: dawn | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 5 take(s) de ~1,8 s, deslizando de um para o outro: direita baixa -> frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto -> leve direita, perto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): TUR (variante 0, expressao shock, segura spyglass); TUR (variante 1, expressao neutral) | multidao: 5 de TUR
- Animacao: reagir | interacao: avanca e o outro recua | o ultimo personagem ENTRA andando
- Objetos/modelos: crate, barrel, kit/campfire, kit/tent
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): acampamento, historiadores, turcos
- RISCOS: nenhum

## Cena b10 - Os turcos venceram sem dar um único tiro.
- Cenario: countryside | luz: dawn | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: direita baixa -> frente
- Personagens principais (1): OFF (variante 0, expressao pained)
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): turcos
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
tools/lantern | b2, b4 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
barrel | b3, b4, b9 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/campfire | b6, b9 | pronto (HEROI: aparece em close) | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/tent | b6, b9 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
buildings/house_small | b7 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/picket_fence | b7 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/tree_oak | b7 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
cannon | b8 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
crate | b9 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: kit/campfire | grandes momentos: b6, b7 | planos abertos: 2 | mistura: close 8% | medio 71% | aberto 15% | detalhe 6%
- Interacoes: b3 aproxima-se, b4 brindar, b5 empurrar, b8 susto, b9 avanca e o outro recua
- RISCOS GERAIS: nenhum

## RESUMO: 1 risco(s) em aberto
- b0: a narracao fala de BATALHA/ATAQUE e a cena nao encena a luta

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh karansebes bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh karansebes` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
