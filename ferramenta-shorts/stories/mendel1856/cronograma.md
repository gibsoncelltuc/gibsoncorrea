# CRONOGRAMA - Curiosidade e Ciência EP 09 - Mendel e as Ervilhas

Gerado em 25/11 19:29 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_campo | two | MEN | - | pe_ervilha, vagem_verde | - | Um monge contando ervilhas descobriu como herdamos o que somos.
b1 | simples | loc_campo | wide | MEN | 6 | - | - | E ninguém acreditou nele enquanto estava vivo.
b2 | transicao | loc_campo | wide | MEN, FRE | - | church, pe_ervilha | - | Em 1856, Gregor Mendel cuidava da horta de um mosteiro.
b3 | simples | loc_campo | two | MEN | - | vagem_amarela, vagem_verde | - | Cruzou ervilhas amarelas com ervilhas verdes.
b4 | simples | loc_campo | close | MEN | - | vagem_amarela | - | Todas saíram amarelas, como se o verde tivesse sumido.
b5 | simples | loc_campo | wide | MEN | - | vagem_amarela | - | Ele plantou de novo e contou ervilha por ervilha, por anos.
b6 | chave | interior pedra | two | MEN | - | bancada, vagem_amarela, vagem_verde | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que o verde voltou: três amarelas para uma verde.
b7 | simples | interior madeira | two | MEN, FRE | - | - | - | Cada filho herda uma instrução do pai e outra da mãe.
b8 | chave | interior pedra | wide | CIE | - | bancada, vagem_amarela, vagem_verde | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Só depois da morte dele, viram que estava certo.
b9 | simples | loc_campo | two | MEN | - | pe_ervilha, vagem_verde | - | Ele morreu sem saber. E foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (11/13 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | PENDENTE | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | REFAZER (a etapa anterior mudou) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh mendel1856
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh mendel1856
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local mendel1856 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 5. Voz

