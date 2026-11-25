# CRONOGRAMA - E Se EP 09 - E Se Você Cavasse um Buraco Até o Outro Lado da Terra?

Gerado em 25/11 17:09 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_campo | two | CAV, POV | - | globe | - | Um buraco até a China? Do Brasil, você sairia no meio do Pacífico.
b1 | simples | interior pedra | two | CAV, PRO | - | - | - | E o pulo nesse buraco nunca acabaria.
b2 | simples | loc_montanha | two | PRO, POV | - | scroll | - | O buraco mais fundo do mundo tem doze quilômetros, na Rússia.
b3 | chave | loc_montanha | wide | PRO, POV | - | scroll | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Lá embaixo, faz cento e oitenta graus.
b4 | simples | loc_campo | wide | PRO | 6 | globe | - | O centro da Terra fica a mais de seis mil quilômetros.
b5 | simples | loc_deserto | close | PRO | - | globe | - | E é quase tão quente quanto a superfície do Sol.
b6 | chave | loc_deserto | orbit | CAV | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que, se você pulasse, cairia cada vez mais rápido.
b7 | simples | loc_campo | two | PRO, POV | - | globe | - | Sairia do outro lado em uns quarenta minutos.
b8 | simples | loc_montanha | two | CAV, PRO | - | - | - | Mas, sem ninguém para segurar, cairia de volta. Para sempre.
b9 | simples | loc_campo | two | CAV, POV | - | globe | - | Para ir ao Japão, a passagem ainda é o melhor caminho.

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/10 itens) | PENDENTE | python3 pesquisar.py ese_buraco
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh ese_buraco
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh ese_buraco
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local ese_buraco <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

