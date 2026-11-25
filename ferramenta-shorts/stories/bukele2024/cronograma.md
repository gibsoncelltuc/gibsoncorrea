# CRONOGRAMA - Poder e Fama EP 26 - O Presidente dos 85 por Cento

Gerado em 25/11 04:17 | 12 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_cidade | two | BUK, POV | - | ballot_box, volcano | - | Um presidente foi reeleito com uma das maiores votações do mundo.
b1 | simples | loc_campo | two | BUK, POV | - | volcano | - | Foi em El Salvador, na América Central, e o presidente era Nayib Bukel
b2 | chave | loc_cidade | wide | BUK, POV | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Ele chegou ao poder prometendo acabar com a violência das gangues.
b3 | simples | interior madeira | two | JUI, REP | - | scroll | - | A Constituição proibia a reeleição seguida, mas em dois mil e vinte e 
b4 | simples | loc_patio | two | REP, POV | - | - | - | Críticos e opositores disseram que a candidatura era ilegal. O governo
b5 | transicao | loc_campo | wide | POV, POV | 12 | ballot_box, volcano | - | No dia da eleição, os salvadorenhos foram às urnas.
b6 | simples | loc_cidade | two | REP, BUK | - | - | - | Acontece que o resultado impressionou: Bukele teve quase oitenta e cin
b7 | chave | loc_cidade | orbit | BUK | 12 | porch | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Os apoiadores lotaram as ruas, e ele comemorou numa sacada.
b8 | simples | interior galpao | two | REP, BUK | - | - | - | O motivo: os assassinatos caíram de cento e seis para dois vírgula qua
b9 | simples | loc_pista | wide | REP | - | prison, volcano | - | Organizações de direitos humanos, porém, criticaram as prisões em mass
b10 | simples | loc_pista | two | BUK | - | ballot_box, globe | - | Amado por muitos e criticado por outros, ele virou um dos presidentes 
b11 | simples | loc_campo | close | BUK | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (13/13 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh bukele2024
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh bukele2024
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local bukele2024 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

