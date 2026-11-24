# CRONOGRAMA - Poder e Fama EP 04 - A Fila de Luzes no Céu

Gerado em 24/11 23:16 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | chave | countryside | two | AST | - | starlink_train | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Uma fila de luzes cruzou o céu da Europa, e virou caso de disco voador
b1 | transicao | loc_pista | reveal | AST | 6 | falcon_air, starlink_sat | - | Em maio de dois mil e dezenove, a SpaceX lançou da Flórida sessenta sa
b2 | simples | countryside | two | AST, JOR | - | starlink_sat | - | Um dia depois, um rastreador de satélites holandês, Marco Langbroek, f
b3 | chave | countryside | wide | AST | - | starlink_train, picket_fence | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Ele registrou uma fila de luzes, que levava cerca de três minutos para
b4 | simples | loc_montanha | wide | AST | - | starlink_train | - | Ele viu pelo menos cinquenta e seis objetos brilhando em linha.
b5 | chave | loc_cidade | crowd | JOR | - | phone | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que o site holandês de avistamentos de OVNIs registrou mais d
b6 | simples | interior loja | two | JOR, JOR2 | - | starlink_sat | - | Jornais de vários países explicaram que não eram OVNIs, e sim satélite
b7 | explicativa | loc_cidade | two | sem personagem | - | falcon_air | corpo: kit/starlink_train (parado); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; so | Os satélites ainda estavam juntos, em fila, logo depois do lançamento.
b8 | simples | loc_cidade | reveal | JOR | 10 | phone | - | A imagem da fila de luzes se espalhou por vários países e foi assunto 
b9 | simples | loc_montanha | two | AST, JOR2 | - | rocket, starlink_sat | - | Moral da história: se olhar o céu e vir uma fila de luzes, pode ser um
b10 | simples | loc_montanha | close | AST | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (6/13 itens) | PENDENTE | python3 pesquisar.py starlink2019
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh starlink2019
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh starlink2019
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local starlink2019 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

