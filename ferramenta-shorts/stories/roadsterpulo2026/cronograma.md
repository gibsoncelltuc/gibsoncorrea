# CRONOGRAMA - Poder e Fama EP 25 - O Carro que Voou de Cabeça para Baixo

Gerado em 24/11 03:06 | 13 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | chave | loc_pista | two | MUS, ENA | - | roadster26, torre_luz, tower | corpo: decola com o jato dos propulsores embaixo e a onda de ar no chao, sobe 5 m, voa atravessando a cena inclinado e a | Elon Musk prometeu um carro que voa. E, diante de convidados, o carro 
b1 | transicao | loc_pista | reveal | POV, POV | 6 | rampa_curva, telao_led, torre_luz, tower | - | Foi em outubro de dois mil e vinte e seis, à noite, numa base de teste
b2 | simples | interior galpao | two | ENG, MUS | - | roadster26 | - | O novo Roadster da Tesla tinha sido prometido em dois mil e dezessete.
b3 | explicativa | loc_estudio | two | sem personagem | - | tower | corpo: kit/roadster26 (paira) em raio-X; emissao: jato; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som  | O segredo são propulsores da SpaceX escondidos no carro: dez bocais qu
b4 | explicativa | loc_estudio | two | sem personagem | - | tower | corpo: kit/roadster26 (parado); emissao: onda; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em cada e | E um sistema de sucção gruda o carro na pista, como uma ventosa, até d
b5 | chave | loc_pista | wide | MUS | - | roadster26, torre_luz, tower | corpo: acelera e sobe a rampa curva gigante ate ficar de cabeca para baixo; emissao: VFX 3D preso no objeto (jato/poeira | Diante dos convidados, o carro acelerou, subiu uma rampa curva gigante
b6 | chave | loc_pista | group | ENA | - | roadster26, torre_luz, tower | corpo: se solta do topo, voa girando com o jato dos propulsores saindo de baixo e pousa numa nuvem branca (onda de ar no | Então se soltou, voou girando no ar e pousou numa nuvem de fumaça bran
b7 | chave | loc_pista | orbit | MUS | 12 | booster_air, cybercab, cybertruck, roadster26, torre_luz | corpo: decola com o jato dos propulsores embaixo e a onda de ar no chao, sobe 5 m, voa atravessando a cena inclinado e a | Depois decolou de outra rampa e voou, nos propulsores, por cima de uma
b8 | explicativa | loc_estudio | two | sem personagem | - | tower | corpo: kit/roadster26 (corre); emissao: velocidade, jato, pneu; luz: estudio; camera: 2 enquadramentos sem corte seco; s | Segundo a Tesla, ele vai de zero a quase cem por hora em menos de um s
b9 | simples | loc_patio | two | ENG, ENA | - | roadster26, tower | - | Mas especialistas lembraram: aquilo durou poucos segundos, não foi um 
b10 | simples | loc_cidade | close | POV | - | telao_led, tower | - | O vídeo correu o mundo. Metade ficou impressionada, a outra metade des
b11 | chave | interior galpao | two | MUS | - | roadster26 | corpo: canta pneu, pula em arco inclinando o nariz e cai do outro lado com poeira; emissao: VFX 3D preso no objeto (jato | Carro voador ou carro que pula? Você decide.
b12 | simples | interior galpao | close | MUS | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/15 itens) | PENDENTE | python3 pesquisar.py roadsterpulo2026
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh roadsterpulo2026
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh roadsterpulo2026
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local roadsterpulo2026 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

