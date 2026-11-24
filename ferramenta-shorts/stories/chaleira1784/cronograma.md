# CRONOGRAMA - Guerras Inusitadas EP 10 - A Guerra da Chaleira

Gerado em 24/11 17:31 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_campo | two | COZ, HOL | - | kettle | - | Uma guerra inteira teve um único tiro, e ele acertou uma chaleira de s
b1 | simples | harbor | wide | MAR, MAR | - | navio_fragata, navios de guerra ao fundo, no tamanho real | - | Foi em mil setecentos e oitenta e quatro. A Holanda mantinha o rio Esc
b2 | simples | interior pedra | two | IMP, GEN | - | - | - | O imperador José Segundo, da Áustria, queria o rio aberto para os navi
b3 | simples | harbor | wide | IMP | - | navio_fragata, navios de guerra ao fundo, no tamanho real | - | Convencido de que os holandeses não reagiriam, ele mandou três navios 
b4 | simples | harbor | wide | IMP | - | navio_fragata, flagpole | - | O maior levava a bandeira do imperador e seguia na frente.
b5 | simples | harbor | two | MAR, MAR | - | cannon, navio_fragata | - | Acontece que o navio de guerra holandês Dolfijn estava esperando, e di
b6 | chave | interior madeira | two | IMP, COZ | - | kettle | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | A bala acertou e destruiu uma chaleira de sopa no convés do navio do i
b7 | chave | harbor | wide | GEN | - | navio_fragata, navios de guerra ao fundo, no tamanho real | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | O navio austríaco se rendeu na hora, sem trocar nem um tiro a mais.
b8 | simples | interior pedra | two | IMP, HOL | - | - | - | Depois, a França mediou a paz, em mil setecentos e oitenta e cinco. O 
b9 | simples | interior madeira | two | COZ | - | kettle | - | O único prejuízo do dia foi o almoço.
b10 | simples | interior madeira | close | COZ | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (9/16 itens) | PENDENTE | python3 pesquisar.py chaleira1784
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | REFAZER (a etapa anterior mudou) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | REFAZER (a etapa anterior mudou) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | REFAZER (a etapa anterior mudou) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | REFAZER (a etapa anterior mudou) | ./aprovar_storyboard.sh chaleira1784
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh chaleira1784
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local chaleira1784 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

