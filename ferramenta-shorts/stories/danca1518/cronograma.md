# CRONOGRAMA - Curiosidade e Ciência EP 22 - A Praga da Dança

Gerado em 26/11 00:35 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | medieval | two | TRO, POV | - | marco_viena | - | Uma mulher começou a dançar na rua e não conseguiu parar.
b1 | simples | medieval | reveal | MED, POV | 8 | - | - | E até hoje ninguém sabe ao certo por quê.
b2 | simples | medieval | two | TRO, POV | - | marco_viena | - | Em 1518, em Estrasburgo, ela dançou por uma semana.
b3 | chave | medieval | crowd | TRO, POV, POV, POV | 48 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em poucos dias, mais de trinta pessoas dançavam também.
b4 | simples | medieval | group | POV, TRO, POV, POV | 36 | - | - | Em agosto, eram centenas, com os pés sangrando.
b5 | simples | interior pedra | two | PRE, MED | - | - | - | Os médicos culparam o sangue quente e receitaram mais dança.
b6 | chave | hall | orbit | MUS, MUS | 12 | house_two, lamppost | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que a cidade contratou músicos para manter todos dançando.
b7 | simples | hall | group | PRE, DAN | 10 | - | - | Deu errado: mais gente entrou na dança.
b8 | transicao | hall | wide | DAN | - | church | - | Levados a uma capela no monte, eles finalmente pararam.
b9 | simples | medieval | two | TRO, POV | - | - | - | Histeria coletiva? Ninguém sabe. Só se sabe que foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (8/8 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | FEITO | 
10 | Render | todos os quadros renderizados nesta versao das folhas | PENDENTE | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh danca1518
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local danca1518 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 10. Render

