# CRONOGRAMA - Poder e Fama EP 07 - A Cidade do Surfe

Gerado em 25/11 17:22 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | interior pedra | two | BUK | - | surfboard | - | Um país pequeno decidiu virar a capital mundial do surfe.
b1 | transicao | loc_cidade | reveal | BUK | 8 | surfboard, volcano | - | E os surfistas do mundo inteiro foram atrás.
b2 | simples | harbor | two | BUK, JOR | - | surfboard, volcano | - | Em 2019, Nayib Bukele lançou a Surf City em El Salvador.
b3 | chave | harbor | crowd | BUK | 10 | surfboard, volcano | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em 2021, o país sediou o Mundial de Surfe.
b4 | simples | loc_cidade | two | JOR, JOR2 | - | - | - | O evento valia vaga para as Olimpíadas de Tóquio.
b5 | chave | harbor | crowd | BUK | 10 | surfboard, volcano | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em 2023, vieram 294 competidores, de olho em Paris.
b6 | simples | interior loja | two | BUK, JOR2 | - | surfboard | - | O governo promete quinhentos mil empregos, sem garantia.
b7 | simples | harbor | low | JOR, JOR2, POV | - | - | - | Acontece que moradores e ambientalistas se preocupam com a costa.
b8 | simples | harbor | group | BUK, JOR, JOR2 | - | surfboard | - | Em 2025, o Mundial voltou para lá.
b9 | simples | interior pedra | two | BUK | - | surfboard | - | Capital do surfe ou promessa grande demais? Você decide.

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (12/13 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 2) | PENDENTE | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | REFAZER (a etapa anterior mudou) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh surfcity2019
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh surfcity2019
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local surfcity2019 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 4. Travas do roteiro

