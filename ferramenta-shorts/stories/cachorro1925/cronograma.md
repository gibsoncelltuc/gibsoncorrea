# CRONOGRAMA - Guerras Inusitadas EP 18 - A Guerra do Cão Fugitivo

Gerado em 25/11 17:51 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_campo | track | GRE, BUL | - | dog_sit | - | Um cachorro perdido quase começou uma guerra na Europa.
b1 | simples | loc_campo | two | GRE | - | dog_sit | - | E até hoje não se sabe nem se o cachorro existiu.
b2 | simples | mountain | reveal | GRE, BUL | 48 | - | - | Em 1925, a fronteira entre Grécia e Bulgária estava tensa.
b3 | transicao | loc_campo | track | GRE, GRE | - | - | - | Dizem que um soldado grego cruzou a fronteira atrás do cachorro.
b4 | simples | mountain | two | BUL, GRE | 12 | - | - | Soldados búlgaros atiraram, e o grego morreu.
b5 | chave | loc_montanha | orbit | GRE, GRE | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | A Grécia deu quarenta e oito horas para a Bulgária pagar.
b6 | chave | mountain | wide | GRE | 48 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Dias depois, vinte mil soldados gregos invadiram a Bulgária.
b7 | simples | interior madeira | two | DIP | - | - | - | A Bulgária apelou à Liga das Nações.
b8 | simples | mountain | two | PRE, DIP | 12 | - | - | A Liga mandou parar. A Grécia recuou e pagou indenização.
b9 | simples | loc_campo | track | GRE, BUL | - | dog_sit | - | Talvez o cachorro nem existisse. Mas foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (10/10 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | PENDENTE | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | REFAZER (a etapa anterior mudou) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | REFAZER (a etapa anterior mudou) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh cachorro1925
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh cachorro1925
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local cachorro1925 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 5. Voz

