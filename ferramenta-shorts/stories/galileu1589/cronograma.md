# CRONOGRAMA - Curiosidade e Ciência EP 03 - Galileu e a Torre de Pisa

Gerado em 25/11 17:52 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | street | two | GAL | - | bola_couro, marco_pisa, pisa_tower | - | Uma bola pesada e uma leve caíram no chão ao mesmo tempo.
b1 | simples | loc_campo | two | GAL | - | bola_couro | - | E, séculos depois, até uma pena provou isso.
b2 | transicao | street | reveal | ALU, ALU | - | marco_pisa | - | Em 1590, Galileu era professor em Pisa.
b3 | simples | interior pedra | two | ARI, ALU | - | - | - | Aristóteles dizia: quanto mais pesado, mais rápido cai.
b4 | transicao | loc_campo | wide | GAL | - | bola_couro, marco_pisa, pisa_tower, cannonballs | - | Dizem que Galileu levou duas bolas ao alto da torre de Pisa.
b5 | chave | loc_campo | wide | GAL | - | bola_couro, marco_pisa, pisa_tower, cannonballs | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que as duas chegaram juntas ao chão.
b6 | simples | interior madeira | two | GAL, ALU | - | - | - | Tem historiador que duvida dessa história.
b7 | chave | arctic | two | AST | - | feather, hammer | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em 1971, na Lua, um astronauta soltou martelo e pena juntos.
b8 | chave | arctic | two | AST | - | feather, hammer | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Os dois caíram exatamente ao mesmo tempo.
b9 | transicao | street | wide | GAL | - | marco_pisa, pisa_tower | - | Aristóteles errou por dois mil anos. Até que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (11/13 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | PENDENTE | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh galileu1589
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh galileu1589
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local galileu1589 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 8. Storyboard e grade de acoes

