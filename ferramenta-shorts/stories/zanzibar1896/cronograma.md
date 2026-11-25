# CRONOGRAMA - Guerras Inusitadas EP 08 - A Guerra de 38 Minutos

Gerado em 25/11 22:22 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | harbor | two | SUL, GUA | - | marco_zanzibar | - | A guerra mais curta da história durou menos de quarenta minutos.
b1 | simples | harbor | reveal | ALM | 8 | - | - | E os derrotados ainda pagaram a conta.
b2 | simples | harbor | two | SUL, POV | - | marco_zanzibar | - | Em 1896, em Zanzibar, na África, o sultão morreu.
b3 | simples | interior pedra | two | SUL, GUA | - | throne | - | Um primo ocupou o palácio sem pedir licença aos ingleses.
b4 | simples | loc_campo | wide | ALM | - | marco_zanzibar, navio_vapor | - | Deram até as nove da manhã para ele sair.
b5 | simples | loc_campo | reveal | GUA, GUA | 32 | marco_zanzibar | - | Ele juntou quase três mil homens e se trancou lá dentro.
b6 | chave | harbor | orbit | sem personagem | - | cannon, marco_zanzibar, navio_vapor_guerra, navios de guerra ao fundo, no tamanho real | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que, às nove e dois, os navios ingleses abriram fogo.
b7 | explicativa | loc_estudio | two | sem personagem | - | - | corpo: kit/forte_colonial (parado); emissao: fogo, onda; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som | O palácio pegou fogo, e o primo fugiu.
b8 | simples | loc_campo | two | GUA | - | forte_colonial, marco_zanzibar, flagpole | - | Às nove e quarenta, a bandeira caiu.
b9 | simples | harbor | two | SUL, GUA | - | - | - | Os ingleses mandaram a conta das balas. E foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (14/15 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | PENDENTE | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh zanzibar1896
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh zanzibar1896
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local zanzibar1896 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 5. Voz

