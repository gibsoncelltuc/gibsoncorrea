# CRONOGRAMA - Poder e Fama EP 19 - O Macaco que Jogou Videogame com a Mente

Gerado em 24/11 03:30 | 13 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_cidade | two | MUS, CIE | - | monkey_pong | - | Uma empresa de Elon Musk mostrou um macaco jogando videogame. Sem as m
b1 | chave | loc_cidade | crowd | POV, POV | 6 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Foi em abril de dois mil e vinte e um, nos Estados Unidos. A empresa s
b2 | simples | interior loja | two | CIM, MUS | - | - | - | A ideia é um chip implantado no cérebro, que lê os sinais dos neurônio
b3 | simples | interior loja | two | CIE | - | monkey_pong | - | O voluntário foi o Pager, um macaco de nove anos. Primeiro, ele aprend
b4 | simples | interior madeira | close | CIE | - | monkey_pong | - | A cada acerto, ganhava um golinho de vitamina de banana, por um canudi
b5 | simples | interior pedra | two | CIM, CIE | - | monkey_pong | - | Enquanto isso, o chip gravava o que os neurônios faziam a cada movimen
b6 | simples | interior loja | two | CIM | - | monkey_pong | - | Acontece que, um dia, desligaram o joystick. E o Pager continuou jogan
b7 | chave | loc_cidade | crowd | POV, POV, MUS | 18 | monkey_pong | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | O vídeo rodou o mundo. Muita gente se encantou, e muita gente debateu 
b8 | simples | loc_cidade | two | MUS, CIM | - | chess_pc, miners, phone | - | O objetivo, segundo a empresa, é ajudar pessoas paralisadas a usar com
b9 | simples | interior madeira | two | NOL, CIE | - | chess_pc | - | Em dois mil e vinte e quatro, o primeiro paciente humano recebeu o chi
b10 | simples | interior loja | two | NOL, CIE | - | chess_pc | - | Ele não mexia o corpo do pescoço para baixo. E voltou a jogar.
b11 | simples | loc_cidade | close | MUS | - | monkey_pong | - | E tudo começou com um macaco, um videogame antigo, e um copo de vitami
b12 | simples | loc_cidade | two | MUS | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/5 itens) | PENDENTE | python3 pesquisar.py neuralink2021
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 3) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | REFAZER (a etapa anterior mudou) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh neuralink2021
10 | Render | todos os quadros renderizados nesta versao das folhas | REFAZER (a etapa anterior mudou) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | REFAZER (a etapa anterior mudou) | ./conferir.sh neuralink2021
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local neuralink2021 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

