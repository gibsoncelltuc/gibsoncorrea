# CRONOGRAMA - Poder e Fama EP 25 - O Carro que Voou de Cabeça para Baixo

Gerado em 25/11 18:20 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | chave | loc_pista | two | MUS, ENA | 8 | roadster26, torre_luz | corpo: decola com o jato dos propulsores embaixo e a onda de ar no chao, sobe 5 m, voa atravessando a cena inclinado e a | Um carro voou na frente dos convidados, e não era efeito especial.
b1 | simples | interior galpao | close | MUS | - | roadster26 | - | E ninguém esperava como ele fez isso.
b2 | simples | interior galpao | two | POV, POV | - | roadster | - | Elon Musk mostrou o novo Roadster numa base no Texas.
b3 | explicativa | loc_estudio | two | sem personagem | - | - | corpo: kit/roadster26 (parado); emissao: onda; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em cada e | Primeiro truque: uma sucção gruda o carro na pista.
b4 | chave | loc_pista | wide | MUS | - | roadster26, torre_luz | corpo: acelera e sobe a rampa curva gigante ate ficar de cabeca para baixo; emissao: VFX 3D preso no objeto (jato/poeira | Assim ele subiu uma rampa e ficou de cabeça para baixo.
b5 | chave | loc_pista | low | ENA | - | roadster26, torre_luz | corpo: se solta do topo, voa girando com o jato dos propulsores saindo de baixo e pousa numa nuvem branca (onda de ar no | Depois se soltou, girou no ar e pousou na fumaça.
b6 | explicativa | loc_estudio | two | sem personagem | - | - | corpo: kit/roadster26 (paira) em raio-X; emissao: jato; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som  | Segundo truque: dez bocais sopram ar comprimido para baixo.
b7 | chave | loc_pista | two | MUS | - | cybercab, cybertruck, roadster26, torre_luz | corpo: decola com o jato dos propulsores embaixo e a onda de ar no chao, sobe 5 m, voa atravessando a cena inclinado e a | Acontece que foi assim que ele decolou por cima de carros.
b8 | simples | loc_pista | group | ENG, ENA | - | roadster26 | - | Mas o voo durou poucos segundos.
b9 | simples | loc_pista | wide | MUS, ENA | 8 | roadster26, torre_luz | - | Ainda não é carro voador. Mas foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (13/14 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh roadsterpulo2026
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh roadsterpulo2026
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local roadsterpulo2026 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

