# CRONOGRAMA - A Invasão da Ilha Vazia

Gerado em 24/11 04:21 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | harbor | two | sem personagem | - | ship | - | Trinta e quatro mil soldados invadiram uma ilha onde não havia inimigo
b1 | transicao | mountain | reveal | USA, CAN, USA | 32 | navio_vapor, airplane | - | Foram mais de trinta e quatro mil soldados americanos e canadenses, co
b2 | chave | arctic | group | USA | 10 | canhao_moderno | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Antes do desembarque, bombardearam Kiska durante semanas.
b3 | chave | mountain | orbit | USA, CAN, USA | 48 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | No meio do nevoeiro, os soldados desceram em silêncio, prontos para um
b4 | simples | mountain | two | USA, CAN | - | - | - | Mas teve um problema: os japoneses já tinham ido embora.
b5 | simples | harbor | orbit | USA | 32 | picket_fence, navios de guerra ao fundo, no tamanho real, ship | - | Duas semanas antes, uma frota tinha evacuado cerca de cinco mil homens
b6 | simples | mountain | group | USA, CAN, USA | - | - | - | Sem inimigo à vista, os Aliados começaram a atirar uns nos outros, no 
b7 | simples | harbor | two | USA | - | - | - | No fim, só acharam na ilha alguns cachorros abandonados.
b8 | simples | harbor | close | OFF | - | - | - | Uma das maiores invasões do Pacífico Norte tomou uma ilha completament
b9 | simples | harbor | two | USA | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (14/16 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 5) | PENDENTE | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh kiska1943
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh kiska1943
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local kiska1943 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 4. Travas do roteiro

