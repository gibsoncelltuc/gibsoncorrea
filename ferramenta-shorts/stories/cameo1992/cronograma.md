# CRONOGRAMA - Poder e Fama EP 02 - O Cameo de Sete Segundos

Gerado em 24/11 12:32 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_cidade | close | FUN | - | marco_liberdade, tv | - | Em mil novecentos e noventa e dois, estreou o filme Esqueceram de Mim 
b1 | simples | interior pedra | two | FUN, TRU | - | - | - | Numa cena rápida, Kevin pergunta a um homem onde fica o saguão do hote
b2 | chave | loc_cidade | group | TRU, POV, POV | 10 | picket_fence | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | A cena dura cerca de sete segundos.
b3 | simples | interior pedra | close | TRU | - | tv | - | Acontece que aquele hotel, o Plaza, pertencia a Trump na época.
b4 | simples | interior loja | two | DIR, TRU | - | - | - | O diretor Chris Columbus disse, anos depois, que a equipe queria o sag
b5 | chave | loc_cidade | wide | DIR, TRU, POV | 10 | apartment, house_two, lamppost | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Segundo o diretor, a participação de Trump foi o preço para usar o hot
b6 | simples | interior loja | two | TRU, DIR | - | - | - | Trump nega isso: diz que a equipe é que pediu, e que ele nem queria ap
b7 | simples | interior loja | two | JOR, JOR2 | - | tv | - | Em dois mil e dezenove, uma emissora canadense exibiu o filme sem esse
b8 | simples | loc_cidade | reveal | JOR | 10 | marco_liberdade | - | O corte virou assunto por lá, e a discussão ainda dura até hoje.
b9 | simples | loc_cidade | close | TRU | - | tv | - | Moral da história: um cameo de sete segundos gera conversa por mais de
b10 | simples | loc_cidade | two | FUN | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/5 itens) | PENDENTE | python3 pesquisar.py cameo1992
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 6) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh cameo1992
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh cameo1992
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local cameo1992 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

