# CRONOGRAMA - Poder e Fama EP 13 - Você Está Demitido

Gerado em 25/11 17:18 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_cidade | close | TRU | - | marco_trumptower | - | O que ninguém lembra: duas palavras deixaram Trump famoso no mundo tod
b1 | simples | interior madeira | close | TRU | - | tv | - | E não foi na política. Foi num programa de TV.
b2 | simples | loc_pista | two | POV, POV | - | marco_trumptower, tv | - | Em 2004, estreou nos Estados Unidos o programa O Aprendiz.
b3 | chave | loc_cidade | crowd | TRU, CND | 16 | marco_trumptower | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Dezesseis candidatos disputavam um emprego na empresa de Trump.
b4 | simples | interior madeira | group | TRU, CND, POV, POV | - | Chair_1, Table_Large | - | Toda semana, a equipe perdedora ia para a sala de reunião.
b5 | simples | interior madeira | close | TRU | - | - | - | E alguém ouvia, com o dedo na cara: você está demitido.
b6 | chave | loc_pista | crowd | POV, POV, CND | 30 | marco_trumptower, tv, picket_fence | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | A final teve cerca de vinte e oito milhões de espectadores.
b7 | simples | loc_estudio | two | JUS, POV | - | marco_trumptower | - | No Brasil, O Aprendiz estreou no mesmo ano, com Roberto Justus.
b8 | simples | loc_estudio | close | TRU | - | tv | - | Trump apresentou o programa por mais de dez anos.
b9 | simples | loc_cidade | close | TRU | - | - | - | Um programa de emprego, famoso por demitir. Tudo por causa de duas pal

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (12/14 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | PENDENTE | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh aprendiz2004
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh aprendiz2004
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local aprendiz2004 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | REFAZER (a etapa anterior mudou) | 

**Etapa atual:** 8. Storyboard e grade de acoes

