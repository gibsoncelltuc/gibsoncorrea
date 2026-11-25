# CRONOGRAMA - Guerras Inusitadas EP 24 - O Cardápio do Zoológico

Gerado em 25/11 17:21 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | street | wide | PAR, PAR | - | bife_elefante, marco_notredame, Table_Large | - | Paris já serviu elefante no jantar de Natal.
b1 | simples | interior loja | two | CHF, PAR | - | bife_elefante | - | E no cardápio tinha até canguru e lobo.
b2 | simples | street | reveal | PAR, PAR | 6 | marco_notredame | - | Em 1870, a Prússia cercou Paris, e a comida acabou.
b3 | simples | street | two | PAR, PAR | - | - | - | Primeiro comeram os cavalos. Depois, cachorros e gatos.
b4 | chave | street | wide | PAR, CHF | - | barrel, panela, rato | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Depois os roedores, que viraram prato chique.
b5 | simples | street | wide | PAR, PAR | 6 | marco_notredame | - | Quando acabou tudo, olharam para o zoológico.
b6 | chave | street | orbit | BUT, PAR | 12 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que um açougueiro comprou os elefantes Castor e Pólux.
b7 | simples | interior loja | two | CHF, PAR | - | bife_elefante | - | No Natal, um restaurante serviu consomê de elefante.
b8 | simples | street | group | CHF, PAR | - | bife_elefante, marco_notredame | - | Só os ricos podiam pagar esse luxo.
b9 | simples | street | two | PAR, PAR | 10 | marco_notredame | - | O povo fazia fila no frio por comida racionada.
b10 | simples | street | wide | PAR, PAR | - | bife_elefante, marco_notredame, Table_Large | - | Na fome, até bicho de zoológico vira comida. Foi assim que...

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
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | PENDENTE | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh paris1870
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh paris1870
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local paris1870 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 8. Storyboard e grade de acoes

