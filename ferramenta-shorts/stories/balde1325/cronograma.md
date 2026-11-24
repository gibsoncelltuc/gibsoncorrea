# CRONOGRAMA - Guerras Inusitadas EP 04 - A Guerra do Balde

Gerado em 24/11 04:38 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_campo | two | MOD, BOL | - | house_two, marco_ghirlandina, lamppost, bucket | - | Duas cidades italianas foram à guerra por causa de um balde de madeira
b1 | transicao | loc_campo | reveal | NOB, BOL | 8 | house_small, marco_ghirlandina, picket_fence, tree_oak | - | Módena e Bolonha se odiavam havia séculos. Uma apoiava o imperador, a 
b2 | simples | loc_montanha | track | MOD, MOD | - | marco_ghirlandina | - | Numa noite, diz a lenda, soldados de Módena entraram escondidos em Bol
b3 | chave | loc_montanha | crowd | MOD, MOD | - | house_small, well, picket_fence, tree_oak, bucket | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Não roubaram ouro, nem armas. Levaram o balde velho do poço da praça, 
b4 | simples | interior pedra | close | NOB | - | bucket | - | "Devolvam o nosso balde", exigiu Bolonha. "Venham buscar", respondeu M
b5 | simples | loc_montanha | crowd | BOL, BOL | 18 | marco_ghirlandina | - | Bolonha juntou um exército de trinta mil homens, e marchou contra a vi
b6 | simples | interior madeira | two | MOD, MOD | - | - | - | Módena tinha só sete mil soldados. Parecia uma derrota certa, e rápida
b7 | chave | loc_deserto | crowd | MOD, BOL | 24 | marco_ghirlandina | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que, numa única tarde de batalha, os sete mil atacaram de sur
b8 | simples | street | track | MOD, MOD | 8 | house_two, marco_ghirlandina, lamppost | - | Módena perseguiu os inimigos até as portas da cidade de Bolonha, e ain
b9 | simples | loc_deserto | close | MOD, MOD | - | marco_ghirlandina, bucket | - | O balde nunca foi devolvido. Está guardado em Módena até hoje, setecen
b10 | simples | loc_campo | close | MOD | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/6 itens) | PENDENTE | python3 pesquisar.py balde1325
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 2) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh balde1325
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh balde1325
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local balde1325 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

