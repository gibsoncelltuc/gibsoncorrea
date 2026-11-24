# CRONOGRAMA - Guerras Inusitadas EP 10 - A Guerra da Chaleira

Gerado em 24/11 15:06 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | harbor | two | COZ, HOL | - | kettle, marco_viena | - | Uma guerra inteira teve um único tiro, e ele acertou uma chaleira de s
b1 | chave | harbor | crowd | HOL, HOL | 48 | marco_viena, navios de guerra ao fundo, no tamanho real | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Era mil setecentos e oitenta e quatro. A Holanda tinha fechado um rio,
b2 | simples | interior pedra | two | IMP, GEN | - | - | - | O imperador da Áustria ficou furioso. Ele queria o rio aberto para os 
b3 | simples | interior pedra | group | IMP, GEN | - | - | - | "Mandem três navios", ordenou ele. "Os holandeses não vão ter coragem 
b4 | simples | harbor | group | AUS, AUS | 14 | marco_viena, flagpole | - | Os três navios desceram o rio, com o maior na frente, cheio de soldado
b5 | chave | harbor | crowd | HOL, HOL | 48 | cannon, marco_viena, navios de guerra ao fundo, no tamanho real | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que um navio holandês estava esperando. Ele mirou, e deu um ú
b6 | simples | loc_campo | two | COZ, AUS | - | kettle | - | A bala atravessou o convés, e acertou em cheio a chaleira de sopa do c
b7 | simples | interior loja | group | GEN, AUS, COZ | - | kettle | - | O capitão austríaco olhou para a sopa derramada, e se rendeu na mesma 
b8 | simples | interior pedra | two | IMP, HOL | - | - | - | O imperador desistiu do rio. Em troca, a Holanda pagou uma indenização
b9 | simples | loc_campo | close | COZ | - | kettle | - | Ninguém morreu. Só o almoço.
b10 | simples | harbor | close | COZ | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (7/7 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 3) | PENDENTE | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh chaleira1784
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh chaleira1784
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local chaleira1784 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 4. Travas do roteiro

