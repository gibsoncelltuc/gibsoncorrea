# CRONOGRAMA - Poder e Fama EP 23 - O Martelo da Meia-Noite

Gerado em 25/11 17:03 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_pista | two | GEN | - | bunker_bomb | - | Uma bomba feita para furar montanhas foi usada pela primeira vez.
b1 | simples | hall | two | POV, POV | - | - | - | E até hoje ninguém concorda sobre o estrago.
b2 | transicao | loc_campo | reveal | POV, POV | 6 | - | - | Foi em junho de 2025, contra usinas nucleares do Irã.
b3 | chave | loc_montanha | orbit | GEN | - | mountain_bunker | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | A principal, Fordow, fica a quase noventa metros, dentro de uma montan
b4 | explicativa | loc_pista | two | sem personagem | - | - | corpo: kit/bunker_bomb (parado); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; som:  | Só a bomba antibunker, de treze toneladas, chega lá.
b5 | explicativa | loc_estudio | two | sem personagem | - | - | corpo: kit/b2_air (parado); emissao: velocidade; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em cada | Sete aviões invisíveis B-2 voaram dezoito horas até o alvo.
b6 | explicativa | loc_estudio | two | sem personagem | - | - | corpo: kit/b2_air (parado); emissao: velocidade; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em cada | Para despistar, outros aviões foram mandados na direção do Pacífico.
b7 | explicativa | loc_estudio | two | sem personagem | - | - | corpo: kit/mountain_bunker (parado); emissao: fogo, onda; luz: estudio; camera: 2 enquadramentos sem corte seco; som: so | Acontece que, de madrugada, catorze bombas caíram, doze sobre Fordow.
b8 | simples | interior pedra | two | GEN, POV | - | - | - | Os Estados Unidos disseram que as usinas foram destruídas.
b9 | simples | loc_pista | wide | GEN | - | bunker_bomb | - | O Irã discorda. E a montanha guarda o segredo.

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (15/16 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | PENDENTE | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh martelo2025
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh martelo2025
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local martelo2025 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 7. Gates

