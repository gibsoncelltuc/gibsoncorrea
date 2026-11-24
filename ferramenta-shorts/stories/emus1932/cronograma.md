# CRONOGRAMA - Guerras Inusitadas EP 02 - A Guerra dos Emus

Gerado em 24/11 17:09 | 12 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | outback | two | sem personagem | - | - | - | A Austrália declarou guerra a um bando de pássaros, e perdeu.
b1 | simples | outback | reveal | FARM, FARM | - | barn, haybale, picket_fence, scarecrow | - | Em mil novecentos e trinta e dois, vinte mil emus invadiram as plantaç
b2 | simples | interior madeira | two | FARM, AUS | - | - | - | Fazendeiros veteranos pediram metralhadoras, e o ministro da Defesa ma
b3 | chave | countryside | crowd | AUS, AUS, AUS | 14 | canhao_moderno, sandbags | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | O major Meredith levou duas metralhadoras e dez mil balas.
b4 | chave | outback | orbit | AUS, AUS | 24 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que os emus se dividiram em grupos pequenos e rápidos, e as b
b5 | chave | countryside | wide | AUS | - | truck | corpo: cavaleiro galopando; emissao: poeira/clarao do tiro; luz: cena; camera: camera acompanha; som: galope | Numa tentativa, uma metralhadora foi montada num caminhão, mas ele sac
b6 | simples | outback | group | AUS, AUS | - | - | - | Depois de seis dias, milhares de balas gastas e poucos emus abatidos.
b7 | simples | countryside | track | AUS, PRESS, PRESS | 12 | - | - | O major comparou os pássaros a tanques, a imprensa riu, e o governo re
b8 | chave | countryside | crowd | AUS, AUS | 24 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | O exército voltou, e o major disse ter abatido novecentos e oitenta e 
b9 | simples | outback | two | FARM, FARM | - | - | - | No fim, o governo preferiu recompensas, e em seis meses pagou por mais
b10 | transicao | outback | orbit | AUS | 5 | - | - | Exército zero, emus um.
b11 | simples | outback | close | FARM | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (8/17 itens) | PENDENTE | python3 pesquisar.py emus1932
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 3) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
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

