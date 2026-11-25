# CRONOGRAMA - Poder e Fama EP 27 - A Maior Prisão das Américas

Gerado em 25/11 17:32 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_campo | two | GUA | - | prison | - | Uma prisão para quarenta mil presos virou notícia no mundo inteiro.
b1 | simples | loc_patio | wide | POV | - | prison | - | E ninguém concorda se ela é solução ou problema.
b2 | transicao | loc_cidade | wide | POV | - | prison | - | Ela abriu em 2023, em El Salvador.
b3 | simples | interior pedra | two | REP, POV | - | - | - | O país tinha das maiores taxas de assassinato do mundo.
b4 | simples | loc_campo | wide | BUK | - | prison | - | O governo decretou estado de exceção contra as gangues.
b5 | explicativa | loc_estudio | two | sem personagem | - | - | corpo: kit/prison (gira); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em  | Muralhas, cercas elétricas e torres de vigia.
b6 | chave | loc_campo | orbit | REP, BUK | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que os assassinatos caíram de 106 para 2,4 por cem mil.
b7 | simples | loc_campo | two | REP, POV | - | - | - | Mas houve denúncias de prisões sem julgamento.
b8 | chave | loc_pista | wide | BUK, POV | - | globe | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | O modelo passou a ser copiado e criticado.
b9 | simples | loc_campo | wide | GUA | - | prison | - | Segurança ou excesso? Foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (11/14 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh cecot2023
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh cecot2023
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local cecot2023 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

