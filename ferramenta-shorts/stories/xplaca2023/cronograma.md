# CRONOGRAMA - Poder e Fama EP 03 - O X no Prédio do Twitter

Gerado em 25/11 17:21 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_patio | two | MUS | - | marco_goldengate, phone | - | Trocar de nome é fácil? Esta placa nova virou caso de investigação.
b1 | simples | interior madeira | two | MUS | - | phone | - | E tudo por causa de uma letra só.
b2 | simples | interior pedra | two | MUS, OPE | - | - | - | Em 2023, Elon Musk trocou o nome do Twitter para X.
b3 | chave | loc_cidade | group | OPE, OPE2, MUS | 10 | finch | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Operários começaram a tirar as letras e o passarinho da fachada.
b4 | simples | interior loja | two | OPE, FIS | - | - | - | O trabalho parou no meio, porque faltavam licenças.
b5 | chave | loc_cidade | wide | MUS | - | apartment, house_two, marco_goldengate, lamppost | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que instalaram um X gigante piscando no alto do prédio.
b6 | simples | loc_cidade | two | POV, JOR | - | house_small, picket_fence, tree_oak | - | A luz entrava nas janelas dos vizinhos de madrugada.
b7 | simples | interior pedra | two | FIS, MUS | - | - | - | Vieram vinte e quatro reclamações num fim de semana.
b8 | simples | loc_cidade | orbit | FIS, OPE | 8 | house_two, bench, lamppost | - | A prefeitura investigou, e o X foi retirado.
b9 | simples | loc_patio | two | MUS | - | phone | - | Até trocar de nome precisa de licença.

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (11/13 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | PENDENTE | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | REFAZER (a etapa anterior mudou) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh xplaca2023
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh xplaca2023
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local xplaca2023 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 4. Travas do roteiro

