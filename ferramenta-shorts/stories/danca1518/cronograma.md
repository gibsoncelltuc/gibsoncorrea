# CRONOGRAMA - Curiosidade e Ciência EP 22 - A Praga da Dança

Gerado em 24/11 08:45 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | street | two | TRO, POV | - | marco_viena | - | Uma mulher começou a dançar no meio da rua, e não conseguiu mais parar
b1 | simples | street | reveal | TRO, POV | 8 | marco_viena | - | Era verão em Estrasburgo. Ela dançou o dia inteiro, a noite inteira, e
b2 | simples | interior madeira | group | TRO, POV, POV, POV | - | - | - | Em uma semana, mais de trinta vizinhos estavam dançando com ela. Ningu
b3 | chave | loc_campo | crowd | POV, POV, TRO | 48 | marco_viena | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em um mês, eram quatrocentas pessoas, de pés sangrando, pedindo socorr
b4 | simples | interior pedra | two | PRE, MED | - | - | - | O prefeito chamou os médicos. "É sangue quente", disseram eles. "O rem
b5 | simples | hall | low | MUS, MUS | 30 | house_two, lamppost | - | Acontece que a cidade levou isso a sério. Montou um palco, e contratou
b6 | chave | loc_campo | orbit | POV, POV | 18 | marco_viena | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Foi a pior ideia possível. Com música, mais gente entrou na dança, e m
b7 | simples | interior loja | two | PRE, MED | - | - | - | As crônicas da época falam em mortes, mas os historiadores discutem qu
b8 | simples | loc_montanha | track | POV, POV, TRO | - | - | - | No fim, os dançarinos foram levados para um santuário nas montanhas, e
b9 | simples | street | close | MED | - | - | - | Até hoje, ninguém sabe explicar direito o que aconteceu naquele verão.
b10 | simples | street | two | PRE | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/3 itens) | PENDENTE | python3 pesquisar.py danca1518
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 2) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh danca1518
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh danca1518
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local danca1518 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

