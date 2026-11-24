# CRONOGRAMA - Guerras Inusitadas EP 16 - A Guerra da Melancia

Gerado em 24/11 04:17 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | street | two | VIA, VEN | - | melon | - | Uma fatia de melancia sem pagar começou uma briga entre o Panamá e os 
b1 | simples | loc_campo | reveal | VIA, VIA | 8 | locomotive | - | Em mil oitocentos e cinquenta e seis, viajantes cruzavam o Panamá de t
b2 | simples | jungle | two | VIA, VEN | - | melon, stall | - | Um deles parou numa barraca, comeu uma fatia de melancia e foi embora 
b3 | simples | street | two | VEN, VIA | - | shop, stall | - | O vendedor cobrou a fatia, e o viajante só riu.
b4 | simples | street | group | VIA, VEN | - | pistol | - | Irritado, o viajante sacou uma arma, e a confusão começou ali mesmo, n
b5 | chave | street | crowd | VEN, VIA | 20 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em poucos minutos, a rua virou uma briga enorme entre moradores e viaj
b6 | simples | street | group | sem personagem | - | house_two, lamppost | - | Os viajantes se trancaram na estação de trem, e a polícia da cidade en
b7 | simples | interior madeira | two | PRE, MOR | - | - | - | Acontece que mais de quinze pessoas morreram naquele dia, e a cidade f
b8 | chave | loc_campo | orbit | SOL, SOL | 48 | locomotive | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Na época, o Panamá fazia parte da Colômbia, e foi a Colômbia que acabo
b9 | simples | jungle | close | VEN | - | melon | - | Tudo isso por uma fatia de melancia que custava poucos centavos.
b10 | simples | jungle | two | VIA | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/15 itens) | PENDENTE | python3 pesquisar.py melancia1856
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh melancia1856
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh melancia1856
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local melancia1856 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

