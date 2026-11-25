# CRONOGRAMA - Guerras Inusitadas EP 02 - A Guerra dos Emus

Gerado em 25/11 17:52 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | outback | two | SOL, FARM | - | - | - | Um exército perdeu uma guerra contra pássaros.
b1 | transicao | countryside | reveal | FARM, FARM | - | - | - | E o placar final virou piada no mundo inteiro.
b2 | simples | outback | group | FARM, FARM | - | barn, haybale, picket_fence, scarecrow | - | Em 1932, vinte mil emus tomaram as lavouras da Austrália.
b3 | simples | interior madeira | two | FARM, AUS | 6 | - | - | Os agricultores pediram ajuda, e o governo mandou soldados.
b4 | simples | countryside | wide | SOL, SOL | 32 | crate, mgun | - | O major Meredith levou duas metralhadoras e dez mil balas.
b5 | chave | outback | orbit | SOL, SOL | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que os emus se espalharam, e as balas só acertavam poeira.
b6 | simples | countryside | wide | SOL | - | mgun, truck | - | Uma metralhadora num caminhão sacudia tanto que ninguém acertava.
b7 | simples | outback | wide | SOL | - | tank | - | O major comparou os emus a tanques. A imprensa riu.
b8 | chave | loc_campo | crowd | SOL, SOL | 48 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Seis dias, milhares de balas, poucos emus abatidos.
b9 | transicao | outback | reveal | SOL, FARM | - | - | - | Exército zero, emus um. E foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (15/18 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | PENDENTE | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | REFAZER (a etapa anterior mudou) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh emus1932
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh emus1932
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local emus1932 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 4. Travas do roteiro

