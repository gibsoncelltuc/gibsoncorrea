# CRONOGRAMA - Curiosidade e Ciência EP 17 - A Borracha que Caiu no Fogão

Gerado em 25/11 19:39 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | interior madeira | two | GOO | - | gosma, stove | - | Uma gosma caiu no fogão de um inventor falido. E mudou o mundo.
b1 | simples | interior galpao | two | POV, POV | - | tires | - | E o nome dele está em pneus do mundo inteiro.
b2 | chave | street | wide | POV, POV | 6 | stove | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Nos Estados Unidos de 1830, a borracha virou moda.
b3 | explicativa | loc_estudio | two | sem personagem | - | - | corpo: kit/borracha (parado); emissao: fogo; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em cada ent | Mas derretia no calor e rachava no frio.
b4 | simples | interior madeira | two | GOO, CLA | - | - | - | Charles Goodyear gastou todo o dinheiro da família em testes.
b5 | simples | interior madeira | group | GUA, GOO | - | - | - | Fez tantas dívidas que foi parar na prisão.
b6 | simples | interior madeira | two | GOO | - | gosma, stove | - | Um dia, borracha com enxofre caiu no fogão quente.
b7 | simples | interior madeira | two | GOO | - | stove | - | Acontece que não derreteu. Ficou firme e elástica.
b8 | chave | street | orbit | POV, POV, CLA | - | bola_couro, borracha, stove, tires | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Era a borracha vulcanizada, hoje em pneus e sapatos.
b9 | simples | interior madeira | two | GOO | - | gosma, stove | - | A Goodyear ganhou o nome dele, sem ele saber. Tudo porque...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (17/17 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh goodyear1839
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh goodyear1839
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local goodyear1839 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

