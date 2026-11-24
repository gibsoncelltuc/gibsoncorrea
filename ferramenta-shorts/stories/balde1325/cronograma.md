# CRONOGRAMA - Guerras Inusitadas EP 04 - A Guerra do Balde

Gerado em 24/11 23:45 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | medieval | two | MOD, BOL | - | house_small, balde_madeira, picket_fence, tree_oak, bucket | - | Dois vizinhos italianos foram à guerra, e o prêmio do vencedor foi um 
b1 | simples | medieval | two | NOB, PAP | - | - | - | Módena e Bolonha disputavam a fronteira havia décadas.
b2 | simples | loc_campo | crowd | BOL, BOL | 18 | picket_fence | - | Em mil trezentos e vinte e cinco, Bolonha juntou cerca de trinta mil s
b3 | simples | loc_campo | two | MOD, MOD | 6 | - | - | Módena tinha menos de oito mil homens, e parecia perdida.
b4 | chave | loc_campo | crowd | MOD, BOL | 32 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que, ao pôr do sol de quinze de novembro, os modeneses atacar
b5 | simples | medieval | group | MOD, MOD | 8 | castle_tower, church, picket_fence | - | Morreram cerca de duas mil pessoas, e os modeneses chegaram aos muros 
b6 | simples | loc_campo | two | MOD, MOD | 8 | - | - | Em vez de invadir, fizeram uma festa lá fora para zombar dos derrotado
b7 | simples | medieval | two | MOD, MOD | - | castle_tower, balde_madeira, well, bucket | - | Na volta, levaram como troféu um balde de madeira, tirado de um poço p
b8 | simples | medieval | close | MOD | - | castle_tower, balde_madeira, bucket | - | O balde ficou guardado na torre Ghirlandina, em Módena, e virou símbol
b9 | simples | interior madeira | two | POV, POV | - | - | - | Séculos depois, um poeta transformou a história numa sátira famosa.
b10 | simples | interior madeira | close | MOD | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/13 itens) | PENDENTE | python3 pesquisar.py balde1325
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | BLOQUEADO (etapa anterior pendente) | modelar em blender/ (formas.py): kit/balde_madeira
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh balde1325
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh balde1325
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local balde1325 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

