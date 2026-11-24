# CRONOGRAMA - Poder e Fama EP 24 - O Foguete que Voltou de Ré

Gerado em 24/11 20:06 | 12 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_pista | two | MUS | - | falcon9_land | - | Durante décadas, todo foguete era jogado fora depois de um voo. Até qu
b1 | transicao | loc_campo | reveal | POV, POV | 6 | - | - | Foi em dezembro de dois mil e quinze, no Cabo Canaveral, na Flórida.
b2 | simples | hall | wide | MUS | - | falcon9_land | - | Elon Musk queria reaproveitar foguetes, em vez de jogá-los fora. Muito
b3 | simples | harbor | two | ENG | - | falcon9_land | - | As primeiras tentativas de pouso deram errado, e os foguetes tombaram 
b4 | simples | loc_pista | wide | MUS | - | falcon9_land | - | Em vinte e um de dezembro, o Falcon nove decolou com onze satélites.
b5 | simples | loc_pista | wide | ENA | - | falcon9_land | - | Depois de soltar o topo, a parte de baixo voltou para a Terra.
b6 | simples | loc_pista | two | ENG | - | falcon9_land | - | Acontece que ela desceu de ré, de pé, com o motor aceso freando a qued
b7 | chave | loc_pista | orbit | MUS | - | falcon9_land | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | E pousou inteira, abrindo as pernas no último segundo.
b8 | simples | hall | reveal | ENA, ENG | 6 | - | - | Os funcionários da SpaceX comemoraram e se abraçaram.
b9 | simples | loc_pista | two | MUS | - | falcon9_land | - | Foi a primeira vez que o primeiro estágio de um foguete orbital voltou
b10 | simples | harbor | two | MUS, POV | - | - | - | Hoje, pousar de ré virou rotina.
b11 | simples | harbor | close | MUS | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (11/11 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | PENDENTE | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | REFAZER (a etapa anterior mudou) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | REFAZER (a etapa anterior mudou) | ./aprovar_storyboard.sh falcon2015
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh falcon2015
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local falcon2015 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 7. Gates

