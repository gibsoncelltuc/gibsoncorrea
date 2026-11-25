# CRONOGRAMA - Guerras Inusitadas EP 09 - A Guerra do Futebol

Gerado em 25/11 17:18 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | stadium | two | HON, SAL | 16 | ball | - | Guerra por futebol parece exagero? Dois países fizeram uma de verdade.
b1 | simples | interior madeira | two | SAL | - | ball | - | E quem ganhou o jogo não fez um gol na Copa.
b2 | transicao | loc_campo | reveal | TOR, TOR | 8 | volcano | - | Em 1969, Honduras e El Salvador já disputavam terras.
b3 | simples | street | two | HON, SAL | 6 | ball | - | Depois veio a disputa de uma vaga na Copa: três jogos.
b4 | simples | stadium | crowd | HON, SAL | 18 | ball | - | No primeiro, Honduras venceu por um a zero.
b5 | simples | street | group | HON, SAL, HON, SAL | 10 | volcano | - | El Salvador venceu o segundo por três a zero. Torcidas brigaram.
b6 | simples | stadium | group | SAL, SAL, HON | 18 | ball | - | No terceiro, El Salvador venceu por três a dois, na prorrogação.
b7 | chave | street | crowd | SOL | 48 | volcano | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que, semanas depois, o exército salvadorenho atacou Honduras.
b8 | chave | street | group | SOL, PRE | 10 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | A guerra durou cem horas, até um cessar-fogo.
b9 | simples | stadium | crowd | HON, SAL | 16 | ball | - | Na Copa, El Salvador perdeu os três jogos. Sem um gol.

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (14/15 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | PENDENTE | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh futebol1969
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh futebol1969
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local futebol1969 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 8. Storyboard e grade de acoes

