# CRONOGRAMA - Poder e Fama EP 10 - A Pia no Twitter

Gerado em 24/11 22:52 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_cidade | two | MUS, FUN | - | marco_goldengate, sink | - | Um bilionário entrou carregando uma pia na empresa que estava comprand
b1 | simples | interior pedra | two | MUS, FUN2 | - | sink | - | Foi Elon Musk, em outubro de dois mil e vinte e dois, na sede do Twitt
b2 | simples | interior pedra | close | MUS | - | sink | - | Ele filmou a própria entrada, com a pia nos braços, e postou o vídeo n
b3 | simples | interior loja | two | MUS, FUN | - | - | - | A legenda dizia: Entrando na sede do Twitter. Deixe isso afundar.
b4 | explicativa | loc_estudio | two | sem personagem | - | - | corpo: kit/sink (gira); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em ca | É um trocadilho: em inglês, a palavra sink quer dizer pia, e também af
b5 | chave | interior madeira | two | MUS, FUN | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que, no dia seguinte, ele fechou a compra do Twitter, por qua
b6 | simples | interior pedra | two | MUS, FUN, FUN2 | - | - | - | No mesmo dia, ele demitiu o presidente e outros chefes da empresa.
b7 | simples | interior loja | two | MUS | - | - | - | Ele também mudou o perfil, e escreveu que era o Chefe Twit.
b8 | chave | loc_cidade | crowd | FUN, FUN2 | 14 | marco_goldengate, sink | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | O vídeo da pia virou piada no mundo inteiro.
b9 | simples | loc_cidade | orbit | MUS | 8 | sink | - | Uma pia, um trocadilho e quarenta e quatro bilhões de dólares.
b10 | simples | loc_cidade | close | MUS | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/12 itens) | PENDENTE | python3 pesquisar.py pia2022
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh pia2022
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh pia2022
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local pia2022 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

