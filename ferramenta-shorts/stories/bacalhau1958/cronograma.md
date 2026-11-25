# CRONOGRAMA - Guerras Inusitadas EP 25 - As Guerras do Bacalhau

Gerado em 25/11 17:33 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | chave | harbor | two | sem personagem | - | barco_guarda, fishing_net, navio_leander, navio_vapor | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | A Islândia derrotou a marinha inglesa usando um cortador de rede.
b1 | simples | harbor | close | PES | - | crate, cod | - | E o motivo da briga era o bacalhau.
b2 | transicao | harbor | wide | ICE, BRI | - | cod, navio_leander | - | Foram três Guerras do Bacalhau, em quase vinte anos.
b3 | simples | harbor | two | ICE, PES | - | crate, cod | - | Barcos ingleses pescavam bacalhau na costa da Islândia.
b4 | transicao | harbor | wide | ICE | - | navio_leander | - | A Islândia ampliou o seu mar: de doze para duzentas milhas.
b5 | chave | harbor | wide | ICE | - | navio_leander | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | A Inglaterra mandou fragatas de guerra.
b6 | chave | harbor | wide | ICE | - | barco_guarda, fishing_net, navio_vapor | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que a Islândia só tinha barcos da guarda costeira.
b7 | transicao | harbor | wide | sem personagem | - | barco_guarda, fishing_net, navio_leander, navio_vapor | - | E eles cortavam as redes inglesas no meio do mar.
b8 | simples | harbor | two | BRI, ICE | - | scroll | - | Em 1976, a Inglaterra finalmente desistiu da briga.
b9 | chave | harbor | wide | sem personagem | - | barco_guarda, fishing_net, navio_leander, navio_vapor | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | As duzentas milhas viraram regra no mundo. E foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (14/16 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | PENDENTE | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | REFAZER (a etapa anterior mudou) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh bacalhau1958
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh bacalhau1958
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local bacalhau1958 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | REFAZER (a etapa anterior mudou) | 

**Etapa atual:** 5. Voz

