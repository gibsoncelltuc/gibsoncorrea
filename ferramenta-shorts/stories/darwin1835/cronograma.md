# CRONOGRAMA - Curiosidade e Ciência EP 08 - Darwin e os Tentilhões

Gerado em 25/11 17:51 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | harbor | two | DAR, MAR | - | bancada, finch | - | Uma etiqueta trocada ajudou Darwin a explicar a vida na Terra.
b1 | simples | countryside | two | DAR | - | bancada, finch | - | E tudo começou no bico de um passarinho.
b2 | simples | harbor | wide | MAR | - | navio_fragata | - | Em 1835, Darwin chegou às ilhas Galápagos.
b3 | simples | harbor | wide | DAR, MAR | - | bancada, finch, navio_fragata | - | Coletou passarinhos de ilha em ilha, sem anotar de onde vinham.
b4 | simples | interior pedra | group | GOU | - | bancada, finch | - | Em Londres, descobriram: eram todos tentilhões.
b5 | simples | interior madeira | two | GOU, DAR | - | bancada, finch_long, finch_thick | - | A diferença estava no bico: grosso para sementes, fino para insetos.
b6 | chave | harbor | two | DAR, GOU | - | bancada, finch, finch_long, finch_thick | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que cada ilha tinha o bico certo para a sua comida.
b7 | simples | interior madeira | group | DAR | - | bancada, finch_thick | - | Quem tinha o bico certo sobrevivia.
b8 | chave | interior madeira | two | DAR, GOU | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em 1859, isso virou a seleção natural.
b9 | simples | harbor | two | DAR, MAR | - | bancada, finch | - | Darwin nunca mais esqueceu de anotar. Porque...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (13/15 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | PENDENTE | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh darwin1835
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh darwin1835
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local darwin1835 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 5. Voz

