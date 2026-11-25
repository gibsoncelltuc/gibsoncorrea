# CRONOGRAMA - Guerras Inusitadas EP 16 - A Guerra da Melancia

Gerado em 25/11 19:30 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | street | two | VIA, VEN | - | melon | - | Uma fatia de melancia quase virou guerra entre dois países.
b1 | simples | jungle | group | VEN | - | melon | - | E a fatia custava só uns centavos.
b2 | simples | loc_campo | wide | VIA | - | locomotive | - | Em 1856, viajantes cruzavam o Panamá atrás de ouro.
b3 | simples | jungle | two | VIA, VEN | - | melon, stall | - | Um americano comeu uma fatia de melancia e não quis pagar.
b4 | simples | street | group | VIA | 6 | shop, stall, pistol | - | O vendedor cobrou. O viajante riu e sacou uma arma.
b5 | chave | street | crowd | VEN | 20 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em minutos, virou briga de moradores contra viajantes.
b6 | chave | street | wide | VIA | - | locomotive | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Os viajantes se trancaram na estação de trem.
b7 | simples | street | two | PRE, MOR | 14 | - | - | Acontece que mais de quinze pessoas morreram naquele dia.
b8 | simples | street | group | PRE, VIA | - | - | - | A Colômbia teve que pagar uma indenização aos americanos.
b9 | simples | street | two | VIA, VEN | - | melon | - | Tudo por centavos que ninguém pagou. E foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (16/15 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh melancia1856
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh melancia1856
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local melancia1856 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

