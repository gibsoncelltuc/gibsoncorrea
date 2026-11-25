# CRONOGRAMA - Guerras Inusitadas EP 03 - A Guerra de Toledo

Gerado em 25/11 13:43 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | countryside | two | OHI | 16 | canivete_aberto | - | Dois estados americanos foram à guerra, e o único ferido levou uma can
b1 | transicao | countryside | reveal | OHI, MIC | 48 | house_two, mapa_antigo, lamppost | - | Ohio e Michigan juravam que a cidade de Toledo era deles, por causa de
b2 | simples | interior madeira | close | GOV | - | - | - | O governador de Michigan tinha só vinte e três anos, e mandou a milíci
b3 | chave | countryside | crowd | OHI | 48 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Ohio respondeu com a própria milícia, e as duas tropas chegaram à beir
b4 | chave | countryside | orbit | OHI | 48 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Houve gritos, ameaças e tiros para o alto. Ninguém acertou ninguém.
b5 | simples | interior madeira | two | RAP, XER | - | canivete_aberto | - | A única baixa foi um xerife de Michigan, espetado numa briga de tavern
b6 | simples | interior pedra | two | GOV, OHI | - | - | - | O presidente mandou os dois pararem, e o Congresso ofereceu um acordo.
b7 | simples | arctic | wide | OHI, MIC, GOV | - | bush, tree_oak, tree_pine | - | Ohio ficou com Toledo. Michigan levou um pedaço de floresta gelada que
b8 | simples | arctic | wide | GOV, MIC | 32 | minerio, bush, tree_oak, tree_pine | - | Só que debaixo daquela floresta havia cobre e ferro. Uma fortuna.
b9 | simples | interior madeira | close | GOV | - | - | - | No fim das contas, Michigan perdeu a guerra, e ficou rico.
b10 | simples | interior madeira | two | OHI | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

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
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh toledo1835
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh toledo1835
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local toledo1835 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

