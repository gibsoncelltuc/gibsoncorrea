# FOLHA 2 - PRODUCAO: Guerras Inusitadas EP 01 - A Batalha de Karánsebes

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/karansebes/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py karansebes` de novo ate esta folha sair sem risco.

## Cena b0 - Um exército inteiro conseguiu perder uma batalha contra si mesmo.
- Cenario: countryside | luz: golden | clima: limpo
- Camera: track = travelling lateral acompanhando quem anda
- Personagens principais (4): AUT (variante 0, expressao neutral); AUT (variante 1, expressao stern); AUT (variante 2, expressao neutral); AUT (variante 3, expressao stern) | multidao: 5 de AUT
- Animacao: -
- Objetos/modelos: -
- RISCOS: nenhum

## Cena b1 - Era o exército austríaco, marchando contra os turcos, com soldados de ...
- Cenario: countryside | luz: golden | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua)
- Personagens principais (4): AUT (variante 0, expressao smile); HUS (variante 0, expressao nervous); AUT (variante 1, expressao neutral); OFF (variante 0, expressao stern) | multidao: 10 de AUT/HUS/OFF
- Animacao: reagir
- Objetos/modelos: -
- RISCOS: nenhum

## Cena b2 - Numa noite, os hussardos foram na frente procurar o inimigo.
- Cenario: countryside | luz: dusk | clima: limpo
- Camera: track = travelling lateral acompanhando quem anda
- Personagens principais (2): HUS (variante 0, expressao stern, segura lantern); HUS (variante 1, expressao neutral)
- Animacao: -
- Objetos/modelos: tools/lantern
- RISCOS: nenhum

## Cena b3 - Não acharam turco nenhum. Acharam moradores vendendo aguardente.
- Cenario: countryside | luz: dusk | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Personagens principais (2): HUS (variante 0, expressao shock); LOC (variante 0, expressao grin, segura bottle)
- Animacao: reagir | interacao: aproxima-se
- Objetos/modelos: barrel
- RISCOS: nenhum

## Cena b4 - Compraram tudo, beberam, e a festa começou.
- Cenario: countryside | luz: dusk | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Personagens principais (2): HUS (variante 0, expressao laugh, segura mug); HUS (variante 1, expressao grin, segura bottle)
- Animacao: comemorar | interacao: pular
- Objetos/modelos: barrel, tools/lantern
- RISCOS: nenhum

## Cena b5 - Aí chegou a infantaria, querendo a parte dela. "Não tem pra vocês", di...
- Cenario: countryside | luz: dusk | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Personagens principais (3): AUT (variante 0, expressao stern); HUS (variante 0, expressao laugh); AUT (variante 1, expressao shock) | multidao: 18 de AUT/HUS
- Animacao: conversar | interacao: empurrar | o ultimo personagem ENTRA andando
- Objetos/modelos: -
- RISCOS: nenhum

## Cena b6 - No escuro, alguém gritou: "Turcos! Turcos!" E o pânico tomou o acampam...
- Cenario: countryside | luz: dusk | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Personagens principais (1): HUS (variante 1, expressao shock) | multidao: 10 de HUS
- Animacao: conversar | batalha encenada
- Objetos/modelos: kit/campfire, kit/tent
- RISCOS: nenhum

## Cena b7 - Acontece que ninguém entendia a língua do vizinho. Todo mundo atirava ...
- Cenario: countryside | luz: dusk | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Personagens principais (3): AUT (variante 0, expressao shock); AUT (variante 1, expressao pained); HUS (variante 0, expressao shock) | multidao: 8 de 
- Animacao: reagir | batalha encenada
- Objetos/modelos: -
- RISCOS: nenhum

## Cena b8 - Um oficial mandou usar a artilharia, e os canhões dispararam contra o ...
- Cenario: countryside | luz: dusk | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Personagens principais (2): OFF (variante 0, expressao shock); AUT (variante 0, expressao pained) | multidao: 5 de OFF/AUT
- Animacao: reagir | interacao: susto
- Objetos/modelos: cannon
- RISCOS: nenhum

## Cena b9 - Dois dias depois, os turcos chegaram de verdade, e acharam o acampamen...
- Cenario: countryside | luz: dawn | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Personagens principais (2): TUR (variante 0, expressao shock, segura spyglass); TUR (variante 1, expressao neutral) | multidao: 5 de TUR
- Animacao: reagir | interacao: avanca e o outro recua | o ultimo personagem ENTRA andando
- Objetos/modelos: crate, barrel, kit/campfire, kit/tent
- RISCOS: nenhum

## Cena b10 - Os turcos venceram sem dar um único tiro.
- Cenario: countryside | luz: dawn | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Personagens principais (1): OFF (variante 0, expressao pained)
- Animacao: conversar
- Objetos/modelos: -
- RISCOS: nenhum

## Video inteiro
- Objeto heroi: kit/campfire | grandes momentos: b6, b7 | planos abertos: 2 | mistura: close 8% | medio 71% | aberto 15% | detalhe 6%
- Interacoes: b3 aproxima-se, b4 pular, b5 empurrar, b8 susto, b9 avanca e o outro recua
- RISCOS GERAIS: 
  - nenhum mapa no video (o canal situa o lugar com mapa rapido) -> CORRECAO: "mapa": "NOME DO LUGAR" na cena 1 ou 2

## RESUMO: 1 risco(s) em aberto
- geral: nenhum mapa no video (o canal situa o lugar com mapa rapido)

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh karansebes bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh karansebes` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
