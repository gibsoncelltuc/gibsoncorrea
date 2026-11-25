# CRONOGRAMA - Poder e Fama EP 20 - A Piada que Virou Tequila

Gerado em 25/11 17:27 | 9 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_cidade | two | MUS, FAN | - | tequila_bolt | - | Uma piada de primeiro de abril virou uma garrafa de 250 dólares.
b1 | simples | loc_patio | two | MUS | - | tequila_bolt | - | E até a garrafa vazia passou a valer uma fortuna.
b2 | simples | loc_cidade | reveal | MUS | 6 | phone, roadster | - | Em 2018, Musk postou que a Tesla faliu. Era piada.
b3 | chave | loc_cidade | wide | INV, MUS | - | tequila_bolt | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Na foto, garrafas de uma tal Teslaquila.
b4 | simples | interior loja | two | FAN, MUS | - | - | - | Muitos riram. Ele levou a sério.
b5 | chave | loc_pista | orbit | MEX, MUS | - | tequila_bolt, veg_cacto | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que o México barrou o nome: tequila tem regras.
b6 | simples | loc_pista | two | MUS, MEX | - | roadster, tequila_bolt, veg_cacto | - | Em 2020, saiu como Tesla Tequila, feita no México.
b7 | simples | interior loja | two | POV, FAN | - | phone, tequila_bolt | - | Garrafas vazias apareceram na internet por mais de mil dólares.
b8 | simples | loc_cidade | two | MUS, FAN | - | tequila_bolt | - | Ninguém acreditou na piada. E foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/13 itens) | PENDENTE | python3 pesquisar.py teslaquila2020
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh teslaquila2020
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh teslaquila2020
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local teslaquila2020 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 5. Voz

