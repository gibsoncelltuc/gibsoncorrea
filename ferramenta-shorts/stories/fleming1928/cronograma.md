# CRONOGRAMA - Curiosidade e Ciência EP 04 - Fleming e a Penicilina

Gerado em 25/11 17:49 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | interior madeira | wide | FLE, COL | - | bancada, petri_mofo | - | Um mofo esquecido numa mesa bagunçada salvou milhões de vidas.
b1 | simples | street | close | FLE | - | marco_bigben | - | E tudo porque o cientista saiu de férias.
b2 | chave | street | wide | MED, MED | 8 | marco_bigben | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em 1928, Alexander Fleming trabalhava num laboratório em Londres.
b3 | simples | interior madeira | wide | FLE, COL | - | bancada, petri | - | Ele deixava os pratos de bactérias empilhados na bancada.
b4 | chave | loc_campo | orbit | FLE, COL | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Saiu de férias por um mês e não limpou nada.
b5 | simples | interior madeira | two | FLE | - | bancada, petri_mofo | - | Na volta, um prato estava coberto de bolor verde.
b6 | simples | interior madeira | wide | FLE, COL | - | bancada, petri_mofo | - | Acontece que, em volta do mofo, as bactérias tinham sumido.
b7 | explicativa | interior pedra | two | sem personagem | - | - | corpo: kit/petri_mofo (parado); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; som: s | O mofo matava bactérias. Era a penicilina.
b8 | simples | interior galpao | group | MED, MED, POV | - | - | - | Virou remédio e salvou milhões de pessoas.
b9 | simples | interior madeira | wide | FLE, COL | - | bancada, petri_mofo | - | Fleming ganhou até o Nobel. E foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (14/15 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | PENDENTE | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh fleming1928
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh fleming1928
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local fleming1928 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 5. Voz

