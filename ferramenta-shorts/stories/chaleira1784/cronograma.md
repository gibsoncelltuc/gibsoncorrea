# CRONOGRAMA - Guerras Inusitadas EP 10 - A Guerra da Chaleira

Gerado em 25/11 16:44 | 9 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_campo | two | COZ, HOL | - | kettle | - | Uma guerra inteira teve um único tiro. E acertou uma chaleira.
b1 | simples | interior madeira | two | IMP, COZ | - | kettle | - | E aquela chaleira estava cheia de sopa quente.
b2 | transicao | harbor | wide | MAR, MAR | - | navio_fragata | - | Em 1784, a Holanda mantinha o rio Escalda fechado.
b3 | simples | interior pedra | two | IMP, GEN | - | - | - | O imperador José Segundo, da Áustria, queria o rio aberto.
b4 | simples | harbor | wide | IMP | - | navio_fragata, navios de guerra ao fundo, no tamanho real | - | Ele mandou três navios descerem o rio, achando que ninguém reagiria.
b5 | simples | harbor | group | MAR, MAR | - | cannon, navio_fragata | - | Acontece que o navio holandês Dolfijn esperava e disparou um tiro.
b6 | chave | interior madeira | two | IMP, COZ | - | kettle | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | A bala destruiu uma chaleira de sopa no convés.
b7 | chave | harbor | group | GEN | - | navio_fragata | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | O navio austríaco se rendeu na hora, sem mais tiros.
b8 | simples | loc_campo | two | COZ, HOL | - | - | - | O único prejuízo do dia foi o almoço.

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/16 itens) | PENDENTE | python3 pesquisar.py chaleira1784
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh chaleira1784
10 | Render | todos os quadros renderizados nesta versao das folhas | REFAZER (a etapa anterior mudou) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | REFAZER (a etapa anterior mudou) | ./conferir.sh chaleira1784
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local chaleira1784 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | REFAZER (a etapa anterior mudou) | 

**Etapa atual:** 2. Pesquisa de campo

