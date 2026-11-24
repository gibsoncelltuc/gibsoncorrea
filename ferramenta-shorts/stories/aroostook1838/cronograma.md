# CRONOGRAMA - Guerras Inusitadas EP 19 - A Guerra de Aroostook

Gerado em 24/11 03:01 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_campo | two | AME, CAN | - | logs, tree_pine | - | Uma guerra entre os Estados Unidos e a Inglaterra foi travada por lenh
b1 | transicao | loc_campo | reveal | AME, CAN | 8 | - | - | Em mil oitocentos e trinta e oito, a fronteira entre o estado do Maine
b2 | simples | loc_campo | two | AME, CAN | - | logs, Axe_Bronze, bush, tree_oak, tree_pine | - | Na mata de Aroostook, lenhadores americanos e ingleses cortavam as mes
b3 | chave | loc_campo | crowd | AME, CAN | 16 | tree_pine | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | "Essa árvore é minha!", gritou um lenhador, e logo os dois lados começ
b4 | chave | loc_montanha | orbit | MIL, ING | 48 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | O Maine chamou milhares de soldados, e a Inglaterra mandou os seus.
b5 | simples | interior pedra | two | AME, ING | - | prison | - | Acontece que um agente do Maine foi preso pelos ingleses, e o clima fi
b6 | simples | loc_montanha | two | GEN, MIL | - | - | - | Mas ninguém queria uma guerra de verdade, então o governo mandou um ge
b7 | simples | interior madeira | two | GEN, PRE | - | - | - | Ele convenceu os dois lados a parar, e a história terminou sem um únic
b8 | simples | interior pedra | two | PRE, PRE | - | scroll | - | Alguns anos depois, as duas nações assinaram um tratado que dividiu o 
b9 | simples | loc_campo | group | AME, AME | - | logs, tree_pine | - | Chamaram de Guerra do Porco com Feijão, porque era só isso que as trop
b10 | simples | loc_campo | close | AME | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/5 itens) | PENDENTE | python3 pesquisar.py aroostook1838
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 3) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh aroostook1838
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh aroostook1838
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local aroostook1838 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

