# CRONOGRAMA - Guerras Inusitadas EP 12 - A Guerra da Orelha de Jenkins

Gerado em 24/11 14:27 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | harbor | two | JEN, ESP | - | ear_jar | - | Uma orelha cortada levou a Inglaterra à guerra contra a Espanha, por q
b1 | simples | harbor | reveal | JEN, MAR | 8 | navios de guerra ao fundo, no tamanho real, ship | - | Em mil setecentos e trinta e um, perto de Cuba, um navio espanhol paro
b2 | chave | loc_campo | two | CAP, JEN | - | ear_jar | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Suspeitaram de contrabando, e o capitão espanhol arrancou a orelha del
b3 | simples | harbor | two | CAP, JEN | - | - | - | "Vá levar isso ao seu rei", teria dito o espanhol.
b4 | simples | interior pedra | group | PRE, JEN, ING, PRE | - | - | - | Sete anos depois, Jenkins relatou a história ao Parlamento inglês, e o
b5 | simples | interior pedra | two | PRE, ING | - | - | - | Acontece que a Inglaterra queria uma desculpa para brigar com a Espanh
b6 | chave | harbor | wide | SOL | 48 | navios de guerra ao fundo, no tamanho real, ship | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em mil setecentos e trinta e nove, a guerra começou, com navios ingles
b7 | simples | palace | two | ESP, ING | - | - | - | Depois de quase dez anos, os dois lados fizeram a paz.
b8 | simples | loc_campo | two | PRE, ING | - | ear_jar | - | Quem deu o nome de Guerra da Orelha de Jenkins foi um escritor, um séc
b9 | simples | loc_campo | close | JEN | - | ear_jar | - | A orelha custou dez anos de guerra, e Jenkins ainda ficou sem ela.
b10 | simples | loc_campo | two | JEN | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (14/16 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh jenkins1739
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh jenkins1739
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local jenkins1739 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

