# CRONOGRAMA - Guerras Inusitadas EP 04 - A Guerra do Balde

Gerado em 26/11 00:02 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | medieval | two | MOD, BOL | - | balde_madeira, bucket | - | Uma guerra de verdade teve um balde de madeira como troféu.
b1 | simples | medieval | two | MOD | - | castle_tower, balde_madeira, bucket | - | E esse balde está guardado até hoje.
b2 | simples | interior pedra | two | NOB, PAP | - | - | - | Módena e Bolonha, na Itália, disputavam a fronteira havia décadas.
b3 | simples | loc_campo | crowd | BOL, BOL | 18 | picket_fence | - | Em 1325, Bolonha marchou com cerca de trinta mil soldados.
b4 | simples | loc_campo | two | MOD, MOD | 6 | - | - | Módena tinha menos de oito mil homens.
b5 | chave | loc_campo | crowd | MOD, BOL | 32 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que Módena atacou ao pôr do sol, e Bolonha fugiu.
b6 | simples | loc_campo | two | MOD, MOD | 8 | - | - | Depois, fizeram festa na porta de Bolonha.
b7 | simples | medieval | two | MOD, MOD | - | castle_tower, balde_madeira, well | - | E levaram de troféu o balde do poço da cidade.
b8 | simples | medieval | two | MOD | - | castle_tower, balde_madeira, bucket | - | O balde está na torre Ghirlandina, em Módena.
b9 | simples | medieval | two | MOD, BOL | - | balde_madeira, bucket | - | Milhares de soldados, e o prêmio foi um balde. Foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (11/12 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh balde1325
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh balde1325
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local balde1325 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

