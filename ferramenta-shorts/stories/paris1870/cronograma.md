# CRONOGRAMA - O Cardápio do Zoológico

Gerado em 24/11 03:55 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | interior madeira | two | PAR, PAR | - | - | - | Paris já serviu elefante no jantar. Era mil oitocentos e setenta, a Pr
b1 | simples | street | reveal | PAR, PAR | 8 | marco_notredame | - | Primeiro, os parisienses comeram os cavalos. Depois, os cachorros e os
b2 | simples | street | two | PAR, CHF | - | barrel | - | Depois, os roedores, que viraram um prato chique.
b3 | chave | street | crowd | PAR, PAR | 6 | house_two, marco_notredame, lamppost | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Quando acabou tudo, olharam para o zoológico da cidade.
b4 | simples | arctic | close | BUT | - | - | - | O açougueiro comprou dois elefantes, Castor e Pólux, e vendeu a carne 
b5 | simples | interior loja | two | CHF, PAR | - | - | - | No Natal, o restaurante Voisin serviu consomê de elefante, ensopado de
b6 | chave | arctic | orbit | PAR | 12 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Tinha até gato servido com roedores em volta.
b7 | simples | arctic | wide | PAR, PAR | 6 | balloon, balloon_air | - | Para mandar notícias, os parisienses usavam balões e pombos-correio.
b8 | simples | arctic | close | PAR | - | - | - | O cerco acabou em janeiro de mil oitocentos e setenta e um, e Paris se
b9 | simples | street | close | PAR | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/15 itens) | PENDENTE | python3 pesquisar.py paris1870
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 4) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh paris1870
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh paris1870
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local paris1870 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

