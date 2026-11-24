# CRONOGRAMA - Poder e Fama EP 15 - Trump na Batalha dos Bilionários

Gerado em 24/11 18:52 | 13 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | stadium | group | TRU, VIN | - | clipper | - | Antes de virar presidente, Donald Trump entrou num ringue de luta livr
b1 | transicao | loc_cidade | reveal | POV, POV | 6 | marco_detroit | - | Foi em abril de dois mil e sete, em Detroit, no maior show de luta liv
b2 | simples | interior loja | two | TRU, VIN | - | - | - | Como todo show de luta, a rivalidade era combinada: Trump contra o don
b3 | simples | interior pedra | group | VIN, TRU | - | clipper | - | A aposta era maluca: cada um escolheu um lutador, e o dono de quem per
b4 | chave | stadium | crowd | POV, POV, POV | 30 | ball | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Mais de oitenta mil pessoas lotaram o estádio, para ver a Batalha dos 
b5 | simples | stadium | wide | LAS | - | ring | - | No ringue, o lutador de Trump, Bobby Lashley, enfrentou o gigante Umag
b6 | simples | stadium | group | JUI | 30 | ring | - | Acontece que o juiz convidado era Steve Austin, famoso por derrubar to
b7 | chave | stadium | orbit | LAS | - | ball, ring | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | No fim, o lutador de Trump venceu. O estádio inteiro foi abaixo.
b8 | simples | stadium | wide | TRU | - | clipper, ring | - | Trump e Lashley seguraram McMahon, e passaram a máquina de raspar na c
b9 | simples | stadium | two | VIB, TRU, LAS | - | clipper | - | O dono da luta livre saiu do ringue completamente careca.
b10 | simples | stadium | close | JUI | - | ring | - | E ainda sobrou para Trump: o juiz aplicou um golpe nele também, e ele 
b11 | simples | interior madeira | two | TRU, JUI | - | - | - | Seis anos depois, Trump entrou para o Hall da Fama da luta livre. Tudo
b12 | simples | interior madeira | close | TRU | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/5 itens) | PENDENTE | python3 pesquisar.py wrestlemania2007
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 4) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
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

