# CRONOGRAMA - Guerras Inusitadas EP 26 - A Guerra do Cachorro Perdido

Gerado em 25/11 16:56 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | mountain | two | GRE | - | dog_sit | - | Ninguém te conta: um cachorro fugido quase começou uma guerra.
b1 | simples | loc_campo | close | GRE | - | dog_sit | - | E até hoje ninguém sabe o que aconteceu com ele.
b2 | chave | mountain | wide | GRE, BUL | 48 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em 1925, na fronteira entre a Grécia e a Bulgária.
b3 | simples | loc_campo | two | GRE | - | - | - | Dizem que o cachorro de um soldado grego cruzou a fronteira.
b4 | simples | loc_campo | track | GRE | - | - | - | O soldado correu atrás e cruzou a fronteira também.
b5 | simples | interior madeira | close | BUL | - | - | - | Uma sentinela búlgara viu o soldado e atirou.
b6 | simples | loc_montanha | close | OFF | - | - | - | A Grécia ficou furiosa e deu um ultimato.
b7 | chave | loc_montanha | crowd | GRE, GRE, GRE | 48 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Dias depois, o exército grego invadiu a Bulgária.
b8 | simples | interior pedra | two | BUL, BUL | - | - | - | A Bulgária apelou para a Liga das Nações.
b9 | simples | interior pedra | group | OFF, GRE | - | - | - | A Grécia teve que recuar e pagar uma indenização.
b10 | simples | mountain | two | GRE | - | dog_sit | - | Tudo por causa de um cachorro.

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/16 itens) | PENDENTE | python3 pesquisar.py petrich1925
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh petrich1925
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh petrich1925
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local petrich1925 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 4. Travas do roteiro

