# CRONOGRAMA - A Morte Branca

Gerado em 24/11 05:20 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 0%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | chave | arctic | crowd | SOV, SOV, SOV, SOV | 48 | barn, haybale, picket_fence, scarecrow | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Um fazendeiro baixinho virou o soldado mais temido de uma guerra intei
b1 | explicativa | arctic | orbit | FIN, FIN, FIN | 32 | bush, tree_oak, tree_pine | - | Os soldados finlandeses eram poucos, mas conheciam a floresta, a neve 
b2 | simples | arctic | close | FIN | - | - | - | Um deles era um homem do campo, baixinho, chamado Simo Häyhä.
b3 | simples | mountain | low | FIN | - | - | - | Vestido de branco, ele esperava imóvel no meio da neve, horas a fio.
b4 | simples | mountain | close | FIN | - | - | - | Dizem que ele mantinha neve na boca, para o vapor da respiração não en
b5 | simples | arctic | two | FIN, FIN | - | campfire, picket_fence | - | Em cerca de cem dias, contam mais de quinhentos inimigos abatidos por 
b6 | chave | mountain | crowd | SOV | 48 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Os soviéticos passaram a chamá-lo de Morte Branca.
b7 | simples | interior hospital | two | FIN, FIN | - | - | - | Em março de mil novecentos e quarenta, uma bala atingiu o rosto dele. 
b8 | simples | interior madeira | close | FIN | - | - | - | Viveu até os noventa e seis anos, e nunca se achou herói. Dizia que só
b9 | simples | interior madeira | two | SOV | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (14/14 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 2) | PENDENTE | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh hayha1939
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh hayha1939
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local hayha1939 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 4. Travas do roteiro

