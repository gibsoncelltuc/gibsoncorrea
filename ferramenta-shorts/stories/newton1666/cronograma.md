# CRONOGRAMA - Curiosidade e Ciência EP 01 - Newton e a Maçã

Gerado em 25/11 16:54 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_campo | group | NEW | - | apple, lua_ceu | - | A maçã não caiu na cabeça de Newton. E mesmo assim mudou tudo.
b1 | simples | loc_campo | reveal | NEW | 8 | apple | - | Ela explicou por que a Lua não cai na nossa cabeça.
b2 | simples | street | two | EST | 10 | - | - | Em 1666, a peste fechou a universidade de Cambridge.
b3 | simples | countryside | two | NEW, MAE | - | barn, haybale, picket_fence, scarecrow | - | Isaac Newton, de 23 anos, voltou para a fazenda da mãe.
b4 | simples | countryside | wide | NEW, AMI | 6 | apple, tree_oak | - | Passava os dias debaixo de uma macieira, pensando.
b5 | chave | countryside | two | NEW, AMI | - | apple, tree_oak | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que uma maçã caiu bem na frente dele.
b6 | simples | countryside | close | NEW | - | apple, tree_oak | - | Ele se perguntou: por que ela cai sempre para baixo?
b7 | explicativa | loc_campo | two | sem personagem | - | lua_ceu | corpo: kit/lua_ceu (parado); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som  | Se a força puxa a maçã, será que puxa a Lua também?
b8 | chave | interior madeira | two | NEW | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Virou a lei da gravidade, publicada em 1687.
b9 | simples | loc_campo | group | NEW | - | apple, lua_ceu | - | A maçã ficou famosa. E nem foi comida.

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (12/14 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | PENDENTE | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh newton1666
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh newton1666
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local newton1666 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 7. Gates

