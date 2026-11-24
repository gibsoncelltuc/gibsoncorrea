# CRONOGRAMA - Guerras Inusitadas EP 07 - A Guerra dos Bolos

Gerado em 24/11 03:01 | 12 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | street | two | CON, OFI | 5 | cake_table, marco_ulua | - | A França invadiu o México por causa de uma conta de confeitaria.
b1 | transicao | street | reveal | CON, OFI | 32 | shop, cake_table, marco_ulua, stall | - | Um confeiteiro francês tinha uma loja perto da Cidade do México, famos
b2 | simples | interior loja | group | OFI, OFI, CON | - | cake_table, Table_Large | - | Um dia, oficiais mexicanos entraram, comeram tudo o que havia, quebrar
b3 | simples | interior pedra | two | CON, REI | - | cake_table | - | O confeiteiro escreveu ao rei da França. "Quero sessenta mil pesos", p
b4 | simples | interior pedra | close | REI | - | - | - | O rei gostou da ideia, juntou outras queixas, e cobrou seiscentos mil.
b5 | simples | loc_campo | two | GEN, OFI | - | marco_ulua | - | O México riu do pedido, e não deu um centavo.
b6 | simples | harbor | wide | FRA, FRA | 32 | marco_ulua, navio em movimento, navios de guerra ao fundo, no tamanho real | - | Acontece que a França mandou mesmo. Navios de guerra chegaram, e fecha
b7 | chave | harbor | crowd | FRA, OFI | 48 | cannon, marco_ulua | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Os canhões franceses bombardearam a fortaleza de Veracruz, e os soldad
b8 | chave | street | orbit | GEN | 40 | cannon, marco_ulua | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Um general mexicano correu para o combate, e tombou, atingido por um t
b9 | simples | interior madeira | two | GEN, FRA | - | - | - | Meses depois, o México pagou os seiscentos mil pesos, e a França foi e
b10 | simples | interior madeira | close | CON | - | cake_table, coin | - | Nunca um doce custou tão caro, e o confeiteiro contou as moedas.
b11 | simples | street | close | CON | - | marco_ulua | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/8 itens) | PENDENTE | python3 pesquisar.py bolos1838
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 2) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh bolos1838
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh bolos1838
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local bolos1838 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

