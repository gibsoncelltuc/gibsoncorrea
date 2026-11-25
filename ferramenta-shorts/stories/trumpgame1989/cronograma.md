# CRONOGRAMA - Poder e Fama EP 18 - O Jogo de Tabuleiro do Trump

Gerado em 25/11 17:27 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_cidade | two | TRU, EXE | - | boardgame | - | Donald Trump lançou um jogo com o próprio rosto no dinheiro.
b1 | simples | loc_pista | two | TRU | - | boardgame | - | E o jogo empacou por um motivo bem simples.
b2 | chave | loc_cidade | wide | POV, POV | 6 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em 1989, ele já era um empresário famoso.
b3 | simples | interior loja | two | EXE, TRU | - | boardgame | - | No jogo, o objetivo era juntar prédios, cassinos e hotéis.
b4 | simples | interior loja | close | TRU | - | boardgame | - | As notas tinham a cara dele.
b5 | simples | interior madeira | two | PAI, FIL | - | boardgame | - | Acontece que o manual era longo, e ninguém entendia as regras.
b6 | simples | interior pedra | two | EXE, EXE | - | - | - | Esperavam dois milhões de jogos. Saíram oitocentos mil.
b7 | transicao | loc_pista | orbit | TRU, EXE | 6 | boardgame | - | Em 2004, com O Aprendiz, o jogo voltou.
b8 | chave | loc_cidade | group | TRU, POV, POV | - | boardgame | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Desta vez, com regras bem mais simples.
b9 | simples | loc_cidade | two | TRU, EXE | - | boardgame | - | Um jogo que ninguém entendia. Foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/11 itens) | PENDENTE | python3 pesquisar.py trumpgame1989
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh trumpgame1989
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh trumpgame1989
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local trumpgame1989 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

