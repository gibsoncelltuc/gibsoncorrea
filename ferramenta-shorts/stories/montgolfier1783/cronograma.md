# CRONOGRAMA - Curiosidade e Ciência EP 18 - Os Primeiros Passageiros do Céu

Gerado em 24/11 22:52 | 12 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_campo | two | JOS | - | balloon, marco_versalhes | - | Os primeiros passageiros de um balão não foram pessoas. Foram uma ovel
b1 | transicao | street | reveal | POV, POV | 6 | marco_versalhes | - | Era mil setecentos e oitenta e três, na França.
b2 | simples | interior madeira | two | JOS, ETI | - | campfire | - | Os irmãos Montgolfier, donos de uma fábrica de papel, viram que a fuma
b3 | simples | interior madeira | two | ETI | - | balloon | - | Então fizeram um balão gigante de pano e papel, cheio de ar quente.
b4 | simples | interior madeira | two | NOB, ETI | - | - | - | Só que ninguém sabia se dava para respirar lá em cima.
b5 | simples | loc_campo | group | JOS | - | balloon, marco_versalhes | - | A solução: mandar bichos na frente. Uma ovelha, um pato e um galo entr
b6 | chave | street | crowd | REI | 30 | balloon, marco_versalhes | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em Versalhes, o rei Luís dezesseis e Maria Antonieta assistiram, no me
b7 | simples | loc_campo | wide | POV | - | balloon, balloon_air, marco_versalhes | - | Acontece que o balão levantou voo de verdade, com os bichos dentro.
b8 | chave | loc_campo | wide | ETI | - | balloon, marco_versalhes, bush, tree_oak, tree_pine | corpo: desce do ar com o jato embaixo e pousa nas rodas com onda de ar e poeira; emissao: VFX 3D preso no objeto (jato/p | Oito minutos depois, ele desceu num bosque a três quilômetros dali, e 
b9 | chave | street | orbit | POV | - | balloon, balloon_air, marco_versalhes | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Dois meses depois, outro balão levou dois homens por cima de Paris.
b10 | simples | loc_montanha | two | ETI | - | balloon, marco_versalhes | - | Tudo graças a três bichos corajosos.
b11 | simples | loc_montanha | close | JOS | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/14 itens) | PENDENTE | python3 pesquisar.py montgolfier1783
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | REFAZER (a etapa anterior mudou) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh montgolfier1783
10 | Render | todos os quadros renderizados nesta versao das folhas | REFAZER (a etapa anterior mudou) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | REFAZER (a etapa anterior mudou) | ./conferir.sh montgolfier1783
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local montgolfier1783 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

