# CRONOGRAMA - E Se EP 06 - E Se o Dinheiro Sumisse do Mundo?

Gerado em 25/11 17:09 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | street | two | PRO, POV | - | coin | - | E se todo o dinheiro do mundo sumisse amanhã?
b1 | simples | countryside | reveal | PRO | 8 | coin | - | Em menos de um ano, a gente inventaria outro.
b2 | simples | interior loja | two | PAD, POV | - | - | - | Na primeira manhã, você não teria como pagar o café.
b3 | simples | countryside | two | FAZ, PAD | - | - | - | A saída seria a troca: uma galinha por uma cesta de comida.
b4 | simples | harbor | wide | PAD, FAZ | 6 | - | - | Acontece que o padeiro pode não querer galinha.
b5 | chave | street | reveal | POV, POV | 18 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Na ilha de Yap, o dinheiro eram pedras gigantes.
b6 | simples | harbor | two | PRO, POV | - | rocks | - | Algumas nem saíam do lugar. Todos só lembravam quem era o dono.
b7 | chave | interior madeira | two | PRO | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em prisões e guerras, quando o dinheiro some, inventam outro.
b8 | simples | harbor | group | POV, POV, FAZ | - | - | - | Dinheiro não é papel. É confiança entre as pessoas.
b9 | simples | street | two | PRO, POV | - | coin | - | E se ele sumisse amanhã? Agora você sabe o que viria.

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/12 itens) | PENDENTE | python3 pesquisar.py ese_dinheiro
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh ese_dinheiro
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh ese_dinheiro
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local ese_dinheiro <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

