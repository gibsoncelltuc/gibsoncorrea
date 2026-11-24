# CRONOGRAMA - Poder e Fama EP 15 - Trump na Batalha dos Bilionários

Gerado em 24/11 22:58 | 12 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | stadium | group | TRU, VIN | - | clipper | - | Donald Trump raspou a cabeça de outro bilionário no meio de um ringue.
b1 | transicao | loc_cidade | reveal | POV, POV | 6 | marco_detroit | - | Foi em abril de dois mil e sete, em Detroit, no maior show de luta liv
b2 | simples | interior loja | two | TRU, VIN | - | - | - | A rivalidade era combinada, como todo show de luta: Trump contra o don
b3 | simples | interior pedra | group | VIN, TRU | - | clipper | - | A aposta: cada um escolheu um lutador, e o dono do perdedor teria a ca
b4 | chave | stadium | crowd | POV, POV, POV | 30 | ball | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Mais de oitenta mil pessoas lotaram o estádio, para ver a Batalha dos 
b5 | simples | stadium | wide | LAS | - | ring | - | No ringue, o lutador de Trump, Bobby Lashley, enfrentou o gigante Umag
b6 | simples | stadium | group | JUI | - | ring | - | Acontece que o juiz convidado era Steve Austin, e a luta virou bagunça
b7 | chave | stadium | orbit | LAS | - | ball, ring | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | No fim, o lutador de Trump venceu. O estádio inteiro foi abaixo.
b8 | simples | stadium | wide | TRU | - | clipper, ring | - | Trump e Lashley seguraram McMahon e rasparam a cabeça dele até ficar c
b9 | simples | stadium | two | JUI | - | ring | - | E sobrou para Trump: o juiz derrubou ele também.
b10 | simples | interior madeira | two | TRU, JUI | - | - | - | Seis anos depois, Trump entrou para o Hall da Fama da luta livre.
b11 | simples | interior madeira | close | TRU | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/15 itens) | PENDENTE | python3 pesquisar.py wrestlemania2007
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh wrestlemania2007
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh wrestlemania2007
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local wrestlemania2007 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

