# CRONOGRAMA - Guerras Inusitadas EP 25 - As Guerras do Bacalhau

Gerado em 25/11 17:20 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | chave | harbor | two | sem personagem | - | barco_guarda, fishing_net, navio_leander, navio_vapor | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Marinha grande é invencível? A Islândia provou que não.
b1 | simples | harbor | close | PES | - | crate, cod | - | Com uma arma que parecia piada: um cortador de rede.
b2 | transicao | harbor | wide | ICE, BRI | - | cod, navio_leander | - | Foram três Guerras do Bacalhau, em quase vinte anos.
b3 | simples | harbor | two | ICE, PES | - | crate | - | A Islândia vivia da pesca, e barcos ingleses pescavam na costa dela.
b4 | transicao | harbor | wide | ICE | - | navio_leander | - | Ela ampliou o mar dela: doze milhas, cinquenta, depois duzentas.
b5 | chave | harbor | wide | ICE | - | navio_leander, navios de guerra ao fundo, no tamanho real | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | A Inglaterra mandou fragatas da marinha para proteger os pesqueiros.
b6 | chave | harbor | wide | ICE | - | barco_guarda, fishing_net, navio_vapor | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | A Islândia só tinha barquinhos da guarda costeira.
b7 | transicao | harbor | wide | sem personagem | - | barco_guarda, fishing_net, navio_leander, navio_vapor | - | Mas eles cortavam os cabos das redes inglesas no meio do mar.
b8 | simples | harbor | two | BRI, ICE | - | scroll | - | Em 1976, a Inglaterra cedeu. As duzentas milhas viraram regra no mundo
b9 | chave | harbor | wide | sem personagem | - | barco_guarda, cod, fishing_net, navio_leander, navio_vapor, navios de guerra ao fundo, no tamanho real | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Tudo por um bacalhau. Marinha grande não é invencível.

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (14/16 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 2) | PENDENTE | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | REFAZER (a etapa anterior mudou) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh bacalhau1958
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh bacalhau1958
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local bacalhau1958 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | REFAZER (a etapa anterior mudou) | 

**Etapa atual:** 4. Travas do roteiro

