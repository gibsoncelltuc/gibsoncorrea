# CRONOGRAMA - Guerras Inusitadas EP 05 - Os Gansos que Salvaram Roma

Gerado em 25/11 17:26 | 9 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | medieval | group | ROM | - | - | - | Um bando de gansos barulhentos salvou Roma numa noite.
b1 | simples | medieval | group | ROM | - | - | - | Mas o ouro de Roma foi embora mesmo assim.
b2 | chave | loc_campo | reveal | GAU | 8 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em 390 antes de Cristo, os gauleses tomaram Roma.
b3 | chave | loc_montanha | orbit | ROM | - | castle_tower | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Os romanos que sobraram se trancaram no Capitólio, uma colina.
b4 | simples | loc_campo | wide | GAU | - | castle_tower | - | Numa noite sem lua, os gauleses chegaram em silêncio à muralha.
b5 | simples | loc_campo | wide | ROM | - | - | - | Acontece que os gansos sagrados de Juno ouviram e gritaram.
b6 | simples | loc_campo | two | MAN, GAU | - | - | - | O barulho acordou o soldado Marco Mânlio, que barrou a subida.
b7 | simples | interior madeira | two | ROM, GAU | - | - | - | Depois de sete meses de fome, Roma pagou mil libras de ouro.
b8 | simples | medieval | group | ROM | - | - | - | Os guardas não ouviram, os gansos sim. E foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (6/8 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | PENDENTE | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | REFAZER (a etapa anterior mudou) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh gansos390
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh gansos390
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local gansos390 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 5. Voz

