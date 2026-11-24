# CRONOGRAMA - Guerras Inusitadas EP 06 - A Guerra do Porco

Gerado em 24/11 01:41 | 8 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | countryside | two | FAZ, IRL | - | haybale, picket_fence | - | Dois países quase entraram em guerra por causa de um porco.
b1 | transicao | countryside | reveal | FAZ, IRL | - | - | - | Foi na ilha de San Juan, entre os Estados Unidos e o Canadá.
b2 | simples | loc_campo | two | FAZ | - | barn, batatas, flowerbed, haybale, picket_fence, scarecrow | - | Um fazendeiro americano achou o porco comendo suas batatas, pegou a es
b3 | simples | loc_campo | two | IRL, FAZ | - | picket_fence | - | O dono, um irlandês da companhia inglesa, exigiu cem dólares. Ninguém 
b4 | chave | harbor | crowd | ING, AME | 48 | cannon, navios de guerra ao fundo, no tamanho real | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Os Estados Unidos mandaram soldados, e a Inglaterra respondeu com navi
b5 | simples | interior madeira | two | ALM, ING | - | - | - | O almirante inglês se recusou a atacar por causa de um porco.
b6 | simples | loc_campo | close | FAZ | - | cross, picket_fence | - | A única baixa da guerra foi o porco.
b7 | simples | countryside | close | FAZ | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (17/17 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | PENDENTE | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh porco_piloto
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh porco_piloto
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local porco_piloto <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 6. Estilo e enquadramento

