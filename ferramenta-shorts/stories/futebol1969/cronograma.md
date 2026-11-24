# CRONOGRAMA - Guerras Inusitadas EP 09 - A Guerra do Futebol

Gerado em 24/11 23:35 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | stadium | two | HON, SAL | 16 | ball | - | Dois países entraram em guerra por causa de um jogo de futebol.
b1 | simples | street | reveal | TOR, TOR | 8 | volcano | - | Em mil novecentos e sessenta e nove, Honduras e El Salvador já brigava
b2 | simples | street | two | HON, SAL | 6 | ball | - | Aí veio a disputa por uma vaga na Copa do Mundo: três jogos, um contra
b3 | simples | stadium | crowd | HON, SAL | 18 | house_small, ball, picket_fence, tree_oak | - | No primeiro, Honduras venceu por um a zero, em casa.
b4 | simples | street | crowd | HON, SAL, HON, SAL | 10 | volcano | - | No segundo, El Salvador devolveu por três a zero, e os torcedores brig
b5 | simples | interior madeira | two | PRE, PRE | - | - | - | Acontece que, na véspera do terceiro jogo, El Salvador cortou relações
b6 | simples | stadium | group | SAL, SAL, HON | 18 | apartment, house_two, ball, lamppost | - | O jogo foi na Cidade do México, e El Salvador venceu por três a dois, 
b7 | chave | street | crowd | SOL | 48 | volcano | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Semanas depois, o exército salvadorenho atacou Honduras.
b8 | chave | street | group | SOL, PRE | 10 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | A guerra durou cem horas, até a Organização dos Estados Americanos imp
b9 | simples | stadium | two | SAL | - | ball | - | Na Copa, El Salvador perdeu os três jogos, sem fazer um único gol.
b10 | simples | stadium | close | HON | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/15 itens) | PENDENTE | python3 pesquisar.py futebol1969
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh futebol1969
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh futebol1969
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local futebol1969 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

