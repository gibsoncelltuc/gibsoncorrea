# CRONOGRAMA - Curiosidade e Ciência EP 12 - O Astrônomo do Nariz de Metal

Gerado em 24/11 02:52 | 12 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | medieval | two | TYC, PAR | - | brass_nose, marco_rostock | - | Um dos maiores astrônomos da história perdeu o nariz numa briga por ca
b1 | chave | street | crowd | TYC, POV | 6 | house_two, marco_rostock, lamppost | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Era mil quinhentos e sessenta e seis. Tycho Brahe, um jovem nobre da D
b2 | simples | interior madeira | group | TYC, PAR, POV | - | - | - | Numa festa, ele discutiu com um primo sobre quem era o melhor em matem
b3 | simples | street | two | TYC, PAR | - | marco_rostock | - | A briga não acabou ali. Dias depois, os dois resolveram tudo num duelo
b4 | simples | street | two | PAR, TYC | - | brass_nose, marco_rostock | - | Acontece que o primo acertou um golpe certeiro, e cortou fora um pedaç
b5 | simples | loc_montanha | two | TYC | - | brass_nose, marco_rostock | - | Para esconder o buraco, ele passou a usar um nariz de metal, colado no
b6 | simples | harbor | orbit | REI, TYC | 6 | marco_rostock | - | Anos depois, o rei da Dinamarca deu a ele uma ilha inteira, só para es
b7 | simples | loc_campo | group | TYC | - | marco_rostock, marco_uraniborg, tower | - | Lá, ele construiu um castelo observatório, e anotou a posição de mais 
b8 | simples | interior pedra | two | TYC, KEP | - | - | - | As anotações eram tão precisas, que ajudaram Kepler a descobrir como o
b9 | chave | medieval | crowd | KEP, POV, POV | 16 | marco_rostock | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Essa descoberta mudou a astronomia para sempre.
b10 | simples | loc_montanha | close | TYC | - | brass_nose, marco_rostock | - | E Tycho entrou para a história assim: com a cabeça nas estrelas, e o n
b11 | simples | street | close | TYC | - | marco_rostock | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/5 itens) | PENDENTE | python3 pesquisar.py tycho1566
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 2) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | REFAZER (a etapa anterior mudou) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh tycho1566
10 | Render | todos os quadros renderizados nesta versao das folhas | REFAZER (a etapa anterior mudou) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh tycho1566
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local tycho1566 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

