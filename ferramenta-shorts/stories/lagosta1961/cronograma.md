# CRONOGRAMA - Guerras Inusitadas EP 11 - A Guerra da Lagosta

Gerado em 24/11 13:01 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_cidade | two | BRA, FRA | - | lobster | - | A França e o Brasil quase entraram em guerra por causa de uma lagosta.
b1 | simples | harbor | reveal | PES, PES | 8 | boat | - | Era mil novecentos e sessenta e um, e barcos franceses pescavam lagost
b2 | chave | harbor | crowd | BRA, PES | 12 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | O Brasil dizia que a lagosta anda no fundo do mar, e por isso era bras
b3 | simples | loc_campo | two | FRA, FRA | - | - | - | A França respondia que a lagosta nada, e por isso era de quem pescasse
b4 | simples | interior pedra | group | FRA, MAR, MAR | - | ship | - | A França mandou um navio de guerra para proteger os pescadores dela.
b5 | chave | harbor | crowd | MAR, MAR | 20 | navios de guerra ao fundo, no tamanho real, ship, airplane | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que o Brasil não recuou. Mandou navios e aviões para a costa,
b6 | simples | harbor | two | MAR, MAR | - | - | - | Marinheiros dos dois lados se encararam no mar.
b7 | simples | interior madeira | two | FRA, BRA | - | - | - | Mas o tiro nunca veio. Os dois governos se reuniram e conversaram, em 
b8 | simples | harbor | reveal | PES, FRA | - | navio em movimento | - | Depois, chegaram a um acordo: alguns barcos franceses podiam pescar, c
b9 | simples | interior pedra | close | BRA | - | lobster | - | No fim, ninguém perguntou para a lagosta de que lado ela queria ficar.
b10 | simples | interior pedra | two | BRA | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/16 itens) | PENDENTE | python3 pesquisar.py lagosta1961
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh lagosta1961
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh lagosta1961
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local lagosta1961 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

