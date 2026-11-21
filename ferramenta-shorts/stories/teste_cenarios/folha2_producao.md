# FOLHA 2 - PRODUCAO: Teste de Cenarios

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/teste_cenarios/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py teste_cenarios` de novo ate esta folha sair sem risco.

## Cena b0 - Um homem dirigia tranquilo pela avenida, quando viu algo impossível.
- Cenario: street | luz: day | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (1): CID (variante 1, expressao neutral)
- Animacao: conversar
- Objetos/modelos: vehicles/car
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): homem
- RISCOS: nenhum

## Cena b1 - "Isso não pode estar certo", disse o guarda, coçando a cabeça.
- Cenario: interior loja | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (2): CID (variante 4, expressao nervous); GUA (variante 5, expressao stern)
- Animacao: conversar | interacao: avanca e o outro recua
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cabeca, guarda
- RISCOS: nenhum

## Cena b2 - Então ele entrou na floresta, onde os animais observavam em silêncio.
- Cenario: jungle | luz: day | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): CID (variante 0, expressao shock) | multidao: 8 de POV
- Animacao: reagir
- Objetos/modelos: nature/tree_pine, nature/tree_oak, nature/bush, bear
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): animais, floresta
- RISCOS: nenhum

## Cena b3 - No salão do palácio, todos esperavam a resposta.
- Cenario: interior madeira | luz: day | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (3): GUA (variante 0, expressao stern); CID (variante 6, expressao smile); GUA (variante 1, expressao neutral) | multidao: 12 de POV
- Animacao: encena | batalha encenada
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): palacio, salao
- RISCOS: 
  - multidao/batalha dentro de sala: nao cabe -> CORRECAO: tirar "interior" desta cena (faz na rua/campo) ou reduzir o "crowd"

## Cena b4 - Acontece que a resposta era simples. Ninguém tinha olhado para cima.
- Cenario: interior pedra | luz: day | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (2): CID (variante 0, expressao grin); GUA (variante 0, expressao pained)
- Animacao: conversar | interacao: susto
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): -
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
vehicles/car | b0 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/tree_pine | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/tree_oak | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/bush | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
bear | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: - | grandes momentos: b3 | planos abertos: 2 | mistura: close 3% | medio 70% | aberto 27% | detalhe 0%
- Interacoes: b1 avanca e o outro recua, b4 susto
- RISCOS GERAIS: 
  - nenhum mapa no video (o canal situa o lugar com mapa rapido) -> CORRECAO: "mapa": "NOME DO LUGAR" na cena 1 ou 2
  - menos de 2 grandes momentos -> CORRECAO: "batalha": true (ou "impact": true) em duas cenas de acao
  - video sem objeto heroi -> CORRECAO: "heroi": "kit/<objeto>" no topo do roteiro (modele se nao existir)

## RESUMO: 4 risco(s) em aberto
- b3: multidao/batalha dentro de sala: nao cabe
- geral: nenhum mapa no video (o canal situa o lugar com mapa rapido)
- geral: menos de 2 grandes momentos
- geral: video sem objeto heroi

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh teste_cenarios bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh teste_cenarios` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
