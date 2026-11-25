# CRONOGRAMA - E Se EP 03 - E Se o Brasil Tivesse Sido Holandês?

Gerado em 25/11 17:29 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | harbor | two | NAS, POV | - | flag_pole, marco_olinda | - | Um pedaço do Brasil foi holandês por 24 anos.
b1 | chave | countryside | crowd | POV, POV, ART | 20 | skyscraper, marco_olinda | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | E essa história termina em Nova York.
b2 | simples | harbor | reveal | POV, POV | 6 | marco_olinda, navios de guerra ao fundo, no tamanho real | - | Em 1630, navios holandeses tomaram Pernambuco, atrás do açúcar.
b3 | simples | countryside | two | NAS, ART | - | marco_olinda | - | Maurício de Nassau levou artistas para Recife.
b4 | simples | street | two | NAS, POV | - | bridge, marco_olinda | - | Recife ganhou até a primeira sinagoga das Américas.
b5 | chave | jungle | orbit | POR, POR, POV | 18 | marco_olinda | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que portugueses, indígenas e africanos se uniram contra eles.
b6 | simples | street | two | NAS, POV | - | ship | - | Em 1654, os holandeses foram embora.
b7 | simples | interior loja | close | ART | - | - | - | O Suriname, aqui do lado, fala holandês até hoje.
b8 | simples | street | two | NAS, ART | - | scroll | - | Depois, a Holanda trocou Nova Amsterdã pelo Suriname.
b9 | chave | street | crowd | POV, POV, ART | 20 | house_small, skyscraper, marco_olinda, picket_fence, tree_oak | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Essa vila hoje se chama Nova York.
b10 | simples | harbor | two | NAS, POV | - | flag_pole | - | Se tivessem ficado, o mapa seria outro. Porque...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/12 itens) | PENDENTE | python3 pesquisar.py ese_holanda
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh ese_holanda
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh ese_holanda
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local ese_holanda <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

