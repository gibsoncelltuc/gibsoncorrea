# CRONOGRAMA - Curiosidade e Ciência EP 18 - Os Primeiros Passageiros do Céu

Gerado em 25/11 18:28 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | street | two | JOS | - | balloon, marco_versalhes | - | Os primeiros passageiros de um balão não foram pessoas.
b1 | transicao | street | wide | JOS | - | balloon, marco_versalhes | - | Foram uma ovelha, um pato e um galo.
b2 | chave | street | wide | POV, POV | 6 | marco_versalhes | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em 1783, os irmãos Montgolfier faziam papel.
b3 | simples | interior madeira | group | JOS, ETI | - | campfire | - | Viram que fumaça quente fazia sacos de papel subirem.
b4 | explicativa | loc_campo | two | sem personagem | - | balloon, campfire, fire | corpo: kit/balloon (parado); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som  | Fizeram um balão gigante de pano e papel.
b5 | simples | loc_campo | group | NOB, ETI | - | - | - | Ninguém sabia se dava para respirar lá em cima.
b6 | chave | loc_campo | orbit | POV | - | balloon_air, marco_versalhes | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que o balão subiu de verdade, com os bichos dentro.
b7 | simples | loc_campo | two | ETI | - | balloon | - | Oito minutos depois, pousou, e os bichos estavam vivos.
b8 | simples | street | two | POV, POV | 10 | balloon_air, marco_versalhes | - | Dois meses depois, um balão levou dois homens.
b9 | simples | street | wide | JOS | - | balloon, marco_versalhes | - | Ninguém quis ser cobaia. E foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (10/14 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | PENDENTE | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | REFAZER (a etapa anterior mudou) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh montgolfier1783
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh montgolfier1783
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local montgolfier1783 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 4. Travas do roteiro

