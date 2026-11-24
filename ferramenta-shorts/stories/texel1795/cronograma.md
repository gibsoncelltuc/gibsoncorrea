# CRONOGRAMA - Guerras Inusitadas EP 22 - A Cavalaria que Capturou uma Frota

Gerado em 24/11 12:49 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | chave | arctic | wide | FRA, FRA | - | ship | corpo: cavaleiro galopando; emissao: poeira/clarao do tiro; luz: cena; camera: camera acompanha; som: galope | Uma frota de navios de guerra foi capturada por soldados a cavalo.
b1 | simples | arctic | reveal | FRA, NED | - | - | - | Era mil setecentos e noventa e cinco, a França invadia a Holanda, e fa
b2 | simples | arctic | orbit | NED, NED | - | ship | - | A frota holandesa estava ancorada perto de Den Helder, e o mar congelo
b3 | simples | arctic | wide | NED | - | ship | - | Os navios ficaram presos no gelo, sem conseguir sair do lugar.
b4 | simples | arctic | group | FRA, FRA, OFF | - | - | - | Do outro lado, os franceses tinham cavalaria, os hussardos, e nenhum n
b5 | simples | arctic | two | GEN, OFF | - | - | - | O chefe da cavalaria teve uma ideia maluca: atacar a frota a cavalo.
b6 | simples | arctic | low | OFF | - | - | - | Só que ninguém sabia se o gelo ia aguentar o peso de centenas de caval
b7 | chave | arctic | two | FRA, FRA | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Na noite de vinte e três de janeiro, os hussardos atravessaram o gelo,
b8 | chave | arctic | group | NED, FRA | 10 | ship | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que os holandeses nem tentaram lutar. A frota inteira se rend
b9 | chave | arctic | crowd | FRA, FRA | - | ship | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Mais de uma dezena de navios de guerra, capturados por soldados a cava
b10 | simples | arctic | close | FRA | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (12/12 itens) | FEITO | 
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

