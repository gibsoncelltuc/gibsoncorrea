# CRONOGRAMA - Poder e Fama EP 13 - Você Está Demitido

Gerado em 24/11 11:34 | 12 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_cidade | close | TRU | - | marco_trumptower | - | Duas palavras transformaram um empresário de Nova York numa estrela mu
b1 | simples | loc_pista | two | POV, POV | - | marco_trumptower, tv | - | Em dois mil e quatro, estreou nos Estados Unidos o programa O Aprendiz
b2 | simples | loc_cidade | crowd | TRU, CND | 16 | marco_trumptower | - | Dezesseis candidatos disputavam um emprego numa empresa de Donald Trum
b3 | simples | loc_pista | two | CND, POV | - | stall | - | Toda semana, as equipes faziam tarefas de negócios, como vender limona
b4 | simples | interior madeira | group | TRU, CND, POV, POV | - | Chair_1, Table_Large | - | A equipe perdedora ia para a sala de reunião, e alguém era eliminado.
b5 | simples | interior madeira | close | TRU | - | - | - | Acontece que o jeito de eliminar virou marca: apontando o dedo, ele di
b6 | chave | loc_pista | crowd | POV, POV, CND | 30 | marco_trumptower, tv, picket_fence | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | A final da primeira temporada teve cerca de vinte e oito milhões de es
b7 | simples | loc_pista | two | RAN, TRU | - | - | - | Bill Rancic venceu e ganhou um salário de duzentos e cinquenta mil dól
b8 | chave | loc_estudio | crowd | JUS, POV | 12 | marco_trumptower | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | No Brasil, O Aprendiz estreou no mesmo ano, com Roberto Justus.
b9 | simples | loc_estudio | two | TRU | - | tv | - | Trump apresentou por mais de dez anos, até dois mil e quinze.
b10 | simples | loc_cidade | close | TRU | - | tv | - | Um programa de emprego que acabou ficando famoso justamente por demiti
b11 | simples | loc_cidade | two | TRU | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (12/14 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | PENDENTE | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh aprendiz2004
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh aprendiz2004
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local aprendiz2004 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 6. Estilo e enquadramento

