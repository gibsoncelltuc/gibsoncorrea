# CRONOGRAMA - Curiosidade e Ciência EP 02 - Arquimedes e o Eureca

Gerado em 25/11 16:41 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | medieval | track | ARQ, POV | - | bathtub | - | Ninguém te conta: um gênio correu da banheira gritando pela rua.
b1 | simples | medieval | two | REI, OUR | - | bathtub | - | E foi a banheira que desmascarou um ladrão de ouro.
b2 | transicao | medieval | reveal | POV, POV | 8 | bathtub | - | Siracusa, na Sicília, há mais de dois mil anos.
b3 | simples | interior pedra | two | REI, OUR | - | coroa_louros | - | O rei Hierão desconfiou que sua coroa de ouro tinha prata.
b4 | simples | interior pedra | group | REI, ARQ | - | coroa_louros | - | Ele pediu a Arquimedes a verdade, sem estragar a coroa.
b5 | chave | interior pedra | two | ARQ | - | bathtub | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que, ao entrar na banheira, a água transbordou.
b6 | explicativa | interior madeira | two | sem personagem | - | - | corpo: kit/bathtub (parado); emissao: onda; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em cada entr | A água que sai tem o tamanho do corpo que entra.
b7 | explicativa | interior madeira | two | sem personagem | - | - | corpo: kit/coroa_louros (parado); emissao: onda; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em cada | Coroa com prata é maior e derrama mais água que ouro puro.
b8 | chave | medieval | crowd | ARQ, POV | 14 | coroa_louros | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Conta a lenda: ele gritou Eureca. E a coroa tinha prata.
b9 | simples | medieval | two | ARQ, POV | - | bathtub | - | Dá para enganar muita gente. Mas não uma banheira.

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (10/15 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | PENDENTE | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | REFAZER (a etapa anterior mudou) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | REFAZER (a etapa anterior mudou) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh arquimedes250
10 | Render | todos os quadros renderizados nesta versao das folhas | REFAZER (a etapa anterior mudou) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | REFAZER (a etapa anterior mudou) | ./conferir.sh arquimedes250
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local arquimedes250 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | REFAZER (a etapa anterior mudou) | 

**Etapa atual:** 4. Travas do roteiro

