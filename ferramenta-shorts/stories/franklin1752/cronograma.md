# CRONOGRAMA - Curiosidade e Ciência EP 07 - Franklin, a Pipa e o Raio

Gerado em 25/11 19:31 | 9 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | street | two | FRA, FIL | - | kite | - | Um homem soltou uma pipa na tempestade para pegar um raio.
b1 | simples | interior madeira | two | FRA | - | - | - | E o que ele descobriu protege a sua casa até hoje.
b2 | transicao | street | reveal | COM, POV | 8 | - | - | Em 1752, Benjamin Franklin queria provar que raio era eletricidade.
b3 | simples | interior madeira | two | COM, POV | - | - | - | Muita gente achava que o raio era castigo dos céus.
b4 | simples | countryside | two | FRA, FIL | - | key, kite | - | Contam que ele prendeu uma chave de metal na linha da pipa.
b5 | chave | countryside | two | FRA | - | key, kite | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que a nuvem passou, e uma faísca pulou da chave.
b6 | simples | interior madeira | two | COM, FRA | - | kite | - | Se um raio caísse na pipa, ele teria morrido.
b7 | chave | street | wide | FRA | - | house_two, lightning_rod, lamppost | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Daí nasceu o para-raios, que protege prédios no mundo inteiro.
b8 | simples | street | two | FRA, FIL | - | kite | - | Coragem ou loucura? Só sei que foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (11/12 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | PENDENTE | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | REFAZER (a etapa anterior mudou) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh franklin1752
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh franklin1752
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local franklin1752 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 5. Voz

