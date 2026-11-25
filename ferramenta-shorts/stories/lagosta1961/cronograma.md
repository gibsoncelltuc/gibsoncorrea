# CRONOGRAMA - Guerras Inusitadas EP 11 - A Guerra da Lagosta

Gerado em 25/11 12:19 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | harbor | two | BRA | - | lobster | - | A França e o Brasil quase entraram em guerra por causa de uma lagosta.
b1 | simples | harbor | wide | PES | - | boat, fishing_net | - | Era mil novecentos e sessenta e um, e barcos franceses pescavam lagost
b2 | explicativa | loc_estudio | two | sem personagem | - | - | corpo: kit/lobster (parado); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som  | O Brasil dizia que a lagosta anda no fundo do mar, e por isso era bras
b3 | explicativa | loc_estudio | two | sem personagem | - | - | corpo: kit/lobster (sobe); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em | A França respondia que a lagosta nada, e por isso era de quem pescasse
b4 | simples | harbor | wide | MFR | - | navio_destroier, navios de guerra ao fundo, no tamanho real | - | A França mandou um navio de guerra para proteger os pescadores dela.
b5 | simples | harbor | two | MAR | - | ship, airplane | - | Acontece que o Brasil não recuou. Mandou navios e aviões para a costa,
b6 | chave | harbor | orbit | MAR, MFR | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Marinheiros dos dois lados se encararam no mar. Os jornais chamaram o 
b7 | simples | interior pedra | two | FRA, BRA | - | - | - | Mas o tiro nunca veio. Os dois governos se reuniram e conversaram, em 
b8 | simples | harbor | reveal | PES, FRA | - | navio em movimento | - | Depois, chegaram a um acordo: alguns barcos franceses podiam pescar, c
b9 | simples | harbor | wide | BRA | - | lobster | - | No fim, ninguém perguntou para a lagosta de que lado ela queria ficar.
b10 | simples | harbor | close | BRA | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (18/18 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh lagosta1961
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh lagosta1961
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local lagosta1961 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

