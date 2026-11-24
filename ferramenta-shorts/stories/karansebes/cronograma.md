# CRONOGRAMA - Guerras Inusitadas EP 01 - A Batalha de Karánsebes

Gerado em 24/11 04:31 | 12 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | chave | countryside | crowd | AUT, AUT, AUT, AUT | 48 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Um exército inteiro conseguiu perder uma batalha contra si mesmo.
b1 | simples | countryside | orbit | AUT, HUS, AUT, OFF | 32 | - | - | Era o exército austríaco, marchando contra os turcos, com soldados de 
b2 | simples | countryside | track | HUS, HUS | 6 | lantern | - | Numa noite, os hussardos foram na frente procurar o inimigo.
b3 | simples | countryside | two | HUS, LOC | 6 | barrel, barrel_r | - | Não acharam turco nenhum. Acharam moradores vendendo aguardente.
b4 | simples | countryside | group | HUS, HUS | 6 | barrel, lantern | - | Compraram tudo, beberam, e a festa começou.
b5 | simples | countryside | two | AUT, HUS, AUT | 6 | - | - | Aí chegou a infantaria, querendo a parte dela. Os hussardos não dividi
b6 | chave | countryside | orbit | HUS | 48 | campfire, tent | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | No escuro, alguém gritou: "Turcos! Turcos!" E o pânico tomou o acampam
b7 | chave | countryside | crowd | AUT, AUT, HUS | 48 | house_small, picket_fence, tree_oak | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que ninguém entendia a língua do vizinho. Todo mundo atirava 
b8 | simples | countryside | group | OFF, AUT | 6 | cannon | - | Um oficial mandou usar a artilharia, e os canhões dispararam contra o 
b9 | simples | countryside | two | TUR, TUR | 5 | barrel, crate, campfire, tent | - | Dois dias depois, os turcos chegaram e acharam o acampamento abandonad
b10 | simples | countryside | close | TUR, TUR | - | - | - | Os turcos venceram sem dar um único tiro.
b11 | simples | countryside | two | AUT | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (15/19 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | PENDENTE | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | REFAZER (a etapa anterior mudou) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh karansebes
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh karansebes
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local karansebes <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 6. Estilo e enquadramento

