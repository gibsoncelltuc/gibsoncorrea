# CRONOGRAMA - Guerras Inusitadas EP 19 - A Guerra de Aroostook

Gerado em 24/11 15:57 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | arctic | group | AME, CAN | - | logs, tree_pine | - | Uma guerra entre Estados Unidos e Inglaterra quase começou por causa d
b1 | simples | arctic | two | AME, CAN | - | - | - | Em mil oitocentos e trinta e oito, a fronteira entre o estado do Maine
b2 | simples | arctic | group | AME, CAN | - | logs, bush, tree_oak, tree_pine | - | Na mata de Aroostook, lenhadores dos dois lados cortavam as mesmas árv
b3 | chave | arctic | wide | AME | 12 | tree_pine | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em fevereiro de mil oitocentos e trinta e nove, o Maine mandou o agent
b4 | simples | arctic | wide | MIL, ING | 48 | - | - | O Maine chamou milhares de soldados da milícia, e a colônia inglesa ma
b5 | simples | interior pedra | two | AME, CAN | - | prison | - | Nessa confusão, lenhadores de New Brunswick prenderam o agente do Main
b6 | simples | interior madeira | two | GEN, MIL | - | - | - | Mas ninguém queria uma guerra de verdade, então o presidente americano
b7 | simples | interior madeira | group | GEN, PRE | - | - | - | Ele ajudou os dois lados a firmar uma trégua, e as tropas nunca chegar
b8 | simples | interior pedra | two | PRE, PRE | - | scroll | - | Em mil oitocentos e quarenta e dois, o Tratado Webster-Ashburton defin
b9 | simples | interior loja | two | AME, AME | - | logs | - | Ficou conhecida até como a Guerra do Porco com Feijão.
b10 | simples | interior loja | close | AME | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (11/11 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh aroostook1838
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh aroostook1838
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local aroostook1838 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

