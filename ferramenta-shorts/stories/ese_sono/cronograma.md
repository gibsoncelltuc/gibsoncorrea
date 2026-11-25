# CRONOGRAMA - E Se EP 05 - E Se Ninguém Precisasse Dormir?

Gerado em 25/11 17:11 | 9 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | street | two | PRO, POV | - | kettle | - | E se ninguém precisasse dormir? Você ganharia 25 anos acordado.
b1 | chave | loc_pista | crowd | POV, POV, RAN | 18 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Mas o preço disso aparece em poucos dias.
b2 | chave | loc_pista | orbit | POV, POV, POV | 22 | apartment, house_two, lamppost | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Cidades funcionariam vinte e quatro horas por dia.
b3 | simples | loc_patio | two | POV, POV | - | ball | - | Daria para aprender três línguas e ver todas as séries.
b4 | simples | street | group | POV, POV | - | - | - | Em 1964, um estudante americano resolveu testar.
b5 | simples | interior madeira | two | RAN, PRO | - | - | - | Randy Gardner ficou onze dias seguidos acordado.
b6 | simples | interior galpao | close | RAN | - | - | - | Acontece que ele esquecia palavras e via coisas que não existiam.
b7 | simples | interior loja | two | PRO, POV | - | - | - | Dormindo, o cérebro faz uma faxina do que acumulou no dia.
b8 | simples | street | two | PRO, POV | - | kettle | - | Se você está vendo isso de madrugada, vai dormir.

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/11 itens) | PENDENTE | python3 pesquisar.py ese_sono
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh ese_sono
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh ese_sono
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local ese_sono <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

