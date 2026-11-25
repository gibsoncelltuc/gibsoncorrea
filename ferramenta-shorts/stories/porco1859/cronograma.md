# CRONOGRAMA - Guerras Inusitadas EP 06 - A Guerra do Porco

Gerado em 25/11 23:37 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | countryside | wide | FAZ | - | haybale, picket_fence | - | Dois países quase foram à guerra por causa de um porco.
b1 | transicao | countryside | wide | FAZ | - | cross, picket_fence | - | E a única baixa da guerra foi ele.
b2 | simples | harbor | two | FAZ, IRL | - | - | - | A ilha de San Juan não tinha dono definido.
b3 | simples | countryside | two | FAZ | - | barn, batatas, flowerbed, haybale, picket_fence, scarecrow, wheelbarrow | - | Um fazendeiro americano viu um porco comendo suas batatas.
b4 | simples | countryside | two | FAZ | - | house_small, haybale, picket_fence, tree_oak | - | Ele atirou. O porco era de um vizinho inglês.
b5 | simples | countryside | two | FAZ, IRL | - | haybale, picket_fence, wheelbarrow | - | Ofereceu dez dólares. O dono exigiu cem.
b6 | simples | harbor | group | AME, AME, FAZ | 16 | - | - | Os americanos mandaram soldados para a ilha.
b7 | chave | harbor | crowd | ING, AME | 48 | navios de guerra ao fundo, no tamanho real | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | A Inglaterra respondeu com navios de guerra.
b8 | simples | harbor | two | ALM, ING | - | - | - | Acontece que o almirante inglês se recusou a atacar.
b9 | simples | interior pedra | group | ING, AME, ING | - | - | - | Os soldados acabaram fazendo festas juntos.
b10 | simples | countryside | wide | FAZ | - | haybale, picket_fence | - | Ninguém deu um tiro, só no porco. E foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (14/17 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh porco1859
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh porco1859
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local porco1859 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

