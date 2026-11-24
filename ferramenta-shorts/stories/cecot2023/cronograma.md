# CRONOGRAMA - Poder e Fama EP 27 - A Maior Prisão das Américas

Gerado em 24/11 23:46 | 12 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_campo | two | GUA, BUK | 26 | prison | - | El Salvador tem uma prisão tão grande que virou notícia no mundo intei
b1 | simples | loc_campo | reveal | POV, POV | 6 | prison | - | Foi inaugurada em janeiro de dois mil e vinte e três, numa área isolad
b2 | simples | interior galpao | two | REP, POV | - | - | - | Por anos, El Salvador teve uma das maiores taxas de assassinato do mun
b3 | simples | loc_campo | orbit | BUK, GUA, GUA | 30 | prison | - | Em dois mil e vinte e dois, o presidente Nayib Bukele decretou estado 
b4 | simples | loc_pista | group | GUA, GUA, GUA | 16 | prison | - | Para guardar tanta gente, ergueram o Centro de Confinamento do Terrori
b5 | explicativa | loc_estudio | two | sem personagem | - | - | corpo: kit/prison (gira); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em  | Muralhas altas, cercas elétricas e torres de vigia por todos os lados.
b6 | chave | loc_campo | wide | REP, BUK | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que os assassinatos despencaram: de cento e seis para dois ví
b7 | simples | loc_campo | two | REP, POV | - | - | - | Organizações de direitos humanos denunciaram prisões sem julgamento e 
b8 | chave | loc_patio | orbit | BUK, REP | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | O governo responde que as ruas ficaram seguras.
b9 | simples | loc_patio | group | POV, POV, POV | - | prison | - | A prisão virou símbolo: de segurança para uns, de excesso para outros.
b10 | simples | loc_pista | group | BUK, POV | - | globe | - | E o modelo passou a ser copiado e criticado pelo mundo.
b11 | simples | loc_campo | close | GUA | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/14 itens) | PENDENTE | python3 pesquisar.py cecot2023
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh cecot2023
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh cecot2023
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local cecot2023 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 4. Travas do roteiro

