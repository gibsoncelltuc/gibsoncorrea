# CRONOGRAMA - Curiosidade e Ciência EP 08 - Darwin e os Tentilhões

Gerado em 24/11 16:10 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | harbor | two | DAR, MAR | - | finch | - | Um cientista misturou as etiquetas de uns passarinhos, e isso explicou
b1 | simples | harbor | reveal | MAR, MAR | 8 | navio em movimento, navios de guerra ao fundo, no tamanho real | - | Em mil oitocentos e trinta e cinco, Charles Darwin chegou às ilhas Gal
b2 | simples | harbor | two | DAR, MAR | - | finch | - | Coletou bichos, plantas e uns passarinhos pequenos, de ilha em ilha. A
b3 | chave | harbor | crowd | DAR, MAR | 12 | finch | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Achou que eram aves bem diferentes, e nem anotou de que ilha vinha cad
b4 | simples | interior pedra | two | DAR, GOU | - | finch | - | Em Londres, o especialista John Gould revelou: eram todos tentilhões, 
b5 | simples | interior madeira | two | GOU, DAR | - | finch_long, finch_thick | - | A diferença estava no bico: uns grossos para quebrar sementes, outros 
b6 | chave | harbor | wide | DAR, GOU | 10 | finch, finch_long, finch_thick | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que, em cada ilha, o bico tinha mudado de acordo com a comida
b7 | simples | interior madeira | two | DAR, GOU | - | finch_thick | - | Os bichos com o bico certo sobreviviam melhor, e passavam isso para os
b8 | simples | interior madeira | group | DAR, GOU | - | - | - | Essa ideia virou a seleção natural, publicada em mil oitocentos e cinq
b9 | simples | loc_campo | close | DAR | - | finch | - | No fim, o erro das etiquetas virou um acerto de bico.
b10 | simples | loc_campo | two | DAR | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/15 itens) | PENDENTE | python3 pesquisar.py darwin1835
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh darwin1835
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh darwin1835
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local darwin1835 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

