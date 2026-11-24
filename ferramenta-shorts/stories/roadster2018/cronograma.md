# CRONOGRAMA - Poder e Fama EP 08 - O Carro que Foi Parar no Espaço

Gerado em 24/11 22:39 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | harbor | two | MUS | - | falcon_air, roadster | - | Em fevereiro de dois mil e dezoito, um Tesla de verdade foi lançado pa
b1 | simples | harbor | wide | MUS | - | roadster | - | Era um Roadster vermelho, e quem teve a ideia foi Elon Musk, o dono da
b2 | transicao | harbor | wide | MUS | - | rocket | - | O voo de estreia do Falcon Heavy, o maior foguete da empresa, acontece
b3 | simples | interior loja | two | ENG | - | roadster | - | Como era só um teste, em vez de colocar peso de concreto, Musk resolve
b4 | chave | harbor | crowd | ENG | - | falcon_air | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | O foguete decolou com um estrondo!
b5 | simples | interior loja | two | STA | - | roadster | - | No banco do motorista foi sentado um boneco de astronauta, chamado Sta
b6 | simples | loc_campo | orbit | STA | - | roadster | - | No painel, estava escrito: Não entre em pânico.
b7 | simples | arctic | wide | ENG | - | globe, roadster | - | O Roadster saiu da órbita da Terra, e seguiu em órbita ao redor do Sol
b8 | simples | arctic | two | MUS | - | roadster | - | E ele continua lá em cima, dando voltas, até hoje.
b9 | chave | arctic | orbit | MUS | - | roadster, rocket | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Um Roadster, um boneco e um aviso no painel: uma das maiores brincadei
b10 | simples | arctic | close | MUS | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/13 itens) | PENDENTE | python3 pesquisar.py roadster2018
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 4) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh roadster2018
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh roadster2018
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local roadster2018 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

