# CRONOGRAMA - E Se EP 01 - E Se Todo Mundo Pulasse ao Mesmo Tempo?

Gerado em 25/11 04:16 | 12 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 0%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_campo | two | PRO, POV | - | globe | - | E se todas as pessoas do planeta pulassem exatamente no mesmo segundo?
b1 | simples | loc_campo | reveal | POV, POV | 6 | - | - | Somos mais de oito bilhões de pessoas, espalhadas por todos os contine
b2 | simples | interior pedra | two | PRO, POV | - | - | - | Juntas, elas pesam mais de quinhentos milhões de toneladas. Parece mui
b3 | chave | loc_montanha | crowd | POV, POV, POV | 30 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Então todo mundo conta até três, e pula ao mesmo tempo!
b4 | simples | loc_montanha | close | PRO | - | globe | - | Acontece que a Terra pesa trilhões de vezes mais que toda a humanidade
b5 | explicativa | loc_montanha | two | PRO, POV | - | globe | - | Ela se mexeria menos que a largura de um átomo. Nenhum instrumento con
b6 | chave | loc_deserto | orbit | POV, POV, POV | 22 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | O que daria para notar seria o barulho. Bilhões de pés batendo no chão
b7 | simples | loc_deserto | group | POV, PRO | 5 | - | - | E se, para facilitar, todo mundo se juntasse num lugar só, para pular 
b8 | simples | interior madeira | two | PRO, POV | - | - | - | Aí seria o caos: bilhões de pessoas presas no mesmo lugar, sem estrada
b9 | simples | interior madeira | group | POV, POV | - | - | - | Ou seja: pular junto é fácil. Difícil seria a volta.
b10 | simples | loc_montanha | close | PRO | - | globe | - | A Terra não liga para o nosso pulo. Mas pode pular aí: ninguém vai sen
b11 | simples | loc_campo | close | PRO | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/4 itens) | PENDENTE | python3 pesquisar.py ese_pulo
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 4) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh ese_pulo
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh ese_pulo
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local ese_pulo <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

