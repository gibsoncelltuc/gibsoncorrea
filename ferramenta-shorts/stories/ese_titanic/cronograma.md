# CRONOGRAMA - E Se EP 10 - E Se o Titanic Não Tivesse Afundado?

Gerado em 25/11 17:12 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | chave | harbor | two | CAP, POV | 10 | iceberg | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Diziam que era impossível de ir ao fundo. Foi na primeira viagem.
b1 | simples | harbor | group | PRO, POV | - | ship | - | E se não tivesse afundado, o mar seria mais perigoso hoje.
b2 | transicao | harbor | reveal | POV, POV | 30 | ship | - | Abril de 1912. O Titanic levava mais de duas mil pessoas.
b3 | simples | harbor | two | MAR, CAP | - | iceberg | - | Perto da meia-noite, o vigia gritou: iceberg à frente!
b4 | explicativa | loc_estudio | two | sem personagem | - | iceberg | corpo: kit/iceberg (gira); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em | O gelo rasgou o casco por baixo da água.
b5 | chave | harbor | crowd | POV, POV, MAR | 22 | boat | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que só havia botes para metade das pessoas.
b6 | chave | harbor | orbit | POV, POV, MAR | 22 | boat, picket_fence | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Cerca de mil e quinhentas pessoas morreram.
b7 | simples | harbor | close | PRO | - | scroll | - | Em 1914, veio o primeiro grande tratado do mar: bote para todos.
b8 | simples | harbor | two | MAR, CAP | - | iceberg | - | E criaram uma patrulha de icebergs, que existe até hoje.
b9 | simples | harbor | two | CAP, POV | - | iceberg | - | O pior dia do Titanic deixou o mar mais seguro.

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/11 itens) | PENDENTE | python3 pesquisar.py ese_titanic
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh ese_titanic
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh ese_titanic
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local ese_titanic <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

