# CRONOGRAMA - Guerras Inusitadas EP 03 - A Guerra de Toledo

Gerado em 24/11 03:00 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | countryside | two | OHI, MIC | - | - | - | Dois estados americanos foram à guerra, e o único ferido levou uma can
b1 | transicao | countryside | reveal | OHI, MIC | 48 | house_two, mapa_antigo, lamppost | - | De um lado, Ohio. Do outro, Michigan. Os dois juravam que a cidade de 
b2 | simples | interior madeira | close | GOV | - | - | - | O governador de Michigan tinha só vinte e três anos, e mandou a milíci
b3 | chave | countryside | crowd | OHI, OHI | 48 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Ohio respondeu com a própria milícia, e as duas tropas chegaram à beir
b4 | chave | countryside | orbit | OHI, MIC | 48 | teodolito | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Houve gritos, ameaças, e tiros por cima dos topógrafos de Ohio. Todos 
b5 | simples | interior madeira | two | RAP, XER | - | canivete | - | Acontece que a única baixa foi um xerife de Michigan, espetado numa br
b6 | simples | interior pedra | two | GOV, OHI | - | - | - | O presidente mandou os dois pararem, e o Congresso ofereceu um acordo.
b7 | simples | jungle | group | OHI, MIC, GOV | - | bush, tree_oak, tree_pine | - | Ohio ficou com Toledo. Michigan levou, de consolação, um pedaço de flo
b8 | simples | arctic | low | GOV, MIC | - | bush, tree_oak, tree_pine | - | Só que debaixo daquela floresta havia cobre e ferro. Uma fortuna.
b9 | simples | interior madeira | close | GOV | - | - | - | No fim das contas, Michigan perdeu a guerra, e ficou rico.
b10 | simples | interior madeira | two | OHI | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/15 itens) | PENDENTE | python3 pesquisar.py toledo1835
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | REFAZER (a etapa anterior mudou) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | REFAZER (a etapa anterior mudou) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh toledo1835
10 | Render | todos os quadros renderizados nesta versao das folhas | REFAZER (a etapa anterior mudou) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | REFAZER (a etapa anterior mudou) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | REFAZER (a etapa anterior mudou) | ./conferir.sh toledo1835
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local toledo1835 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

