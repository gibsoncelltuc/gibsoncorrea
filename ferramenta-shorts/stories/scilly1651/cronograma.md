# CRONOGRAMA - Guerras Inusitadas EP 14 - A Guerra de 335 Anos

Gerado em 25/11 17:22 | 9 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | harbor | two | ILH, HOL | - | scroll | - | Uma guerra durou 335 anos e ninguém disparou um tiro.
b1 | simples | harbor | group | ILH, ILH | - | - | - | E só acabou porque alguém resolveu perguntar.
b2 | chave | harbor | crowd | ILH | 18 | navios de guerra ao fundo, no tamanho real, ship | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em 1651, piratas das ilhas Scilly atacavam navios holandeses.
b3 | chave | harbor | orbit | MAR | - | ship | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | A Holanda declarou guerra às ilhas.
b4 | simples | loc_campo | two | PRE, ILH | - | - | - | Acontece que a Inglaterra tomou as ilhas antes da Holanda chegar.
b5 | simples | harbor | wide | HOL | - | ship | - | Os holandeses foram embora. E ninguém lembrou de assinar a paz.
b6 | simples | interior madeira | two | PRE, EMB | - | - | - | Três séculos depois, um historiador escreveu para a Holanda.
b7 | simples | interior pedra | two | EMB | - | scroll | - | O embaixador veio às ilhas e assinou a paz.
b8 | simples | harbor | two | ILH, HOL | - | scroll | - | Ninguém lembrou de um papel. E foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (12/14 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | PENDENTE | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh scilly1651
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh scilly1651
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local scilly1651 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 7. Gates

