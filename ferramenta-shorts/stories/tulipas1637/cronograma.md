# CRONOGRAMA - Curiosidade e Ciência EP 21 - A Febre das Tulipas

Gerado em 25/11 19:36 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | street | two | MER, RIC | - | house_small, marco_amsterdam, tulip_striped, picket_fence, tree_oak | - | Uma única flor já custou o preço de uma casa.
b1 | simples | countryside | wide | RIC | - | marco_amsterdam, tulip_bed | - | E quem pagou isso perdeu tudo em poucos dias.
b2 | simples | countryside | wide | POV | - | windmill, marco_amsterdam, tulip_bed | - | Em 1637, na Holanda, a tulipa virou moda.
b3 | simples | countryside | two | RIC, RIC | - | coin, tulip_striped | - | Num leilão, um bulbo saiu por duas mil moedas.
b4 | chave | countryside | wide | POV | - | marco_amsterdam, tulip_bed | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Logo, padeiros e sapateiros também queriam bulbos.
b5 | simples | harbor | wide | RIC, MER | - | house_small, marco_amsterdam, scroll, tulip_striped, picket_fence, tree_oak | - | Contam que teve gente trocando casas por um único bulbo.
b6 | simples | interior madeira | two | MAR, MER | - | tulip_red | - | Um marinheiro comeu um bulbo achando que era cebola.
b7 | simples | interior loja | group | MER, POV, POV, RIC | - | - | - | Acontece que, num leilão de fevereiro, ninguém levantou a mão.
b8 | chave | countryside | wide | POV | - | house_small, marco_amsterdam, tulip_bed, picket_fence, tree_oak | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Os preços desabaram. Quem trocou a casa ficou só com flores.
b9 | simples | street | two | MER, RIC | - | tulip_striped | - | Uma loucura que se repete. Foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (11/14 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | PENDENTE | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh tulipas1637
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh tulipas1637
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local tulipas1637 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 8. Storyboard e grade de acoes

