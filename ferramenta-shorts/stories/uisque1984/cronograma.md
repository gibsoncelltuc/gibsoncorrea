# CRONOGRAMA - Guerras Inusitadas EP 17 - A Guerra do Uísque

Gerado em 26/11 00:17 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | arctic | two | CAN, DIN | - | whisky | - | Dois países brigaram quase quarenta anos por uma rocha, usando uísque.
b1 | transicao | arctic | wide | CAN, DIN | - | - | - | E essa guerra acabou do jeito mais educado possível.
b2 | transicao | arctic | reveal | CAN, DIN | - | - | - | A ilha Hans é uma rocha gelada entre Canadá e Groenlândia.
b3 | simples | interior madeira | two | CAN, DIN | - | - | - | Canadá e Dinamarca diziam que a ilha era deles.
b4 | chave | arctic | wide | CAN | 12 | helicopter | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em 1984, soldados canadenses desembarcaram lá.
b5 | simples | arctic | two | CAN, CAN | - | bandeira_canada, whisky | - | Fincaram a bandeira e deixaram uma garrafa de uísque.
b6 | chave | arctic | wide | DIN | - | bandeira_dinamarca | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que os dinamarqueses voltaram e puseram a bandeira deles.
b7 | simples | arctic | two | DIN, CAN | - | barrel, whisky | - | E deixaram aguardente com um bilhete de boas-vindas.
b8 | simples | interior pedra | two | PRE, MIN | - | - | - | Em 2022, enfim, dividiram a ilha ao meio.
b9 | simples | arctic | two | CAN, DIN | - | whisky | - | Nenhum tiro, só garrafas trocadas. E foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (12/15 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh uisque1984
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh uisque1984
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local uisque1984 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

