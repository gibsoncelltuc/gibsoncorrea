# CRONOGRAMA - Guerras Inusitadas EP 02 - A Guerra dos Emus

Gerado em 24/11 02:52 | 12 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | outback | two | sem personagem | - | - | - | A Austrália declarou guerra a um bando de pássaros. E perdeu.
b1 | simples | outback | reveal | FARM, FARM | - | barn, haybale, picket_fence, scarecrow | - | Vinte mil emus estavam devorando as plantações de trigo no oeste do pa
b2 | simples | interior madeira | two | FARM, AUS | - | - | - | "Mande o exército", pediram eles. E o ministro mandou.
b3 | chave | outback | crowd | AUS, AUS, AUS | 14 | canhao_moderno, sandbags | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Soldados, duas metralhadoras, e dez mil balas. Contra emus.
b4 | chave | outback | orbit | AUS, AUS | 24 | barn, haybale, picket_fence, scarecrow | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que emu é rápido, e não fica parado. Os soldados atiravam, e 
b5 | chave | countryside | two | AUS | - | truck | corpo: canta pneu, pula em arco inclinando o nariz e cai do outro lado com poeira; emissao: VFX 3D preso no objeto (jato | Um atirador montou a metralhadora num caminhão. Mas o caminhão pulava 
b6 | simples | outback | group | AUS, AUS | - | - | - | Depois de uma semana, milhares de balas gastas, e os emus quase sem um
b7 | simples | countryside | track | AUS, PRESS, PRESS | 12 | - | - | A tropa bateu em retirada. A imprensa gargalhou, e o comandante admiti
b8 | chave | outback | crowd | AUS, AUS | 24 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | O exército tentou de novo, abateu algumas centenas, e os emus continua
b9 | simples | outback | two | FARM, FARM | - | barn, haybale, picket_fence, scarecrow | - | No fim, o governo desistiu da guerra, e passou a pagar recompensa aos 
b10 | simples | outback | close | AUS | - | - | - | Humanos, zero. Emus, um.
b11 | simples | outback | two | FARM | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/8 itens) | PENDENTE | python3 pesquisar.py emus1932
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 4) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh emus1932
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh emus1932
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local emus1932 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

