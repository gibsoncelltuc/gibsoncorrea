# CRONOGRAMA - Curiosidade e Ciência EP 20 - As Abelhas que Dançam um Mapa

Gerado em 24/11 04:21 | 13 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_campo | two | FRI, COL | - | bee, beehive | - | As abelhas conversam dançando. E foi um cientista teimoso que descobri
b1 | simples | loc_campo | reveal | POV, POV | 6 | beehive | - | Karl von Frisch nasceu na Áustria, e passou a vida inteira estudando a
b2 | chave | loc_campo | crowd | FRI, ASS | 12 | bee, beehive | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Ele construiu uma colmeia com vidro para ver tudo lá dentro, e colocou
b3 | simples | interior madeira | two | FRI, ASS | - | bee, beehive | - | Depois pintou pontinhos coloridos nas costas das abelhas, para saber q
b4 | simples | loc_campo | close | FRI | - | bee, beehive | - | Acontece que, quando uma abelha achava o açúcar, ela voltava e dançava
b5 | simples | loc_montanha | two | FRI, COL | - | bee, beehive | - | Se a comida estava perto, ela dava voltinhas. Se estava longe, fazia u
b6 | simples | loc_montanha | low | FRI | - | bee, beehive | - | E o mais incrível: o ângulo da rebolada mostrava a direção, comparada 
b7 | simples | loc_montanha | two | FRI, ASS | - | bee, beehive | - | Quanto mais tempo ela rebolava, mais longe estava a comida. Era um map
b8 | simples | interior madeira | two | COL, FRI | - | - | - | Muitos cientistas não acreditaram. Inseto com linguagem? Parecia piada
b9 | chave | loc_montanha | crowd | POV, COL, FRI | 30 | bee, beehive | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Ele repetiu os testes centenas de vezes, mudando o açúcar de lugar. As
b10 | simples | interior pedra | group | FRI, ASS, COL | 4 | - | - | Em mil novecentos e setenta e três, já idoso, ele ganhou o Prêmio Nobe
b11 | simples | loc_campo | close | FRI | - | bee, beehive | - | Então, da próxima vez que vir uma abelha, lembre: ela pode estar conta
b12 | simples | loc_campo | two | FRI | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/13 itens) | PENDENTE | python3 pesquisar.py abelhas1945
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 2) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh abelhas1945
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh abelhas1945
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local abelhas1945 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

