# CRONOGRAMA - Poder e Fama EP 02 - O Cameo de Sete Segundos

Gerado em 25/11 17:31 | 9 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_cidade | two | FUN | - | tv | - | Sete segundos de um filme de Natal ainda geram briga até hoje.
b1 | transicao | loc_cidade | reveal | DIR, TRU | - | apartment, house_two, lamppost | - | E a culpa é de um hotel.
b2 | chave | interior pedra | two | FUN, TRU | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em Esqueceram de Mim 2, Kevin pede informação a um homem.
b3 | simples | interior pedra | group | FUN, TRU | - | - | - | O homem era Donald Trump, dono do hotel Plaza.
b4 | simples | interior loja | two | DIR, TRU | - | - | - | O diretor diz que a cena foi o preço do hotel.
b5 | simples | interior loja | group | TRU, DIR | - | - | - | Acontece que Trump nega: diz que foi a equipe que pediu.
b6 | simples | interior pedra | two | JOR, JOR2 | - | tv | - | Em 2019, uma TV canadense passou o filme sem a cena.
b7 | chave | loc_cidade | wide | JOR | 10 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | O corte virou polêmica no mundo inteiro.
b8 | simples | loc_cidade | two | FUN | - | tv | - | Um cameo virou briga política. E foi assim que...

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
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | PENDENTE | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh cameo1992
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh cameo1992
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local cameo1992 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 8. Storyboard e grade de acoes

