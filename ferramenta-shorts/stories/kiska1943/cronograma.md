# CRONOGRAMA - Guerras Inusitadas EP 21 - A Invasão da Ilha Vazia

Gerado em 24/11 12:24 | 13 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | harbor | two | USA, CAN | 24 | ship | - | Trinta e quatro mil soldados invadiram uma ilha onde não havia inimigo
b1 | simples | arctic | group | USA, CAN, USA | 8 | navio_vapor, airplane | - | Era agosto de mil novecentos e quarenta e três. A ilha de Kiska, no Al
b2 | simples | harbor | reveal | USA, CAN | - | aviao_ww2, tanque_ww2, navio em movimento, navios de guerra ao fundo, no tamanho real | - | Americanos e canadenses chegaram com navios, aviões e tanques.
b3 | chave | arctic | crowd | USA | 48 | aviao_ww2, canhao_moderno | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Antes do desembarque, bombardearam Kiska durante semanas.
b4 | chave | arctic | orbit | USA, CAN, USA | 48 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | No meio do nevoeiro, os soldados desceram em silêncio, prontos para um
b5 | simples | interior pedra | two | USA, CAN | - | - | - | Mas teve um problema: os japoneses já tinham ido embora.
b6 | simples | arctic | track | USA, CAN | 8 | sandbags | - | Eles procuraram o inimigo por dias, em trincheiras vazias.
b7 | transicao | harbor | wide | sem personagem | - | navios de guerra ao fundo, no tamanho real, ship | - | Semanas antes, navios japoneses levaram cinco mil homens embora em men
b8 | simples | arctic | group | USA, CAN, USA | - | - | - | Sem inimigo à vista, os Aliados começaram a atirar uns nos outros, no 
b9 | simples | harbor | group | USA, CAN | 5 | navio_encouracado | - | Mais de vinte soldados morreram nesses tiros, e um navio americano ain
b10 | simples | harbor | prop | USA, CAN | - | dog_sit | - | No fim, só acharam na ilha alguns cachorros abandonados.
b11 | simples | interior madeira | two | OFF, USA | - | dog_sit | - | Uma das maiores invasões do Pacífico Norte tomou uma ilha completament
b12 | simples | interior madeira | close | USA | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (14/16 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh kiska1943
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh kiska1943
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local kiska1943 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

