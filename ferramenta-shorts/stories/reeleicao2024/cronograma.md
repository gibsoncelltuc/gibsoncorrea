# CRONOGRAMA - Poder e Fama EP 21 - A Volta de Trump

Gerado em 25/11 17:26 | 9 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_cidade | two | TRU, REP | - | ballot_box, white_house | - | Um presidente perdeu a eleição e voltou quatro anos depois.
b1 | chave | loc_pista | wide | REP, POV | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | E isso só tinha acontecido uma vez na história americana.
b2 | simples | loc_cidade | wide | POV | - | white_house | - | Em 2024, americanos escolhiam entre Trump e Kamala Harris.
b3 | simples | interior loja | two | REP, TRU | - | - | - | A contagem dos votos entrou pela madrugada.
b4 | simples | interior loja | close | REP | - | - | - | Acontece que Trump venceu todos os estados decisivos: 312 votos.
b5 | chave | hall | orbit | TRU | 14 | white_house | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Os apoiadores comemoraram, e ele declarou vitória.
b6 | simples | interior madeira | two | REP, POV | - | scroll | - | Antes dele, só Grover Cleveland tinha voltado assim, há 130 anos.
b7 | simples | loc_pista | group | TRU | - | white_house | - | Antes foi o presidente 45. Agora, o 47.
b8 | simples | loc_cidade | two | TRU, REP | - | ballot_box, white_house | - | Perdeu, voltou e ganhou. E foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/13 itens) | PENDENTE | python3 pesquisar.py reeleicao2024
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh reeleicao2024
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh reeleicao2024
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local reeleicao2024 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

