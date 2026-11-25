# CRONOGRAMA - Curiosidade e Ciência EP 12 - O Astrônomo do Nariz de Metal

Gerado em 25/11 19:43 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | medieval | two | TYC, PAR | - | brass_nose | - | Um gênio da astronomia perdeu o nariz numa briga por matemática.
b1 | simples | loc_deserto | two | TYC | - | brass_nose | - | E passou o resto da vida com um nariz de metal.
b2 | chave | loc_campo | wide | TYC, POV | 6 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em 1566, Tycho Brahe estudava na Alemanha.
b3 | simples | interior madeira | group | TYC, PAR, POV | - | - | - | Numa festa, discutiu com um primo sobre matemática.
b4 | simples | loc_deserto | two | TYC, PAR | - | - | - | Dias depois, os dois resolveram tudo num duelo de espadas.
b5 | simples | loc_montanha | two | PAR, TYC | - | brass_nose | - | Acontece que o primo cortou fora um pedaço do nariz de Tycho.
b6 | chave | harbor | orbit | REI, TYC | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Depois, o rei lhe deu uma ilha só para estudar o céu.
b7 | simples | loc_campo | orbit | TYC | - | marco_uraniborg, tower | - | Mediu mais de mil estrelas, sem telescópio.
b8 | simples | interior pedra | two | TYC, KEP | - | - | - | Os dados dele ajudaram o astrônomo Kepler.
b9 | simples | loc_campo | two | TYC, PAR | - | brass_nose | - | Cabeça nas estrelas e nariz de metal. Tudo porque...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (9/13 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | PENDENTE | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh tycho1566
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh tycho1566
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local tycho1566 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 8. Storyboard e grade de acoes

