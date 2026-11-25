# FOLHA 2 - PRODUCAO: Guerras Inusitadas EP 05 - Os Gansos que Salvaram Roma

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/gansos390/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py gansos390` de novo ate esta folha sair sem risco.

## Cena b0 - Ninguém te conta: um bando de gansos salvou Roma numa noite.
- Cenario: medieval | luz: noite | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (1): ROM (variante 2, expressao shock)
- Animacao: reagir
- Objetos/modelos: goose
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): bando, gansos
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: vila medieval; hora: noite
- CAMERA: plano de grupo (3+ pessoas)
- PERSONAGENS: ROM no centro, expressao shock; sem multidao; acao: fala/gesto
- OBJETOS: so cenario (nenhum objeto da historia nesta cena)
- EFEITO nuvem de fumaca nos pes: no chao, aos pes; entra no quadro +30 da cena
- SOM: squeal@10
- SOM: squeal@40
- SOM: squeal@80
- TEXTO NA TELA: "GANSOS x GAULESES" flutuando no alto, na palavra 1 da frase
- TAKES: 2 takes (troca de angulo a cada ~2.0 s, sem corte seco):
  - take 1 (0.1-2.1 s): gira 8 graus para a direita, camera mais baixa, olhando um pouco de baixo, um pouco mais perto
  - take 2 (2.1-4.1 s): gira 18 graus para a esquerda, camera mais alta, olhando um pouco de cima, um pouco mais longe
<!-- /FICHA -->

## Cena b1 - Mas o ouro de Roma foi embora mesmo assim.
- Cenario: medieval | luz: dia | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (1): ROM (variante 0, expressao sad) | multidao: 0 de POV
- Animacao: encena
- Objetos/modelos: goose
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): ouro, roma
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: vila medieval; hora: dia
- CAMERA: plano de grupo (3+ pessoas)
- PERSONAGENS: ROM no centro, expressao sad; sem multidao; acao: fala/gesto
- OBJETOS: so cenario (nenhum objeto da historia nesta cena)
- TAKES: 1 take continuo (2.6 s), a camera desliza devagar do enquadramento inicial ao final
<!-- /FICHA -->

## Cena b2 - Em 390 antes de Cristo, os gauleses tomaram Roma.
- Cenario: loc_campo | luz: day | clima: limpo
- Camera: reveal = ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): GAU (variante 0, expressao angry, segura torch) | multidao: 8 de GAU
- Animacao: encena
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cristo, gauleses
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: loc_campo; hora: dia
- CAMERA: revelacao (camera sobe e abre)
- PERSONAGENS: GAU no centro, expressao angry, segura torch; multidao de 8 (GAU) ATRAS dos principais; acao: batalha
- OBJETOS: so cenario (nenhum objeto da historia nesta cena)
- EFEITO poeira nos pes: no chao, aos pes; entra no quadro +20 da cena
- EFEITO clarao/explosao: na frente, na altura do peito do 1o personagem; entra no quadro +55 da cena
- SOM: thump@20
- SOM: thump@55
- MAPA: ROMA (cobre a tela 1-2 s)
- TAKES: sequencia de acao em 3 cameras (3.1 s): 1) plano medio baixo na tropa (30%); 2) travelling lateral acompanhando a acao (25%); 3) grua subindo ate a vista de cima do campo (45%)
<!-- /FICHA -->

## Cena b3 - Os romanos que sobraram se trancaram no Capitólio, uma colina.
- Cenario: loc_montanha | luz: day | clima: limpo
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): ROM (variante 0, expressao nervous) | multidao: 0 de POV
- Animacao: reagir | grande momento (efeito + som, sem tiro)
- Objetos/modelos: buildings/castle_tower
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): capitolio, colina, romanos
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: encosta de montanha; hora: dia
- CAMERA: plano aberto (cenario inteiro); plano aberto mirando o castle_tower (alvo z -2.0, camera a 20.0 m, altura 4.0 m), sem multidao na frente
- PERSONAGENS: ROM no centro, expressao nervous; sem multidao; acao: fala/gesto
- OBJETO buildings/castle_tower: FUNDO, centro (objeto principal da cena); tamanho na tela: 30% da altura da tela; estado: PARADO; 24.6 m de altura x 13.4 m: ATRAS dos personagens, de lado, ocupando a largura do quadro (a ponta pode sair da tela); personagens na frente, menores
- TEXTO NA TELA: "CAPITÓLIO" flutuando no alto, na palavra 1 da frase
- TAKES: 2 takes (troca de angulo a cada ~2.0 s, sem corte seco):
  - take 1 (10.5-12.5 s): gira 16 graus para a direita, camera mais baixa, olhando um pouco de baixo, um pouco mais perto
  - take 2 (12.5-14.5 s): gira 14 graus para a esquerda, camera mais alta, olhando um pouco de cima, um pouco mais longe
<!-- /FICHA -->

## Cena b4 - Numa noite sem lua, os gauleses chegaram em silêncio à muralha.
- Cenario: loc_campo | luz: noite | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): GAU (variante 0, expressao stern) | multidao: 0 de POV
- Animacao: -
- Objetos/modelos: buildings/castle_tower
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): gauleses, muralha
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: loc_campo; hora: noite
- CAMERA: plano aberto (cenario inteiro); plano aberto mirando o castle_tower (alvo z -2.0, camera a 20.0 m, altura 4.0 m), sem multidao na frente
- PERSONAGENS: GAU no centro, expressao stern; sem multidao; acao: fala/gesto
- OBJETO buildings/castle_tower: FUNDO, centro (objeto principal da cena); tamanho na tela: 30% da altura da tela; estado: PARADO; 19.7 m de altura x 10.7 m: ATRAS dos personagens, de lado, ocupando a largura do quadro (a ponta pode sair da tela); personagens na frente, menores
- TAKES: 2 takes (troca de angulo a cada ~1.6 s, sem corte seco):
  - take 1 (14.6-16.1 s): gira 8 graus para a direita, camera mais baixa, olhando um pouco de baixo, um pouco mais perto
  - take 2 (16.1-17.7 s): gira 18 graus para a esquerda, camera mais alta, olhando um pouco de cima, um pouco mais longe
<!-- /FICHA -->

## Cena b5 - Acontece que os gansos sagrados de Juno ouviram e começaram a gritar.
- Cenario: loc_campo | luz: noite | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): ROM (variante 2, expressao shock)
- Animacao: reagir
- Objetos/modelos: goose
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): gansos, gritar, juno
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: loc_campo; hora: dia
- CAMERA: plano aberto (cenario inteiro)
- PERSONAGENS: ROM no centro, expressao shock; sem multidao; acao: fala/gesto
- OBJETOS: so cenario (nenhum objeto da historia nesta cena)
- SOM: squeal@20
- SOM: squeal@55
- SOM: squeal@90
- TEXTO NA TELA: "JUNO" flutuando no alto, na palavra 1 da frase
- TAKES: 2 takes (troca de angulo a cada ~1.4 s, sem corte seco):
  - take 1 (18.8-20.1 s): gira 12 graus para a direita, camera mais baixa, olhando um pouco de baixo
  - take 2 (20.1-21.5 s): mesmo angulo
<!-- /FICHA -->

## Cena b6 - O barulho acordou o soldado Marco Mânlio, que barrou a subida.
- Cenario: loc_campo | luz: noite | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (2): MAN (variante 0, expressao angry); GAU (variante 0, expressao scared) | multidao: 0 de POV
- Animacao: conversar | interacao: cochichar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): barulho, soldado, subida
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: loc_campo; hora: noite
- CAMERA: plano medio, 2 personagens de corpo inteiro
- PERSONAGENS: MAN na esquerda, expressao angry; GAU na direita, expressao scared; sem multidao; acao: fala/gesto
- OBJETOS: so cenario (nenhum objeto da historia nesta cena)
- EFEITO poeira nos pes: no chao, aos pes; entra no quadro +70 da cena
- EFEITO nuvem de fumaca nos pes: no chao, aos pes; entra no quadro +80 da cena
- SOM: thump@66
- SOM: whoosh@60
- TAKES: 2 takes (troca de angulo a cada ~1.7 s, sem corte seco):
  - take 1 (22.2-23.9 s): gira 16 graus para a direita, camera mais baixa, olhando um pouco de baixo, um pouco mais perto
  - take 2 (23.9-25.6 s): gira 14 graus para a esquerda, camera mais alta, olhando um pouco de cima, um pouco mais longe
<!-- /FICHA -->

## Cena b7 - Depois de sete meses de fome, Roma pagou mil libras de ouro.
- Cenario: interior madeira | luz: dia | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (2): ROM (variante 0, expressao sad, segura coin); GAU (variante 0, expressao grin, segura coin)
- Animacao: encena | interacao: entregar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): fome, ouro, sete
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: loc_campo; hora: dia
- CAMERA: plano medio, 2 personagens de corpo inteiro
- PERSONAGENS: ROM na esquerda, expressao sad, segura coin; GAU na direita, expressao grin, segura coin; sem multidao; acao: fala/gesto
- OBJETOS: so cenario (nenhum objeto da historia nesta cena)
- TEXTO NA TELA: "1.000 LIBRAS" numa placa atras dos personagens, na palavra 1 da frase
- TAKES: 2 takes (troca de angulo a cada ~1.6 s, sem corte seco):
  - take 1 (26.0-27.6 s): gira 14 graus para a esquerda, camera mais alta, olhando um pouco de cima, um pouco mais longe
  - take 2 (27.6-29.1 s): gira 8 graus para a direita, camera mais baixa, olhando um pouco de baixo, um pouco mais perto
<!-- /FICHA -->

## Cena b8 - Os gansos salvaram a colina. O ouro, não.
- Cenario: medieval | luz: noite | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: leve direita, perto -> esquerda alta, aberto
- Personagens principais (1): ROM (variante 2, expressao shock)
- Animacao: reagir
- Objetos/modelos: goose
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): colina, gansos, ouro
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
goose | b0, b1, b5, b8 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
buildings/castle_tower | b3, b4 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: - | grandes momentos: b3 | planos abertos: 4 | mistura: close 2% | medio 64% | aberto 34% | detalhe 0%
- Interacoes: b6 cochichar, b7 entregar
- RISCOS GERAIS: nenhum

## RESUMO: 0 risco(s) em aberto - pode renderizar

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh gansos390 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh gansos390` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: vila medieval; hora: noite
- CAMERA: plano de grupo (3+ pessoas)
- PERSONAGENS: ROM no centro, expressao shock; sem multidao; acao: fala/gesto
- OBJETOS: so cenario (nenhum objeto da historia nesta cena)
- EFEITO nuvem de fumaca nos pes: no chao, aos pes; entra no quadro +30 da cena
- SOM: squeal@10
- SOM: squeal@40
- SOM: squeal@80
- TAKES: 2 takes (troca de angulo a cada ~1.5 s, sem corte seco):
  - take 1 (29.3-30.8 s): gira 18 graus para a esquerda, camera mais alta, olhando um pouco de cima, um pouco mais longe
  - take 2 (30.8-32.2 s): gira 12 graus para a direita, camera mais baixa, olhando um pouco de baixo
<!-- /FICHA -->

