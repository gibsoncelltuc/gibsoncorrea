# CRONOGRAMA - Poder e Fama EP 05 - Cem Dias ou de Graça

Gerado em 24/11 23:06 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | interior loja | two | MUS | - | megapack | - | Um homem apostou cinquenta milhões de dólares numa conversa no Twitter
b1 | simples | loc_campo | wide | MUS | - | megapack | - | Em dois mil e dezessete, Elon Musk prometeu baterias gigantes para a A
b2 | chave | loc_cidade | wide | MUS | 30 | megapack | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Os jornais calcularam que ele podia perder mais de cinquenta milhões d
b3 | simples | interior pedra | two | MUS, JOR | - | megapack | - | O contrato foi fechado no fim de setembro, e o prazo de cem dias começ
b4 | chave | loc_campo | wide | MUS | - | megapack, picket_fence | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que a bateria ficou pronta em cerca de cinquenta e cinco dias
b5 | explicativa | loc_campo | two | sem personagem | - | megapack | corpo: kit/megapack (gira); emissao: brilho; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em cada ent | A imprensa chamou de a maior bateria do mundo, com cem megawatts de po
b6 | simples | interior loja | two | CAN, MUS | - | - | - | O empresário que fez o desafio teve que admitir: Musk cumpriu.
b7 | simples | loc_campo | two | CAN | - | megapack | - | Ou seja, uma conversa no Twitter virou uma obra de cinquenta e cinco d
b8 | simples | interior madeira | two | MUS, JOR | - | megapack, phone | - | E tudo começou com uma resposta curta, escrita no celular.
b9 | simples | loc_cidade | group | MUS, CAN | - | megapack | - | Moral da história: antes de apostar cinquenta milhões num prazo, leia 
b10 | simples | loc_cidade | close | MUS | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/13 itens) | PENDENTE | python3 pesquisar.py bateria2017
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh bateria2017
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh bateria2017
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local bateria2017 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

