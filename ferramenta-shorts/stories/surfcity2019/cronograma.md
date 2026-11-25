# CRONOGRAMA - Poder e Fama EP 07 - A Cidade do Surfe

Gerado em 25/11 17:28 | 9 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | interior pedra | two | BUK | - | surfboard | - | Um país pequeno decidiu virar a capital mundial do surfe.
b1 | transicao | loc_cidade | reveal | BUK | 8 | surfboard, volcano | - | E os surfistas do mundo inteiro foram atrás.
b2 | simples | loc_cidade | two | BUK, JOR | - | surfboard, volcano | - | Em 2019, o presidente Nayib Bukele lançou a Surf City.
b3 | chave | harbor | crowd | BUK | 10 | surfboard, volcano | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em 2021, o país sediou o Mundial de Surfe.
b4 | chave | harbor | crowd | BUK | 10 | surfboard, volcano | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Depois, vieram 294 surfistas, de olho em Paris.
b5 | simples | interior loja | two | BUK, JOR2 | - | surfboard | - | O governo promete quinhentos mil empregos, sem garantia.
b6 | simples | harbor | low | JOR, JOR2, POV | - | - | - | Acontece que moradores e ambientalistas se preocupam com a costa.
b7 | simples | harbor | group | BUK, JOR, JOR2 | - | surfboard | - | Em 2025, o Mundial voltou para lá.
b8 | simples | interior pedra | two | BUK | - | surfboard | - | Capital do surfe ou exagero? Só sei que foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/13 itens) | PENDENTE | python3 pesquisar.py surfcity2019
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh surfcity2019
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh surfcity2019
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local surfcity2019 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

