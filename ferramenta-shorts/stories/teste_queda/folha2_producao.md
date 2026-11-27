# FOLHA 2 - PRODUCAO: Teste EP 14 - Teste queda 1900

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/teste_queda/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py teste_queda` de novo ate esta folha sair sem risco.

## Cena b0 - No campo, João empurrou Pedro com força e Pedro caiu no chão.
- Cenario: countryside | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (2): JOA (variante 0, expressao angry); PED (variante 0, expressao surprised)
- Animacao: conversar | interacao: empurrar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): campo, chao, forca
- RISCOS: nenhum

## Cena b1 - Ele tropeçou numa pedra, desmaiou e ficou caído por um minuto.
- Cenario: countryside | luz: day | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (1): PED (variante 0, expressao scared)
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): minuto
- RISCOS: nenhum

## Cena b2 - Depois os dois pularam de alegria e jogaram a bola para cima.
- Cenario: countryside | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (2): JOA (variante 0, expressao smile); PED (variante 0, expressao grin)
- Animacao: conversar | interacao: o outro se aproxima
- Objetos/modelos: kit/balloon, kit/ball
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): alegria, bola, dois
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
kit/balloon | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/ball | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: - | grandes momentos: - | planos abertos: 0 | mistura: close 31% | medio 69% | aberto 0% | detalhe 0%
- Interacoes: b0 empurrar, b2 o outro se aproxima
- RISCOS GERAIS: 
  - nenhum mapa no video (o canal situa o lugar com mapa rapido) -> CORRECAO: "mapa": "NOME DO LUGAR" na cena 1 ou 2
  - menos de 2 grandes momentos -> CORRECAO: "batalha": true (ou "impact": true) em duas cenas de acao
  - video sem objeto heroi -> CORRECAO: "heroi": "kit/<objeto>" no topo do roteiro (modele se nao existir)

## RESUMO: 3 risco(s) em aberto
- geral: nenhum mapa no video (o canal situa o lugar com mapa rapido)
- geral: menos de 2 grandes momentos
- geral: video sem objeto heroi

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh teste_queda bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh teste_queda` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
