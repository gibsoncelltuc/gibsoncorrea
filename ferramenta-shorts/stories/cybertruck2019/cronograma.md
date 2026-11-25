# CRONOGRAMA - Poder e Fama EP 11 - A Janela do Cybertruck

Gerado em 25/11 17:18 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | chave | hall | two | MUS | - | cybertruck | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Uma picape blindada teve as janelas rachadas ao vivo, no lançamento.
b1 | simples | hall | group | MUS, DSG | - | cybertruck, steel_ball | - | E mesmo assim, ela virou um sucesso de reservas.
b2 | transicao | hall | wide | MUS | - | cybertruck | - | Em 2019, na Califórnia, a Tesla apresentou o Cybertruck.
b3 | transicao | hall | wide | MUS | - | cybertruck | - | Musk garantiu que o vidro era super resistente.
b4 | simples | hall | two | DSG | - | cybertruck, steel_ball | - | O designer jogou uma esfera de aço na janela.
b5 | chave | hall | wide | MUS | 30 | cybertruck | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que o vidro rachou, ao vivo, na frente da plateia.
b6 | chave | hall | wide | DSG | - | cybertruck | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Ele tentou em outra janela. Também rachou.
b7 | simples | hall | two | MUS | - | cybertruck, phone, steel_ball | - | Musk disse que, nos testes, a esfera nem arranhava o vidro.
b8 | transicao | hall | orbit | MUS, DSG | - | globe | - | Mesmo assim, em poucos dias, vieram mais de 140 mil reservas.
b9 | simples | hall | wide | MUS | - | cybertruck | - | A janela quebrou. As reservas, não.

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (10/12 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | PENDENTE | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh cybertruck2019
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh cybertruck2019
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local cybertruck2019 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 8. Storyboard e grade de acoes

