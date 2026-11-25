# CRONOGRAMA - Guerras Inusitadas EP 24 - O Cardápio do Zoológico

Gerado em 25/11 12:24 | 12 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | street | wide | PAR, PAR | - | bife_elefante, marco_notredame, Table_Large | - | Paris já serviu elefante no jantar.
b1 | simples | street | reveal | PAR, PAR | 6 | house_two, marco_notredame, lamppost | - | Era mil oitocentos e setenta. A Prússia cercou a cidade, e a comida ac
b2 | simples | street | two | PAR, PAR | - | - | - | Primeiro, os parisienses comeram os cavalos. Depois, os cachorros e os
b3 | simples | street | group | PAR, CHF | - | barrel, panela, rato | - | Depois, os roedores, que viraram um prato chique.
b4 | chave | arctic | crowd | PAR, PAR | 6 | house_two, lamppost | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Quando acabou tudo, olharam para o zoológico da cidade.
b5 | simples | arctic | two | BUT, PAR | - | - | - | O açougueiro comprou dois elefantes, Castor e Pólux, e vendeu a carne 
b6 | simples | interior loja | two | CHF, PAR | - | bife_elefante | - | No Natal, o restaurante Voisin serviu consomê de elefante, ensopado de
b7 | chave | street | orbit | CHF, PAR | 6 | bife_elefante, marco_notredame | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que carne de elefante custava uma fortuna. Só os ricos comiam
b8 | simples | street | wide | PAR, PAR | 30 | marco_notredame | - | Enquanto isso, o povo fazia fila no frio, com comida racionada.
b9 | simples | street | two | PAR | - | balloon_air, marco_notredame | - | Para mandar notícias, soltavam balões por cima do cerco.
b10 | simples | street | group | PAR, PAR | - | marco_notredame, panela | - | Em janeiro de mil oitocentos e setenta e um, Paris se rendeu. De barri
b11 | simples | street | close | PAR | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (10/15 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | FEITO | 
10 | Render | todos os quadros renderizados nesta versao das folhas | PENDENTE | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh paris1870
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local paris1870 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 10. Render

