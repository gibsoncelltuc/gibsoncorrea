# CRONOGRAMA - Curiosidade e Ciência EP 04 - Fleming e a Penicilina

Gerado em 24/11 13:07 | 12 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_campo | two | FLE, COL | - | marco_bigben, petri | - | Um mofo esquecido no meio da bagunça acabou salvando milhões de vidas.
b1 | transicao | loc_campo | reveal | MED, MED | 8 | marco_bigben | - | Era mil novecentos e vinte e oito, em Londres, e Alexander Fleming era
b2 | simples | interior madeira | two | FLE, COL | - | - | - | Ele estudava bactérias e deixava os pratos de cultura empilhados na ba
b3 | simples | interior madeira | group | FLE, COL | - | - | - | Um dia, ele saiu de férias por um mês e não limpou nada.
b4 | simples | interior madeira | two | COL, FLE | - | gosma, petri | - | Quando voltou, achou um prato estragado, coberto de bolor verde.
b5 | simples | loc_montanha | close | FLE | - | gosma, petri | - | Ele ia jogar o prato fora, mas olhou melhor.
b6 | chave | hall | orbit | FLE, COL | 10 | petri | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que, em volta do mofo, as bactérias tinham sumido.
b7 | explicativa | interior madeira | two | sem personagem | - | - | corpo: kit/petri (parado); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em | O mofo soltava algo que matava as bactérias, e ele deu a isso o nome d
b8 | simples | interior pedra | group | MED, MED, POV | - | petri | - | Anos depois, outros cientistas transformaram o bolor em remédio, e ele
b9 | chave | hall | group | FLE, COL | 14 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em mil novecentos e quarenta e cinco, Fleming ganhou o Nobel.
b10 | simples | loc_montanha | close | FLE | - | - | - | No fim, a bagunça dele valeu mais que qualquer faxina.
b11 | simples | loc_campo | close | FLE | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/12 itens) | PENDENTE | python3 pesquisar.py fleming1928
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh fleming1928
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh fleming1928
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local fleming1928 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

