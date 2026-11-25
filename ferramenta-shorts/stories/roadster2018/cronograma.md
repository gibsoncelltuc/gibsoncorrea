# CRONOGRAMA - Poder e Fama EP 08 - O Carro que Foi Parar no Espaço

Gerado em 25/11 17:33 | 9 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | arctic | two | MUS | - | roadster | - | Um carro de verdade está dando voltas em torno do Sol.
b1 | simples | interior loja | two | STA | - | roadster | - | E o motorista dele não respira.
b2 | transicao | loc_pista | wide | MUS | - | rocket | - | Em 2018, a SpaceX testou o Falcon Heavy, seu maior foguete.
b3 | simples | interior loja | two | ENG | - | roadster | - | Em vez de um peso de concreto, Musk mandou o próprio carro.
b4 | chave | loc_pista | wide | ENG | - | falcon_air | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | O foguete decolou com um estrondo!
b5 | simples | interior loja | two | STA | - | roadster | - | Acontece que no volante ia um boneco astronauta, o Starman.
b6 | simples | arctic | crowd | STA | - | roadster | - | No painel, um aviso: não entre em pânico.
b7 | explicativa | arctic | two | sem personagem | - | globe, roadster | corpo: kit/roadster (gira); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som e | O carro deixou a Terra e foi girar em torno do Sol.
b8 | transicao | arctic | wide | MUS | - | roadster | - | Ele continua lá até hoje. Porque...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (12/15 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | PENDENTE | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh roadster2018
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh roadster2018
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local roadster2018 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 5. Voz

