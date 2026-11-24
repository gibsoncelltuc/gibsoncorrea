# CRONOGRAMA - Guerras Inusitadas EP 18 - A Guerra do Cão Fugitivo

Gerado em 24/11 08:45 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_campo | two | GRE, BUL | - | dog_sit | - | Um cachorro fugiu, e por causa dele dois países entraram em guerra, e 
b1 | simples | loc_montanha | reveal | GRE, BUL | 48 | - | - | Em mil novecentos e vinte e cinco, a fronteira entre a Grécia e a Bulg
b2 | simples | loc_campo | track | GRE, GRE | - | - | - | Um soldado grego estava de guarda quando o cachorro dele fugiu para o 
b3 | simples | loc_campo | track | GRE, GRE | - | - | - | O soldado correu atrás do cachorro, e atravessou a fronteira sem pensa
b4 | chave | loc_montanha | group | BUL, GRE | 10 | dog_sit | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Do outro lado, uma sentinela búlgara viu um estranho armado, e atirou.
b5 | simples | loc_montanha | low | GRE, GRE | - | - | - | Acontece que o soldado morreu, e a Grécia deu um ultimato furioso à Bu
b6 | chave | loc_montanha | orbit | GRE, BUL | 48 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Poucos dias depois, o exército grego invadiu a Bulgária e ocupou a reg
b7 | simples | interior madeira | two | DIP, PRE | - | - | - | A Bulgária pediu ajuda à Liga das Nações, a antecessora da ONU.
b8 | simples | interior pedra | two | PRE, DIP | - | - | - | A Liga mandou a Grécia parar, retirar as tropas e pagar uma indenizaçã
b9 | simples | loc_campo | close | GRE | - | dog_sit | - | A Grécia obedeceu, e ninguém sabe o que aconteceu com o cachorro.
b10 | simples | loc_campo | two | GRE | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/6 itens) | PENDENTE | python3 pesquisar.py cachorro1925
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 2) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh cachorro1925
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh cachorro1925
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local cachorro1925 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

