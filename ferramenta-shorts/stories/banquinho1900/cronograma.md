# CRONOGRAMA - Guerras Inusitadas EP 13 - A Guerra do Banquinho Dourado

Gerado em 24/11 03:10 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_campo | two | GOV, ASH | - | golden_stool | - | Um governador inglês pediu para sentar num banquinho, e isso começou u
b1 | simples | loc_campo | reveal | ASH, ASH | 30 | - | - | Em mil e novecentos, os ingleses mandavam numa região da África chamad
b2 | simples | loc_campo | two | CHE, ASH | - | golden_stool | - | Os ashanti tinham um banquinho dourado sagrado, que representava a alm
b3 | simples | interior madeira | two | GOV, CHE | - | golden_stool | - | Acontece que o governador inglês exigiu o banquinho: "Por que eu ainda
b4 | simples | loc_campo | two | CHE, ASH | - | - | - | Os líderes ashanti ficaram em choque, porque isso era como pedir para 
b5 | chave | loc_campo | crowd | ASH, ASH | 20 | castle_tower | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Eles se revoltaram, cercaram o forte onde ele estava, e o governador t
b6 | chave | loc_campo | orbit | SOL, SOL | 48 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Soldados ingleses marcharam para salvar o governador preso, e a guerra
b7 | simples | interior pedra | two | GOV, PRE | - | - | - | No fim, os ingleses venceram a guerra e assumiram o controle da região
b8 | simples | interior loja | two | CHE, ASH | - | golden_stool | - | Mas os ashanti esconderam o banquinho, e os ingleses nunca conseguiram
b9 | simples | loc_campo | close | GOV | - | golden_stool | - | O governador ganhou a guerra, mas o banquinho nunca foi dele.
b10 | simples | loc_campo | two | GOV | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/5 itens) | PENDENTE | python3 pesquisar.py banquinho1900
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 3) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh banquinho1900
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh banquinho1900
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local banquinho1900 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

