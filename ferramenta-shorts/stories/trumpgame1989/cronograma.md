# CRONOGRAMA - Poder e Fama EP 18 - O Jogo de Tabuleiro do Trump

Gerado em 24/11 23:46 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_cidade | two | TRU, EXE | - | boardgame, marco_liberdade | - | Donald Trump lançou um jogo de tabuleiro com o próprio rosto no dinhei
b1 | chave | loc_cidade | wide | POV, POV | 6 | marco_liberdade | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Era mil novecentos e oitenta e nove, e ele era um empresário famoso de
b2 | simples | interior loja | two | EXE, TRU | - | boardgame | - | Uma fábrica de brinquedos fez o jogo: comprar prédios, cassinos e hoté
b3 | simples | interior loja | close | TRU | - | boardgame | - | As notas eram de dez, cinquenta e cem milhões de dólares, com a cara d
b4 | simples | interior madeira | two | PAI, FIL | - | boardgame | - | Acontece que o manual era longo, e as famílias abriam a caixa e não en
b5 | simples | interior pedra | two | EXE, EXE | - | - | - | A fábrica esperava vender dois milhões de jogos, e vendeu oitocentos m
b6 | transicao | loc_pista | orbit | TRU, EXE | 6 | boardgame | - | Em dois mil e quatro, Trump virou estrela do programa O Aprendiz.
b7 | chave | loc_cidade | crowd | TRU, POV, POV | - | boardgame, marco_liberdade | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | E o jogo voltou às lojas, com regras mais simples e a frase do program
b8 | simples | loc_pista | two | TRU | - | boardgame | - | Um jogo sobre ficar bilionário, que virou curiosidade.
b9 | simples | loc_cidade | close | TRU | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (4/12 itens) | PENDENTE | python3 pesquisar.py trumpgame1989
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh trumpgame1989
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh trumpgame1989
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local trumpgame1989 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

