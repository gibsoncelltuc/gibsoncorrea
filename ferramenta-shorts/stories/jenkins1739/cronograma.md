# CRONOGRAMA - Guerras Inusitadas EP 12 - A Guerra da Orelha de Jenkins

Gerado em 25/11 17:32 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | harbor | two | JEN, ESP | - | ear_jar | - | Uma orelha cortada começou uma guerra de nove anos.
b1 | simples | street | two | JEN, ESP | 12 | ear_jar | - | E o dono da orelha levou ela até o Parlamento.
b2 | simples | harbor | wide | JEN | - | navios de guerra ao fundo, no tamanho real, ship | - | Perto de Cuba, espanhóis pararam o navio do capitão Robert Jenkins.
b3 | chave | street | two | CAP, JEN | - | ear_jar | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | O comandante espanhol cortou a orelha dele com a espada.
b4 | simples | harbor | two | CAP, JEN | - | - | - | "Leve isso ao seu rei", teria dito.
b5 | simples | interior pedra | two | PRE, JEN | - | ear_jar | - | Anos depois, dizem, Jenkins mostrou a orelha aos deputados.
b6 | simples | interior pedra | group | PRE, ING | - | - | - | Acontece que a Inglaterra só queria um pretexto.
b7 | chave | harbor | wide | SOL | 48 | navios de guerra ao fundo, no tamanho real, ship | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em 1739, navios ingleses atacaram o Caribe espanhol.
b8 | simples | interior pedra | two | ESP, ING | - | ear_jar | - | Nove anos de guerra, por causa de uma orelha.
b9 | simples | harbor | two | JEN, ESP | - | ear_jar | - | Jenkins nunca recuperou a orelha. E foi assim que...

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
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh jenkins1739
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh jenkins1739
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local jenkins1739 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

