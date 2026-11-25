# CRONOGRAMA - Curiosidade e Ciência EP 10 - Eratóstenes Mede a Terra

Gerado em 25/11 19:37 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_campo | two | ERA, BIB | - | marco_alexandria, stick | - | Um homem mediu o tamanho da Terra usando só uma vara.
b1 | simples | loc_campo | wide | ERA | - | marco_alexandria, starlink_sat, stick, well | - | E chegou perto do número certo, sem satélite.
b2 | transicao | loc_campo | reveal | BIB, POV | 8 | marco_alexandria | - | Há dois mil anos, Eratóstenes cuidava da biblioteca de Alexandria.
b3 | chave | loc_montanha | wide | ERA, BIB | - | well, tree_palm, bucket | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em Siena, ao meio-dia, o sol iluminava o fundo de um poço.
b4 | simples | loc_montanha | two | ERA, CAM | - | well, tree_palm | - | Ou seja: lá, nada fazia sombra.
b5 | explicativa | loc_estudio | two | sem personagem | - | marco_alexandria, stick, tree_palm | corpo: kit/stick (parado); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em | Em Alexandria, no mesmo dia, uma vara fazia sombra.
b6 | explicativa | loc_estudio | two | sem personagem | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que isso só acontece se a Terra for curva.
b7 | explicativa | loc_estudio | two | sem personagem | - | - | corpo: kit/stick (parado); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em | Ele mediu o ângulo da sombra e a distância entre as cidades.
b8 | explicativa | loc_estudio | two | sem personagem | - | - | corpo: kit/stick (parado); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em | A conta deu quase o tamanho real da Terra.
b9 | simples | loc_campo | two | ERA, BIB | - | rocket, stick | - | Sem foguete, só uma sombra. E foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (13/18 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | PENDENTE | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | REFAZER (a etapa anterior mudou) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh eratostenes240
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh eratostenes240
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local eratostenes240 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 5. Voz

