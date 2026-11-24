# CRONOGRAMA - Guerras Inusitadas EP 24 - O Cardápio do Zoológico

Gerado em 24/11 08:38 | 12 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | interior madeira | two | PAR, PAR | - | panela | - | Paris já serviu elefante no jantar.
b1 | simples | street | reveal | PAR, PAR | 6 | house_two, marco_notredame, lamppost | - | Era mil oitocentos e setenta. A Prússia cercou a cidade, ninguém entra
b2 | simples | street | group | PAR, PAR | - | - | - | Primeiro, os parisienses comeram os cavalos. Depois, os cachorros e os
b3 | simples | street | two | PAR, CHF | - | barrel, panela | - | Depois, os roedores, que viraram um prato chique.
b4 | chave | arctic | crowd | PAR, PAR | 6 | house_two, lamppost | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Quando acabou tudo, olharam para o zoológico da cidade.
b5 | simples | arctic | close | BUT | - | - | - | O açougueiro comprou dois elefantes, Castor e Pólux, e vendeu a carne 
b6 | simples | interior loja | two | CHF, PAR | - | panela | - | No Natal, o restaurante Voisin serviu consomê de elefante, ensopado de
b7 | simples | arctic | group | PAR, PAR | - | balloon, balloon_air | - | Para mandar notícias, os parisienses usavam balões e pombos-correio.
b8 | chave | arctic | crowd | PAR, PAR | 18 | house_two, balloon, balloon_air, lamppost | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Um ministro chegou a fugir da cidade num balão, por cima das tropas in
b9 | simples | arctic | two | PAR, PAR | - | - | - | O cerco durou mais de quatro meses, em pleno inverno.
b10 | simples | arctic | close | PAR | - | panela | - | O cerco acabou em janeiro de mil oitocentos e setenta e um, e Paris se
b11 | simples | street | close | PAR | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (13/16 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | PENDENTE | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | REFAZER (a etapa anterior mudou) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh paris1870
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh paris1870
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local paris1870 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 6. Estilo e enquadramento

