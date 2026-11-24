# CRONOGRAMA - Poder e Fama EP 03 - O X no Prédio do Twitter

Gerado em 24/11 23:35 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_patio | two | MUS | - | house_two, marco_goldengate, phone, bench, lamppost | - | Uma empresa trocou de nome, e a placa nova acabou investigada pela pre
b1 | simples | interior pedra | two | MUS, OPE | - | - | - | Foi em julho de dois mil e vinte e três: Elon Musk trocou o nome do Tw
b2 | chave | loc_cidade | group | OPE, OPE2, MUS | 10 | finch | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Os operários começaram a tirar as letras e o passarinho da fachada.
b3 | simples | interior loja | two | OPE, FIS | - | - | - | Mas o trabalho parou no meio, porque faltavam licenças.
b4 | transicao | loc_cidade | wide | OPE2 | 6 | - | - | Sobraram só as letras E e R, em cinza, na fachada.
b5 | chave | loc_cidade | crowd | MUS | - | apartment, house_two, marco_goldengate, lamppost | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que depois instalaram um X gigante piscando no alto do prédio
b6 | simples | interior pedra | two | FIS, MUS | - | - | - | A prefeitura recebeu vinte e quatro reclamações num fim de semana e ab
b7 | simples | interior loja | two | MUS, FIS | - | - | - | A empresa disse que era uma placa temporária para um evento.
b8 | simples | loc_cidade | two | FIS, OPE | - | - | - | A polícia foi ao local, mas concluiu que nenhum crime tinha acontecido
b9 | simples | interior madeira | two | MUS | - | phone | - | Moral da história: até trocar de nome precisa de licença da prefeitura
b10 | simples | interior madeira | close | MUS | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (4/13 itens) | PENDENTE | python3 pesquisar.py xplaca2023
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh xplaca2023
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh xplaca2023
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local xplaca2023 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

