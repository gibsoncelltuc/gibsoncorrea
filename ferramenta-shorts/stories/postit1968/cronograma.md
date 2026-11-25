# CRONOGRAMA - Curiosidade e Ciência EP 15 - A Cola que Não Colava

Gerado em 25/11 19:30 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | street | two | SIL, CHE | - | postit | - | Uma cola que falhou virou sucesso no mundo inteiro.
b1 | chave | street | wide | SIL, CHE | - | church, postit | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | E a ideia veio de alguém cantando na igreja.
b2 | simples | interior galpao | two | POV, SIL | - | - | - | Em 1968, Spencer Silver tentava criar uma super cola.
b3 | simples | interior madeira | two | SIL, CHE | - | - | - | Saiu o contrário: uma cola que grudava e soltava fácil.
b4 | simples | interior pedra | group | FRY, PAD, POV | - | - | - | Acontece que Art Fry cantava no coral da igreja.
b5 | simples | interior pedra | two | FRY, PAD | - | postit | - | E os papeizinhos do hinário viviam caindo.
b6 | chave | street | orbit | FRY | - | postit | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Ele pensou: marcadores com a cola fraca.
b7 | explicativa | loc_estudio | two | sem personagem | - | - | corpo: kit/postit (gira); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em  | O papel saiu amarelo por acaso: era o único que tinha.
b8 | simples | countryside | wide | SIL, CHE | 6 | postit | - | Em 1980, o post-it chegou às lojas.
b9 | simples | street | two | SIL, CHE | - | postit | - | A cola não colava direito. E foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (8/14 itens) | PENDENTE | python3 pesquisar.py postit1968
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | REFAZER (a etapa anterior mudou) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh postit1968
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh postit1968
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local postit1968 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

