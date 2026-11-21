# FOLHA 2 - PRODUCAO: Teste de Personagens

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/teste_personagens/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py teste_personagens` de novo ate esta folha sair sem risco.

## Cena b0 - Capacete, chapéu coco, chapéu de palha e chapéu australiano.
- Cenario: outback | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (4): A (variante 0, expressao neutral); B (variante 1, expressao smile, segura paper); C (variante 2, expressao grin, segura pitchfork); D (variante 3, expressao stern)
- Animacao: conversar | interacao: insiste
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): palha
- RISCOS: nenhum

## Cena b1 - Fez, turbante, coroa e boina, cada um com um objeto.
- Cenario: countryside | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (4): E (variante 0, expressao neutral, segura mug); F (variante 1, expressao smile, segura spyglass); G (variante 2, expressao grin, segura coin); H (variante 3, expressao stern, segura book)
- Animacao: conversar | interacao: vai ate o outro
- Objetos/modelos: kit/crown
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): objeto
- RISCOS: nenhum

## Cena b2 - Mago, e três cortes de cabelo diferentes, sem chapéu.
- Cenario: countryside | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (4): I (variante 0, expressao neutral, segura staff); N (variante 0, expressao smile, segura lantern); N (variante 2, expressao grin, segura bottle); N (variante 4, expressao stern, segura bag)
- Animacao: conversar | interacao: aproxima-se
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cabelo
- RISCOS: nenhum

## Cena b3 - E uma turma misturada, com tocha e bandeira.
- Cenario: countryside | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (6): M (variante 0, expressao neutral, segura flag); M (variante 1, expressao smile, segura torch); M (variante 2, expressao grin); M (variante 3, expressao stern); N (variante 1, expressao shock); N (variante 3, expressao laugh)
- Animacao: conversar | interacao: avanca e o outro recua
- Objetos/modelos: war/flagpole
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): tocha, turma
- RISCOS: 
  - 6 personagens em plano fechado: alguem sai cortado -> CORRECAO: no maximo 3 no "who" (o resto vai em "crowd") ou "shot": "group"

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
kit/crown | b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
war/flagpole | b3 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: - | grandes momentos: - | planos abertos: 0 | mistura: close 0% | medio 100% | aberto 0% | detalhe 0%
- Interacoes: b0 insiste, b1 vai ate o outro, b2 aproxima-se, b3 avanca e o outro recua
- RISCOS GERAIS: 
  - nenhum mapa no video (o canal situa o lugar com mapa rapido) -> CORRECAO: "mapa": "NOME DO LUGAR" na cena 1 ou 2
  - menos de 2 grandes momentos -> CORRECAO: "batalha": true (ou "impact": true) em duas cenas de acao
  - video sem objeto heroi -> CORRECAO: "heroi": "kit/<objeto>" no topo do roteiro (modele se nao existir)

## RESUMO: 4 risco(s) em aberto
- b3: 6 personagens em plano fechado: alguem sai cortado
- geral: nenhum mapa no video (o canal situa o lugar com mapa rapido)
- geral: menos de 2 grandes momentos
- geral: video sem objeto heroi

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh teste_personagens bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh teste_personagens` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
