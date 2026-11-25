# CRONOGRAMA - Guerras Inusitadas EP 03 - A Guerra de Toledo

Gerado em 25/11 16:48 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | countryside | two | OHI | 16 | canivete_aberto | - | Dois estados americanos foram à guerra. O único ferido levou uma caniv
b1 | simples | interior madeira | close | GOV | - | - | - | E quem perdeu a guerra acabou ficando rico.
b2 | simples | countryside | two | OHI, MIC | - | mapa_antigo | - | Ohio e Michigan disputavam Toledo por causa de um mapa errado.
b3 | simples | interior madeira | close | GOV | - | - | - | Em 1835, o governador de Michigan, de 23 anos, ocupou Toledo.
b4 | chave | countryside | crowd | OHI | 48 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Ohio mandou a própria milícia. As tropas ficaram frente a frente.
b5 | chave | countryside | orbit | OHI | 48 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Houve gritos e tiros para o alto. Ninguém acertou ninguém.
b6 | simples | interior madeira | two | RAP, XER | - | canivete_aberto | - | A única baixa: um xerife esfaqueado com canivete numa taverna.
b7 | simples | arctic | wide | OHI, MIC, GOV | - | bush, tree_oak, tree_pine | - | Ohio ficou com Toledo. Michigan levou uma floresta gelada.
b8 | simples | jungle | two | GOV, MIC | - | minerio, bush, tree_oak, tree_pine | - | Acontece que debaixo da floresta havia cobre e ferro. Uma fortuna.
b9 | simples | countryside | two | OHI | 16 | canivete_aberto | - | Michigan perdeu a guerra e ficou rico.

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (12/15 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh toledo1835
10 | Render | todos os quadros renderizados nesta versao das folhas | REFAZER (a etapa anterior mudou) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | REFAZER (a etapa anterior mudou) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | REFAZER (a etapa anterior mudou) | ./conferir.sh toledo1835
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local toledo1835 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | REFAZER (a etapa anterior mudou) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

