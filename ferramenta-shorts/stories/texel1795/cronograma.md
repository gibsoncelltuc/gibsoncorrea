# CRONOGRAMA - Guerras Inusitadas EP 22 - A Cavalaria que Capturou uma Frota

Gerado em 25/11 18:28 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | chave | arctic | wide | FRA | 8 | ship | corpo: cavaleiro galopando; emissao: poeira/clarao do tiro; luz: cena; camera: camera acompanha; som: galope | Uma frota de navios de guerra foi capturada por soldados a cavalo.
b1 | simples | arctic | wide | FRA, FRA | - | ship | - | E nenhum dos lados precisou dar um tiro.
b2 | simples | arctic | reveal | FRA, NED | - | - | - | Em 1795, a França invadia a Holanda.
b3 | simples | arctic | group | NED, NED | - | ship | - | A frota holandesa estava parada, e o mar congelou em volta.
b4 | transicao | arctic | wide | NED | - | ship | - | Os navios ficaram presos no gelo.
b5 | simples | arctic | group | GEN, OFF | - | - | - | O chefe da cavalaria francesa teve uma ideia: atacar a cavalo.
b6 | simples | arctic | wide | OFF | - | - | - | Mas ninguém sabia se o gelo aguentaria os cavalos.
b7 | chave | arctic | two | FRA, FRA | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | De noite, os hussardos cruzaram o gelo com panos nos cascos.
b8 | chave | arctic | group | NED, FRA | 10 | ship | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que os holandeses nem lutaram. A frota inteira se rendeu.
b9 | chave | arctic | wide | FRA | 8 | ship | corpo: cavaleiro galopando; emissao: poeira/clarao do tiro; luz: cena; camera: camera acompanha; som: galope | Cavalaria um, marinha zero. E foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (10/12 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh texel1795
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh texel1795
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local texel1795 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

