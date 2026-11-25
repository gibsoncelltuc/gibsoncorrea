# CRONOGRAMA - Guerras Inusitadas EP 23 - A Morte Branca

Gerado em 25/11 16:46 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | chave | arctic | wide | FIN, SOV | 48 | barn, haybale, picket_fence, scarecrow | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Um fazendeiro baixinho virou o soldado mais temido de uma guerra.
b1 | simples | arctic | close | SOV | - | - | - | Os inimigos tinham tanto medo que deram um apelido a ele.
b2 | chave | arctic | crowd | SOV, SOV | 48 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | No inverno de 1939, a União Soviética invadiu a Finlândia.
b3 | explicativa | arctic | group | FIN, FIN, FIN | - | bush, tree_oak, tree_pine | - | Fazia quarenta graus abaixo de zero na floresta.
b4 | simples | arctic | close | FIN | - | - | - | Um soldado do campo, baixinho, se chamava Simo Häyhä.
b5 | simples | arctic | low | FIN | - | - | - | Vestido de branco, ele esperava imóvel na neve por horas.
b6 | simples | arctic | close | FIN | - | - | - | Dizem que punha neve na boca para o vapor não aparecer.
b7 | chave | arctic | wide | FIN, FIN | 48 | picket_fence | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em cerca de cem dias, contam mais de quinhentos abatidos por ele.
b8 | simples | arctic | close | SOV | - | - | - | Os soviéticos o chamavam de Morte Branca.
b9 | simples | interior hospital | two | FIN, FIN | - | - | - | Em 1940, uma bala atingiu o rosto dele. Ele sobreviveu.
b10 | simples | arctic | wide | FIN, SOV | 32 | - | - | Viveu até 96 anos e dizia: só fiz meu trabalho.

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (12/13 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh hayha1939
10 | Render | todos os quadros renderizados nesta versao das folhas | REFAZER (a etapa anterior mudou) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | REFAZER (a etapa anterior mudou) | ./conferir.sh hayha1939
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local hayha1939 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | REFAZER (a etapa anterior mudou) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

