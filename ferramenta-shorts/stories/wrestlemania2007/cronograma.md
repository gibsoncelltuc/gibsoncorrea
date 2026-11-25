# CRONOGRAMA - Poder e Fama EP 15 - Trump na Batalha dos Bilionários

Gerado em 25/11 17:29 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | stadium | group | TRU, VIN | - | clipper | - | Donald Trump raspou a cabeça de outro bilionário num ringue.
b1 | simples | stadium | wide | JUI, TRU | - | ring | - | E no fim, ele mesmo acabou no chão.
b2 | transicao | loc_cidade | reveal | POV, POV | 6 | - | - | Foi em 2007, no maior show de luta livre.
b3 | simples | interior pedra | group | VIN, TRU | - | clipper | - | Cada um escolheu um lutador. A aposta valia uma cabeça raspada.
b4 | chave | stadium | group | POV, POV, POV | 18 | ball | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Mais de oitenta mil pessoas lotaram o estádio.
b5 | transicao | stadium | wide | LAS, UMA | - | ring | - | O lutador de Trump enfrentou o gigante Umaga.
b6 | chave | stadium | group | LAS | 18 | ball, ring | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que o lutador de Trump venceu, e o estádio foi abaixo.
b7 | simples | stadium | two | TRU, LAS, VIB | - | clipper, ring | - | Trump ajudou a raspar a cabeça de Vince McMahon.
b8 | simples | stadium | group | JUI, TRU | - | ring | - | E o juiz derrubou Trump também.
b9 | simples | stadium | group | TRU, VIN | - | clipper | - | Anos depois, foi para o Hall da Fama. Tudo porque...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/15 itens) | PENDENTE | python3 pesquisar.py wrestlemania2007
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh wrestlemania2007
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh wrestlemania2007
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local wrestlemania2007 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 5. Voz

