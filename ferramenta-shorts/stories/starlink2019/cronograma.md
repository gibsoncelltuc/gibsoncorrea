# CRONOGRAMA - Poder e Fama EP 04 - A Fila de Luzes no Céu

Gerado em 25/11 17:34 | 9 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | chave | countryside | two | AST | - | starlink_train | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Uma fila de luzes cruzou o céu, e chamaram de ETs.
b1 | simples | interior loja | two | JOR, JOR2 | - | rocket | - | E a verdade estava num foguete da Flórida.
b2 | transicao | loc_pista | wide | AST | - | falcon_air, starlink_sat | - | Em 2019, a SpaceX lançou sessenta satélites de uma vez.
b3 | simples | countryside | two | AST, JOR | - | - | - | Um dia depois, o holandês Marco Langbroek filmou o céu.
b4 | transicao | loc_montanha | wide | AST | - | starlink_train | - | Viu pelo menos cinquenta e seis luzes em fila.
b5 | chave | loc_cidade | crowd | JOR | - | phone | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que um site de OVNIs recebeu mais de 150 relatos.
b6 | explicativa | loc_cidade | two | sem personagem | - | falcon_air | corpo: kit/starlink_train (parado); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; so | Os satélites ainda voavam juntos, logo depois do lançamento.
b7 | simples | interior loja | two | JOR, JOR2 | - | starlink_sat | - | Não eram ETs. Eram satélites de internet.
b8 | chave | countryside | wide | AST | - | starlink_train | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Internet no céu, e foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (11/13 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | PENDENTE | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh starlink2019
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh starlink2019
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local starlink2019 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 7. Gates

