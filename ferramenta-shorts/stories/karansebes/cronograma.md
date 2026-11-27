# CRONOGRAMA - Guerras Inusitadas EP 01 - A Batalha de Karánsebes

Gerado em 24/11 01:52 | 12 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | chave | countryside | crowd | AUT, AUT, AUT, AUT | 48 | marco_viena | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Um exército inteiro conseguiu perder uma batalha contra si mesmo.
b1 | simples | countryside | orbit | AUT, HUS, AUT, OFF | 32 | marco_viena | - | Era o exército austríaco, marchando contra os turcos, com soldados de 
b2 | simples | countryside | track | HUS, HUS | - | marco_viena, lantern | - | Numa noite, os hussardos foram na frente procurar o inimigo.
b3 | simples | countryside | two | HUS, LOC | - | barrel, barrel_r, marco_viena | - | Não acharam turco nenhum. Acharam moradores vendendo aguardente.
b4 | simples | countryside | group | HUS, HUS | - | barrel, marco_viena, lantern | - | Compraram tudo, beberam, e a festa começou.
b5 | simples | countryside | two | AUT, HUS, AUT | 5 | marco_viena | - | Aí chegou a infantaria, querendo a parte dela. Os hussardos não quiser
b6 | chave | countryside | orbit | HUS | 18 | campfire, marco_viena, tent | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | No escuro, alguém gritou: "Turcos! Turcos!" E o pânico tomou o acampam
b7 | chave | countryside | crowd | AUT, AUT, HUS | 48 | house_small, marco_viena, picket_fence, tree_oak | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que ninguém entendia a língua do vizinho. Todo mundo atirava 
b8 | simples | countryside | group | OFF, AUT | 5 | cannon, marco_viena | - | Um oficial mandou usar a artilharia, e os canhões dispararam contra o 
b9 | simples | countryside | two | TUR, TUR | 5 | barrel, crate, campfire, marco_viena, tent | - | Dois dias depois, os turcos chegaram de verdade, e acharam o acampamen
b10 | simples | countryside | close | TUR, TUR | - | marco_viena | - | Os turcos venceram sem dar um único tiro.
b11 | simples | countryside | two | AUT | - | marco_viena | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/19 itens) | PENDENTE | python3 pesquisar.py karansebes
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | REFAZER (a etapa anterior mudou) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | REFAZER (a etapa anterior mudou) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh karansebes
10 | Render | todos os quadros renderizados nesta versao das folhas | REFAZER (a etapa anterior mudou) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | REFAZER (a etapa anterior mudou) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh karansebes
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local karansebes <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

