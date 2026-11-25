# CRONOGRAMA - Poder e Fama EP 26 - O Presidente dos 85 por Cento

Gerado em 25/11 19:25 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_cidade | two | BUK, POV | - | ballot_box, volcano | - | Um presidente teve quase 85% dos votos, e o mundo se dividiu.
b1 | simples | loc_campo | group | BUK | - | ballot_box | - | E o motivo dessa votação é polêmico.
b2 | chave | loc_campo | wide | BUK, POV | - | volcano | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em 2024, Bukele tentou a reeleição em El Salvador.
b3 | simples | loc_cidade | two | BUK, POV | - | - | - | Ele prometeu acabar com a violência das gangues.
b4 | simples | loc_campo | wide | REP, BUK | 6 | - | - | Os assassinatos caíram de 106 para 2,4 por cem mil.
b5 | simples | interior madeira | two | JUI, REP | - | scroll | - | Acontece que a Constituição proibia reeleição seguida.
b6 | chave | loc_patio | orbit | REP, POV | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Uma corte liberou, e críticos chamaram de ilegal.
b7 | simples | loc_campo | wide | REP | 14 | prison, volcano | - | Grupos de direitos humanos criticaram as prisões em massa.
b8 | simples | loc_cidade | two | BUK, REP | - | - | - | Mesmo assim, ele levou 84,6% dos votos.
b9 | simples | loc_cidade | two | BUK, POV | - | ballot_box | - | Amado por uns, criticado por outros. Foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (13/13 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | PENDENTE | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh bukele2024
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh bukele2024
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local bukele2024 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 5. Voz

