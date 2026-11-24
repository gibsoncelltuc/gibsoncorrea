# CRONOGRAMA - Poder e Fama EP 26 - O Presidente dos 85 por Cento

Gerado em 24/11 02:52 | 12 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_cidade | two | BUK, REP | - | ballot_box, volcano | - | Em fevereiro de dois mil e vinte e quatro, um presidente foi reeleito 
b1 | transicao | loc_campo | reveal | POV, POV | 6 | volcano | - | Foi em El Salvador, na América Central. O presidente era Nayib Bukele.
b2 | simples | palace | two | BUK, POV | - | volcano | - | Ele tinha chegado ao poder em dois mil e dezenove, com trinta e sete a
b3 | simples | interior madeira | two | JUI, REP | - | scroll | - | A Constituição proibia a reeleição seguida. Mas, em dois mil e vinte e
b4 | chave | hall | crowd | REP, POV | 12 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Críticos e opositores disseram que a candidatura era ilegal. O governo
b5 | simples | loc_campo | two | POV, POV | - | ballot_box, volcano | - | No dia da eleição, os salvadorenhos foram às urnas.
b6 | simples | interior loja | close | REP | - | - | - | Acontece que o resultado impressionou: Bukele teve quase oitenta e cin
b7 | chave | palace | crowd | BUK, POV, POV | 30 | ballot_box, volcano | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Os apoiadores lotaram as ruas. Ele comemorou numa sacada, diante de um
b8 | simples | interior hospital | two | REP, BUK | - | - | - | O motivo mais citado pelos eleitores: a queda enorme no número de assa
b9 | simples | loc_pista | two | REP, POV | - | volcano | - | Organizações de direitos humanos, porém, criticaram as prisões em mass
b10 | simples | loc_pista | close | BUK | - | ballot_box, globe, volcano | - | Amado por muitos e criticado por outros, ele virou um dos presidentes 
b11 | simples | loc_campo | close | BUK | - | volcano | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/13 itens) | PENDENTE | python3 pesquisar.py bukele2024
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 2) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh bukele2024
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh bukele2024
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local bukele2024 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

