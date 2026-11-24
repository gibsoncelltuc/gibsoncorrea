# FOLHA 2 - PRODUCAO: Poder e Fama EP 05 - Cem Dias ou de Graça

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/bateria2017/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py bateria2017` de novo ate esta folha sair sem risco.

## Cena b0 - Em março de dois mil e dezessete, Elon Musk respondeu no Twitter ao em...
- Cenario: interior loja | luz: golden | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto
- Personagens principais (1): MUS (variante 0, expressao smug)
- Animacao: conversar
- Objetos/modelos: kit/megapack
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): dois, twitter
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: loja / taverna; hora: golden
- CAMERA: plano medio, 2 personagens de corpo inteiro; plano medio enquadrando personagens e megapack juntos (camera a 8.0 m)
- PERSONAGENS: MUS no centro, expressao smug; sem multidao; acao: fala/gesto
- OBJETO kit/megapack: MEIO, direita (objeto principal da cena); tamanho na tela: 32% da altura da tela; estado: PARADO; 0.6 m: ao lado do personagem, mesmo plano, tamanho de uma pessoa
- TAKES: 3 takes (troca de angulo a cada ~1.7 s, sem corte seco):
  - take 1 (0.2-1.9 s): mesmo angulo
  - take 2 (1.9-3.5 s): gira 16 graus para a direita, camera mais baixa, olhando um pouco de baixo, um pouco mais perto
  - take 3 (3.5-5.2 s): gira 14 graus para a esquerda, camera mais alta, olhando um pouco de cima, um pouco mais longe
<!-- /FICHA -->

## Cena b1 - Musk escreveu que a Tesla instalaria baterias gigantes na Austrália do...
- Cenario: outback | luz: golden | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): MUS (variante 0, expressao grin) | multidao: 0 de 
- Animacao: encena
- Objetos/modelos: kit/megapack, kit/marco_goldengate, kit/roadster
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): australia, graca, tesla
- RISCOS: 
  - frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada -> CORRECAO: "explica": {"objeto": "kit/<objeto>", "vfx": [{"k": "jato", "na": "<palavra>"}], "rotulos": [["NOME", "baixo", "<palavra>"]], "setas": [["cima", "FORCA"]], "medidor"/"passos"/"comparar": ...} (GUIA_DO_ROTEIRISTA.md "Cena de explicacao"); para so mostrar um numero em cima da cena com personagens: "hud": {"contador": {"de": 0, "para": -40, "un": "graus", "na": "<palavra>"}}; se a frase nao e' explicacao: "explica": false
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: fazenda aberta; hora: golden
- CAMERA: plano aberto (cenario inteiro); plano aberto mirando o megapack (alvo z -3.6, camera a 10.0 m, altura 2.4 m), sem multidao na frente
- PERSONAGENS: MUS no centro, expressao grin; sem multidao; acao: fala/gesto
- OBJETO kit/megapack: FUNDO, centro (objeto principal da cena); tamanho na tela: 30% da altura da tela; estado: PARADO; 2.0 m de altura x 6.7 m: ATRAS dos personagens, de lado, ocupando a largura do quadro (a ponta pode sair da tela); personagens na frente, menores
- TEXTO NA TELA: "100 DIAS" flutuando no alto, na palavra 1 da frase
- MAPA: AUSTRÁLIA (cobre a tela 1-2 s)
- TAKES: 3 takes (troca de angulo a cada ~1.7 s, sem corte seco):
  - take 1 (6.7-8.4 s): gira 8 graus para a direita, camera mais baixa, olhando um pouco de baixo, um pouco mais perto
  - take 2 (8.4-10.2 s): gira 18 graus para a esquerda, camera mais alta, olhando um pouco de cima, um pouco mais longe
  - take 3 (10.2-11.9 s): gira 12 graus para a direita, camera mais baixa, olhando um pouco de baixo
<!-- /FICHA -->

## Cena b2 - Os jornais calcularam que ele podia perder mais de cinquenta milhões d...
- Cenario: outback | luz: golden | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (1): MUS (variante 0, expressao worried) | multidao: 30 de 
- Animacao: encena | batalha encenada
- Objetos/modelos: kit/megapack, kit/marco_goldengate
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cinquenta, dolares, jornais
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: fazenda aberta; hora: golden
- CAMERA: plano aberto (cenario inteiro); plano aberto mirando o megapack (alvo z -3.6, camera a 10.0 m, altura 2.4 m), sem multidao na frente
- PERSONAGENS: MUS no centro, expressao worried; sem multidao; acao: fala/gesto
- OBJETO kit/megapack: FUNDO, centro (objeto principal da cena); tamanho na tela: 30% da altura da tela; estado: PARADO; 2.3 m de altura x 7.4 m: ATRAS dos personagens, de lado, ocupando a largura do quadro (a ponta pode sair da tela); personagens na frente, menores
- OBJETO kit/megapack: FUNDO, direita; tamanho na tela: 18% da altura da tela; estado: PARADO; 2.3 m de altura x 7.4 m: ATRAS dos personagens, de lado, ocupando a largura do quadro (a ponta pode sair da tela); personagens na frente, menores
- EFEITO clarao/explosao: na frente, na altura do peito do 1o personagem; entra no quadro +40 da cena
- SOM: sting@40
- TEXTO NA TELA: "50 MILHÕES" flutuando no alto, na palavra 1 da frase
- TAKES: sequencia de acao em 3 cameras (3.5 s): 1) plano medio baixo na tropa (30%); 2) travelling lateral acompanhando a acao (25%); 3) grua subindo ate a vista de cima do campo (45%)
<!-- /FICHA -->

## Cena b3 - O contrato foi fechado no fim de setembro, e o prazo de cem dias começ...
- Cenario: interior pedra | luz: golden | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto
- Personagens principais (2): MUS (variante 0, expressao nervous); JOR (variante 0, expressao suspicious)
- Animacao: reagir | interacao: aproxima-se
- Objetos/modelos: kit/megapack
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): contrato, prazo, setembro
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: sala de pedra (governo/castelo); hora: golden
- CAMERA: plano medio, 2 personagens de corpo inteiro; plano medio enquadrando personagens e megapack juntos (camera a 11.5 m)
- PERSONAGENS: MUS na esquerda, expressao nervous; JOR na direita, expressao suspicious; sem multidao; acao: fala/gesto
- OBJETO kit/megapack: MEIO, centro (objeto principal da cena); tamanho na tela: 32% da altura da tela; estado: PARADO; 0.7 m: entre e um pouco atras dos personagens, mesmo plano, tamanho de uma pessoa
- TAKES: 2 takes (troca de angulo a cada ~1.9 s, sem corte seco):
  - take 1 (17.7-19.5 s): gira 14 graus para a esquerda, camera mais alta, olhando um pouco de cima, um pouco mais longe
  - take 2 (19.5-21.4 s): gira 8 graus para a direita, camera mais baixa, olhando um pouco de baixo, um pouco mais perto
<!-- /FICHA -->

## Cena b4 - Acontece que a bateria ficou pronta em cerca de cinquenta e cinco dias...
- Cenario: outback | luz: golden | clima: limpo
- Camera: wide = ABERTO fixo
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (1): MUS (variante 0, expressao grin) | multidao: 0 de 
- Animacao: - | batalha encenada
- Objetos/modelos: kit/megapack, kit/marco_goldengate, nature/picket_fence
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): bateria, cinquenta, prazo
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: fazenda aberta; hora: golden
- CAMERA: plano aberto (cenario inteiro); plano aberto mirando o megapack (alvo z -3.6, camera a 10.0 m, altura 2.4 m), sem multidao na frente
- PERSONAGENS: MUS no centro, expressao grin; sem multidao; acao: fala/gesto
- OBJETO kit/megapack: FUNDO, centro (objeto principal da cena); tamanho na tela: 30% da altura da tela; estado: PARADO; 2.3 m de altura x 7.4 m: ATRAS dos personagens, de lado, ocupando a largura do quadro (a ponta pode sair da tela); personagens na frente, menores
- OBJETO kit/megapack: FUNDO, direita; tamanho na tela: 18% da altura da tela; estado: PARADO; 2.3 m de altura x 7.4 m: ATRAS dos personagens, de lado, ocupando a largura do quadro (a ponta pode sair da tela); personagens na frente, menores
- OBJETO kit/megapack: FUNDO, esquerda; tamanho na tela: 18% da altura da tela; estado: PARADO; 2.3 m de altura x 7.4 m: ATRAS dos personagens, de lado, ocupando a largura do quadro (a ponta pode sair da tela); personagens na frente, menores
- EFEITO clarao/explosao: na frente, na altura do peito do 1o personagem; entra no quadro +40 da cena
- SOM: ding@40
- TEXTO NA TELA: "55 DIAS" flutuando no alto, na palavra 1 da frase
- TAKES: sequencia de acao em 3 cameras (4.3 s): 1) plano medio baixo na tropa (30%); 2) travelling lateral acompanhando a acao (25%); 3) grua subindo ate a vista de cima do campo (45%)
<!-- /FICHA -->

## Cena b5 - A imprensa chamou de a maior bateria do mundo, com cem megawatts de po...
- Cenario: outback | luz: golden | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): JOR (variante 0, expressao shock); JOR2 (variante 0, expressao laugh)
- Animacao: reagir | interacao: avanca e o outro recua
- Objetos/modelos: kit/megapack, kit/marco_goldengate
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): imprensa, potencia
- RISCOS: 
  - frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada -> CORRECAO: "explica": {"objeto": "kit/<objeto>", "vfx": [{"k": "jato", "na": "<palavra>"}], "rotulos": [["NOME", "baixo", "<palavra>"]], "setas": [["cima", "FORCA"]], "medidor"/"passos"/"comparar": ...} (GUIA_DO_ROTEIRISTA.md "Cena de explicacao"); para so mostrar um numero em cima da cena com personagens: "hud": {"contador": {"de": 0, "para": -40, "un": "graus", "na": "<palavra>"}}; se a frase nao e' explicacao: "explica": false
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: fazenda aberta; hora: golden
- CAMERA: plano medio, 2 personagens de corpo inteiro; plano medio enquadrando personagens e megapack juntos (camera a 11.5 m)
- PERSONAGENS: JOR na esquerda, expressao shock; JOR2 na direita, expressao laugh; sem multidao; acao: fala/gesto
- OBJETO kit/megapack: MEIO, centro (objeto principal da cena); tamanho na tela: 32% da altura da tela; estado: PARADO; 0.7 m: entre e um pouco atras dos personagens, mesmo plano, tamanho de uma pessoa
- MAPA: MUNDO (cobre a tela 1-2 s)
- TAKES: 2 takes (troca de angulo a cada ~1.8 s, sem corte seco):
  - take 1 (28.2-29.9 s): mesmo angulo
  - take 2 (29.9-31.7 s): gira 16 graus para a direita, camera mais baixa, olhando um pouco de baixo, um pouco mais perto
<!-- /FICHA -->

## Cena b6 - Mike Cannon-Brookes disse que nunca tinha ficado tão feliz de perder u...
- Cenario: interior loja | luz: golden | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo
- Personagens principais (1): CAN (variante 0, expressao laugh)
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): aposta, perder
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: loja / taverna; hora: golden
- CAMERA: plano medio, 2 personagens de corpo inteiro
- PERSONAGENS: CAN na esquerda, expressao laugh; MUS na direita, expressao smug; sem multidao; acao: fala/gesto
- OBJETOS: so cenario (nenhum objeto da historia nesta cena)
- TAKES: 2 takes (troca de angulo a cada ~1.7 s, sem corte seco):
  - take 1 (33.0-34.6 s): gira 8 graus para a direita, camera mais baixa, olhando um pouco de baixo, um pouco mais perto
  - take 2 (34.6-36.3 s): gira 18 graus para a esquerda, camera mais alta, olhando um pouco de cima, um pouco mais longe
<!-- /FICHA -->

## Cena b7 - Ou seja, uma conversa no Twitter virou uma obra de cinquenta e cinco d...
- Cenario: outback | luz: golden | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo -> 3/4 pela esquerda, mais alto e aberto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (1): CAN (variante 0, expressao grin)
- Animacao: conversar
- Objetos/modelos: kit/megapack, kit/marco_goldengate
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): cinquenta, conversa, obra, twitter
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: fazenda aberta; hora: golden
- CAMERA: plano medio, 2 personagens de corpo inteiro; plano medio enquadrando personagens e megapack juntos (camera a 8.0 m)
- PERSONAGENS: CAN no centro, expressao grin; sem multidao; acao: fala/gesto
- OBJETO kit/megapack: MEIO, direita (objeto principal da cena); tamanho na tela: 32% da altura da tela; estado: PARADO; 0.6 m: ao lado do personagem, mesmo plano, tamanho de uma pessoa
- TAKES: 2 takes (troca de angulo a cada ~1.9 s, sem corte seco):
  - take 1 (37.6-39.5 s): gira 12 graus para a direita, camera mais baixa, olhando um pouco de baixo
  - take 2 (39.5-41.4 s): mesmo angulo
<!-- /FICHA -->

## Cena b8 - E tudo começou com uma resposta curta, escrita no celular.
- Cenario: loc_campo | luz: golden | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): MUS (variante 0, expressao laugh); JOR (variante 0, expressao shock)
- Animacao: conversar | interacao: susto
- Objetos/modelos: kit/megapack, kit/phone
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): celular
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: vila rural (casas, cercas, campo); hora: golden
- CAMERA: plano medio, 2 personagens de corpo inteiro; plano medio enquadrando personagens e megapack juntos (camera a 11.5 m)
- PERSONAGENS: MUS na esquerda, expressao laugh; JOR na direita, expressao shock; sem multidao; acao: fala/gesto
- OBJETO kit/megapack: MEIO, centro (objeto principal da cena); tamanho na tela: 32% da altura da tela; estado: PARADO; 0.7 m: entre e um pouco atras dos personagens, mesmo plano, tamanho de uma pessoa
- TAKES: 2 takes (troca de angulo a cada ~1.4 s, sem corte seco):
  - take 1 (42.4-43.8 s): gira 16 graus para a direita, camera mais baixa, olhando um pouco de baixo, um pouco mais perto
  - take 2 (43.8-45.1 s): gira 14 graus para a esquerda, camera mais alta, olhando um pouco de cima, um pouco mais longe
<!-- /FICHA -->

## Cena b9 - Moral da história: antes de apostar cinquenta milhões num prazo, leia ...
- Cenario: loc_campo | luz: golden | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo
- Personagens principais (2): MUS (variante 0, expressao laugh); CAN (variante 0, expressao grin)
- Animacao: conversar | interacao: o outro se aproxima
- Objetos/modelos: kit/megapack
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): apostar, contrato
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: vila rural (casas, cercas, campo); hora: golden
- CAMERA: plano medio, 2 personagens de corpo inteiro; plano medio enquadrando personagens e megapack juntos (camera a 11.5 m)
- PERSONAGENS: MUS na esquerda, expressao laugh; CAN na direita, expressao grin; sem multidao; acao: fala/gesto
- OBJETO kit/megapack: MEIO, centro (objeto principal da cena); tamanho na tela: 32% da altura da tela; estado: PARADO; 0.6 m: entre e um pouco atras dos personagens, mesmo plano, tamanho de uma pessoa
- TAKES: 2 takes (troca de angulo a cada ~1.9 s, sem corte seco):
  - take 1 (46.3-48.2 s): gira 8 graus para a direita, camera mais baixa, olhando um pouco de baixo, um pouco mais perto
  - take 2 (48.2-50.1 s): gira 18 graus para a esquerda, camera mais alta, olhando um pouco de cima, um pouco mais longe
<!-- /FICHA -->

## Cena b10 - Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?
- Cenario: loc_campo | luz: golden | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: frente -> 3/4 pela direita, mais perto e mais baixo
- Personagens principais (1): MUS (variante 0, expressao grin)
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): comentar, proximo, tema
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
kit/megapack | b0, b1, b2, b3, b4, b5, b7, b8, b9 | pronto (HEROI: aparece em close) | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/marco_goldengate | b1, b2, b4, b5, b7 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/roadster | b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
nature/picket_fence | b4 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/phone | b8 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: kit/megapack | grandes momentos: b2, b4 | planos abertos: 3 | mistura: close 20% | medio 55% | aberto 18% | detalhe 6%
- Interacoes: b3 aproxima-se, b5 avanca e o outro recua, b8 susto, b9 o outro se aproxima
- RISCOS GERAIS: 
  - o video ABRE com a data (gancho fraco: o canal abre com o fato estranho e so depois situa) -> CORRECAO: reescrever a 1a frase com o fato mais absurdo da historia (sem ano); a data entra na 2a frase ou no mapa
  - GANCHO longo: a 1a frase tem 17 palavras (o canal fecha o gancho em ~4 s: 8-16 palavras) -> CORRECAO: reescrever a 1a frase: o fato mais absurdo da historia, curto, com algo em jogo
  - roteiro sem pesquisa visual completa (falta: local, quando, participantes, roupas, cenario, objetos, fontes_visuais) -> CORRECAO: pesquisar fotos/quadros/videos do fato e preencher "visual" no topo do beats.json (veja GUIA_DO_ROTEIRISTA.md "Pesquisa visual") e ajustar figurino, cenario e objetos a ela

## RESUMO: 5 risco(s) em aberto
- b1: frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada
- b5: frase EXPLICATIVA (ciencia/mecanismo) sem cena de explicacao: a narracao explica e a tela so mostra gente parada
- geral: o video ABRE com a data (gancho fraco: o canal abre com o fato estranho e so depois situa)
- geral: GANCHO longo: a 1a frase tem 17 palavras (o canal fecha o gancho em ~4 s: 8-16 palavras)
- geral: roteiro sem pesquisa visual completa (falta: local, quando, participantes, roupas, cenario, objetos, fontes_visuais)

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh bateria2017 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh bateria2017` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- (sem ficha)
- TAKES: 2 takes (troca de angulo a cada ~1.7 s, sem corte seco):
  - take 1 (51.4-53.0 s): gira 12 graus para a direita, camera mais baixa, olhando um pouco de baixo
  - take 2 (53.0-54.7 s): mesmo angulo
<!-- /FICHA -->

