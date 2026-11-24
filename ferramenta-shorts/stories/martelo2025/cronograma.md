# CRONOGRAMA - Poder e Fama EP 23 - O Martelo da Meia-Noite

Gerado em 24/11 21:01 | 13 cenas | metricas: acoes_encenadas 85%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_pista | two | GEN | - | bunker_bomb | - | Uma bomba gigante, feita para furar montanhas, foi usada de verdade pe
b1 | transicao | loc_campo | reveal | POV, POV | 6 | - | - | Foi em junho de dois mil e vinte e cinco, contra usinas nucleares do I
b2 | transicao | mountain | wide | GEN | - | mountain_bunker | - | A principal, Fordow, fica de oitenta a noventa metros de profundidade,
b3 | simples | loc_pista | two | GEN, PIL | - | b2_air, bunker_bomb, airplane | - | Só uma bomba chegava lá, a antibunker, com treze toneladas. E só um av
b4 | simples | interior pedra | two | GEN, PIL | - | - | - | A missão se chamou Martelo da Meia-Noite.
b5 | simples | loc_pista | wide | PIL | - | b2_air | - | Sete bombardeiros invisíveis decolaram do Missouri e voaram dezoito ho
b6 | simples | harbor | wide | PIL | - | b2_air | - | Para despistar, outros aviões foram mandados na direção do Pacífico.
b7 | chave | mountain | orbit | PIL | - | b2_air, mountain_bunker | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que, de madrugada, catorze bombas caíram, doze delas sobre Fo
b8 | transicao | harbor | wide | PIL | - | submarino_ww2 | - | Um submarino ainda lançou mísseis contra uma terceira usina.
b9 | simples | loc_pista | two | PIL, GEN | - | house_small, picket_fence, tree_oak, airplane | - | Os bombardeiros voltaram para casa.
b10 | simples | interior pedra | two | GEN, POV | - | - | - | Os Estados Unidos disseram que as usinas foram destruídas.
b11 | simples | hall | two | POV, POV | - | - | - | Mas até hoje ninguém concorda sobre o tamanho do estrago.
b12 | simples | hall | close | GEN | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (7/14 itens) | PENDENTE | python3 pesquisar.py martelo2025
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 13) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh martelo2025
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh martelo2025
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local martelo2025 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

