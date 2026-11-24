# CRONOGRAMA - Poder e Fama EP 19 - O Macaco que Jogou Videogame com a Mente

Gerado em 24/11 23:16 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_cidade | two | MUS, CIE | - | monkey_pong | - | Um macaco jogou videogame sem usar as mãos, só com o pensamento.
b1 | chave | loc_cidade | crowd | POV, POV | 6 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Foi em dois mil e vinte e um, e a empresa se chama Neuralink.
b2 | simples | interior loja | two | CIM, MUS | - | chess_pc | - | A ideia é um chip no cérebro, que lê os sinais dos neurônios e manda p
b3 | simples | interior loja | two | CIE | - | monkey_pong | - | O voluntário foi o Pager, um macaco de nove anos, que aprendeu a jogar
b4 | simples | interior madeira | two | CIE | - | monkey_pong | - | A cada acerto, ganhava um golinho de vitamina de banana.
b5 | simples | interior loja | two | CIM | - | monkey_pong | - | Acontece que, um dia, desligaram o joystick, e o Pager continuou jogan
b6 | simples | loc_cidade | crowd | POV, POV, MUS | 14 | monkey_pong | - | O vídeo rodou o mundo, e também abriu debate sobre o uso de animais em
b7 | chave | loc_cidade | orbit | MUS, CIM | 12 | chess_pc, phone | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Segundo a empresa, o objetivo é ajudar quem é paralisado a usar o comp
b8 | simples | interior madeira | two | NOL, CIE | - | chess_pc | - | Em dois mil e vinte e quatro, o primeiro paciente, que não mexia o cor
b9 | simples | loc_cidade | two | MUS | - | monkey_pong | - | Tudo começou com um macaco, um videogame e um copo de vitamina de bana
b10 | simples | loc_cidade | close | MUS | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (4/15 itens) | PENDENTE | python3 pesquisar.py neuralink2021
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh neuralink2021
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh neuralink2021
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local neuralink2021 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

