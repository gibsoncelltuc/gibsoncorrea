# CRONOGRAMA - Poder e Fama EP 11 - A Janela do Cybertruck

Gerado em 24/11 22:42 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | hall | two | MUS | - | cybertruck | - | Uma picape blindada teve as janelas quebradas ao vivo, no próprio lanç
b1 | simples | hall | wide | MUS | - | cybertruck | - | Foi em novembro de dois mil e dezenove, na Califórnia. A Tesla apresen
b2 | simples | hall | wide | DSG | - | cybertruck, steel_ball | - | Para provar, o designer Franz von Holzhausen jogou uma esfera de aço n
b3 | chave | hall | wide | MUS | 30 | cybertruck | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que o vidro rachou, ao vivo, na frente de toda a plateia.
b4 | chave | hall | wide | DSG | - | ball, cybertruck | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Ele tentou de novo, em outra janela, e ela também rachou. Musk brincou
b5 | simples | hall | two | MUS | - | cybertruck, steel_ball | - | Depois, Musk explicou na internet que, nos ensaios, a mesma esfera tin
b6 | simples | hall | orbit | MUS, DSG | 30 | globe | - | A plateia riu, a internet também, e a cena deu o que falar no mundo in
b7 | simples | hall | group | MUS, DSG | 8 | cybertruck, globe | - | Mesmo assim, poucos dias depois, Musk anunciou mais de cento e quarent
b8 | simples | hall | two | MUS, DSG | 10 | cybertruck, steel_ball | - | Uma picape, uma esfera de aço e uma janela que não aguentou: um lançam
b9 | simples | hall | close | MUS | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/12 itens) | PENDENTE | python3 pesquisar.py cybertruck2019
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh cybertruck2019
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh cybertruck2019
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local cybertruck2019 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

