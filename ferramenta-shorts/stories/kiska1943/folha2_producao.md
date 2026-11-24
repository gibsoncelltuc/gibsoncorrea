# FOLHA 2 - PRODUCAO: Guerras Inusitadas EP 21 - A Invasão da Ilha Vazia

Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/kiska1943/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py kiska1943` de novo ate esta folha sair sem risco.

## Cena b0 - Trinta e quatro mil soldados invadiram uma ilha onde não havia inimigo...
- Cenario: harbor | luz: overcast | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): USA (variante 0, expressao stern); CAN (variante 0, expressao stern) | multidao: 24 de USA/CAN
- Animacao: conversar | interacao: aproxima-se | o ultimo personagem ENTRA andando
- Objetos/modelos: ship
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): ilha
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: cais de madeira na beira do mar (agua e horizonte ao fundo); hora: overcast
- CAMERA: plano aberto (cenario inteiro); plano aberto mirando o ship (alvo z -2.0, camera a 20.0 m, altura 4.0 m), multidao ATRAS dos personagens, na frente do objeto
- PERSONAGENS: USA na esquerda, expressao stern; CAN na direita, expressao stern; multidao de 24 (USA, CAN) marchando ATRAS dos principais; acao: fala/gesto
- OBJETO ship: FUNDO, centro (objeto principal da cena); tamanho na tela: 30% da altura da tela; estado: CHEGANDO; 44.3 m de altura x 40.5 m: ATRAS dos personagens, de lado, ocupando a largura do quadro (a ponta pode sair da tela); personagens na frente, menores
- OBJETO ship: FUNDO, direita; tamanho na tela: 18% da altura da tela; estado: CHEGANDO; 44.3 m de altura x 40.5 m: ATRAS dos personagens, de lado, ocupando a largura do quadro (a ponta pode sair da tela); personagens na frente, menores
- EFEITO poeira nos pes: no chao, aos pes; entra no quadro +25 da cena
- SOM: thump@25
- TEXTO NA TELA: "KISKA 1943" flutuando no alto, na palavra 3 da frase
- TAKES: 2 takes (troca de angulo a cada ~1.7 s, sem corte seco):
  - take 1 (0.2-1.8 s): gira 14 graus para a esquerda, camera mais alta, olhando um pouco de cima, um pouco mais longe
  - take 2 (1.8-3.5 s): gira 8 graus para a direita, camera mais baixa, olhando um pouco de baixo, um pouco mais perto
<!-- /FICHA -->

## Cena b1 - Era agosto de mil novecentos e quarenta e três. A ilha de Kiska, no Al...
- Cenario: arctic | luz: overcast | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 4 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto -> direita baixa | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (3): USA (variante 0, expressao stern); CAN (variante 0, expressao stern); USA (variante 1, expressao grin) | multidao: 8 de 
- Animacao: conversar | interacao: avanca e o outro recua
- Objetos/modelos: vehicles/airplane, kit/navio_vapor
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): alasca, ilha, kiska
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: campo de gelo e neve (mar congelado, rochas); hora: overcast
- CAMERA: plano de grupo (3+ pessoas); plano aberto mirando o airplane (alvo z -2.0, camera a 20.0 m, altura 4.0 m), sem multidao na frente
- PERSONAGENS: USA na esquerda, expressao stern; CAN no centro, expressao stern; USA na direita, expressao grin; multidao de 8 () ATRAS dos principais; acao: fala/gesto
- OBJETO vehicles/airplane: FUNDO, centro (objeto principal da cena); tamanho na tela: 30% da altura da tela; estado: PARADO; 14.3 m de altura x 14.3 m: ATRAS dos personagens, de lado, ocupando a largura do quadro (a ponta pode sair da tela); personagens na frente, menores
- OBJETO kit/navio_vapor: FUNDO, direita; tamanho na tela: 18% da altura da tela; estado: PARADO; 26.5 m de altura x 40.5 m: ATRAS dos personagens, de lado, ocupando a largura do quadro (a ponta pode sair da tela); personagens na frente, menores
- TEXTO NA TELA: "34.000 SOLDADOS" numa placa atras dos personagens, na palavra 6 da frase
- MAPA: ALASCA (cobre a tela 1-2 s)
- TAKES: 3 takes (troca de angulo a cada ~2.0 s, sem corte seco):
  - take 1 (4.6-6.6 s): gira 18 graus para a esquerda, camera mais alta, olhando um pouco de cima, um pouco mais longe
  - take 2 (6.6-8.7 s): gira 12 graus para a direita, camera mais baixa, olhando um pouco de baixo
  - take 3 (8.7-10.7 s): mesmo angulo
<!-- /FICHA -->

## Cena b2 - Americanos e canadenses chegaram com navios, aviões e tanques.
- Cenario: harbor | luz: overcast | clima: limpo
- Camera: reveal = ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (2): USA (variante 0, expressao stern); CAN (variante 1, expressao smile)
- Animacao: encena
- Objetos/modelos: kit/aviao_ww2, kit/tanque_ww2, navios de guerra ao fundo, no tamanho real, navio em movimento
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): navios
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: cais de madeira na beira do mar (agua e horizonte ao fundo); hora: overcast
- CAMERA: plano aberto (cenario inteiro); plano aberto mirando o tanque_ww2 (alvo z -3.6, camera a 10.0 m, altura 2.4 m), sem multidao na frente
- PERSONAGENS: USA na esquerda, expressao stern; CAN na direita, expressao smile; sem multidao; acao: fala/gesto
- OBJETO kit/tanque_ww2: FUNDO, centro (objeto principal da cena); tamanho na tela: 30% da altura da tela; estado: CHEGANDO; 2.9 m de altura x 8.0 m: ATRAS dos personagens, de lado, ocupando a largura do quadro (a ponta pode sair da tela); personagens na frente, menores
- OBJETO kit/aviao_ww2: FUNDO, direita; tamanho na tela: 18% da altura da tela; estado: CHEGANDO; 4.9 m de altura x 16.2 m: ATRAS dos personagens, de lado, ocupando a largura do quadro (a ponta pode sair da tela); personagens na frente, menores
- TAKES: 2 takes (troca de angulo a cada ~1.6 s, sem corte seco):
  - take 1 (12.0-13.6 s): gira 16 graus para a direita, camera mais baixa, olhando um pouco de baixo, um pouco mais perto
  - take 2 (13.6-15.1 s): gira 14 graus para a esquerda, camera mais alta, olhando um pouco de cima, um pouco mais longe
<!-- /FICHA -->

## Cena b3 - Antes do desembarque, bombardearam Kiska durante semanas.
- Cenario: arctic | luz: overcast | clima: limpo
- Camera: crowd = ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua)
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (1): USA (variante 2, expressao grin) | multidao: 18 de USA
- Animacao: encena | grande momento (efeito + som, sem tiro)
- Objetos/modelos: kit/aviao_ww2, kit/canhao_moderno
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): desembarque
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: campo de gelo e neve (mar congelado, rochas); hora: overcast
- CAMERA: plano de grupo (3+ pessoas); plano aberto mirando o aviao_ww2 (alvo z -4.4, camera a 16.9 m, altura 2.4 m), sem multidao na frente
- PERSONAGENS: USA no centro, expressao grin; sem multidao; acao: fala/gesto
- OBJETO kit/aviao_ww2: FUNDO, centro (objeto principal da cena); tamanho na tela: 30% da altura da tela; estado: PARADO; 4.9 m de altura x 16.2 m: ATRAS dos personagens, de lado, ocupando a largura do quadro (a ponta pode sair da tela); personagens na frente, menores
- OBJETO cannon: FUNDO, direita; tamanho na tela: 18% da altura da tela; estado: PARADO; 4.9 m de altura x 7.1 m: ATRAS dos personagens, de lado, ocupando a largura do quadro (a ponta pode sair da tela); personagens na frente, menores
- EFEITO clarao/explosao: na frente, na altura do peito do 1o personagem; entra no quadro +38 da cena
- EFEITO clarao/explosao: na frente, na altura do peito do 1o personagem; entra no quadro +60 da cena
- EFEITO clarao/explosao: na frente, na altura do peito do 1o personagem; entra no quadro +82 da cena
- SOM: cannon@38
- SOM: cannon@60
- SOM: cannon@82
- TEXTO NA TELA: "BOMBARDEIO" numa placa atras dos personagens, na palavra 4 da frase
- TAKES: 1 take continuo (2.6 s), a camera desliza devagar do enquadramento inicial ao final
<!-- /FICHA -->

## Cena b4 - No meio do nevoeiro, os soldados desceram em silêncio, prontos para um...
- Cenario: arctic | luz: overcast | clima: neblina
- Camera: orbit = ABERTO: camera girando em volta da acao (tomada continua)
- Takes: 4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som
- Personagens principais (3): USA (variante 0, expressao stern); CAN (variante 1, expressao stern); USA (variante 3, expressao nervous) | multidao: 48 de USA/CAN
- Animacao: encena | batalha encenada
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): combate, nevoeiro, soldados
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: campo de gelo e neve (mar congelado, rochas); hora: overcast; clima: neblina
- CAMERA: travelling (camera acompanha andando)
- PERSONAGENS: USA na esquerda, expressao stern; CAN no centro, expressao stern; USA na direita, expressao nervous; sem multidao; acao: fala/gesto
- OBJETOS: so cenario (nenhum objeto da historia nesta cena)
- TAKES: 2 takes (troca de angulo a cada ~2.2 s, sem corte seco):
  - take 1 (20.4-22.5 s): gira 12 graus para a direita, camera mais baixa, olhando um pouco de baixo
  - take 2 (22.5-24.7 s): mesmo angulo
<!-- /FICHA -->

## Cena b5 - Mas teve um problema: os japoneses já tinham ido embora.
- Cenario: interior pedra | luz: overcast | clima: neblina
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (2): USA (variante 1, expressao shock); CAN (variante 0, expressao shock)
- Animacao: reagir | interacao: susto
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): japoneses, problema
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: sala de pedra (governo/castelo); hora: overcast; clima: neblina
- CAMERA: plano medio, 2 personagens de corpo inteiro
- PERSONAGENS: USA na esquerda, expressao shock; CAN na direita, expressao shock; sem multidao; acao: fala/gesto
- OBJETOS: so cenario (nenhum objeto da historia nesta cena)
- TEXTO NA TELA: "ILHA VAZIA" numa placa atras dos personagens, na palavra 11 da frase
- TAKES: 2 takes (troca de angulo a cada ~1.4 s, sem corte seco):
  - take 1 (25.8-27.1 s): gira 16 graus para a direita, camera mais baixa, olhando um pouco de baixo, um pouco mais perto
  - take 2 (27.1-28.5 s): gira 14 graus para a esquerda, camera mais alta, olhando um pouco de cima, um pouco mais longe
<!-- /FICHA -->

## Cena b6 - Eles procuraram o inimigo por dias, em trincheiras vazias.
- Cenario: arctic | luz: overcast | clima: limpo
- Camera: track = travelling lateral acompanhando quem anda
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (2): USA (variante 0, expressao nervous); CAN (variante 0, expressao nervous) | multidao: 0 de 
- Animacao: encena
- Objetos/modelos: war/sandbags
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): inimigo
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: campo de gelo e neve (mar congelado, rochas); hora: overcast
- CAMERA: travelling (camera acompanha andando)
- PERSONAGENS: USA na esquerda, expressao nervous; CAN na direita, expressao nervous; sem multidao; acao: fala/gesto
- OBJETOS: so cenario (nenhum objeto da historia nesta cena)
- TAKES: 2 takes (troca de angulo a cada ~1.4 s, sem corte seco):
  - take 1 (29.8-31.1 s): gira 8 graus para a direita, camera mais baixa, olhando um pouco de baixo, um pouco mais perto
  - take 2 (31.1-32.5 s): gira 18 graus para a esquerda, camera mais alta, olhando um pouco de cima, um pouco mais longe
<!-- /FICHA -->

## Cena b7 - Semanas antes, navios japoneses levaram cinco mil homens embora em men...
- Cenario: harbor | luz: overcast | clima: neblina
- Camera: wide = ABERTO fixo
- Takes: 1 tomada continua, sem corte (camera abre/gira devagar)
- Personagens principais (0): -
- Animacao: -
- Objetos/modelos: ship, navios de guerra ao fundo, no tamanho real
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): neblina
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: cais de madeira na beira do mar (agua e horizonte ao fundo); hora: overcast; clima: neblina
- CAMERA: plano aberto (cenario inteiro); plano aberto mirando o ship (alvo z -8.2, camera a 101.7 m, altura 6.0 m), sem multidao na frente
- PERSONAGENS: nenhum; sem multidao; acao: fala/gesto
- OBJETO ship: FUNDO, centro (objeto principal da cena); tamanho na tela: 30% da altura da tela; estado: PARADO; 44.3 m de altura x 40.5 m: ATRAS dos personagens, de lado, ocupando a largura do quadro (a ponta pode sair da tela); personagens na frente, menores
- OBJETO ship: FUNDO, direita; tamanho na tela: 18% da altura da tela; estado: PARADO; 44.3 m de altura x 40.5 m: ATRAS dos personagens, de lado, ocupando a largura do quadro (a ponta pode sair da tela); personagens na frente, menores
- TAKES: 3 takes (troca de angulo a cada ~1.8 s, sem corte seco):
  - take 1 (33.8-35.6 s): gira 12 graus para a direita, camera mais baixa, olhando um pouco de baixo
  - take 2 (35.6-37.5 s): mesmo angulo
  - take 3 (37.5-39.3 s): gira 16 graus para a direita, camera mais baixa, olhando um pouco de baixo, um pouco mais perto
<!-- /FICHA -->

## Cena b8 - Sem inimigo à vista, os Aliados começaram a atirar uns nos outros, no ...
- Cenario: arctic | luz: overcast | clima: neblina
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto
- Personagens principais (3): USA (variante 0, expressao shock); CAN (variante 0, expressao shock); USA (variante 2, expressao pained)
- Animacao: reagir | interacao: discutir
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): aliados, atirar, escuro, neblina, vista
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: campo de gelo e neve (mar congelado, rochas); hora: overcast; clima: neblina
- CAMERA: plano de grupo (3+ pessoas)
- PERSONAGENS: USA na esquerda, expressao shock; CAN no centro, expressao shock; USA na direita, expressao pained; sem multidao; acao: fala/gesto
- OBJETOS: so cenario (nenhum objeto da historia nesta cena)
- EFEITO clarao/explosao: na frente, na altura do peito do 1o personagem; entra no quadro +30 da cena
- EFEITO clarao/explosao: na frente, na altura do peito do 1o personagem; entra no quadro +60 da cena
- SOM: gun@30
- SOM: gun@50
- SOM: gun@65
- TEXTO NA TELA: "FOGO AMIGO" numa placa atras dos personagens, na palavra 15 da frase
- TAKES: 2 takes (troca de angulo a cada ~2.2 s, sem corte seco):
  - take 1 (40.6-42.8 s): gira 14 graus para a esquerda, camera mais alta, olhando um pouco de cima, um pouco mais longe
  - take 2 (42.8-45.0 s): gira 8 graus para a direita, camera mais baixa, olhando um pouco de baixo, um pouco mais perto
<!-- /FICHA -->

## Cena b9 - Mais de vinte soldados morreram nesses tiros, e um navio americano ain...
- Cenario: harbor | luz: overcast | clima: limpo
- Camera: group = plano de grupo (corpo inteiro); angulo muda a cada ~2 s
- Takes: 3 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto -> esquerda alta, aberto
- Personagens principais (2): USA (variante 0, expressao sad); CAN (variante 0, expressao sad) | multidao: 12 de CAN/USA
- Animacao: conversar | interacao: empurrar
- Objetos/modelos: kit/navio_encouracado
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): navio, vinte
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: cais de madeira na beira do mar (agua e horizonte ao fundo); hora: overcast
- CAMERA: plano aberto (cenario inteiro); plano aberto mirando o navio_encouracado (alvo z -2.0, camera a 20.0 m, altura 4.0 m), multidao ATRAS dos personagens, na frente do objeto
- PERSONAGENS: USA na esquerda, expressao sad; CAN na direita, expressao sad; multidao de 12 (CAN, USA) ATRAS dos principais; acao: fala/gesto
- OBJETO kit/navio_encouracado: FUNDO, centro (objeto principal da cena); tamanho na tela: 30% da altura da tela; estado: PARADO; 33.4 m de altura x 40.5 m: ATRAS dos personagens, de lado, ocupando a largura do quadro (a ponta pode sair da tela); personagens na frente, menores
- EFEITO clarao/explosao: na frente, na altura do peito do 1o personagem; entra no quadro +126 da cena
- SOM: cannon@126
- TEXTO NA TELA: "MINA" flutuando no alto, na palavra 15 da frase
- TAKES: 2 takes (troca de angulo a cada ~2.1 s, sem corte seco):
  - take 1 (46.2-48.3 s): gira 12 graus para a direita, camera mais baixa, olhando um pouco de baixo
  - take 2 (48.3-50.4 s): mesmo angulo
<!-- /FICHA -->

## Cena b10 - No fim, só acharam na ilha alguns cachorros abandonados.
- Cenario: harbor | luz: arctic | clima: neblina
- Camera: prop = -
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (2): USA (variante 1, expressao surprised); CAN (variante 0, expressao surprised)
- Animacao: conversar | interacao: o outro se aproxima
- Objetos/modelos: kit/dog_sit, dog
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): ilha
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: cais de madeira na beira do mar (agua e horizonte ao fundo); hora: arctic; clima: neblina
- CAMERA: plano do objeto; plano medio enquadrando personagens e dog_sit juntos (camera a 11.5 m)
- PERSONAGENS: USA na esquerda, expressao surprised; CAN na direita, expressao surprised; sem multidao; acao: fala/gesto
- OBJETO kit/dog_sit: MEIO, centro (objeto principal da cena); tamanho na tela: 32% da altura da tela; estado: PARADO; 1.1 m: entre e um pouco atras dos personagens, mesmo plano, tamanho de uma pessoa
- OBJETO kit/dog_sit: MEIO, direita; tamanho na tela: 32% da altura da tela; estado: PARADO; 1.1 m: entre e um pouco atras dos personagens, mesmo plano, tamanho de uma pessoa
- TEXTO NA TELA: "SÓ CACHORROS" numa placa atras dos personagens, na palavra 7 da frase
- TAKES: 1 take continuo (2.2 s), a camera desliza devagar do enquadramento inicial ao final
<!-- /FICHA -->

## Cena b11 - Uma das maiores invasões do Pacífico Norte tomou uma ilha completament...
- Cenario: harbor | luz: overcast | clima: limpo
- Camera: two = plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s + CLOSE NO OBJETO no meio da cena (vai e volta)
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto | no meio: desliza ate o objeto (close), segura ~1,5 s e volta
- Personagens principais (2): OFF (variante 0, expressao pained); USA (variante 0, expressao surprised)
- Animacao: conversar | interacao: insiste
- Objetos/modelos: kit/dog_sit
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): ilha, maiores, pacifico
- RISCOS: nenhum
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- LOCAL: cais de madeira na beira do mar (agua e horizonte ao fundo); hora: overcast
- CAMERA: plano medio, 2 personagens de corpo inteiro; plano medio enquadrando personagens e dog_sit juntos (camera a 11.5 m)
- PERSONAGENS: OFF na esquerda, expressao pained; USA na direita, expressao surprised; sem multidao; acao: fala/gesto
- OBJETO kit/dog_sit: MEIO, centro (objeto principal da cena); tamanho na tela: 32% da altura da tela; estado: PARADO; 2.2 m: entre e um pouco atras dos personagens, mesmo plano, tamanho de uma pessoa
- OBJETO kit/dog_sit: MEIO, direita; tamanho na tela: 32% da altura da tela; estado: PARADO; 1.3 m: entre e um pouco atras dos personagens, mesmo plano, tamanho de uma pessoa
- TEXTO NA TELA: "OPERAÇÃO ILHA VAZIA" numa placa atras dos personagens, na palavra 12 da frase
- TAKES: 2 takes (troca de angulo a cada ~1.9 s, sem corte seco):
  - take 1 (55.2-57.0 s): gira 8 graus para a direita, camera mais baixa, olhando um pouco de baixo, um pouco mais perto
  - take 2 (57.0-58.9 s): gira 18 graus para a esquerda, camera mais alta, olhando um pouco de cima, um pouco mais longe
<!-- /FICHA -->

## Cena b12 - Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?
- Cenario: harbor | luz: overcast | clima: limpo
- Camera: close = close no rosto; empurra devagar
- Takes: 2 take(s) de ~1,8 s, deslizando de um para o outro: 3/4 pela esquerda, mais alto e aberto -> leve direita, perto
- Personagens principais (1): USA (variante 0, expressao grin)
- Animacao: conversar
- Objetos/modelos: -
- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): comentar, proximo, tema
- RISCOS: nenhum

## PARA O BLENDER (objetos 3D deste video)
Regra: todo objeto, utensilio, veiculo e animal que aparece e' modelo 3D feito no Blender; a ferramenta so' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).

Objeto | Cenas | Situacao | O que fazer
---|---|---|---
ship | b0, b7 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
vehicles/airplane | b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/navio_vapor | b1 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/aviao_ww2 | b2, b3 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/tanque_ww2 | b2 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/canhao_moderno | b3 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
war/sandbags | b6 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/navio_encouracado | b9 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
kit/dog_sit | b10, b11 | pronto (HEROI: aparece em close) | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py
dog | b10 | pronto | conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py


## Video inteiro
- Objeto heroi: kit/dog_sit | grandes momentos: b3, b4 | planos abertos: 4 | mistura: close 10% | medio 65% | aberto 18% | detalhe 6%
- Interacoes: b0 aproxima-se, b1 avanca e o outro recua, b5 susto, b8 discutir, b9 empurrar, b10 o outro se aproxima, b11 insiste
- RISCOS GERAIS: nenhum

## RESUMO: 0 risco(s) em aberto - pode renderizar

## Reparos depois do render
- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh kiska1943 bN bM` (so essas cenas).
- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh kiska1943` (render completo).
- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.
<!-- FICHA -->

### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)
- (sem ficha)
- TAKES: 2 takes (troca de angulo a cada ~1.7 s, sem corte seco):
  - take 1 (60.0-61.7 s): gira 12 graus para a direita, camera mais baixa, olhando um pouco de baixo
  - take 2 (61.7-63.4 s): mesmo angulo
<!-- /FICHA -->

