# CRONOGRAMA - Guerras Inusitadas EP 11 - A Guerra da Lagosta

Gerado em 25/11 16:55 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | harbor | two | BRA | - | crate, lobster | - | Você acha que guerra é por petróleo? O Brasil quase brigou por lagosta
b1 | simples | harbor | close | BRA | - | crate, lobster | - | E a briga dependia de uma pergunta: a lagosta anda ou nada?
b2 | transicao | harbor | wide | PES | - | boat, fishing_net | - | Em 1961, barcos franceses pescavam lagosta na costa de Pernambuco.
b3 | explicativa | loc_estudio | two | sem personagem | - | - | corpo: kit/lobster (parado); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som  | O Brasil dizia: lagosta anda no fundo do mar, é nossa.
b4 | explicativa | loc_estudio | two | sem personagem | - | - | corpo: kit/lobster (sobe); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em | A França respondia: lagosta nada, é de quem pescar.
b5 | transicao | harbor | wide | MFR | - | navio_destroier, navios de guerra ao fundo, no tamanho real | - | A França mandou um navio de guerra para a costa.
b6 | chave | harbor | orbit | MAR | - | navios de guerra ao fundo, no tamanho real, ship, airplane | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que o Brasil não recuou e mandou navios e aviões.
b7 | simples | interior pedra | two | FRA, BRA | - | - | - | Mas o tiro nunca veio. Os dois governos fizeram um acordo.
b8 | chave | harbor | wide | PES, FRA | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | No fim, alguns barcos franceses puderam pescar, com limite.
b9 | simples | harbor | two | BRA | - | crate, lobster | - | Petróleo, ouro, terra? Aqui, o motivo foi uma lagosta.

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (18/19 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | PENDENTE | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh lagosta1961
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh lagosta1961
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local lagosta1961 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 8. Storyboard e grade de acoes

