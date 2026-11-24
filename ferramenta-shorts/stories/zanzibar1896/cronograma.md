# CRONOGRAMA - Guerras Inusitadas EP 08 - A Guerra de 38 Minutos

Gerado em 24/11 03:30 | 12 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | palace | two | SUL, GUA | - | marco_zanzibar | - | A guerra mais curta da história durou menos que um almoço.
b1 | transicao | palace | reveal | SUL, POV | 8 | marco_zanzibar | - | Era em Zanzibar, uma ilha da costa da África, controlada pela Inglater
b2 | simples | interior pedra | two | SUL, GUA | - | throne | - | O sultão morreu de repente, e um primo dele correu para o palácio, e s
b3 | simples | interior pedra | group | ALM, ING | - | - | - | Os ingleses não gostaram. "Saia do palácio até as nove da manhã", avis
b4 | chave | harbor | crowd | GUA, GUA | 48 | cannon, marco_zanzibar | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | O novo sultão juntou quase três mil homens, alguns canhões velhos, e s
b5 | simples | interior pedra | close | SUL | - | - | - | "Eles não vão atirar", disse ele.
b6 | chave | palace | orbit | ING, GUA | 48 | marco_zanzibar, navios de guerra ao fundo, no tamanho real | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que, às nove e dois, os navios ingleses abriram fogo. O palác
b7 | simples | harbor | track | SUL, GUA | - | house_two, bench, lamppost | - | O sultão fugiu pela porta dos fundos, e foi pedir abrigo no consulado 
b8 | simples | interior pedra | two | GUA, ING | - | cannon, flagpole | - | Às nove e quarenta, a bandeira do palácio caiu, e os canhões pararam.
b9 | simples | loc_campo | group | ALM, ING, POV | - | - | - | Trinta e oito minutos. No mesmo dia, os ingleses colocaram outro sultã
b10 | simples | interior loja | close | ALM | - | - | - | E ainda mandaram a conta das balas para Zanzibar.
b11 | simples | palace | close | SUL | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/5 itens) | PENDENTE | python3 pesquisar.py zanzibar1896
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 4) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh zanzibar1896
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh zanzibar1896
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local zanzibar1896 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

