# CRONOGRAMA - Guerras Inusitadas EP 01 - A Batalha de Karánsebes

Gerado em 25/11 16:47 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | chave | countryside | crowd | AUT, AUT, AUT, AUT | 48 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Um exército inteiro perdeu uma batalha contra si mesmo.
b1 | simples | countryside | close | TUR, TUR | - | - | - | E o inimigo venceu sem disparar um único tiro.
b2 | simples | countryside | orbit | AUT, HUS, AUT, OFF | 32 | - | - | Em 1788, o exército austríaco tinha soldados de vários países.
b3 | chave | countryside | track | HUS, HUS | 6 | lantern | corpo: cavaleiro galopando; emissao: poeira/clarao do tiro; luz: cena; camera: camera acompanha; som: galope | Numa noite, os hussardos foram na frente procurar o inimigo.
b4 | simples | countryside | two | HUS, LOC | 6 | barrel, barrel_r | - | Acharam moradores vendendo aguardente. Compraram tudo e beberam.
b5 | simples | countryside | group | AUT, HUS, AUT | 6 | - | - | A infantaria quis um gole. Eles negaram, e alguém atirou.
b6 | simples | countryside | close | HUS | 12 | - | - | No escuro, alguém gritou: Turcos! Turcos!
b7 | chave | countryside | orbit | AUT, AUT, HUS | 48 | house_small, picket_fence, tree_oak | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Ninguém entendia a língua do vizinho. Todos atiraram em todos.
b8 | simples | countryside | group | OFF | 6 | cannon | - | Até os canhões dispararam contra o próprio exército.
b9 | simples | countryside | two | TUR, TUR | 5 | campfire, tent | - | Dois dias depois, os turcos acharam o acampamento abandonado.
b10 | chave | countryside | wide | AUT, AUT, AUT, AUT | 48 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Venceram sem um tiro. O exército perdeu para si mesmo.

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (13/18 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh karansebes
10 | Render | todos os quadros renderizados nesta versao das folhas | REFAZER (a etapa anterior mudou) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | REFAZER (a etapa anterior mudou) | ./conferir.sh karansebes
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local karansebes <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | REFAZER (a etapa anterior mudou) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

